import streamlit as st

DEFAULT_USERNAME = "mans"
DEFAULT_PASSWORD = "mans123"

def login_required():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        st.title("Login")

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if username == DEFAULT_USERNAME and password == DEFAULT_PASSWORD:
                st.session_state.logged_in = True
                st.success("Login successful")
                st.rerun()
            else:
                st.error("Invalid username or password")

        st.stop()


def show_logout():
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()