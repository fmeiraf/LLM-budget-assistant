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
MAX_TOKENS = 3800


class TokenValidator:
    def __init__(
        self, model: str, base_prompt: str, max_tokens_threshold: int = MAX_TOKENS
    ):
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
        self.max_transaction_input_tokens = int(
            (self.max_tokens_threshold / 2) - self.base_prompt_tokens
        )

        self.initial_set_up_done = True

    def calculate_expected_final_tokens(self, transaction_input_tokens: int) -> int:
        if not self.initial_set_up_done:
            self.set_up_initial_counts()

        return (self.base_prompt_tokens + transaction_input_tokens) * 2

    def split_tokens(self, transaction_input: str):
        if not self.initial_set_up_done:
            self.set_up_initial_counts()
        transaction_input_token_count = self.get_token_count(transaction_input)

        ## There area 2 base information that matters here
        # The amount of tokens available based on prompt + transaction input size
        # The amount that could be used for the transaction input

        # in our case the prompt consists of guardrails support prompt + transaction input
        # once transaction input is what will be parsed for final result we could expect that at max
        # we would get 2x the transaction input tokens + prompt
        max_available_tokens = int(
            self.max_tokens_threshold
            - ((transaction_input_token_count + self.base_prompt_tokens) * 2)
        )

        # when the input is less than the max tokens threshold
        if max_available_tokens >= 0:
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
                token_per_transaction_cumsum > self.max_transaction_input_tokens
            )[0][0]

            # slip the transactions in [left, right] format

            left_transaction_string = "\n".join(transactions[: max_token_index - 1])
            right_transaction_string = "\t\t\n".join(transactions[max_token_index:])

            self.result.append(
                (
                    left_transaction_string,
                    self.calculate_expected_final_tokens(
                        self.max_transaction_input_tokens
                    ),
                )
            )
            # split the remaining tokens

            self.split_tokens(right_transaction_string)

    def process(self, input: str) -> list[tuple[str, int]]:
        self.split_tokens(input)
        return self.result


if __name__ == "__main__":
    from rich import print as rprint

    # with open("./app/test_data/test_data_no_header.txt", "r") as f:
    #     test_input = f.read()

    test_input = """Jul 22, 2023	AMZ*Sleepsheep Direct		$141.75	$4,838.90
Jul 22, 2023	FIVE GUYS BURGERS & FR	$71.12		$4,980.65
Jul 22, 2023	ABC*ANYTIME FITNESS	$28.34		$4,909.53
Jul 21, 2023	RING MULTICAM MTH PLAN	$15.75		$4,881.19
Jul 19, 2023	DOORDASH*LUNA MEXICAN	$130.82		$4,865.44
Jul 15, 2023	AMZN Mktp CA*F307K57V3	$39.86		$4,315.77
Jul 14, 2023	AMZN Mktp CA*WV57D4SK3	$33.59		$4,275.91
Jul 13, 2023	adidas 2021 Edmonton	$90.32		$3,242.59
Jul 12, 2023	NIKE CANADA - EDMONTON	$580.71		$3,152.27
Jul 12, 2023	GAP OUTLET CA 8893	$172.73		$2,571.56
Jul 10, 2023	APPLE STORE #R411	$10.00		$2,398.83"""

    guard = gd.Guard.from_rail_string(rail_str)
    tv = TokenValidator(model=MODEL, base_prompt=guard.base_prompt)

    # rprint(tv.split_transactions(test_input))

    # rprint(tv.split_transactions(test_input))

    rprint(tv.process(test_input))
