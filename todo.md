# HiredGPT Duel - TODO List

## High Priority Tasks

### PDF Parser (Assigned to: Kunjan)
- [x] Implement resume reading functionality
- [x] Implement job description reading functionality

### Question Generation (Assigned to: Kunjan)
- [x] Create question generator based on resume and job description
  - [x] [**Improve Question Quality**]
- [x] Add Groq Client in model.py.
- [x] Create utils.py file.
- [ ] Create a separate file for the question agent
  - [x] [**Improve Question Quality**]
- [x] Add Groq Client in model.py.
- [x] Create utils.py file.
- [x] Create a separate file for the question agent
- [ ] Integrate Whisper STT Agent

### UI Components (Assigned to: Aryman)
- [x] Implement user per-question submit button
- [x] Add next question button
- [x] No Need for Scrolling, Previous and Next Question button is ok.
    
- [x] Create a summary view at the end of interview (UI)
  - [x] Generate a summary prompt  
- [x] No Need for Scrolling, Previous and Next Question button is ok.


### Metrics and Analysis (Assigned to: Amal)
- [x] Develop per-question metrics with visualizations
- [x] Implement competitor resume enhancement:
- [x] Develop per-question metrics with visualizations
- [x] Implement competitor resume enhancement:
  - [x] Extract 5 key factors from job description
  - [x] For each experience/project, level up with respect to the 5 factors
  - [x] For each experience/project, level up with respect to the 5 factors

## Low Priority Tasks
- [x] Add user character limit/time limit 
- [x] Implement voice input functionality on streamlit (st.audio_input)
- [x] Add user character limit/time limit 
- [x] Add competitor text-to-speech capability
      
- [ ] Add downloadable txt file for session results


- [x] Remove Resume and JD preview from top.
- [x] Interview Duel should always be displayed.
- [ ] Time skip for rival answer.
- [x] Rival answer duplication.
- [x] Submit button twice click issue.
- [ ] Deployment of the whole app and hosting.  
