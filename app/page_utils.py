import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from database import Database, db_config
from dotenv import load_dotenv

load_dotenv()

database = Database(**db_config)


def register():
    st.subheader("Create New Account")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Register"):
        if email and password:
            user_is_registered = database.get_user_id_by_email(email)
            if user_is_registered:
                st.warning("Email already registered.")
            else:
                database.create_user(email, password)
                st.success("Registration successful. Please log in.")
        else:
            st.warning("Please enter both email and password.")


def login():
    st.subheader("Log In")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Log In"):
        if email and password:
            user_is_registered = database.get_user_id_by_email(email)
            if user_is_registered:
                is_logged_in = database.log_in(email, password)
                if is_logged_in:
                    st.success("Logged in successfully.")
                    st.session_state["logged_in"] = True
                    st.session_state["user_id"] = is_logged_in
                    st.session_state["user_email"] = email
                    st.experimental_rerun()
                # Proceed with authenticated functionality
                else:
                    st.warning("Invalid email.")
            else:
                st.warning("Invalid email or password.")
        else:
            st.warning("Please enter both email and password.")

    if st.button("Sign Up", type="secondary"):
        switch_page("Sign up")


def login_status():
    _, col2 = st.columns([0.40, 0.60])
    if st.session_state["logged_in"]:
        # col2.text(f"Logged in as: {st.session_state['user_email']} 🟢")
        style = """
        <style>
            .right-aligned {
                text-align: right;
            }
        </style>"""

        login_status_text = f"""
            {style}

        <div class="right-aligned">
            <b>Logged in as</b> : {st.session_state['user_email']}  🟢
        </div>
        """

        # Display the left-aligned Markdown
        st.markdown(login_status_text, unsafe_allow_html=True)
