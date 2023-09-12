import streamlit as st
import pandas as pd
from database import Database, db_config
from dotenv import load_dotenv
from page_utils import register, login, login_status, menu, database
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

    # st.write(st.session_state["logged_in"])


if __name__ == "__main__":
    main()
