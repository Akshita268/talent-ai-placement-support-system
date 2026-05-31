
import os
import json
from ai_modules.resume_feedback import (
    generate_resume_feedback
)
from flask import (
    render_template,
    redirect,
    session,
    url_for,
    request,
    flash
)

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from werkzeug.utils import secure_filename

from flask import Blueprint

from ai_modules.ats_engine import calculate_ats_score, extract_pdf_text, clean_text, extract_skills
from ai_modules.embedding_engine import get_similarity_score
from ai_modules.career_recommender import recommend_career
from ai_modules.roadmap_generator import generate_roadmap
from flask_login import current_user

from models.models import (
    db,
    Student,
    Job,
    Application,
    InterviewSession,
    TechnicalInterviewSession,
    Notification,
    CandidateContactDetails
)


student_bp = Blueprint(
    'student',
    __name__
)



# =========================================
# STUDENT REGISTER
# =========================================

@student_bp.route(
    '/student/register',
    methods=['GET', 'POST']
)
def student_register():

    if request.method == 'POST':

        full_name = request.form.get('full_name')

        email = request.form.get('email')

        password = request.form.get('password')

        resume = request.files.get('resume')


        # Check duplicate email
        existing_student = Student.query.filter_by(
            email=email
        ).first()


        if existing_student:

            flash('Email already registered.', 'error')

            return redirect(
                url_for('student.student_register')
            )


        # Hash password
        hashed_password = generate_password_hash(
            password
        )


        # Resume upload
        resume_filename = None

        if resume and resume.filename != '':

            filename = secure_filename(
                resume.filename
            )

            resume_path = os.path.join(
                'uploads/resumes',
                filename
            )

            resume.save(resume_path)

            resume_filename = filename


        # Create student
        new_student = Student(

            full_name=full_name,

            email=email,

            password=hashed_password

        )


        db.session.add(new_student)

        db.session.commit()


        flash('Registration Successful', 'success')

        return redirect(
            url_for('student.student_login')
        )


    return render_template(
        'student_register.html'
    )



# =========================================
# STUDENT LOGIN
# =========================================

@student_bp.route(
    '/student/login',
    methods=['GET', 'POST']
)
def student_login():

    if request.method == 'POST':

        email = request.form.get('email')

        password = request.form.get('password')


        student = Student.query.filter_by(
            email=email
        ).first()


        if student and check_password_hash(
            student.password,
            password
        ):

            # Store student session
            session['student_id'] = student.id


            flash('Login Successful', 'success')


            return redirect(
                url_for(
                    'student.student_dashboard'
                )
            )

        else:

            flash('Invalid Email or Password', 'error')

            return redirect(
                url_for('student.student_login')
            )


    return render_template(
        'student_login.html'
    )



# =========================================
# STUDENT LOGOUT
# =========================================

@student_bp.route('/student/logout')
def student_logout():

    session.pop('student_id', None)

    flash('Logged Out Successfully', 'success')

    return redirect(
        url_for('student.student_login')
    )



# =========================================
# STUDENT DASHBOARD
# =========================================

