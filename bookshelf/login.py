from bookshelf import get_model
from bookshelf import crude
from flask import Blueprint, redirect, render_template, request, url_for
from .model_cloudsql import User, db
from flask import Flask
from bookshelf import bcrypt
from flask_sqlalchemy import SQLAlchemy
# from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, current_user, logout_user, login_required
from bookshelf.forms import RegistrationForm, LoginForm
from flask import render_template, url_for, flash, redirect, request



lgin = Blueprint('lgin', __name__)



@lgin.route("/", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return render_template('eventslist.html')
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else render_template('eventslist.html')
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)
