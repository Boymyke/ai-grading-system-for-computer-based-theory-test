import streamlit as st
import re

from backend.user import create_user
from backend.user import email_exist

st.set_page_config(page_title="Signup", page_icon="📖", layout="centered")


st.title("Sign Up")
with st.form("signup"):
    last_name = st.text_input("Last Name")
    other_names = st.text_input("Other Names")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    password_confirm = st.text_input("Confirm Password", type="password")
    user_type = st.selectbox("What best describes you", ["student", "teacher"])
    submitted = st.form_submit_button("Create my account!")

    if submitted:
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            st.error("Invalid email address.")
        elif email_exist(email):
            st.error("Email already exists. Please [Log in](login)")
        elif password != password_confirm:
            st.error("Passwords do not match.")
        else:
            try:
                success = create_user(email, password, last_name, other_names, user_type)
                st.success("Sign up successful.")
                with st.spinner("Redirecting to login page..."):
                    st.switch_page("pages/login.py")
            except ValueError as e:
                st.error(f"⚠️ {e}") 
            except Exception as e:
                st.error(f"❌ Unexpected error: {e}") 

    st.write("Already have an account? [Log in](login)")