@student_bp.route('/student/dashboard')
def student_dashboard():
    student_id = session.get('student_id')
    if not student_id:
        flash('Please login first.', 'warning')
        return redirect(url_for('student.student_login'))
        
    student = Student.query.get_or_404(student_id)
    
    # Calculate performance averages
    apps = Application.query.filter_by(student_id=student.id).all()
    ats_avg = sum(app.ats_score for app in apps if app.ats_score is not None) / len([app for app in apps if app.ats_score is not None]) if [app for app in apps if app.ats_score is not None] else 0
    
    hr_sessions = InterviewSession.query.filter_by(student_id=student.id).all()
    hr_avg = sum(s.total_score for s in hr_sessions if s.total_score is not None) / len([s for s in hr_sessions if s.total_score is not None]) if [s for s in hr_sessions if s.total_score is not None] else 0
    
    tech_sessions = TechnicalInterviewSession.query.filter_by(student_id=student.id).all()
    tech_avg = sum(s.total_score for s in tech_sessions if s.total_score is not None) / len([s for s in tech_sessions if s.total_score is not None]) if [s for s in tech_sessions if s.total_score is not None] else 0
    
    # Calculate Readiness Score (0-100)
    # Readiness = 0.4 ATS + 0.3 HR + 0.3 Technical
    readiness_score = round(0.4 * ats_avg + 0.3 * hr_avg + 0.3 * tech_avg, 2)
    
    # Generate Strengths, Weak Areas, and Improvement Plan
    strengths = []
    weak_areas = []
    
    if ats_avg >= 70:
        strengths.append("Resume Alignment (ATS match is strong)")
    else:
        weak_areas.append("Resume Quality (ATS match requires optimization)")
        
    if hr_avg >= 70:
        strengths.append("HR Communication (Strong behavioral response structure)")
    else:
        weak_areas.append("HR Interview Prep (Needs practice with behavioral scenarios)")
        
    if tech_avg >= 70:
        strengths.append("Technical Concepts (Domain knowledge is solid)")
    else:
        weak_areas.append("Technical Theory (Requires review of core CS concepts)")
        
    if not strengths:
        strengths.append("Initial platform setup completed")
    if not weak_areas:
        weak_areas.append("Keep practicing mock interviews to maintain peak readiness")
        
    # Improvement Plan logic based on lowest category
    scores_dict = {
        "ATS Resume Match": ats_avg,
        "HR Interview": hr_avg,
        "Technical Interview": tech_avg
    }
    lowest_area = min(scores_dict, key=scores_dict.get)
    
    if len(apps) == 0 and len(hr_sessions) == 0 and len(tech_sessions) == 0:
        improvement_plan = "Welcome to TalentAI! Start by uploading your resume, taking an HR mock interview, or taking a Technical mock interview to calculate your readiness metrics."
    elif lowest_area == "ATS Resume Match":
        improvement_plan = "Your average ATS score is the lowest category. Optimize your resume by adding quantifiable achievements and aligning your skills list with your target role."
    elif lowest_area == "HR Interview":
        improvement_plan = "Focus on HR Communication: Your HR mock scores are relatively low. Avoid filler words, speak confidently, and structure your responses using the STAR method."
    else:
        improvement_plan = "Focus on Technical Concepts: Your mock technical score shows room for growth. Review CS core topics like database normalization, OS concurrency, or specific domain frameworks."
    
    # AI Skill Gap Analysis
    target_role = student.target_role
    role_skills = []
    resume_skills = []
    missing_skills = []
    matched_skills = []
    skill_gap_recommendations = []
    
    latest_app = Application.query.filter_by(student_id=student.id).order_by(Application.id.desc()).first()
    if target_role:
        from ai_modules.career_recommender import ROLE_KEYWORDS
        role_skills = ROLE_KEYWORDS.get(target_role, [])
        if latest_app and latest_app.resume_filename:
            resume_path = os.path.join('uploads/resumes', latest_app.resume_filename)
            resume_text = extract_pdf_text(resume_path)
            if resume_text:
                resume_skills = extract_skills(clean_text(resume_text))
                matched_skills = [s for s in role_skills if s in resume_skills]
                missing_skills = [s for s in role_skills if s not in resume_skills]
        else:
            missing_skills = list(role_skills)
            
        # Recommended Learning Actions mapping
        learning_actions_map = {
            "docker": "Learn Docker Fundamentals & Containerization",
            "aws": "Learn AWS EC2, S3, & Cloud deployment",
            "flask": "Deploy Flask or FastAPI web applications",
            "django": "Learn Django MVC architecture and ORM",
            "fastapi": "Build high-performance REST APIs with FastAPI",
            "machine learning": "Build Machine Learning Models using Scikit-Learn",
            "deep learning": "Train Deep Learning neural networks",
            "pytorch": "Train neural networks using PyTorch",
            "tensorflow": "Learn TensorFlow & Keras model training",
            "sql": "Practice SQL queries and database indexes",
            "databases": "Learn Database Normalization and Schema Design",
            "mysql": "Learn MySQL querying and schema designs",
            "postgresql": "Practice PostgreSQL indexing and window functions",
            "sqlite": "Practice SQLite lightweight database setups",
            "react": "Build single-page web applications with React",
            "react.js": "Build UI components with React",
            "javascript": "Learn modern JavaScript (ES6+, Event Loop, Promises)",
            "html": "Learn Semantic HTML5 layout systems",
            "css": "Master CSS Layouts (Flexbox, Grid) and animations",
            "tailwind": "Implement modern UI styling with Tailwind CSS",
            "bootstrap": "Implement responsive UI components with Bootstrap 5",
            "data structures": "Practice Data Structures (Arrays, Linked Lists, HashMaps)",
            "algorithms": "Solve Algorithm challenges (Sorting, Searching, DP)",
            "operating systems": "Study OS Core processes, threads, and memory",
            "computer networks": "Study TCP/IP protocols, DNS, and HTTP methods",
            "excel": "Analyze datasets and create charts in Microsoft Excel",
            "tableau": "Create interactive BI dashboards in Tableau",
            "power bi": "Design metrics dashboards in Power BI",
            "data analysis": "Data cleaning and analysis using Python",
            "pandas": "Practice data manipulation using Pandas dataframes",
            "numpy": "Learn vector operations and matrices with NumPy",
            "statistics": "Study descriptive and inferential statistics (p-values, hypothesis tests)",
            "visualization": "Create storytelling charts with Matplotlib & Seaborn",
            "dashboard": "Design metrics monitoring dashboards",
            "ui": "Learn User Interface design principles",
            "ux": "Study User Experience design & wireframing",
            "frontend": "Learn frontend build systems & SEO optimizations",
            "backend": "Study backend systems design and API caching",
            "git": "Learn Git Version Control (branches, commits, pulls)",
            "github": "Host portfolio code repositories on GitHub"
        }
        
        for ms in missing_skills:
            action = learning_actions_map.get(ms.lower())
            if action and action not in skill_gap_recommendations:
                skill_gap_recommendations.append(action)
            if len(skill_gap_recommendations) >= 4:
                break
                
        if not skill_gap_recommendations:
            skill_gap_recommendations = [
                "Practice core data structures & algorithms daily",
                "Build a portfolio project and deploy it to a cloud provider",
                "Take mock technical and HR interviews to refine communication",
                "Ensure your resume highlights quantifiable project results"
            ]

    # Job Recommendations using Resume Embedding
    recommended_jobs = []
    if latest_app and latest_app.resume_filename:
        resume_path = os.path.join('uploads/resumes', latest_app.resume_filename)
        resume_text = extract_pdf_text(resume_path)
        if resume_text:
            clean_res = clean_text(resume_text)
            all_jobs = Job.query.all()
            scored_jobs = []
            for j in all_jobs:
                applied = Application.query.filter_by(student_id=student.id, job_id=j.id).first()
                if not applied:
                    clean_jd = clean_text(j.job_description)
                    sim = get_similarity_score(clean_res, clean_jd)
                    scored_jobs.append((j, sim))
            scored_jobs.sort(key=lambda x: x[1], reverse=True)
            for j, sim in scored_jobs[:3]:
                if sim >= 80:
                    why_rec = f"Strong match ({sim}%). Your resume shows a highly compatible set of skills for this role, matching key requirements."
                elif sim >= 60:
                    why_rec = f"Good match ({sim}%). Your background has significant overlap with this role. Some missing skills can be bridged easily."
                else:
                    why_rec = f"Moderate match ({sim}%). This role shares engineering fundamentals with your profile. A great opportunity to expand your skillset."
                recommended_jobs.append((j, sim, why_rec))
            
    # Parse roadmap data
    roadmap_data = None
    if student.learning_roadmap:
        try:
            roadmap_data = json.loads(student.learning_roadmap)
            if not isinstance(roadmap_data, dict):
                roadmap_data = None
        except Exception:
            pass
 
    notifications = Notification.query.filter_by(student_id=student.id).order_by(Notification.created_at.desc()).all()

    return render_template(
        'student_dashboard.html',
        student=student,
        readiness_score=readiness_score,
        ats_avg=round(ats_avg, 2),
        hr_avg=round(hr_avg, 2),
        tech_avg=round(tech_avg, 2),
        recommended_jobs=recommended_jobs,
        improvement_plan=improvement_plan,
        strengths=strengths,
        weak_areas=weak_areas,
        roadmap_data=roadmap_data,
        role_skills=role_skills,
        resume_skills=resume_skills,
        missing_skills=missing_skills,
        matched_skills=matched_skills,
        skill_gap_recommendations=skill_gap_recommendations,
        notifications=notifications
    )
 
