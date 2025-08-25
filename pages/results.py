import streamlit as st
import json
import time
from backend.user import get_first_name_by_email, get_user_type_by_id
from backend.results import get_results_by_id
from backend.tests import get_questions, get_tests_by_id
from modules.utils.result_utilities import (
    compute_total_score, 
    compute_total_obtainable_score,
)
from backend.user import get_first_name_by_email, update_user_info, get_user_profile_by_email
from modules.export_result import export_results

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
    .test-info {
        background-color: white;
        padding: 1.2rem;
        border-radius: 8px;
        margin-bottom: 1rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    .sidebar-content {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
    }
    .table-header {
        background-color: #f0f2f6;
        padding: 10px 0;
        border-radius: 5px;
        margin-bottom: 10px;
        font-weight: bold;
    }
    .table-row {
        padding: 8px 0;
        border-bottom: 1px solid #f0f0f0;
        margin-bottom: 5px;
    }
    .table-row:hover {
        background-color: #f9f9f9;
    }
    .score-cell {
        font-weight: bold;
        padding: 4px 8px;
        border-radius: 4px;
        text-align: center;
        display: inline-block;
        min-width: 40px;
    }
    .score-high {
        background-color: #e6f7e6;
        color: #00a86b;
    }
    .score-medium {
        background-color: #e6f0ff;
        color: #0068c9;
    }
    .score-low {
        background-color: #fff2e6;
        color: #ff8c00;
    }
    .score-very-low {
        background-color: #ffe6e6;
        color: #ff4b4b;
    }
    .score-not-graded {
        background-color: #f0f0f0;
        color: #666666;
    }
    .table-container {
        background-color: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        margin-top: 1.5rem;
    }
    .stButton > button {
        background-color: #0068c9;
        color: white;
        border: none;
        border-radius: 4px;
        padding: 5px 10px;
        width: 100%;
    }
    .stButton > button:hover {
        background-color: #d5ecfa;
    }
</style>
""", unsafe_allow_html=True)

# Verify user is logged in and is a teacher
teacher_id = st.session_state.get("user_id")
if not teacher_id:
    st.warning("Please [log in](login) first.")
    st.stop()
    
email = st.session_state.get("email", None)
if not email:
    st.warning("Session information missing. Please log in again.")
    st.stop()
    
# Get user info and verify they're a teacher
user_type = get_user_type_by_id(teacher_id)
if user_type != "teacher":
    st.warning("This page is only accessible to teachers.")
    with st.spinner("Redirecting to appropriate dashboard..."):
        time.sleep(2)
    st.switch_page("pages/student.py")
    st.stop()
    
name = get_first_name_by_email(email)
user = get_user_profile_by_email(email)

# Main content with enhanced styling
st.markdown("<h1 style='margin-bottom: 1.5rem;'>Student Test Results</h1>", unsafe_allow_html=True)

# Get all test results (all tests created by this teacher)
teacher_tests = get_tests_by_id(teacher_id)
if not teacher_tests:
    st.info("No tests found. Create a test to see results here.")
    with st.spinner("Redirecting to dashboard..."):
        time.sleep(2)
    st.switch_page("pages/teacher.py")
    st.stop()

# Enhanced sidebar
with st.sidebar:
    st.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
    st.markdown("<h3>📊 Select Test</h3>", unsafe_allow_html=True)
    
    # Fixed: proper dictionary comprehension for test options
    test_options = {test[0]: f"{test[2]} ({test[1]})" for test in teacher_tests}
    
    selected_test_id = st.selectbox(
        "Choose a test",
        options=list(test_options.keys()),
        format_func=lambda tid: test_options[tid]
    )

    if st.button("Go to dashboard", use_container_width=True):
        st.switch_page("pages/teacher.py")
    st.markdown('</div>', unsafe_allow_html=True)

if selected_test_id:
    # Get test details
    test_info = next((t for t in teacher_tests if t[0] == selected_test_id), None)
    if test_info:
        test_id, test_code, title, created_at = test_info
        
        # Enhanced test info card
        st.markdown(f"""
        <div class="main-header">
            <div class="test-info">
                <h2>{title}</h2>
                <p><strong>Test Code:</strong> {test_code}</p>
                <p><strong>Created on:</strong> {created_at}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Get test questions
        questions_data = get_questions(test_id)
        if not questions_data:
            st.error("Test questions not found.")
            st.stop()
        
        # Get all student results for this test
        student_results = get_results_by_id(test_id)
        
        if not student_results:
            st.info("No students have taken this test yet.")
            st.stop()
        
        # Calculate total obtainable score
        total_obtainable = compute_total_obtainable_score(questions_data)
        
        # Display results in a styled table
        st.markdown("<h3>Results Summary</h3>", unsafe_allow_html=True)
        
        # Create a container for the table
        st.markdown('<div class="table-container">', unsafe_allow_html=True)
        
        # Create table header with Streamlit columns
        cols = st.columns([1, 3, 2, 2, 2])
        cols[0].markdown('<div class="table-header">#</div>', unsafe_allow_html=True)
        cols[1].markdown('<div class="table-header">Student Name</div>', unsafe_allow_html=True)
        cols[2].markdown('<div class="table-header">ID/Matric</div>', unsafe_allow_html=True)
        cols[3].markdown(f'<div class="table-header">Score (/{total_obtainable})</div>', unsafe_allow_html=True)
        cols[4].markdown('<div class="table-header">Actions</div>', unsafe_allow_html=True)
        
        # Display student results
        for i, result in enumerate(student_results):
            try:
                full_name, matric_number, result_json, result_id = result
                
                # Calculate score and determine color class
                score_class = "score-not-graded"
                score_display = "Not graded"
                
                if result_json:
                    try:
                        score = compute_total_score(result_json)
                        score_display = str(score)
                        
                        # Calculate percentage for color coding
                        if isinstance(total_obtainable, (int, float)) and total_obtainable > 0:
                            percentage = (score / total_obtainable) * 100
                            
                            if percentage >= 80:
                                score_class = "score-high"
                            elif percentage >= 60:
                                score_class = "score-medium"
                            elif percentage >= 40:
                                score_class = "score-low"
                            else:
                                score_class = "score-very-low"
                        
                    except Exception as e:
                        score_display = "Error"
                        score_class = "score-not-graded"
                
                # Create row with Streamlit columns
                row = st.columns([1, 3, 2, 2, 2])
                row[0].markdown(f'<div class="table-row">{i+1}</div>', unsafe_allow_html=True)
                row[1].markdown(f'<div class="table-row">{full_name or "Unknown"}</div>', unsafe_allow_html=True)
                row[2].markdown(f'<div class="table-row">{matric_number or "N/A"}</div>', unsafe_allow_html=True)
                row[3].markdown(f'<div class="table-row"><span class="score-cell {score_class}">{score_display}</span> / {total_obtainable}</div>', unsafe_allow_html=True)
                
                # Use Streamlit's native button for the action
                if row[4].button("View Details", key=f"view_{result_id}"):
                    # Store the result_id in session state
                    st.session_state.result_id = result_id
                    # Redirect to student_result.py page
                    st.switch_page("pages/student_result.py")
                
            except Exception as e:
                st.error(f"Error displaying result: {str(e)}")
        
        st.markdown('</div>', unsafe_allow_html=True)
else:
    st.info("Select a test from the sidebar to view results.")

export_format = st.selectbox("Select export format:", ["CSV", "PDF"], key="export_format")

student_results_for_export = [
    (full_name, matric_number, compute_total_score(result_json) if result_json else "Not Graded", result_json)
    for full_name, matric_number, result_json, result_id in student_results
]

if st.button("Export Results"):
    export_results(student_results_for_export, export_format)
