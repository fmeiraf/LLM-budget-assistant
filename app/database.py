from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    ForeignKey,
    Float,
    MetaData,
    Date,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.orm import DeclarativeBase

from datetime import datetime

import os
from dotenv import load_dotenv

load_dotenv()

# Create the database engine
db_config = {
    "host": "localhost",  # running on docker locally
    "port": "5432",
    "database": "llm_finance",
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD"),
}


# Base = declarative_base()
metadata_obj = MetaData(schema="llm_finances")


class Base(DeclarativeBase):
    metadata = metadata_obj


class User(Base):
    __tablename__ = "users"
    # __table_args__ = {"schema": "llm_finances"}

    user_id = Column(Integer, primary_key=True)
    email = Column(String)
    password = Column(String)
    accounts = relationship("Account", backref="users")
    categories = relationship("Category", backref="users")
    transactions = relationship("Transaction", backref="users")


class Account(Base):
    __tablename__ = "accounts"
    # __table_args__ = {"schema": "llm_finances"}

    account_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    account_last_4_digits = Column(String(4))
    account_name = Column(String)
    user = relationship("User", backref="user_accounts")


class Category(Base):
    __tablename__ = "categories"
    # __table_args__ = {"schema": "llm_finances"}

    category_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    category_name = Column(String)
    user = relationship("User", backref="user_categories")


class Transaction(Base):
    __tablename__ = "transactions"
    # __table_args__ = {"schema": "llm_finances"}

    transaction_id = Column(Integer, primary_key=True)
    transaction_date = Column(Date)
    transaction_description = Column(String)
    credit = Column(Float)
    debit = Column(Float)
    account_id = Column(Integer, ForeignKey("accounts.account_id"))
    category_id = Column(Integer, ForeignKey("categories.category_id"))
    user_id = Column(Integer, ForeignKey("users.user_id"))
    user = relationship("User", backref="user_transactions")


class Database:
    def __init__(self, host: str, port: str, database: str, user: str, password: str):
        self.engine = create_engine(
            f"postgresql://{user}:{password}@{host}:{port}/{database}",
            echo=True,  # Set to False to disable SQL query logging
        )
        self.Session = sessionmaker(bind=self.engine)

    def get_user_id_by_email(self, email: str):
        session = self.Session()
        user = session.query(User).filter_by(email=email).first()
        session.close()
        if user:
            return user.user_id
        else:
            return None

    def create_user(self, email: str, password: str):
        session = self.Session()
        user = User(email=email, password=password)
        session.add(user)
        session.commit()
        user_id = user.user_id
        session.close()
        return user_id

    def get_account_id_by_name(self, user_id: int, account_name: str):
        session = self.Session()
        account = (
            session.query(Account)
            .filter_by(user_id=user_id, account_name=account_name)
            .first()
        )
        session.close()
        if account:
            return account.account_id
        else:
            return None

    def create_account(
        self,
        user_id: int,
        account_name: str,
        account_last_4_digits: str = "0000",
    ):
        if len(account_last_4_digits) != 4 or not account_last_4_digits.isdigit():
            raise ValueError(
                "account_last_4_digits must be 4 digits long and contain only numbers"
            )

        session = self.Session()
        account = Account(
            user_id=user_id,
            account_last_4_digits=account_last_4_digits,
            account_name=account_name,
        )
        session.add(account)
        session.commit()
        account_id = account.account_id
        session.close()
        return account_id

    def get_all_categories_by_user_id(self, user_id: int):
        session = self.Session()
        categories = [
            category.category_name
            for category in session.query(Category)
            .filter_by(user_id=user_id)
            .order_by("category_name")
        ]
        session.close()
        return categories

    def create_category(self, user_id: int, category_name: str):
        session = self.Session()
        category = Category(user_id=user_id, category_name=category_name)
        session.add(category)
        session.commit()
        category_id = category.category_id
        session.close()
        return category_id

    def create_transactions(self, user_id: int, transactions: list):
        session = self.Session()
        for transaction in transactions:
            transaction_obj = Transaction(
                transaction_date=transaction["transaction_date"],
                transaction_description=transaction["transaction_description"],
                credit=transaction["credit"],
                debit=transaction["debit"],
                account_id=transaction["account_id"],
                category_id=transaction["category_id"],
                user_id=user_id,
            )
            session.add(transaction_obj)
        session.commit()
        session.close()

    # add function for log in
    def log_in(self, email: str, password: str):
        session = self.Session()
        user = session.query(User).filter_by(email=email).first()
        session.close()
        if user:
            if user and user.password == password:
                return True
            else:
                return None
        else:
            return None


## Test

# Populate the database with some test data
# Import the necessary libraries and classes


# Create an instance of the Database class with your PostgreSQL credentials
def populate_test_db():
    db = Database(**db_config)

    # Test data for creating a user
    email = "test@example.com"
    password = "testpassword"

    # Test data for creating an account
    card_last_4_digits = "1234"
    account_name = "Test Card"

    # Test data for creating a category
    category_name = "Test Category"

    # Test data for creating transactions
    transactions = [
        {
            "transaction_date": datetime.now(),
            "transaction_description": "Transaction 1",
            "credit": 100,
            "debit": 0,
            "account_id": None,  # Replace with the appropriate card ID
            "category_id": None,  # Replace with the appropriate category ID
        },
        {
            "transaction_date": datetime.now(),
            "transaction_description": "Transaction 2",
            "credit": 0,
            "debit": 50,
            "account_id": None,  # Replace with the appropriate card ID
            "category_id": None,  # Replace with the appropriate category ID
        },
    ]

    # Query all users
    # users = db.get_all_users()
    # for user in users:
    #     print(user.user_id, user.email, user.password)

    # Create a user and retrieve the user ID
    user_id = db.create_user(email, password)

    # Create an account for the user and retrieve the card ID
    account_id = db.create_account(
        user_id=user_id,
        account_last_4_digits=card_last_4_digits,
        account_name=account_name,
    )

    # Create a category for the user and retrieve the category ID
    category_id = db.create_category(user_id, category_name)

    # Update the transactions with the card ID and category ID
    for transaction in transactions:
        transaction["account_id"] = account_id
        transaction["category_id"] = category_id

    # Create the transactions for the user
    db.create_transactions(user_id, transactions)

    # Close the database connection

    print("Test records have been inserted successfully.")


def test_email_retriver():
    db = Database(**db_config)
    email = "test@example.com"
    user_id = db.get_user_id_by_email(email)

    if user_id:
        print(f"User ID for {email} is {user_id}")
    else:
        print(f"No user found with email {email}")


if __name__ == "__main__":
    populate_test_db()
    test_email_retriver()


# %%
"1234".isdigit()

# %%
