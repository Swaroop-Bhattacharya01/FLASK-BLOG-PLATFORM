from flask_wtf import FlaskForm
from wtforms import StringField ,PasswordField ,SubmitField,BooleanField#we use wtforms to create form fields
from wtforms.validators import DataRequired,Length,Email,EqualTo
class RegistrationForm(FlaskForm):
    username=StringField('Username',validators=[DataRequired(),Length(min=2,max=20)])
    email=StringField('Email',validators=[DataRequired(),Email()])
    password=PasswordField('Password',validators=[DataRequired()])
    confirm_password=PasswordField('Confirm Password',validators=[DataRequired(),EqualTo('password')])
    submit=SubmitField('sign up')

class LoginForm(FlaskForm):
    email=StringField('Email',validators=[DataRequired(),Email()])
    password=PasswordField('Password',validators=[DataRequired()])
    remember=BooleanField('remember me')
    submit=SubmitField('Login')