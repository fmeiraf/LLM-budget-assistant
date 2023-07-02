import streamlit as st
from page_utils import register, login_status


def main():
    st.write("# Sign up ")

    register()


if __name__ == "__main__":
    main()