@student_bp.route('/student/set_target_role', methods=['POST'])
def set_target_role():
    student_id = session.get('student_id')
    if not student_id:
        flash('Please login first.', 'warning')
        return redirect(url_for('student.student_login'))
        
    target_role = request.form.get('target_role')
    student = Student.query.get(student_id)
    if student:
        student.target_role = target_role
        
        # Calculate career recommendation
        latest_app = Application.query.filter_by(student_id=student.id).order_by(Application.id.desc()).first()
        resume_path = None
        if latest_app and latest_app.resume_filename:
            resume_path = os.path.join('uploads/resumes', latest_app.resume_filename)
            
        apps = Application.query.filter_by(student_id=student.id).all()
        ats_history = [{'job_role': app.job.job_role, 'ats_score': app.ats_score} for app in apps if app.job is not None]
        
        hr_sessions = InterviewSession.query.filter_by(student_id=student.id).all()
        hr_scores = [{'score': s.total_score} for s in hr_sessions]
        
        tech_sessions = TechnicalInterviewSession.query.filter_by(student_id=student.id).all()
        tech_scores = [{'domain': s.domain, 'score': s.total_score} for s in tech_sessions]
        
        rec = recommend_career(resume_path, ats_history, hr_scores, tech_scores)
        student.career_recommendation = f"Path: {rec['career_path']} | Compatibility: {rec['alignment_score']}% | Rationale: {rec['rationale']}"
        
        # Extract skills from resume for learning roadmap customization
        resume_skills = []
        if resume_path:
            resume_text = extract_pdf_text(resume_path)
            if resume_text:
                resume_skills = extract_skills(clean_text(resume_text))
                
        # Generate learning roadmap with missing skills
        from ai_modules.career_recommender import ROLE_KEYWORDS
        role_skills = ROLE_KEYWORDS.get(target_role, [])
        missing_skills = [s for s in role_skills if s not in resume_skills]
        
        rm = generate_roadmap(target_role, missing_skills)
        student.learning_roadmap = json.dumps(rm)
        
        # Trigger Student Notification: Roadmap Update
        rm_msg = f"Your learning roadmap for {target_role} has been successfully generated."
        rm_notif = Notification(
            student_id=student_id,
            message=rm_msg
        )
        db.session.add(rm_notif)
        
        db.session.commit()
        flash('Target role updated, career alignment checked, and AI roadmap updated!', 'success')
        
    return redirect(url_for('student.student_dashboard'))



