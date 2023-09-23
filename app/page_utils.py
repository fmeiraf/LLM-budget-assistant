import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_extras.switch_page_button import switch_page
from streamlit_extras.add_vertical_space import add_vertical_space
from database import Database, db_config
from transaction_parser import TransactionParser

from auth import hash_password, check_password

from dotenv import load_dotenv

load_dotenv()

database = Database(**db_config)


def convert_transactions_to_dataframe(user_id: int):
    transactions = database.get_all_transactions_by_user_id(user_id=user_id)
    df = pd.DataFrame(
        [
            {
                "transaction_id": transaction.transaction_id,
                "transaction_date": transaction.transaction_date,
                "transaction_description": transaction.transaction_description,
                "transaction_name": transaction.transaction_name,
                "credit": transaction.credit,
                "amount": transaction.debit,
                "account_id": transaction.account_id,
                "category_id": transaction.category_id,
                "user_id": transaction.user_id,
                "category": category.category_name,
            }
            for transaction, category in transactions
        ]
    )

    return df


def register():
    st.subheader("Create New Account")
    username = st.text_input("Username")
    password = hash_password(st.text_input("Password", type="password")).decode()

    if st.button("Register"):
        if username and password:
            user_is_registered = database.get_user_id_by_username(username)
            if user_is_registered:
                st.warning("username already registered.")
            else:
                database.create_user(username, password)
                st.success("Registration successful. Please log in.")
                switch_page("home")
        else:
            st.warning("Please enter both username and password.")


def login():
    st.subheader("Log In")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Log In"):
        if username and password:
            user_is_registered = database.get_user_id_by_username(username)
            if user_is_registered:
                user_hashed_password = database.get_user_password_by_username(username)

                if check_password(
                    user_password=password, hashed_password=user_hashed_password
                ):
                    st.success("Logged in successfully.")
                    st.session_state["logged_in"] = True
                    st.session_state["user_id"] = user_is_registered
                    st.session_state["username"] = username
                    st.experimental_rerun()
                # Proceed with authenticated functionality
                else:
                    st.warning("Invalid password.")
            else:
                st.warning("Invalid username.")
        else:
            st.warning("Please enter both username and password.")

    if st.button("Sign Up", type="secondary"):
        switch_page("Sign up")


def login_status():
    _, col2 = st.columns([0.30, 0.70])
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
            <b>Logged in as</b> : {st.session_state['username']}  🟢
        </div>
        """

        # Display the left-aligned Markdown
        st.markdown(login_status_text, unsafe_allow_html=True)
        if st.button("Log Out", type="secondary"):
            st.session_state["logged_in"] = False
            st.session_state["user_id"] = None
            st.session_state["username"] = None
            st.experimental_rerun()
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
            switch_page("Financial Assistant")


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


def credit_updater(credit_type: str):
    if credit_type == "parsing":
        if st.session_state["parsing_credits"] > 0:
            st.session_state["parsing_credits"] -= 1
            database.update_user_add_credit(
                user_id=st.session_state["user_id"],
                new_credit=st.session_state["parsing_credits"],
            )
    elif credit_type == "query":
        if st.session_state["query_credits"] > 0:
            st.session_state["query_credits"] -= 1
            database.update_user_query_credit(
                user_id=st.session_state["user_id"],
                new_credit=st.session_state["query_credits"],
            )
    else:
        raise ValueError("Invalid credit type.")


@st.cache_data
def get_database_categories(user_id: int):
    return database.get_all_categories_by_user_id(user_id=user_id)


@st.cache_data
def get_transaction_names(
    _parser_obj: TransactionParser, parsed_transactions: list, user_id: int
):
    return _parser_obj.get_transaction_names(
        new_transactions=pd.DataFrame(parsed_transactions),
        older_transactions=convert_transactions_to_dataframe(user_id=user_id),
    )


def overall_speding_trend(data=pd.DataFrame()):
    if not data.empty:
        tab1, tab2 = st.tabs(["Monthly", "Daily"])

        with tab1:
            # Trend line per month
            monthly_spending = (
                data.copy()
                .assign(
                    transaction_date=lambda x: pd.to_datetime(x["transaction_date"])
                )
                .assign(
                    transaction_month=lambda x: x["transaction_date"].dt.strftime(
                        "%m-%y"
                    )
                )
                .loc[lambda x: x.amount.notnull()]
                .groupby("transaction_month")
                .agg({"amount": "sum"})
                .reset_index()
            )

            monthly_line_trend = px.line(
                monthly_spending,
                x="transaction_month",
                y="amount",
                markers=True,
            )
            st.plotly_chart(monthly_line_trend)

        with tab2:
            # Trend line per day
            daily_line_trend = px.line(
                data,
                x="transaction_date",
                y="amount",
                markers=True,
            )
            st.plotly_chart(daily_line_trend)
    else:
        st.warning("No transactions found.")


def category_stacked_bars(data=pd.DataFrame()):
    if not data.empty:
        # aggregating the category spending type by month
        category_spending = (
            data.copy()
            .assign(transaction_date=lambda x: pd.to_datetime(x["transaction_date"]))
            .assign(
                transaction_month=lambda x: x["transaction_date"].dt.strftime("%m-%y")
            )
            .loc[lambda x: x.amount.notnull()]
            .groupby(["transaction_month", "category"])
            .agg({"amount": "sum"})
            .reset_index()
            .sort_values(["category", "transaction_month"], ascending=[True, True])
        )
        # Stacked bar chart
        stacked_bar_chart = px.bar(
            category_spending,
            x="transaction_month",
            y="amount",
            color="category",
            barmode="stack",
            title="Spending by Category",
        )
        st.plotly_chart(stacked_bar_chart)
    else:
        st.warning("No transactions found.")


def user_credit_status(credit_type: str):
    if st.session_state["logged_in"]:
        st.metric(
            label=f"Credits left for {credit_type}",
            value=st.session_state[f"{credit_type}_credits"],
            help="For resource reasons the amount of queries you can make is limited.",
        )


def next_step_tip(page_name: str):
    with st.container():
        st.write(f"### 💡 Next step")

        st.write(("If you are __not sure what to do__ next:"))

        if st.button(f"Take me to the next step", type="primary"):
            switch_page(page_name)
