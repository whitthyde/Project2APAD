#This file is the crud methods for the events
from flask import Flask, flash
from flask_sqlalchemy import SQLAlchemy
from bookshelf import login_manager
from flask_login import UserMixin
import os
import urllib
from flask import Flask, render_template, request, redirect
import pymysql
from bookshelf import model_cloudsql
from bookshelf import get_model
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import Blueprint, redirect, render_template, request, url_for
import os
import urllib
from flask import Flask, render_template, request, redirect, jsonify, json
import pymysql
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy import inspect
from flask_login import login_user, current_user, logout_user, login_required
from .model_cloudsql import Event, db, User, from_sql,builtin_list, Venue
import datetime
from datetime import date, datetime


crude = Blueprint('crude', __name__)





####################################################################################################################################################################################################################################################################################################################
################################################################################################################################################################################################################################################################################################################################################################################################
#######################################################             ROUTES               ######################################################################################################################################################################################################################################################################################################
################################################################################################################################################################################################################################################################
 


@crude.route('/')
def eventslist():
    if request.user_agent.platform == "android":
        # query = Event.query
        # events = builtin_list(map(from_sql, query.all()))
        query2 = Event.query.all()

        ids, names, descriptions, dates,timeslots,listcurrentusers,listmaxusers,prices,venueids = [], [], [], [],[],[],[],[],[]
        for event in query2:
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
    token = request.args.get('page_token', None)
    if token:
        token = token.encode('utf-8')

    events, next_page_token = get_model().events_list(cursor=token)
    return render_template(
        "eventslist.html",
        events=events,
        next_page_token=next_page_token)


    



@crude.route('/<id>')
def viewevents(id):
    event = get_model().readevent(id)
    return render_template("eventsview.html", event=event)


# [START add]
@crude.route('/add', methods=['GET', 'POST'])
def addevents():
    if request.user_agent.platform == "android":
        content = request.json
        event_name = content['eventname']
        host_name = content['hostname']
        description = content['description']
        day = content['day']
        date = datetime.strptime(day, '%m-%d-%Y')
        ts = content['timeslot']
        timeslot = int(ts)
        cu = content['currentusers']
        current_users = int(cu)
        mu = content['maxusers']
        max_users = int(mu)
        pri = content['price']
        price= float(pri)
        vid = content['venueid']
        venue_id = int(vid)

        event = Event(hostname=host_name,eventname=event_name,description =description,day=date,timeslot=timeslot, currentusers=current_users,maxusers=max_users,price=price,venue_id=venue_id)
        db.session.add(event)
        db.session.commit()
        return jsonify(result=event_name)
    if request.method == 'POST':
        data = request.form.to_dict(flat=True)

        event = get_model().createevent(data)

        return redirect(url_for('.viewevents', id=event['id']))

    return render_template("eventsform.html", action="Add", event={})
# [END add]




@crude.route('/<id>/edit', methods=['GET', 'POST'])
def editevents(id):
    event = get_model().readevent(id)

    if request.method == 'POST':
        data = request.form.to_dict(flat=True)

        event = get_model().updateevent(data, id)

        return redirect(url_for('.viewevents', id=event['id']))

    return render_template("eventsform.html", action="Edit", event=event)



@crude.route('/<id>/join')
def joinevent(id):
    event_id = id
    user_id = current_user.get_id()
    if get_model().is_event_full(id):
        flash('Sorry! This event is already full.','danger')
        error = 'Sorry! This event is already full.'
        return redirect(url_for('.eventslist'))
    get_model().join_event(event_id,user_id)
    ####ABOVE THIS WORKS    
    return redirect(url_for('.viewevents', id=id))

@crude.route('/joinandroid', methods=['POST'])
def joinandroid():
    if request.user_agent.platform == "android":
        content = request.json
        eid = content['eventid']
        ename = content['eventname']
        user_email = content['email']
        if eid == '' or eid is None:
            event_id = get_model().eventgetid(ename)
        else:
            event_id = int(eid)
        user = User.query.filter_by(email=user_email).first()
        user_id=user.id
    if get_model().is_event_full(event_id):
        return jsonify(result="false")
    get_model().join_event(event_id,user_id)
    ####ABOVE THIS WORKS    
    return jsonify(result=ename,userid=user_id)


@crude.route('/<id>/delete')
def deleteevents(id):
    get_model().deleteevents(id)
    return redirect(url_for('.eventslist'))

