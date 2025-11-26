from flask import Blueprint, render_template, request, redirect, url_for, flash, send_file
from flask_login import login_required, current_user

from app import db
from models import Outline
from utils import export_to_docx

admin_bp = Blueprint('admin', __name__)


def admin_required(f):
    from functools import wraps
    @wraps(f)
    def wrapped(*args, **kwargs):
        if current_user.role != 'admin':
            flash('Access denied', 'error')
            return redirect(url_for('professor.dashboard'))
        return f(*args, **kwargs)
    return wrapped


# -------------------------
# Admin Dashboard
# -------------------------
@admin_bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    term_filter = request.args.get('term', '')
    email_filter = request.args.get('email', '')
    status_filter = request.args.get('status', '')

    query = Outline.query

    if term_filter:
        query = query.filter(Outline.term.contains(term_filter))
    if email_filter:
        query = query.join(Outline.user).filter(Outline.user.email.contains(email_filter))
    if status_filter:
        query = query.filter(Outline.status == status_filter)

    outlines = query.order_by(Outline.updated_at.desc()).all()

    return render_template(
        'admin_dashboard.html',
        outlines=outlines,
        term_filter=term_filter,
        email_filter=email_filter,
        status_filter=status_filter
    )