# =========================================
# VIEW AVAILABLE JOBS
# =========================================

@student_bp.route('/jobs')
def available_jobs():

    jobs = Job.query.all()

    return render_template(
        'available_jobs.html',
        jobs=jobs
    )



# =========================================
# JOB DETAILS PAGE
# =========================================

@student_bp.route('/job/<int:job_id>')
def job_details(job_id):
    job = Job.query.get_or_404(job_id)
    student_id = session.get('student_id')
    skill_gap = None
    if student_id:
        latest_app = Application.query.filter_by(student_id=student_id).order_by(Application.id.desc()).first()
        if latest_app and latest_app.resume_filename:
            resume_path = os.path.join('uploads/resumes', latest_app.resume_filename)
            if os.path.exists(resume_path):
                try:
                    resume_text = extract_pdf_text(resume_path)
                    if resume_text:
                        resume_skills = set([s.lower() for s in extract_skills(clean_text(resume_text))])
                        job_skills_list = [s.strip().lower() for s in job.skills_required.split(',') if s.strip()]
                        
                        matched = [s for s in job_skills_list if s in resume_skills]
                        missing = [s for s in job_skills_list if s not in resume_skills]
                        priority = missing[:2]
                        
                        learning_map = {
                            "docker": "Learn Docker Fundamentals & Containerization",
                            "aws": "Learn AWS EC2, S3, & Cloud deployment",
                            "flask": "Deploy Flask or FastAPI web applications",
                            "django": "Learn Django MVC architecture and ORM",
                            "fastapi": "Build high-performance REST APIs with FastAPI",
                            "machine learning": "Build Machine Learning Models using Scikit-Learn",
                            "deep learning": "Train Deep Learning neural networks",
                            "pytorch": "Train neural networks using PyTorch",
                            "tensorflow": "Learn TensorFlow & Keras model training",
                            "sql": "Practice SQL queries and database indexes",
                            "databases": "Learn Database Normalization and Schema Design",
                            "mysql": "Learn MySQL querying and schema designs",
                            "postgresql": "Practice PostgreSQL indexing and window functions",
                            "sqlite": "Practice SQLite lightweight database setups",
                            "react": "Build single-page web applications with React",
                            "javascript": "Learn modern JavaScript (ES6+, Event Loop, Promises)",
                            "html": "Learn Semantic HTML5 layout systems",
                            "css": "Master CSS Layouts (Flexbox, Grid) and animations",
                            "tailwind": "Implement modern UI styling with Tailwind CSS",
                            "git": "Learn Git Version Control (branches, commits, pulls)"
                        }
                        
                        suggestions = []
                        for ms in missing:
                            action = learning_map.get(ms.lower(), f"Master the fundamentals and advanced usages of {ms.title()}")
                            if action and action not in suggestions:
                                suggestions.append(action)
                        if not suggestions:
                            suggestions = ["Practice core coding patterns", "Build hands-on projects representing this role's workflows"]
                            
                        skill_gap = {
                            "matched": [s.title() for s in matched],
                            "missing": [s.title() for s in missing],
                            "priority": [s.title() for s in priority],
                            "suggestions": suggestions
                        }
                except Exception:
                    pass

    return render_template(
        'job_details.html',
        job=job,
        skill_gap=skill_gap
    )



