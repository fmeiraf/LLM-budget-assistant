import dotenv
import guardrails as gd
import openai
from guardrails_specs.specs import rail_str
from token_validator import TokenValidator
import os

dotenv.load_dotenv()
OPEN_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL = os.getenv("OPENAI_MODEL_NAME")
MAX_TOKENS = 2000


def parse_transactions(transaction_string: str):
    guard = gd.Guard.from_rail_string(rail_str)
    openai.api_key = OPEN_API_KEY

    token_validator = TokenValidator(model=MODEL)

    split_input = token_validator.validate_input(
        inputs=[transaction_string],
        base_prompt=guard.base_prompt,
        max_tokens_threshold=MAX_TOKENS,
    )

    parsed_transactions = []
    for input in split_input:
        string, token_number = input

        _, validated_response = guard(
            openai.Completion.create,
            prompt_params={"transaction_string": string},
            engine=MODEL,
            max_tokens=token_number,
            temperature=0.0,
        )

        if validated_response is None:
            raise ValueError("LLM answer does not evaluate into valid object")

        parsed_transactions.append(validated_response)

    return parsed_transactions
