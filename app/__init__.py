# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from datetime import datetime
from config import Config

# Initialize extensions (no circular imports)
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'main.login'

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions with app
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    # Register Blueprints
    from .routes import main
    app.register_blueprint(main)

    # Database setup and default admin creation
    with app.app_context():
        from .models import User  # Import models here to avoid circular imports
        db.create_all()

        # Create default admin if not exists
        if not User.query.filter_by(role="admin").first():
            admin_password = bcrypt.generate_password_hash("adminpassword").decode('utf-8')
            date_of_birth_str = "01/01/2000"
            date_of_birth = datetime.strptime(date_of_birth_str, '%d/%m/%Y').date()

            admin = User(
                username="admin",
                email="admin@example.com",
                password=admin_password,
                role="admin",
                fullName="Admin User",
                date_of_birth=date_of_birth
            )
            db.session.add(admin)
            db.session.commit()
            print("Admin user created.")
        else:
            print("Admin user already exists.")

    return app

@login_manager.user_loader
def load_user(user_id):
    from .models import User  # Avoid circular import
    return User.query.get(int(user_id))
