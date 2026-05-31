from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()


# =========================================
# RECRUITER MODEL
# =========================================

class Recruiter(UserMixin, db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    company_name = db.Column(
        db.String(100),
        nullable=False
    )

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(200),
        nullable=False
    )

    jobs = db.relationship(
        'Job',
        backref='recruiter',
        lazy=True
    )

    notifications = db.relationship(
        'Notification',
        backref='recruiter',
        lazy=True,
        cascade="all, delete-orphan"
    )


# =========================================
# JOB MODEL
# =========================================

class Job(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    recruiter_id = db.Column(
        db.Integer,
        db.ForeignKey("recruiter.id"),
        nullable=False
    )

    company_name = db.Column(
        db.String(100),
        nullable=False
    )

    job_role = db.Column(
        db.String(100),
        nullable=False
    )

    eligibility = db.Column(
        db.String(200),
        nullable=False
    )

    skills_required = db.Column(
        db.Text,
        nullable=False
    )

    job_description = db.Column(
        db.Text,
        nullable=False
    )

    jd_pdf_filename = db.Column(
        db.String(200)
    )

    applications = db.relationship(
        'Application',
        backref='job',
        lazy=True
    )


# =========================================
# STUDENT MODEL
# =========================================

class Student(UserMixin, db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    full_name = db.Column(
        db.String(100),
        nullable=False
    )

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(200),
        nullable=False
    )

    applications = db.relationship(
        'Application',
        backref='student',
        lazy=True
    )

    target_role = db.Column(
        db.String(100)
    )

    career_recommendation = db.Column(
        db.Text
    )

    learning_roadmap = db.Column(
        db.Text
    )

    interview_sessions = db.relationship(
        'InterviewSession',
        backref='student',
        lazy=True
    )

    technical_sessions = db.relationship(
        'TechnicalInterviewSession',
        backref='student',
        lazy=True
    )

    notifications = db.relationship(
        'Notification',
        backref='student',
        lazy=True,
        cascade="all, delete-orphan"
    )

    contact_details = db.relationship(
        'CandidateContactDetails',
        backref='student',
        lazy=True,
        cascade="all, delete-orphan"
    )



# =========================================
# APPLICATION MODEL
# =========================================

class Application(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    student_id = db.Column(
        db.Integer,
        db.ForeignKey('student.id')
    )

    job_id = db.Column(
        db.Integer,
        db.ForeignKey('job.id')
    )

    status = db.Column(
        db.String(50),
        default='Applied'
    )

    resume_filename = db.Column(
        db.String(200)
    )

    ats_score = db.Column(
        db.Float
    )

    matched_skills = db.Column(
        db.Text
    )

    missing_skills = db.Column(
        db.Text
    )

    feedback = db.Column(
        db.Text
    )

    strengths = db.Column(
        db.Text
    )

    suggestions = db.Column(
        db.Text
    )

    embedding_score = db.Column(
        db.Float
    )

    skill_score = db.Column(
        db.Float
    )

    project_score = db.Column(
        db.Float
    )

    recruiter_notes = db.Column(
        db.Text
    )

    notifications = db.relationship(
        'Notification',
        backref='application',
        lazy=True,
        cascade="all, delete-orphan"
    )

    contact_details = db.relationship(
        'CandidateContactDetails',
        backref='application',
        uselist=False,
        lazy=True,
        cascade="all, delete-orphan"
    )
# =========================================
# HR INTERVIEW SESSION
# =========================================

class InterviewSession(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    student_id = db.Column(
        db.Integer,
        db.ForeignKey('student.id'),
        nullable=False
    )

    job_role = db.Column(
        db.String(100)
    )

    experience_level = db.Column(
        db.String(50)
    )

    total_score = db.Column(
        db.Float,
        default=0
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    answers = db.relationship(
        'InterviewAnswer',
        backref='session',
        lazy=True,
        cascade="all, delete-orphan"
    )


# =========================================
# HR INTERVIEW ANSWERS
# =========================================

class InterviewAnswer(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    session_id = db.Column(
        db.Integer,
        db.ForeignKey('interview_session.id'),
        nullable=False
    )

    question = db.Column(
        db.Text
    )

    student_answer = db.Column(
        db.Text
    )

    score = db.Column(
        db.Float
    )

    feedback = db.Column(
        db.Text
    )

    communication_score = db.Column(
        db.Float
    )

    confidence_score = db.Column(
        db.Float
    )

    leadership_score = db.Column(
        db.Float
    )

    problem_solving_score = db.Column(
        db.Float
    )

    improved_answer = db.Column(
        db.Text
    )


# =========================================
# TECHNICAL INTERVIEW SESSION
# =========================================

class TechnicalInterviewSession(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    student_id = db.Column(
        db.Integer,
        db.ForeignKey('student.id'),
        nullable=False
    )

    domain = db.Column(
        db.String(100)
    )

    difficulty = db.Column(
        db.String(50)
    )

    total_score = db.Column(
        db.Float,
        default=0
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    answers = db.relationship(
        'TechnicalInterviewAnswer',
        backref='session',
        lazy=True,
        cascade="all, delete-orphan"
    )


# =========================================
# TECHNICAL INTERVIEW ANSWERS
# =========================================

class TechnicalInterviewAnswer(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    session_id = db.Column(
        db.Integer,
        db.ForeignKey(
            'technical_interview_session.id'
        ),
        nullable=False
    )

    question = db.Column(
        db.Text
    )

    correct_answer = db.Column(
        db.Text
    )

    student_answer = db.Column(
        db.Text
    )

    score = db.Column(
        db.Float
    )

    feedback = db.Column(
        db.Text
    )

    topic_score = db.Column(
        db.Float
    )

    weak_areas = db.Column(
        db.Text
    )

    strong_areas = db.Column(
        db.Text
    )

    suggested_better_answer = db.Column(
        db.Text
    )


# =========================================
# TECHNICAL QUESTION BANK
# =========================================

class TechnicalQuestion(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    topic = db.Column(
        db.String(50),
        nullable=False
    )

    question = db.Column(
        db.Text,
        nullable=False
    )

    answer = db.Column(
        db.Text,
        nullable=False
    )

    difficulty = db.Column(
        db.String(20),
        default='Easy'
    )


# =========================================
# NOTIFICATION MODEL
# =========================================

class Notification(db.Model):
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    
    student_id = db.Column(
        db.Integer,
        db.ForeignKey('student.id'),
        nullable=True
    )
    
    recruiter_id = db.Column(
        db.Integer,
        db.ForeignKey('recruiter.id'),
        nullable=True
    )
    
    application_id = db.Column(
        db.Integer,
        db.ForeignKey('application.id'),
        nullable=True
    )
    
    message = db.Column(
        db.Text,
        nullable=False
    )
    
    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )
    
    is_read = db.Column(
        db.Boolean,
        default=False
    )


# =========================================
# CANDIDATE CONTACT DETAILS MODEL
# =========================================

class CandidateContactDetails(db.Model):
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    
    student_id = db.Column(
        db.Integer,
        db.ForeignKey('student.id'),
        nullable=False
    )
    
    application_id = db.Column(
        db.Integer,
        db.ForeignKey('application.id'),
        nullable=False
    )
    
    phone = db.Column(
        db.String(50),
        nullable=False
    )
    
    linkedin = db.Column(
        db.String(200),
        nullable=False
    )
    
    location = db.Column(
        db.String(100),
        nullable=False
    )
    
    contact_time = db.Column(
        db.String(100),
        nullable=False
    )
    
    notes = db.Column(
        db.Text,
        nullable=True
    )
    
    submitted_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )


# =========================================
# CODING PREP PROGRESS MODEL
# =========================================

class CodingPrepProgress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    subcategory = db.Column(db.String(50), nullable=False)
    question_id = db.Column(db.Integer, nullable=False)
    completed_at = db.Column(db.DateTime, default=datetime.utcnow)




