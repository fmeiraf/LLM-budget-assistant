import streamlit as st
import pandas as pd
from database import Database, db_config
from dotenv import load_dotenv
from page_utils import register, login

load_dotenv()

st.set_page_config(
    page_title="LLM Financial Assistant",
    page_icon="🤖",
)


if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False


def main():
    st.sidebar.success("Select a demo above.")

    st.write("# Welcome to Streamlit! 👋")

    login()

    # st.write(st.session_state["logged_in"])


if __name__ == "__main__":
    main()
