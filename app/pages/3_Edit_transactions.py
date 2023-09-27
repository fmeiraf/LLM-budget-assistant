import streamlit as st
import pandas as pd
from streamlit_extras.add_vertical_space import add_vertical_space
from time import sleep

from page_utils import login_status, login, database, convert_transactions_to_dataframe


def main():
    st.write("# Edit transactions 💳")
    add_vertical_space(2)

    if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
        st.warning("Please log in to continue.")
        login()
    else:
        login_status()

        ## section to add new categories
        with st.form("new_category_form", clear_on_submit=True):
            st.markdown("#### If you need more to add more categories..")
            new_category = st.text_input("Add new category:", key="new_category")
            submitted = st.form_submit_button("Submit")
            if submitted:
                if new_category:
                    database.create_category(
                        user_id=st.session_state["user_id"],
                        category_name=new_category,
                    )
                    st.success(f"'{new_category}' successfully added to categories!")
                    st.experimental_rerun()
                else:
                    st.warning("Please enter a category name.")
        st.divider()
        add_vertical_space(1)
        st.write(
            "Here is a list of ALL your added transactions. Feel free to edit them as you want. If you need new categories, please use the form above to add them."
        )

        add_vertical_space(2)

        data = convert_transactions_to_dataframe(st.session_state["user_id"])

        user_categories = database.get_all_categories_info_by_user_id(
            user_id=st.session_state["user_id"]
        )

        edited_data = st.data_editor(
            data,
            hide_index=True,
            column_config={
                "transaction_name": "Name",
                "transaction_description": "Description",
                "transaction_date": "Date",
                "transaction_id": None,
                "credit": None,
                "account_id": None,
                "category_id": None,
                "user_id": None,
                "amount": "Amount",
                "category": st.column_config.SelectboxColumn(
                    "Transaction Category",
                    options=sorted(set(user_categories.keys())),
                ),
            },
            key="edited_transactions",
        )

        edited_transactions = st.session_state["edited_transactions"]

        if edited_transactions["edited_rows"]:
            # creating the upsert data
            updated_transactions = []
            for row_edited in edited_transactions["edited_rows"].keys():
                new_data = edited_data.iloc[int(row_edited)].to_dict()
                for modified_column in edited_transactions["edited_rows"][row_edited]:
                    if modified_column == "category":
                        new_data["category_id"] = int(
                            user_categories[
                                edited_transactions["edited_rows"][row_edited][
                                    modified_column
                                ]
                            ],
                        )

                        new_data[modified_column] = edited_transactions["edited_rows"][
                            row_edited
                        ][modified_column]

                    else:
                        new_data[modified_column] = edited_transactions["edited_rows"][
                            row_edited
                        ][modified_column]

                updated_transactions.append(new_data)

            if st.button("Updated transactions", type="primary"):
                database.update_transactions(
                    user_id=st.session_state["user_id"],
                    transactions=updated_transactions,
                )
                st.success("Transactions successfully updated!")
                sleep(2)
                st.experimental_rerun()

        else:
            st.button("Update transactions", disabled=True)


if __name__ == "__main__":
    main()
