import dotenv
import guardrails as gd
import openai
from guardrails_specs.specs import rail_str
from token_validator import TokenValidator
from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

from rich import print as rprint

import os


dotenv.load_dotenv()
OPEN_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL = os.getenv("OPENAI_MODEL_NAME")
MAX_TOKENS = 2000


class TransactionParser:
    def __init__(self, transaction_string: str):
        self.transaction_string = transaction_string
        self.parsed_transactions = None
        self.llm = None

    def start_llm(self):
        self.llm = OpenAI(temperature=0)

    def extract_transaction_info(self):
        guard = gd.Guard.from_rail_string(rail_str)
        openai.api_key = OPEN_API_KEY

        token_validator = TokenValidator(
            model=MODEL, base_prompt=guard.base_prompt, max_tokens_threshold=MAX_TOKENS
        )

        split_input = token_validator.process(input=self.transaction_string)

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
                rprint(string)
                raise ValueError("LLM answer does not evaluate into valid object")

            for transaction in validated_response["transaction_list"]:
                parsed_transactions.append(transaction)

        rprint(parsed_transactions)
        self.parsed_transactions = parsed_transactions

        return parsed_transactions

    def categorize_transactions(self, transaction_description: str):
        template = """
        You are an expert in assigning categories to a transaction. 
        Be very brief and try to use the least amount of words to the categories you create as possible.
        It's very important that if you can't identify a category you assign "N/A" to it.

        An example of how important it's to be brief:

        example_description: Netflix Super PRemium ultra mega plan
        category: Entertainment

        You will be given the transaction description within triple backticks.


        Your transaction is: ```{transaction_description}```

        Return your answer as string.
        """

        if self.llm is None:
            self.start_llm()

        llm_chain = LLMChain(
            llm=self.llm, prompt=PromptTemplate.from_template(template)
        )

        return llm_chain(transaction_description)["text"].strip()

    def parse_transactions(self):
        if self.parsed_transactions is None:
            self.extract_transaction_info()

        categorized_transactions = []
        for transaction in self.parsed_transactions:
            # filtering possible obj format for transactions due to LLM randomnes
            if (
                transaction.get("transaction_info", {}).get("transaction_description")
                is not None
            ):
                """format {transaction_info: {transaction_description: 'description'}, ...}"""
                new_transacion_obj = {**transaction["transaction_info"]}
            # Check for format B
            elif transaction.get("transaction_description") is not None:
                """format {transaction_description: 'description', ...}"""
                new_transacion_obj = {**transaction}
            else:
                raise ValueError("Invalid transaction format")
            # if
            # new_transacion_obj = {**transaction}  # {**transaction["transaction_info"]}
            try:
                new_transacion_obj["category"] = self.categorize_transactions(
                    new_transacion_obj["transaction_description"]
                )
            except KeyError as e:
                rprint(e)
                rprint(transaction)

            # new_transacion_obj["category"] = self.categorize_transactions(
            #     new_transacion_obj["transaction_description"]
            # )
            categorized_transactions.append(new_transacion_obj)

        return categorized_transactions
