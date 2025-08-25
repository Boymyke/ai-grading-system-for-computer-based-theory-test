import json
import streamlit as st

# ================================
# Utility Functions for Scoring
# ================================
def compute_total_score(result_json):
    """
    Computes the total score from the result JSON.
    
    The result JSON is expected to be either:
      - A dict with keys "total_score" and "details", or
      - A list of per-question entries (each with a "score" key).
      
    Returns the total score (a float) or "Pending"/"Invalid Data" on error.
    """
    try:
        # Handle case where result_json is already a dict or list
        if isinstance(result_json, (dict, list)):
            result_data = result_json
        else:
            result_data = json.loads(result_json)
            
        if isinstance(result_data, dict):
            if "total_score" in result_data:
                return result_data["total_score"]
            elif "details" in result_data and isinstance(result_data["details"], list):
                return round(sum(item.get("score", 0) for item in result_data["details"]), 2)
        elif isinstance(result_data, list):
            return round(sum(item.get("score", 0) for item in result_data), 2)
        
        return "Pending"
    except (json.JSONDecodeError, TypeError, Exception) as e:
        st.error(f"Error computing total score: {e}")
        return "Invalid Data"

def compute_total_obtainable_score(questions_json):
    """
    Computes the total obtainable score by summing the 'max_score' of each question.
    Each question is expected to have a 'max_score' key.
    
    Returns the total obtainable score (a float) or "Invalid Data" on error.
    """
    try:
        if isinstance(questions_json, str):
            questions = json.loads(questions_json)
        else:
            questions = questions_json
            
        # Handle case where questions is a tuple (like from database query)
        if isinstance(questions, tuple) and len(questions) > 0:
            questions = questions[0]
            
        # Handle case where questions is a JSON string within the tuple/list
        if isinstance(questions, str):
            questions = json.loads(questions)
            
        # Handle both dict and list formats
        if isinstance(questions, dict):
            # Check if it's a single question dict
            if "max_score" in questions:
                return round(questions.get("max_score", 2.0), 2)
            
            # Otherwise, it's a dict of questions
            question_list = []
            for key in questions:
                if isinstance(questions[key], dict):
                    question_list.append(questions[key])
                elif isinstance(questions[key], str):
                    try:
                        q = json.loads(questions[key])
                        if isinstance(q, dict):
                            question_list.append(q)
                    except:
                        pass
            
            return round(sum(q.get("max_score", 2.0) for q in question_list), 2)
        elif isinstance(questions, list):
            return round(sum(q.get("max_score", 2.0) for q in questions if isinstance(q, dict)), 2)
            
        return "Invalid Data"
    except (json.JSONDecodeError, TypeError, Exception) as e:
        st.error(f"Error computing total obtainable score: {e}")
        return "Invalid Data"

def normalize_questions(questions):
    """
    Convert questions into a list of dictionaries.
    
    - If 'questions' is a dict with keys like "id", "question", etc., we wrap it in a list.
    - If it's a mapping (dict with non-standard keys), we sort its keys and process each value.
    - If it's a list, we try to ensure each element is a dict (parsing JSON strings if necessary).
    - Invalid or empty entries are skipped.
    """
    normalized = []
    
    # Handle tuple from database query
    if isinstance(questions, tuple) and len(questions) > 0:
        questions = questions[0]
        
    # Handle JSON string
    if isinstance(questions, str):
        try:
            questions = json.loads(questions)
        except json.JSONDecodeError as e:
            st.error(f"Error parsing questions JSON: {e}")
            return []
    
    # Single question case: a dict with expected keys.
    expected_keys = {"id", "question", "model_answer", "max_score"}
    if isinstance(questions, dict):
        if any(key in questions for key in expected_keys):
            return [questions]
        else:
            try:
                # Attempt to sort keys numerically; if fails, sort alphabetically.
                try:
                    keys = sorted(questions, key=lambda k: int(k))
                except Exception:
                    keys = sorted(questions.keys())
                for k in keys:
                    q = questions[k]
                    if isinstance(q, dict):
                        normalized.append(q)
                    elif isinstance(q, str):
                        if not q.strip():
                            st.info(f"Skipping empty question for key {k}.")
                            continue
                        try:
                            parsed = json.loads(q)
                            if isinstance(parsed, dict):
                                normalized.append(parsed)
                            else:
                                st.error(f"Parsed question for key {k} is not a dict: {parsed}")
                        except Exception as e:
                            st.error(f"Error parsing question string for key {k}: {e}")
                    else:
                        st.error(f"Skipping question with key {k} of invalid type: {type(q)}")
            except Exception as e:
                st.error(f"Error processing questions dict: {e}")
            return normalized
    elif isinstance(questions, list):
        for idx, q in enumerate(questions):
            if isinstance(q, dict):
                normalized.append(q)
            elif isinstance(q, str):
                if not q.strip():
                    st.info(f"Skipping empty question at index {idx}.")
                    continue
                try:
                    parsed = json.loads(q)
                    if isinstance(parsed, dict):
                        normalized.append(parsed)
                    else:
                        st.error(f"Parsed question at index {idx} is not a dict: {parsed}")
                except Exception as e:
                    st.error(f"Error parsing question string at index {idx}: {e}")
            else:
                st.error(f"Skipping question at index {idx} of invalid type: {type(q)}")
        return normalized
    else:
        st.error(f"Questions data is neither a list nor a dict: {type(questions)}")
        return []

