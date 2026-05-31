# ai_modules/hr_question_generator.py

def generate_hr_questions(role, experience):
    """
    Dynamically generates a list of 5 role-specific HR questions based on the role and experience.
    """
    role = role.strip() if role else "Software Engineer"
    
    questions = [
        f"Tell me about yourself and your journey to becoming a {role}.",
        f"Why should we hire you for this {role} position? What makes you a good fit?",
        f"Explain a technical challenge or bug you faced in a project related to {role} and how you solved it.",
        f"Describe a leadership experience or a time when you took ownership of a task or team project.",
        f"Where do you see yourself in 5 years in the field of {role}?"
    ]
    return questions
