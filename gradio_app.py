import os
import gradio as gr
import json
from datetime import datetime
import tempfile

# Import your existing modules
from core.utils import FileProcessor, star_rating
from core.question_generator import generate_question
from core.answering_competitor import Answering_competitor
from core.response_evaluator import scorer
from core.summary_utils import custom_css, generate_text_summary, clean_json_response
from core.generate_summary import generate_summary_content
from core.speech_converter import text_to_audio, load_model

# Initialize Whisper model
whisper_model = load_model()

# Global CSS for styling
CUSTOM_CSS = """
.gradio-container {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.question-container {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 20px;
    border-radius: 10px;
    color: white;
    margin: 10px 0;
}

.score-container {
    background: #f8f9fa;
    padding: 15px;
    border-radius: 8px;
    border-left: 4px solid #007bff;
    margin: 10px 0;
}

.summary-section {
    background: #ffffff;
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    margin: 15px 0;
}

.metric-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 20px;
    border-radius: 10px;
    text-align: center;
    margin: 10px;
}

.strength-card {
    background: #d4edda;
    border: 1px solid #c3e6cb;
    color: #155724;
    padding: 15px;
    border-radius: 8px;
}

.weakness-card {
    background: #f8d7da;
    border: 1px solid #f5c6cb;
    color: #721c24;
    padding: 15px;
    border-radius: 8px;
}
"""

def initialize_app_state():
    """Initialize the application state"""
    return {
        'current_page': 'welcome',
        'questions': [],
        'current_question': 0,
        'resume_text': '',
        'jd_text': '',
        'job_role': '',
        'improve_percentage': 10,
        'user_answers': [],
        'ai_answers': [],
        'scores': [],
        'track_score': [],
        'summary_data': None,
        'questions_generated': False,
        'competitor_initialized': False
    }

def process_files_and_generate_questions(resume_file, jd_file, jd_text, job_role, improve_percentage, app_state):
    """Process uploaded files and generate questions"""
    try:
        # Process resume
        if resume_file is None:
            return "❌ Please upload a resume file", app_state, gr.update(visible=False)
        
        resume_text = FileProcessor.read_resume(resume_file)
        
        # Process job description
        jd_content = ""
        if jd_file is not None:
            if jd_file.name.endswith('.pdf'):
                jd_content = FileProcessor.read_job_description_pdf(jd_file)
            elif jd_file.name.endswith('.txt'):
                jd_content = FileProcessor.read_job_description_txt(jd_file)
        elif jd_text and len(jd_text.strip()) > 10:
            jd_content = jd_text.strip()
        else:
            return "❌ Please provide a job description", app_state, gr.update(visible=False)
        
        if not job_role or len(job_role.strip()) == 0:
            return "❌ Please enter a job role", app_state, gr.update(visible=False)
        
        # Update state
        app_state['resume_text'] = resume_text
        app_state['jd_text'] = jd_content
        app_state['job_role'] = job_role
        app_state['improve_percentage'] = improve_percentage
        app_state['current_page'] = 'loading'
        
        # Generate questions
        questions = generate_question(resume_text, jd_content, job_role)
        app_state['questions'] = questions
        app_state['questions_generated'] = True
        
        # Initialize competitor
        comp_ans_gen = Answering_competitor(
            resume=resume_text,
            job_description=jd_content,
            difficulty_level=improve_percentage,
            questions=questions
        )
        comp_ans_gen.extract_factors()
        comp_ans_gen.determine_enhancement()
        comp_ans_gen.generate_resume()
        
        # Generate competitor answers
        comp_answers = comp_ans_gen.answer_questions()
        app_state['ai_answers'] = list(comp_answers.values())
        app_state['competitor_initialized'] = True
        app_state['current_page'] = 'questions'
        app_state['current_question'] = 0
        
        return "✅ Questions generated successfully! Starting interview...", app_state, gr.update(visible=True)
        
    except Exception as e:
        return f"❌ Error: {str(e)}", app_state, gr.update(visible=False)

def get_current_question_display(app_state):
    """Get the current question display information"""
    if not app_state['questions'] or app_state['current_question'] >= len(app_state['questions']):
        return "No questions available", "", "", False, False, gr.update(visible=False)
    
    current_q = app_state['current_question']
    question = app_state['questions'][current_q]
    ai_answer = app_state['ai_answers'][current_q] if current_q < len(app_state['ai_answers']) else ""
    
    progress = f"Question {current_q + 1} of {len(app_state['questions'])}"
    
    show_prev = current_q > 0
    show_next = current_q < len(app_state['questions']) - 1
    show_summary = current_q == len(app_state['questions']) - 1
    
    return question, ai_answer, progress, show_prev, show_next or show_summary, gr.update(visible=True)

