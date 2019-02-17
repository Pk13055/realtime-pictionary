#!/usr/bin/env python3
from sys import argv as rd
from app import app

def main():
	try:
		port = int(rd[1])
	except:
		port = 3000
	app.run(debug=True, host='127.0.0.1', port=port)

if __name__ == '__main__':
	main()