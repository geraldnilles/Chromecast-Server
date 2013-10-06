#!/usr/bin/env python

#--------------------
# Playback Control
#
# This is module allows controlling of Video Playback.  It also contains 
# CLI interface.
#-------------------

import libcommand_center as libcc



## Command Center Communication Function
#
# This Function communicates with the command center.  It takes a request 
# object, adds the source.  It then sends the request and returns the response 
def cc_communicate(req):
	# Add the source to the request object
	req["source"] = "cli"
	
	resp = libcc.send_recv(req)
	return resp

#--------------------
# Playback Functions
#
# These functions are used to control the Chromecast Device
#--------------------


## Play/Pause 
def play_pause(addr):
	obj = {
		"cmd":"play_pause",
		"addr":addr
		}

	print repr(cc_communicate(obj))

## Load Path into the Player
def load(addr,path):
	obj = {
		"cmd":"load",
		"addr":addr,
		"path":path
	}
	print repr(cc_communicate(obj))

## Get Status from Player
def status(addr):
	obj = {
		"cmd":"status",
		"addr":addr
	}
	print repr(cc_ommunicate(obj))

## Skip progress bar
#
# Jumps player to a certain percentage in the playback.
def skip(addr,percent):
	obj = {
		"cmd":"skip",
		"addr":addr,
		"percent":percent
	}
	print repr(cc_communicate(obj))


#-----------------
# DB Fetch Functions
#
# These functions fetch data from the Command Center database and prints
# them.  These are Read-Only functions.
#-----------------

## List Movies
#
# Generates a list of movies that are currently in the database
def movies():
	obj = {"cmd":"movies"}
	resp = cc_communicate(obj)
	for x in resp["movies"]:
		print x["title"]

## List TV Shows
#
# Generates a list of TV shows that are current in the database
def tv():
	obj = {"cmd":"tv"}
	resp = cc_communicate(obj)
	for show in resp["tv"]:
		print show["title"]
		for eps in show:
			print "\t",eps["title"]

## List Discovered Devices
#
# Generates a list of devices that have been discovered using the DIAL protocol
def devices():
	obj = {"cmd":"devices"}
	resp = cc_communicate(obj)
	for ip in resp["devices"]:
		print resp["devices"][ip]["name"]
		print ip+":"+resp["devices"][ip]["port"]
		print ""

#------------------
# Command Center Action Functions
#
# These functions request actions from the Command Center
#-------------------

## Launch the Chromecast App
def launch(addr):
	obj = {
		"cmd":"launch",
		"addr":addr	
		}
	resp = cc_communicate(obj)
	
	print resp["message"]

def exit(addr):
	obj = {
		"cmd":"exit",
		"addr":addr
		}
	resp = cc_communicate(obj)

	print resp["message"]

## CLI argument Parser
if __name__ == "__main__":
	import argparse
	parser = argparse.ArgumentParser(description="Send Commands to Player")
	parser.add_argument("-f","--path", metavar="/path/to/file")
	parser.add_argument("-p","--play-pause",action="store_true")
	parser.add_argument("-s","--status",action="store_true")
	parser.add_argument("-k","--skip", type=float)
	parser.add_argument("-d","--devices", action="store_true")
	parser.add_argument("-m","--movies", action="store_true")
	parser.add_argument("-l","--launch",action="store_true")
	parser.add_argument("-a","--address",metavar="IP_ADDR")

	parser.add_argument("-x","--exit",action="store_true")


	args = parser.parse_args()

	## Non-Chromecast Specific Commands
	if args.devices:
		devices()
	elif args.movies:
		movies()
	## Chromecast Specific Commands
	elif args.address == None:
		print "You must specify an IP address for some commands"
		print_help()
	elif args.launch:
		launch(args.address)
	elif args.exit:
		exit(args.address)
	elif args.play_pause:
		play_pause(args.address)
	elif args.status:
		status(args.address)
	else:
		parser.print_help()
	



