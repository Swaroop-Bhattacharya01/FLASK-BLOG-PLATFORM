from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager #we use flask login to manage user sessions

app=Flask(__name__)


app.config['SECRET_KEY']='bbe58e27522d0f25802798769c99e8b1' #config is used to set secret key for forms because it is required for security purposes

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'
#creating a database instance
db=SQLAlchemy(app)

bcrypt=Bcrypt(app)
login_manager=LoginManager(app)

from app import routes  #to avoid circular import we import routes at the end after creating the app instance
