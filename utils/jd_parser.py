import re


# =========================
# SKILL DATABASE
# =========================

SKILLS = [

    "python",
    "java",
    "c",
    "c++",
    "sql",
    "mysql",
    "mongodb",
    "flask",
    "django",
    "react",
    "node.js",
    "html",
    "css",
    "javascript",
    "machine learning",
    "deep learning",
    "tensorflow",
    "pytorch",
    "data structures",
    "algorithms",
    "git",
    "github",
    "rest api"
]


# =========================
# EXTRACT SKILLS
# =========================

def extract_skills(text):

    text = text.lower()

    found_skills = []

    for skill in SKILLS:

        if skill.lower() in text:

            found_skills.append(skill)

    return list(set(found_skills))


# =========================
# EXTRACT ELIGIBILITY
# =========================

def extract_eligibility(text):

    text = text.lower()

    eligibility_keywords = [

        "b.tech",
        "btech",
        "m.tech",
        "mtech",
        "bca",
        "mca",
        "computer science",
        "information technology"
    ]

    found_eligibility = []

    for keyword in eligibility_keywords:

        if keyword in text:

            found_eligibility.append(keyword)

    return list(set(found_eligibility))


# =========================
# EXTRACT JOB ROLE
# =========================

def extract_job_role(text):

    text = text.lower()

    roles = [

        "python developer",
        "software engineer",
        "frontend developer",
        "backend developer",
        "full stack developer",
        "data analyst",
        "machine learning engineer",
        "web developer",
        "ai engineer"
    ]

    for role in roles:

        if role in text:

            return role.title()

    return "Role Not Detected"


# =========================
# CLEAN TEXT
# =========================

def clean_text(text):

    text = text.lower()

    text = text.replace("\n", " ")

    text = re.sub(r"\s+", " ", text)

    return text


# =========================
# MAIN PARSER FUNCTION
# =========================

def parse_job_description(raw_text):

    cleaned_text = clean_text(raw_text)

    skills = extract_skills(cleaned_text)

    eligibility = extract_eligibility(
        cleaned_text
    )

    job_role = extract_job_role(
        cleaned_text
    )

    parsed_data = {

        "job_role": job_role,

        "skills_required":
            ", ".join(skills),

        "eligibility":
            ", ".join(eligibility),

        "job_description":
            raw_text
    }

    return parsed_data