# =========================================
# APPLY TO JOB
# =========================================

@student_bp.route(
    '/check_ats/<int:job_id>',
    methods=['GET', 'POST']
)
def check_ats(job_id):

    job = Job.query.get_or_404(job_id)

    student_id = session.get('student_id')

    if not student_id:
        flash('Please login first.', 'warning')
        return redirect(
            url_for('student.student_login')
        )

    if request.method == 'POST':

        resume = request.files.get('resume')

        if not resume or resume.filename == '':
            flash('Please upload resume.', 'warning')
            return redirect(request.url)

        filename = secure_filename(
            resume.filename
        )

        resume_path = os.path.join(
            'uploads/resumes',
            filename
        )

        resume.save(resume_path)

        jd_text = job.job_description

        try:

            ats_result = calculate_ats_score(
                resume_path,
                jd_text
            )

            feedback_result = generate_resume_feedback(
                ats_result['ats_score'],
                ats_result['matched_skills'],
                ats_result['missing_skills']
            )

        except Exception:

            flash("Invalid PDF file uploaded. Please upload a valid PDF.", "error")
            return redirect(url_for('student.check_ats', job_id=job_id))

        session['resume_filename'] = filename
        session['ats_score'] = ats_result['ats_score']
        session['embedding_score'] = ats_result['embedding_score']
        session['skill_score'] = ats_result['skill_match_score']
        session['project_score'] = ats_result['project_score']
        session['matched_skills'] = ", ".join(ats_result['matched_skills'])
        session['missing_skills'] = ", ".join(ats_result['missing_skills'])
        session['feedback'] = ats_result['feedback']

        return render_template(
            'ats_result.html',
            job=job,
            ats_result=ats_result,
            feedback_result=feedback_result
        )

    return render_template(
        'upload_resume.html',
        job=job
    )

