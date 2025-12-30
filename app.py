from datetime import datetime
from flask import Flask,render_template,url_for,flash,redirect
from forms import RegistrationForm,LoginForm #we import the forms we created in forms.py so that we can use them in out routes
from flask_sqlalchemy import SQLAlchemy
app=Flask(__name__)


app.config['SECRET_KEY']='bbe58e27522d0f25802798769c99e8b1' #config is used to set secret key for forms because it is required for security purposes

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'
#creating a database instance
db=SQLAlchemy(app)

class User(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(20),unique=True,nullable=False)
    email=db.Column(db.String(120),unique=True,nullable=False)
    image_file=db.Column(db.String(20),nullable=False,default='default.jpeg')
    password=db.Column(db.String(60),nullable=False)
    posts=db.relationship('Post',backref='author',lazy=True) # we use this to create relationship between user and post like one to many relationship and the backref is used to add a column tto the post table which will reference the user who created the post and lazy is used to tell sqlalchemy when to load the data from the database
    
    
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
posts=[
    {
        'author':'corey schafer',
        'title':'first post',
        'content':'first post content',
        'date_posted':'april 20,2018'
    },
    {
        'author':'jane doe',
        'title':'second post',
        'content':'second post content',
        'date_posted':'april 21,2018'
    }

]
@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html',posts=posts)

@app.route('/about')
def about():
    return render_template('about.html', title='About')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form=RegistrationForm()
    if form.validate_on_submit():
        flash(f'account created for {form.username.data}','success') #success is a category for the flash message
        return redirect(url_for('home'))
    return render_template('register.html',title='Register',form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        if form.email.data=='admin@blog.com' and form.password.data=='password':
            flash(f'you have been succesfully logged in','success')
            return redirect(url_for('home'))
        else:
            flash('Login unsuccessful pls check username and password','danger')
    return render_template('login.html',title='Login',form=form)


if __name__=="__main__":
    app.run(debug=True)