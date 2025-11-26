from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from app import db
from models import User

main_bp = Blueprint('main', __name__)


# -------------------------
# Index
# -------------------------
@main_bp.route('/')
def index():
    return render_template('index.html')


# -------------------------
# Login
# -------------------------
@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email'].lower()
        password = request.form['password']

        user = User.query.filter_by(email=email).first()

        if not user or not check_password_hash(user.password_hash, password):
            flash('Invalid email or password', 'error')
            return redirect(url_for('main.login'))

        login_user(user)
        flash('Logged in successfully!', 'success')

        if user.role == 'admin':
            return redirect(url_for('admin.dashboard'))
        return redirect(url_for('professor.dashboard'))

    return render_template('login.html')


# -------------------------
# Register
# -------------------------
@main_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email'].lower()
        password = request.form['password']
        confirm = request.form['confirm']

        if password != confirm:
            flash('Passwords do not match', 'error')
            return redirect(url_for('main.register'))

        if User.query.filter_by(email=email).first():
            flash('Email already registered', 'error')
            return redirect(url_for('main.register'))

        new_user = User(
            name=name,
            email=email,
            password_hash=generate_password_hash(password),
            role='professor'
        )
        db.session.add(new_user)
        db.session.commit()

        flash('Account created successfully! Please log in.', 'success')
        return redirect(url_for('main.login'))

    return render_template('register.html')


# -------------------------
# Logout
# -------------------------
@main_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('main.index'))
