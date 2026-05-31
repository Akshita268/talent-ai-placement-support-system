from flask import Blueprint, jsonify, session
from models.models import (
    db,
    Application,
    InterviewSession,
    TechnicalInterviewSession,
    Job,
    Student
)
import os

analytics_bp = Blueprint('analytics', __name__)

@analytics_bp.route('/api/student/performance')
def student_performance_api():
    student_id = session.get('student_id')
    if not student_id:
        return jsonify({"error": "Unauthorized"}), 401
        
    apps = Application.query.filter_by(student_id=student_id).all()
    ats_avg = sum(app.ats_score for app in apps if app.ats_score is not None) / len([app for app in apps if app.ats_score is not None]) if [app for app in apps if app.ats_score is not None] else 0
    
    hr_sessions = InterviewSession.query.filter_by(student_id=student_id).all()
    hr_avg = sum(s.total_score for s in hr_sessions if s.total_score is not None) / len([s for s in hr_sessions if s.total_score is not None]) if [s for s in hr_sessions if s.total_score is not None] else 0
    
    tech_sessions = TechnicalInterviewSession.query.filter_by(student_id=student_id).all()
    tech_avg = sum(s.total_score for s in tech_sessions if s.total_score is not None) / len([s for s in tech_sessions if s.total_score is not None]) if [s for s in tech_sessions if s.total_score is not None] else 0
    
    return jsonify({
        "labels": ["ATS Average", "HR Interview", "Technical mock"],
        "scores": [round(float(ats_avg), 2), round(float(hr_avg), 2), round(float(tech_avg), 2)]
    })

@analytics_bp.route('/api/recruiter/stats')
def recruiter_stats_api():
    # Recruiter ID is standard Flask-Login current_user.id
    # We import current_user
    from flask_login import current_user, login_required
    if not current_user.is_authenticated:
        return jsonify({"error": "Unauthorized"}), 401
        
    jobs = Job.query.filter_by(recruiter_id=current_user.id).all()
    job_ids = [j.id for j in jobs]
    
    applications = Application.query.filter(Application.job_id.in_(job_ids)).all() if job_ids else []
    
    # Funnel
    funnel = {"Applied": 0, "Shortlisted": 0, "Interviewed": 0, "Hired": 0}
    for app in applications:
        status = app.status or 'Applied'
        if status in funnel:
            funnel[status] += 1
        else:
            funnel["Applied"] += 1
            
    # ATS Dist
    ats_dist = {"Excellent": 0, "Good": 0, "Average": 0, "Low": 0}
    for app in applications:
        score = app.ats_score or 0
        if score >= 80:
            ats_dist["Excellent"] += 1
        elif score >= 60:
            ats_dist["Good"] += 1
        elif score >= 40:
            ats_dist["Average"] += 1
        else:
            ats_dist["Low"] += 1
            
    return jsonify({
        "funnel": funnel,
        "ats_dist": ats_dist
    })
