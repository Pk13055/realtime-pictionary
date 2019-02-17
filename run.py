#!/usr/bin/env python3
from sys import argv as rd
from app import socketio, app
from config import DEBUG


def main():
	try:
		port = int(rd[1])
	except:
		port = 3000
	socketio.run(app, debug=DEBUG, host='127.0.0.1', port=port)

if __name__ == '__main__':
	main()