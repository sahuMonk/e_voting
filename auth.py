from flask import Blueprint, render_template, redirect, url_for, request, flash
from models import UserModel,db
from werkzeug.security import generate_password_hash, check_password_hash
import validators
import string
from flask_login import login_user, login_required, logout_user

auth = Blueprint('auth', __name__)


# login page
@auth.route('/login')
def login():
    return render_template("login.html")


@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')

    user = UserModel.query.filter_by(email=email).first()

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login'))

    login_user(user)
    return redirect(url_for('profile'))


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

# sing up page
@auth.route('/register')
def register():
    return render_template("register.html")


@auth.route('/register', methods=['POST'])
def register_post():
    rollno = request.form.get('rollno')
    email = request.form.get('email')
    name = request.form.get('name')
    password1 = request.form.get('password1')
    password2 = request.form.get('password2')

    user = UserModel.query.filter_by(email=email).first()  # if this returns a user, email already exists in db
    roll_no = UserModel.query.filter_by(roll_num=rollno).first()

    error = False
    # if a user or roll no is found, we want to redirect to signup page
    if user:
        flash('Email address already exists.', 'error')
        error = True

    if roll_no:
        flash('Roll number already exists', 'error')
        error = True

    if password1 != password2:  # if passwords do not match, redirect
        flash('Passwords do not match. Please try again.', 'error')
        error = True

    if (len(password1) or len(password2)) < 8:
        flash('Password too short. Should be atleast 8 characters.', 'error')
        error = True

    # to validate the email
    if not validators.email(email):
        flash('Enter a valid email', 'error')
        error = True

    # name can contain alphabets
    if not set(name).issubset(string.ascii_letters + " "):
        flash('Name can only contain alphabets.', 'error')
        error = True

    # if any error then redirect to signup page
    if error:
        return redirect(url_for('auth.register'))

    # if no error then add user to UserModel
    else:
        new_user = UserModel(roll_num=rollno, email=email, name=name,
                             password=generate_password_hash(password1, method='sha256'))
        db.session.add(new_user)
        db.session.commit()
        flash('User successfully registered.', 'success')
        return redirect(url_for('auth.register'))
