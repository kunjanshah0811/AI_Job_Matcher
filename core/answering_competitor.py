from core.model import generate_response
from core.test import resume, jd,questions

class Answering_competitor:
    def __init__(self,resume,job_description,difficulty_level,questions):
        self.resume = resume
        self.job_description = job_description
        self.difficulty_level = int(difficulty_level)
        self.questions = questions
        self.persona = None
        self.factors = None


    def extract_factors(self):
        if self.factors is not None :
            return self.factors

        system_prompt = """
                You are an expert job analysis AI specialized in distilling job descriptions to their core requirements.        
                Your task is to analyze a job description and identify the 5 most critical factors that will determine success in this role. Focus on extracting:
                    1. Required Technical Skills: The specific technical abilities and knowledge domains essential for this position
                    2. Key Responsibilities: The main tasks and responsibilities that form the core of this role
                Only include specific and relevant terms (e.g., 'machine learning', 'project management', 'AWS', 'data analysis', 'React') — avoid vague or general terms like 'team player' or 'communication skills'.
                Your output must be a valid list in the format: "Factor1", "Factor2", "Factor3", "Factor4", "Factor5"
            """
        user_prompt = f"""
                Extract the 5 key factors (each max 2 words) that most strongly influence the job role described below. 
                Here is the Job Description: {self.job_description}
                """
        self.factors = generate_response(system_prompt,user_prompt)
        return self.factors

    def determine_enhancement(self):
        if self.difficulty_level <= 20:
            self.enhancement_description = "slightly more impressive"
            self.intensity = "modest"
        elif self.difficulty_level <= 30 :
            self.enhancement_description = "noticeably more impressive"
            self.intensity = "significant"
        elif self.difficulty_level <= 60:
            self.enhancement_description = "substantially more impressive"
            self.intensity = "extensive"
        else:
            self.enhancement_description = "dramatically more impressive"
            self.intensity = "comprehensive"
        return (self.enhancement_description, self.intensity)

    def generate_resume(self):
        if self.persona is not None :
            return self.persona
        
        if not hasattr(self, 'enhancement_description') or not hasattr(self, 'intensity'):
            self.determine_enhancement()

        
        system_prompt = f"""
            You are an expert resume enhancer tasked with creating a stronger competitor version of a candidate's resume.
            
            Your job is to create a resume that is {self.enhancement_description} than the original (approximately {self.difficulty_level}% stronger) by:
            1. Enhancing technical skills with {self.intensity} additions of relevant technologies and frameworks
            2. Upgrading project descriptions with more advanced concepts and technical depth
            3. Making work experience more impactful with better metrics and higher achievement levels
            4. Improving the overall impression of expertise, seniority, and capabilities
            
            IMPORTANT RULES:
            - Keep the same basic career trajectory and education
            - Don't add fictional jobs or degrees
            - Maintain the same job titles and employers but enhance accomplishments
            - Focus particularly on the key factors identified from the job description
            - The enhanced resume should be realistic for someone with {self.difficulty_level}% more expertise
            - Preserve the overall format and structure of the original resume
            """
    
        user_prompt = f"""
            I need you to create a more competitive version of this candidate's resume.
            Original resume:{self.resume}
            Job description they're applying for:{self.job_description}
            Key factors to focus enhancement on (these are the most important for the job):{self.factors}            
            Please create a resume that is approximately {self.difficulty_level}% stronger than the original, focusing especially on enhancing the areas related to the key factors.
            Return ONLY the enhanced resume with the fixed header above and formatted consistently with the original resume structure.
        """

        self.persona= generate_response(system_prompt, user_prompt)
        return self.persona
        
    def answer_questions(self):
        if self.persona is None :
            self.generate_resume()
        
        answers={}

        system_prompt = f"""
        You are an AI interview coach creating responses for a job candidate.
        You are helping prepare a candidate for a job interview. Their enhanced resume is:{self.persona}
        They are applying for this job:{self.job_description}
        
        Your task is to write interview question responses AS IF YOU WERE THIS CANDIDATE.
        Each response must:
        1. Be written in first person (I, my, mine)
        2. Reflect the skills, experience, and qualifications in the enhanced resume.
        3. Be tailored to the job requirements and context of questions
        4. Show confidence, clarity, and competence but realistic
        5. Be approximately 500 characters long (about 3-4 sentences)
        6. Include specific examples from the resume when relevant
        7. Show enthusiasm and cultural fit
        You may use STAR (Situation, Task, Action, Result) format if appropriate, especially for behavioral questions.
        DO NOT mention that you're an AI or that this is preparation - write as if you are the actual candidate.
        """

        for i,question in enumerate(self.questions,1):
            user_prompt = f"""
                        Question {i} : {question}
                        Please provide a response that is about 500 characters (3-4 sentences).
                        Write AS THE CANDIDATE, not as an AI assistant.
                        Use the candidate's background from the enhanced resume to create a realistic answer.
                    """
            
            answer=generate_response(system_prompt,user_prompt)
            answers[i]=answer.strip()
        return answers

if __name__=="__main__":
    obj=Answering_competitor(resume,jd,20,questions)  
    factors=obj.extract_factors()  
    obj.determine_enhancement()
    competitor_resume=obj.generate_resume()
    answers=obj.answer_questions()
    print(answers)
