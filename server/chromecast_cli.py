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
#
# This fuction toggles the Chromecast video player between Play and pause
#
# @param addr - A string containing the Chromecast's IP address
# @return a JSON object containing the response
def play_pause(addr):
	obj = {
		"cmd":"play_pause",
		"addr":addr
		}

	return cc_communicate(obj)

## Get Status
#
# This function reads the Chromecast's video player status
#
# @param addr - A stirng containing the IP address of the Chomecast
# @return A JSON boject containing the Player's status
def status(addr):
	obj = {
		"cmd":"status",
		"addr":addr
	}
	resp = cc_communicate(obj)
	for key in resp["message"]:
		print key,":",resp["message"][key]

## Skip Ahead/Behind
#
# Jumps Chromecast video player to a certain percentage in the playback.
#
# @param addr - A string containing the IP address of the Chromecast Device
# @param percent - A float containing the Percentage you want to jump to.  This 
# 		should be between 0 and 100
# @return A JSON object containing the response (usually just "OK")
def skip(addr,percent):
	obj = {
		"cmd":"skip",
		"addr":addr,
		"percent":percent
	}
	return cc_communicate(obj)

## Load URL into the Player
#
# This function loads a URL into the Video Player
#
# @param addr - A stirng containing te Chromecast's Ip address
# @param path - A URL to the Media File to be played
# @return - A JSON object containing the Command's response
def load(addr,url):
	obj = {
		"cmd":"load",
		"addr":addr,
		"src":url
	}
	return cc_communicate(obj)

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
#
# This launches this project's Chromecast App on the selected Device.
#
# @param addr - A string containing the IP address of the device on which you want
#		to launch the app.
# @return - A JSOn object containing the message
def launch(addr):
	obj = {
		"cmd":"launch",
		"addr":addr	
		}
	resp = cc_communicate(obj)
	
	return resp["message"]

## Exist the Chromecast App
#
# This exits the custom Chromecast App on the selected device
#
# @param addr - A Stirng containing the Ip address of the device
# @return - A JSOn object containing the response message
def exit(addr):
	obj = {
		"cmd":"exit",
		"addr":addr
		}
	resp = cc_communicate(obj)

	return resp["message"]


## Prepare Media for Streaming
#
# This function tells the Command Center to add the follwing file to the
# streaming Queue

def conv_add(path):
	obj = {
		"cmd":"conv_add",
		"path":path
	}
	resp = cc_communicate(obj)
	return resp["message"]

def conv_status():
	obj = {
		"cmd":"conv_status"
	}
	resp = cc_communicate(obj)
        return resp["message"]


def conv_remove(path):
	obj = {
		"cmd":"conv_remove",
		"path":path
	}
	resp = cc_communicate(obj)
        return resp["message"]
	

## CLI argument Parser
if __name__ == "__main__":
	import argparse
	parser = argparse.ArgumentParser(description="Send Commands to Player")
	parser.add_argument("-u","--url", metavar="/path/to/file")
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
		parser.print_help()
	elif args.launch:
		launch(args.address)
	elif args.exit:
		exit(args.address)
	elif args.play_pause:
		play_pause(args.address)
	elif args.status:
		status(args.address)
	elif args.skip:
		skip(args.address,args.skip)
	elif args.url:
		load(args.address,args.url)
	else:
		parser.print_help()
	



