import streamlit as st
import json
import time
from backend.user import get_first_name_by_email, get_user_type_by_id
from backend.results import get_student_results
from backend.tests import get_questions
from modules.utils.result_utilities import compute_total_score, display_one_result, compute_total_obtainable_score
from backend.user import get_first_name_by_email, get_user_profile_by_email

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1.5rem;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    .student-info {
        display: flex;
        align-items: center;
        margin-bottom: 0.5rem;
    }
    .result-card {
        background-color: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    .score-display {
        font-size: 1.8rem;
        font-weight: bold;
        color: #0068c9;
        text-align: center;
        margin: 1rem 0;
    }
    .question-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
        border-left: 4px solid #0068c9;
    }
    .answer-section {
        background-color: white;
        padding: 0.8rem;
        border-radius: 5px;
        margin-top: 0.5rem;
    }
    .correct-answer {
        border-left: 4px solid #00c16e;
    }
    .incorrect-answer {
        border-left: 4px solid #ff4b4b;
    }
    .sidebar-content {
        padding: 1rem;
        background-color: #f0f2f6;
        border-radius: 8px;
    }
    .dashboard-btn {
        width: 100%;
        margin-top: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Verify user is logged in
student_id = st.session_state.get("user_id")
if not student_id:
    st.warning("Please [log in](login) first.")
    st.stop()
    
email = st.session_state.get("email", None)
if email:
    name = get_first_name_by_email(email)
    user = get_user_profile_by_email(email)
    if user:
        student_id, last_name, other_names, user_type, matric_number, _ = user
    
    # Enhanced header with student info
    st.markdown(f"""
    <div class="main-header">
        <h1>{name}'s Test Results</h1>
        <div class="student-info">
            <p><strong>Matric Number:</strong> {matric_number if matric_number else 'N/A'}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    results_data = get_student_results(student_id)
    if not results_data:
        st.info("No exam results found.")
        if st.button("Go to dashboard", key="dashboard_empty"):
            st.switch_page("pages/student.py")
        st.stop()
        
    with st.sidebar:
        st.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
        st.subheader("Exam Selection")
        selected_test_id = st.selectbox(
            "Select an exam",
            options=list(results_data.keys()),
            format_func=lambda tid: f"{results_data[tid]['title']} ({results_data[tid]['test_code']})"
        )
        
        if st.button("Go to dashboard", key="dashboard_sidebar", use_container_width=True):
            st.switch_page("pages/student.py")
        st.markdown('</div>', unsafe_allow_html=True)
    
    selected_exam = results_data[selected_test_id]
    test_row = get_questions(selected_test_id)
    if not test_row:
        st.error("Test questions not found.")
        st.stop()
        
    questions = test_row
    student_answers = selected_exam["answers"]
    grading_results = selected_exam["result"]
    
    # Exam details card
    st.markdown(f"""
    <div class="result-card">
        <h2>Exam: {selected_exam['title']} ({selected_exam['test_code']})</h2>
        <p><strong>Taken on:</strong> {selected_exam['created_at']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Calculate total obtainable score
    total_obtainable_score = compute_total_obtainable_score(questions)
    
    # Calculate total score
    if grading_results:
        total_score = compute_total_score(grading_results)
        score_percentage = (total_score / total_obtainable_score) * 100 if total_obtainable_score > 0 else 0
        
        # Score card with progress bar
        st.markdown(f"""
        <div class="result-card">
            <div class="score-display">
                {total_score} / {total_obtainable_score} Points
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Add progress bar for visual representation
        st.progress(score_percentage/100)
        st.markdown(f"<p style='text-align: center;'>{score_percentage:.1f}%</p>", unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="result-card">
            <div class="score-display" style="color: #ffa62b;">
                Not Graded Yet
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Display detailed results
    st.markdown("<h2>Detailed Results</h2>", unsafe_allow_html=True)
    
    if grading_results:
        # We'll keep the original display_one_result function for functionality
        # but wrap it in an expander for better organization
        with st.expander("View Question Details", expanded=True):
            display_one_result(questions, student_answers, grading_results)
    else:
        st.info("This exam has not been graded yet.")
        
        # Still display questions and answers even if not graded
        normalized_questions = []
        try:
            from modules.utils.result_utilities import normalize_questions
            normalized_questions = normalize_questions(questions)
        except Exception as e:
            st.error(f"Error normalizing questions: {e}")
            
        if normalized_questions:
            st.markdown("<h3>Your Answers</h3>", unsafe_allow_html=True)
            for question in normalized_questions:
                q_id = str(question.get("id", ""))
                if q_id:
                    st.markdown(f"""
                    <div class="question-card">
                        <h4>Question {q_id}</h4>
                        <p>{question.get("question", "No question text available.")}</p>
                        <div class="answer-section">
                            <strong>Your Answer:</strong>
                            <p>{student_answers.get(q_id, "No answer provided.")}</p>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)