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
import os
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import current_app, Flask, redirect, url_for
from flask_bcrypt import Bcrypt
from flask_login import LoginManager 




app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
DATA_BACKEND = 'cloudsql'
PROJECT_ID = 'whydeyyanp2'
CLOUDSQL_USER = 'root'
CLOUDSQL_PASSWORD = 'texasfight'
CLOUDSQL_DATABASE = 'mydb2'
CLOUDSQL_CONNECTION_NAME = 'whydeyyanp2:us-central1:library'


LOCAL_SQLALCHEMY_DATABASE_URI = (
    'mysql+pymysql://{user}:{password}@127.0.0.1:3306/{database}').format(
        user=CLOUDSQL_USER, password=CLOUDSQL_PASSWORD,
        database=CLOUDSQL_DATABASE)

LIVE_SQLALCHEMY_DATABASE_URI = (
    'mysql+pymysql://{user}:{password}@localhost/{database}'
    '?unix_socket=/cloudsql/{connection_name}').format(
        user=CLOUDSQL_USER, password=CLOUDSQL_PASSWORD,
        database=CLOUDSQL_DATABASE, connection_name=CLOUDSQL_CONNECTION_NAME)

if os.environ.get('GAE_INSTANCE'):
    SQLALCHEMY_DATABASE_URI = LIVE_SQLALCHEMY_DATABASE_URI
else:
    SQLALCHEMY_DATABASE_URI = LOCAL_SQLALCHEMY_DATABASE_URI


app.config['SQLALCHEMY_DATABASE_URI'] = (
    'mysql+pymysql://{user}:{password}@127.0.0.1:3306/{database}').format(
        user=CLOUDSQL_USER, password=CLOUDSQL_PASSWORD,
        database=CLOUDSQL_DATABASE)

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'


# Add a default root route.
@app.route("/")
def index():
    return redirect(url_for('crud.list'))

# Add an error handler. This is useful for debugging the live application,
# however, you should disable the output of the exception for production
# applications.
@app.errorhandler(500)
def server_error(e):
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500



def get_model():
    
    from . import model_cloudsql
    model = model_cloudsql
    return model

with app.app_context():
    model = get_model()
    model.init_app(app)

from bookshelf import login,register

from .login import lgin
app.register_blueprint(lgin, url_prefix='/login')

from .register import signu
app.register_blueprint(signu, url_prefix='/signup')

# Register the Bookshelf CRUD blueprint.
from .crud import crud
app.register_blueprint(crud, url_prefix ='/books')

# Register the events CRUD blueprint.
from .crude import crude
app.register_blueprint(crude, url_prefix ='/events')

#Register the events CRUD blueprint.
from .crudvens import crudvens
app.register_blueprint(crudvens, url_prefix ='/venues')

from .crudu import crudu
app.register_blueprint(crudu, url_prefix ='/users')

