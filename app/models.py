from . import db
from flask_login import UserMixin
from datetime import datetime

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    fullName = db.Column(db.String(100))
    qualification = db.Column(db.String(100))
    date_of_birth = db.Column(db.DateTime, default=datetime.utcnow)
    role = db.Column(db.String(100), default='student')

class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String(100), unique=True)
    description = db.Column(db.String(100))

class Chapter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String(100), unique=True)
    description = db.Column(db.String(100))
    subjectId = db.Column(db.Integer, db.ForeignKey('subject.id'),nullable=False)

class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapter.id'), nullable=False)
    date_of_quiz = db.Column(db.DateTime, default=datetime.utcnow, nullable=False) 
    duration = db.Column(db.String(5), nullable=False)
    remarks = db.Column(db.String(255), nullable=True) 

class Question(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    question_statement= db.Column(db.String(255), nullable=False)
    option1= db.Column(db.String(255), nullable=False)
    option2= db.Column(db.String(255), nullable=False)
    option3= db.Column(db.String(255), nullable=False)
    option4= db.Column(db.String(255), nullable=False)
    correct_option= db.Column(db.String(255), nullable=False)

class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    total_scored = db.Column(db.Integer, nullable=False)
    time_stamp_of_attempt = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
