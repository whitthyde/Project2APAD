#signup
from bookshelf import get_model
from bookshelf import crude, app
from flask import Blueprint, redirect, render_template, request, url_for
from .model_cloudsql import User, db, Event
from flask import Flask
from bookshelf import bcrypt
from flask_sqlalchemy import SQLAlchemy
# from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, current_user, logout_user, login_required
from bookshelf.forms import RegistrationForm, LoginForm
from flask import render_template, url_for, flash, redirect, request, jsonify,json




signu = Blueprint('signu', __name__)


@signu.route("/", methods=['GET', 'POST'])
def register():
    
    if request.user_agent.platform == "android":
        content = request.json
        first_name = content['firstname']
        last_name = content['lastname']
        useremail = content['email']
        password = content['password']
        user_name = content['username']


        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(username=user_name, firstname=first_name,lastname=last_name,email=useremail, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        return jsonify(result=useremail)
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
    if request.user_agent.platform == "android":
        logout_user()
        return jsonify(result="true")


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

@app.route("/account/androidevents/<username>/")
def myeventsandroid(username):
    user = User.query.filter_by(email=username).first()
    events = get_model().see_my_events(user)
    eventids = get_model().see_my_eventids(user)
    allevents = Event.query.all()
    myevents = []
    for event in allevents:
        for eventid in eventids:
            if eventid == event.id:
                myevents.append(event)

    ids, names, descriptions, dates,timeslots,listcurrentusers,listmaxusers,prices,venueids = [], [], [], [],[],[],[],[],[]
    for event in myevents:
        ids.append(event.id)
        names.append(event.eventname)
        descriptions.append(event.description)
        date_of_event = (event.day).strftime("%m/%d/%Y")
        dates.append(date_of_event)
        timeslots.append(event.timeslot)
        listcurrentusers.append(event.currentusers)
        listmaxusers.append(event.maxusers)
        pstring = str(event.price)
        prices.append(pstring)
        venueids.append(event.venue_id)


    events_list = [{"id": i, "eventname": e, "description": d,"date":da,"timeslot":t,"currentusers":cu,"maxusers":mu,"price":pr,"venueid":vid} for i, e,d,da,t,cu,mu,pr,vid in zip(ids, names, descriptions, dates,timeslots,listcurrentusers,listmaxusers,prices,venueids)]
    
    return json.dumps(events_list)


#Routes to the info and tutorial pages
@app.route("/info")
def infoindex():
    return render_template("info.html")

@app.route("/info/webtutorial")
def webtutorial():
    return render_template("webtutorial.html")

@app.route("/info/apptutorial")
def apptutorial():
    return render_template("AndroidTutorial.html")
@app.route("/info/aboutus")
def aboutus():
    return render_template("aboutus.html")
