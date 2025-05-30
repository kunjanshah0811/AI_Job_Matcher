import streamlit as st
import json  
from typing import Dict, Any, List, Tuple
from model import generate_response 
from utils import FileProcessor 
from speech_converter import audio_to_text  
import tempfile
import os


def generate_question(resume_text, job_desc_text, job_role):
    system_prompt = "You are an experienced technical interviewer and JSON generator. You create professional interview questions and respond only with valid JSON arrays. Never include explanations, markdown formatting, or any text outside the JSON array."
    
    user_prompt = f"""
    You are conducting a technical interview for the "{job_role}" position. 
    
    Based on the candidate's resume and job requirements, generate exactly 5 technical interview questions that:
    1. Test relevant technical skills mentioned in the job description
    2. Assess the candidate's experience from their resume
    3. Include appropriate follow-up questions to dive deeper
    4. Progress from foundational to advanced concepts
    5. Are specific to the role and industry

    Resume Background:
    {resume_text}

    Job Requirements:
    {job_desc_text}

    Generate 5 technical interview questions with follow-up probes. Format each question to include the main question and potential follow-up in parentheses.

    Example format for a software role:
    - "Explain how you implemented [specific technology from resume]. (Follow-up: What challenges did you face and how did you optimize performance?)"
    - "The job requires [specific requirement]. Walk me through how you would approach this. (Follow-up: How would you handle scalability concerns?)"

    You must respond with ONLY a valid JSON array of strings. No explanations, no markdown, just the JSON array.
    """
    # Use generate_response instead of direct client call
    response = generate_response(system_prompt, user_prompt, temp=0.7)
                                 

    text = response.strip()
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
        "What specific skills and experience make you the best fit for this position? (Follow-up: Provide examples of applying these skills)",
        "Describe a significant challenge in your most recent role and how you overcame it. (Follow-up: What did you learn from this experience?)",
        "How do you stay updated with industry trends and continue learning? (Follow-up: Share a recent learning experience)",
        "Tell me about a time you had to adapt to a major change. (Follow-up: How did you manage the transition?)",
        "What are your expectations for this role and why do you want to join our team? (Follow-up: How does this align with your career goals?)"
    ]

# Initialize session state variables
if 'q_num' not in st.session_state:
    st.session_state.q_num = 0
if 'questions' not in st.session_state:
    st.session_state.questions = []
if 'processing_complete' not in st.session_state:
    st.session_state.processing_complete = False
if 'user_answers' not in st.session_state:
    st.session_state.user_answers = {}

#=== Sidebar: User Inputs ===#
with st.sidebar:
    st.title("AI-Job_Matcher – HiredGPT Duel")

    # 1. Resume Upload
    st.header("1. Upload Your Resume")
    user_resume = st.file_uploader("Upload your resume in PDF", type=['pdf'])

    # 2. Job Description
    st.header("2. Upload or Paste Job Description")
    job_desc_method = st.radio("How would you like to provide the job description?",
                                options=["Upload file", "Paste text"])
    
    if job_desc_method == "Upload file":
        job_desc_file = st.file_uploader("Upload job description (PDF, TXT)", 
                                        type=['pdf', 'txt'], key="jd")
        job_desc_text = None
    else:
        job_desc_file = None
        job_desc_text = st.text_area("Paste the job description text here")

    # 3. Star Competitor Settings
    st.header("3. Star Competitor Settings")
    improve_percentage = st.slider("How much stronger should the rival be? (%)", 
                                min_value=5, max_value=50, value=10, step=5)

    # 4. Job Role/Title
    st.header("4. Job Role/Title")
    job_role = st.text_input("Job role/title you're applying for")

    # 5. Submit Button
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
            resume_text = FileProcessor.read_resume(user_resume)
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
                jd_text = FileProcessor.read_job_description_pdf(job_desc_file)   
            elif job_desc_file.type == "text/plain":
                jd_text = FileProcessor.read_job_description_txt(job_desc_file)  
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
        
        # with st.expander("📄 View Resume Preview", expanded=False):
        #     st.write(resume_text[:3000] + "..." if len(resume_text) > 3000 else resume_text) 
        # with st.expander("📋 View Job Description Preview", expanded=False):
        #     st.write(jd_text[:3000] + "..." if len(jd_text) > 3000 else jd_text)

        #3 Generate Interview Questions
        with st.spinner("🤖 Generating interview questions..."):
            st.session_state.questions = generate_question(resume_text, jd_text,job_role)
            st.session_state.processing_complete = True
            
        with st.sidebar:
            st.success("✅ Interview questions generated!")

