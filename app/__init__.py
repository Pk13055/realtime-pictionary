from functools import wraps

from flask import (Flask, render_template, session,
					blueprints,jsonify, redirect, url_for)
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect,CSRFError
from flask_socketio import SocketIO


# Define the WSGI application object
app = Flask(__name__, static_url_path = '/static')

# Configurations
app.config.from_object('config')

# initialize socketIO
socketio = SocketIO()
socketio.init_app(app)

# Define the database object which is imported
# by modules and controllers
db = SQLAlchemy(app)

# in-memory data stores for various operations
words = open('./words.csv').read().splitlines()
rooms = {}
# TODO: check purpose of d_url and translate to new schema
room_urls = {}

# csrf protection
csrf=CSRFProtect(app)
@app.errorhandler(CSRFError)
def csrf_error(reason):
    # return jsonify(success=True,error=reason)
    return render_template('error.html.j2', error=reason), 400

# HTTP error handling route
@app.errorhandler(404)
def not_found(error):
	return render_template('error.html.j2', error=error) , 404

# authorization for the logged in state
# modify this according to your needs
def requires_auth(f):
	@wraps(f)
	def decorated(*args, **kwargs):
		# FIXME: change this part according to your login mechanism
		if 'user' not in session:
			return redirect(url_for('main.main_route'))
		return f(*args, **kwargs)
	return decorated

# Import a module / component using its blueprint handler variable (mod_auth)
from app.main.controller import main

# Register blueprint(s)
app.register_blueprint(main)

# Build the database:
# This will create the database file using SQLAlchemy
db.create_all()

