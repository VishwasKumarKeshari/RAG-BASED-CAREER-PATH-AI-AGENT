from typing import List

"""
Career knowledge base documents for RAG system.
"""

CAREER_DOCUMENTS = [
    """
    Career: Data Scientist
    Description: Analyzes complex datasets and builds machine learning models to drive business decisions.
    Required Skills: Python, SQL, Machine Learning, Statistics, Data Visualization (Tableau/Power BI)
    Educational Background: B.Tech in CSE/IT, B.Sc in Statistics or Mathematics
    Experience Level: Entry-level requires 0-2 years, Senior requires 5+ years
    Salary Range: ₹6-15 LPA (Entry), ₹20-40 LPA (Senior)
    Key Responsibilities: 
    - Collect and clean data from multiple sources
    - Build predictive and descriptive models
    - Present insights to stakeholders
    - Implement ML models in production
    Growth Opportunities: Lead to ML Engineering, Analytics Manager, or CTO roles
    Tools: Python, R, Spark, TensorFlow, Scikit-learn, Jupyter
    """,
    
    """
    Career: Machine Learning Engineer
    Description: Develops and deploys machine learning models at scale, focusing on production systems.
    Required Skills: Python, TensorFlow/PyTorch, ML Algorithms, System Design, Cloud Platforms (AWS/GCP/Azure)
    Educational Background: B.Tech in CSE/IT with strong ML background
    Experience Level: Requires 2+ years ML/Data Science experience
    Salary Range: ₹12-25 LPA (Mid), ₹30-60 LPA (Senior)
    Key Responsibilities:
    - Design scalable ML systems
    - Optimize model performance
    - Deploy models to production
    - Monitor model performance and retrain
    Growth Opportunities: ML Architect, AI Lead, Research Scientist
    Tools: Python, TensorFlow, PyTorch, Kubernetes, Docker, MLOps tools
    """,
    
    """
    Career: Web Developer
    Description: Creates responsive and interactive web applications using front-end and back-end technologies.
    Required Skills: HTML, CSS, JavaScript, React/Vue/Angular, Node.js/Django/Flask, Databases
    Educational Background: B.Tech in CSE/IT or Self-taught with portfolio
    Experience Level: Entry-level requires 0-2 years, Senior requires 5+ years
    Salary Range: ₹5-12 LPA (Entry), ₹18-35 LPA (Senior)
    Key Responsibilities:
    - Develop user interfaces
    - Build backend APIs
    - Integrate databases
    - Optimize performance
    Growth Opportunities: Full-Stack Architect, Tech Lead, CTO
    Tools: React, Node.js, Django, MongoDB, PostgreSQL, Docker
    """,
    
    """
    Career: DevOps Engineer
    Description: Manages infrastructure, deployment pipelines, and ensures smooth application operations.
    Required Skills: Linux, Docker, Kubernetes, CI/CD, AWS/Azure/GCP, Terraform, Jenkins
    Educational Background: B.Tech in CSE/IT with systems focus
    Experience Level: Requires 2+ years backend/infrastructure experience
    Salary Range: ₹10-20 LPA (Mid), ₹25-50 LPA (Senior)
    Key Responsibilities:
    - Design and maintain infrastructure
    - Implement CI/CD pipelines
    - Monitor system performance
    - Manage cloud resources
    - Ensure security and compliance
    Growth Opportunities: Infrastructure Architect, Site Reliability Engineer, Cloud Architect
    Tools: Docker, Kubernetes, Jenkins, GitLab CI, Terraform, Prometheus
    """,
    
    """
    Career: Cloud Engineer
    Description: Designs and manages cloud infrastructure solutions for scalable applications.
    Required Skills: AWS/Azure/GCP, Linux, Networking, Security, Infrastructure as Code, Docker
    Educational Background: B.Tech in CSE/IT with networking or systems knowledge
    Experience Level: Requires 2+ years infrastructure experience
    Salary Range: ₹12-22 LPA (Mid), ₹28-55 LPA (Senior)
    Key Responsibilities:
    - Design cloud architecture
    - Implement cloud solutions
    - Optimize cloud costs
    - Ensure security and disaster recovery
    Growth Opportunities: Solutions Architect, Cloud Architect, CTO
    Certifications: AWS Solutions Architect, Azure Administrator, GCP Associate
    Tools: AWS, Azure, GCP, Terraform, CloudFormation
    """,
    
    """
    Career: Mobile Developer
    Description: Develops native or cross-platform mobile applications for iOS and Android.
    Required Skills: Java/Kotlin (Android), Swift (iOS), React Native/Flutter, Mobile UI/UX
    Educational Background: B.Tech in CSE/IT with mobile development focus
    Experience Level: Entry-level requires 0-2 years
    Salary Range: ₹6-14 LPA (Entry), ₹18-40 LPA (Senior)
    Key Responsibilities:
    - Develop mobile apps
    - Optimize performance
    - Implement user interfaces
    - Debug and fix issues
    Growth Opportunities: Lead Mobile Developer, Mobile Architect, Tech Lead
    Tools: Android Studio, Xcode, React Native, Flutter, Firebase
    """,
    
    """
    Career: UI/UX Designer
    Description: Creates intuitive and visually appealing user interfaces and experiences for applications.
    Required Skills: Figma, Adobe XD, UI/UX Design Principles, Wireframing, User Research, Prototyping
    Educational Background: B.Des in Graphic/UI Design or self-taught with portfolio
    Experience Level: Entry-level requires 0-2 years
    Salary Range: ₹5-12 LPA (Entry), ₹15-30 LPA (Senior)
    Key Responsibilities:
    - Design user interfaces
    - Conduct user research
    - Create prototypes
    - Collaborate with developers
    Growth Opportunities: Design Lead, Product Manager, Design Director
    Tools: Figma, Adobe XD, Sketch, Protopie, Usability Testing
    """,
    
    """
    Career: Cybersecurity Analyst
    Description: Protects organizations from security threats through monitoring, analysis, and remediation.
    Required Skills: Network Security, SIEM Tools, Incident Response, Firewalls, Encryption, Linux
    Educational Background: B.Tech in CSE with security focus or B.Sc in IT Security
    Experience Level: Requires 2+ years IT/Network experience
    Salary Range: ₹10-18 LPA (Entry Security role), ₹25-50 LPA (Senior)
    Key Responsibilities:
    - Monitor security events
    - Analyze threats
    - Implement security measures
    - Conduct vulnerability assessments
    Growth Opportunities: Security Architect, Chief Information Security Officer, Ethical Hacker
    Certifications: CEH, CISSP, Security+
    Tools: Splunk, Wireshark, Metasploit, Burp Suite
    """,
    
    """
    Career: Business Analyst
    Description: Analyzes business requirements and translates them into technical solutions.
    Required Skills: SQL, Excel, Tableau, Business Analysis, Communication, Problem-solving
    Educational Background: B.Tech/B.Sc in any field, MBA beneficial
    Experience Level: Entry-level can start with 0 years
    Salary Range: ₹5-10 LPA (Entry), ₹15-30 LPA (Senior)
    Key Responsibilities:
    - Gather business requirements
    - Analyze data and trends
    - Create documentation
    - Communicate with stakeholders
    Growth Opportunities: Senior Analyst, Product Manager, Strategy Lead
    Tools: SQL, Tableau, Power BI, JIRA, Excel
    """,
    
    """
    Career: Database Administrator
    Description: Manages databases, ensures data security, and optimizes database performance.
    Required Skills: SQL, Database Design, Performance Tuning, Backup & Recovery, Security
    Educational Background: B.Tech in CSE/IT
    Experience Level: Requires 2+ years database experience
    Salary Range: ₹10-18 LPA (Mid), ₹25-45 LPA (Senior)
    Key Responsibilities:
    - Design and manage databases
    - Perform backups and recovery
    - Optimize performance
    - Ensure data security
    Growth Opportunities: Database Architect, Infrastructure Manager
    Databases: Oracle, SQL Server, PostgreSQL, MySQL, MongoDB
    """
]


def get_career_documents() -> List[str]:
    """Return all career documents for RAG knowledge base."""
    return CAREER_DOCUMENTS
