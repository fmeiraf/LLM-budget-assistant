import os
from dotenv import load_dotenv
from transaction_parser import parse_transactions


from database import Database

load_dotenv()

# Getting the transaction list:

# loading test data
with open("app/test_data/test_data.txt", "r") as f:
    test_data = f.read()

# parsing test data
parsed_test_data = parse_transactions(test_data)


# Adding info to the tables:

db_config = {
    "host": "localhost",  # running on docker locally
    "port": "5432",
    "database": "llm_finance",
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD"),
}

db = Database(**db_config)

# Usage example
user_id = db.create_user("example@example.com", "password123")
card_id = db.create_credit_card(user_id, "1234", "My Card")
category_id = db.create_category(user_id, "Groceries")
transactions = [
    {
        "transaction_date": "2023-05-01",
        "transaction_description": "Grocery store",
        "credit": 0.00,
        "debit": 50.00,
        "card_id": card_id,
        "category_id": category_id,
    },
    {
        "transaction_date": "2023-05-05",
        "transaction_description": "Gas station",
        "credit": 0.00,
        "debit": 30.00,
        "card_id": card_id,
        "category_id": category_id,
    },
]
db.create_transactions(user_id, transactions)

# Close the database connection
db.connection.close()
