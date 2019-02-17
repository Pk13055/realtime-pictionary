from functools import wraps
from logging.config import dictConfig

from flask import (Flask, render_template, session, current_app,
					blueprints,jsonify, redirect, url_for)
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect,CSRFError
from flask_socketio import SocketIO
from werkzeug.local import LocalProxy


# setup app logging
dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})
logger = LocalProxy(lambda: current_app.logger)

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
def requires_auth(f):
	@wraps(f)
	def decorated(*args, **kwargs):
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

