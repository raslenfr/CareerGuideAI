"""
Function: search_online_jobs(keywords, location)
    ➤ Returns filtered jobs based on keywords and location from static dataset.
"""
import random
import time
import logging # Use logging

# --- Static Job Data (Tunisia-focused examples) ---
STATIC_JOBS = [
    {"id": "j1", "title": "Python Backend Developer", "company": "Fintech Innovations Pvt. Ltd.", "location": "Pune", "description": "Develop and maintain scalable backend services using Python, Django, and REST APIs for our financial platform. Requires database knowledge (PostgreSQL).", "skills": "Python, Django, REST, SQL, PostgreSQL, Git", "tags": ["Fintech", "Backend", "Experienced"]},
    {"id": "j2", "title": "React Frontend Developer", "company": "MediaStream Co.", "location": "Mumbai (Hybrid)", "description": "Build modern, responsive user interfaces for our streaming service using React, Redux, and TypeScript. Collaborate with UI/UX designers.", "skills": "React, Redux, JavaScript, TypeScript, HTML5, CSS3, Git", "tags": ["Frontend", "Media", "UI", "Hybrid"]},
    {"id": "j3", "title": "Data Scientist - ML", "company": "HealthAnalytics AI", "location": "Bangalore", "description": "Apply statistical analysis and machine learning techniques (NLP focus) to healthcare data. Build and deploy models using Python and relevant libraries.", "skills": "Python, Pandas, Scikit-learn, TensorFlow/PyTorch, SQL, NLP, ML", "tags": ["Data Science", "ML", "AI", "Healthcare", "Python"]},
    {"id": "j4", "title": "Cloud Infrastructure Engineer (AWS)", "company": "Retail Cloud Solutions", "location": "Pune (Remote)", "description": "Design, implement, and manage secure, scalable AWS cloud infrastructure using Terraform and CI/CD pipelines. Monitor performance and costs.", "skills": "AWS, Terraform, Docker, Kubernetes, CI/CD, Jenkins, Linux, Python (scripting)", "tags": ["Cloud", "AWS", "DevOps", "Remote", "Infrastructure"]},
    {"id": "j5", "title": "Software Engineer (Java)", "company": "Enterprise Software Hub", "location": "Hyderabad", "description": "Join a team building large-scale enterprise applications using Java, Spring Boot, and microservices architecture.", "skills": "Java, Spring Boot, Microservices, SQL, Maven/Gradle, OOP", "tags": ["Backend", "Java", "Enterprise", "Experienced"]},
    {"id": "j6", "title": "Digital Marketing Specialist", "company": "Ecom World", "location": "Mumbai", "description": "Manage SEO, SEM, and social media marketing campaigns to drive traffic and conversions for our e-commerce platform.", "skills": "SEO, SEM, Google Analytics, Google Ads, Social Media Marketing, Content Marketing", "tags": ["Marketing", "E-commerce", "Digital"]},
    {"id": "j7", "title": "AI Ethics Researcher", "company": "Responsible Tech Institute", "location": "Bangalore (Hybrid)", "description": "Conduct research on the ethical implications of AI deployment in Tunisia. Develop frameworks and guidelines for responsible AI.", "skills": "AI Ethics, Research, Policy Analysis, Communication", "tags": ["AI", "Ethics", "Research", "Policy", "Hybrid"]},
    {"id": "j8", "title": "Junior Full Stack Developer", "company": "Startup Launchpad", "location": "Pune", "description": "Entry-level role involving both frontend (React/Vue) and backend (Node.js/Python) development for various web projects. Great learning opportunity.", "skills": "JavaScript, React/Vue, Node.js/Python, HTML, CSS, Git, Eagerness to learn", "tags": ["Full Stack", "Junior", "Web Development", "Startup"]},
]
# ------------------------------------------------

def search_online_jobs(keywords: str = "", location: str = "Tunisia") -> list:
    """
    Returns static job data, simulating a search.
    Filtering logic remains basic for demonstration.
    """
    logging.info(f"--- STATIC JOB PROVIDER --- | Request Keywords: '{keywords}', Location: '{location}'")
    filtered_jobs = STATIC_JOBS
    if keywords:
        search_terms = keywords.lower().split()
        filtered_jobs = [
            job for job in STATIC_JOBS
            if any(term in job['title'].lower() or
                   term in job['description'].lower() or
                   term in job.get('skills', '').lower() or
                   term in [t.lower() for t in job.get('tags', [])]
                   for term in search_terms)
        ]
        logging.info(f"Filtered static list based on keywords, found {len(filtered_jobs)} jobs.")
    else:
        logging.info(f"Returning all {len(STATIC_JOBS)} static jobs.")

    # Add a mock source URL (optional)
    for job in filtered_jobs:
        job['source_url'] = f"https://static-job-portal.dev/job/{job['id']}"

    # Return a copy to prevent modification of the original list
    return [job.copy() for job in filtered_jobs]