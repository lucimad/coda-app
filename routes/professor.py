from flask import Blueprint, render_template, request, redirect, url_for, flash, send_file
from flask_login import login_required, current_user

from app import db
from models import Outline
from utils import export_to_docx, validate_assessments_weight
import json

professor_bp = Blueprint('professor', __name__)


# -------------------------
# Dashboard
# -------------------------
@professor_bp.route('/dashboard')
@login_required
def dashboard():
    outlines = Outline.query.filter_by(user_id=current_user.id).order_by(Outline.updated_at.desc()).all()
    return render_template('dashboard.html', outlines=outlines)


# -------------------------
# Create Outline
# -------------------------
@professor_bp.route('/outline/new', methods=['GET', 'POST'])
@login_required
def create_outline():
    if request.method == 'POST':
        course_code = request.form['course_code']
        course_title = request.form['course_title']
        term = request.form['term']
        language = request.form['language']
        credits = request.form['credits']
        modality = request.form['modality']

        professor_name = request.form['professor_name']
        professor_email = request.form['professor_email']
        office_hours = request.form['office_hours']
        location = request.form['location']
        teaching_assistant = request.form['teaching_assistant']

        assessments = request.form.get('assessments_json', '[]')
        schedule = request.form.get('schedule_json', '[]')
        policies = request.form.get('policies_text', '')

        # Validate assessments = 100%
        if not validate_assessments_weight(json.loads(assessments)):
            flash('Assessment weights must total 100%', 'error')
            return redirect(url_for('professor.create_outline'))

        outline = Outline(
            user_id=current_user.id,
            course_code=course_code,
            course_title=course_title,
            term=term,
            language=language,
            credits=credits,
            modality=modality,
            professor_name=professor_name,
            professor_email=professor_email,
            office_hours=office_hours,
            location=location,
            teaching_assistant=teaching_assistant,
            assessments_json=assessments,
            schedule_json=schedule,
            policies_text=policies,
            status='Draft'
        )

        db.session.add(outline)
        db.session.commit()

        flash('Outline created successfully!', 'success')
        return redirect(url_for('professor.dashboard'))

    return render_template('outline_form.html')