@crude.route('/search', methods=['GET', 'POST'])
def eventsearch():
    if request.user_agent.platform == "android":
        content = request.json
        vid = content['venueid']
        venue_id = int(vid)
        ename = content['eventname']
        date = content['day']
        day = datetime.strptime(day, '%m-%d-%y')
        ts = content['timeslot']
        timeslot = int(ts)
        if timeslot == '':
            events = get_model().eventsearch(day,venue_id)
        else:
            events = get_model().eventsearch(day,venue_id,timeslot)
        ids, names, descriptions, dates,timeslots,listcurrentusers,listmaxusers,prices,venueids = [], [], [], [],[],[],[],[],[]
        for event in events:
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


    token = request.args.get('page_token', None)
    if token:
        token = token.encode('utf-8')
    if request.method == 'POST':
        day = request.form['day']
        venue_id = request.form['venue_id']
        timeslot = request.form['timeslot']
        if timeslot == '':
            events = get_model().eventsearch(day,venue_id)
        else:
            events = get_model().eventsearch(day,venue_id,timeslot)
        return render_template(
        "eventslist.html",
        events=events)
    return render_template('eventsearch.html', action='Search')



@crude.route('/venuesearch', methods=['GET', 'POST'])
def venuesearch():
    token = request.args.get('page_token', None)
    if token:
        token = token.encode('utf-8')
    if request.method == 'POST':
        day = request.form['day']
        venue_id = request.form['venue_id']

        times = get_model().venuesearch(day,venue_id)

        return render_template(
        "VenueSearchResults.html",
        times=times)
    return render_template('venuesearch.html', action='Search')

@crude.route('/timesearch', methods=['GET', 'POST'])
def venuesavailable():
    token = request.args.get('page_token', None)
    if token:
        token = token.encode('utf-8')
    if request.method == 'POST':
        day = request.form['day']
        timeslot = request.form['timeslot']

        venues = get_model().timesearch(day,timeslot)

        return render_template(
        "timesearchresults.html",
        venues=venues,timeslot=timeslot, day=day)
    return render_template('timeslotsearch.html', action='Search')

@crude.route('/searchandroidvenues/<date>/<ts>/', methods=['GET', 'POST'])
def venuesavailableandroid(date,ts):
    dayentered = datetime.strptime(date, '%m-%d-%Y')
    timeslotentered = int(ts)
    venues = get_model().timesearch(dayentered,timeslotentered)
    ids, venuenames = [],[]
    for venue in venues:
        ids.append(venue.id)
        venuenames.append(venue.name)
    venues_list = [{"id": i, "venuename": n} for i, n in zip(ids, venuenames)]
    return json.dumps(venues_list)


################################################
########IN PROGRESS
@crude.route('/searchandroidtimes/<date>/<vi>/', methods=['GET', 'POST'])
def timesavailableandroid(date,vi):
    dayentered = datetime.strptime(date, '%m-%d-%Y')
    venid = int(vi)

    times = get_model().venuesearch(dayentered,venid)
    all_times = [8,9,10,11,12,13,14,15,16,17,18,19,20]

    taken_times = list(set(all_times) - set(times))

    

    finaltimes, statuses = [],[]
    for time in all_times:
        finaltimes.append((str(time)+":00"))
        if time in taken_times:
            statuses.append("Taken")
        else:
            statuses.append("Available")

    times_list = [{"time": t, "status": s} for t, s in zip(finaltimes, statuses)]
    return json.dumps(times_list)
    ##################################################

@crude.route('/searchandroid/<ename>/<date>/<ts>/<vid>/', methods=['GET', 'POST'])
def eventsearchandroid(ename,date,ts,vid):
    if request.user_agent.platform == "android":
        allevents = Event.query.all()
        events_filtered = []
        for event in allevents:
            input_venue_id = vid
            if input_venue_id != "default":
                input_venue_id = int(vid)
            if input_venue_id == event.venue_id:
                events_filtered.append(event)
            event_name = ename
            if event_name == event.eventname:
                events_filtered.append(event)

            dayentered = date
            if dayentered != "default":
                dayentered = datetime.strptime(input_date, '%m-%d-%Y')
            if dayentered == event.day:
                events_filtered.append(event)

            timeslotentered = ts
            if timeslotentered != "default":
                timeslotentered = int(input_time)
            if timeslotentered == event.timeslot:
                events_filtered.append(event)

        
        ids, names, descriptions, dates,timeslots,listcurrentusers,listmaxusers,prices,venueids = [], [], [], [],[],[],[],[],[]
        for event in events_filtered:
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
