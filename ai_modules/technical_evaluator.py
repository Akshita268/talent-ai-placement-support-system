# ai_modules/technical_evaluator.py
from ai_modules.embedding_engine import get_similarity_score
import re

def evaluate_technical_answer(correct_answer, student_answer):
    student = student_answer.strip().lower()
    correct = correct_answer.strip().lower()

    # 1. Embedding Similarity Score
    similarity = get_similarity_score(student, correct)
    # Scale to be a bit more lenient
    emb_score = min(100.0, similarity * 1.25)

    # 2. Keyword profiling
    # Extract significant technical terms from the correct answer
    words = re.findall(r'\b[a-z]{3,15}\b', correct)
    stop_terms = {"the", "and", "a", "an", "of", "to", "in", "is", "that", "it", "with", "for", "are", "on", "as", "by", "its", "from"}
    key_terms = list(set([w for w in words if w not in stop_terms]))

    matched_terms = []
    missing_terms = []
    for term in key_terms:
        if term in student:
            matched_terms.append(term)
        else:
            missing_terms.append(term)

    # Keyword match percentage
    kw_score = 0.0
    if key_terms:
        kw_score = (len(matched_terms) / len(key_terms)) * 100.0

    # Final scores
    final_score = round(0.60 * emb_score + 0.40 * kw_score, 2)

    # Build the single-paragraph Detailed Critique containing strengths, weaknesses, missing concepts, and suggestions.
    critique_parts = []
    if final_score >= 80:
        critique_parts.append("Excellent explanation! Your answer demonstrates a strong grasp of the technical concepts and aligns closely with standard definitions.")
    elif final_score >= 50:
        critique_parts.append("Your response shows a partial technical understanding, capturing some key elements but lacking complete depth and technical precision.")
    else:
        critique_parts.append("Your technical explanation needs improvement. There is a significant conceptual and semantic gap between your explanation and the expected standard definition.")

    if matched_terms:
        critique_parts.append(f"Your strengths include correctly referencing concepts like {', '.join(matched_terms[:3])}.")
    
    if missing_terms:
        critique_parts.append(f"However, the response was weakened by omitting key aspects such as {', '.join(missing_terms[:3])}.")
        critique_parts.append(f"To improve, you should review this topic and explicitly incorporate these missing concepts into your technical explanations.")
    else:
        critique_parts.append("You covered all the core concepts successfully. To stand out further, consider adding real-world context or design trade-offs in similar questions.")

    detailed_critique = " ".join(critique_parts)

    return {
        "score": final_score,
        "detailed_critique": detailed_critique
    }
