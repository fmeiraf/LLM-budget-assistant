import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="LLM Financial Assistant",
    page_icon="🤖",
)


def main():
    st.sidebar.success("Select a demo above.")

    st.write("# Welcome to Streamlit! 👋")
    # st.write("Here's our first attempt at using data to create a table:")
    # st.write(
    #     pd.DataFrame({"first column": [1, 2, 3, 4], "second column": [10, 20, 30, 40]})
    # )


if __name__ == "__main__":
    main()
