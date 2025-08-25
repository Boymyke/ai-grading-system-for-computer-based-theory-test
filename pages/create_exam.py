import streamlit as st
import json
from modules.generate_questions import generate_questions
from modules.utils.test_utilities import (
    handle_pdf_upload, 
    render_questions, 
    save_test_data
)
from backend.user import get_user_type_by_id, get_user_profile_by_email, update_user_info
from backend.tests import get_tests_by_id, create_test_from_existing

st.title("Create a New Test")
teacher_id = st.session_state.get("user_id")

if not teacher_id:
    st.warning("Please [log in](login) first.")
    st.stop()
if get_user_type_by_id(teacher_id) != "teacher":
    st.error("Access denied. Only teachers can create tests.")
    st.stop()

email = st.session_state.get("email", None)
if email:
    user = get_user_profile_by_email(email)
    if user:
        user_id, last_name, other_names, user_type, _, title = user
        with st.sidebar:
            st.subheader("Manage Account")
            new_last_name = st.text_input("Last Name", last_name)
            new_other_names = st.text_input("Other Names", other_names)
            new_title = st.text_input("Title", title)
            new_password = st.text_input("New Password (leave blank to keep current)", type="password")

            if st.button("Update Profile"):
                success = update_user_info(user_id, new_last_name, new_other_names, new_title, new_password)
                if success:
                    st.success("Profile updated successfully! Refresh to see the new update.")

            if st.button("Logout"):
                st.session_state.email = None


num_questions = st.slider("Number of Questions", min_value=1, max_value=10, value=3)
test_creation = st.pills("Select Method", ["From PDF", "Manually", "From Existing"], default="From PDF")

if 'updated_questions' not in st.session_state:
    st.session_state.updated_questions = []

if 'test_fields' not in st.session_state:
    st.session_state.test_fields = {"title": "", "description": "", "questions": [], "strict": False}

edited_questions = None
questions = None

if test_creation == "From PDF":
    questions = handle_pdf_upload(num_questions)
    if questions:
        edited_questions = render_questions(len(questions), questions, "edit")
        st.session_state.edited_questions = edited_questions

elif test_creation == "Manually":
    questions = [{
        "id": i + 1,
        "question": "",
        "model_answer": "",
        "max_score": 2
    } for i in range(num_questions)]
    edited_questions = render_questions(num_questions, questions, "manual_")

elif test_creation == "From Existing":
    existing_tests = get_tests_by_id(teacher_id)
    if existing_tests:
        test_options = {test[1]: test[0] for test in existing_tests}
        selected_test = st.selectbox("Select an existing test", list(test_options.keys()))

        if selected_test:
            existing_test_id = test_options[selected_test]
            new_test = create_test_from_existing(existing_test_id=existing_test_id)

            st.session_state.test_fields = {
                "title": new_test.title,
                "description": new_test.description,
                "questions": new_test.questions,
            }

            test_title = st.session_state.test_fields["title"]
            test_description = st.session_state.test_fields["description"]
            questions = st.session_state.test_fields["questions"]
            edited_questions = render_questions(len(questions), questions, "edit") if questions else None

    else:
        st.warning("No existing tests found.")

test_title = st.text_input("Test Title", "" if test_creation != "From Existing" else f"Copy of {st.session_state.test_fields['title']}")
test_description = st.text_area("Test Description", "" if test_creation != "From Existing" else st.session_state.test_fields["description"])
strict_mode = st.toggle("Enable Strict Grading")

if st.button("Save Test"):
    if not test_title:
        st.error("Test title is required.")
    elif not edited_questions and not st.session_state.get('edited_questions'):
        st.error("No questions have been created. Please generate or add questions.")
    else:
        questions_to_save = edited_questions if edited_questions else st.session_state.get('edited_questions', [])
        if save_test_data(teacher_id, test_title, test_description, questions_to_save, strict_mode):
            st.session_state.test_fields = {"title": "", "description": "", "questions": [], "strict": False}
            if "questions" in st.session_state:
                st.session_state.questions = None
            if "edited_questions" in st.session_state:
                st.session_state.edited_questions = None
            if "updated_questions" in st.session_state:
                st.session_state.updated_questions = []



if st.button("Go back to dashboard"):
    st.switch_page("pages/teacher.py")
