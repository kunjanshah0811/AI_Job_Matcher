import streamlit as st

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
    st.header("3. Star Applicant Settings")
    improve_percentage = st.slider("How much stronger should the rival be? (%)", min_value=5, max_value=50, value=10, step=5)

    #4 Job Role/Title Input
    st.header("4. Job Role/Title")
    job_role = st.text_input("Job role/title you're applying for")

    #5 Submit Button
    submit = st.button("Submit - (Next: generate rival resume and interview questions)")

#=== Main Area: Q&A and Duel ===#
if submit:
        # ---- Placeholder: LLM Question Generation ----
    st.header("Interview Duel")
    # Imagine questions are generated in a list called `questions`
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