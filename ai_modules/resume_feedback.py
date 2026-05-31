# ai_modules/resume_feedback.py
import re
import pdfplumber

def extract_pdf_text_local(pdf_path):
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

def generate_resume_feedback(
        ats_score,
        matched_skills,
        missing_skills,
        resume_path=None
):
    """
    Generate ATS strengths, weaknesses, suggestions,
    and recruiter match prediction.
    """

    strengths = []
    weaknesses = []
    suggestions = []

    # =========================
    # STRENGTHS
    # =========================
    if ats_score >= 80:
        strengths.append("Strong alignment with job requirements.")
        strengths.append("Relevant technical skills detected.")
        strengths.append("Resume is likely to pass initial ATS screening.")
    elif ats_score >= 60:
        strengths.append("Good match with job description.")
        strengths.append("Several required skills are present.")
    else:
        strengths.append("Basic technical foundation detected.")

    # =========================
    # RESUME QUALITY ANALYSIS (AI-driven heuristics)
    # =========================
    resume_text = None
    if resume_path:
        resume_text = extract_pdf_text_local(resume_path)

    if resume_text:
        text_lower = resume_text.lower()
        
        # 1. Missing measurable achievements
        # Look for numbers with % or +, or metric words
        metrics_found = re.findall(r'\b\d+(?:%|\s*percent|\s*\+|k|m|b)\b', text_lower)
        impact_words = ["reduced", "increased", "optimized", "improved", "saved", "scaled", "revenue"]
        has_impact = any(word in text_lower for word in impact_words)
        
        if len(metrics_found) < 2 and not has_impact:
            weaknesses.append("Missing measurable achievements: The resume lacks quantified impact metrics.")
            suggestions.append("Quantify your project results. Use percentages, time savings, or scale (e.g., 'improved page load times by 40%', 'reduced query execution time from 5s to 0.2s').")
        else:
            strengths.append("Includes measurable metrics and achievements.")
            
        # 2. Missing technical depth
        depth_words = ["architecture", "scaling", "docker", "kubernetes", "aws", "gcp", "ci/cd", "microservices", "redis", "kafka", "graphql", "rest api", "nosql", "postgres", "design patterns"]
        depth_score = sum(1 for word in depth_words if word in text_lower)
        if depth_score < 3:
            weaknesses.append("Missing technical depth: Project explanations are high-level and lack architectural details.")
            suggestions.append("Add technical details on architectures, databases, and DevOps tools. Explain why you chose specific libraries or patterns.")
        else:
            strengths.append("Demonstrates good technical and architectural depth.")
            
        # 3. Weak project descriptions
        action_verbs = ["architected", "implemented", "developed", "engineered", "designed", "optimized", "built", "spearheaded", "automated"]
        verb_count = sum(1 for verb in action_verbs if verb in text_lower)
        if verb_count < 3 or len(text_lower.split()) < 100:
            weaknesses.append("Weak project descriptions: Descriptions are brief or do not start with strong action verbs.")
            suggestions.append("Use the STAR (Situation, Task, Action, Result) method for project bullets. Start each bullet point with a strong action verb.")
        else:
            strengths.append("Uses strong action verbs in project descriptions.")

    # =========================
    # MISSING SKILL ANALYSIS
    # =========================
    if missing_skills:
        suggestions.append(
            "Add or highlight the following skills: "
            + ", ".join(missing_skills)
        )

    # =========================
    # ATS SCORE BASED FEEDBACK
    # =========================
    if ats_score < 40:
        suggestions.append("Resume has low alignment with the job description.")
        suggestions.append("Consider updating projects and skills relevant to the role.")
    elif ats_score < 60:
        suggestions.append("Add more role-specific skills and project experience.")
        suggestions.append("Use keywords from the job description where appropriate.")
    elif ats_score < 80:
        suggestions.append("Resume is competitive but can be improved further.")
        suggestions.append("Add measurable achievements in projects and internships.")
    else:
        suggestions.append("Resume is well aligned with the job requirements.")
        suggestions.append("Consider adding quantified achievements to strengthen impact.")

    # =========================
    # PROJECT SUGGESTIONS
    # =========================
    if len(matched_skills) < 3:
        suggestions.append("Include more relevant technical projects.")
    else:
        strengths.append("Good coverage of required technical skills.")

    # =========================
    # RECRUITER MATCH PREDICTION
    # =========================
    if ats_score >= 85:
        prediction = "Excellent Match"
    elif ats_score >= 70:
        prediction = "Strong Match"
    elif ats_score >= 50:
        prediction = "Moderate Match"
    else:
        prediction = "Low Match"

    return {
        "strengths": strengths,
        "weaknesses": weaknesses,
        "suggestions": suggestions,
        "prediction": prediction
    }
