import psycopg2

# create database class to handle all database interactions


class Database:
    def __init__(self, host: str, port: str, database: str, user: str, password: str):
        self.connection = psycopg2.connect(
            host=host,
            port=port,
            database=database,
            user=user,
            password=password,
        )

    def create_user(self, email: str, password: str):
        with self.connection:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO llm_finances.users (email, password) VALUES (%s, %s) RETURNING user_id;",
                    (email, password),
                )
                user_id = cursor.fetchone()[0]
                return user_id

    def create_credit_card(self, user_id: int, card_last_4_digits: str, card_name: str):
        # check card_last_4_digits has indeed 4 digits and that all digits are numbers
        if len(card_last_4_digits) != 4:
            raise ValueError("card_last_4_digits must be 4 digits long")
        if not card_last_4_digits.isdigit():
            raise ValueError("card_last_4_digits must be all numbers")

        with self.connection:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO llm_finances.credit_cards (user_id, card_last_4_digits, card_name) VALUES (%s, %s, %s) RETURNING card_id;",
                    (user_id, card_last_4_digits, card_name),
                )
                card_id = cursor.fetchone()[0]
                return card_id

    def create_category(self, user_id: int, category_name: str):
        with self.connection:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO llm_finances.categories (user_id, category_name) VALUES (%s, %s) RETURNING category_id;",
                    (user_id, category_name),
                )
                category_id = cursor.fetchone()[0]
                return category_id

    def create_transactions(self, user_id: int, transactions: list):
        with self.connection:
            with self.connection.cursor() as cursor:
                for transaction in transactions:
                    cursor.execute(
                        "INSERT INTO llm_finances.transactions (transaction_date, transaction_description, credit, debit, card_id, category_id, user_id) VALUES (%s, %s, %s, %s, %s, %s, %s);",
                        (
                            transaction["transaction_date"],
                            transaction["transaction_description"],
                            transaction["credit"],
                            transaction["debit"],
                            transaction["card_id"],
                            transaction["category_id"],
                            user_id,
                        ),
                    )

    def close(self):
        self.connection.close()
