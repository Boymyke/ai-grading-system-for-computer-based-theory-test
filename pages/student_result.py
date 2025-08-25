import streamlit as st
import json
from backend.results import get_student_result
from backend.tests import get_questions
from modules.utils.result_utilities import compute_total_score, display_one_result, compute_total_obtainable_score
from backend.user import get_user_profile_by_email, update_user_info

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
        background-color: white;
        padding: 1.2rem;
        border-radius: 8px;
        margin-bottom: 1rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    .test-info {
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
        margin-top: 0.5rem;
    }
    .result-card {
        background-color: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        margin-bottom: 1.5rem;
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
        padding: 1.2rem;
        border-radius: 8px;
        margin-bottom: 1.5rem;
        border-left: 4px solid #0068c9;
    }
    .answer-section {
        background-color: white;
        padding: 1rem;
        border-radius: 5px;
        margin-top: 0.8rem;
        margin-bottom: 0.8rem;
    }
    .feedback-section {
        background-color: #f0f8ff;
        padding: 1rem;
        border-radius: 5px;
        margin-top: 0.8rem;
        border-left: 4px solid #ffa62b;
    }
    .score-section {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        background-color: #f0f2f6;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        margin-top: 0.5rem;
        width: fit-content;
    }
    .back-button {
        background-color: #f0f2f6;
        padding: 0.8rem;
        border-radius: 8px;
        text-align: center;
        margin-bottom: 1rem;
        transition: background-color 0.3s;
    }
    .back-button:hover {
        background-color: #e0e2e6;
    }
    .divider {
        height: 1px;
        background-color: #e0e2e6;
        margin: 1.5rem 0;
    }
    .not-graded {
        color: #ffa62b;
    }
</style>
""", unsafe_allow_html=True)

# Page title with enhanced styling
st.markdown("<h1 style='margin-bottom: 1.5rem;'>Student Result Details</h1>", unsafe_allow_html=True)

if "user_id" not in st.session_state:
    st.warning("Please [log in](login) first.")
    st.stop()

user_id = st.session_state.get("user_id")

# Enhanced sidebar with styled back button
with st.sidebar:
    st.markdown("""
    <div class="back-button" onclick="window.location.href='results'">
        ← Back to Results
    </div>
    """, unsafe_allow_html=True)
    # Keep the original button for functionality
    if st.button("← Back to Results", key="back_button"):
        st.switch_page("pages/results.py")

if "result_id" not in st.session_state:
    query_params = st.experimental_get_query_params()
    if "id" in query_params:
        st.session_state.result_id = query_params["id"][0]
    else:
        st.error("No result ID provided.")
        st.stop()

result_id = st.session_state.result_id

result_data = get_student_result(result_id)

if not result_data:
    st.error("Result not found.")
    st.stop()

result_id, test_id, student_id, answers_json, result_json, created_at, full_name, matric_number, test_title, test_code = result_data

questions_json = get_questions(test_id)

try:
    answers = json.loads(answers_json) if answers_json else {}
except Exception as e:
    st.error(f"Error parsing answers: {str(e)}")
    answers = {}

try:
    grading_results = json.loads(result_json) if result_json else None
except Exception as e:
    st.error(f"Error parsing grading results: {str(e)}")
    grading_results = None

# Enhanced student and test info card
st.markdown(f"""
<div class="main-header">
    <div class="student-info">
        <h2>{full_name}</h2>
        <p><strong>Matric Number:</strong> {matric_number}</p>
    </div>
    <div class="test-info">
        <p><strong>Test:</strong> {test_title} ({test_code})</p>
        <p><strong>Taken on:</strong> {created_at}</p>
    </div>
</div>
""", unsafe_allow_html=True)

try:
    questions = json.loads(questions_json) if isinstance(questions_json, str) else questions_json
    total_obtainable = compute_total_obtainable_score(questions)
except Exception as e:
    st.error(f"Error parsing questions: {str(e)}")
    questions = []
    total_obtainable = "N/A"

# Score card with visual elements
if grading_results:
    try:
        if isinstance(grading_results, str):
            total_score = compute_total_score(grading_results)
        else:
            total_score = compute_total_score(json.dumps(grading_results))
            
        # Calculate percentage for progress bar
        if isinstance(total_obtainable, (int, float)) and total_obtainable > 0:
            score_percentage = (total_score / total_obtainable) * 100
        else:
            score_percentage = 0
            
        st.markdown(f"""
        <div class="result-card">
            <div class="score-display">
                {total_score} / {total_obtainable} Points
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Add progress bar for visual representation
        st.progress(score_percentage/100)
        st.markdown(f"<p style='text-align: center;'>{score_percentage:.1f}%</p>", unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error computing score: {str(e)}")
        st.markdown("""
        <div class="result-card">
            <div class="score-display" style="color: #ff4b4b;">
                Could not compute score
            </div>
        </div>
        """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div class="result-card">
        <div class="score-display not-graded">
            Not graded yet
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
st.markdown("<h2>Detailed Results per Question</h2>", unsafe_allow_html=True)

# Try to use the original display function first
try:
    with st.expander("View All Questions", expanded=True):
        display_one_result(questions, answers, grading_results)
except Exception as e:
    st.error(f"Error displaying results: {str(e)}")
    
    # Fallback to custom display if the original function fails
    if questions:
        for question in questions:
            if isinstance(question, dict):
                q_id = str(question.get("id", ""))
                if q_id:
                    # Enhanced question card
                    st.markdown(f"""
                    <div class="question-card">
                        <h3>Question {q_id}</h3>
                        <p>{question.get("question", "No question text available.")}</p>
                        
                        <div class="answer-section">
                            <strong>Student Answer:</strong>
                            <p>{answers.get(q_id, "No answer provided.")}</p>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    if grading_results:
                        if isinstance(grading_results, list):
                            result_item = next((r for r in grading_results if str(r.get("question_id", "")) == q_id), None)
                        elif isinstance(grading_results, dict):
                            result_item = grading_results.get(q_id, None)
                        else:
                            result_item = None
                            
                        if result_item:
                            score = result_item.get("score", "N/A")
                            max_score = question.get("max_score", 2.0)
                            
                            # Score display
                            st.markdown(f"""
                            <div class="score-section">
                                <strong>Score:</strong> {score} / {max_score}
                            </div>
                            """, unsafe_allow_html=True)
                            
                            # Feedback section
                            feedback = result_item.get("feedback", "No feedback provided.")
                            st.markdown(f"""
                            <div class="feedback-section">
                                <strong>Feedback:</strong>
                                <p>{feedback}</p>
                            </div>
                            """, unsafe_allow_html=True)
                        else:
                            st.markdown("""
                            <div class="answer-section" style="background-color: #fff8e1;">
                                <p>No grading info available for this question.</p>
                            </div>
                            """, unsafe_allow_html=True)
                    else:
                        st.markdown("""
                        <div class="answer-section" style="background-color: #fff8e1;">
                            <p>This question has not been graded yet.</p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # Close the question card div
                    st.markdown("</div>", unsafe_allow_html=True)