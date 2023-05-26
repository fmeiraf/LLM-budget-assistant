import dotenv
from transaction_parser import parse_transactions

# loading test data
with open("app/test_data/test_data.txt", "r") as f:
    test_data = f.read()


# parsing test data
parsed_test_data = parse_transactions(test_data)

print(parsed_test_data)

# dotenv.load_dotenv(dotenv.find_dotenv())

# guard = gd.Guard.from_rail_string(rail_str)
# openai.api_key = os.getenv("OPENAI_API_KEY")

# print(openai.api_key)

# raw_llm_response, validated_response = guard(
#     openai.Completion.create,
#     prompt_params={"transaction_string": test_data},
#     engine="text-davinci-003",
#     max_tokens=2500,
#     temperature=0.0,
# )

# print(validated_response)
