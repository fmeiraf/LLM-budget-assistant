import streamlit as st
from streamlit_extras.add_vertical_space import add_vertical_space
from page_utils import (
    login_status,
    login,
    convert_transactions_to_dataframe,
    overall_transaction_summary,
)

# if "transaction_dataframe" not in st.session_state:
#     st.session_state["transaction_dataframe"] = pd.DataFrame()


def main():
    st.write("# Transaction Summary 📓")
    if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
        st.warning("Please log in to continue.")
        login()
    else:
        login_status()
        add_vertical_space(1)

        # getting dataframe with all transactions
        data = convert_transactions_to_dataframe(user_id=st.session_state["user_id"])

        # Overall sumamry
        st.write("### Overall Summary")

        # Spending category summary
        add_vertical_space(1)
        st.write("### Spending Category Summary")


if __name__ == "__main__":
    main()
