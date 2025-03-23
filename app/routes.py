# app/routes.py
from flask import Blueprint, render_template, redirect, url_for, flash,session, request
from . import db, bcrypt
from .models import User, Subject, Chapter, Quiz, Question, Score
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
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        form.date_of_birth.data = datetime.strptime(form.date_of_birth.data, '%d/%m/%Y').date()
        user = User(username=form.username.data, email=form.email.data, password=hashed_password, fullName=form.fullName.data, date_of_birth=form.date_of_birth.data,role="user")
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
    chapters=  Chapter.query.filter_by(subjectId=subject_id).all()
    for chapter in chapters:
        db.session.delete(chapter)
        db.session.commit()
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

@main.route('/subjects/<int:subject_id>')
def subject(subject_id):
    chapters = Chapter.query.filter_by(subjectId=subject_id).all()
    subject = Subject.query.filter_by(id=subject_id).first()
    return render_template("subject.html",chapters=chapters,user_role=current_user.role,subject=subject)

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
        return redirect(url_for('main.subject',subject_id=subject_id))
    return render_template("add_chapter.html", form=form,subject_id=subject_id)

@main.route('/delete_chapter/<int:chapter_id>', methods=['GET', 'POST'])
@login_required
def delete_chapter(chapter_id):
    chapter = Chapter.query.get(chapter_id)
    db.session.delete(chapter)
    db.session.commit()
    flash(f'Chapter {chapter.name} deleted successfully!', 'success')
    return redirect(url_for('main.subject',subject_id=chapter.subjectId))

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
        return redirect(url_for('main.subject',subject_id=chapter.subjectId))
    elif request.method == 'GET':
        form.name.data = chapter.name
        form.description.data = chapter.description
    return render_template("edit_chapter.html", form=form,chapter=chapter)

@main.route('/chapters/<int:chapter_id>')
def chapter(chapter_id):
    quizzes = Quiz.query.filter_by(chapter_id=chapter_id).all()
    chapter = Chapter.query.filter_by(id=chapter_id).first()
    return render_template("chapter.html",quizzes=quizzes,user_role=current_user.role,chapter=chapter,subject_id=chapter.subjectId)

#quiz routes
@main.route('/add_quiz/<int:chapter_id>', methods=['GET', 'POST'])
@login_required
def add_quiz(chapter_id):
    form = QuizForm()
    if form.validate_on_submit():
        quiz = Quiz(name=form.name.data,chapter_id=chapter_id, remarks=form.remarks.data)
        db.session.add(quiz)
        db.session.commit()
        flash(f'Quiz added successfully!', 'success')
        return redirect(url_for('main.chapter', chapter_id=chapter_id))
    return render_template("add_quiz.html", form=form,chapter_id=chapter_id)

@main.route('/edit_quiz/<int:quiz_id>',methods=['GET','POST'])
@login_required
def edit_quiz(quiz_id):
    form=QuizForm()
    quiz=Quiz.query.get(quiz_id)
    if form.validate_on_submit():
        quiz.name=form.name.data
        quiz.remarks=form.remarks.data
        db.session.commit()
        flash(f'Quiz edited successfully!','success')
        return redirect(url_for('main.chapter',chapter_id=quiz.chapter_id))
    elif request.method=='GET':
        form.name.data=quiz.name
        form.remarks.data=quiz.remarks
    return render_template("edit_quiz.html",form=form,quiz=quiz)

@main.route('/delete_quiz/<int:quiz_id>', methods=['GET', 'POST'])
@login_required
def delete_quiz(quiz_id):
    quiz = Quiz.query.get(quiz_id)
    db.session.delete(quiz)
    db.session.commit()
    flash(f'Quiz deleted successfully!', 'success')
    return redirect(url_for('main.chapter',chapter_id=quiz.chapter_id))

@main.route('/quiz/<int:quiz_id>')
def quiz(quiz_id):
    questions = Question.query.filter_by(quiz_id=quiz_id).all()
    quiz = Quiz.query.filter_by(id=quiz_id).first()
    return render_template("quiz.html",questions=questions,user_role=current_user.role,quiz=quiz)

@main.route('/submit_quiz/<int:quiz_id>', methods=['POST'])
@login_required
def submit_quiz(quiz_id):
    questions = Question.query.filter_by(quiz_id=quiz_id).all()
    score = 0
    total = len(questions)
    correct_answers = []

    for question in questions:
        selected = request.form.get(f'answer_{question.id}')
        if selected == question.correct_option:
            score += 1
        correct_answers.append({'question': question.question_statement, 'correct_option': getattr(question, f'option{question.correct_option}')})

    new_score = Score(user_id=current_user.id, quiz_id=quiz_id, total_scored=score)
    db.session.add(new_score)
    db.session.commit()

    return render_template('score.html', score=score, total=total, correct_answers=correct_answers)


#question routes
@main.route('/add_question/<int:quiz_id>', methods=['GET', 'POST'])
@login_required
def add_question(quiz_id):
    if current_user.role != 'admin':
        return "Unauthorized", 403

    quiz = Quiz.query.get_or_404(quiz_id)
    form = QuestionForm()

    if form.validate_on_submit():
        new_question = Question(
            quiz_id=quiz_id,
            question_statement=form.question_statement.data,
            option1=form.option1.data,
            option2=form.option2.data,
            option3=form.option3.data,
            option4=form.option4.data,
            correct_option=form.correct_option.data
        )
        db.session.add(new_question)
        db.session.commit()
        return redirect(url_for('main.quiz', quiz_id=quiz_id))

    return render_template('add_question.html', form=form, quiz=quiz)

@main.route('/edit_question/<int:question_id>', methods=['GET', 'POST'])
@login_required
def edit_question(question_id):
    if current_user.role != 'admin':
        return "Unauthorized", 403

    question = Question.query.get_or_404(question_id)
    form = QuestionForm(obj=question)

    if form.validate_on_submit():
        question.question_statement = form.question_statement.data
        question.option1 = form.option1.data
        question.option2 = form.option2.data
        question.option3 = form.option3.data
        question.option4 = form.option4.data
        question.correct_option = form.correct_option.data
        db.session.commit()
        return redirect(url_for('main.quiz', quiz_id=question.quiz_id))

    return render_template('edit_question.html', form=form, question=question)


@main.route('/delete_question/<int:question_id>')
@login_required
def delete_question(question_id):
    if current_user.role != 'admin':
        return "Unauthorized", 403

    question = Question.query.get_or_404(question_id)
    quiz_id = question.quiz_id
    db.session.delete(question)
    db.session.commit()
    return redirect(url_for('main.quiz', quiz_id=quiz_id))

#score route
@main.route('/my_scores')
@login_required
def my_scores():
    scores = Score.query.filter_by(user_id=current_user.id).join(Quiz, Quiz.id == Score.quiz_id).add_columns(Quiz.name, Score.total_scored, Score.time_stamp_of_attempt).all()
    return render_template('my_scores.html', scores=scores)



@main.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))