# Show Interview Duel if processing is complete
if st.session_state.processing_complete and st.session_state.questions:
    st.header("🥊 Interview Duel")
    
    qn = st.session_state.q_num
    questions = st.session_state.questions

    if 'user_answers' not in st.session_state:
        st.session_state.user_answers = {}

    if qn < len(questions):
        st.subheader(f"Question {qn+1}/{len(questions)}:")
        st.info(questions[qn])

        # Duel columns: User vs LLM
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**👤 Your Answer:**")
            current_answer = st.session_state.user_answers.get(qn, "")
            answer_submitted = qn in st.session_state.user_answers
            
            if answer_submitted:
                # Show submitted answer as read-only
                st.text_area(
                    "Your submitted answer:", 
                    value=current_answer,
                    key=f"readonly_ans_{qn}", 
                    height=150,
                    disabled=True
                )
                with st.sidebar:
                    st.success("✅ Answer submitted successfully!")
            else:
                # Audio input button
                st.markdown("🎤 **Record your answer:**")
                audio_file = st.audio_input("Record audio", key=f"audio_input_{qn}")
                
                # Process audio if available
                if audio_file is not None:
                    with st.spinner("🎧 Converting speech to text..."):
                        try:
                            # Save audio to temporary file
                            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
                                # Read bytes from UploadedFile object
                                audio_file.seek(0)  # Reset file pointer
                                tmp_file.write(audio_file.read())
                                tmp_file_path = tmp_file.name
                            
                            # Convert audio to text using speech_converter
                            transcribed_text = audio_to_text(tmp_file_path)
                            
                            # Clean up temporary file
                            os.unlink(tmp_file_path)
                            
                            if transcribed_text:
                                st.session_state[f"transcribed_text_{qn}"] = transcribed_text
                                with st.sidebar:
                                    st.success("✅ Audio transcribed successfully!")
                            else:
                                with st.sidebar:
                                    st.error("❌ Could not understand the audio. Please try again.")
                                
                        except Exception as e:
                            with st.sidebar:
                                st.error(f"❌ Audio processing error: {str(e)}")
                            if 'tmp_file_path' in locals():
                                try:
                                    os.unlink(tmp_file_path)
                                except:
                                    pass
                
                # Text area with transcribed text or manual input
                initial_text = st.session_state.get(f"transcribed_text_{qn}", current_answer)
                user_answer = st.text_area(
                    "Type your answer here (max 500 characters)", 
                    value=initial_text,
                    key=f"user_ans_{qn}", 
                    height=150,
                    max_chars=500
                )

        with col2:
            st.markdown("**🤖 Rival's Answer:**")
            if st.button("Generate Rival's Answer", key=f"rival_ans_{qn}"):
                # Place your LLM call here to get the rival's answer
                
                llm_answer = "This is how the star applicant would answer."
                st.write(llm_answer)
        
        # Centered Submit Answer Button (spans both columns)
        if not answer_submitted:            
            _, center_col, _ = st.columns([1, 2, 1])
            with center_col:
                if st.button("🚀 Submit Answer", key=f"submit_ans_{qn}", type="primary", use_container_width=True):
                    # Get answer directly from text area instead of session state
                    if len(user_answer.strip()) == 0:
                        st.error("Please provide an answer before submitting.")
                    elif len(user_answer) > 500:
                        st.error("Answer exceeds 500 characters limit.")
                    else:
                        # Store answer directly in user_answers
                        st.session_state.user_answers[qn] = user_answer
                        # Clear temporary storage
                        if f"temp_answer_{qn}" in st.session_state:
                            del st.session_state[f"temp_answer_{qn}"]
                        st.rerun()

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
                answer_submitted = qn in st.session_state.user_answers
                if answer_submitted:
                    if st.button("➡️ Next Question", key=f"next_{qn}"):
                        st.session_state.q_num += 1
                        st.rerun()
                else:
                    st.button("➡️ Next Question", key=f"next_{qn}", disabled=True, help="Please submit your answer first")
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
            for key in ['q_num', 'questions', 'processing_complete', 'user_answers']:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()