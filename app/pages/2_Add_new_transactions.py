import streamlit as st
from streamlit_extras.add_vertical_space import add_vertical_space
from page_utils import login_status, login, add_new_transactions


if "show_transaction_input" not in st.session_state:
    st.session_state["show_transaction_input"] = True

if "show_transaction_output" not in st.session_state:
    st.session_state["show_transaction_output"] = False

if "input_state" not in st.session_state:
    st.session_state["input_state"] = "no_input"

if "parsed_transactions" not in st.session_state:
    st.session_state["parsed_transactions"] = []

if "transaction_parser" not in st.session_state:
    st.session_state["transaction_parser"] = None


def main():
    if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
        st.warning("Please log in to continue.")
        login()
    else:
        login_status()
        st.write("# Add new transactions 💸")
        add_vertical_space(1)

        st.markdown(
            """Here is where you can add transactions to your accounts: 
            """,
            unsafe_allow_html=True,
        )

        if st.session_state["logged_in"]:
            expander = st.expander("Instructions to add transactions:")
            expander.write(
                """- First, select the account you want to add transactions to.\
            \n- Go to your account's portal (at your bank, credit card vendor, etc).\
            \n- Copy and paste the transaction history into the text box below.\
            \n- You can add multiple transactions at once.
            \n- Make sure you have at list the transaction date, description, and amount.\
            \n- Click the "Add Transactions" button.\
            \n- After we proceess your transactions, you will be able see a summary of them.
            \n- You can edit or delete transactions from the summary page.
            """
            )
            add_vertical_space(1)
            add_new_transactions()


if __name__ == "__main__":
    main()
