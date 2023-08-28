import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_extras.switch_page_button import switch_page
from streamlit_extras.add_vertical_space import add_vertical_space
from database import Database, db_config
from transaction_parser import TransactionParser

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
    if st.session_state["input_state"] == "no_input":
        """User has not entered any transactions yet"""
        st.markdown("### Part 1 - Enter your transactions")
        transaction_input = st.text_area(
            "Simply copy and past your transactions here (you can get them straight from your statements or documents, no need to edit them).",
            height=300,
            key="transaction_input",
        )
        if st.button("Process Transactions"):
            if transaction_input:
                st.session_state["transaction_parser"] = TransactionParser(
                    transaction_input
                )
                with st.spinner("We are parsing your transactions ..."):
                    st.session_state["parsed_transactions"] = st.session_state[
                        "transaction_parser"
                    ].parse_transactions()

                    st.session_state["transaction_categories"] = st.session_state[
                        "transaction_parser"
                    ].generate_transaction_categories()

                st.session_state["input_state"] = "input_processed"

                # gathering all information needed for reviewing transactions

                st.experimental_rerun()
            else:
                st.warning("Please enter your transactions.")

    elif st.session_state["input_state"] == "input_processed":
        print(st.session_state["input_state"])
        """Transactions were initially processed, now we want to assign categories to transactions"""
        st.markdown("### Part 2 - Review your Transactions")

        st.markdown(
            """<span>These are all the different transactions we identified. <b><span style="color:#c27ba0">You can edit them AS YOU WANT.</span></b>. Please review carefully the following aspects below: </span>""",
            unsafe_allow_html=True,
        )

        st.markdown(
            """
        <ul style:"fontsize:12">
            <li><b><span style="color:#D8EF9F">Transaction name</span></b>: We give your transactions simplified names (to make things easier 😎).</li>
             <li><b><span style="color:#D8EF9F">Transaction category</span></b>: This is the category we believe this transactions belongs too.</li>
        </ul>

        <span><b><span style="color:#c27ba0">IMPORTANT:</span></b>: if want to create your own categories use the input below and add them, so you can find them on the Dropdown in the table.</span>
    """,
            unsafe_allow_html=True,
        )

        add_vertical_space(1)

        ## select categories for all unique transactions

        # processing the categories already used by the customer
        database_categories = database.get_all_categories_by_user_id(
            st.session_state["user_id"]
        )

        categories_dt = pd.DataFrame(st.session_state["transaction_categories"])

        llm_proposed_categories = [
            obj["transaction_category"]
            for obj in st.session_state["transaction_categories"]
        ]

        # st.write(
        #     st.session_state["transaction_parser"].get_transaction_names(
        #         new_transactions=pd.DataFrame(st.session_state["parsed_transactions"]),
        #         older_transactions=convert_transactions_to_dataframe(
        #             st.session_state["user_id"]
        #         ),
        #     )
        # )

        # adding transaction names to the dataframe
        transaction_names = st.session_state[
            "transaction_parser"
        ].get_transaction_names(
            new_transactions=pd.DataFrame(st.session_state["parsed_transactions"]),
            older_transactions=convert_transactions_to_dataframe(
                st.session_state["user_id"]
            ),
        )
        categories_dt = categories_dt.merge(
            transaction_names.loc[:, ["transaction_description", "transaction_name"]],
            on="transaction_description",
            how="left",
        )

        # displaying the dataframe for the customer to edit
        all_categs = set()
        for category in database_categories + llm_proposed_categories:
            all_categs.add(category)
        final_categories = sorted(all_categs, key=lambda x: x.lower())

        edited_category_data = st.data_editor(
            categories_dt.loc[
                :,
                ["transaction_description", "transaction_name", "transaction_category"],
            ],
            column_config={
                "transaction_category": st.column_config.SelectboxColumn(
                    "Transaction Category", options=final_categories
                ),
                "transaction_name": st.column_config.TextColumn("Transaction Name"),
                "transaction_description": st.column_config.TextColumn(
                    "Transaction Description"
                ),
            },
            key="category_edit_history",
        )

        if st.button("I am ok with the categories assigned!", type="primary"):
            st.session_state["transaction_parser"].update_transaction_categories(
                edited_category_data.to_dict("records")
            )

            st.session_state["input_state"] = "categories_assigned"
            st.experimental_rerun()

        st.divider()
        ## section to add new categories
        with st.form("new_category_form", clear_on_submit=True):
            st.markdown("#### If you need more to add more categories..")
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

    else:
        """All transaction have been processed and categories were chosen, now we need to review and submit final transaction info"""
        st.markdown("### Part 3 - Last check before submitting your transactions")

        st.markdown(
            """<span>We are almost there, this is how your transactions will be added (you can still edit if you want to).""",
            unsafe_allow_html=True,
        )

        add_vertical_space(1)

        # ## section to add new categories
        # with st.form("new_category_form", clear_on_submit=True):
        #     new_category = st.text_input("Add new category:", key="new_category")
        #     submitted = st.form_submit_button("Submit")
        #     if submitted:
        #         if new_category:
        #             database.create_category(
        #                 user_id=st.session_state["user_id"], category_name=new_category
        #             )
        #             st.success(f"'{new_category}' successfully added to categories!")
        #         else:
        #             st.warning("Please enter a category name.")

        ## section to edit transactions
        st.session_state["parsed_transactions"] = st.session_state[
            "transaction_parser"
        ].add_categories()  # updating categories using inputs from LLM and the review from the user

        raw_dataframe = pd.DataFrame(st.session_state["parsed_transactions"])

        transaction_dt = (
            raw_dataframe.loc[
                :,
                [
                    "transaction_date",
                    "transaction_description",
                    "transaction_name",
                    "debit",
                    "category",
                ],
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
                "category": st.column_config.SelectboxColumn(
                    "Transaction Category", options=final_categories
                ),
                "transaction_description": None,
                "transaction_date": st.column_config.TextColumn("Transaction Date"),
                "transaction_name": st.column_config.TextColumn("Transaction Name"),
                "amount": st.column_config.NumberColumn("Amount"),
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
            categories = edited_data.loc[
                edited_data["category"].notnull(), "category"
            ].unique()

            category_ids = add_new_categories(categories, st.session_state["user_id"])
            # print("category_ids", category_ids)
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
                if any(value is None for value in transaction.values()):
                    continue
                else:
                    insert_data.append(
                        {
                            "transaction_date": transaction["transaction_date"],
                            "transaction_description": transaction[
                                "transaction_description"
                            ],
                            "transaction_name": transaction["transaction_name"],
                            "credit": 0,
                            "debit": transaction["amount"],
                            "account_id": account_id,
                            "category_id": category_ids[transaction["category"]],
                            "user_id": st.session_state["user_id"],
                        }
                    )
            print(insert_data)
            database.create_transactions(
                user_id=st.session_state["user_id"], transactions=insert_data
            )

            st.success("Transactions saved successfully!")
            st.session_state["input_state"] = "no_input"
            st.session_state["parsed_transactions"] = []
            st.session_state["transaction_categories"] = []
            st.session_state["transaction_parser"] = None
            st.experimental_rerun()


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
