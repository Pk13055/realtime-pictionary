from flask import session
from flask_socketio import emit, join_room, leave_room

from app import logger, requires_auth, sketch_urls, rooms, socketio


@socketio.on('joined', namespace='/chat')
def joined(message):
	"""Emitted by clients who join a room

	:param message: str -> Message broadcasted
	:return None:
	"""
	print("joined", message)
	user = session['user']
	room = user['room']
	name = user['name']
	join_room(room)
	message = f"{name} has joined the room!"
	emit('status', {
		'message': message
	}, room=room)
	logger.info(message)


@socketio.on('message', namespace='/chat')
def message(json, methods=['GET', 'POST']):
	"""IO listener to capture messages by a user in a session

	:param message: str -> Message broadcasted
	:return None:
	"""
	print(message)
	user = session['user']
	message = f"{user['name']} : {message['message']}"
	emit('message', {
		'message': message
	}, room=user['room'])
	logger.info(message)


@socketio.on('image', namespace='/chat')
def image(json, methods=['GET', 'POST']):
	"""Update the image in the urls

	:param img: base64 encoded image data blob
	:return None:
	"""
	user = session['user']
	if data != sketch_urls[sender]:
		sketch_urls.update({
			sender: data
		})
	emit('image', {
		'image': data
	}, room=user['room'])
	logger.info(f"{sender} image updated!")


@socketio.on('left', namespace='/chat')
def left(json, methods=['GET', 'POST']):
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
	}, room=room, namespace='/chat')
	logger.info(message)