@student_bp.route('/final_apply/<int:job_id>')
def final_apply(job_id):

    student_id = session.get('student_id')

    if not student_id:

        flash('Please login first.', 'warning')
        return redirect(
            url_for('student.student_login')
        )


    # Prevent duplicate application
    existing_application = Application.query.filter_by(
        student_id=student_id,
        job_id=job_id
    ).first()


    if existing_application:

        flash('Already applied for this job.', 'warning')

        return redirect(
            url_for('student.available_jobs')
        )


    # Get ATS data from session
    resume_filename = session.get('resume_filename')
    ats_score = session.get('ats_score')
    feedback = session.get('feedback')
    embedding_score = session.get('embedding_score')
    skill_score = session.get('skill_score')
    project_score = session.get('project_score')
    matched_skills = session.get('matched_skills')
    missing_skills = session.get('missing_skills')

    # Save application
    application = Application(
        student_id=student_id,
        job_id=job_id,
        resume_filename=resume_filename,
        ats_score=ats_score,
        feedback=feedback,
        embedding_score=embedding_score,
        skill_score=skill_score,
        project_score=project_score,
        matched_skills=matched_skills,
        missing_skills=missing_skills
    )


    db.session.add(application)
    db.session.commit()

    try:
        student = Student.query.get(student_id)
        job = Job.query.get(job_id)
        if student and job:
            # 1. Student Notification: ATS Update
            stud_msg = f"Your ATS evaluation for {job.job_role} at {job.company_name} is complete. Score: {int(ats_score)}%."
            stud_notif = Notification(
                student_id=student_id,
                application_id=application.id,
                message=stud_msg
            )
            db.session.add(stud_notif)
            
            # 2. Recruiter Notification: New Application
            rec_msg = f"New application received from {student.full_name} for {job.job_role}."
            rec_notif = Notification(
                recruiter_id=job.recruiter_id,
                application_id=application.id,
                message=rec_msg
            )
            db.session.add(rec_notif)
            
            db.session.commit()
    except Exception:
        pass


    flash('Application Submitted Successfully', 'success')


    return redirect(
        url_for('student.my_applications')
    )

# =========================================
# MY APPLICATIONS
# =========================================

@student_bp.route('/my_applications')
def my_applications():

    student_id = session.get('student_id')


    if not student_id:

        flash('Please login first.', 'warning')
        return redirect(
            url_for('student.student_login')
        )


    applications = Application.query.filter_by(
        student_id=student_id
    ).all()


    return render_template(
        'my_applications.html',
        applications=applications
    )
@student_bp.route('/student/profile', methods=['GET', 'POST'])
def student_profile():
    student_id = session.get('student_id')
    if not student_id:
        flash('Please login first.', 'warning')
        return redirect(url_for('student.student_login'))
        
    student = Student.query.get_or_404(student_id)
    
    if request.method == 'POST':
        full_name = request.form.get('full_name', '').strip()
        email = request.form.get('email', '').strip()
        if not full_name or not email:
            flash('All fields are required', 'error')
            return redirect(url_for('student.student_profile'))
            
        existing = Student.query.filter_by(email=email).first()
        if existing and existing.id != student.id:
            flash('Email already registered by another user', 'error')
            return redirect(url_for('student.student_profile'))
            
        student.full_name = full_name
        student.email = email
        db.session.commit()
        flash('Profile updated successfully', 'success')
        return redirect(url_for('student.student_profile'))
        
    # Calculate stats
    apps = Application.query.filter_by(student_id=student.id).all()
    total_apps = len(apps)
    ats_avg = sum(app.ats_score for app in apps if app.ats_score is not None) / len([app for app in apps if app.ats_score is not None]) if [app for app in apps if app.ats_score is not None] else 0
    
    hr_sessions = InterviewSession.query.filter_by(student_id=student.id).all()
    hr_avg = sum(s.total_score for s in hr_sessions if s.total_score is not None) / len([s for s in hr_sessions if s.total_score is not None]) if [s for s in hr_sessions if s.total_score is not None] else 0
    
    tech_sessions = TechnicalInterviewSession.query.filter_by(student_id=student.id).all()
    tech_avg = sum(s.total_score for s in tech_sessions if s.total_score is not None) / len([s for s in tech_sessions if s.total_score is not None]) if [s for s in tech_sessions if s.total_score is not None] else 0
    
    return render_template(
        'student_profile.html',
        student=student,
        total_apps=total_apps,
        ats_avg=round(ats_avg, 2),
        hr_avg=round(hr_avg, 2),
        tech_avg=round(tech_avg, 2)
    )

@student_bp.route('/student')
def student_home():

    return render_template(
        'student_home.html'
    )

