import streamlit as st
import json

from modules.grading import generate_results
from rubric import STRICT_RUBRIC, LENIENT_RUBRIC
from backend.tests import get_test_data, check_previous_attempt, save_student_answers 
from backend.results import save_results

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1EE51E;
        margin-bottom: 1.5rem;
        text-align: center;
        padding-bottom: 1rem;
        border-bottom: 2px solid #f0f2f6;
    }
    .question-container {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1.5rem;
        border-left: 5px solid #1EE51E;
    }
    .question-header {
        color: #1EE51E;
        font-size: 1.3rem;
        margin-bottom: 0.8rem;
    }
    .question-text {
        font-size: 1.1rem;
        margin-bottom: 1rem;
    }
    .submit-btn {
        background-color: #1EE51E;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        border: none;
        cursor: pointer;
        font-size: 1rem;
    }
    .info-box {
        background-color: #e3f2fd;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .error-box {
        background-color: #ffebee;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .success-box {
        background-color: #e8f5e9;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .exam-code-input {
        max-width: 400px;
        margin: 1rem auto;
    }
    .stTextArea textarea {
        border-radius: 5px;
        border: 1px solid #ddd;
        padding: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Main title with custom styling
st.markdown("<h1 class='main-header'>📘 Take Exam</h1>", unsafe_allow_html=True)

student_id = st.session_state.get("user_id", None)

if not student_id:
    st.markdown("""
    <div class="error-box">
        <strong>⚠️ Authentication Required</strong><br>
        You must be logged in to take an exam.
    </div>
    """, unsafe_allow_html=True)
    st.switch_page("pages/login.py")

# Create a card-like container for the exam code input
st.markdown("<div class='exam-code-input'>", unsafe_allow_html=True)
test_code = st.text_input("Enter Exam Code:", key="exam_code_input", 
                          placeholder="Enter your exam code here...")
st.markdown("</div>", unsafe_allow_html=True)

if "exam_fetched" not in st.session_state:
    st.session_state.exam_fetched = False
if "student_answers" not in st.session_state:
    st.session_state.student_answers = {}

# Style the fetch button
fetch_col1, fetch_col2, fetch_col3 = st.columns([1, 2, 1])
with fetch_col2:
    fetch_button = st.button("Fetch Questions", key="fetch_button", 
                             help="Click to load exam questions")

if fetch_button:
    with st.spinner("Loading exam questions..."):
        test_data = get_test_data(test_code)
        if not test_data:
            st.markdown("""
            <div class="error-box">
                <strong>❌ Invalid Exam Code</strong><br>
                Please check your exam code and try again.
            </div>
            """, unsafe_allow_html=True)
        else:
            test_id, questions_json = test_data
            previous_attempt = check_previous_attempt(test_id, student_id)
            if previous_attempt:
                st.markdown("""
                <div class="info-box">
                    <strong>ℹ️ Previous Attempt Detected</strong><br>
                    You have already taken this exam. Redirecting to results...
                </div>
                """, unsafe_allow_html=True)
                st.session_state.test_id = test_id
                st.session_state.student_id = student_id
                st.switch_page("pages/result.py")
            else:
                questions = json.loads(questions_json)
                st.session_state.exam_fetched = True
                st.session_state.test_id = test_id
                st.session_state.questions = questions
                # Initialize student answers for each question if not already done
                st.session_state.student_answers = {q["id"]: "" for q in questions}

# If exam is fetched, display the exam questions and persist answers
if st.session_state.exam_fetched:
    st.markdown("<h2 style='text-align: center; margin: 2rem 0 1.5rem 0;'>Exam Questions</h2>", unsafe_allow_html=True)
    
    # Add a progress indicator
    total_questions = len(st.session_state.questions)
    answered_questions = sum(1 for ans in st.session_state.student_answers.values() if ans.strip())
    st.progress(answered_questions / total_questions)
    st.markdown(f"<p style='text-align: center; margin-bottom: 2rem;'><strong>Progress:</strong> {answered_questions}/{total_questions} questions answered</p>", unsafe_allow_html=True)
    
    for question in st.session_state.questions:
        q_id = question["id"]
        
        # Create a styled container for each question
        st.markdown(f"""
        <div class="question-container">
            <div class="question-header">Question {q_id}</div>
            <div class="question-text">{question["question"]}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Bind the text area to session_state so the answer persists
        st.session_state.student_answers[q_id] = st.text_area(
            f"Your Answer (Q{q_id})", 
            value=st.session_state.student_answers.get(q_id, ""), 
            key=f"answer_{st.session_state.test_id}_{q_id}",
            height=150,
            placeholder="Type your answer here..."
        )
        
        st.markdown("<hr style='margin: 2rem 0;'>", unsafe_allow_html=True)
    
    # Center the submit button
    submit_col1, submit_col2, submit_col3 = st.columns([1, 2, 1])
    with submit_col2:
        submit_button = st.button("Submit Exam", key="submit_button", 
                                 help="Click to submit your answers")
    
    if submit_button:
        with st.spinner("Processing your submission..."):
            save_student_answers(st.session_state.test_id, student_id, st.session_state.student_answers)
            
            st.markdown("""
            <div class="info-box">
                <strong>⏳ Grading in Progress</strong><br>
                Please wait while we grade your exam...
            </div>
            """, unsafe_allow_html=True)
            
            raw_results = generate_results(st.session_state.test_id, student_id, STRICT_RUBRIC)
            if raw_results:
                save_results(st.session_state.test_id, student_id, raw_results)
                
                st.markdown("""
                <div class="success-box">
                    <strong>✅ Exam Submitted Successfully</strong><br>
                    Your exam has been graded. Redirecting to results...
                </div>
                """, unsafe_allow_html=True)
                
                st.session_state.test_id = st.session_state.test_id
                st.session_state.student_id = student_id
                st.switch_page("pages/result.py")
            else:
                st.markdown("""
                <div class="error-box">
                    <strong>⚠️ Grading Error</strong><br>
                    There was an error while grading your exam. Please try again later.
                </div>
                """, unsafe_allow_html=True)