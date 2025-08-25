import streamlit as st
from modules.utils.utilities import extract_text_from_pdf
import random
import string
from backend.tests import save_test, create_test_from_existing
from modules.generate_questions import generate_questions
from backend.query import execute_query 
import time

def generate_unique_test_code(max_attempts=10) -> str:
    """Generates a unique 6-character test code, ensuring it doesn't exist in the database."""
    for _ in range(max_attempts):
        test_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        existing_test = execute_query("SELECT id FROM Tests WHERE test_code = ?", (test_code,), fetchone=True)

        if existing_test is None:  
            return test_code

    raise ValueError("Failed to generate a unique test code after multiple attempts.")

def render_questions(num_questions, questions_data, prefix=""):  
    """Dynamically render editable questions."""
    updated_questions = []
    
    if questions_data:
        for i in range(min(num_questions, len(questions_data))):
            st.subheader(f"Question {i+1}")
            
            question_obj = questions_data[i]
            if question_obj:
                if isinstance(question_obj, dict):
                    question_text = question_obj.get("question", "")
                    model_answer = question_obj.get("model_answer", "")
                    max_score = question_obj.get("max_score", 2)
                else:
                    question_text = getattr(question_obj, "question", "")
                    model_answer = getattr(question_obj, "model_answer", "")
                    max_score = getattr(question_obj, "max_score", 2)
                
                key_prefix = f"{prefix}_{i}"
                question_text = st.text_area(f"Question {i+1}", value=question_text, key=f"{key_prefix}_question")
                model_answer = st.text_area(f"Model Answer {i+1}", value=model_answer, key=f"{key_prefix}_model_answer")
                max_score = st.number_input(f"Max Score {i+1}", min_value=1, value=int(max_score), key=f"{key_prefix}_max_score")
                
                updated_questions.append({
                    "id": i + 1, 
                    "question": question_text, 
                    "model_answer": model_answer, 
                    "max_score": max_score
                })
    
    # Update session state with the new values
    st.session_state.updated_questions = updated_questions
    return updated_questions

def save_test_data(teacher_id, test_title, test_description, questions, strict_mode):
    """Save test data and show success message if successful."""
    
    if not questions or len(questions) == 0:
        st.error("No questions to save.")
        return False
        
    test_code = generate_unique_test_code()
    
    success = save_test(teacher_id, test_code, test_title, test_description, questions, strict_mode)
    
    if success:
        st.success(f"Test saved successfully! Test Code: {test_code}")
        with st.spinner("Redirecting to test results..."):
            time.sleep(5)
        st.switch_page("pages/results.py")
        return True
    else:
        st.error("An error occurred while saving the test.")
        return False

def handle_pdf_upload(num_questions):
    """Handle test creation from a PDF file."""
    uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])    
    
    if 'last_uploaded_file' not in st.session_state:
        st.session_state.last_uploaded_file = None
    
    if uploaded_file and uploaded_file != st.session_state.last_uploaded_file:
        st.session_state.last_uploaded_file = uploaded_file
        if 'questions' in st.session_state:
            st.session_state.questions = None
        if 'edited_questions' in st.session_state:
            st.session_state.edited_questions = None
            
    if uploaded_file:    
        if st.button("Generate Questions"):
            try:
                with st.spinner("Generating questions..."):
                    content = extract_text_from_pdf(uploaded_file)
                    questions = generate_questions(num_questions, content)
                    st.session_state.questions = questions
                    return questions
            except Exception as e:
                st.error(f"Error generating questions: {str(e)}")
                return []
        
    return st.session_state.questions if 'questions' in st.session_state and st.session_state.questions else []