def submit_answer(user_answer, audio_file, app_state):
    """Submit user answer and get scoring"""
    if not user_answer and not audio_file:
        return "Please provide an answer", app_state, "", ""
    
    # Handle audio transcription if provided
    final_answer = user_answer
    if audio_file:
        try:
            # Create temporary file for audio processing
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp_file:
                # Save audio file
                with open(audio_file, 'rb') as f:
                    tmp_file.write(f.read())
                tmp_file.flush()
                
                # Transcribe audio
                transcribed = whisper_model.transcribe(tmp_file.name)["text"]
                final_answer = transcribed if not user_answer else user_answer + " " + transcribed
                
                # Clean up
                os.unlink(tmp_file.name)
        except Exception as e:
            return f"Audio transcription error: {str(e)}", app_state, "", ""
    
    current_q = app_state['current_question']
    
    # Ensure user_answers list is long enough
    while len(app_state['user_answers']) <= current_q:
        app_state['user_answers'].append("")
    
    app_state['user_answers'][current_q] = final_answer
    
    # Score the answer
    try:
        result_score = scorer(
            jd=app_state['jd_text'],
            ques=app_state['questions'][current_q],
            user=final_answer,
            competitor=app_state['ai_answers'][current_q]
        )
        
        # Track user score
        user_score = result_score["user"]
        app_state['track_score'].append(user_score)
        
        # Format scoring display
        user_scoring = f"""
        **Your Score:**
        Structure: {star_rating(user_score['structure_star']['score'])}
        Depth: {star_rating(user_score['depth']['score'])}
        Clarity: {star_rating(user_score['clarity']['score'])}
        Correctness: {star_rating(user_score['correctness']['score'])}
        """
        
        competitor_score = result_score["competitor"]
        ai_scoring = f"""
        **AI Competitor Score:**
        Structure: {star_rating(competitor_score['structure_star']['score'])}
        Depth: {star_rating(competitor_score['depth']['score'])}
        Clarity: {star_rating(competitor_score['clarity']['score'])}
        Correctness: {star_rating(competitor_score['correctness']['score'])}
        """
        
        return "Answer submitted successfully!", app_state, user_scoring, ai_scoring
        
    except Exception as e:
        return f"Scoring error: {str(e)}", app_state, "", ""

def navigate_question(direction, app_state):
    """Navigate between questions"""
    if direction == "prev" and app_state['current_question'] > 0:
        app_state['current_question'] -= 1
    elif direction == "next" and app_state['current_question'] < len(app_state['questions']) - 1:
        app_state['current_question'] += 1
    elif direction == "summary":
        app_state['current_page'] = 'summary'
    
    return app_state

def generate_summary_display(app_state):
    """Generate and display interview summary"""
    if app_state['current_page'] != 'summary':
        return "Summary not ready", app_state, "", gr.update(visible=False)
    
    try:
        # Ensure all answers are collected
        if not app_state['summary_data']:
            # Calculate scores
            app_state['scores'] = [
                [
                    int(track_score["structure_star"]["score"]),
                    int(track_score["depth"]["score"]),
                    int(track_score["clarity"]["score"]),
                    int(track_score["correctness"]["score"])
                ] 
                for track_score in app_state['track_score']
            ]
            
            # Generate summary
            summary_json = generate_summary_content(
                app_state['resume_text'],
                app_state['jd_text'],
                app_state['job_role'],
                app_state['questions'],
                app_state['user_answers'],
                app_state['ai_answers'],
                app_state['scores']
            )
            
            cleaned_json = clean_json_response(summary_json)
            summary_data = json.loads(cleaned_json)
            app_state['summary_data'] = summary_data
        
        summary_data = app_state['summary_data']
        
        # Calculate average score
        scores_list = app_state['scores']
        avg_score = sum([sum(q_score) for q_score in scores_list]) / (len(scores_list) * 4) * 10 if scores_list else 0
        
        # Format summary display
        summary_html = f"""
        <div class="summary-section">
            <h1>🎯 Interview Performance Summary</h1>
            
            <div class="metric-card">
                <h2>Overall Score: {avg_score:.1f}/100</h2>
                <p>Questions Analyzed: {len(summary_data.get("comparison_table", []))}</p>
                <p>Topics Covered: {len(summary_data.get("topics_covered", []))}</p>
            </div>
            
            <h2>📈 Performance Trends</h2>
            <div class="score-container">
                {summary_data.get("trends", "No trend data available")}
            </div>
            
            <div style="display: flex; gap: 20px;">
                <div style="flex: 1;">
                    <h2>💪 Your Strengths</h2>
                    <div class="strength-card">
                        {summary_data.get("strengths", "No strengths data available")}
                    </div>
                </div>
                
                <div style="flex: 1;">
                    <h2>🎯 Areas for Improvement</h2>
                    <div class="weakness-card">
                        {summary_data.get("weaknesses", "No weaknesses data available")}
                    </div>
                </div>
            </div>
            
            <h2>📚 Recommended Resources</h2>
            <div class="score-container">
                {summary_data.get("resources", "No resources available")}
            </div>
        </div>
        """
        
        # Generate text summary for download
        text_summary = generate_text_summary(summary_data, scores_list)
        
        return summary_html, app_state, text_summary, gr.update(visible=True)
        
    except Exception as e:
        return f"Error generating summary: {str(e)}", app_state, "", gr.update(visible=False)

