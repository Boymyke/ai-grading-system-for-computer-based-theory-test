import streamlit as st
from backend.user import authenticate_user
from backend.user import email_exist
from backend.user import get_user_type_by_email

st.set_page_config(page_title="Login", page_icon="📖", layout="centered")

st.title("Log In")

email = st.text_input("Email")
password = st.text_input("Password", type="password")

if st.button("Log in", key="login"):
    if not email or not password:  
        st.error("Please enter both email and password.")
    else:
        try:
            valid = authenticate_user(email, password)
            
            if valid:
                st.session_state["email"] = email
                
                with st.spinner("Redirecting to dashboard..."):
                    if get_user_type_by_email(st.session_state['email']) == "teacher":
                        st.switch_page("pages/teacher.py")
                    elif get_user_type_by_email(st.session_state['email']) == "student":
                        st.switch_page("pages/student.py")
                    else:
                        st.error("Invalid user type")
                
            else:
                st.error("❌ Invalid email or password.")

        except ValueError as e:
            if not email_exist(email):
                st.error("⚠️ Email not found. [Sign up](signup) to create an account.")
            else:
                st.error(f"⚠️ {e}") 
        except Exception as e:
            st.error(f"❌ Unexpected error: {e}") 

st.write("Don't have an account? [Sign up](signup)")
