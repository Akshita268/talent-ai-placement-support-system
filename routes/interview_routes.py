from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    session
)

from models.models import (
    db,
    InterviewSession,
    InterviewAnswer
)

from ai_modules.hr_question_generator import generate_hr_questions

from ai_modules.hr_answer_evaluator import evaluate_answer
interview_bp = Blueprint(
    'interview',
    __name__
)
@interview_bp.route('/interview')
def interview_dashboard():

    if 'student_id' not in session:

        return redirect(
            url_for('student.student_login')
        )

    return render_template(
        'interview_dashboard.html'
    )
    return render_template(
        'interview_dashboard.html'
    )
@interview_bp.route(
    '/start_interview',
    methods=['POST']
)
def start_interview():

    if 'student_id' not in session:
        return redirect(
            url_for('student.student_login')
        )

    role = request.form['job_role']

    experience = request.form['experience']

    student_id = session.get('student_id')

    new_session = InterviewSession(
        student_id=student_id,
        job_role=role,
        experience_level=experience
    )

    db.session.add(new_session)

    db.session.commit()

    questions = generate_hr_questions(
        role,
        experience
    )

    session['interview_session_id'] = new_session.id

    session['questions'] = questions

    session['current_question_index'] = 0

    return redirect(
        url_for('interview.show_question')
    )
@interview_bp.route('/question')
def show_question():

    questions = session.get('questions')

    if not questions:
        return redirect(
            url_for('interview.interview_dashboard')
        )

    index = session.get(
        'current_question_index',
        0
    )

    if index >= len(questions):
        return redirect(
            url_for('interview.interview_summary')
        )

    question = questions[index]

    return render_template(
        'interview_question.html',
        question=question,
        question_number=index + 1
    )
@interview_bp.route(
    '/submit_answer',
    methods=['POST']
)
def submit_answer():

    answer = request.form['answer']

    questions = session.get('questions')

    index = session.get(
        'current_question_index'
    )

    current_question = questions[index]

    result = evaluate_answer(
        current_question,
        answer
    )

    interview_answer = InterviewAnswer(
        session_id=session['interview_session_id'],
        question=current_question,
        student_answer=answer,
        score=result['score'],
        feedback=result['feedback'],
        communication_score=result['communication_score'],
        confidence_score=result['confidence_score'],
        leadership_score=result['leadership_score'],
        problem_solving_score=result['problem_solving_score'],
        improved_answer=result['improved_answer']
    )

    db.session.add(interview_answer)
    db.session.commit()

    session['current_question_index'] += 1

    return render_template(
        'interview_feedback.html',
        score=result['score'],
        feedback=result['feedback']
    )
@interview_bp.route('/interview_summary')
def interview_summary():

    interview_id = session.get(
        'interview_session_id'
    )

    answers = InterviewAnswer.query.filter_by(
        session_id=interview_id
    ).all()

    total = 0

    for ans in answers:
        total += ans.score

    average = total / len(answers)

    interview = InterviewSession.query.get(
        interview_id
    )

    interview.total_score = average

    db.session.commit()
    session.pop('questions', None)

    session.pop('current_question_index', None)

    session.pop('interview_session_id', None)

    return render_template(
        'interview_summary.html',
        answers=answers,
        average=average
    )
@interview_bp.route('/interview_history')
def interview_history():

    student_id = session.get('student_id')

    interviews = InterviewSession.query.filter_by(
        student_id=student_id
    ).order_by(
        InterviewSession.created_at.desc()
    ).all()

    return render_template(
        'interview_history.html',
        interviews=interviews
    )