import tiktoken
import dotenv
import os
from guardrails_specs.specs import rail_str
import guardrails as gd


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

    def set_up_initial_counts(self):
        # getting base propmpt token counts for future use
        self.base_prompt_tokens = self.get_token_count(self.base_prompt)

        # getting max transactions tokens for future use``
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
        transaction_input_tokens = self.encode(transaction_input)

        print("max_tokens_threshold", self.max_transactions_tokens)
        print("initial_count", transaction_input_token_count)

        # when the input is less than the max tokens threshold
        if transaction_input_token_count <= self.max_transactions_tokens:
            self.result.append(
                (
                    transaction_input,
                    self.calculate_expected_final_tokens(transaction_input_token_count),
                )
            )
        else:
            # truncat the input to the max tokens threshold
            self.result.append(
                (
                    self.decode(
                        transaction_input_tokens[: self.max_transactions_tokens]
                    ),
                    self.calculate_expected_final_tokens(self.max_transactions_tokens),
                )
            )
            # split the remaining tokens
            print(
                "split_count",
                len(transaction_input_tokens[self.max_transactions_tokens :]),
            )

            self.split_tokens(
                transaction_input=self.decode(
                    transaction_input_tokens[self.max_transactions_tokens :]
                )
            )

    def process(self, input: str) -> list[tuple[str, int]]:
        self.split_tokens(input)
        return self.result


if __name__ == "__main__":
    with open("./app/test_data/long_transaction.txt", "r") as f:
        test_input = f.read()

    guard = gd.Guard.from_rail_string(rail_str)
    tv = TokenValidator(model=MODEL, base_prompt=guard.base_prompt)

    from rich import print as rprint

    rprint(tv.process(test_input))
