from flask import render_template, request, redirect, flash, send_from_directory

from flask_login import (
    login_user,
    logout_user,
    login_required,
    current_user
)

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from werkzeug.utils import secure_filename

from models.models import (
    db,
    Recruiter,
    Job,
    Application,
    Student,
    InterviewSession,
    TechnicalInterviewSession,
    Notification,
    CandidateContactDetails
)

import os


def register_routes(app):

    # =========================================
    # RECRUITER HOME
    # =========================================

    @app.route("/recruiter")
    def recruiter_home():

        return render_template(
            "recruiter_home.html"
        )

    # =========================================
    # RECRUITER REGISTER
    # =========================================

    @app.route(
        "/recruiter/register",
        methods=["GET", "POST"]
    )
    def recruiter_register():

        if request.method == "POST":

            company_name = request.form[
                "company_name"
            ].strip()

            email = request.form[
                "email"
            ].strip()

            password = request.form[
                "password"
            ].strip()

            if not company_name or not email or not password:

                flash("All fields are required", "error")
                return render_template("recruiter_register.html")

            existing_recruiter = Recruiter.query.filter_by(
                email=email
            ).first()

            if existing_recruiter:

                flash("Email already registered", "error")
                return render_template("recruiter_register.html")

            hashed_password = generate_password_hash(
                password
            )

            recruiter = Recruiter(
                company_name=company_name,
                email=email,
                password=hashed_password
            )

            db.session.add(recruiter)

            db.session.commit()

            login_user(recruiter)
            flash("Registration successful", "success")

            return redirect(
                "/recruiter/dashboard"
            )

        return render_template(
            "recruiter_register.html"
        )

    # =========================================
    # RECRUITER LOGIN
    # =========================================

    @app.route(
        "/recruiter/login",
        methods=["GET", "POST"]
    )
    def recruiter_login():

        if request.method == "POST":

            email = request.form[
                "email"
            ].strip()

            password = request.form[
                "password"
            ].strip()

            if not email or not password:

                flash("All fields are required", "error")
                return render_template("recruiter_login.html")

            recruiter = Recruiter.query.filter_by(
                email=email
            ).first()

            if recruiter and check_password_hash(
                recruiter.password,
                password
            ):

                login_user(recruiter)
                flash("Login successful", "success")

                return redirect(
                    "/recruiter/dashboard"
                )

            flash("Invalid Email or Password", "error")
            return render_template("recruiter_login.html")

        return render_template(
            "recruiter_login.html"
        )

    # =========================================
    # RECRUITER DASHBOARD
    # =========================================

    @app.route("/recruiter/dashboard")
    @login_required
    def recruiter_dashboard():
        # Get all jobs posted by the recruiter
        jobs = Job.query.filter_by(recruiter_id=current_user.id).all()
        job_ids = [j.id for j in jobs]
        
        # Get all applications
        applications = Application.query.filter(Application.job_id.in_(job_ids)).all() if job_ids else []
        total_apps = len(applications)
        
        # Calculate average ATS score
        valid_ats = [app.ats_score for app in applications if app.ats_score]
        avg_ats = round(sum(valid_ats) / len(valid_ats), 2) if valid_ats else 0
        
        # Recruiter Funnel metrics (Applied -> Shortlisted -> Interview Scheduled -> Selected -> Rejected)
        funnel = {"Applied": 0, "Shortlisted": 0, "Interview Scheduled": 0, "Selected": 0, "Rejected": 0}
        for app in applications:
            status = app.status or 'Applied'
            if status in funnel:
                funnel[status] += 1
            else:
                funnel["Applied"] += 1
                
        shortlisted_count = funnel["Shortlisted"]
        selected_count = funnel["Selected"]
        rejected_count = funnel["Rejected"]
                
        # ATS Score Distribution (Excellent >=80, Good 60-79, Average 40-59, Low <40)
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
                
        # Skill Distribution analysis
        skill_counts = {}
        for app in applications:
            if app.matched_skills:
                skills = [s.strip().lower() for s in app.matched_skills.split(',') if s.strip()]
                for s in skills:
                    skill_counts[s] = skill_counts.get(s, 0) + 1
        # Get top 5 skills
        sorted_skills = sorted(skill_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        top_skills = [s[0].title() for s in sorted_skills]
        top_skill_values = [s[1] for s in sorted_skills]
        
        # Compute Top 3 Ranked Candidates across all jobs using recruiter ranking formula:
        # 0.3 * ATS + 0.2 * Resume Match + 0.2 * Skill Match + 0.2 * Project Strength + 0.1 * Completeness
        ranked_candidates = []
        for app in applications:
            student = Student.query.get(app.student_id)
            if not student:
                continue
            
            ats_val = app.ats_score or 0
            resume_match = app.embedding_score or 0
            skill_match = app.skill_score or 0
            project_strength = app.project_score or 0
            completeness = 100 if app.contact_details else 80
            
            final_score = round(0.30 * ats_val + 0.20 * resume_match + 0.20 * skill_match + 0.20 * project_strength + 0.10 * completeness, 2)
            
            ranked_candidates.append({
                "student_name": student.full_name,
                "job_role": app.job.job_role,
                "ats_score": ats_val,
                "resume_match": resume_match,
                "skill_match": skill_match,
                "project_strength": project_strength,
                "completeness": completeness,
                "final_score": final_score
            })
            
        ranked_candidates.sort(key=lambda x: x["final_score"], reverse=True)
        top_candidates = ranked_candidates[:3]
        best_candidate = ranked_candidates[0] if ranked_candidates else None
        
        # Calculate most common missing skills
        missing_skill_counts = {}
        for app in applications:
            if app.missing_skills:
                skills = [s.strip().lower() for s in app.missing_skills.split(',') if s.strip()]
                for s in skills:
                    missing_skill_counts[s] = missing_skill_counts.get(s, 0) + 1
        sorted_missing = sorted(missing_skill_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        top_missing_skills = [s[0].title() for s in sorted_missing]
        top_missing_values = [s[1] for s in sorted_missing]
        
        # Query recruiter notifications
        notifications = Notification.query.filter_by(recruiter_id=current_user.id).order_by(Notification.created_at.desc()).all()
        
        # Generate automatic Recruiter Insights text
        insights = []
        if top_candidates:
            insights.append(f"Top Talent: {top_candidates[0]['student_name']} is highly recommended for the {top_candidates[0]['job_role']} role with an application match score of {top_candidates[0]['final_score']}% (ATS: {top_candidates[0]['ats_score']}%).")
        else:
            insights.append("No applications submitted yet. Insights will compile once candidates apply.")
            
        if sorted_skills:
            insights.append(f"Common Skill: '{sorted_skills[0][0].title()}' is the most common skill among candidates. If seeking differentiators, check for candidates with Docker, Kubernetes, or AWS cloud experience.")
        
        if applications:
            if avg_ats < 60:
                insights.append(f"ATS Alert: The average candidate match rate is relatively low ({avg_ats}%). Consider adjusting role keywords to broaden the pipeline.")
            else:
                insights.append(f"Pipeline Health: Average ATS compatibility is solid at {avg_ats}%, showing highly aligned candidates.")
        
        return render_template(
            "recruiter_dashboard.html",
            total_jobs=len(jobs),
            total_apps=total_apps,
            avg_ats=avg_ats,
            shortlisted_count=shortlisted_count,
            selected_count=selected_count,
            rejected_count=rejected_count,
            funnel=funnel,
            ats_dist=ats_dist,
            top_skills=top_skills,
            top_skill_values=top_skill_values,
            top_missing_skills=top_missing_skills,
            top_missing_values=top_missing_values,
            top_candidates=top_candidates,
            best_candidate=best_candidate,
            notifications=notifications,
            insights=insights
        )

    # =========================================
    # RECRUITER PROFILE
    # =========================================

    @app.route(
        "/recruiter/profile",
        methods=["GET", "POST"]
    )
    @login_required
    def recruiter_profile():
        if request.method == "POST":
            company_name = request.form.get("company_name", "").strip()
            email = request.form.get("email", "").strip()
            if not company_name or not email:
                flash("All fields are required", "error")
                return redirect("/recruiter/profile")
            
            existing = Recruiter.query.filter_by(email=email).first()
            if existing and existing.id != current_user.id:
                flash("Email already registered by another user", "error")
                return redirect("/recruiter/profile")
            
            current_user.company_name = company_name
            current_user.email = email
            db.session.commit()
            flash("Profile updated successfully", "success")
            return redirect("/recruiter/profile")

        total_jobs = Job.query.filter_by(
            recruiter_id=current_user.id
        ).count()
        
        jobs = Job.query.filter_by(recruiter_id=current_user.id).all()
        job_ids = [j.id for j in jobs]
        total_apps = Application.query.filter(Application.job_id.in_(job_ids)).count() if job_ids else 0
        valid_ats = db.session.query(db.func.avg(Application.ats_score)).filter(Application.job_id.in_(job_ids), Application.ats_score.isnot(None)).scalar() if job_ids else 0
        avg_ats = round(valid_ats, 2) if valid_ats else 0

        return render_template(
            "recruiter_profile.html",
            recruiter=current_user,
            total_jobs=total_jobs,
            total_apps=total_apps,
            avg_ats=avg_ats
        )

    # =========================================
    # RECRUITER LOGOUT
    # =========================================

    @app.route("/recruiter/logout")
    @login_required
    def recruiter_logout():

        logout_user()

        return redirect("/")

    # =========================================
    # CREATE JOB
    # =========================================

    @app.route(
        "/recruiter/create-job",
        methods=["GET", "POST"]
    )
    @login_required
    def create_job():

        if request.method == "POST":

            company_name = request.form[
                "company_name"
            ].strip()

            job_role = request.form[
                "job_role"
            ].strip()

            eligibility = request.form[
                "eligibility"
            ].strip()

            skills_required = request.form[
                "skills_required"
            ].strip()

            job_description = request.form[
                "job_description"
            ].strip()

            if (
                not company_name
                or not job_role
                or not eligibility
                or not skills_required
                or not job_description
            ):
                flash("Please fill all fields", "error")
                return render_template("create_job.html")

            uploaded_file = request.files.get(
                "jd_pdf"
            )

            pdf_filename = None

            if uploaded_file and uploaded_file.filename != "":

                if not uploaded_file.filename.lower().endswith(
                    ".pdf"
                ):
                    flash("Only PDF files allowed", "warning")
                    return render_template("create_job.html")

                os.makedirs(
                    "uploads/job_descriptions",
                    exist_ok=True
                )

                pdf_filename = secure_filename(
                    uploaded_file.filename
                )

                file_path = os.path.join(
                    "uploads/job_descriptions",
                    pdf_filename
                )

                uploaded_file.save(
                    file_path
                )

            job = Job(
                recruiter_id=current_user.id,
                company_name=company_name,
                job_role=job_role,
                eligibility=eligibility,
                skills_required=skills_required,
                job_description=job_description,
                jd_pdf_filename=pdf_filename
            )

            db.session.add(job)

            db.session.commit()
            flash("Job created successfully", "success")

            return redirect(
                "/recruiter/jobs"
            )

        return render_template(
            "create_job.html"
        )

    # =========================================
    # VIEW JOBS
    # =========================================

    @app.route("/recruiter/jobs")
    @login_required
    def recruiter_jobs():

        jobs = Job.query.filter_by(
            recruiter_id=current_user.id
        ).all()

        return render_template(
            "recruiter_jobs.html",
            jobs=jobs
        )

    # =========================================
    # DELETE JOB
    # =========================================

    @app.route(
        "/recruiter/delete-job/<int:job_id>"
    )
    @login_required
    def delete_job(job_id):

        job = Job.query.filter_by(
            id=job_id,
            recruiter_id=current_user.id
        ).first()

        if not job:

            flash("Job not found", "error")
            return redirect(
                "/recruiter/jobs"
            )

        db.session.delete(job)

        db.session.commit()
        flash("Job deleted successfully", "success")

        return redirect(
            "/recruiter/jobs"
        )

    # =========================================
    # VIEW APPLICANTS
    # =========================================

    @app.route(
        "/recruiter/job/<int:job_id>/applicants"
    )
    @login_required
    def view_applicants(job_id):
        job = Job.query.filter_by(
            id=job_id,
            recruiter_id=current_user.id
        ).first()

        if not job:
            flash("Job not found", "error")
            return redirect("/recruiter/dashboard")

        raw_applicants = Application.query.filter_by(
            job_id=job.id
        ).all()

        applicants = []
        for app in raw_applicants:
            student = Student.query.get(app.student_id)
            if not student:
                continue
            
            ats_val = app.ats_score or 0
            resume_match = app.embedding_score or 0
            skill_match = app.skill_score or 0
            project_strength = app.project_score or 0
            completeness = 100 if app.contact_details else 80
            
            final_score = round(0.30 * ats_val + 0.20 * resume_match + 0.20 * skill_match + 0.20 * project_strength + 0.10 * completeness, 2)
            
            # Attach dynamic properties
            app.student_name = student.full_name
            app.student_email = student.email
            app.final_score = final_score
            applicants.append(app)
            
        # Sort applicants descending by final_score
        applicants.sort(key=lambda x: x.final_score, reverse=True)

        return render_template(
            "job_applicants.html",
            job=job,
            applicants=applicants
        )

    # =========================================
    # SERVE RESUME
    # =========================================

    @app.route('/uploads/resumes/<filename>')
    def serve_resume(filename):
        from flask import session
        if not current_user.is_authenticated and not session.get('student_id'):
            flash("Unauthorized access", "error")
            return redirect("/")
            
        download = request.args.get('download', 'false').lower() == 'true'
        uploads_dir = os.path.abspath(os.path.join(os.getcwd(), 'uploads', 'resumes'))
        return send_from_directory(
            uploads_dir,
            filename,
            as_attachment=download
        )

    # =========================================
    # UPDATE APPLICATION STATUS
    # =========================================

    @app.route('/recruiter/application/<int:app_id>/update-status', methods=['POST'])
    @login_required
    def update_application_status(app_id):
        application = Application.query.get_or_404(app_id)
        job = Job.query.get(application.job_id)
        if not job or job.recruiter_id != current_user.id:
            flash("Unauthorized access", "error")
            return redirect("/recruiter/dashboard")
            
        new_status = request.form.get("status")
        if new_status not in ["Applied", "Shortlisted", "Interview Scheduled", "Selected", "Rejected"]:
            flash("Invalid status", "error")
            return redirect(f"/recruiter/job/{job.id}/applicants")
            
        application.status = new_status
        student = Student.query.get(application.student_id)
        
        # Trigger student notification
        if new_status in ["Shortlisted", "Interview Scheduled", "Selected", "Rejected"]:
            msg = ""
            if new_status == "Shortlisted":
                msg = f"You have been shortlisted for {job.job_role} at {job.company_name}."
            elif new_status == "Interview Scheduled":
                msg = f"Your interview has been scheduled for {job.job_role} at {job.company_name}."
            elif new_status == "Selected":
                msg = f"You have been selected for {job.job_role} at {job.company_name}."
            elif new_status == "Rejected":
                msg = "We appreciate your interest. Your application was not selected for this role."
                
            notification = Notification(
                student_id=application.student_id,
                application_id=application.id,
                message=msg
            )
            db.session.add(notification)
            
            # Trigger Recruiter Notification for Status Update
            if student:
                rec_msg = f"Status updated to '{new_status}' for candidate {student.full_name} (Role: {job.job_role})."
                rec_notif = Notification(
                    recruiter_id=job.recruiter_id,
                    application_id=application.id,
                    message=rec_msg
                )
                db.session.add(rec_notif)
            
        db.session.commit()
        flash("Application status updated successfully", "success")
        return redirect(f"/recruiter/job/{job.id}/applicants")

    # =========================================
    # AI JD GENERATOR ROUTE
    # =========================================

    @app.route('/recruiter/generate-jd', methods=['POST'])
    @login_required
    def generate_ai_jd():
        data = request.get_json() or {}
        action = data.get("action", "generate")
        role = data.get("role", "")
        skills = data.get("skills", "")
        eligibility = data.get("eligibility", "")
        text = data.get("text", "")
        
        from ai_modules.jd_generator import generate_jd, improve_jd, enhance_structure, make_professional
        
        if action == "generate":
            if not role:
                return {"error": "Job Role is required to generate a description."}, 400
            generated_text = generate_jd(role, skills, eligibility)
        elif action == "improve":
            if not text:
                return {"error": "Job Description text is required to improve."}, 400
            generated_text = improve_jd(text)
        elif action == "enhance":
            if not text:
                return {"error": "Job Description text is required to enhance structure."}, 400
            generated_text = enhance_structure(text)
        elif action == "professional":
            if not text:
                return {"error": "Job Description text is required to perform a professional rewrite."}, 400
            generated_text = make_professional(text)
        else:
            return {"error": "Invalid action specified."}, 400
            
        return {
            "job_description": generated_text
        }

    # =========================================
    # APPLICANT DETAILS & NOTES
    # =========================================

    @app.route('/recruiter/application/<int:app_id>/details', methods=['GET', 'POST'])
    @login_required
    def applicant_details(app_id):
        application = Application.query.get_or_404(app_id)
        job = Job.query.get(application.job_id)
        if not job or job.recruiter_id != current_user.id:
            flash("Unauthorized access", "error")
            return redirect("/recruiter/dashboard")
            
        student = Student.query.get_or_404(application.student_id)
        
        if request.method == 'POST':
            notes = request.form.get("recruiter_notes", "").strip()
            application.recruiter_notes = notes
            db.session.commit()
            flash("Recruiter notes updated successfully", "success")
            return redirect(f"/recruiter/application/{app_id}/details")
            
        ats_val = application.ats_score or 0
        resume_match = application.embedding_score or 0
        skill_match = application.skill_score or 0
        project_strength = application.project_score or 0
        completeness = 100 if application.contact_details else 80
        
        final_score = round(0.30 * ats_val + 0.20 * resume_match + 0.20 * skill_match + 0.20 * project_strength + 0.10 * completeness, 2)
        
        # Attach properties for presentation
        application.student_name = student.full_name
        application.student_email = student.email
        application.resume_match = resume_match
        application.skill_match = skill_match
        application.project_strength = project_strength
        application.completeness = completeness
        application.final_score = final_score
        
        return render_template(
            "applicant_details.html",
            application=application,
            job=job,
            student=student
        )

    # =========================================
    # VIEW CANDIDATE CONTACT DETAILS (SEPARATE PAGE)
    # =========================================

    @app.route('/recruiter/applicant/<int:app_id>', methods=['GET'])
    @login_required
    def view_candidate_contact_details(app_id):
        application = Application.query.get_or_404(app_id)
        job = Job.query.get(application.job_id)
        if not job or job.recruiter_id != current_user.id:
            flash("Unauthorized access", "error")
            return redirect("/recruiter/dashboard")
            
        student = Student.query.get_or_404(application.student_id)
        
        # Attach properties for presentation
        application.student_name = student.full_name
        application.student_email = student.email
        
        return render_template(
            "candidate_contact_details.html",
            application=application,
            job=job
        )

    # =========================================
    # SERVE JOB DESCRIPTION PDF
    # =========================================

    @app.route('/uploads/job_descriptions/<filename>')
    def serve_job_description(filename):
        from flask import session
        if not current_user.is_authenticated and not session.get('student_id'):
            flash("Unauthorized access", "error")
            return redirect("/")
            
        uploads_dir = os.path.abspath(os.path.join(os.getcwd(), 'uploads', 'job_descriptions'))
        return send_from_directory(
            uploads_dir,
            filename
        )


