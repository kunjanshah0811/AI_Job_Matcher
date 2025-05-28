import streamlit as st
import PyPDF2
#import io

def read_resume(file):
    reader=PyPDF2.PdfReader(file)
    text= ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text.strip()

def read_job_description(file):
    return file.read().decode("utf-8").strip()


#=== Sidebar: User Inputs ===#
with st.sidebar:
    st.title("AI_Job_Matcher – HiredGPT Duel")

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


#=== Main Area: Q&A and Duel ===#
if submit:

    # Input Validation
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


    # Resume and Job Description Processing    
    resume_text = ""
    if user_resume:
        try:
            resume_text = read_resume(user_resume)
            st.success("Resume uploaded successfully!")
        except Exception as e:
            st.error(f"Error reading resume: {e}")
    else:
        st.error("Please upload your resume.")
    
    jd_text=''
    if job_desc_file:
        try:
            if job_desc_file.type == "application/pdf":
                jd_text = read_job_description(job_desc_file)   
            elif job_desc_file.type == "text/plain":
                jd_text = job_desc_file.read().decode("utf-8").strip()  
            else:
                st.error("Unsupported file type for job description.")
        except Exception as e:  
            st.error(f"Error reading job description: {e}")
    elif job_desc_text:
        jd_text = job_desc_text.strip() 
        st.success("Job description successfully read.")
    else:
        st.error("Please provide the job description to continue.")
    
    if resume_text and jd_text:
        st.success("Resume & JD Preview")
        with st.expander("View Resume", expanded=False):
            st.write(resume_text[:3000]) 
        with st.expander("View Job Description", expanded=False):
            st.write(jd_text[:3000])

        st.header("Interview Duel")

        questions = ["Tell me about yourself.", "Describe a challenge at work and how you solved it."]
        if "q_num" not in st.session_state:
            st.session_state.q_num = 0
        
        question = questions[st.session_state.q_num]
        st.subheader(f"Question {st.session_state.q_num+1}: {question}")

        # Duel columns: User vs LLM
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Your Answer:**")
            user_answer = st.text_area("Type your answer here", key=f"user_ans_{st.session_state.q_num}")

        with col2:
            st.markdown("**Star Applicant's Answer:**")
            if st.button("Generate Rival's Answer"):
                # Place your LLM call here to get the rival's answer
                llm_answer = "This is how the star applicant would answer."
                st.write(llm_answer)

        # Scoring/Feedback
        if st.button("Score & Feedback"):
            # Call LLM to compare and score
            st.success("Your Score: 7/10\nStar Applicant's Score: 9/10")
            st.info("Tip: Give more specific examples to boost your answer.")

        # Next question navigation (simple MVP)
        if st.session_state.q_num < len(questions) - 1:
            if st.button("Next Question"):
                st.session_state.q_num += 1
                st.experimental_rerun()