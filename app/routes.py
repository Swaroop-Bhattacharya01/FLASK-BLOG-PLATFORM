import os
import secrets
from flask import abort, render_template,url_for,flash,redirect,request
from app import app,db,bcrypt
from app.forms import RegistrationForm,LoginForm ,UpdateForm,PostForm#we import the forms we created in forms.py so that we can use them in out routes

from app.models import User,Post #the reason this is after the db instance is created is because models.py uses the db instance to create the models
from flask_login import login_user,current_user,logout_user,login_required


@app.route('/')
@app.route('/home')
def home():
    posts=Post.query.all()
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


def save_picture(form_picture):
    random_hex=secrets.token_hex(8) #hex is taken to generate a random filename for the picture
    _,f_ext=os.path.splitext(form_picture.filename)# the reason for the _ is because we dont need the first value returned by splitext which is the path and _ext is the extension
    picture_fn=random_hex+f_ext  #basically we r creating a unique filename for the picture by combining the hex and the file extension
    picture_path=os.path.join(app.root_path,'static/profile_pics',picture_fn)
    form_picture.save(picture_path)

    return picture_fn

@app.route('/account',methods=['GET','POST'])
@login_required
def account():
    form=UpdateForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file=save_picture(form.picture.data)
            current_user.image_file=picture_file
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

@app.route('/post/new',methods=['GET','POST'])
@login_required
def new_post():
    form=PostForm()
    if form.validate_on_submit():
        post=Post(title=form.title.data,content=form.content.data,author=current_user) 
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created','success')
        return redirect(url_for('home'))
    return render_template('create_post.html',title='NEW POST',form=form,legend='NEW POST')

@app.route('/post/<int:post_id>')
def post(post_id):
    post=Post.query.get_or_404(post_id)
    return render_template('post.html',title=post.title,post=post)

@app.route('/post/<int:post_id>/update',methods=['GET','POST'])
@login_required
def update_post(post_id):
    post=Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form =PostForm()
    if form.validate_on_submit():
        post.title=form.title.data
        post.content=form.content.data
        db.session.commit()
        flash('Your post has been upated','success')
        return redirect(url_for('post',post_id=post.id))
    elif request.method=='GET':
        form.title.data=post.title
        form.content.data=post.content
    return render_template('create_post.html',title='UPDATE POST',form=form,legend='UPDATE POST')

@app.route('/post/<int:post_id>/delete',methods=['POST'])
@login_required
def delete_post(post_id):
    post=Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted','success')
    return redirect(url_for('home'))