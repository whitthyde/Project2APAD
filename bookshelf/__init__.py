
import os
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import current_app, Flask, redirect, url_for, render_template
from flask_bcrypt import Bcrypt
from flask_login import LoginManager 

class config(object):
    SECRET_KEY = 'secret'
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




app = Flask(__name__)
app.config.from_object(config)


bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'


# Add a default root route.
@app.route("/")
def index():
    return render_template("info.html")

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

# Register the events CRUD blueprint.
from .crude import crude
app.register_blueprint(crude, url_prefix ='/events')

#Register the events CRUD blueprint.
from .crudvens import crudvens
app.register_blueprint(crudvens, url_prefix ='/venues')

from .crudu import crudu
app.register_blueprint(crudu, url_prefix ='/users')

