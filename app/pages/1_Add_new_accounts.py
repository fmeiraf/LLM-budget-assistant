import streamlit as st
from streamlit_extras.add_vertical_space import add_vertical_space

from page_utils import add_new_accounts, login_status, login


def main():
    if st.session_state["logged_in"]:
        login_status()

    st.write("# Add New accounts  💳")
    add_vertical_space(2)

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
        add_new_accounts()
    else:
        st.warning("Please log in to continue.")
        login()


if __name__ == "__main__":
    main()
