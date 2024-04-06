from flask import Blueprint, render_template, url_for, request, redirect
from . import db
from .models import Users
from passlib.hash import sha256_crypt
from flask_login import login_user, logout_user, login_required

auth = Blueprint("auth", __name__)

# route for sign up
@auth.route("/signup")
def signup():
    return render_template("signup.html")

# route for post sign up
@auth.route("/signup", methods=['POST'])
def signup_post():
    # get the form values
    name = request.form.get("name")
    email = request.form.get("email")
    password = request.form.get("password")
    
    # filter the user 
    user = Users.query.filter_by(email=email).first()
    
    # check if already exits
    if user:
        # redirect to sign up again
        return redirect(url_for('auth.singup'))
    else:
        '''
        1.  Hash Generation:
        *   To HASH: sha256_crypt.hash("your_password").
        *   To HASH: sha256_crypt.encrypt("your_password").
        *   RESULT: '$5$rounds=80000$wnsT7Yr92oJoP28r$cKhJImk5mfuSKV9b3mumNzlbstFUplKtQXXMo4G6Ep5'.
        '''
        
        # hash the password
        hashed_password = sha256_crypt.hash(password)
        
        # create a new user or Object of Users class
        new_user = Users(name=name, email=email, password=hashed_password)
        
        # add the suser to the table
        db.session.add(new_user)
        
        # commit it 
        db.session.commit()
    # redirect to login page
    return redirect(url_for('auth.login', Name=name))


# route for log in
@auth.route("/login")
def login():
    return render_template("login.html")

# reute for post login form
@auth.route("/login",methods=["POST"])
def login_post():
    # get the email and password
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False
    
    # filter the user 
    user = Users.query.filter_by(email=email).first()
    '''
    2.  Password Verification:
        *   To verify a password: sha256_crypt.verify("user_input_password", hashed_password).
        *   It will return True if the password matches the hash, and False otherwise.
    '''
    is_valid = sha256_crypt.verify(password, user.password)
    
    # if user not exists
    if not is_valid or not user:
        # redirect to login page for trying again
        return redirect(url_for('auth.login'))
    
    # login the User to website and redirect to profile page
    login_user(user, remember=remember)
    return redirect(url_for('main.profile'))

# route for logout
@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))