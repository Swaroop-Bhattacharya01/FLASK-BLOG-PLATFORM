from flask import render_template,url_for,flash,redirect,request
from app import app,db,bcrypt
from app.forms import RegistrationForm,LoginForm ,UpdateForm#we import the forms we created in forms.py so that we can use them in out routes

from app.models import User,Post #the reason this is after the db instance is created is because models.py uses the db instance to create the models
from flask_login import login_user,current_user,logout_user,login_required




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
    if current_user.is_authenticated:
       return redirect(url_for('home'))
    form=RegistrationForm()
    if form.validate_on_submit():
        hashed_pw= bcrypt.generate_password_hash(form.password.data).decode('utf-8') #this is to validate the user password by hashing it for security purposes and the use of utf 8 is to convert the hashed password from bytes to string
        user=User(username=form.username.data,email=form.email.data,password=hashed_pw) #we create a user instance with the data from the form and add it to the db
        db.session.add(user)
        db.session.commit()
        flash('your account has been created','success') #success is a category for the flash message
        return redirect(url_for('login'))
    return render_template('register.html',title='Register',form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form=LoginForm()
    if form.validate_on_submit():
       user=User.query.filter_by(email=form.email.data).first() 
       if user and bcrypt.check_password_hash(user.password,form.password.data):#simultaneously checks if user exists and if the password matches
            login_user(user,remember=form.remember.data)
            next_page=request.args.get('next') #this is to redirect the user to the page they are trying to access before login
            return redirect(next_page) if next_page else redirect(url_for('home'))
       else:
            flash('Login unsuccessful pls check email and password','danger')
    return render_template('login.html',title='Login',form=form)

@app.route('/Logout')
def logout():
   logout_user()
   return redirect(url_for('home'))

@app.route('/account',methods=['GET','POST'])
@login_required
def account():
    form=UpdateForm()
    if form.validate_on_submit():
        current_user.username=form.username.data
        current_user.email=form.email.data
        db.session.commit()
        flash('Your account has beeen updated','success')
        return redirect(url_for('account'))
    elif request.method=='GET':  
        form.username.data=current_user.username
        form.email.data=current_user.email

    image_file=url_for('static',filename='profile_pics/' + current_user.image_file)
    return render_template('account.html',title='Account',image_file=image_file,form=form) 