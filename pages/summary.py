import streamlit as st
import json
import re
import pandas as pd
from core.generate_summary import generate_summary_content
from core.test import resume, jd, jr, questions, ai_answers, user_answers, scores

# Update the custom CSS to include full width container settings
custom_css = """
<style>
    /* Main colors and styling - adaptive to Streamlit's themes */
    :root {
        --primary: #A370F7;        /* Light purple */
        --primary-light: #BF9DF8;  /* Lighter purple */
        --secondary: #14B8A6;      /* Kept teal as it works well with purple */
        --danger: #FF4B4B;
        --warning: #F7B32B;
        --info: #4B9EFF;           /* Blue for links */
        --success: #14B8A6;
        --header-color: #A370F7;   /* Changed to purple */
        --text-color: #FFFFFF;
    }
    
    /* Custom download button styling */
    .stDownloadButton button {
        background-color: #4B9EFF !important;
        color: white !important;
        border: none !important;
        font-weight: 500 !important;
        padding: 0.5rem 1rem !important;
    }
    
    .stDownloadButton button:hover {
        background-color: var(--primary-light) !important;
        color: white !important;
    }
    
    /* Download button container */
    .download-btn-container {
        text-align: center;
        display: flex;
        justify-content: center;
        margin: 1rem auto;
    }
    
    /* Ensure full width */
    .block-container {
        max-width: 100% !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
    }
    
    /* Page header styling */
    .page-header {
        padding: 0.8rem 0 0 0;
        margin-bottom: 1.5rem;
    }
    
    .page-title {
        font-size: 3.2rem;
        font-weight: 700;
        margin-bottom: 0.4rem;
        padding-bottom: 0.5rem;
        /* Color is now set inline */
    }
    
    .page-subtitle {
        font-size: 1rem;
    }
    
    /* Section dividers */
    .section-divider {
        margin: 1.5rem 0;
        height: 1px;
        background-color: rgba(255, 255, 255, 0.1);
        border: none;
    }
    
    /* Right sidebar styling */
    .right-sidebar {
        padding: 1rem 0;
    }
    
    /* Topic list sidebar styling */
    .topic-list-sidebar {
        margin-top: 1rem;
        padding: 1rem;
        background-color: transparent;
    }
    
    .topic-list-title {
        font-size: 2rem;
        font-weight: 600;
        color: var(--header-color);
        margin-bottom: 0.8rem;
    }
    
    .sidebar-topic-badge {
        background-color: var(--primary);
        color: var(--text-color);
        padding: 0.3rem 0.6rem;
        border-radius: 12px;
        margin: 0.15rem;
        display: inline-block;
        font-weight: 500;
        font-size: 0.75rem;
    }
    
    /* Metric cards with more vibrant colors */
    .metric-container {
        display: flex;
        justify-content: space-between;
        gap: 0.8rem;
        margin-bottom: 1.5rem;
    }
    
    .metric-card {
        background: var(--primary);
        color: var(--text-color);
        border-radius: 10px;
        padding: 1.2rem;
        flex: 1;
        text-align: center;
        box-shadow: 0 3px 10px rgba(0, 0, 0, 0.1);
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 0.4rem;
    }
    
    .metric-label {
        font-size: 0.8rem;
        opacity: 0.9;
        letter-spacing: 0.4px;
        text-transform: uppercase;
    }
    
    /* Section headers - line comes after text */
    .section-header {
        font-size: 1.4rem;
        font-weight: 600;
        color: var(--header-color);
        margin: 1.5rem 0 0.8rem 0;
        padding-bottom: 0.4rem;
        border-bottom: 2px solid rgba(255, 75, 75, 0.3);
    }
    
    /* Sub-section headers */
    .sub-header {
        font-size: 1.1rem;
        font-weight: 600;
        color: var(--header-color);
        margin: 1rem 0 0.6rem 0;
        border-bottom: none;
    }
    
    /* Topic badges */
    .topic-badge {
        background-color: var(--primary);
        color: var(--text-color);
        padding: 0.4rem 0.8rem;
        border-radius: 16px;
        margin: 0.2rem;
        display: inline-block;
        font-weight: 500;
        font-size: 0.8rem;
    }
    
    /* Resource links styling */
    .resource-item a {
        color: var(--info);
        text-decoration: none;
        transition: color 0.2s;
    }
    
    .resource-item a:hover {
        color: var(--primary-light);
        text-decoration: underline;
    }
    
    /* Transparent backgrounds for info boxes */
    .stInfo {
        background-color: rgba(75, 158, 255, 0.1) !important;
        border-left: 3px solid var(--info) !important;
        border-top: none !important;
        border-right: none !important;
        border-bottom: none !important;
    }
    
    .stSuccess {
        background-color: rgba(20, 184, 166, 0.1) !important;
        border-left: 3px solid var(--success) !important;
        border-top: none !important;
        border-right: none !important;
        border-bottom: none !important;
    }
    
    /* Strengths and weakness cards */
    .strength-card {
        background-color: rgba(20, 184, 166, 0.1);
        border-left: 3px solid var(--success);
        padding: 0.8rem;
        margin-bottom: 0.8rem;
        border-radius: 4px;
        font-size: 0.9rem;
    }
    
    .weakness-card {
        background-color: rgba(255, 75, 75, 0.1);
        border-left: 3px solid var(--danger);
        padding: 0.8rem;
        margin-bottom: 0.8rem;
        border-radius: 4px;
        font-size: 0.9rem;
    }
    
    /* Override Streamlit's default text size */
    .stMarkdown {
        font-size: 0.9rem !important;
    }
    
    /* Override streamlit headers */
    h1 {
        font-size: 2.2rem !important;
        color: var(--header-color) !important;
    }
    
    h2 {
        font-size: 1.4rem !important;
        color: var(--header-color) !important;
    }
    
    h3 {
        font-size: 1.1rem !important;
        color: var(--header-color) !important;
    }
    
    h4, h5, h6 {
        font-size: 1rem !important;
        color: var(--header-color) !important;
    }
</style>
"""