def create_gradio_interface():
    """Create the main Gradio interface"""
    
    with gr.Blocks(css=CUSTOM_CSS, title="AI Job Matcher - HiredGPT Duel") as app:
        # State management
        app_state = gr.State(initialize_app_state())
        
        gr.Markdown("# 🤖 AI Job Matcher - HiredGPT Duel")
        gr.Markdown("Test your interview skills against an AI competitor!")
        
        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown("## 📄 Upload Your Resume")
                resume_file = gr.File(label="Resume (PDF)", file_types=[".pdf"])
                
                gr.Markdown("## 📋 Job Description")
                jd_method = gr.Radio(
                    choices=["Upload File", "Paste Text"],
                    value="Upload File",
                    label="How to provide job description?"
                )
                
                jd_file = gr.File(
                    label="Job Description File (PDF/TXT)",
                    file_types=[".pdf", ".txt"],
                    visible=True
                )
                
                jd_text = gr.Textbox(
                    label="Job Description Text",
                    lines=5,
                    visible=False
                )
                
                gr.Markdown("## ⭐ Competitor Settings")
                improve_percentage = gr.Slider(
                    minimum=10,
                    maximum=100,
                    step=10,
                    value=10,
                    label="AI Competitor Strength (%)"
                )
                
                gr.Markdown("## 💼 Job Role")
                job_role = gr.Textbox(label="Job Title/Role")
                
                start_btn = gr.Button("🚀 Start HiredGPT Duel", variant="primary")
                status_msg = gr.Markdown("")
            
            with gr.Column(scale=2):
                # Question Interface
                question_interface = gr.Group(visible=False)
                
                with question_interface:
                    progress_display = gr.Markdown("")
                    question_display = gr.Markdown("")
                    
                    with gr.Row():
                        with gr.Column():
                            gr.Markdown("### 👤 Your Answer")
                            user_answer = gr.Textbox(
                                label="Type your answer",
                                lines=6,
                                placeholder="Enter your response here..."
                            )
                            audio_input = gr.Audio(
                                label="Or record audio answer",
                                type="filepath"
                            )
                            submit_answer_btn = gr.Button("Submit Answer", variant="primary")
                            
                            user_score_display = gr.Markdown("")
                        
                        with gr.Column():
                            gr.Markdown("### 🤖 AI Competitor's Answer")
                            ai_answer_display = gr.Markdown("")
                            ai_score_display = gr.Markdown("")
                    
                    with gr.Row():
                        prev_btn = gr.Button("⬅️ Previous", visible=False)
                        next_btn = gr.Button("Next ➡️", visible=False)
                        summary_btn = gr.Button("📊 View Summary", visible=False)
                
                # Summary Interface
                summary_interface = gr.Group(visible=False)
                
                with summary_interface:
                    summary_display = gr.HTML("")
                    download_summary = gr.File(label="Download Summary", visible=False)
                    restart_btn = gr.Button("🔄 Start New Interview", variant="secondary")
        
        # Event handlers
        def toggle_jd_input(method):
            if method == "Upload File":
                return gr.update(visible=True), gr.update(visible=False)
            else:
                return gr.update(visible=False), gr.update(visible=True)
        
        jd_method.change(
            toggle_jd_input,
            inputs=[jd_method],
            outputs=[jd_file, jd_text]
        )
        
        def handle_start_click(resume, jd_file, jd_text, job_role, improve_pct, state):
            msg, new_state, interface_update = process_files_and_generate_questions(
                resume, jd_file, jd_text, job_role, improve_pct, state
            )
            
            if new_state['current_page'] == 'questions':
                question, ai_answer, progress, show_prev, show_next, _ = get_current_question_display(new_state)
                return (
                    msg, new_state, interface_update,
                    f"**{progress}**", f"### {question}",
                    "", ai_answer, "", "",
                    gr.update(visible=show_prev), gr.update(visible=show_next),
                    gr.update(visible=False), gr.update(visible=False)
                )
            
            return (
                msg, new_state, interface_update,
                "", "", "", "", "", "",
                gr.update(visible=False), gr.update(visible=False),
                gr.update(visible=False), gr.update(visible=False)
            )
        
        start_btn.click(
            handle_start_click,
            inputs=[resume_file, jd_file, jd_text, job_role, improve_percentage, app_state],
            outputs=[
                status_msg, app_state, question_interface,
                progress_display, question_display,
                user_answer, ai_answer_display, user_score_display, ai_score_display,
                prev_btn, next_btn, summary_btn, summary_interface
            ]
        )
        
        def handle_submit_answer(user_ans, audio, state):
            msg, new_state, user_scoring, ai_scoring = submit_answer(user_ans, audio, state)
            
            # Show AI answer after submission
            current_q = new_state['current_question']
            ai_answer = new_state['ai_answers'][current_q] if current_q < len(new_state['ai_answers']) else ""
            
            # Update navigation buttons
            show_prev = current_q > 0
            show_next = current_q < len(new_state['questions']) - 1
            show_summary = current_q == len(new_state['questions']) - 1
            
            return (
                new_state, ai_answer, user_scoring, ai_scoring,
                gr.update(visible=show_prev),
                gr.update(visible=show_next and not show_summary),
                gr.update(visible=show_summary)
            )
        
        submit_answer_btn.click(
            handle_submit_answer,
            inputs=[user_answer, audio_input, app_state],
            outputs=[
                app_state, ai_answer_display, user_score_display, ai_score_display,
                prev_btn, next_btn, summary_btn
            ]
        )
        
        def handle_navigation(direction, state):
            new_state = navigate_question(direction, state)
            
            if new_state['current_page'] == 'summary':
                summary_html, updated_state, text_summary, summary_visible = generate_summary_display(new_state)
                
                # Create downloadable file
                summary_file = None
                if text_summary:
                    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
                        f.write(text_summary)
                        summary_file = f.name
                
                return (
                    updated_state,
                    gr.update(visible=False), summary_visible,
                    summary_html, summary_file,
                    "", "", "", "", "", "",
                    gr.update(visible=False), gr.update(visible=False), gr.update(visible=False)
                )
            else:
                question, ai_answer, progress, show_prev, show_next, _ = get_current_question_display(new_state)
                current_q = new_state['current_question']
                user_ans = new_state['user_answers'][current_q] if current_q < len(new_state['user_answers']) else ""
                
                return (
                    new_state,
                    gr.update(visible=True), gr.update(visible=False),
                    "", None,
                    f"**{progress}**", f"### {question}", user_ans, ai_answer, "", "",
                    gr.update(visible=show_prev), gr.update(visible=show_next),
                    gr.update(visible=current_q == len(new_state['questions']) - 1)
                )
        
        prev_btn.click(
            lambda state: handle_navigation("prev", state),
            inputs=[app_state],
            outputs=[
                app_state, question_interface, summary_interface,
                summary_display, download_summary,
                progress_display, question_display, user_answer, ai_answer_display,
                user_score_display, ai_score_display,
                prev_btn, next_btn, summary_btn
            ]
        )
        
        next_btn.click(
            lambda state: handle_navigation("next", state),
            inputs=[app_state],
            outputs=[
                app_state, question_interface, summary_interface,
                summary_display, download_summary,
                progress_display, question_display, user_answer, ai_answer_display,
                user_score_display, ai_score_display,
                prev_btn, next_btn, summary_btn
            ]
        )
        
        summary_btn.click(
            lambda state: handle_navigation("summary", state),
            inputs=[app_state],
            outputs=[
                app_state, question_interface, summary_interface,
                summary_display, download_summary,
                progress_display, question_display, user_answer, ai_answer_display,
                user_score_display, ai_score_display,
                prev_btn, next_btn, summary_btn
            ]
        )
        
        def restart_app():
            return initialize_app_state(), gr.update(visible=False), gr.update(visible=False)
        
        restart_btn.click(
            restart_app,
            outputs=[app_state, question_interface, summary_interface]
        )
    
    return app

if __name__ == "__main__":
    # Create and launch the Gradio app
    app = create_gradio_interface()
    app.launch(
        
        server_port=7860,
        share=False,
        debug=True
    )