import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager #we use flask login to manage user sessions
from flask_mail import Mail

app=Flask(__name__)


app.config['SECRET_KEY']='bbe58e27522d0f25802798769c99e8b1' #config is used to set secret key for forms because it is required for security purposes

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'
#creating a database instance
db=SQLAlchemy(app)

bcrypt=Bcrypt(app)
login_manager=LoginManager(app)
login_manager.login_view='login'
login_manager.login_message_category='info'#info represent the category of flask message in bootstrap which is blue
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT']=587
app.config['MAIL_USE_TLS']=True
app.config['MAIL_USERNAME']=os.environ.get('EMAIL_USER')
app.config['MAIL_PASSWORD']=os.environ.get('EMAIL_PASS')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('EMAIL_USER')#we do this to set a defualt sender so that we can avoid specifying the sender email

if not app.config['MAIL_USERNAME'] or not app.config['MAIL_PASSWORD']:
    raise RuntimeError("Email credentials not set in environment variables")

mail=Mail(app)

from app import routes  #to avoid circular import we import routes at the end after creating the app instance
