import re

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


def generate_text_summary(summary_data, scores_list):
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
