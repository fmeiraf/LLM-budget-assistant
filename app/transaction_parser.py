# import tiktoken
import dotenv
import guardrails as gd
import openai
from guardrails_specs.specs import rail_str
import tiktoken
import os

dotenv.load_dotenv()

model = "text-davinci-003"
enc = tiktoken.encoding_for_model(model)


def parse_transactions(transaction_string: str):
    guard = gd.Guard.from_rail_string(rail_str)
    formatted_prompt = guard.prompt.format(
        **{"transaction_string": transaction_string}
    ).source
    openai.api_key = os.getenv("OPENAI_API_KEY")

    max_tokens_calculated = 4096 - (2 * len(enc.encode(formatted_prompt)))

    print(max_tokens_calculated)

    raw_llm_response, validated_response = guard(
        openai.Completion.create,
        prompt_params={"transaction_string": transaction_string},
        engine=model,
        max_tokens=max_tokens_calculated,
        temperature=0.0,
    )

    if validated_response is None:
        raise ValueError("LLM answer does not evaluate into valid object")

    return validated_response
