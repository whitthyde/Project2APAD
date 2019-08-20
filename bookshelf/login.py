import os
from bookshelf import get_model
from bookshelf import crude
from flask import Blueprint, redirect, render_template, request, url_for
from .model_cloudsql import User, db
from flask import Flask
from bookshelf import bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_user, current_user, logout_user, login_required
from bookshelf.forms import RegistrationForm, LoginForm
import urllib
from flask import render_template, url_for, flash, redirect, request, jsonify, request, json


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
            return redirect(next_page) if next_page else redirect(url_for('crude.eventslist'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


#https://<project-id>/appspot.com/auth?username=<username>&password=<password>
@lgin.route("/auth/<username>/<password>", methods=['GET'])
def auth(username,password):
    user = User.query.filter_by(email=username).first()
    user_id = user.get_id()
    userdict = {1:user.email,2: user.email}
    allusers = User.query.all()
    if user and bcrypt.check_password_hash(user.password, password):
        login_user(user)
        return jsonify(email=user.email,password=password,result="success",userid=user_id)
    else:
        return jsonify(result="false")
