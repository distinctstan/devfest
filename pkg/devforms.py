from flask_wtf import FlaskForm

from wtforms import StringField,SubmitField,EmailField,PasswordField,TextAreaField
from wtforms.validators import DataRequired,Email,EqualTo,Length

from flask_wtf.file import FileField, FileAllowed,FileRequired


class RegistrationForm(FlaskForm):
    firstname=StringField("Firstname:", validators=[DataRequired(message='Supply Your Firstname')])
    lastname=StringField("Lastname:", validators=[DataRequired(message='Supply Your Lastname')])

    email=EmailField("Email:",validators=[Email(message='Email is not valid')])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_pass = PasswordField("Confirm Password", validators=[EqualTo("password")])

    btnsubmit = SubmitField("Register")

class LoginForm(FlaskForm):
    email=EmailField("Email:",validators=[Email(message='Email is not valid')])
    password = PasswordField("Password", validators=[DataRequired()])
    btnlogin = SubmitField("Login")

class ConversationForm(FlaskForm):
    title=StringField("Title:",validators=[DataRequired(message='Specify the Title')])
    content = TextAreaField("Content", validators=[DataRequired(),Length(max=200)])
    btnsubmit = SubmitField("Submit Form")

class ProfileForm(FlaskForm):
    firstname=StringField("Firstname:",validators=[DataRequired(message='Specify the Firstname')])
    
    lastname=StringField("Lastname:",validators=[DataRequired(message='Specify the Lastname')])
    
    summary = TextAreaField("User Bio", validators=[DataRequired(),Length(max=200)])

    btnsubmit = SubmitField("Submit Form")

class PhotoForm(FlaskForm):
    photo = FileField(validators=[FileRequired(), FileAllowed(["jpg","png","jpeg"],message="Invalid File type") ])
    btn = SubmitField("Upload File")