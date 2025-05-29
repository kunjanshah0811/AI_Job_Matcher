from model import generate_response
from test import resume,jd,jr

def generate_question(resume_text, job_desc_text, job_role):
    system_prompt = f"""
    You are an interview coach.Based on this resume and job description, 
    generate exactly 5 interview questions for the role "{job_role}".

    Resume:
    {resume_text}

    Job Description:
    {job_desc_text}

    Generate 5 relevant interview questions. Include follow-up prompts in parentheses if needed.
    You must respond with ONLY a valid JSON array of strings. No explanations, no markdown, just the JSON array.

    Example format: ["Question 1 here", "Question 2 here", "Question 3 here", "Question 4 here", "Question 5 here"]
    """

    user_prompt="""You are a JSON generator. You only respond with valid JSON arrays. 
                    Never include explanations or markdown formatting.
                """
    
    questions = generate_response(system_prompt,user_prompt)
    return questions

if __name__=="__main":

    resume = """
    TAYLOR MORGAN
    Email: taylor.morgan@email.com | Phone: (555) 987-6543
    Address: Seattle, WA 98101 | LinkedIn: linkedin.com/in/taylormorgan
    GitHub: github.com/tmorgan

    PROFESSIONAL SUMMARY
    Software Developer with 3 years of experience building web applications using React and Node.js. Strong knowledge of JavaScript, HTML/CSS, and database design. Passionate about creating intuitive user experiences and writing clean, maintainable code.

    EDUCATION
    BACHELOR OF SCIENCE IN COMPUTER SCIENCE
    University of Washington
    2018 - 2022

    TECHNICAL SKILLS
    • Front-end: React, JavaScript, HTML5, CSS3, TypeScript
    • Back-end: Node.js, Express, Python
    • Database: MongoDB, PostgreSQL, MySQL
    • Tools: Git, Docker, AWS, Jest

    EXPERIENCE
    JUNIOR SOFTWARE DEVELOPER
    TechSolutions Inc. | Seattle, WA
    2022 - Present
    • Developed and maintained React components for customer-facing web applications
    • Collaborated with design team to implement responsive UI features
    • Reduced page load time by 30% through code optimization
    • Participated in code reviews and contributed to team documentation

    PROJECTS
    ECOMMERCE PLATFORM
    • Built a full-stack ecommerce site using React, Node.js and MongoDB
    • Implemented secure payment processing with Stripe API
    • Created admin dashboard for product and inventory management
    """
    jd= """
        COMPANY: DataViz Technologies
        LOCATION: Remote (US-based)
        POSITION: Front-End Developer

        ABOUT US:
        DataViz Technologies specializes in data visualization tools and analytics dashboards for business intelligence. Our products help companies make sense of complex data through intuitive visual interfaces.

        JOB DESCRIPTION:
        We're looking for a talented Front-End Developer to join our growing product team. You'll be responsible for building and optimizing user interfaces that make complex data accessible and actionable.

        RESPONSIBILITIES:
        • Develop new user-facing features using React.js
        • Build reusable components and libraries for future use
        • Translate designs and wireframes into high-quality code
        • Optimize components for maximum performance across devices
        • Collaborate with back-end developers to integrate UI with API services

        REQUIREMENTS:
        • 2+ years experience with React.js and modern JavaScript (ES6+)
        • Strong proficiency in HTML5, CSS3, and responsive design
        • Experience with state management (Redux, Context API)
        • Understanding of REST APIs and asynchronous request handling
        • Knowledge of browser testing and debugging
        • Familiarity with code versioning tools (Git)
        • Experience with data visualization libraries (D3.js, Chart.js) is a plus

        WHAT WE OFFER:
        • Competitive salary and benefits
        • Flexible remote work policy
        • Professional development budget
        • Collaborative, innovative team environment
        """

    jr="Front-End Developer"
    questions=generate_question(resume,jd,jr)
    print(questions)
