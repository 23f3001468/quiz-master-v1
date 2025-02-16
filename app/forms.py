from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")

class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=2, max=20)])
    fullName = StringField("Full Name", validators=[DataRequired()])
    qualification = StringField("Qualification", validators=[DataRequired()])
    date_of_birth= StringField("Date of Birth", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField("Sign Up")

class SubjectForm(FlaskForm):
    name = StringField("Subject Name", validators=[DataRequired()])
    description = TextAreaField("Description", validators=[DataRequired()])
    submit = SubmitField("Add Subject")

class ChapterForm(FlaskForm):
    name = StringField("Chapter Name", validators=[DataRequired()])
    description = TextAreaField("Description", validators=[DataRequired()])
    submit = SubmitField("Add Chapter")

class QuizForm(FlaskForm):
    date_of_quiz = StringField("Date of Quiz", validators=[DataRequired()])
    duration = StringField("Duration", validators=[DataRequired()])
    remarks = TextAreaField("Remarks")
    submit = SubmitField("Add Quiz")

class QuestionForm(FlaskForm):
    question = TextAreaField("Question", validators=[DataRequired()])
    option1 = StringField("Option 1", validators=[DataRequired()])
    option2 = StringField("Option 2", validators=[DataRequired()])
    option3 = StringField("Option 3", validators=[DataRequired()])
    option4 = StringField("Option 4", validators=[DataRequired()])
    correct_option = SelectField("Correct Option", choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')], validators=[DataRequired()])
    submit = SubmitField("Add Question")