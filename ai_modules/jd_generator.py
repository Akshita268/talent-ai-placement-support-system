# ai_modules/jd_generator.py
import re

def generate_jd(role, skills, eligibility):
    """
    Rule-based generator to produce structured Job Descriptions
    including Job Summary, Responsibilities, Requirements, Preferred Skills, and Qualifications.
    """
    role = role.strip() if role else "Software Engineer"
    skills_list = [s.strip() for s in skills.split(",") if s.strip()] if skills else []
    skills_formatted = ", ".join(skills_list) if skills_list else "core technical competencies"
    eligibility = eligibility.strip() if eligibility else "Bachelor's degree or equivalent experience"
    
    # Job Summary
    jd_summary = (
        f"We are seeking a talented and motivated {role} to join our growing engineering team. "
        f"In this role, you will be responsible for developing high-quality software solutions, "
        f"collaborating with cross-functional teams, and continuously improving our system architectures. "
        f"This position requires eligibility aligned with: {eligibility}."
    )
    
    # Responsibilities
    responsibilities = [
        f"Design, develop, and maintain clean, scalable, and efficient application services as a {role}.",
        "Collaborate with developers, testers, and product managers to map feature requirements into functional systems.",
        "Perform code reviews, write comprehensive tests, and adhere to structural development guidelines.",
        "Optimize system response metrics, resolve latency overheads, and maintain application stability.",
    ]
    # Add context-specific responsibilities
    skills_lower = [s.lower() for s in skills_list]
    if any(s in ["python", "flask", "django", "fastapi", "sql", "postgres", "node", "backend"] for s in skills_lower):
        responsibilities.append("Implement secure backend APIs, database normalization models, and query configurations.")
    if any(s in ["react", "react.js", "javascript", "html", "css", "vue", "angular", "frontend"] for s in skills_lower):
        responsibilities.append("Translate UI/UX wireframes into functional, interactive, and responsive frontend client elements.")
    if any(s in ["docker", "kubernetes", "aws", "gcp", "azure", "devops", "ci/cd"] for s in skills_lower):
        responsibilities.append("Manage containerized deployment configurations, automate CI/CD delivery pipelines, and monitor cloud resources.")
        
    # Requirements
    requirements = [
        f"Eligibility criteria met: {eligibility}.",
        "Strong understanding of object-oriented design patterns, data structure efficiency, and algorithm designs.",
        "Ability to troubleshoot complex run-time errors and perform debugging sessions.",
    ]
    for skill in skills_list[:4]:
        requirements.append(f"Practical knowledge and hands-on developer experience utilizing {skill.title()}.")
        
    # Preferred Skills
    preferred_skills = [
        "Familiarity with cloud hosting suites (such as AWS, GCP, or Azure) and orchestration strategies.",
        "Proficiency in Git version controls, pull request reviews, and repository staging configurations.",
        "Strong analytical logic, debug competence, and capability to adapt within agile sprints."
    ]
    
    # Qualifications
    qualifications = [
        "Bachelor's or Master's degree in Computer Science, Information Technology, Engineering, or a related field (or equivalent practical work experience).",
        "Clear communicative capabilities and capacity to collaborate smoothly in team environments."
    ]
    
    # Assemble the full description
    text = f"""### Job Summary
{jd_summary}

### Responsibilities
"""
    for r in responsibilities:
        text += f"- {r}\n"
        
    text += "\n### Requirements\n"
    for req in requirements:
        text += f"- {req}\n"
        
    text += "\n### Preferred Skills\n"
    for pref in preferred_skills:
        text += f"- {pref}\n"
        
    text += "\n### Qualifications\n"
    for qual in qualifications:
        text += f"- {qual}\n"
        
    return text.strip()


def improve_jd(text):
    """
    Polishes grammar, wording, and applies a recruiter-friendly structure.
    """
    if not text or not text.strip():
        return ""
        
    replacements = {
        r"\blooking for\b": "seeking a qualified",
        r"\bneed\b": "require competence in",
        r"\bgood at\b": "demonstrates proficiency in",
        r"\bbuild\b": "architect and implement",
        r"\bmake sure\b": "ensure optimal performance and reliability of",
        r"\bfix\b": "troubleshoot, debug, and resolve",
        r"\bdo\b": "execute",
        r"\bwork with\b": "collaborate with cross-functional teams and",
        r"\btrack\b": "monitor and evaluate",
        r"\bchange\b": "optimize",
        r"\bplus\b": "preferred qualifications include",
        r"\bnice to have\b": "preferred skills",
        r"\bhelp\b": "assist in",
        r"\buse\b": "utilize",
        r"\bjob description\b": "role profile",
        r"\bwant\b": "seek to onboard",
        r"\bcreate\b": "design and construct",
        r"\bwrite\b": "draft and maintain",
        r"\bcheck\b": "review and inspect",
        r"\brun\b": "operate and manage"
    }
    
    improved = text
    for pattern, repl in replacements.items():
        improved = re.sub(pattern, repl, improved, flags=re.IGNORECASE)
        
    return improved.strip()


