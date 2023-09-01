import streamlit as st
from streamlit_extras.add_vertical_space import add_vertical_space

from ai_assistant import AIAssistant

from page_utils import (
    login_status,
    login,
    convert_transactions_to_dataframe,
    overall_speding_trend,
    category_stacked_bars,
    database,
    user_credit_status,
    credit_updater,
)

import dotenv
import os

dotenv.load_dotenv()
OPEN_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL_NAME = os.getenv("OPENAI_MODEL_NAME")


if "messages" not in st.session_state:
    st.session_state.messages = []


def main():
    if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
        st.warning("Please log in to continue.")
        login()
    else:
        login_status()

        st.session_state["query_credits"] = database.get_user_query_credit(
            st.session_state["user_id"]
        )

        user_credit_status(credit_type="query")

        st.title("AI Financial Assistant 🤖")
        add_vertical_space(1)

        _, col2 = st.columns([0.80, 0.20])
        with col2:
            if st.button("Clear history"):
                st.session_state.messages = []

        # Initialize chat history

        # Display chat messages from history on app rerun
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        assistant = AIAssistant(model=MODEL_NAME)
        # React to user input
        if prompt := st.chat_input("What is up?"):
            # Display user message in chat message container
            st.chat_message("user").markdown(prompt)
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})

            # Get assistant response

            data = convert_transactions_to_dataframe(
                user_id=st.session_state["user_id"]
            )

            if st.session_state["query_credits"] > 0:
                with st.spinner("Thinking..."):
                    credit_updater(credit_type="query")
                    response = assistant.chat(dataframe=data, question=prompt)

                # Display assistant response in chat message container
                with st.chat_message("assistant"):
                    st.markdown(response["answer"])
                    if response["plot_path"]:
                        st.image(response["plot_path"])
                # Add assistant response to chat history

                st.session_state.messages.append(
                    {"role": "assistant", "content": response["answer"]}
                )


if __name__ == "__main__":
    main()
