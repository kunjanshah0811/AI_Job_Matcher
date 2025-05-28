from model import generate_response

class Answering_competitor:
    def __init__(self,resume,job_description,difficulty_level):
        self.resume = resume
        self.job_description = job_description
        self.difficulty_level = int(difficulty_level)
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
        factors = generate_response(system_prompt,user_prompt)
        return factors

    def generate_persona(self):
        if self.persona is not None :
            return self.persona
        
        system_prompt = """
                    You are a professional resume enhancement agent. You are given:
                    1. A current resume.
                    2. A list of key factors (skills or experiences).
                    3. A difficulty level from 10 to 100.

                    Your task is to improve the resume by **only enhancing sentences that include the specified factors**, based on the difficulty level. 

                    Rules:
                    - You can add new tools, technologies, or frameworks that are not present in the original sentence.
                    - You MUST NOT add new bullet points or sections.
                    - You MUST preserve the overall structure of the resume.
                    - You MAY rewrite sentences to improve clarity, technical strength, or phrasing in proportion to the difficulty level.
                    - Sentences unrelated to the factor list should remain unchanged.

                    At difficulty 10, make very light improvements.  
                    At difficulty 100, make sentences as strong, impactful, and technically advanced as possible **using only the existing information**.

                    Return the new resume in the same structure.
                """
        
        user_prompt = f"""
                Enhance the following resume by only improving the parts that involve the specified factors. The difficulty level determines how much the improvements scale, from minimal (10) to highly advanced (100). Do not add any new technologies, bullet points, or content not originally present.
                Difficulty Level: {self.difficulty_level}
                Factors to focus on: {self.factors}
                Current Resume:{self.resume}"""

        competitor_resume = generate_response(system_prompt, user_prompt)
        return competitor_resume
        
    def answer_questions(self):
        pass

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

    obj=Answering_competitor(resume,jd,20)  
    factors=obj.extract_factors()  
    competitor_resume=obj.generate_persona()

    print(factors)
    print(competitor_resume)
