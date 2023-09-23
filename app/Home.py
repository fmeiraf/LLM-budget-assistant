import streamlit as st
import pandas as pd
from database import Database, db_config
from dotenv import load_dotenv
from page_utils import register, login, login_status, menu, database, next_step_tip
from streamlit_extras.add_vertical_space import add_vertical_space

load_dotenv()

st.set_page_config(
    page_title="BanQstream - your LLM Financial Assistant", page_icon="🎏"
)

# state declarations
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if "user_id" not in st.session_state:
    st.session_state["user_id"] = None

if "username" not in st.session_state:
    st.session_state["username"] = None

if "parsing_credits" not in st.session_state:
    st.session_state["add_credits"] = None

if "query_credits" not in st.session_state:
    st.session_state["query_credits"] = None

if "added_accounts" not in st.session_state:
    st.session_state["added_accounts"] = False

if "added_transactions" not in st.session_state:
    st.session_state["added_transactions"] = False

if "question_assistant" not in st.session_state:
    st.session_state["question_assistant"] = False


def main():
    _, col, _ = st.columns([0.30, 0.40, 0.30])
    with col:
        st.image(
            "https://storage.googleapis.com/banqstream/original_logo_small_transp.png",
            width=100,
        )
    st.write("# Welcome to BanQstream! 👋 \n\n")
    st.divider()

    if not st.session_state["logged_in"]:
        st.markdown("#### Please log in to continue or sign up for a new account.")
        login()
    else:
        login_status()
        menu()

        st.divider()
        add_vertical_space(1)

        st.write("### Here is a list of things you might want to do (in sequence):")

        add_account = st.checkbox(
            "Add at least one new account",
            value=st.session_state["added_accounts"],
            key="add_account",
        )
        add_transaction = st.checkbox(
            "Add new transactions",
            value=st.session_state["added_transactions"],
            key="add_transaction",
        )
        add_question = st.checkbox(
            "Make questions to the assistant",
            value=st.session_state["question_assistant"],
            key="add_question",
        )

        st.divider()

        next_step_tip(page_name="Add new accounts")


if __name__ == "__main__":
    main()
