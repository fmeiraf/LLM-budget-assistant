import streamlit as st
import pandas as pd
from transaction_parser import TransactionParser
from streamlit_extras.add_vertical_space import add_vertical_space
from page_utils import (
    login_status,
    login,
    user_credit_status,
    credit_updater,
    convert_transactions_to_dataframe,
    add_new_categories,
    get_database_categories,
    get_transaction_names,
    database,
)


if "show_transaction_input" not in st.session_state:
    st.session_state["show_transaction_input"] = True


if "input_state" not in st.session_state:
    st.session_state["input_state"] = "no_input"

if "parsed_transactions" not in st.session_state:
    st.session_state["parsed_transactions"] = []

if "transaction_parser" not in st.session_state:
    st.session_state["transaction_parser"] = None

if "transaction_categories" not in st.session_state:
    st.session_state["transaction_categories"] = []


def main():
    st.write("# Add New Transactions  💳")
    add_vertical_space(1)
    if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
        st.warning("Please log in to continue.")
        login()
    else:
        login_status()
        st.session_state["parsing_credits"] = database.get_user_add_credit(
            st.session_state["user_id"]
        )

        user_credit_status(credit_type="parsing")

        if st.session_state["logged_in"]:
            add_vertical_space(1)

            ### Starting the transaction parsing process
            if st.session_state["input_state"] == "no_input":
                """User has not entered any transactions yet"""
                st.markdown("### Part 1 - Enter your transactions")
                transaction_input = st.text_area(
                    "Simply copy and past your transactions here (you can get them straight from your statements or documents, no need to edit them).",
                    height=300,
                    key="transaction_input",
                )
                if st.button("Process Transactions"):
                    if st.session_state["parsing_credits"] > 0:
                        if transaction_input:
                            credit_updater(credit_type="parsing")
                            st.session_state["transaction_parser"] = TransactionParser(
                                transaction_input
                            )
                            with st.spinner("We are parsing your transactions ..."):
                                st.session_state[
                                    "parsed_transactions"
                                ] = st.session_state[
                                    "transaction_parser"
                                ].parse_transactions()

                                st.session_state[
                                    "transaction_categories"
                                ] = st.session_state[
                                    "transaction_parser"
                                ].generate_transaction_categories()

                            st.session_state["input_state"] = "input_processed"

                            # gathering all information needed for reviewing transactions

                            st.experimental_rerun()
                        else:
                            st.warning("Please enter your transactions.")
                    else:
                        st.warning(
                            "You have no more credits left. Sorry, you can't add more transactions."
                        )

            elif st.session_state["input_state"] == "input_processed":
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
                # database_categories = get_database_categories(
                #     user_id=st.session_state["user_id"]
                # )

                categories_dt = pd.DataFrame(st.session_state["transaction_categories"])

                llm_proposed_categories = [
                    obj["transaction_category"]
                    for obj in st.session_state["transaction_categories"]
                ]

                # adding transaction names to the dataframe
                with st.spinner(
                    "We are adding transaction names to your transactions ..."
                ):
                    transaction_names = get_transaction_names(
                        _parser_obj=st.session_state["transaction_parser"],
                        parsed_transactions=st.session_state["parsed_transactions"],
                        user_id=st.session_state["user_id"],
                    )

                categories_dt = categories_dt.merge(
                    transaction_names.loc[
                        :, ["transaction_description", "transaction_name"]
                    ],
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
                        [
                            "transaction_description",
                            "transaction_name",
                            "transaction_category",
                        ],
                    ].drop_duplicates("transaction_description"),
                    column_config={
                        "transaction_category": st.column_config.SelectboxColumn(
                            "Transaction Category", options=final_categories
                        ),
                        "transaction_name": st.column_config.TextColumn(
                            "Transaction Name"
                        ),
                        "transaction_description": st.column_config.TextColumn(
                            "Transaction Description"
                        ),
                    },
                    key="category_edit_history",
                )

                if st.button("I am ok with the categories assigned!", type="primary"):
                    st.session_state[
                        "transaction_parser"
                    ].update_transaction_categories(
                        edited_category_data.to_dict("records")
                    )

                    st.session_state["input_state"] = "categories_assigned"
                    st.experimental_rerun()

                st.divider()
                ## section to add new categories
                with st.form("new_category_form", clear_on_submit=True):
                    st.markdown("#### If you need more to add more categories..")
                    new_category = st.text_input(
                        "Add new category:", key="new_category"
                    )
                    submitted = st.form_submit_button("Submit")
                    if submitted:
                        if new_category:
                            database.create_category(
                                user_id=st.session_state["user_id"],
                                category_name=new_category,
                            )
                            st.success(
                                f"'{new_category}' successfully added to categories!"
                            )
                            st.experimental_rerun()
                        else:
                            st.warning("Please enter a category name.")

            else:
                """All transaction have been processed and categories were chosen, now we need to review and submit final transaction info"""
                st.markdown(
                    "### Part 3 - Last check before submitting your transactions"
                )

                st.markdown(
                    """<span>We are almost there, this is how your transactions will be added (you can still edit if you want to).""",
                    unsafe_allow_html=True,
                )

                add_vertical_space(1)

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
                        "transaction_date": st.column_config.TextColumn(
                            "Transaction Date"
                        ),
                        "transaction_name": st.column_config.TextColumn(
                            "Transaction Name"
                        ),
                        "amount": st.column_config.NumberColumn("Amount"),
                    },
                    key="edit_history",
                )

                # adding dropdown for accounts
                st.markdown("### Submit your transactions")
                accounts = database.get_all_accounts_names_by_user_id(
                    st.session_state["user_id"]
                )
                account_selected = st.selectbox(
                    "Select an account (where these transactions will be added):",
                    accounts,
                )

                if st.button("Submit Transactions", type="primary"):
                    # checking categories
                    categories = edited_data.loc[
                        edited_data["category"].notnull(), "category"
                    ].unique()

                    category_ids = add_new_categories(
                        categories, st.session_state["user_id"]
                    )
                    # print("category_ids", category_ids)
                    if not category_ids:
                        st.warning(
                            "Please make sure you have categories assigned to all your transactions."
                        )

                    # checking account selection
                    account_id = database.get_account_id_by_name(
                        user_id=st.session_state["user_id"],
                        account_name=account_selected,
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
                                    "category_id": category_ids[
                                        transaction["category"]
                                    ],
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


if __name__ == "__main__":
    main()
