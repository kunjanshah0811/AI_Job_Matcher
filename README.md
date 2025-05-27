# AI_Job_Matcher

### “HiredGPT Duel” – Competitive Chat Simulation vs. Another Applicant
Element	Quick Pitch\ 
Problem	Interview coaching tools ignore relative performance—you never know how you’d stack up against the other top candidate.
Innovation	Two tracks: User vs AI rival. LLM plays both interviewer and a benchmark “star applicant” using the same résumé—but 10 % stronger in each key area. After every question the tool shows a realtime split-screen answer comparison and highlights where you lost points.
One-We

1. Resume and jd as input
2. Generate 5 interview questions / include follow-up questions .
2.1 generate 10% better resume for the competitor which will act as a persona.
3. First user answers via text / speech and side by side llm (10% smarter) also answers.
4. LLM as a scorer, grades both responses based on some criteria.
5. Suggestions from llm on how to improve at the end.



AI_Job_Matcher/
├── .env                          # API keys and configuration
├── main.py                       # Application entry point
├── requirements.txt              # Dependencies
├── README.md                     # Your project description
│
├── core/                         # Core functionality
│   ├── __init__.py
│   ├── model.py                  # LLM interaction (your existing file)
│   ├── audio_to_text.py          # Speech recognition module
│   ├── resume_enhancer.py        # Creates 10% enhanced resume for AI competitor
│   ├── question_generator.py     # Generates interview questions from resume/JD
│   └── response_evaluator.py     # Scores and compares user vs AI responses
│
├── data/                         # Data storage
│   ├── resumes/                  # User uploaded resumes
│   ├── job_descriptions/         # Job descriptions
│   └── session_history/          # Saved interview sessions
│
├── ui/                           # User interface
│   ├── __init__.py
│   ├── app.py                    # Main UI wrapper (Streamlit/Flask)
│   ├── components/               # UI components
│   │   ├── comparison_view.py    # Side-by-side answer comparison
│   │   ├── score_display.py      # Real-time scoring visualization
│   │   └── chat_interface.py     # Q&A interface
│   └── static/                   # CSS, JS, images if using web interface
│
└── utils/                        # Helper utilities
    ├── __init__.py
    ├── prompt_templates.py       # System prompts for different LLM roles
    ├── text_processor.py         # Text processing utilities
    └── session_manager.py        # Manages interview session state