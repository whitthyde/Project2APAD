# Copyright 2015 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from flask import Flask
from flask_sqlalchemy import SQLAlchemy


###########################################################################################################################################################################
##################################################                CRUD - Books                             ##########################################################################################################
###############################################################################################################################################################################
#####################################################################################################################################################

builtin_list = list

db = SQLAlchemy()

def init_app(app):
    # Disable track modifications, as it unnecessarily uses memory.
    app.config.setdefault('SQLALCHEMY_TRACK_MODIFICATIONS', False)
    db.init_app(app)

def from_sql(row):
    """Translates a SQLAlchemy model instance into a dictionary"""
    data = row.__dict__.copy()
    data['id'] = row.id
    data.pop('_sa_instance_state')
    return data

###########################################################################################################################################################################
##################################################                DECLARING - MODELS                           ##########################################################################################################
###############################################################################################################################################################################
#####################################################################################################################################################

userevents = db.Table('userevents',
                      db.Column('event_id', db.SmallInteger(), db.ForeignKey('events.id'), primary_key=True),
                      db.Column('user_id', db.SmallInteger(), db.ForeignKey('users.id'), primary_key=True)
                      )

# [START model]

class Book(db.Model):
    __tablename__ = 'books'
    
    id = db.Column(db.SmallInteger(), primary_key=True)
    title = db.Column(db.String(255))
    author = db.Column(db.String(255))
    publishedDate = db.Column(db.String(255))
    imageUrl = db.Column(db.String(255))
    description = db.Column(db.String(767))
    createdBy = db.Column(db.String(255))
    createdById = db.Column(db.String(255))
    
    def __repr__(self):
        return "<Book(title='%s', author=%s)" % (self.title, self.author)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.SmallInteger(), primary_key=True)
    username = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=False, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    firstname = db.Column(db.String(80), unique=False, nullable=False)
    lastname = db.Column(db.String(80), unique=False, nullable=False)
    events_users = db.relationship('EventsUsers', backref='User', lazy=True)
    userevents = db.relationship('Event', secondary=userevents, lazy='subquery',
                                 backref=db.backref('users', lazy=True))
    
    def __repr__(self):
        return '<User %r>' % self.username

class Venue(db.Model):
    __tablename__ = 'venues'
    id = db.Column(db.SmallInteger(), primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    events = db.relationship('Event', backref='venues', lazy=True)
    
    def __repr__(self):
        return '<Venue %r>' % self.name

class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.SmallInteger(), primary_key=True)
    hostname = db.Column(db.String(80), unique=False, nullable=False)
    eventname = db.Column(db.String(120), unique=False, nullable=False)
    description = db.Column(db.String(767), unique=False, nullable=False)
    day = db.Column(db.DateTime(), unique=False, nullable=False)
    timeslot = db.Column(db.SmallInteger(), unique=False, nullable=False)
    currentusers = db.Column(db.SmallInteger(), unique=False, nullable=False)
    maxusers = db.Column(db.SmallInteger(), unique=False, nullable=False)
    price = db.Column(db.Float(7,2), unique=False, nullable=True)
    venue_id = db.Column(db.SmallInteger(),db.ForeignKey('venues.id'),nullable=False)
    events_users = db.relationship('EventsUsers', backref='Events', lazy=True)
    def __repr__(self):
        return '<Event %r>' % self.eventname


class EventsUsers(db.Model):
    __tablename__ = 'eventsusers'
    id = db.Column(db.SmallInteger(), primary_key=True)
    user_id = db.Column(db.SmallInteger(), db.ForeignKey('users.id'), nullable=False)
    event_id = db.Column(db.SmallInteger(), db.ForeignKey('events.id'), nullable=False)


###########################################################################################################################################################################
##################################################                CRUD - Books                     ##########################################################################################################
###############################################################################################################################################################################
#####################################################################################################################################################
# [START list]
def list(limit=10, cursor=None):
    cursor = int(cursor) if cursor else 0
    query = (Book.query
             .order_by(Book.title)
             .limit(limit)
             .offset(cursor))
    books = builtin_list(map(from_sql, query.all()))
    next_page = cursor + limit if len(books) == limit else None
    return (books, next_page)
