from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, Note
from werkzeug.security import generate_password_hash, check_password_hash
from website import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in Successfully', 'success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect Password, try again!', 'danger')
                return redirect(url_for('auth.login'))
        else:
            flash('Email does not exist', 'danger')
            return redirect(url_for('auth.login'))


    return render_template('login.html', title='Login', user=current_user)
     
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/register',  methods = ['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstname')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        
        user = User.query.filter_by(email=email).first()
        if user:
            flash('This email already exist', 'danger')
            return redirect(url_for('auth.register'))
        elif len(email) < 4:
            flash('Email must be greater than 3 characters', 'danger')
            return redirect(url_for('auth.register'))
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character', 'danger')
            return redirect(url_for('auth.register'))
        elif password1 != password2:
            flash('Oops! Passwords dont match', 'danger')
            return redirect(url_for('auth.register'))
        elif len(password1) < 7:
            flash('Password must be atleast 7 characters ', 'danger')
            return redirect(url_for('auth.register'))
        else:
            new_user = User(email= email, first_name=first_name, password=generate_password_hash(password1, method='sha256') )
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account Created!', 'success')
            return redirect(url_for('views.home'))
        
    return render_template('register.html', title='Register', user=current_user)

