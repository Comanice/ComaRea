from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from website.models import User, db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from email_validator import validate_email, EmailNotValidError
import re


auth = Blueprint('auth', __name__)


# Create a route decorator
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if session.get('_404_redirect'):
            # Clear the session variable
            session.pop('_404_redirect', None)
            # Redirect the user to the sign-up page
            return redirect(url_for('auth.login'))

        user = User.query.filter_by(username=username).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')  # Typo corrected here
        else:
            flash('This username does not exist.', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.home'))


def validate_password(password):
    if len(password) < 7:
        return False, "Password must be at least 7 characters long."
    if not any(char.isupper() for char in password):
        return False, "Password must include at least one capital letter."
    if not any(char.isdigit() for char in password):
        return False, "Password must include at least one number."
    if not any(char in "!@#$%^&*()-_=+{}[];:'\"<>,.?/" for char in password):
        return False, "Password must include at least one special character."

    return True, "Password is valid."


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')

        if session.get('_404_redirect'):
            # Clear the session variable
            session.pop('_404_redirect', None)
            # Redirect the user to the sign-up page
            return redirect(url_for('auth.sign_up'))

        if not email:
            flash('Email address is required.', category='error')
            return render_template("sign_up.html", user=current_user)

        user = User.query.filter_by(username=username).first()
        user_email = User.query.filter_by(email=email).first()

        try:
            validate_email(email)
        except EmailNotValidError:
            flash('Invalid email address.', category='error')
            return render_template("sign_up.html", user=current_user)

        if user:
            flash('Username already exists.', category='error')
            return render_template("sign_up.html", user=current_user)
        elif user_email:
            flash('There is already an account with this Email address.', category='error')
            return render_template("sign_up.html", user=current_user)
        elif len(username) < 2 or len(username) > 100:
            flash('Usernames must have more than 1 and less than 100 characters.', category='error')

        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        if password1 != password2:
            flash('Passwords do not match.', category='error')
            return render_template("sign_up.html", user=current_user)
        elif not validate_password(password1)[0]:
            flash(validate_password(password1)[1], category='error')
            return render_template("sign_up.html", user=current_user)
        else:
            new_user = User(email=email,
                            username=username,
                            password=generate_password_hash(password1,
                            method='pbkdf2:sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)