@student_bp.route('/student/application/<int:app_id>/contact-details', methods=['GET', 'POST'])
def submit_contact_details(app_id):
    student_id = session.get('student_id')
    if not student_id:
        flash('Please login first.', 'warning')
        return redirect(url_for('student.student_login'))
        
    application = Application.query.get_or_404(app_id)
    if application.student_id != student_id:
        flash('Unauthorized access', 'error')
        return redirect(url_for('student.student_dashboard'))
        
    if application.status not in ['Shortlisted', 'Selected']:
        flash('Cannot submit contact details for this application status.', 'warning')
        return redirect(url_for('student.my_applications'))
        
    existing = CandidateContactDetails.query.filter_by(application_id=app_id).first()
    if existing:
        flash('Contact details already submitted.', 'info')
        return redirect(url_for('student.my_applications'))
        
    if request.method == 'POST':
        phone = request.form.get('phone', '').strip()
        linkedin = request.form.get('linkedin', '').strip()
        location = request.form.get('location', '').strip()
        contact_time = request.form.get('contact_time', '').strip()
        notes = request.form.get('notes', '').strip()
        
        if linkedin and not linkedin.startswith(('http://', 'https://')):
            linkedin = 'https://' + linkedin
            
        if not phone or not linkedin or not location or not contact_time:
            flash('All required fields must be filled.', 'error')
            return render_template('submit_contact_details.html', application=application)
            
        details = CandidateContactDetails(
            student_id=student_id,
            application_id=app_id,
            phone=phone,
            linkedin=linkedin,
            location=location,
            contact_time=contact_time,
            notes=notes
        )
        db.session.add(details)
        
        try:
            student = Student.query.get(student_id)
            job = Job.query.get(application.job_id)
            if student and job:
                rec_msg = f"Candidate {student.full_name} has submitted contact details for {job.job_role}."
                rec_notif = Notification(
                    recruiter_id=job.recruiter_id,
                    application_id=app_id,
                    message=rec_msg
                )
                db.session.add(rec_notif)
        except Exception:
            pass
            
        db.session.commit()
        flash('Contact details submitted successfully!', 'success')
        return redirect(url_for('student.my_applications'))
        
    return render_template('submit_contact_details.html', application=application)

