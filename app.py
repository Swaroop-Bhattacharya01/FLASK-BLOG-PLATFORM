
from flask import Flask,render_template,url_for,flash,redirect
from forms import RegistrationForm,LoginForm #we import the forms we created in forms.py so that we can use them in out routes
from flask_sqlalchemy import SQLAlchemy


app=Flask(__name__)


app.config['SECRET_KEY']='bbe58e27522d0f25802798769c99e8b1' #config is used to set secret key for forms because it is required for security purposes

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'
#creating a database instance
db=SQLAlchemy(app)

from models import User,Post #the reason this is after the db instance is created is because models.py uses the db instance to create the models



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