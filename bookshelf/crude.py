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
from flask import Flask, render_template, request, redirect
import pymysql
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy import inspect
from flask_login import login_user, current_user, logout_user, login_required
from datetime import date


crude = Blueprint('crude', __name__)





####################################################################################################################################################################################################################################################################################################################
################################################################################################################################################################################################################################################################################################################################################################################################
#######################################################             ROUTES               ######################################################################################################################################################################################################################################################################################################
################################################################################################################################################################################################################################################################



@crude.route('/')
def eventslist():
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


@crude.route('/<id>/delete')
def deleteevents(id):
    get_model().delete(id)
    return redirect(url_for('.eventslist'))

@crude.route('/search', methods=['GET', 'POST'])
def eventsearch():
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

