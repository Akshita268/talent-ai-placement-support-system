from flask import Blueprint, render_template, session, redirect, url_for, flash, request
from models.models import db, CodingPrepProgress
from ai_modules.coding_prep_questions import CATEGORIES, get_subcategory_questions

technical_prep_bp = Blueprint(
    "technical_prep",
    __name__
)

# ==========================================
# CODING PREPARATION DASHBOARD (CATEGORIES)
# ==========================================

@technical_prep_bp.route("/coding-prep")
def coding_prep_dashboard():
    if 'student_id' not in session:
        flash('Please login first.', 'warning')
        return redirect(url_for('student.student_login'))
        
    return render_template(
        "coding_prep_dashboard.html",
        categories=CATEGORIES
    )


# ==========================================
# CATEGORY PAGE (SUBCATEGORIES)
# ==========================================

@technical_prep_bp.route("/coding-prep/category/<category_name>")
def coding_prep_category(category_name):
    if 'student_id' not in session:
        flash('Please login first.', 'warning')
        return redirect(url_for('student.student_login'))
        
    category_data = CATEGORIES.get(category_name)
    if not category_data:
        flash('Category not found.', 'error')
        return redirect(url_for('technical_prep.coding_prep_dashboard'))
        
    # Get completion progress count for this category
    student_id = session.get('student_id')
    completions = CodingPrepProgress.query.filter_by(
        student_id=student_id,
        category=category_name
    ).all()
    
    # Map subcategory to completed count
    completed_map = {}
    for comp in completions:
        completed_map[comp.subcategory] = completed_map.get(comp.subcategory, 0) + 1
        
    return render_template(
        "coding_prep_category.html",
        category_name=category_name,
        category=category_data,
        completed_map=completed_map
    )


# ==========================================
# SUBCATEGORY PAGE (TOP 15 QUESTIONS LIST)
# ==========================================

@technical_prep_bp.route("/coding-prep/subcategory/<category_name>/<subcategory_name>")
def coding_prep_subcategory(category_name, subcategory_name):
    if 'student_id' not in session:
        flash('Please login first.', 'warning')
        return redirect(url_for('student.student_login'))
        
    category_data = CATEGORIES.get(category_name)
    if not category_data or subcategory_name not in category_data["topics"]:
        flash('Subcategory not found.', 'error')
        return redirect(url_for('technical_prep.coding_prep_dashboard'))
        
    student_id = session.get('student_id')
    
    # Get all 15 questions
    all_questions = get_subcategory_questions(category_name, subcategory_name)
    
    # Get completed question IDs for this subcategory
    completions = CodingPrepProgress.query.filter_by(
        student_id=student_id,
        category=category_name,
        subcategory=subcategory_name
    ).all()
    completed_ids = {comp.question_id for comp in completions}
    
    # Search filter
    search_query = request.args.get('search', '').strip()
    filtered_questions = []
    for q in all_questions:
        # Attach completion state
        q["completed"] = q["id"] in completed_ids
        
        # Apply search filter
        if search_query:
            if search_query.lower() in q["question"].lower() or search_query.lower() in q["answer"].lower():
                filtered_questions.append(q)
        else:
            filtered_questions.append(q)
            
    completed_count = len(completed_ids)
    total_count = len(all_questions)
    progress_pct = int((completed_count / total_count) * 100) if total_count > 0 else 0
    
    return render_template(
        "coding_prep_subcategory.html",
        category_name=category_name,
        category=category_data,
        subcategory_name=subcategory_name,
        questions=filtered_questions,
        completed_count=completed_count,
        total_count=total_count,
        progress_pct=progress_pct,
        search_query=search_query
    )


# ==========================================
# QUESTION DETAILS PAGE
# ==========================================

@technical_prep_bp.route("/coding-prep/question/<category_name>/<subcategory_name>/<int:question_id>")
def coding_prep_question(category_name, subcategory_name, question_id):
    if 'student_id' not in session:
        flash('Please login first.', 'warning')
        return redirect(url_for('student.student_login'))
        
    category_data = CATEGORIES.get(category_name)
    if not category_data or subcategory_name not in category_data["topics"]:
        flash('Subcategory not found.', 'error')
        return redirect(url_for('technical_prep.coding_prep_dashboard'))
        
    # Get all questions and locate the matching one
    all_questions = get_subcategory_questions(category_name, subcategory_name)
    target_question = None
    for q in all_questions:
        if q["id"] == question_id:
            target_question = q
            break
            
    if not target_question:
        flash('Question not found.', 'error')
        return redirect(url_for('technical_prep.coding_prep_subcategory', category_name=category_name, subcategory_name=subcategory_name))
        
    student_id = session.get('student_id')
    
    # Check if completed
    completed = CodingPrepProgress.query.filter_by(
        student_id=student_id,
        category=category_name,
        subcategory=subcategory_name,
        question_id=question_id
    ).first() is not None
    
    # Find prev/next question IDs for navigation
    prev_id = question_id - 1 if question_id > 1 else None
    next_id = question_id + 1 if question_id < len(all_questions) else None
    
    return render_template(
        "coding_prep_question.html",
        category_name=category_name,
        category=category_data,
        subcategory_name=subcategory_name,
        question=target_question,
        completed=completed,
        prev_id=prev_id,
        next_id=next_id
    )


# ==========================================
# TOGGLE COMPLETION ACTION
# ==========================================

@technical_prep_bp.route("/coding-prep/toggle-completion/<category_name>/<subcategory_name>/<int:question_id>", methods=['GET', 'POST'])
def toggle_completion(category_name, subcategory_name, question_id):
    if 'student_id' not in session:
        flash('Please login first.', 'warning')
        return redirect(url_for('student.student_login'))
        
    student_id = session.get('student_id')
    
    existing = CodingPrepProgress.query.filter_by(
        student_id=student_id,
        category=category_name,
        subcategory=subcategory_name,
        question_id=question_id
    ).first()
    
    if existing:
        db.session.delete(existing)
        db.session.commit()
        flash('Question marked as incomplete.', 'info')
    else:
        new_progress = CodingPrepProgress(
            student_id=student_id,
            category=category_name,
            subcategory=subcategory_name,
            question_id=question_id
        )
        db.session.add(new_progress)
        db.session.commit()
        flash('Question marked as completed!', 'success')
        
    # Redirect back to where user came from
    referrer = request.referrer or ""
    if "question" in referrer:
        return redirect(url_for('technical_prep.coding_prep_question', category_name=category_name, subcategory_name=subcategory_name, question_id=question_id))
    else:
        return redirect(url_for('technical_prep.coding_prep_subcategory', category_name=category_name, subcategory_name=subcategory_name))
