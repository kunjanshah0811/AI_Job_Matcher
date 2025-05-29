# HiredGPT Duel  
A competitive interview simulation platform that shows how you stack up against top candidates

<img alt="HiredGPT Duel" src="https://img.shields.io/badge/Status-In Development-yellow">
<img alt="Python" src="https://img.shields.io/badge/Python-3.9+-blue">
<img alt="Streamlit" src="https://img.shields.io/badge/Streamlit-1.28+-red">

---

## 🚀 Overview  
**HiredGPT Duel** provides a unique interview preparation experience by simulating a head-to-head competition between you and an AI-generated "star candidate." Unlike traditional interview coaching tools that only evaluate your responses in isolation, our platform shows you how your answers compare to a top-tier candidate in real time.

The AI competitor uses your same resume but with subtle enhancements, creating a realistic benchmark for improvement while giving you actionable insights on how to level up your interview performance.

---

## ✨ Key Features
- **Dual-Track Interview Simulation**: Practice alongside an AI competitor to see where you stand  
- **Resume-Based Question Generation**: Get personalized interview questions based on your resume and target job  
- **Enhanced AI Competitor**: Compete against a slightly stronger version of yourself (10% better)  
- **Real-Time Performance Comparison**: See side-by-side answer evaluation after each response  
- **Voice & Text Input**: Choose your preferred way to answer questions  
- **Detailed Scoring System**: Understand exactly where and why you gain or lose points  
- **Actionable Improvement Suggestions**: Get concrete advice on how to improve your responses  

---

## 📋 How It Works
1. Upload your resume and job description to set the interview context  
2. The system generates 5 relevant interview questions based on your materials  
3. Answer each question via text or voice input  
4. See how the AI competitor answers the same question (using an enhanced version of your resume)  
5. Review the side-by-side comparison showing strengths and weaknesses of each answer  
6. Get a final report with actionable improvement suggestions  

---

## 🛠️ Technology Stack

Frontend: Streamlit  
AI Models: Google Gemini models  
Speech Recognition: SpeechRecognition library  
Document Processing:PyPDF2  

--- 

## 🏗️ Project Structure

    AI_Job_Matcher/
    ├── .env                          # API keys and configuration
    ├── main.py                       # Application entry point
    ├── requirements.txt              # Dependencies
    ├── README.md                     # Project documentation
    │
    ├── core/                         # Core functionality
    │   ├── model.py                  # LLM interaction
    │   ├── speech_converter.py       # Speech recognition module
    │   ├── input_comp_gen.py         # UI
    │   ├── question_generator.py     # Generates interview questions from resume/JD
    │   ├── response_evaluator.py     # Scores and compares responses
    │   └── answering_competitor.py   # AI persona generation
    │
    ├── data/                         # Data storage
    │   ├── resumes/                  # User uploaded resumes
    │   ├── job_descriptions/         # Job descriptions
    │   └── session_history/          # Saved interview sessions
    │
    ├── ui/                           # User interface components
    └── utils/                        # Helper utilities