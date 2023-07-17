import streamlit as st
import pandas as pd
from streamlit_extras.switch_page_button import switch_page
from streamlit_extras.add_vertical_space import add_vertical_space
from database import Database, db_config
from transaction_parser import TransactionParser

from dotenv import load_dotenv

load_dotenv()

database = Database(**db_config)


def register():
    st.subheader("Create New Account")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Register"):
        if email and password:
            user_is_registered = database.get_user_id_by_email(email)
            if user_is_registered:
                st.warning("Email already registered.")
            else:
                database.create_user(email, password)
                st.success("Registration successful. Please log in.")
        else:
            st.warning("Please enter both email and password.")


def login():
    st.subheader("Log In")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Log In"):
        if email and password:
            user_is_registered = database.get_user_id_by_email(email)
            if user_is_registered:
                is_logged_in = database.log_in(email, password)
                if is_logged_in:
                    st.success("Logged in successfully.")
                    st.session_state["logged_in"] = True
                    st.session_state["user_id"] = user_is_registered
                    st.session_state["user_email"] = email
                    st.experimental_rerun()
                # Proceed with authenticated functionality
                else:
                    st.warning("Invalid email.")
            else:
                st.warning("Invalid email or password.")
        else:
            st.warning("Please enter both email and password.")

    if st.button("Sign Up", type="secondary"):
        switch_page("Sign up")


def login_status():
    _, col2 = st.columns([0.40, 0.60])
    if st.session_state["logged_in"]:
        # col2.text(f"Logged in as: {st.session_state['user_email']} 🟢")
        style = """
        <style>
            .right-aligned {
                text-align: right;
            }
        </style>"""

        login_status_text = f"""
            {style}

        <div class="right-aligned">
            <b>Logged in as</b> : {st.session_state['user_email']}  🟢
        </div>
        """

        # Display the left-aligned Markdown
        st.markdown(login_status_text, unsafe_allow_html=True)
        add_vertical_space(2)


def menu():
    # Create buttons in different colors and columns
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button(
            ":blue[Add New Accounts 💳]",
        ):
            switch_page("Add new accounts")

    with col2:
        if st.button(
            ":blue[Add New Transactions 💰]",
        ):
            switch_page("Add new transactions")

    with col3:
        if st.button(
            ":green[Transaction Summary] 📈",
        ):
            switch_page("Transaction summary")

    with col4:
        if st.button("Financial Assistant 🧑‍🎨"):
            switch_page("Financial ")


def add_new_accounts():
    account_name = st.text_input("Account Name")
    account_last_digits = st.text_input("Last 4 digits (optional)", max_chars=4)

    if st.button("Add Account"):
        if account_name:
            if not account_last_digits:
                account_last_digits = "0000"

            database.create_account(
                user_id=st.session_state["user_id"],
                account_last_4_digits=account_last_digits,
                account_name=account_name,
            )
            st.success("Account added successfully.")
        else:
            st.warning("Please enter an account name.")


def add_new_category(category_name: str, user_id: int):
    # check if category already exists
    category_id = database.get_category_id_by_name(
        user_id=user_id, category_name=category_name
    )

    if category_id:
        # st.warning(f"'{category_name}' already exists in categories!")
        return category_id
    else:
        # st.success(f"'{category_name}' successfully added to categories!")
        return database.create_category(user_id=user_id, category_name=category_name)


def add_new_categories(categories: list, user_id: int):
    category_ids = {}
    for category in categories:
        category_ids[category] = add_new_category(
            category_name=category, user_id=user_id
        )
    return category_ids


def add_new_transactions():
    ## state 1: parsed_transactions is empty
    if st.session_state["parsed_transactions"]:
        st.markdown("### Review your Transactions")

        st.markdown(
            "Review your transactions and make changes as needed (mostly check the suggested categories). You can use the space below to add new categories if you need to."
        )

        ## section to add new categories
        with st.form("new_category_form", clear_on_submit=True):
            new_category = st.text_input("Add new category:", key="new_category")
            submitted = st.form_submit_button("Submit")
            if submitted:
                if new_category:
                    database.create_category(
                        user_id=st.session_state["user_id"], category_name=new_category
                    )
                    st.success(f"'{new_category}' successfully added to categories!")
                else:
                    st.warning("Please enter a category name.")

        ## section to edit transactions
        raw_dataframe = pd.DataFrame(st.session_state["parsed_transactions"])
        transaction_dt = (
            raw_dataframe.loc[
                :, ["transaction_date", "transaction_description", "debit", "category"]
            ]
            .copy()
            .rename(columns={"debit": "amount"})
        )

        # processing the categories already used by the customer
        database_categories = database.get_all_categories_by_user_id(
            st.session_state["user_id"]
        )
        llm_proposed_categories = [
            obj["category"] for obj in st.session_state["parsed_transactions"]
        ]

        all_categs = set()
        for category in database_categories + llm_proposed_categories:
            all_categs.add(category)
        final_categories = sorted(all_categs, key=lambda x: x.lower())

        edited_data = st.data_editor(
            transaction_dt,
            column_config={
                "category": st.column_config.SelectboxColumn(options=final_categories)
            },
            key="edit_history",
        )

        # adding dropdown for accounts
        st.markdown("### Submit your transactions")
        accounts = database.get_all_accounts_by_user_id(st.session_state["user_id"])
        account_selected = st.selectbox(
            "Select an account (where these transactions will be added):", accounts
        )

        if st.button("Submit Transactions", type="primary"):
            # checking categories
            categories = edited_data["category"].unique()
            category_ids = add_new_categories(categories, st.session_state["user_id"])
            if not category_ids:
                st.warning(
                    "Please make sure you have categories assigned to all your transactions."
                )

            # checking account selection
            account_id = database.get_account_id_by_name(
                user_id=st.session_state["user_id"], account_name=account_selected
            )
            if not account_id:
                st.warning("Please select an account.")

            # adding transactions to database

            # rebuilding the transactions object:
            insert_data = []
            for transaction in edited_data.to_dict("records"):
                insert_data.append(
                    {
                        "transaction_date": transaction["transaction_date"],
                        "transaction_description": transaction[
                            "transaction_description"
                        ],
                        "credit": 0,
                        "debit": transaction["amount"],
                        "account_id": account_id,
                        "category_id": category_ids[transaction["category"]],
                        "user_id": st.session_state["user_id"],
                    }
                )

            database.create_transactions(
                user_id=st.session_state["user_id"], transactions=insert_data
            )
            # print(edited_data.to_dict("records"))
            st.success("Transactions saved successfully!")

            # cleaning all variables used on transaction insertion
            # account_id

    ## state 2: parsed_transactions is empty
    else:
        st.markdown("### Add New Transactions")
        transaction_input = st.text_area(
            "Paste your transactions here:", height=300, key="transaction_input"
        )
        if st.button("Process Transactions"):
            if transaction_input:
                transaction_parser = TransactionParser(transaction_input)
                with st.spinner("We are parsing your transactions ..."):
                    st.session_state[
                        "parsed_transactions"
                    ] = transaction_parser.parse_transactions()

                st.experimental_rerun()
            else:
                st.warning("Please enter your transactions.")
