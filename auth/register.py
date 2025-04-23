import streamlit as st
from auth.auth_utils import save_user

def register_page():
    st.title("📝 Register Page")

    new_username = st.text_input("New Username")
    new_password = st.text_input("New Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    if st.button("Register"):
        if new_password != confirm_password:
            st.error("❌ Passwords do not match!")
        elif save_user(new_username, new_password):
            st.success("✅ Registration successful! Please log in.")
        else:
            st.error("❌ Username already taken!")

if __name__ == "__main__":
    register_page()
