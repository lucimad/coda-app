from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

db = SQLAlchemy()
login_manager = LoginManager()


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'change-this-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///coda.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'main.login'

    from models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from routes.main import main_bp
    from routes.professor import professor_bp
    from routes.admin import admin_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(professor_bp, url_prefix='/professor')
    app.register_blueprint(admin_bp, url_prefix='/admin')

    with app.app_context():
        db.create_all()
        seed_admin()

    return app


def seed_admin():
    from models import User
    from werkzeug.security import generate_password_hash

    admin = User.query.filter_by(email='admin@coda.com').first()
    if not admin:
        admin = User(
            name='Admin',
            email='admin@coda.com',
            password_hash=generate_password_hash('admin123'),
            role='admin'
        )
        db.session.add(admin)
        db.session.commit()
        print("Admin created: admin@coda.com / admin123")


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
