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


def add_new_transactions():
    ## state 1: parsed_transactions is empty
    if st.session_state["parsed_transactions"]:
        st.markdown("### Review your Transactions")

        st.markdown(
            "Review your transactions and make changes as needed (mostly check the proposed categories). You can use the space below to add new categories if you need to."
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

        st.data_editor(
            transaction_dt,
            column_config={
                "category": st.column_config.SelectboxColumn(
                    options=["Food", "Transportation", "Entertainment", "Other"]
                )
            },
            key="editable_transactions",
        )
        if st.button("Save Transactions", type="primary"):
            st.success("Transactions saved successfully!")
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
