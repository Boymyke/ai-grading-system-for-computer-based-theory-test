import json
import random
import string
from dataclasses import dataclass
from typing import List

from backend.query import execute_query

@dataclass
class Question:
    id: int
    question: str
    model_answer: str
    max_score: float

@dataclass
class Test:
    title: str
    description: str
    questions: List[Question]
    created_at: str = None

def create_test_from_existing(existing_test_id: int) -> Test:
    query = "SELECT title, description, questions_data FROM Tests WHERE id = ?"
    result = execute_query(query, (existing_test_id,), fetchone=True)

    if result:
        title, description, questions_json = result
        questions_data = json.loads(questions_json)
        
        return Test(
            title=title,
            description=description,
            questions=[Question(**q) for q in questions_data]
        )
    return None

def get_questions(test_id: int):
    """Retrieve questions from the Tests table."""
    result = execute_query("SELECT questions_data FROM Tests WHERE id = ?", (test_id,), fetchone=True)
    return json.loads(result[0]) if result else None

def get_student_answers(test_id: int, student_id: int):
    """Retrieve student answers for a specific test."""
    result = execute_query("SELECT answers FROM Student_Test WHERE test_id = ? AND student_id = ?", 
                           (test_id, student_id), fetchone=True)
    return json.loads(result[0]) if result else None

def get_tests_by_id(user_id):
    """Retrieve tests created by a specific teacher."""
    query = "SELECT id, test_code, title, created_at FROM Tests WHERE teacher_id = ?"
    result = execute_query(query, (user_id,), fetchall=True)
    
    return [tuple(row) for row in result] if result else []



def save_test(teacher_id, test_code, title, description, questions, strict):
    """Save a new test into the database with strictness option."""
    questions_list = [
        {
            "id": q.get("id"),
            "question": q.get("question"),
            "model_answer": q.get("model_answer"),
            "max_score": q.get("max_score")
        }
        for q in questions
    ]
    
    questions_json = json.dumps(questions_list)

    query = """
        INSERT INTO Tests (teacher_id, test_code, title, description, questions_data, strict)
        VALUES (?, ?, ?, ?, ?, ?)
    """
    
    try:
        execute_query(query, (teacher_id, test_code, title, description, questions_json, int(strict)), commit=True)
        return True  
    except Exception as e:
        print("Error saving test:", e)
        return False

def get_test_data(test_code):
    """Retrieve test details using the exam code."""
    return execute_query("SELECT id, questions_data FROM Tests WHERE test_code = ?", (test_code,), fetchone=True)

def check_previous_attempt(test_id, student_id):
    """Check if a student has already taken the exam."""
    return execute_query("SELECT answers FROM Student_Test WHERE test_id = ? AND student_id = ?", (test_id, student_id), fetchone=True)

def save_student_answers(test_id, student_id, student_answers):
    """Save or update student answers in the database."""
    query = """
        INSERT INTO Student_Test (test_id, student_id, answers, updated_at) 
        VALUES (?, ?, ?, CURRENT_TIMESTAMP)
        ON CONFLICT(test_id, student_id) 
        DO UPDATE SET answers = excluded.answers, updated_at = CURRENT_TIMESTAMP
    """
    execute_query(query, (test_id, student_id, json.dumps(student_answers)))

