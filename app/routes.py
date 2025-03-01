# app/routes.py
from flask import Blueprint, render_template, redirect, url_for, flash,session, request
from . import db, bcrypt
from .models import User, Subject, Chapter, Quiz, Question
from .forms import LoginForm, RegistrationForm, SubjectForm, ChapterForm, QuizForm, QuestionForm
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
            return redirect(url_for('main.dashboard'))
        else:
            print("Not logged in")
            flash("Login Unsuccessful. Check email and password.", 'danger')
    return render_template("login.html", form=form)


#register route
@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        print(f"Selected Role: {form.role.data}")
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        form.date_of_birth.data = datetime.strptime(form.date_of_birth.data, '%d/%m/%Y').date()
        user = User(username=form.username.data, email=form.email.data, password=hashed_password, fullName=form.fullName.data, qualification=form.qualification.data, date_of_birth=form.date_of_birth.data,role=form.role.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('main.login'))
    return render_template("register.html", form=form)


#create a dashboard route
@main.route('/dashboard')
@login_required
def dashboard():
    subjects = Subject.query.all()
    return render_template("dashboard.html",subjects=subjects, user_role=current_user.role)

#subject routes
@main.route('/add_subject', methods=['GET', 'POST'])
@login_required
def add_subject():
    form = SubjectForm()
    if form.validate_on_submit():
        subject = Subject(name=form.name.data, description=form.description.data)
        db.session.add(subject)
        db.session.commit()
        flash(f'Subject {form.name.data} added successfully!', 'success')
        return redirect(url_for('main.dashboard'))
    return render_template("add_subject.html", form=form)

@main.route('/delete_subject/<int:subject_id>', methods=['GET', 'POST'])
@login_required
def delete_subject(subject_id):
    subject = Subject.query.get(subject_id)
    db.session.delete(subject)
    db.session.commit()
    flash(f'Subject {subject.name} deleted successfully!', 'success')
    return redirect(url_for('main.dashboard'))

@main.route('/edit_subject/<int:subject_id>', methods=['GET', 'POST'])
@login_required
def edit_subject(subject_id):
    subject = Subject.query.get(subject_id)
    form = SubjectForm()
    if form.validate_on_submit():
        subject.name = form.name.data
        subject.description = form.description.data
        db.session.commit()
        flash(f'Subject {form.name.data} edited successfully!', 'success')
        return redirect(url_for('main.dashboard'))
    elif request.method == 'GET':
        form.name.data = subject.name
        form.description.data = subject.description
    return render_template("edit_subject.html", form=form,subject=subject)

#chapter routes
@main.route('/add_chapter/<int:subject_id>', methods=['GET', 'POST'])
@login_required
def add_chapter(subject_id):
    form = ChapterForm()
    if form.validate_on_submit():
        chapter = Chapter(name=form.name.data, description=form.description.data, subjectId=subject_id)
        db.session.add(chapter)
        db.session.commit()
        flash(f'Chapter {form.name.data} added successfully!', 'success')
        return redirect(url_for('main.add_chapter'))
    return render_template("add_chapter.html", form=form)

@main.route('/delete_chapter/<int:chapter_id>', methods=['GET', 'POST'])
@login_required
def delete_chapter(chapter_id):
    chapter = Chapter.query.get(chapter_id)
    db.session.delete(chapter)
    db.session.commit()
    flash(f'Chapter {chapter.name} deleted successfully!', 'success')
    return redirect(url_for('main.dashboard'))

@main.route('/edit_chapter/<int:chapter_id>', methods=['GET', 'POST'])
@login_required
def edit_chapter(chapter_id):
    chapter = Chapter.query.get(chapter_id)
    form = ChapterForm()
    if form.validate_on_submit():
        chapter.name = form.name.data
        chapter.description = form.description.data
        db.session.commit()
        flash(f'Chapter {form.name.data} edited successfully!', 'success')
        return redirect(url_for('main.dashboard'))
    elif request.method == 'GET':
        form.name.data = chapter.name
        form.description.data = chapter.description
    return render_template("edit_chapter.html", form=form)


@main.route('/add_quiz/<int:chapter_id>', methods=['GET', 'POST'])
@login_required
def add_quiz(chapter_id):
    form = QuizForm()
    if form.validate_on_submit():
        quiz = Quiz(chapter_id=chapter_id, date_of_quiz=form.date_of_quiz.data, duration=form.duration.data, remarks=form.remarks.data)
        db.session.add(quiz)
        db.session.commit()
        flash(f'Quiz added successfully!', 'success')
        return redirect(url_for('main.add_quiz'))
    return render_template("add_quiz.html", form=form)

@main.route('/add_question/<int:quiz_id>', methods=['GET', 'POST'])
@login_required
def add_question(quiz_id):
    form = QuestionForm()
    if form.validate_on_submit():
        question = Question(quiz_id=quiz_id, question_statement=form.question_statement.data, option1=form.option1.data, option2=form.option2.data, option3=form.option3.data, option4=form.option4.data, correct_option=form.correct_option.data)
        db.session.add(question)
        db.session.commit()
        flash(f'Question added successfully!', 'success')
        return redirect(url_for('main.add_question'))
    return render_template("add_question.html", form=form)

@main.route('/subjects/<int:subject_id>')
def subject(subject_id):
    chapters = Chapter.query.filter_by(subjectId=subject_id).all()
    subject = Subject.query.filter_by(id=subject_id).first()
    return render_template("subject.html",chapters=chapters,user_role=current_user.role,subject=subject)

@main.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))