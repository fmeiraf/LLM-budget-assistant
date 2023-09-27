import streamlit as st


def main():
    st.write("# About BanQstream")

    st.write("### What to expect from this app?")
    st.write(
        """

    This is:

    - An exploration project
    - A place to test new ideas
    - A place to test new models
 
    This is not: 
             
    - An official product (yet, maybe? 🙂)
    - A place to store your data (only you can see your data, but it is not encrypted yet and storage is not guaranteed)
      
    """
    )

    st.write("### What is BanQstream for?")
    st.write(
        """This is an <b> exploration project </b> to create a finance/budgeting assistant. This will be using LLMs to parse raw text coming from account statements and feeding this into a database used for further analysis. Among the features on this app:

- Parse raw account transactions
- Assign categories based on transactions names (try to make this as consistent and flexible as possible)
- Split big inputs from customers that might exceed model max tokens limitations (i.e 4096 etc)
- Simple dashboard for data visualization
- Enable user to talk to its own data through chat UI""",
        unsafe_allow_html=True,
    )

    st.write("### Background")
    st.write(
        "This was a project I created to exercise some of the new trends on LLMs. I was particularly interested in LLM's capacity to extract information from raw inputs and further transform it either by grouping similar things ( embeddings > ANN > etc) to transforming and proposing new meaning to data (assigning automatic labels for example)."
    )
    st.write(
        "To check the codebase behind this app check: [github repo](https://github.com/fmeiraf/LLM-budget-assistant)",
        unsafe_allow_html=True,
    )

    st.write("### About the author")
    st.write(
        "I'm currently working as data scientist. I love building data apps and I have been working for the last 5 years applying ML models to a buch of different business problems."
    )
    st.write(
        "For more information check: [fmeira.com](https://www.fmeira.com)",
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
