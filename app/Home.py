import streamlit as st
import pandas as pd
from database import Database, db_config
from dotenv import load_dotenv
from page_utils import register, login, login_status, menu
from streamlit_extras.add_vertical_space import add_vertical_space

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

    st.write("# Welcome to the LLM budget assistant! 👋 \n\n")
    st.divider()

    if not st.session_state["logged_in"]:
        st.markdown("#### Please log in to continue or sign up for a new account.")
        login()

    login_status()
    menu()

    # st.write(st.session_state["logged_in"])


if __name__ == "__main__":
    main()