@student_bp.route('/student/resume-compare', methods=['GET', 'POST'])
def resume_compare():
    student_id = session.get('student_id')
    if not student_id:
        flash('Please login first.', 'warning')
        return redirect(url_for('student.student_login'))
        
    jobs = Job.query.all()
    comparison = None
    
    if request.method == 'POST':
        job_id = request.form.get('job_id')
        resume_v1 = request.files.get('resume_v1')
        resume_v2 = request.files.get('resume_v2')
        
        if not job_id or not resume_v1 or not resume_v2 or resume_v1.filename == '' or resume_v2.filename == '':
            flash('Please select a job and upload both resume versions.', 'warning')
            return redirect(url_for('student.resume_compare'))
            
        job = Job.query.get_or_404(job_id)
        
        # Save temp files
        os.makedirs('uploads/temp', exist_ok=True)
        path_v1 = os.path.join('uploads/temp', secure_filename('v1_' + resume_v1.filename))
        path_v2 = os.path.join('uploads/temp', secure_filename('v2_' + resume_v2.filename))
        
        try:
            resume_v1.save(path_v1)
            resume_v2.save(path_v2)
            
            # Extract texts
            text_v1 = extract_pdf_text(path_v1)
            text_v2 = extract_pdf_text(path_v2)
            
            if not text_v1 or not text_v2:
                flash('Could not extract text from one or both resumes. Make sure they are valid PDFs.', 'error')
                return redirect(url_for('student.resume_compare'))
                
            # ATS scores
            ats_v1 = calculate_ats_score(path_v1, job.job_description)
            ats_v2 = calculate_ats_score(path_v2, job.job_description)
            
            # Clean and get embedding similarity between resumes
            clean_v1 = clean_text(text_v1)
            clean_v2 = clean_text(text_v2)
            embedding_sim = get_similarity_score(clean_v1, clean_v2)
            
            # Skills extraction
            skills_v1 = set([s.lower() for s in extract_skills(clean_v1)])
            skills_v2 = set([s.lower() for s in extract_skills(clean_v2)])
            job_skills = set([s.strip().lower() for s in job.skills_required.split(',') if s.strip()])
            
            new_skills = [s.title() for s in (skills_v2 - skills_v1)]
            removed_skills = [s.title() for s in (skills_v1 - skills_v2)]
            still_missing = [s.title() for s in (job_skills - skills_v2)]
            
            score_diff = round(ats_v2['ats_score'] - ats_v1['ats_score'], 2)
            
            # Generate Report Rationale
            insights = []
            if score_diff > 0:
                insights.append(f"Resume V2 increases your ATS alignment score by {score_diff}%, showing positive optimization.")
            elif score_diff < 0:
                insights.append(f"Resume V2 decreases your ATS alignment score by {abs(score_diff)}%. Check if critical keywords or projects were removed.")
            else:
                insights.append("Both resumes scored the same. The semantic adjustments did not alter the keyword match weights significantly.")
                
            if new_skills:
                insights.append(f"Added {len(new_skills)} new skills to your profile: {', '.join(new_skills[:4])}.")
            if still_missing:
                insights.append(f"You still have {len(still_missing)} missing skills compared to the job description: {', '.join(still_missing[:4])}.")
            
            # Clean up files
            if os.path.exists(path_v1):
                os.remove(path_v1)
            if os.path.exists(path_v2):
                os.remove(path_v2)
                
            comparison = {
                "job": job,
                "score_v1": ats_v1['ats_score'],
                "score_v2": ats_v2['ats_score'],
                "score_diff": score_diff,
                "similarity": embedding_sim,
                "skills_v1": [s.title() for s in skills_v1],
                "skills_v2": [s.title() for s in skills_v2],
                "new_skills": new_skills,
                "removed_skills": removed_skills,
                "still_missing": still_missing,
                "insights": insights
            }
        except Exception as e:
            # clean up files
            if os.path.exists(path_v1):
                os.remove(path_v1)
            if os.path.exists(path_v2):
                os.remove(path_v2)
            flash(f"Error comparing resumes: {str(e)}", 'error')
            return redirect(url_for('student.resume_compare'))
            
    return render_template(
        'resume_compare.html',
        jobs=jobs,
        comparison=comparison
    )

# =========================================
# NOTIFICATION ROUTES
# =========================================

@student_bp.route('/notification/delete/<int:notification_id>', methods=['GET', 'POST'])
def delete_notification(notification_id):
    student_id = session.get('student_id')
    is_recruiter = current_user.is_authenticated
    
    if not student_id and not is_recruiter:
        flash('Please login first.', 'warning')
        return redirect(url_for('home'))
        
    notification = Notification.query.get_or_404(notification_id)
    
    # Verify authorization
    if student_id and notification.student_id == student_id:
        db.session.delete(notification)
        db.session.commit()
        flash('Notification deleted successfully.', 'success')
        return redirect(url_for('student.student_dashboard'))
    elif is_recruiter and notification.recruiter_id == current_user.id:
        db.session.delete(notification)
        db.session.commit()
        flash('Notification deleted successfully.', 'success')
        return redirect('/recruiter/dashboard')
    else:
        flash('Unauthorized access.', 'error')
        if student_id:
            return redirect(url_for('student.student_dashboard'))
        else:
            return redirect('/recruiter/dashboard')

@student_bp.route('/notification/clear-all', methods=['GET', 'POST'])
def clear_all_notifications():
    student_id = session.get('student_id')
    is_recruiter = current_user.is_authenticated
    
    if not student_id and not is_recruiter:
        flash('Please login first.', 'warning')
        return redirect(url_for('home'))
        
    if student_id:
        Notification.query.filter_by(student_id=student_id).delete()
        db.session.commit()
        flash('All notifications cleared.', 'success')
        return redirect(url_for('student.student_dashboard'))
    elif is_recruiter:
        Notification.query.filter_by(recruiter_id=current_user.id).delete()
        db.session.commit()
        flash('All notifications cleared.', 'success')
        return redirect('/recruiter/dashboard')
