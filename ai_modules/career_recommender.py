import re
from ai_modules.resume_feedback import extract_pdf_text_local

ROLE_KEYWORDS = {
    "Backend Developer": ["python", "flask", "django", "fastapi", "backend", "databases", "mysql", "postgresql", "sqlite", "sql", "api", "rest", "docker", "aws", "node.js", "express.js", "restful api", "git", "github", "data structures", "algorithms"],
    "Data Analyst": ["sql", "excel", "tableau", "power bi", "data analysis", "pandas", "statistics", "visualization", "dashboard", "numpy", "sqlite", "databases", "postgresql", "mysql"],
    "ML Engineer": ["machine learning", "deep learning", "pytorch", "tensorflow", "pandas", "numpy", "scikit-learn", "model", "training", "cnn", "yolov8", "deep learning", "python", "algorithms"],
    "Frontend Developer": ["html", "css", "javascript", "react", "react.js", "tailwind", "bootstrap", "ui", "ux", "frontend", "git", "github"],
    "Full Stack Developer": ["python", "flask", "javascript", "react", "html", "css", "tailwind", "bootstrap", "databases", "sql", "api", "backend", "frontend", "git", "github"]
}

def recommend_career(resume_path=None, ats_history=None, hr_scores=None, technical_scores=None):
    """
    Recommends a career path based on Resume Text, ATS History, HR Interview Scores, and Technical Prep Scores.
    Returns:
        {
            "career_path": str,
            "rationale": str,
            "alignment_score": float,
            "all_scores": {role: score, ...}
        }
    """
    # 1. Parse Resume Text
    resume_text = ""
    if resume_path:
        resume_text = extract_pdf_text_local(resume_path)
    
    resume_text = (resume_text or "").lower()
    
    # 2. Base Scores from Resume Keywords
    resume_scores = {}
    for role, keywords in ROLE_KEYWORDS.items():
        score = 0
        if resume_text:
            for keyword in keywords:
                # Count matches
                matches = len(re.findall(r'\b' + re.escape(keyword) + r'\b', resume_text))
                score += matches * 5
        resume_scores[role] = min(score, 50)  # Max 50 points from resume keywords
        
    # 3. Add points from Application / ATS History (Max 20 points)
    application_boosts = {role: 0 for role in ROLE_KEYWORDS}
    if ats_history:
        for app in ats_history:
            job_role = app.get('job_role', '').lower()
            if 'backend' in job_role or 'python' in job_role or 'java' in job_role:
                application_boosts["Backend Developer"] += 5
                application_boosts["Full Stack Developer"] += 3
            elif 'data' in job_role or 'analyst' in job_role:
                application_boosts["Data Analyst"] += 5
            elif 'ml' in job_role or 'machine learning' in job_role or 'intelligence' in job_role:
                application_boosts["ML Engineer"] += 5
            elif 'frontend' in job_role or 'react' in job_role or 'web' in job_role:
                application_boosts["Frontend Developer"] += 5
                application_boosts["Full Stack Developer"] += 3
                
    for role in ROLE_KEYWORDS:
        resume_scores[role] += min(application_boosts[role], 20)
        
    # 4. Add points from Technical preparation (Max 30 points)
    tech_boosts = {role: 0 for role in ROLE_KEYWORDS}
    if technical_scores:
        for session in technical_scores:
            domain = session.get('domain', '').upper()
            score = session.get('score', 0)
            
            # Boost based on average performance in specific technical domains
            if domain == 'ML' and score > 50:
                tech_boosts["ML Engineer"] += (score / 100) * 30
            elif domain in ['DSA', 'OOP'] and score > 50:
                tech_boosts["Backend Developer"] += (score / 100) * 15
                tech_boosts["Full Stack Developer"] += (score / 100) * 15
            elif domain == 'DBMS' and score > 50:
                tech_boosts["Backend Developer"] += (score / 100) * 15
                tech_boosts["Data Analyst"] += (score / 100) * 20
            elif domain in ['CN', 'OS'] and score > 50:
                tech_boosts["Backend Developer"] += (score / 100) * 10
                
    for role in ROLE_KEYWORDS:
        resume_scores[role] += min(tech_boosts[role], 30)
        
    # Standardize/normalize final scores between 20 and 100
    final_scores = {}
    for role, score in resume_scores.items():
        # Minimum baseline of 30, scaled
        final_scores[role] = round(max(30, min(score + 30, 100)), 2)
        
    # Determine the best career path
    recommended_role = max(final_scores, key=final_scores.get)
    best_score = final_scores[recommended_role]
    
    # 5. Generate Rationale
    rationales = {
        "Backend Developer": f"Your profile shows a strong foundation in backend technologies, server logic, and algorithms. You have scored highly in technical topics and have a good keyword density for databases, APIs, and python libraries in your resume.",
        "Data Analyst": f"You show high compatibility with Data roles. Your profile indicates query skills, database familiarity (like SQL), and analytical thinking, supported by your database scores and relevant keywords.",
        "ML Engineer": f"Your background is strongly aligned with Artificial Intelligence and Machine Learning. Your resume includes deep learning, model keywords, and you have completed machine learning prep sessions.",
        "Frontend Developer": f"You demonstrate excellent frontend developer potential, with styling, framework, and design elements present in your projects. Your resume mentions key web tech (HTML/CSS/JS/React).",
        "Full Stack Developer": f"You exhibit a versatile skill set covering both backend server databases and frontend user interface technologies. Your resume shows strong coverage across both domains."
    }
    
    rationale = rationales[recommended_role]
    
    # If student has done HR prep, add positive feedback
    if hr_scores:
        avg_hr = sum(session.get('score', 0) for session in hr_scores) / len(hr_scores)
        if avg_hr >= 75:
            rationale += " Furthermore, your strong performance in HR interviews indicates excellent communication and leadership capabilities, vital for developer and team collaboration roles."

    return {
        "career_path": recommended_role,
        "rationale": rationale,
        "alignment_score": best_score,
        "all_scores": final_scores
    }
