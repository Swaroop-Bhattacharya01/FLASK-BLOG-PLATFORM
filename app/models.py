
from datetime import datetime
#from app import db  this is wrong because it will create circular import
from itsdangerous import URLSafeTimedSerializer as Serializer
#from __main__ import db
from app import db,login_manager,app #app is imported to use the secret key
from flask_login import UserMixin #user mixin provides default implementations for the methods that flask login expects user objects to have

@login_manager.user_loader  #thsi is a callback function that flask login uses to reload the user object from th userid stored inn the session
def load_user(user_id):
     return User.query.get(int(user_id))

class User(db.Model,UserMixin):#usermixin is used to add flask login functionality to the suer model
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(20),unique=True,nullable=False)
    email=db.Column(db.String(120),unique=True,nullable=False)
    image_file=db.Column(db.String(20),nullable=False,default='default.jpeg')
    password=db.Column(db.String(60),nullable=False)
    posts=db.relationship('Post',backref='author',lazy=True) # we use this to create relationship between user and post like one to many relationship and the backref is used to add a column tto the post table which will reference the user who created the post and lazy is used to tell sqlalchemy when to load the data from the database
    
    def get_reset_token(self):
        s = Serializer(app.config['SECRET_KEY'])
        return s.dumps({'user_id': self.id})
    
    @staticmethod #this is used because the method does not take self as arg
    def verify_reset_token(token,expires_sec=180):
        s=Serializer(app.config['SECRET_KEY'])
        try:
            user_id=s.loads(token,max_age=expires_sec)['user_id']
        except:
            return None
        return User.query.get(user_id)
    def __repr__(self):
        return f"user('{self.username},'{self.email}','{self.image_file}')"
    
class Post(db.Model):
        id=db.Column(db.Integer,primary_key=True)
        title=db.Column(db.String(100),nullable=False)
        date_posted=db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
        content=db.Column(db.Text,nullable=False)
        user_id=db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)

        def __repr__(self):
            return f"Post('{self.title}','{self.date_posted}')"
        
     