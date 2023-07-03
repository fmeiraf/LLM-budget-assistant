import streamlit as st
from streamlit_extras.add_vertical_space import add_vertical_space
from page_utils import login_status, login, add_new_transactions


def main():
    if st.session_state["logged_in"]:
        login_status()
    st.write("# Add new transactions 💸")
    add_vertical_space(2)

    st.markdown(
        """Here is where you can add transactions to your accounts: 
        """,
        unsafe_allow_html=True,
    )

    if st.session_state["logged_in"]:
        expander = st.expander("Instructions to add transactions:")
        expander.write("""- First, select the account you want to add transactions to.\
        \n- Go to your account's portal (at your bank, credit card vendor, etc).\
        \n- Copy and paste the transaction history into the text box below.\
        \n- You can add multiple transactions at once.
        \n- Make sure you have at list the transaction date, description, and amount.\
        \n- Click the "Add Transactions" button.\
        """)
        add_vertical_space(2)
        add_new_transactions()
    else:
        st.warning("Please log in to continue.")
        login()

if __name__ == "__main__":
    main()
