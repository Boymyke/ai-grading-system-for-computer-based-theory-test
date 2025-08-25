# ================================
# Backend Results Functions
# ================================
from backend.query import execute_query
from dataclasses import dataclass
import json

@dataclass
class Result:
    question_id: int
    score: float 
    feedback: str

class ResultEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Result):
            return obj.__dict__
        return super().default(obj)

def save_results(test_id, student_id, results):
    """Store student test results in the database."""
    try:
        results_json = json.dumps(results, cls=ResultEncoder)
    except TypeError:
        results_json = json.dumps({"error": "Invalid results format"})
    
    query = """
        UPDATE Student_Test 
        SET result = ?, updated_at = CURRENT_TIMESTAMP
        WHERE test_id = ? AND student_id = ?
    """
    execute_query(query, (results_json, test_id, student_id), commit=True)

def get_results_by_id(test_id):
    """Retrieve student results for a specific test."""
    query = """
        SELECT u.other_names || ' ' || u.last_name AS full_name, 
               u.matric_number, 
               s.result, 
               s.id 
        FROM Student_Test s 
        JOIN User u ON s.student_id = u.id 
        WHERE s.test_id = ?
    """
    return execute_query(query, (test_id,), fetchall=True)

def get_student_results(student_id: int) -> dict | None:
    """
    Fetch all test results for the given student.
    """
    results = execute_query(
        """
        SELECT st.test_id, t.test_code, t.title, st.answers, st.result, st.created_at
        FROM Student_Test st
        JOIN Tests t ON st.test_id = t.id
        WHERE st.student_id = ?
        ORDER BY st.created_at DESC
        """,
        (student_id,), fetchall=True
    )
    
    if not results:
        return None 
        
    results_dict = {}
    for row in results:
        try:
            test_id = row[0]
            test_code = row[1]
            title = row[2]
            
            try:
                answers = json.loads(row[3]) if row[3] else {}
            except json.JSONDecodeError:
                answers = {"error": "Invalid answer format"}
                
            try:
                result = json.loads(row[4]) if row[4] else None
            except json.JSONDecodeError:
                result = {"error": "Invalid result format"}
                
            created_at = row[5]
            
            results_dict[test_id] = {
                "test_code": test_code,
                "title": title,
                "answers": answers,
                "result": result,
                "created_at": created_at
            }
        except Exception as e:
            print(f"Error processing result row: {e}")
            continue
            
    return results_dict

def get_student_result(result_id: int):
    '''Get single student result by result_id'''

    query = """
        SELECT st.id, st.test_id, st.student_id, st.answers, st.result, st.created_at,
            u.other_names || ' ' || u.last_name AS full_name, u.matric_number,
            t.title, t.test_code
        FROM Student_Test st
        JOIN User u ON st.student_id = u.id
        JOIN Tests t ON st.test_id = t.id
        WHERE st.id = ?
    """

    result_data = execute_query(query, (result_id,), fetchone=True)
    return result_data