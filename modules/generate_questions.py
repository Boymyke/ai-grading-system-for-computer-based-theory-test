import google.generativeai as genai
from google.ai.generativelanguage_v1beta.types import content
import json
import re
from dataclasses import dataclass
from typing import List
import streamlit as st

from backend.tests import Question

GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=GEMINI_API_KEY)

generation_config = {
    "temperature": 1,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

def generate_questions(num_questions: int, course_material: str) -> List[Question]:
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config
    )

    prompt = f"""
    Given the following course content, generate {num_questions} theory questions that test understanding.
    Return strictly as JSON array:
    [
        {{
            "question": "theory question",
            "model_answer": "correct answer"
        }}
    ]

    Course Content: {course_material}
    """

    response = model.generate_content(prompt).text
    response = re.sub(r"^```json|```$", "", response).strip()

    try:
        questions_data = json.loads(response)
        questions = [
                Question(id=i+1, 
                        question=q["question"], 
                        model_answer=q["model_answer"], 
                        max_score=2.0) 
                for i, q in enumerate(questions_data)
            ]

        return questions
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        return []
