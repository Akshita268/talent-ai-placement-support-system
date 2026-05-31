# ai_modules/hr_answer_evaluator.py
import re
from ai_modules.embedding_engine import get_similarity_score

EXPECTED_ANSWERS = {
    "yourself": "I am a motivated developer with strong technical skills. I have worked on projects, solved technical challenges, and continuously seek to learn and grow in my career.",
    "hire_you": "You should hire me because I have the required technical skills, practical experience from projects, a strong work ethic, and the ability to collaborate effectively in a team.",
    "challenge": "I faced a challenge where a system failed or a bug occurred. I analyzed the root cause, researched solutions, collaborated with others, and successfully fixed it, improving system performance.",
    "leadership": "I demonstrated leadership by taking ownership of a critical project task, organizing the team, resolving communication gaps, and ensuring the project was delivered successfully.",
    "five_years": "In 5 years, I plan to be in a senior technical role, leading key features, mentoring junior developers, and contributing to the technical and architectural roadmap of the company."
}

IMPROVED_EXAMPLES = {
    "yourself": "An improved response would be: 'I am a passionate software engineer specializing in modern web technologies. I have built several projects using Flask and React, focusing on clean architecture. I have a strong foundation in data structures and databases, and I am excited to apply my skills to build robust software solutions in a collaborative team.'",
    "hire_you": "An improved response would be: 'You should hire me because I offer a blend of technical capability and collaborative mindset. I have hands-on experience designing REST APIs and working with databases. I am highly adaptable, eager to learn your stack, and have demonstrated ability to solve problems under tight deadlines.'",
    "challenge": "An improved response would be: 'A notable challenge I faced was optimizing database query latency in a project. The application was slow because of inefficient joins. I analyzed the query execution plans, added indexes, and refactored the SQL queries, which reduced response time by 60%.'",
    "leadership": "An improved response would be: 'During a university hackathon, our backend developer was stuck. I took the lead, set up a pair programming session to debug their module, and re-allocated tasks to keep us on track. We finished the project on time and won the runner-up prize.'",
    "five_years": "An improved response would be: 'In 5 years, I aim to grow into a Senior Engineer. I want to deepen my expertise in system design and cloud deployments, take on ownership of core services, and mentor junior developers while contributing to the team's engineering standards.'"
}

def evaluate_answer(question, answer):
    cleaned = answer.strip()
    words = cleaned.split()
    word_count = len(words)

    # 1. Identify question category
    q_lower = question.lower()
    category = "yourself"
    if "hire" in q_lower or "fit" in q_lower:
        category = "hire_you"
    elif "challenge" in q_lower or "bug" in q_lower:
        category = "challenge"
    elif "leadership" in q_lower or "ownership" in q_lower or "team" in q_lower:
        category = "leadership"
    elif "5 years" in q_lower or "five years" in q_lower:
        category = "five_years"

    expected_ans = EXPECTED_ANSWERS[category]
    improved_ans = IMPROVED_EXAMPLES[category]

    # 2. Embedding Score (Semantic Similarity)
    similarity_score = get_similarity_score(cleaned, expected_ans)
    # Scale similarity score to be a bit more generous for natural answers
    embedding_score = min(100.0, similarity_score * 1.3)

    # 3. Communication Score
    # Deduct for filler words, reward for length and structure
    filler_words = ["umm", "aaa", "don't know", "nothing", "like", "basically", "actually"]
    filler_count = sum(1 for filler in filler_words if re.search(r'\b' + re.escape(filler) + r'\b', cleaned.lower()))
    
    comm_score = 100
    if word_count < 15:
        comm_score -= 40
    elif word_count < 30:
        comm_score -= 20
        
    comm_score -= filler_count * 10
    comm_score = max(0, min(100, comm_score))

    # 4. Confidence Score
    # Reward active verbs and confident terms
    confidence_keywords = ["achieved", "managed", "designed", "built", "implemented", "solved", "optimized", "spearheaded", "confident", "passion", "skills"]
    conf_matches = sum(1 for word in confidence_keywords if word in cleaned.lower())
    conf_score = min(100, 40 + conf_matches * 15)
    if word_count < 10:
        conf_score = 30

    # 5. Leadership Score
    leadership_keywords = ["team", "led", "leadership", "coordinate", "collaboration", "guidance", "ownership", "helped", "we", "group"]
    lead_matches = sum(1 for word in leadership_keywords if word in cleaned.lower())
    lead_score = min(100, 30 + lead_matches * 15)

    # 6. Problem Solving Score
    problem_keywords = ["solved", "fixed", "analyzed", "challenge", "bug", "resolved", "issue", "debugged", "figured", "because", "result"]
    prob_matches = sum(1 for word in problem_keywords if word in cleaned.lower())
    prob_score = min(100, 30 + prob_matches * 15)

    # Calculate overall average score
    overall_score = round((embedding_score * 0.40 + comm_score * 0.20 + conf_score * 0.15 + lead_score * 0.10 + prob_score * 0.15), 2)

    # Generate feedback
    feedback_details = []
    if overall_score >= 80:
        feedback_details.append("Excellent response. Your answer aligns very well with the expected candidate profile.")
    elif overall_score >= 60:
        feedback_details.append("Good response. You cover the key points, but could expand more on specifics.")
    else:
        feedback_details.append("Needs improvement. The response is either too brief or lacks structural alignment with the question.")

    if filler_count > 1:
        feedback_details.append("Try to reduce filler words (e.g. 'umm', 'like') to improve professionalism.")
    if word_count < 25:
        feedback_details.append("Provide a more detailed explanation (aim for 30-50 words) to strengthen your points.")

    return {
        "score": overall_score,
        "communication_score": comm_score,
        "confidence_score": conf_score,
        "leadership_score": lead_score,
        "problem_solving_score": prob_score,
        "feedback": " ".join(feedback_details),
        "improved_answer": improved_ans
    }
