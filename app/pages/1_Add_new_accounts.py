import streamlit as st
from streamlit_extras.add_vertical_space import add_vertical_space

from page_utils import add_new_accounts, login_status, login, database


def main():
    st.write("# Add New accounts  💳")
    add_vertical_space(2)

    if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
        st.warning("Please log in to continue.")
        login()
    else:
        login_status()

        st.markdown(
            """Here is where you can add new accounts. Accounts represent the origins of your transactions.
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            """ For example: here is where you would add your <b>credit cards</b>, <b>bank accounts</b>, and <b>cash accounts</b>.
            """,
            unsafe_allow_html=True,
        )

        if st.session_state["logged_in"]:
            with st.form("add_new_accounts", clear_on_submit=True):
                account_name = st.text_input(
                    "Account Name",
                )
                account_last_digits = st.text_input(
                    "Last 4 digits (optional)",
                    max_chars=4,
                )

                if st.form_submit_button("Add Account"):
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


if __name__ == "__main__":
    main()
