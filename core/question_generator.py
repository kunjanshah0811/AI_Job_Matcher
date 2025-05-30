from model import generate_response
from test import resume,jd,jr
from utils import trim_backticks

import json

def generate_question(resume_text, job_desc_text, job_role):
    system_prompt = "You are a question generator API, you always respond is correct, directly parsable JSON. You are an experienced technical interviewer and question generator. " \
    "You create professional interview questions in a JSON format. Never include explanations, markdown formatting, or any text outside the JSON"
    
    user_prompt = f"""
    Generate 5 technical interview questions for a "{job_role}" position based on this resume and job description.
    
    Resume:
    {resume_text}

    Job Description:
    {job_desc_text}

    IMPORTANT FORMATTING INSTRUCTIONS:
    1. Return ONLY a raw directly parsable JSON
    2. Do NOT use markdown formatting
    3. Do NOT include ```json or ``` markers
    4. Do NOT add any explanations or comments
    5. Output ONLY the JSON with questions
    
    Each question should test technical skills and include a follow-up in parentheses.
    
    Example of EXACTLY how your response should be formatted:
    {{
    questions:  ["Question 1 (Follow-up question)", "Question 2 (Follow-up question)", "Question 3 (Follow-up question)", "Question 4 (Follow-up question)", "Question 5 (Follow-up question)"]
    }}
    """

    fallback_questions=  [
        "Tell me about your relevant experience for this role.",
        "What are your key strengths and weaknesses?",
        "Why are you interested in this position?",
        "Describe a challenging project you've worked on.",
        "What questions do you have about the role?"
    ]
    # Use generate_response instead of direct client call
    try:
        response = generate_response(system_prompt, user_prompt, temp=0.7)
        # print(response)

        if response.startswith("```"):
            response = trim_backticks(response)
        
        parsed_response = json.loads(response)
        return parsed_response["questions"]
    
    except Exception as e :
        print(f"Error {e}")
        return fallback_questions

if __name__=="__main__":
    questions=generate_question(resume,jd,jr)
    print(questions)
