from model import generate_response

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
    resume= """
                ALEX JOHNSON
                Email: alex.johnson@email.com | Phone: (555) 123-4567
                Address: Seattle, WA 98101 | LinkedIn: linkedin.com/in/alexjohnson
                GitHub: github.com/ajohnson

                PROFESSIONAL SUMMARY
                Detail-oriented Computer Engineer with a strong foundation in software development and hardware systems. 
                Skilled in programming languages including Python, Java, and C++. 
                Passionate about creating efficient solutions and implementing new technologies.

                EDUCATION
                BACHELOR OF SCIENCE IN COMPUTER ENGINEERING
                University of Washington
                2018 - 2022
                Relevant Coursework: Computer Architecture, Digital Systems Design, Software Engineering, Database Systems, Operating Systems

                TECHNICAL SKILLS
                • Programming Languages: Python, Java, C++, JavaScript
                • Hardware: PCB Design, Microcontroller Programming, Digital Circuit Design
                • Software: MATLAB, Visual Studio, Git, Linux/Unix
                • Web Technologies: HTML, CSS, React.js
                • Database Systems: SQL, MongoDB

                PROJECTS
                SMART HOME MONITORING SYSTEM
                • Designed and built an IoT-based monitoring system using Raspberry Pi and Arduino
                • Implemented sensors for temperature, humidity, and motion detection
                • Created a web interface for remote monitoring using React.js and Node.js

                INVENTORY MANAGEMENT APPLICATION
                • Developed a desktop application for inventory tracking using Java
                • Implemented database functionality with MySQL for data persistence
                • Created user-friendly interface with filtering and reporting capabilities

                EXPERIENCE
                SOFTWARE ENGINEERING INTERN
                TechSolutions Inc. | Seattle, WA
                Summer 2021
                • Assisted in developing and testing code for client-facing applications
                • Participated in code reviews and debugging sessions
                • Collaborated with team members using Agile methodology
                • Documented software processes and requirements

                COMPUTER LAB ASSISTANT
                University of Washington | Seattle, WA
                2019 - 2022
                • Assisted students with hardware and software troubleshooting
                • Maintained lab equipment and installed software updates
                • Conducted basic workshops on programming fundamentals

                CERTIFICATIONS
                • CompTIA A+ Certification - 2021
                • Cisco Certified Network Associate (CCNA) - 2022
            """

    jd="""
        COMPANY: Tech Innovations Inc.
        LOCATION: San Francisco, CA (Hybrid)
        POSITION: Software Engineer

        ABOUT US:
        Tech Innovations Inc. is a leading software company specializing in cloud-based solutions and AI-driven applications. 
        We are currently seeking a talented and motivated Software Engineer to join our growing development team.

        JOB DESCRIPTION:
        We are looking for a Software Engineer with strong programming skills to design, develop, and maintain efficient, reusable, and reliable code. You will be part of a cross-functional team that is responsible for the full software development life cycle, from conception to deployment.

        RESPONSIBILITIES:
        • Design and develop high-quality software solutions that meet project requirements
        • Write clean, maintainable, and efficient code following best practices
        • Collaborate with cross-functional teams to define, design, and ship new features
        • Troubleshoot, debug, and upgrade existing systems
        • Participate in code reviews and mentor junior developers
        • Work with product managers to understand end-user requirements and translate them into technical specifications
        • Ensure the performance, quality, and responsiveness of applications
        • Monitor and improve application performance and reliability

        REQUIREMENTS:
        • Bachelor's degree in Computer Science, Engineering, or related field
        • 2+ years of professional software development experience
        • Strong proficiency in one or more programming languages (Java, Python, C++, JavaScript)
        • Experience with front-end technologies (React, Angular, or Vue.js)
        • Knowledge of database systems (SQL, NoSQL) and data structures
        • Familiarity with version control tools (Git) and continuous integration processes
        • Strong problem-solving skills and attention to detail
        • Excellent communication and teamwork skills
        • Experience with cloud services (AWS, Azure, or GCP) preferred
        • Knowledge of agile development methodologies

        WHAT WE OFFER:
        • Competitive salary and benefits package
        • Professional growth opportunities
        • Flexible work arrangements
        • Collaborative and innovative work environment
        • Opportunity to work with cutting-edge technologies
        • Regular team building activities and events

        Tech Innovations Inc. is an equal opportunity employer. We celebrate diversity and are committed to creating an inclusive environment for all employees.

        """
    
    questions= [
    "Tell me about your experience with software development and how it prepares you for this role.",
    "Describe a challenging project you worked on and how you approached problem-solving during its development.",
    "How do you stay current with emerging technologies and programming languages in the fast-paced tech industry?",
    "Can you share your experience working in Agile development environments and how you collaborate with cross-functional teams?",
    "What experience do you have with cloud services, and how have you implemented them in your previous projects?"
    ]   

    obj=Answering_competitor(resume,jd,20,questions)  
    factors=obj.extract_factors()  
    obj.determine_enhancement()
    competitor_resume=obj.generate_resume()
    answers=obj.answer_questions()

    print(answers)