def normalize_grading_results(grading_results):
    """
    Convert grading_results into a list of dictionaries.
    
    - If grading_results is a JSON string, parse it.
    - If it's a list, ensure each element is a dict (parsing if necessary).
    - Invalid entries are skipped.
    """
    normalized = []
    
    # Handle None case
    if grading_results is None:
        return []
        
    if isinstance(grading_results, str):
        try:
            parsed = json.loads(grading_results)
            if isinstance(parsed, list):
                normalized = parsed
            elif isinstance(parsed, dict):
                # Check if it has a 'details' field with results
                if "details" in parsed and isinstance(parsed["details"], list):
                    normalized = parsed["details"]
                else:
                    normalized = [parsed]
        except Exception as e:
            st.error(f"Error parsing grading_results: {e}")
            return []
    elif isinstance(grading_results, list):
        for idx, item in enumerate(grading_results):
            if isinstance(item, dict):
                normalized.append(item)
            elif isinstance(item, str):
                try:
                    parsed = json.loads(item)
                    if isinstance(parsed, dict):
                        normalized.append(parsed)
                    else:
                        st.error(f"Parsed grading result at index {idx} is not a dict: {parsed}")
                except Exception as e:
                    st.error(f"Error parsing grading result string at index {idx}: {e}")
            else:
                st.error(f"Skipping grading result at index {idx} of invalid type: {type(item)}")
    elif isinstance(grading_results, dict):
        # Check if it has a 'details' field with results
        if "details" in grading_results and isinstance(grading_results["details"], list):
            normalized = grading_results["details"]
        else:
            normalized = [grading_results]
    else:
        st.error(f"grading_results is neither a str, list, nor dict: {type(grading_results)}")
        
    return normalized

def display_one_result(questions, student_answers, grading_results):
    """
    Displays detailed results for a single student's exam.
    
    - 'questions' should be a list (or a dict representing one question) of question data.
    - 'student_answers' maps question IDs (as strings) to answers.
    - 'grading_results' contains per-question grading details.
    """
    # Check for None or empty inputs
    if not questions:
        st.warning("No questions available.")
        return
        
    if not student_answers:
        st.warning("No student answers available.")
    
    # Normalize questions and grading results.
    questions = normalize_questions(questions)
    grading_results = normalize_grading_results(grading_results)
    
    for question in questions:
        try:
            q_id = str(question.get("id", ""))
            if not q_id:
                st.error("Question missing ID")
                continue
        except Exception as e:
            st.error(f"Error processing question: {e}")
            continue
            
        st.markdown(f"### Question {q_id}")
        st.write(question.get("question", "No question text available."))
        
        st.markdown("**Your Answer:**")
        answer = student_answers.get(q_id, "No answer provided.")
        st.write(answer)
        
        if grading_results:
            # Find grading entry matching this question.
            result_for_q = next((
                item for item in grading_results 
                if str(item.get("question_id", "")) == q_id
            ), None)
            
            if not result_for_q:
                # Try alternative field names that might contain the question ID
                result_for_q = next((
                    item for item in grading_results 
                    if (str(item.get("id", "")) == q_id or 
                        str(item.get("qid", "")) == q_id or
                        str(item.get("question", "")) == q_id)
                ), None)
                
            if result_for_q:
                st.markdown("**Score:**")
                score = result_for_q.get("score", "N/A")
                max_score = question.get("max_score", 2.0)
                st.write(f"{score} / {max_score}")
                
                st.markdown("**Feedback:**")
                st.write(result_for_q.get("feedback", "No feedback provided."))
            else:
                st.info("No grading info available for this question.")
        else:
            st.info("This exam has not been graded yet.")

def display_results(test_id):
    """
    Displays all student results for the selected test.
    
    - Retrieves student results and questions.
    - Computes total obtainable score.
    - Displays results in a table with a 'View' button for details.
    """
    from backend.results import get_results_by_id  # Import here to avoid circular imports
    from backend.tests import get_questions
    
    student_results = get_results_by_id(test_id)
    
    if not student_results:
        st.warning("No results available for this test.")
        return
        
    questions_json = get_questions(test_id)
    total_obtainable_score = compute_total_obtainable_score(questions_json) if questions_json else "N/A"
    
    st.write("### Student Results")
    header_cols = st.columns([1, 3, 3, 2, 2])
    header_cols[0].write("S/N")
    header_cols[1].write("Full Name")
    header_cols[2].write("Matric Number")
    header_cols[3].write(f"Total Score ({total_obtainable_score})")
    header_cols[4].write("View Details")
    
    for i, r in enumerate(student_results):
        try:
            full_name, matric_number, result_json, result_id = r
            row_cols = st.columns([1, 3, 3, 2, 2])
            row_cols[0].write(i + 1)
            row_cols[1].write(full_name or "N/A")
            row_cols[2].write(matric_number or "N/A")
            
            score = compute_total_score(result_json)
            row_cols[3].write(score)
            
            if row_cols[4].button("View", key=f"view_{result_id}"):
                st.session_state.result_id = result_id
                st.switch_page("pages/student_result.py")
        except Exception as e:
            st.error(f"Error displaying result row {i+1}: {e}")