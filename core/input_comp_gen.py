import streamlit as st
import PyPDF2
import os
import json  # Added import for JSON parsing
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = OpenAI(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

def read_resume(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text.strip()

def read_job_description_pdf(file):
    """Read PDF job description"""
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text.strip()

def read_job_description_txt(file):
    """Read TXT job description"""
    return file.read().decode("utf-8").strip()

def generate_question(resume_text, job_desc_text, job_role):
    prompt = f"""
    You are an interview coach. Based on this resume and job description, generate exactly 5 interview questions for the role "{job_role}".

    Resume:
    {resume_text}

    Job Description:
    {job_desc_text}

    Generate 5 relevant interview questions. Include follow-up prompts in parentheses if needed.
    You must respond with ONLY a valid JSON array of strings. No explanations, no markdown, just the JSON array.

    Example format: ["Question 1 here", "Question 2 here", "Question 3 here", "Question 4 here", "Question 5 here"]
    """
    response = client.chat.completions.create(
        model="gemini-2.0-flash-lite",
        messages=[
            {"role": "system", "content": "You are a JSON generator. You only respond with valid JSON arrays. Never include explanations or markdown formatting."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,

    )
    text = response.choices[0].message.content.strip()
    #st.write("Raw API Response:", text)  # Debug line

    try:
        # Debug: Check if response is empty
        if not text:
            st.error("Empty response from API")
            return default_questions()
            
        # Debug: Try to clean the response
        cleaned_text = text
        if not text.startswith('['):
            #st.warning("Response not in JSON format, attempting to clean...")
            # Find JSON array markers
            start_idx = text.find('[')
            end_idx = text.rfind(']')
            
            if start_idx != -1 and end_idx != -1:
                cleaned_text = text[start_idx:end_idx + 1]
                #st.write("Cleaned text:", cleaned_text)  # Debug line
            else:
                #st.error("Could not find JSON array markers")
                return default_questions()
        
        # Try parsing the cleaned JSON
        questions = json.loads(cleaned_text)
        return questions
        
    except json.JSONDecodeError as e:
        st.error(f"JSON Parse Error: {str(e)}")
        st.error(f"Problem at position: {e.pos}")
        st.error(f"Problem line: {e.lineno}, col: {e.colno}")
        return default_questions()
    except Exception as e:
        st.error(f"Other error: {str(e)}")
        return default_questions()

def default_questions():
    """Fallback questions if API fails"""
    return [
        "Tell me about your relevant experience for this role.",
        "What are your key strengths and weaknesses?",
        "Why are you interested in this position?",
        "Describe a challenging project you've worked on.",
        "What questions do you have about the role?"
    ]

# Initialize session state variables
if 'q_num' not in st.session_state:
    st.session_state.q_num = 0
if 'questions' not in st.session_state:
    st.session_state.questions = []
if 'processing_complete' not in st.session_state:
    st.session_state.processing_complete = False

#=== Sidebar: User Inputs ===#
with st.sidebar:
    st.title("AI-Job_Matcher – HiredGPT Duel")

    #1 Resume Upload
    st.header("1. Upload Your Resume")
    user_resume = st.file_uploader("Upload your resume in PDF", type=['pdf'])

    #2 Job Description Upload or Paste
    st.header("2. Upload or Paste Job Description")

    job_desc_method = st.radio("How would you like to provide the job description?",
                            options=["Upload file", "Paste text"])
    if job_desc_method == "Upload file":
        job_desc_file = st.file_uploader("Upload job description (PDF, TXT)", type=['pdf', 'txt'], key="jd")
        job_desc_text = None
    else:
        job_desc_file = None
        job_desc_text = st.text_area("Paste the job description text here")

    #3 Improvement Percentage or Manual Input
    st.header("3. Star Competitor Settings")
    improve_percentage = st.slider("How much stronger should the rival be? (%)", min_value=5, max_value=50, value=10, step=5)

    #4 Job Role/Title Input
    st.header("4. Job Role/Title")
    job_role = st.text_input("Job role/title you're applying for")

    #5 Submit Button
    submit = st.button("Submit - (Next: generate rival resume and interview questions)")

    # Status messages in sidebar
    if submit or st.session_state.processing_complete:
        st.subheader("📋 Processing Status")

#=== Main Area: Q&A and Duel ===#
if submit:
    #1 Input Validation
    errors = []
    if not user_resume:
        errors.append("Please upload your resume (PDF).")
    if job_desc_method == "Upload file" and not job_desc_file:
        errors.append("Please upload the Job description file.")
    if job_desc_method == "Paste text" and not job_desc_text.strip():
        errors.append("Please paste the Job description text.")
    if not job_role.strip():
        errors.append("Please enter the Job role/title.")

    if errors:
        for error in errors:
            st.toast(error, icon="⚠️")
        st.stop()

    #2 Resume and Job Description Processing    
    resume_text = ""
    if user_resume:
        try:
            resume_text = read_resume(user_resume)
            with st.sidebar:
                st.success("✅ Resume uploaded successfully!")
        except Exception as e:
            with st.sidebar:
                st.error(f"❌ Error reading resume: {e}")
            st.stop()
    
    jd_text = ''
    if job_desc_file:
        try:
            if job_desc_file.type == "application/pdf":
                jd_text = read_job_description_pdf(job_desc_file)   
            elif job_desc_file.type == "text/plain":
                jd_text = read_job_description_txt(job_desc_file)  
            else:
                st.error("Unsupported file type for job description.")
                st.stop()
            with st.sidebar:
                st.success("✅ Job description uploaded successfully!")
        except Exception as e:  
            with st.sidebar:
                st.error(f"❌ Error reading job description: {e}")
            st.stop()
    elif job_desc_text:
        jd_text = job_desc_text.strip() 
        with st.sidebar:
            st.success("✅ Job description text processed!")
    else:
        st.error("Please provide the job description to continue.")
        st.stop()
    
    if resume_text and jd_text:
        # Show preview in main area
        st.success("🎉 All files processed successfully!")
        
        with st.expander("📄 View Resume Preview", expanded=False):
            st.write(resume_text[:3000] + "..." if len(resume_text) > 3000 else resume_text) 
        with st.expander("📋 View Job Description Preview", expanded=False):
            st.write(jd_text[:3000] + "..." if len(jd_text) > 3000 else jd_text)

        #3 Generate Interview Questions
        with st.spinner("🤖 Generating interview questions..."):
            st.session_state.questions = generate_question(resume_text, jd_text, job_role)
            st.session_state.processing_complete = True
            
        with st.sidebar:
            st.success("✅ Interview questions generated!")

# Show Interview Duel if processing is complete
if st.session_state.processing_complete and st.session_state.questions:
    st.header("🥊 Interview Duel")
    
    qn = st.session_state.q_num
    questions = st.session_state.questions

    if qn < len(questions):
        st.subheader(f"Question {qn+1}/{len(questions)}:")
        st.info(questions[qn])

        # Duel columns: User vs LLM
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**👤 Your Answer:**")
            user_answer = st.text_area("Type your answer here", key=f"user_ans_{qn}", height=150)

        with col2:
            st.markdown("**🤖 Rival's Answer:**")
            if st.button("Generate Rival's Answer", key=f"rival_ans_{qn}"):
                # Place your LLM call here to get the rival's answer
                llm_answer = "This is how the star applicant would answer."
                st.write(llm_answer)

        # Scoring/Feedback
        col3, col4, col5 = st.columns([1, 1, 1])
        with col3:
            if st.button("📊 Score & Feedback", key=f"score_{qn}"):
                # Call LLM to compare and score
                st.success("Your Score: 7/10\nStar Applicant's Score: 9/10")
                st.info("💡 Tip: Give more specific examples to boost your answer.")

        # Next question navigation
        with col4:
            if st.session_state.q_num < len(questions) - 1:
                if st.button("➡️ Next Question", key=f"next_{qn}"):
                    st.session_state.q_num += 1
                    st.rerun()
            else:
                st.success("🎉 Interview Complete!")
                
        with col5:
            if st.session_state.q_num > 0:
                if st.button("⬅️ Previous Question", key=f"prev_{qn}"):
                    st.session_state.q_num -= 1
                    st.rerun()

        # Progress bar
        progress = (qn + 1) / len(questions)
        st.progress(progress, text=f"Progress: {qn + 1}/{len(questions)} questions")

elif st.session_state.processing_complete and not st.session_state.questions:
    st.error("❌ Failed to generate questions. Please try again.")
    
# Reset button in sidebar
if st.session_state.processing_complete:
    with st.sidebar:
        st.divider()
        if st.button("🔄 Start New Interview", type="secondary"):
            for key in ['q_num', 'questions', 'processing_complete']:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()