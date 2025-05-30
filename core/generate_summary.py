from core.model import generate_response
from core.test import resume, jd, jr, questions,ai_answers,user_answers,scores

def generate_summary_content(resume_text, job_desc_text, job_role, questions_list, 
                           user_answers, ai_answers, scores):
    """Generate just the dynamic content pieces for the summary"""
    
    system_prompt = """
    You are an interview analysis expert. Your task is to analyze interview performance data and 
    generate specific content sections that will be inserted into a fixed report template.
    
    You will generate JSON output containing ONLY the requested sections. For each section,
    write concise, insightful content based on the provided data.
    
    The output must be valid JSON with these exact keys: strengths, weaknesses, trends, resources, comparison_table.
    """
    
    user_prompt = f"""
    Based on this interview data:
    
    - Resume: {resume_text}
    - Job Description: {job_desc_text} 
    - Role: {job_role}
    - Questions: {questions_list}
    - User Answers: {user_answers}
    - AI Answers: {ai_answers}
    - Scores: {scores}
    
    Generate ONLY the following sections for our report (structured as a JSON object):
    
    1. "strengths": A markdown list of 2-5 specific strengths demonstrated by the user
    2. "weaknesses": A markdown list of 2-5 specific mistakes or gaps in the user's answers
    3. "trends": A 2-3 sentence paragraph summarizing trends from the interview
    4. "resources": A markdown list of 2-5 useful links with descriptions (use proper markdown link format)
    5. "comparison_table": An array of objects, one per question, each with:
       - "question": The question text
       - "differences": Key differences between user and AI answers (1-2 sentences)
       - "strong_phrases": Notable strong phrases or points from either answer (comma separated)
    6. "topics_covered : return 5 or more keywords of topics covered in questions"
    
    Return ONLY a JSON object with these exact keys.

    Don't add ```json or ``` 
    Do not include single and double quotation inside the sentences
    """

    response=generate_response(system_prompt,user_prompt)
    return response
    
if __name__ == "__main__":
    print(generate_summary_content(resume, jd, jr, questions,ai_answers,user_answers,scores))