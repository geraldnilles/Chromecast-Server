#!/usr/bin/env python

#--------------------
# Playback Control
#
# This is module allows controlling of Video Playback.  It also contains 
# CLI interface.
#-------------------

import libcommand_center as libcc

#------------------
# Constants
#-----------------

WS_UNIX_SOCKET = "/tmp/WSUnixSocket"



## Play/Pause 
def play_pause():
	obj = {
		"cmd":"PLAYPAUSE",
		"addr":"192.168.0.103"
		}

	resp = libcc.client_send_recv(obj,WS_UNIX_SOCKET)
	return resp

## Load Path into the Player
def load(source):
	obj = {
		"cmd":"LOAD",
		"source":source
	}
	resp = libcc.client_send_recv(obj,WS_UNIX_SOCKET)
	return resp

## Get Status from Player
def status():
	obj = {
		"cmd":"STATUS"
	}
	resp = libcc.client_send_recv(obj,WS_UNIX_SOCKET)
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
	resp = libcc.client_send_recv(obj,WS_UNIX_SOCKET)
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
		print play_pause()
	elif args.skip:
		skip(args.skip)
	elif args.status:
		status()
	else:
		parser.print_help()
	



