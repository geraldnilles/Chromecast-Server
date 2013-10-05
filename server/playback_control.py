#!/usr/bin/env python

#--------------------
# Playback Control
#
# This is module allows controlling of Video Playback.  It also contains 
# CLI interface.
#-------------------

import libcommand_center as libcc


def cc_communicate(req):
	# Add the source to the request object
	req["source"] = "cli"
	
	resp = libcc.send_recv(req)
	return resp

## Play/Pause 
def play_pause(addr):
	obj = {
		"cmd":"PLAYPAUSE",
		"addr":addr
		}

	print repr(cc_communicate(obj))

## Load Path into the Player
def load(addr,path):
	obj = {
		"cmd":"LOAD",
		"addr":addr,
		"path":path
	}
	print repr(cc_communicate(obj))

## Get Status from Player
def status(addr):
	obj = {
		"cmd":"STATUS",
		"addr":addr
	}
	print repr(cc_ommunicate(obj))

## Skip progress bar
#
# Jumps player to a certain percentage in the playback.
def skip(addr,percent):
	obj = {
		"cmd":"SKIP",
		"addr":addr,
		"percent":percent
	}
	print repr(cc_communicate(obj))


def movies():
	obj = {"cmd":"movies"}
	resp = cc_communicate(obj)
	for x in resp["movies"]:
		print x["title"]
	

def devices():
	obj = {"cmd":"devices"}
	resp = cc_communicate(obj)
	
	for x in resp["devices"]:
		print x["name"]
		print x["ip"]+":"+x["port"]
		print ""


## CLI argument Parser
if __name__ == "__main__":
	import argparse
	parser = argparse.ArgumentParser(description="Send Commands to Player")
	parser.add_argument("-s","--source")
	parser.add_argument("-p","--play-pause", action="store_true")
	parser.add_argument("-t","--status",action="store_true")
	parser.add_argument("-k","--skip", type=float)
	parser.add_argument("-d","--devices", action="store_true")
	parser.add_argument("-m","--movies", action="store_true")
	parser.add_argument("-a","--address")

	args = parser.parse_args()

	if args.source:
		load(addr,args.source)
	elif args.play_pause:
		print play_pause(addr)
	elif args.skip:
		skip(addr,args.skip)
	elif args.status:
		status(addr)
	elif args.devices:
		devices()
	elif args.movies:
		movies()
	else:
		parser.print_help()
	



