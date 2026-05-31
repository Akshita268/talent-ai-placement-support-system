from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash
)

from models.models import (
    db,
    TechnicalInterviewSession,
    TechnicalInterviewAnswer
)

from ai_modules.technical_question_generator import generate_technical_questions
from ai_modules.technical_evaluator import evaluate_technical_answer

technical_bp = Blueprint(
    'technical_interview',
    __name__
)

@technical_bp.route('/technical_interview')
def technical_interview_dashboard():
    if 'student_id' not in session:
        flash('Please login first.')
        return redirect(url_for('student.student_login'))
    return render_template('technical_interview_dashboard.html')

@technical_bp.route('/start_technical_interview', methods=['POST'])
def start_technical_interview():
    if 'student_id' not in session:
        return redirect(url_for('student.student_login'))

    role = request.form['target_role']
    difficulty = request.form['difficulty']
    student_id = session.get('student_id')

    new_session = TechnicalInterviewSession(
        student_id=student_id,
        domain=role,
        difficulty=difficulty
    )
    db.session.add(new_session)
    db.session.commit()

    # Generate 5 questions based on role
    questions_list = generate_technical_questions(role, difficulty)
    
    session['tech_interview_session_id'] = new_session.id
    session['tech_questions'] = questions_list
    session['tech_current_question_index'] = 0

    return redirect(url_for('technical_interview.show_technical_question'))

@technical_bp.route('/technical_question')
def show_technical_question():
    questions = session.get('tech_questions')
    if not questions:
        return redirect(url_for('technical_interview.technical_interview_dashboard'))

    index = session.get('tech_current_question_index', 0)
    if index >= len(questions):
        return redirect(url_for('technical_interview.technical_interview_summary'))

    q_data = questions[index]
    return render_template(
        'take_technical_question.html',
        question=q_data['question'],
        question_number=index + 1
    )

@technical_bp.route('/submit_technical_answer', methods=['POST'])
def submit_technical_answer():
    answer = request.form['answer']
    questions = session.get('tech_questions')
    index = session.get('tech_current_question_index', 0)
    
    current_q_data = questions[index]
    
    result = evaluate_technical_answer(
        current_q_data['answer'],
        answer
    )

    tech_answer = TechnicalInterviewAnswer(
        session_id=session['tech_interview_session_id'],
        question=current_q_data['question'],
        correct_answer=current_q_data['answer'],
        student_answer=answer,
        score=result['score'],
        feedback=result['detailed_critique']
    )
    db.session.add(tech_answer)
    db.session.commit()

    session['tech_current_question_index'] += 1

    return render_template(
        'technical_interview_feedback.html',
        question=current_q_data['question'],
        student_answer=answer,
        score=result['score'],
        detailed_critique=result['detailed_critique']
    )

@technical_bp.route('/technical_interview_summary')
def technical_interview_summary():
    session_id = session.get('tech_interview_session_id')
    answers = TechnicalInterviewAnswer.query.filter_by(
        session_id=session_id
    ).all()

    total = 0
    for ans in answers:
        total += ans.score

    average = total / len(answers) if answers else 0

    tech_session = TechnicalInterviewSession.query.get(session_id)
    if tech_session:
        tech_session.total_score = average
        db.session.commit()

    session.pop('tech_questions', None)
    session.pop('tech_current_question_index', None)
    session.pop('tech_interview_session_id', None)

    return render_template(
        'technical_interview_summary.html',
        answers=answers,
        average=round(average, 2)
    )

@technical_bp.route('/technical_interview_history')
def technical_interview_history():
    if 'student_id' not in session:
        return redirect(url_for('student.student_login'))
    student_id = session.get('student_id')
    sessions = TechnicalInterviewSession.query.filter_by(
        student_id=student_id
    ).order_by(TechnicalInterviewSession.created_at.desc()).all()
    return render_template(
        'technical_interview_history.html',
        sessions=sessions
    )
