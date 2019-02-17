import json

from flask import session
from flask_socketio import emit, join_room, leave_room

from app import rooms, socketio, requires_auth


log = []
def write_to(log):
    filename = "output_log.json"
    with (open(filename,'w')) as fd:
        fd.write(json.dumps(log))
    return

@socketio.on('joined', namespace='/chat/')
@requires_auth
def joined_io(message):
	"""Emitted by clients who join a room

	:param message: str -> Message broadcasted
	:return None:
	"""
	user = session['user']
	room = user['room']
	name = user['name']

	join_room(room)
	message = f"{name} has joined the room!"
	emit(message)
	# TODO: add (optional) logging


@socketio.on('text')
@requires_auth
def text_io(message, namespace='/chat/'):
	"""IO listener to capture messages by a user in a session

	:param message: str -> Message broadcasted
	:return None:
	"""
	user = session['user']
	message = f"{user['name']} : {message['message']}"
	emit('message', {
		'message': message
	}, room=user['room'])
	# TODO: add (optional) logging


@socketio.on('left', namespace='/chat/')
@requires_auth
def left_io(message):
	"""Capture left events, ie when a user leaves

	:param message: str -> Broadcasted message
	:return None:
	"""
	user = session['user']
	name = user['name']
	room = user['room']
	if rooms[room] == name.strip():
		rooms.pop(room, None)
	leave_room(room)
	message = f"{name} has left the room!"
	emit('message', {
		'message': message
	}, room=room)
	# TODO: add (optional) logging