def clean_json_response(response_text):
    """Remove markdown code formatting and other unwanted characters from JSON responses"""
    # Remove markdown code block syntax (```json and ```)
    response_text = re.sub(r'^```json\s*', '', response_text)
    response_text = re.sub(r'```json', '', response_text)
    response_text = re.sub(r'\s*```$', '', response_text)
    response_text = re.sub(r'```', '', response_text)
    
    # Find the actual JSON content - from first { to last }
    start_idx = response_text.find('{')
    end_idx = response_text.rfind('}') + 1
    
    if start_idx >= 0 and end_idx > start_idx:
        return response_text[start_idx:end_idx]
    
    return response_text

def generate_text_summary(summary_data, scores_list, username, current_datetime):
    """Generate a plain text version of the summary for downloading"""
    # Calculate average score
    avg_score = sum([sum(q_score) for q_score in scores_list]) / (len(scores_list) * 4) * 10
    
    # Format topics as a comma-separated list
    topics = summary_data.get("topics_covered", [])
    topics_str = ", ".join(topics) if isinstance(topics, list) else str(topics)
    
    # Build the text summary
    text_summary = f"""INTERVIEW PERFORMANCE SUMMARY
==============================
OVERVIEW
------------------------------
Overall Score: {avg_score:.1f}/100
Questions Analyzed: {len(summary_data.get('comparison_table', []))}
Topics Covered: {topics_str}

PERFORMANCE OVERVIEW
------------------------------
{summary_data.get('trends', 'No trend data available')}

YOUR STRENGTHS
------------------------------
{summary_data.get('strengths', 'No strengths data available')}

AREAS FOR IMPROVEMENT
------------------------------
{summary_data.get('weaknesses', 'No weaknesses data available')}

QUESTION ANALYSIS
------------------------------
"""
    
    # Add each question analysis
    for i, item in enumerate(summary_data.get('comparison_table', [])):
        text_summary += f"\nQ{i+1}: {item.get('question', 'Question')}\n"
        text_summary += f"Key Differences: {item.get('differences', 'No comparison available')}\n"
        text_summary += f"Strong Phrases: {item.get('strong_phrases', 'No notable phrases identified')}\n"
    
    # Add resources
    text_summary += "\nRECOMMENDED RESOURCES\n"
    text_summary += "------------------------------\n"
    
    resources = summary_data.get("resources", "No resources available")
    if isinstance(resources, str):
        if "\n" in resources:
            resources_list = resources.split("\n")
            for resource in resources_list:
                if resource.strip():  # Skip empty lines
                    text_summary += f"- {resource}\n"
        else:
            text_summary += f"- {resources}\n"
    
    return text_summary

