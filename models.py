from app import db
from flask_login import UserMixin
from datetime import datetime


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    email = db.Column(db.String(150), unique=True)
    password_hash = db.Column(db.String(200))
    role = db.Column(db.String(20), default='professor')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    outlines = db.relationship('Outline', backref='user', lazy=True)


class Outline(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    term = db.Column(db.String(50))
    course_code = db.Column(db.String(50))
    course_title = db.Column(db.String(150))
    language = db.Column(db.String(10))
    credits = db.Column(db.String(10))
    modality = db.Column(db.String(50))

    professor_name = db.Column(db.String(150))
    professor_email = db.Column(db.String(150))
    office_hours = db.Column(db.String(200))
    location = db.Column(db.String(200))
    teaching_assistant = db.Column(db.String(200))

    assessments_json = db.Column(db.Text)
    schedule_json = db.Column(db.Text)
    policies_text = db.Column(db.Text)

    status = db.Column(db.String(20), default='Draft')

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
