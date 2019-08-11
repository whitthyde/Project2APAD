#This file is the crud methods for the events
from flask import Flask
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
db = SQLAlchemy()
# db = sqlalchemy.create_engine(
#     # Equivalent URL:
#     # mysql+pymysql://<db_user>:<db_pass>@/<db_name>?unix_socket=/cloudsql/<cloud_sql_instance_name>
#     sqlalchemy.engine.url.URL(
#         drivername='mysql+pymysql',
#         username='root',
#         password="texasfight",
#         database="mydb2",
#         query={
#             'unix_socket': '/cloudsql/{}'.format("whydeyyanp2:us-central1:library")
#         }
#     ),
#     # ... Specify additional properties here.
#     # ...
# )


###########################################################################################################################################################################
##################################################                Connecting to DB                          ##########################################################################################################
###############################################################################################################################################################################
#####################################################################################################################################################
db_user = "root"
db_password = "texasfight"
db_name = "mydb2"
db_connection_name = "whydeyyanp2:us-central1:library"

def connect():
   # When deployed to App Engine, the `GAE_ENV` environment variable will be
    # set to `standard`
    if os.environ.get('GAE_ENV') == 'standard':
        unix_socket = '/cloudsql/{}'.format(db_connection_name)
        cnx = pymysql.connect(user=db_user, password=db_password, unix_socket=unix_socket, db=db_name)
    else:
        # If running locally, use the TCP connections instead
        # Set up Cloud SQL Proxy (cloud.google.com/sql/docs/mysql/sql-proxy)
        # so that your application can use 127.0.0.1:3306 to connect to your
        # Cloud SQL instance
        host = '127.0.0.1'
        # cnx = pymysql.connect(user=db_user, password=db_password, host=host, db=db_name)
        cnx = pymysql.connect(user=db_user, password=db_password, host=host, db=db_name)
    return cnx


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

# @crude.route('/add', methods=['GET', 'POST'])
# def addevents():
#     if request.method == 'POST':
#         hostname = request.form['hostname']
#         eventname = request.form['eventname']
#         date = request.form['day']
#         description = request.form['description']
#         timeslot = request.form['timeslot']
#         currentusers = request.form['currentusers']
#         maxusers = request.form['maxusers']
#         price = request.form['price']
#         venue_id = request.form['venue_id']

#         #(host, name, des,vID, date, time,currU, maxU)
#         start_event(hostname,eventname,description, venue_id,date,timeslot,currentusers,maxusers,price)

#         return redirect(url_for('.eventslist'))
#     return render_template("eventsform.html", action="Add", event={})
# # [END add]


@crude.route('/<id>/edit', methods=['GET', 'POST'])
def editevents(id):
    book = get_model().read(id)

    if request.method == 'POST':
        data = request.form.to_dict(flat=True)

        book = get_model().update(data, id)

        return redirect(url_for('.view', id=book['id']))

    return render_template("form.html", action="Edit", book=book)



@crude.route('/<id>/join')
def joinevent(id):
    event_id = id
    user_id = current_user.get_id()
    get_model().join_event(event_id,user_id)
    ####ABOVE THIS WORKS    
    return redirect(url_for('.eventslist'))


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
        "venuesearchresults.html",
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



###########################################################################################################################################################################
##################################################                SQL Utility functions                          ##########################################################################################################
###############################################################################################################################################################################
#####################################################################################################################################################
#EventID,Name, Description, VenueID, Day, Timeslot, CurrentUsers, MaxUsers

builtin_list = list

db = SQLAlchemy()

def start_event(host, name, des,vID, date, time,currU, maxU,cost):

    with db.session.connect() as cursor:
        cursor.execute('''SELECT * FROM events WHERE Day=%s''', (date,))
        events_on_day = cursor.fetchall()
    if events_on_day:
        sametime = False
        for x in events_on_day:
            if x[6]==time:
                errorstring = 'That timeslot has already been taken. Please select a different timeslot or choose another venue.'
                return render_template("sqlerror.html",errorstring=errorstring)
                sametime = True
        if not sametime:
            with db.session.connect() as cursor:
                #selecting the maxID from the table
                cursor.execute(''' SELECT max(EventID) FROM Events''')
                maxID = cursor.fetchone() [0]
                maxID+=1
                cursor.execute('''INSERT INTO events(EventID,hostname,eventname, Description, Day, Timeslot, CurrentUsers, MaxUsers,price,venue_id) VALUES (?,?,?,?,?,?,?,?,?,?)''',(maxID,host, name, des, date, time,currU, maxU,cost,vID))
                conn.commit()
                conn.close()
            
    else:
        #selecting the maxID from the table
        with db.session.connect() as cursor:
            cursor.execute(''' SELECT max(EventID) FROM Events''')
            maxID = cursor.fetchone() [0]
            maxID+=1
            cursor.execute('''INSERT INTO events(EventID,hostname,eventname, Description, Day, Timeslot, CurrentUsers, MaxUsers, price, Venue_ID) VALUES (?,?,?,?,?,?,?,?,?,?)''',(maxID,host, name, des, date, time,currU, maxU,cost,vID))
            db.close()
            db.commit()
            db.commit()




