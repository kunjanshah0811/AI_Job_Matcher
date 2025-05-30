import streamlit as st

# Configure page settings
st.set_page_config(
    page_title="AI Job Matcher",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
custom_css = """
<style>
    /* Main color palette */
    :root {
        --primary: #4F46E5;
        --primary-light: #818CF8;
        --secondary: #10B981;
        --bg-dark: #111827;
        --text-light: #F9FAFB;
    }
    
    /* Header styling with background */
    .header-section {
        position: relative;
        padding: 3rem 2rem;
        margin-bottom: 2rem;
        overflow: hidden;
    }
    
    .header-bg {
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
        border-radius: 12px;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
        z-index: -2;
    }
    
    /* Header Styling */
    .main-header {
        background: linear-gradient(90deg, #38BDF8, #818CF8, #C084FC);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 4.2rem !important;
        font-weight: 800 !important;
        margin-bottom: 0.2rem !important;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
        letter-spacing: -1px;
        position: relative;
        z-index: 1;
    }
    
    /* Add glow effect */
    .header-glow {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        width: 80%;
        height: 80%;
        background: radial-gradient(circle, rgba(56, 189, 248, 0.2) 0%, rgba(129, 140, 248, 0.1) 50%, rgba(192, 132, 252, 0) 100%);
        filter: blur(40px);
        z-index: -1;
    }
    
    .subheader {
        font-size: 1.6rem !important;
        color: #CBD5E1 !important;
        font-weight: 400 !important;
        margin-bottom: 0.5rem !important;
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.3);
        position: relative;
        z-index: 1;
    }
    
    /* Button styling */
    .start-button {
        background-color: var(--primary);
        color: white;
        padding: 0.75rem 2rem;
        font-size: 1.2rem;
        font-weight: 600;
        border-radius: 8px;
        border: none;
        cursor: pointer;
        transition: all 0.3s ease;
        display: inline-block;
        margin: 1.5rem 0;
        text-align: center;
        text-decoration: none;
    }
    
    .start-button:hover {
        background-color: var(--primary-light);
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(79, 70, 229, 0.3);
    }
    
    /* Feature list */
    .feature-list li {
        margin-bottom: 0.8rem;
        font-size: 1.1rem;
        color: #1F2937;
    }
    
    /* Feature icons */
    .feature-icon {
        color: var(--secondary);
        margin-right: 0.5rem;
    }
    
    /* Hide menu and footer */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Metrics styling */
    .metric-card {
        background: linear-gradient(135deg, #4F46E5 0%, #818CF8 100%);
        color: white;
        border-radius: 10px;
        padding: 1.2rem;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        margin: 0.5rem 0;
    }
    
    .metric-label {
        font-size: 1rem;
        opacity: 0.8;
    }
</style>
"""

# Apply the CSS
st.markdown(custom_css, unsafe_allow_html=True)

# Header with background behind it instead of around it
st.markdown("""
<div class="header-section">
    <div class="header-bg"></div>
    <div class="header-glow"></div>
    <h1 class="main-header">AI Job Matcher</h1>
    <p class="subheader">Prepare for your dream job with AI-powered interview practice</p>
</div>
""", unsafe_allow_html=True)

# Call-to-action button that redirects to interview page
def go_to_interview():
        # This creates a session state variable that can be checked by pages/1_Interview.py
        st.session_state.page = "interview"
        
    # Check if we need to create the button with the on_click handler
if st.button("🚀 Start Interview Practice", key="start_button", on_click=go_to_interview, 
                help="Click to begin your practice interview session"):
        # This won't actually run because the page will rerun with the new state
        pass
        
st.markdown("<br>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-label">Users Helped</div>
        <div class="metric-value">1,500+</div>
        <div class="metric-label">professionals worldwide</div>
    </div>
    """, unsafe_allow_html=True)
    
with col2:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-label">Interview Success Rate</div>
        <div class="metric-value">+45%</div>
        <div class="metric-label">higher job offer rates</div>
    </div>
    """, unsafe_allow_html=True)
    
with col3:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-label">Score Improvement</div>
        <div class="metric-value">+28%</div>
        <div class="metric-label">after just 3 practice sessions</div>
    </div>
    """, unsafe_allow_html=True)

# Create two columns for main content
col1, col2 = st.columns([3, 2])

with col1:
    # Main content directly without the info card
    st.markdown('<h3 style="color: #4F46E5; margin-bottom: 1rem;">Level Up Your Interview Skills</h3>', unsafe_allow_html=True)
    st.markdown('<p style="font-size: 1.1rem; margin-bottom: 1.5rem;">AI Job Matcher uses advanced AI to simulate realistic job interviews tailored to your target position. Get instant feedback, expert analysis, and practical tips to improve your performance.</p>', unsafe_allow_html=True)
    
    st.markdown("""
    <ul class="feature-list">
        <li><span class="feature-icon">🎯</span> Practice with AI-generated questions specific to your job</li>
        <li><span class="feature-icon">📊</span> Receive detailed feedback and scoring on your answers</li>
        <li><span class="feature-icon">🔄</span> Compare your responses with optimized examples</li>
        <li><span class="feature-icon">📈</span> Track your improvement over multiple practice sessions</li>
    </ul>
    """, unsafe_allow_html=True)
    
with col2:    
    # Additional text without the info card wrapper
    st.markdown('<p style="color: #4F46E5; margin-top: 1rem; margin-bottom: 0.5rem;">Why Practice with AI?</p>', unsafe_allow_html=True)
    st.markdown('<p>Practice in a stress-free environment before your actual interview. Our AI provides honest feedback to help you improve in areas that matter most.</p>', unsafe_allow_html=True)


# Additional space at the bottom for better layout
st.markdown("<br><br>", unsafe_allow_html=True)