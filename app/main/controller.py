import hashlib
import random

from flask import (Blueprint, flash, g, jsonify, redirect, render_template,
                   request, session, url_for)

import app.main.helper as helper
from app import db, models, requires_auth, sketch_urls, rooms, words

main = Blueprint('main', __name__, url_prefix='/')


@main.route('/', methods=['GET', 'POST'])
def main_route():
	"""Login page to enter the room(s)

	:param POST: username, room_id -> str, str
	:return context**: template
	"""
	seed = hashlib.md5(str(random.random()).encode()).hexdigest()
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
		'title': "Homepage - Login",
		'seed': seed,
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
		sketch_urls.update({room: None})

	session['user'].update({'role': role})  # update the role in the session
	context_kwargs = {
		'title': "Chat",
		'role': role,
		'user': user,
		'word': word,
		'room': room
	}
	return render_template('main/chat.html.j2', **context_kwargs)


@main.route('/logout', methods=['POST'])
@requires_auth
def logout_route():
	"""Logout the user and remove all session data

	TODO: deprecate this route after handling socketio events
	:param POST: None
	:returns status: dict -> Response status
	"""
	final_status = all([
		session.pop('user', False),
		session.pop('word', False)
		])
	return jsonify({
		'status': final_status
	})


import app.main.helper as helper