def display_summary_page():
    # Set page configuration to wide mode
    st.set_page_config(layout="wide")
    
    # Apply custom CSS
    st.markdown(custom_css, unsafe_allow_html=True)
    
    # Current date/time and username - updated to latest values
    current_datetime = "2025-05-30 21:11:21"  # Updated timestamp
    username = "AmalNLal"  # Same username
    
    # Check if we have the necessary session state variables
    required_vars = ['resume', 'job_description', 'job_role', 'questions', 
                     'ai_answers', 'user_answers', 'scores']
    
    # For development/testing: If session state doesn't have the data, we can use test data
    if any(var not in st.session_state for var in required_vars):
        if st.checkbox("Use test data for development", value=True):
            st.session_state.update({
                'resume': resume,
                'job_description': jd,
                'job_role': jr,
                'questions': questions,
                'ai_answers': ai_answers,
                'user_answers': user_answers,
                'scores': scores
            })
        else:
            st.error("Please complete the interview process first to generate a summary.")
            return
    
    # Generate or retrieve summary
    if 'summary_data' not in st.session_state:
        with st.spinner("Analyzing your interview performance..."):
            try:
                summary_json = generate_summary_content(
                    st.session_state.resume,
                    st.session_state.job_description,
                    st.session_state.job_role,
                    st.session_state.questions,
                    st.session_state.user_answers,
                    st.session_state.ai_answers,
                    st.session_state.scores
                )
                
                # Clean the JSON response before parsing
                cleaned_json = clean_json_response(summary_json)
                
                try:
                    summary_data = json.loads(cleaned_json)
                    st.session_state.summary_data = summary_data
                except json.JSONDecodeError as e:
                    st.error(f"Error parsing summary data: {e}")
                    st.code(summary_json)  # Show the raw response for debugging
                    return
            except Exception as e:
                st.error(f"Error generating summary: {e}")
                return
    
    summary_data = st.session_state.summary_data
    
    # Process lists into strings for strengths, weaknesses, resources if needed
    for key in ["strengths", "weaknesses", "resources"]:
        if key in summary_data and isinstance(summary_data[key], list):
            summary_data[key] = "\n".join(summary_data[key])
    
    # Ensure topics are processed correctly - fix for topic badges
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
    
    # Calculate average score
    scores_list = st.session_state.scores
    avg_score = sum([sum(q_score) for q_score in scores_list]) / (len(scores_list) * 4) * 10  # Assuming 4 criteria per question
    
    # Generate text summary for download button (do this before the page layout)
    text_summary = generate_text_summary(summary_data, scores_list, username, current_datetime)
    
    # Page header with styled title - moved above the line
    st.markdown('<div class="page-header">', unsafe_allow_html=True)
    st.markdown('<h1 class="page-title" style="color: white;">Interview Performance Summary</h1>', unsafe_allow_html=True)
    
    st.markdown(f'<p>Review your performance and get insights to improve your next interview.</p>', unsafe_allow_html=True)
    st.markdown('<hr style="height:1px;border:none;background-color:#E8E0D0;">', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Center the download button using columns
    left_space, download_col, right_space = st.columns([3, 4, 3])
    
    with download_col:
        st.markdown('<div class="download-btn-container">', unsafe_allow_html=True)
        st.download_button(
            label="Download Summary",
            data=text_summary,
            file_name=f"interview_summary_{username}_{current_datetime.replace(' ', '_').replace(':', '-')}.txt",
            mime="text/plain",
            use_container_width=True  # Make button take full column width
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Create a layout with right sidebar for metrics and main content on left - adjusted ratio
    left_col, right_col = st.columns([8, 2])  # Changed from 7:3 to 8:2
    
    # Right column - Display metrics
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
        
        # Questions Analyzed
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{len(summary_data.get("comparison_table", []))}</div>
            <div class="metric-label">Questions Analyzed</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Add topic list below the metrics in the right sidebar - fixed to show full topics
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
    
    # Left column - Main content
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
        
        # Process resources into HTML list with links
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


# Run the function
if __name__ == "__main__":
    display_summary_page()