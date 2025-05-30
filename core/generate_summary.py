import streamlit as st
import datetime
import json
from model import generate_response
from test import resume, jd, jr, questions,ai_answers,user_answers,scores

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
    - Questions: {json.dumps(questions_list)}
    - User Answers: {json.dumps(user_answers)}
    - AI Answers: {json.dumps(ai_answers)}
    - Scores: {json.dumps(scores)}
    
    Generate ONLY the following sections for our report (structured as a JSON object):
    
    1. "strengths": A markdown list of 2-5 specific strengths demonstrated by the user
    2. "weaknesses": A markdown list of 2-5 specific mistakes or gaps in the user's answers
    3. "trends": A 2-3 sentence paragraph summarizing trends from the interview
    4. "resources": A markdown list of 2-5 useful links with descriptions (use proper markdown link format)
    5. "comparison_table": An array of objects, one per question, each with:
       - "question": The question text
       - "differences": Key differences between user and AI answers (1-2 sentences)
       - "strong_phrases": Notable strong phrases or points from either answer (comma separated)
    6. "topics_covered : return 4 keywords of topics covered in questions"
    
    Return ONLY a JSON object with these exact keys.
    """
    
    # Generate content
    try:
        response = generate_response(system_prompt, user_prompt)
        content = json.loads(response)
        return content
    except Exception as e:
        print(f"Error generating summary content: {e}")
        # Return fallback content if generation fails
        return {
            "strengths": "- Unable to analyze strengths\n- Please try again",
            "weaknesses": "- Unable to analyze weaknesses\n- Please try again",
            "trends": "Unable to analyze trends from the session data.",
            "resources": "- [Interview Preparation Tips](https://www.indeed.com/career-advice/interviewing)\n- [Job-Specific Interview Questions](https://www.glassdoor.com)",
            "comparison_table": [],
            "topics_covered":[]
        }

# Streamlit app
def app():
    st.set_page_config(page_title="Interview Summary", layout="centered")
    st.title("Interview Practice Summary")
        
    # Check if we need to generate content
    if 'summary_content' not in st.session_state:
        with st.spinner("Analyzing your interview performance..."):
            st.session_state.summary_content = generate_summary_content(
                resume_text=resume,
                job_desc_text=jd,
                job_role=jr,
                questions_list=questions,
                user_answers=user_answers,
                ai_answers=ai_answers,
                scores=scores
            )
    
    # Get content from state
    content = st.session_state.summary_content
    
    # Calculate overall score (average of all scores)
    flat_scores = [score for question_scores in scores for score in question_scores]
    overall_score = sum(flat_scores) / len(flat_scores) if flat_scores else "No data"
    
    today = datetime.datetime.now().strftime("%B %d, %Y")
    
    # Start building the fixed structure with dynamic content inserted
    st.markdown(f"""
    - **Date:** {today}
    """)
    
    st.header("Session Overview")
    st.markdown(f"""
    - **Questions Attempted:** {len(questions) if questions else "No data"}
    - **Topics Covered:** {', '.join(content.get("topics_covered", ["No data"]))}
    - **Overall Score:** {overall_score}/5
    """)
    
    st.header("Comparative Analysis")
    
    # Create the comparison table
    if "comparison_table" in content and content["comparison_table"]:
        table_md = "| Question | Key Differences | Strong Phrases |\n|----------|----------------|---------------|\n"
        for item in content["comparison_table"]:
            q = item.get("question", "No question")
            diff = item.get("differences", "No data")
            phrases = item.get("strong_phrases", "No data")
            table_md += f"| {q} | {diff} | {phrases} |\n"
        st.markdown(table_md)
    else:
        st.markdown("No comparison data available")
    
    st.header("Aggregated Feedback")
    
    st.subheader("Strengths")
    st.markdown(content.get("strengths", "No strengths data available"))
    
    st.subheader("Areas for Improvement")
    st.markdown(content.get("weaknesses", "No weaknesses data available"))
    
    st.subheader("Trends")
    st.markdown(content.get("trends", "No trend data available"))
    
    st.header("Useful Links & Resources")
    st.markdown(content.get("resources", "No resource data available"))
    
    # Create downloadable content
    full_markdown = f"""# Interview Practice Summary

## 1. User Information
- **Date:** {today}

## 2. Session Overview
- **Questions Attempted:** {len(questions) if questions else "No data"}
- **Topics Covered:** Technical skills for {jr}
- **Overall Score:** {overall_score}/5

## 3. Comparative Analysis
{table_md if "comparison_table" in content and content["comparison_table"] else "No comparison data available"}

## 4. Aggregated Feedback

### Strengths
{content.get("strengths", "No strengths data available")}

### Areas for Improvement
{content.get("weaknesses", "No weaknesses data available")}

### Trends
{content.get("trends", "No trend data available")}

## 5. Useful Links & Resources
{content.get("resources", "No resource data available")}
"""
    
    # Download button
    st.download_button(
        label="Download Summary as Markdown",
        data=full_markdown,
        file_name="interview_summary.md",
        mime="text/markdown"
    )
    
    st.info("This summary is generated based on your interview practice session.")

if __name__ == "__main__":
    app()