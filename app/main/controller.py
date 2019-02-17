import hashlib
import random

from flask import (Blueprint, flash, g, jsonify, redirect, render_template,
                   request, session, url_for)

import app.main.helper as helper
from app import db, models, requires_auth, room_urls, rooms, words

main = Blueprint('main', __name__, url_prefix='/')


@main.route('/', methods=['GET', 'POST'])
def main_route():
	"""Login page to enter the room(s)

	:param POST: username, room_id -> str, str
	:return context**: template
	"""
	if request.method == "POST":
		session['word'] = random.choice(words)
		name = request.form['name']
		hash_ = hashlib.md5(name.encode()).hexdigest()
		img_url = f"https://www.gravatar.com/avatar/{hash_}?s=200&d=identicon&r=PG"
		session['user'] = {
			'name': name,
			'room': request.form['room'],
			'image': img_url
		}
		return redirect(url_for('main.chat'))

	context_kwargs = {
		'title': "Homepage - Login"
	}
	return render_template('main/index.html.j2', **context_kwargs)


@main.route('/chat/', methods=['GET'])
@requires_auth
def chat():
	"""Main drawer/viewer route after logging in

	:params None:
	:return context**: template
	"""
	user = session['user']
	word = session['word']
	name = user['name']
	room = user['room']
	role = 'drawer'

	if room in rooms and rooms[room] != name.strip():
		#  viewer role set
		role = 'viewer'
		word = None  # viewer does not have access to the word
	else:
		# create a new room and assign drawer role (default)
		rooms.update({room: name.strip()})
		room_urls.update({room: None})

	context_kwargs = {
		'title': "Chat",
		'role': role,
		'user': user,
		'word': word
	}
	return render_template('main/chat.html.j2', **context_kwargs)


@main.route('/updateImg', methods=['GET'])
@requires_auth
def update_route():
	"""Update the canvas template

	:param url_params: vy -> str: The params for the drawing
	:return result: dict -> success status
	"""
	try:
		url = request.args.get('vy', None)
		room = session['user']['room']
		room_urls.update({room: url})
		status, error = True, None
	except Exception as e:
		status, error = False, str(e)
	finally:
		return jsonify({
			'status': status,
			'error': error
		})
