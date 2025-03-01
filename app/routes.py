# app/routes.py
from flask import Blueprint, render_template, redirect, url_for, flash,session, request
from . import db, bcrypt
from .models import User
from .forms import LoginForm, RegistrationForm
from flask_login import login_user, login_required, logout_user, current_user
from flask_bcrypt import generate_password_hash
from datetime import datetime

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template("home.html")

from flask_login import current_user

#login route
@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            print(f'Logged in user: {current_user.email}, Role: {current_user.role}')

            # Debugging role value
            print(f"User role type: {type(current_user.role)}, Value: {current_user.role}")

            if current_user.role.strip().lower() == 'student':
                return redirect(url_for('main.student_dashboard'))
            elif current_user.role.strip().lower() == 'teacher':
                return redirect(url_for('main.teacher_dashboard'))
        else:
            print("Not logged in")
            flash("Login Unsuccessful. Check email and password.", 'danger')
    return render_template("login.html", form=form)


#register route
@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        form.date_of_birth.data = datetime.strptime(form.date_of_birth.data, '%d/%m/%Y').date()
        user = User(username=form.username.data, email=form.email.data, password=hashed_password, fullName=form.fullName.data, qualification=form.qualification.data, date_of_birth=form.date_of_birth.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('main.login'))
    return render_template("register.html", form=form)


#create a dashboard route
@main.route('/student_dashboard')
@login_required
def student_dashboard():
    return render_template("student_dashboard.html")

@main.route('/teacher_dashboard')
@login_required
def teacher_dashboard():
    return render_template("teacher_dashboard.html")

@main.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))