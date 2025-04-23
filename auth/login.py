import streamlit as st
from auth.auth_utils import authenticate_user

def login_page():
    st.title("🔐 Login Page")
    
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if authenticate_user(username, password):
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success("✅ Login successful!")
            st.experimental_rerun()
        else:
            st.error("❌ Invalid username or password")

if __name__ == "__main__":
    login_page()
