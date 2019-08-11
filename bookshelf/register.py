#signup
from bookshelf import get_model
from bookshelf import crude, app
from flask import Blueprint, redirect, render_template, request, url_for
from .model_cloudsql import User, db
from flask import Flask
from bookshelf import bcrypt
from flask_sqlalchemy import SQLAlchemy
# from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, current_user, logout_user, login_required
from bookshelf.forms import RegistrationForm, LoginForm
from flask import render_template, url_for, flash, redirect, request




signu = Blueprint('signu', __name__)


@signu.route("/", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('eventslist.html'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, firstname=form.firstname.data,lastname=form.lastname.data,email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('lgin.login'))
    return render_template('signup.html', title='Register', form=form)

@app.route("/logout")
def log_out():
    logout_user()
    return redirect(url_for('crude.eventslist'))

@app.route("/account")
@login_required
def account():
    return render_template('account.html', title='Account')

@app.route("/account/myevents")
@login_required
def myevents():
    user = current_user
    events = get_model().see_my_events(current_user)
    eventids = get_model().see_my_eventids(current_user)
    return render_template('myevents.html', events=events,eventids=eventids)
