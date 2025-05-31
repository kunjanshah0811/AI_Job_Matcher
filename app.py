import os
os.environ["STREAMLIT_WATCHER_TYPE"] = "none"
os.environ["PYTORCH_DISABLE_WIN_FIX"] = "1"

import streamlit as st
import json
from datetime import datetime

from core.utils import FileProcessor, star_rating
from core.question_generator import generate_question
from core.answering_competitor import Answering_competitor
from core.response_evaluator import scorer
from core.summary_utils import custom_css, generate_text_summary, clean_json_response
from core.generate_summary import generate_summary_content
from core.speech_converter import text_to_audio, load_model

# Page configuration
st.set_page_config(
    page_title="AI Job Matcher - HiredGPT Duel",
    page_icon="🤖",
    layout="wide"
)

whisper_model = load_model()

if 'questions_generated' not in st.session_state:
    st.session_state.questions_generated = []

if "page_stack" not in st.session_state:
    st.session_state.page_stack = ["Welcome"]

if "track_score" not in st.session_state:
    st.session_state["track_score"] = []

if st.session_state.page_stack[-1] == "Welcome":
    st.title("🤖 Welcome to AI Job Matcher - HiredGPT Duel")
    st.markdown("""
    ### 🎯 How it works:
    1. **📄 Upload your resume** in the sidebar
    2. **📋 Provide job description** (upload file or paste text)
    3. **⭐ Set competitor strength** (how challenging should it be?)
    4. **💼 Enter the job role** you're applying for
    5. **🚀 Click submit** to start the duel!
    
    **Complete all fields in the sidebar to begin →**
    """)

if st.session_state.page_stack[-1] == "Loading":
    st.title("🤖 Welcome to AI Job Matcher - HiredGPT Duel")
    st.success("🎉 All files processed successfully!")

    with st.spinner("🤖 Generating interview questions..."):
        st.session_state.questions = generate_question(st.session_state.resume_text, 
                                                        st.session_state.jd_text, 
                                                        st.session_state.job_role)
        
    with st.spinner("🔧 Initializing your interview competitor..."):
        comp_ans_gen = Answering_competitor(resume=st.session_state.resume_text, 
                                        job_description=st.session_state.jd_text, 
                                        difficulty_level=st.session_state.improve_percentage,
                                        questions=st.session_state.questions)
        comp_ans_gen.extract_factors()
        comp_ans_gen.determine_enhancement()
        comp_ans_gen.generate_resume()

    with st.spinner("🧠 Crafting rival candidate persona..."):
        
        comp_answers = comp_ans_gen.answer_questions()

        for key, val in comp_answers.items():
            st.session_state[f"llm_answer_{key-1}"] = val
    
    st.session_state.page_stack.append("Ques_0")
    st.rerun()

