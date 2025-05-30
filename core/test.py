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

scores = [[4, 3, 5, 4], [3, 4, 4, 3], [5, 4, 4, 5], [3, 4, 4, 3], [5, 4, 4, 5]],

questions= [
    "Tell me about your experience with software development and how it prepares you for this role.",
    "Describe a challenging project you worked on and how you approached problem-solving during its development.",
    "How do you stay current with emerging technologies and programming languages in the fast-paced tech industry?",
    "Can you share your experience working in Agile development environments and how you collaborate with cross-functional teams?",
    "What experience do you have with cloud services, and how have you implemented them in your previous projects?"],

ai_answers=["In my three years as a front-end developer, I've specialized in React.js for data visualization interfaces. At TechSolutions, I developed interactive UIs that display complex data sets, directly relevant to DataViz's needs. I've implemented responsive designs while optimizing performance, reducing page load times by 30%. I'm proficient with Redux and Context API as mentioned in your requirements. I've built reusable component libraries that create scalable architecture, essential for visualization dashboards.",
            "I led development of a real-time financial analytics dashboard handling multiple data sources with sub-second updates. Performance was the key challenge with large datasets causing frequent DOM updates. I created benchmarks to identify bottlenecks, then implemented React.memo and useMemo hooks to prevent unnecessary re-renders. I designed a custom caching layer for efficient updates and collaborated with back-end engineers on data pagination when memory issues arose. The result was a dashboard handling 50+ concurrent streams while maintaining 60fps.",
            "I dedicate 5 weekly hours to structured learning on platforms like Frontend Masters, currently completing an advanced D3.js course relevant to DataViz. I contribute to open-source visualization projects to learn cutting-edge techniques. I maintain a technology trends database in Notion to prioritize learning investments. I follow TC39 proposals to understand JavaScript's future direction and attend ReactConf annually. This systematic approach ensures I develop expertise in technologies with real business value.",
            "I've worked extensively with both Scrum and Kanban methodologies. As the front-end representative in our cross-functional squad, I implemented automated Figma-to-component pipelines that reduced design implementation time by 40%. With back-end teams, I introduced typed API contracts using OpenAPI specifications, reducing integration issues by 60%. I established a "tech debt hour" during sprint planning and created interactive prototypes for data visualization projects before full implementation to test different approaches.",
            "I've implemented AWS and GCP solutions across multiple projects. At TechSolutions, I architected a front-end pipeline using AWS Amplify enabling feature-branch previews and automated A/B testing. I implemented multi-region CloudFront with S3 origin reducing global load times by 40%. I designed serverless architecture using Lambda and API Gateway for data microservices, and leveraged Firebase for real-time synchronization. I've worked with BigQuery for large dataset processing and recently experimented with AWS ECS for container-based deployment."],

user_answers=[
    "I've been a Junior Software Developer at TechSolutions for three years, working with React and Node.js. I've built several customer-facing components and worked on responsive UI features. My experience includes JavaScript, HTML5, and CSS3 - all requirements for this position. My proudest project is an ecommerce platform where I built the entire front-end in React, handling state management and API integration. My background provides a solid foundation in the technologies you're using.",
    "My most challenging project was building an ecommerce platform with React, Node.js, and MongoDB. Implementing secure payment processing with Stripe API presented the biggest challenge. I researched best practices first and created a detailed implementation plan. When payment confirmations weren't syncing with our database, I set up a logging system to track transaction flow and identify breakpoints. After consulting with senior developers, we implemented a queue-based retry system for failed confirmations.",
    "I stay current by following JavaScript Weekly and React Status newsletters, and monitoring trending GitHub repositories. I dedicate time twice monthly to work through tutorials on relevant libraries - currently focusing on TypeScript which is gaining popularity in React projects. I attend local Seattle React meetups when possible and find side projects are the best way to gain hands-on experience with new technologies without production pressure.",
    "At TechSolutions, we use modified Agile with two-week sprints including daily standups, planning, reviews, and retrospectives. Standups help identify blockers early. When working with designers, I provide early feedback on technical feasibility rather than waiting until designs are finalized. With back-end developers, I participate in API discussions from the beginning to ensure endpoints work efficiently for front-end needs. I document decisions in our project management tools and keep tickets updated.",
    "I've used AWS at TechSolutions and in personal projects. For our ecommerce platform, I configured S3 buckets for product images and wrote code for image uploads and optimizations. We used CloudFront as a CDN for faster global delivery and AWS CodePipeline for CI/CD. In personal projects, I've worked with AWS Lambda for serverless functions handling image processing and API integrations. While not an AWS expert, I'm comfortable with core services and can quickly learn new ones as needed."]

if __name__ == "__main__":
    print("Test data loaded")