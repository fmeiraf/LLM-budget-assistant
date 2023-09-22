import tiktoken
import dotenv
import os
from guardrails_specs.specs import rail_str
import guardrails as gd
import re
import numpy as np
from rich import print as rprint

dotenv.load_dotenv()

MODEL = os.getenv("OPENAI_MODEL_NAME")
MAX_TOKENS = 2000


class TokenValidator:
    def __init__(self, model: str, base_prompt: str, max_tokens_threshold: int = 3000):
        self.model = model
        self.max_tokens_threshold = max_tokens_threshold
        self.base_prompt = base_prompt
        self.encoder = tiktoken.encoding_for_model(self.model)
        self.base_prompt_tokens = 0
        self.max_transactions_tokens = 0
        self.initial_set_up_done = False
        self.result = []

    def encode(self, input: str) -> list[int]:
        return self.encoder.encode(input)

    def decode(self, tokens: list[int]) -> str:
        return self.encoder.decode(tokens)

    def get_token_count(self, input: str) -> int:
        return len(self.encode(input))

    def split_transactions(self, input_string):
        # Detect the string format
        if "\t\t\n" in input_string:  # string1 format (RBC)
            transactions = re.split(
                r"\t\t\n|\n\n", input_string  # .strip()
            )  # Split on extra newlines or \t\t\n for transactions

        else:  # string2 format (TD Bank)
            transactions = re.split(
                r"\n", input_string  # .strip()
            )  # Split on newline for transactions

        # checking if the transactions lines are empty strings or  pieces of non-transactional information
        transactions = [t for t in transactions if len(re.split(r"\n|\t", t)) > 2]

        return transactions

    def set_up_initial_counts(self):
        # getting base propmpt token counts for future use
        self.base_prompt_tokens = self.get_token_count(self.base_prompt)

        # getting max transactions tokens for future use
        self.max_transactions_tokens = int(
            (self.max_tokens_threshold - (2 * self.base_prompt_tokens)) / 3
        )

        self.initial_set_up_done = True

    def calculate_expected_final_tokens(self, transaction_input_tokens: int) -> int:
        if not self.initial_set_up_done:
            self.set_up_initial_counts()

        return (
            (self.base_prompt_tokens + transaction_input_tokens) * 2
        ) + transaction_input_tokens

    def split_tokens(self, transaction_input: str):
        if not self.initial_set_up_done:
            self.set_up_initial_counts()
        transaction_input_token_count = self.get_token_count(transaction_input)
        # transaction_input_tokens = self.encode(transaction_input)

        # when the input is less than the max tokens threshold
        if transaction_input_token_count <= self.max_transactions_tokens:
            self.result.append(
                (
                    transaction_input,
                    self.calculate_expected_final_tokens(transaction_input_token_count),
                )
            )
        else:
            # Separate input per transaction and calculate token count for each
            transactions = self.split_transactions(transaction_input)

            # get the most amount of transactions that can fit in the max tokens threshold
            token_per_transaction = [self.get_token_count(t) for t in transactions]

            # getting the cumulative sum of the token count per transaction
            token_per_transaction_cumsum = np.cumsum(token_per_transaction)

            max_token_index = np.argwhere(
                token_per_transaction_cumsum > self.max_transactions_tokens
            )[0][0]

            # slip the transactions in [left, right] format

            left_transaction_string = "\n".join(transactions[: max_token_index - 1])
            right_transaction_string = "\t\t\n".join(transactions[max_token_index:])

            self.result.append(
                (
                    left_transaction_string,
                    self.calculate_expected_final_tokens(self.max_transactions_tokens),
                )
            )
            # split the remaining tokens

            self.split_tokens(right_transaction_string)

    def process(self, input: str) -> list[tuple[str, int]]:
        self.split_tokens(input)
        return self.result


if __name__ == "__main__":
    from rich import print as rprint

    with open("./app/test_data/long_transaction_td.txt", "r") as f:
        test_input = f.read()

    guard = gd.Guard.from_rail_string(rail_str)
    tv = TokenValidator(model=MODEL, base_prompt=guard.base_prompt)

    # rprint(tv.split_transactions(test_input))

    rprint(tv.process(test_input))
