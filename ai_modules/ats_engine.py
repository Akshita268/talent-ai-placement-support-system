import pdfplumber
import re
import nltk

from nltk.corpus import stopwords

from ai_modules.embedding_engine import (
get_similarity_score
)

# Download stopwords

nltk.download('stopwords')

# =========================

# SKILLS DATABASE

# =========================

skills_database = [

# Programming Languages
'python',
'java',
'javascript',
'c',
'c++',
'c#',

# Backend
'flask',
'fastapi',
'django',
'node.js',
'express.js',
'rest api',
'restful api',

# Frontend
'react',
'react.js',
'html',
'css',
'tailwind',

# Databases
'mongodb',
'mysql',
'postgresql',
'sqlite',
'sql',

# AI / ML
'machine learning',
'deep learning',
'pytorch',
'tensorflow',
'cnn',
'yolov8',

# Tools
'git',
'github',
'docker',
'google colab',
'vscode',

# Core Concepts
'data structures',
'algorithms',
'operating systems',
'computer networks'

]

# =========================

# PROJECT KEYWORDS

# =========================

project_keywords = [

'project',
'api',
'backend',
'database',
'model',
'detection',
'authentication',
'deployment',
'inference',
'cnn',
'yolov8'

]

# =========================

# STOPWORDS

# =========================

stop_words = set(stopwords.words('english'))

# =========================

# CLEAN TEXT

# =========================

def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z0-9+#.]', ' ', text)
    words = text.split()
    filtered_words = [word for word in words if word not in stop_words]
    return ' '.join(filtered_words)

# =========================

# EXTRACT PDF TEXT

# =========================

def extract_pdf_text(pdf_path):
    try:
        text = ""
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text
    except Exception:
        return None

# =========================

# EXTRACT SKILLS

# =========================

def extract_skills(text):
    found_skills = []
    text = text.lower()
    for skill in skills_database:
        if skill.lower() in text:
            found_skills.append(skill)
    return list(set(found_skills))

# =========================

# PROJECT SCORE

# =========================

def calculate_project_score(clean_resume):
    matched_project_keywords = []
    for keyword in project_keywords:
        if keyword in clean_resume:
            matched_project_keywords.append(keyword)
    project_score = len(set(matched_project_keywords)) * 3
    project_score = min(project_score, 20)
    return project_score

# =========================

# ATS ENGINE

# =========================

def calculate_ats_score(resume_pdf_path, job_description):
    resume_text = extract_pdf_text(resume_pdf_path)
    if resume_text is None:
        return {
            "ats_score": 0,
            "embedding_score": 0,
            "skill_match_score": 0,
            "project_score": 0,
            "matched_skills": [],
            "missing_skills": [],
            "resume_skills": [],
            "jd_skills": [],
            "feedback": "Invalid Resume File"
        }

    clean_resume = clean_text(resume_text)
    clean_jd = clean_text(job_description)

    # EMBEDDING SIMILARITY
    embedding_score = get_similarity_score(clean_resume, clean_jd)

    # SKILLS
    resume_skills = extract_skills(clean_resume)
    jd_skills = extract_skills(clean_jd)

    matched_skills = set(resume_skills).intersection(set(jd_skills))
    missing_skills = set(jd_skills) - set(resume_skills)

    # SKILL MATCH SCORE
    if len(jd_skills) > 0:
        skill_match_score = (len(matched_skills) / len(jd_skills)) * 100
    else:
        skill_match_score = 0

    # PROJECT SCORE
    project_score = calculate_project_score(clean_resume)

    # FINAL ATS SCORE
    final_ats_score = 0.40 * skill_match_score + 0.40 * embedding_score + project_score
    final_ats_score = min(final_ats_score, 100)

    # FEEDBACK
    if final_ats_score >= 80:
        feedback = "Excellent Resume Match"
    elif final_ats_score >= 60:
        feedback = "Good Resume Match"
    elif final_ats_score >= 40:
        feedback = "Average Resume Match"
    else:
        feedback = "Low Resume Match"

    return {
        "ats_score": round(final_ats_score, 2),
        "embedding_score": round(embedding_score, 2),
        "skill_match_score": round(skill_match_score, 2),
        "project_score": project_score,
        "matched_skills": list(matched_skills),
        "missing_skills": list(missing_skills),
        "resume_skills": resume_skills,
        "jd_skills": jd_skills,
        "feedback": feedback
    }
    resume_pdf_path
