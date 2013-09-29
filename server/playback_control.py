#!/usr/bin/env python

#--------------------
# Playback Control
#
# This is module allows controlling of Video Playback.  It also contains 
# CLI interface.
#-------------------


import socket,json

#------------------
# Constants
#-----------------

LOCAL_UNIX_SOCKET = "/tmp/WSUnixSocket"


## Send Message to WebSocket
def send_message(data):
	s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
	s.connect(LOCAL_UNIX_SOCKET)
	s.settimeout(5)

	s.sendall(data)

	return s.recv(1024)

## Play/Pause 
def play_pause():
	obj = {
		"cmd":"PLAYPAUSE"
		}

	resp = send_message(json.dumps(obj))
	return resp

## Load Path into the Player
def load(source):
	obj = {
		"cmd":"LOAD",
		"source":source
	}
	resp = send_message(json.dumps(obj))
	return resp

## Get Status from Player
def status():
	obj = {
		"cmd":"STATUS"
	}
	resp = send_message(json.dumps(obj))
	print resp
	return json.loads(resp)

## Skip progress bar
#
# Jumps player to a certain percentage in the playback.
def skip(percent):
	obj = {
		"cmd":"SKIP",
		"percent":percent
	}
	resp = send_message(json.dumps(obj))
	return resp

## CLI argument Parser
if __name__ == "__main__":
	import argparse
	parser = argparse.ArgumentParser(description="Send Commands to Player")
	parser.add_argument("-s","--source")
	parser.add_argument("-p","--play-pause", action="store_true")
	parser.add_argument("-t","--status",action="store_true")
	parser.add_argument("-k","--skip", type=float)

	args = parser.parse_args()

	if args.source:
		load(args.source)
	elif args.play_pause:
		play_pause()
	elif args.skip:
		skip(args.skip)
	elif args.status:
		status()
	else:
		parser.print_help()
	



