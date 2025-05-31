Demo Script: HiredGPT 

DuelHiredGPT Duel – Competitive Interview Simulation

Hello everyone,

I’m Amal, and this is HiredGPT Duel – a competitive interview simulator that shows you exactly how you stack up against a top-tier candidate.

1 — Problem & Idea\
Most interview-prep tools grade you in isolation. You get a score, but no sense of what great really looks like.
HiredGPT Duel fixes that by pitting you against an AI “star applicant” who’s about 10 percent stronger than your own résumé. After every answer you see a side-by-side comparison and immediate feedback.

2 — Quick Walk-through\
1. Upload your resume and the target job description in pdf format or paste job description text format. 

2. Pick how much stronger the rival should be—10 to 100 percent—or leave it at the default 10 percent.

3. Enter the job role you are targeting

4. Submit to generate rival resume and interview questions.

5. Behind the scenes, the system generates (LLM) interview questions based on submited resume JD and job description with few shot prompt engineering tech. 

6. System generates difficulty level, job desciption, resume and key factors exteacted. 
Now we jump into the duel.

- Question view
on the top 

- Answer the question—type or speak. If you record audio, Whisper transcribes it instantly.
- Click “Generate Rival Answer.” The AI competitor responds using the upgraded résumé.
- 














3 — Tech Highlights
Frontend: Streamlit for a fast, sharable UI.

LLMs: Google Gemini (via Groq client) for question generation, résumé enhancement, rival answers, and scoring and report generation. 

Speech-to-Text: OpenAI Whisper running locally for offline transcription

Text-to-Speech: pyttsx3 python library. if you’d like the rival to read answers aloud.

Document Handling: PyPDF2 for parsing PDFs.
Everything runs on-device except the LLM calls, keeping latency low and privacy high.



