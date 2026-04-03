import os
import streamlit as st

DEFAULT_USERNAME = os.getenv("APP_USERNAME", "admin")
DEFAULT_PASSWORD = os.getenv("APP_PASSWORD", "admin123")


def _get_credentials():
    username = DEFAULT_USERNAME
    password = DEFAULT_PASSWORD

    try:
        if "APP_USERNAME" in st.secrets:
            username = st.secrets["APP_USERNAME"]
        if "APP_PASSWORD" in st.secrets:
            password = st.secrets["APP_PASSWORD"]
    except Exception:
        pass

    return username, password


def login_required():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        app_username, app_password = _get_credentials()

        st.title("Login")
        st.caption("Please sign in to access the Media Finance Manager.")

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login", type="primary"):
            if username == app_username and password == app_password:
                st.session_state.logged_in = True
                st.success("Login successful")
                st.rerun()
            else:
                st.error("Invalid username or password")

        st.stop()


def show_logout():
    st.sidebar.caption("Session active")
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()