if st.session_state.page_stack[-1] == "Summary":    
    st.markdown(custom_css, unsafe_allow_html=True)
    st.session_state.user_answers = [st.session_state[f"user_answer_{ques}"] for ques in range(len(st.session_state.questions))]
    st.session_state.ai_answers = [st.session_state[f"llm_answer_{ques}"] for ques in range(len(st.session_state.questions))]
    st.session_state.scores = [
            [
                int(track_score["structure_star"]["score"]),
                int(track_score["depth"]["score"]),
                int(track_score["clarity"]["score"]),
                int(track_score["correctness"]["score"])
            ] 
            for track_score in st.session_state.track_score
        ]
    
    if "summary_data" not in st.session_state:
        with st.spinner("Analyzing your interview performance..."):
            try:
                summary_json = generate_summary_content(
                    st.session_state.resume_text,
                    st.session_state.jd_text,
                    st.session_state.job_role,
                    st.session_state.questions,
                    st.session_state.user_answers,
                    st.session_state.ai_answers,
                    st.session_state.scores
                )

                cleaned_json = clean_json_response(summary_json)

                try:
                    summary_data = json.loads(cleaned_json)
                    st.session_state.summary_data = summary_data
                except json.JSONDecodeError as e:
                    st.error(f"Error parsing summary data: {e}")
                    st.code(summary_json)  # Show the raw response for debugging
                    st.stop()
                
            except Exception as e:
                st.error(f"Error generating summary: {e}")
                st.stop()
    
    summary_data = st.session_state.summary_data
    for key in ["strengths", "weaknesses", "resources"]:
        if key in summary_data and isinstance(summary_data[key], list):
            summary_data[key] = "\n".join(summary_data[key])
    
    if "topics_covered" in summary_data:
        # If topics is a string, split it into a list
        if isinstance(summary_data["topics_covered"], str):
            # Split by common separators
            if "," in summary_data["topics_covered"]:
                summary_data["topics_covered"] = [t.strip() for t in summary_data["topics_covered"].split(",")]
            elif ";" in summary_data["topics_covered"]:
                summary_data["topics_covered"] = [t.strip() for t in summary_data["topics_covered"].split(";")]
            elif "\n" in summary_data["topics_covered"]:
                summary_data["topics_covered"] = [t.strip() for t in summary_data["topics_covered"].split("\n")]
            # If no separators, use the whole string as one topic
            else:
                summary_data["topics_covered"] = [summary_data["topics_covered"]]
    
    scores_list = st.session_state.scores
    avg_score = sum([sum(q_score) for q_score in scores_list]) / (len(scores_list) * 4) * 10
    text_summary = generate_text_summary(summary_data, scores_list)

    st.markdown('<div class="page-header">', unsafe_allow_html=True)
    st.markdown('<h1 class="page-title" style="color: white;">Interview Performance Summary</h1>', unsafe_allow_html=True)
    
    st.markdown(f'<p>Review your performance and get insights to improve your next interview.</p>', unsafe_allow_html=True)
    st.markdown('<hr style="height:1px;border:none;background-color:#E8E0D0;">', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Center the download button using columns
    _, download_col, _ = st.columns([3, 4, 3])
    with download_col:
        st.markdown('<div class="download-btn-container">', unsafe_allow_html=True)
        st.download_button(
            label="Download Summary",
            data=text_summary,
            file_name=f"interview_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain",
            use_container_width=True  # Make button take full column width
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    left_col, right_col = st.columns([8, 2])
    with right_col:
        st.markdown('<div class="metric-container" style="flex-direction: column; height: 100%;">', unsafe_allow_html=True)
        
        # Overall Score
        st.markdown(f"""
        <div class="metric-card" style="margin-bottom: 1rem;">
            <div class="metric-value">{avg_score:.1f}<span style="font-size: 1.2rem;">/100</span></div>
            <div class="metric-label">Overall Score</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Topics Covered
        topics = summary_data.get("topics_covered", [])
        st.markdown(f"""
        <div class="metric-card" style="margin-bottom: 1rem;">
            <div class="metric-value">{len(topics)}</div>
            <div class="metric-label">Topics Covered</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{len(summary_data.get("comparison_table", []))}</div>
            <div class="metric-label">Questions Analyzed</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        if topics:
            st.markdown('<div class="topic-list-sidebar">', unsafe_allow_html=True)
            st.markdown('<div class="topic-list-title">Topics List</div>', unsafe_allow_html=True)
            
            # Fixed: Create a single string with all topic badges properly formatted
            topics_html = ""
            for topic in topics:
                if isinstance(topic, str):
                    # Properly handle each topic as a full word
                    topics_html += f'<div class="sidebar-topic-badge">{topic}</div> '
            
            # Display all topics as HTML
            st.markdown(topics_html, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
    
    with left_col:
        # Display trends - removed background
        st.markdown('<h2 class="section-header">Performance Overview</h2>', unsafe_allow_html=True)
        st.info(summary_data.get("trends", "No trend data available"))
        # Add section divider
        st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
        
        # Strengths and weaknesses section - removed content wrapper
        strength_weak_cols = st.columns(2)
        
        with strength_weak_cols[0]:
            st.markdown('<h2 class="section-header">Your Strengths</h2>', unsafe_allow_html=True)
            st.markdown(f'<div class="strength-card">{summary_data.get("strengths", "No strengths data available")}</div>', unsafe_allow_html=True)
        
        with strength_weak_cols[1]:
            st.markdown('<h2 class="section-header">Areas for Improvement</h2>', unsafe_allow_html=True)
            st.markdown(f'<div class="weakness-card">{summary_data.get("weaknesses", "No weaknesses data available")}</div>', unsafe_allow_html=True)
        
        # Add section divider
        st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
        
        # Question-by-question analysis - removed content wrapper
        st.markdown('<h2 class="section-header">Question Analysis</h2>', unsafe_allow_html=True)
        
        comparison_table = summary_data.get("comparison_table", [])

        for i, item in enumerate(comparison_table):
            with st.expander(f"Q{i+1}: {item.get('question', 'Question')}"):
                qa_cols = st.columns(2)
                
                with qa_cols[0]:
                    st.markdown('<h3 class="sub-header">Key Differences</h3>', unsafe_allow_html=True)
                    st.info(item.get("differences", "No comparison available"))
                
                with qa_cols[1]:    
                    st.markdown('<h3 class="sub-header">Strong Phrases</h3>', unsafe_allow_html=True)
                    st.success(item.get("strong_phrases", "No notable phrases identified"))
                
                # Display answers side by side
                if i < len(st.session_state.user_answers) and i < len(st.session_state.ai_answers):
                    tab1, tab2 = st.tabs(["Your Answer", "AI Answer"])
                    
                    with tab1:
                        st.markdown(st.session_state.user_answers[i])
                    
                    with tab2:
                        st.markdown(st.session_state.ai_answers[i])
        
        # Add section divider
        st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
        
        # Resources section - make links blue, removed content wrapper
        st.markdown('<h2 class="section-header">Recommended Resources</h2>', unsafe_allow_html=True)
        
        # Format resources as a list with blue link styling
        resources = summary_data.get("resources", "No resources available")

        if isinstance(resources, str):
            if "\n" in resources:
                resources_list = resources.split("\n")
                resources_html = '<ul class="resource-list">'
                
                for resource in resources_list:
                    if resource.strip():  # Skip empty lines
                        # If it doesn't already contain HTML links, style it as a link
                        if "<a href" not in resource.lower():
                            formatted_resource = f'<a href="#">{resource}</a>'
                        else:
                            formatted_resource = resource
                        
                        resources_html += f'<li class="resource-item">{formatted_resource}</li>'
                
                resources_html += '</ul>'
                st.markdown(resources_html, unsafe_allow_html=True)
            else:
                # Single resource, no newlines
                st.markdown(f'<div class="resource-item"><a href="#">{resources}</a></div>', unsafe_allow_html=True)
    
    if st.button("Rerun"):
        st.rerun()


if st.session_state.page_stack[-1].startswith("Ques_"):
    ques = int(st.session_state.page_stack[-1][-1])

    st.header("🥊 Interview Duel")
    st.subheader(f"Question {ques+1}/{len(st.session_state.questions)}")
    
    st.info(st.session_state.questions[ques])

    user_ans, llm_ans = st.columns(2)

    user_answer = ""
    with user_ans:
        st.markdown("**👤 Your Answer:**")
        if f"submitted_ans_{ques}" in st.session_state and st.session_state[f"submitted_ans_{ques}"]:
            st.audio_input(label="Record Audio",disabled=True, label_visibility="collapsed")
            st.text_area(
                    "Type your answer here",
                    value=st.session_state[f"user_answer_{ques}"],
                    height=150,
                    label_visibility="collapsed",
                    disabled=True
                    )
            
            
        else:
            audio_file = st.audio_input(label="Record Audio",key=f"audio_ip_{ques}" ,label_visibility="collapsed")
            transcribed_text = ""
            if audio_file:
                file_path = os.path.join("audio",f"user_answer_{ques}.wav")
                try:
                    with open(file_path, "wb") as f:
                        audio_file.seek(0)
                        f.write(audio_file.read())

                    transcribed_text = whisper_model.transcribe(file_path)["text"]
                    # print(st.session_state[f"transcribed_{ques}"])
                    # st.rerun()
                except Exception as e:
                    st.error(f"Error occured while transcribing {e}")
            
            user_answer = st.text_area(
                    "Type your answer here",
                    value= transcribed_text,
                    height=150,
                    label_visibility="collapsed",
                    )

                    


    with llm_ans:
        st.markdown("**🤖 Rival's Answer:**")
        if f"submitted_ans_{ques}" in st.session_state and st.session_state[f"submitted_ans_{ques}"]:
            st.text_area("Competitor Response",st.session_state[f"llm_answer_{ques}"], height=150, label_visibility="collapsed")
            st.audio(data=os.path.join("audio",f"llm_answer_{ques}.wav"))

        else:
            # st.text_area("Competitor Response",value="Hidden values", height=150, label_visibility="collapsed")
            st.markdown(f"""
                <div style="
                    height: 150px;
                    background-color: transparent;
                    border: 1px solid #d4d4d4;
                    border-radius: 4px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    filter: blur(3px);
                    font-family: monospace;
                    font-size: 15px;
                    color: #FAFAFA;
                    padding: 10px;
                    overflow: hidden;
                    text-overflow: ellipsis;
                    word-wrap: break-word;
                    white-space: pre-wrap;
                    text-align: left;
                ">
                    {st.session_state[f"llm_answer_{ques}"]}
                </div>
                """, unsafe_allow_html=True)
            try:
                os.makedirs("audio",exist_ok=True)
                text_to_audio(st.session_state[f"llm_answer_{ques}"], os.path.join("audio",f"llm_answer_{ques}.wav"))
            except Exception as e:
                print(e)
                st.error(f"An error occurred {e}")

    left_area,_ = st.columns([1,1])
    _, submit_area, _  = left_area.columns([1,3,1])
    with submit_area:
        if st.button("🚀 Submit & Compare Answers", use_container_width=True, type="primary"):
            st.session_state[f"submitted_ans_{ques}"] = True
            st.session_state[f"user_answer_{ques}"] = user_answer
            print("User answer\n",st.session_state[f"user_answer_{ques}"])
            st.rerun()
    
    
    if f"submitted_ans_{ques}" in st.session_state and st.session_state[f"submitted_ans_{ques}"]:
        result_score = dict()
        if f"result_score_{ques}" in st.session_state and st.session_state[f"result_score_{ques}"]:
            result_score = st.session_state[f"result_score_{ques}"]
        else:
            result_score = scorer(
                jd= st.session_state.jd_text,
                ques= st.session_state.questions[ques],
                user= st.session_state[f"user_answer_{ques}"],
                competitor= st.session_state[f"llm_answer_{ques}"],
            )

            st.session_state[f"result_score_{ques}"] = result_score
            st.session_state.track_score.append(result_score["user"])

        with st.container(border=True):
            user_score, llm_score = st.columns(2)
            with user_score:
                participant = result_score["user"]
                st.markdown(f"**Structure:** {star_rating(participant['structure_star']['score'])}")
                st.markdown(f"**Depth:** {star_rating(participant['depth']['score'])}")
                st.markdown(f"**Clarity:** {star_rating(participant['clarity']['score'])}")
                st.markdown(f"**Correctness:** {star_rating(participant['correctness']['score'])}")
                
            
            with llm_score:
                participant = result_score["competitor"]
                st.markdown(f"**Structure:** {star_rating(participant['structure_star']['score'])}")
                st.markdown(f"**Depth:** {star_rating(participant['depth']['score'])}")
                st.markdown(f"**Clarity:** {star_rating(participant['clarity']['score'])}")
                st.markdown(f"**Correctness:** {star_rating(participant['correctness']['score'])}")


    st.markdown("---")
    prev,_,next = st.columns([1,3,1])

    if ques>0:
        with prev:
            if st.button("⬅️ Previous Question"):
                st.session_state.page_stack.pop()
                st.rerun()

    with next:
        if ques < len(st.session_state.questions)-1:
            if st.button("Next Question ➡️"):
                st.session_state.page_stack.append(f"Ques_{ques+1}")
                st.rerun()
        if ques == len(st.session_state.questions) -1:
            if st.button("📊 Summary"):
                st.session_state.page_stack.append("Summary")
                st.rerun()


with st.sidebar:
    st.title("AI-Job_Matcher - HiredGPT Duel")
    st.markdown("---")

    # 1. Resume Upload
    st.header("📄 1. Upload Your Resume")
    user_resume = st.file_uploader("Upload your resume in PDF", type=['pdf'])

    # 2. Job Description
    st.header("📋 2. Upload or Paste Job Description")
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
    st.header("⭐ 3. Star Competitor Settings")
    improve_percentage = st.slider("How much stronger should the rival be? (%)", 
                                min_value=10, max_value=100, value=10, step=10)
    
    st.info(f"🎯 Your competitor will be {improve_percentage}% stronger")

    # 4. Job Role/Title
    st.header("💼 4. Job Role/Title")
    job_role = st.text_input("Job role/title you're applying for")
    st.markdown("---")
    submit_button = st.button("🚀 Start HiredGPT Duel", type="primary", use_container_width=True)

    if submit_button:
        # Clear previous session state to restart the process
        if 'resume_text' in st.session_state:
            del st.session_state.resume_text
        if 'jd_text' in st.session_state:
            del st.session_state.jd_text
        if 'questions_generated' in st.session_state:
            st.session_state.questions_generated = []
        
        if "page_stack" in st.session_state:
            st.session_state.page_stack = ["Welcome"]


        missing_fields = []

        if not user_resume:
            missing_fields.append("📄 Resume")
        
        if job_desc_method == "Upload file":
            if not job_desc_file:
                missing_fields.append("📋 Job Description File")
        else:
            if not job_desc_text or len(job_desc_text.strip()) < 10:
                missing_fields.append("📋 Job Description Text")
        
        if not job_role or len(job_role.strip()) == 0:
            missing_fields.append("💼 Job Role/Title")
        
        if missing_fields:
            st.error(f"❌ Please complete the following fields:\n\n" + "\n\n".join([f"• {field}" for field in missing_fields]))
        
        else:
            st.success("✅ All fields completed successfully!")
            st.session_state.improve_percentage = improve_percentage
            st.session_state.job_role = job_role
            
            resume_text = ""
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


            if resume_text and jd_text:
                st.session_state.resume_text = resume_text
                st.session_state.jd_text = jd_text
                st.session_state.page_stack.append("Loading")
                st.rerun()

    