def enhance_structure(text):
    """
    Groups paragraphs/lists under standard ### headings.
    """
    if not text or not text.strip():
        return ""
        
    has_summary = "job summary" in text.lower() or "summary" in text.lower()
    has_resp = "responsibilities" in text.lower() or "duties" in text.lower()
    has_req = "requirements" in text.lower() or "skills required" in text.lower() or "criteria" in text.lower()
    
    if has_summary and has_resp and has_req:
        return text.strip()
        
    lines = text.strip().split("\n")
    summary_lines = []
    responsibilities_lines = []
    requirements_lines = []
    
    for line in lines:
        line_clean = line.strip().lower()
        if not line_clean:
            continue
            
        if line_clean.startswith("#") or line_clean.endswith(":"):
            continue
            
        # Responsibilities detection
        is_resp = any(line_clean.startswith(v) or f" {v} " in line_clean for v in [
            "build", "develop", "design", "maintain", "collaborate", "test", "optimize", 
            "deploy", "support", "document", "troubleshoot", "monitor", "lead", "manage",
            "implement", "translate", "write", "perform", "ensure", "architect"
        ])
        
        # Requirements detection
        is_req = any(word in line_clean for word in [
            "experience", "years", "degree", "proficiency", "knowledge", "strong understanding",
            "skills", "familiarity", "background", "expert", "bachelor", "master", "phd"
        ])
        
        if is_resp and not is_req:
            clean_line = re.sub(r"^[\-\*\•\d\.\s]+", "", line.strip())
            responsibilities_lines.append(clean_line)
        elif is_req:
            clean_line = re.sub(r"^[\-\*\•\d\.\s]+", "", line.strip())
            requirements_lines.append(clean_line)
        else:
            summary_lines.append(line.strip())
            
    output = []
    if summary_lines:
        output.append("### Job Summary")
        output.append(" ".join(summary_lines))
        output.append("")
        
    if responsibilities_lines:
        output.append("### Responsibilities")
        for r in responsibilities_lines:
            output.append(f"- {r}")
        output.append("")
        
    if requirements_lines:
        output.append("### Requirements")
        for req in requirements_lines:
            output.append(f"- {req}")
        output.append("")
        
    if not responsibilities_lines and not requirements_lines:
        output = [
            "### Job Summary",
            text,
            "",
            "### Responsibilities",
            "- Collaborate with engineering teams to build key applications.",
            "- Adhere to project timelines and code standards.",
            "",
            "### Requirements",
            "- Experience with core technologies specified in the description.",
            "- Strong communication and team-working capabilities."
        ]
        
    return "\n".join(output).strip()


def make_professional(text):
    """
    Transforms informal terminology into recruiter-grade language.
    """
    if not text or not text.strip():
        return ""
        
    formal_replacements = {
        r"\bi want\b": "The organization seeks to align",
        r"\bwe want\b": "The engineering team seeks to onboard",
        r"\bwe need\b": "We require candidates to demonstrate",
        r"\byou will do\b": "The successful candidate will be tasked with",
        r"\byou'll do\b": "The successful candidate will be tasked with",
        r"\bhelp us\b": "contribute to the team's capacity to",
        r"\bcool\b": "innovative",
        r"\bgreat\b": "exceptional",
        r"\bstuff\b": "technical deliverables",
        r"\bthings\b": "domain solutions",
        r"\bsmart\b": "highly capable",
        r"\bquick\b": "efficient",
        r"\bdone\b": "successfully finalized",
        r"\bdeal with\b": "manage and navigate",
        r"\btalk to\b": "communicate and align with",
        r"\bget along\b": "collaborate effectively"
    }
    
    professional = text
    for pattern, repl in formal_replacements.items():
        professional = re.sub(pattern, repl, professional, flags=re.IGNORECASE)
        
    return improve_jd(professional)
