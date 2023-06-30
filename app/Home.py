import streamlit as st
import pandas as pd
from database import Database, db_config
from dotenv import load_dotenv
from page_utils import register, login, login_status

load_dotenv()

st.set_page_config(
    page_title="LLM Financial Assistant",
    page_icon="🤖",
)

# state declarations
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if "user_id" not in st.session_state:
    st.session_state["user_id"] = None

if "user_email" not in st.session_state:
    st.session_state["user_email"] = None


def main():
    st.sidebar.success("Select a demo above.")

    if not st.session_state["logged_in"]:
        login()

    login_status()
    st.write("# Welcome to Streamlit! 👋")

    # st.write(st.session_state["logged_in"])


if __name__ == "__main__":
    main()