# [END list]

# [START read]
def read(id):
    result = Book.query.get(id)
    if not result:
        return None
    return from_sql(result)
# [END read]

# [START create]
def create(data):
    book = Book(**data)
    db.session.add(book)
    db.session.commit()
    return from_sql(book)
# [END create]

# [START update]
def update(data, id):
    book = Book.query.get(id)
    for k, v in data.items():
        setattr(book, k, v)
    db.session.commit()
    return from_sql(book)
# [END update]

def delete(id):
    Book.query.filter_by(id=id).delete()
    db.session.commit()

###########################################################################################################################################################################
##################################################                CRUD - Users                             ##########################################################################################################
###############################################################################################################################################################################
#####################################################################################################################################################
# [START list]
def users_list(limit=10, cursor=None):
    cursor = int(cursor) if cursor else 0
    query = (User.query
             .limit(limit)
             .offset(cursor))
    users = builtin_list(map(from_sql, query.all()))
    next_page = cursor + limit if len(users) == limit else None
    return (users, next_page)
# [END list]

def readuser(id):
    result = User.query.get(id)
    if not result:
        return None
    return from_sql(result)
# [END read]
# [START create]
def createuser(data):
    user = User(**data)
    db.session.add(user)
    db.session.commit()
    return from_sql(user)
# [END create]
# [START update]
def updateuser(data, id):
    user = User.query.get(id)
    for k, v in data.items():
        setattr(user, k, v)
    db.session.commit()
    return from_sql(user)
# [END update]
def deleteuser(id):
    User.query.filter_by(id=id).delete()
    db.session.commit()

###########################################################################################################################################################################
##################################################                CRUD - Events                             ##########################################################################################################
###############################################################################################################################################################################
#####################################################################################################################################################
# [START list]
def events_list(limit=10, cursor=None):
    cursor = int(cursor) if cursor else 0
    query = (Event.query
             .limit(limit)
             .offset(cursor))
    evnts = builtin_list(map(from_sql, query.all()))
    next_page = cursor + limit if len(evnts) == limit else None
    return (evnts, next_page)
# [END list]

def readevent(id):
    result = Event.query.get(id)
    if not result:
        return None
    return from_sql(result)
# [END read]
# [START create]
def createevent(data):
    event = Event(**data)
    db.session.add(event)
    db.session.commit()
    return from_sql(event)
# [END create]
# [START update]
def updateevent(data, id):
    event = Event.query.get(id)
    for k, v in data.items():
        setattr(event, k, v)
    db.session.commit()
    return from_sql(event)
# [END update]
def deleteevent(id):
    Event.query.filter_by(id=id).delete()
    db.session.commit()

###########################################################################################################################################################################
##################################################                CRUD - Venues                             ##########################################################################################################
###############################################################################################################################################################################
#####################################################################################################################################################

def venues_list(limit=10, cursor=None):
    cursor = int(cursor) if cursor else 0
    query = (Venue.query
             .limit(limit)
             .offset(cursor))
    vens = builtin_list(map(from_sql, query.all()))
    next_page = cursor + limit if len(vens) == limit else None
    return (vens, next_page)
# [END list]
def readvenue(id):
    result = Venue.query.get(id)
    if not result:
        return None
    return from_sql(result)
# [END read]
# [START create]
def createvenue(data):
    venue = Venue(**data)
    db.session.add(venue)
    db.session.commit()
    return from_sql(venue)
# [END create]
# [START update]
def updatevenue(data, id):
    venue = Venue.query.get(id)
    for k, v in data.items():
        setattr(venue, k, v)
    db.session.commit()
    return from_sql(venue)
# [END update]
def deletevenue(id):
    Venue.query.filter_by(id=id).delete()
    db.session.commit()



###########################################################################################################################################################################
##################################################                CREATE DATABASE                ##########################################################################################################
###############################################################################################################################################################################
#####################################################################################################################################################

def _create_database():
    """
    If this script is run directly, create all the tables necessary to run the
    application.
    """
    app = Flask(__name__)
    app.config.from_pyfile('../config.py')
    init_app(app)
    with app.app_context():
        db.create_all()
    print("All tables created")


if __name__ == '__main__':
    _create_database()
