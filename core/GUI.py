import streamlit as st
from input_comp_gen import read_resume, read_job_description_pdf, read_job_description_txt
from question_generator import generate_question
from answering_competitor import Answering_competitor
import json
                    
# Initialize session state variables
if 'q_num' not in st.session_state:
    st.session_state.q_num = 0
if 'questions' not in st.session_state:
    st.session_state.questions = []
if 'processing_complete' not in st.session_state:
    st.session_state.processing_complete = False

#=== Sidebar: User Inputs ===#
with st.sidebar:
    st.title("HiredGPT Duel")

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

