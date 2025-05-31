from core.model import generate_response
import json
from typing import List
from core.utils import trim_backticks, Collect_score


SYS_PROMPT= """
You are Scorer API. You always respond in proper, directly parsable JSON.
You are a highly accurate, impartial, JSON-only scoring system. 
Your sole task is to evaluate two written answers to the same question: one from a user and one from a competitor.

You are provided with the following input:
- job_description: a role-specific job description that defines the expected skills, tone, and content quality.
- question: an open-ended prompt relevant to the job.
- user: the user's written answer to the question.
- competitor: the competitor's written answer to the same question.

Evaluate each answer based on the rubric and **how well it aligns with the job description**.

Rubric criteria (each scored from 0-5):
1. structure_star - Logical organization and coherence.
2. depth - Insight, reasoning, and sophistication, especially in relation to the job requirements.
3. clarity - How clear, readable, and accessible the response is.
4. correctness - Factual and conceptual accuracy, including relevance to the job description.

Important:
- Improvement tip should be less than 25 words.
Your output must strictly follow this **parsable JSON format**:

{
  "user": {
    "structure_star": {"score": 0-5, "improvement_tip": "STRING"},
    "depth": {"score": 0-5, "improvement_tip": "STRING"},
    "clarity": {"score": 0-5, "improvement_tip": "STRING"},
    "correctness": {"score": 0-5, "improvement_tip": "STRING"}
  },
  "competitor": {
    "structure_star": {"score": 0-5, "improvement_tip": "STRING"},
    "depth": {"score": 0-5, "improvement_tip": "STRING"},
    "clarity": {"score": 0-5, "improvement_tip": "STRING"},
    "correctness": {"score": 0-5, "improvement_tip": "STRING"}
  }
}

Only output a valid JSON object. Do not include any commentary, headers, or extra text outside of the JSON.

"""
    

def scorer(jd:str, ques: str, user: str, competitor: str):
    user_prompt = f"""
        You are Scorer API.
        Please evaluate the following answers based on the rubric criteria (structure_star, depth, clarity, correctness), considering the job description provided. 
        Return a **valid, strictly formatted JSON object** as described.

        job_description:
        {jd}

        question:
        {ques}

        user:
        {user}

        competitor:
        {competitor}
    """
    response = generate_response(system_prompt=SYS_PROMPT, user_prompt=user_prompt, temp=0.1)
    print("Model Executed")
    if response.startswith("```"):
        response = trim_backticks(response)
    
    parsed_response = json.loads(response)
    return parsed_response



def improvement_summary(scores: List[Collect_score]):
    system_prompt = """
        You are Summarizer, a writing assistant focused on delivering concise improvement insights.

        You will receive a list of objects, each containing:
        - category (string): the evaluation dimension (e.g., "structure_star", "depth", etc.)
        - score (string): a number between "0" and "5"
        - improvement_tip (string): an actionable suggestion

        Your task:
        1. For these five, rewrite the `improvement_tip` into a short, readable, properly formatted string.
        2. Each line should start with the category in bold, followed by a colon and the rewritten improvement tip.
        3. Return a simple, plain text string of 5 lines. No extra text or formatting beyond what is specified.
        4. Merge improvement tips of same categories.

        Format example:
        **structure_star**: Consider using clearer paragraph breaks to improve organization.  
        **depth**: Expand on your examples to show deeper understanding.  
        ...

        """
    scores_json = json.dumps([score.model_dump() for score in scores])
    user_prompt = f"""
        Here are the scores and improvement tips to summarize:
        {scores_json}
        
        Please provide a concise summary with formatting as described.
    """
    response = generate_response(system_prompt=system_prompt, user_prompt=user_prompt, temp=0.3)
    return response



if __name__ == "__main__":
    jd = """
        We are seeking a product manager with experience in agile development, 
        cross-functional collaboration, and data-driven decision-making. 
        Strong communication skills and the ability to prioritize customer needs 
        are essential.
        """
    ques = "How do you prioritize features during a product sprint?"
    user = """
        I look at customer pain points and align them with strategic goals. 
        Then I negotiate with engineering based on effort and value.
        """
    competitor = """
        I use a RICE scoring model and validate assumptions with customer interviews and 
        analytics. Prioritization is then presented in sprint planning.
        """
    print(scorer(jd=jd,
                 ques=ques,
                 user=user,
                 competitor=competitor))

    scores = [
        Collect_score(
            category="structure_star",
            score="3",
            improvement_tip="Use more paragraph breaks and bullet points"
        ),
        Collect_score(
            category="depth",
            score="4",
            improvement_tip="Include more specific industry examples"
        ),
        Collect_score(
            category="clarity",
            score="2", 
            improvement_tip="Simplify technical jargon for broader audience"
        ),
        Collect_score(
            category="correctness",
            score="5",
            improvement_tip="Excellent factual accuracy, maintain this standard"
        ),
        Collect_score(
            category="depth",
            score="3",
            improvement_tip="include more in depth approach."
        )
    ]
    # summary = improvement_summary(scores)
    # print(summary)

    
    

