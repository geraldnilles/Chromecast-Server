#------------------------
# DIAL REST
#
# This module is used to manage Chromecast apps.
# You can launch, kill, and check the status through HTTP requests
#--------------------------

import httplib
import uuid

## Launches an App Given the App-ID
def launch_app(device,app_id,args=None):

	# Setup HTTP Connection
	conn = httplib.HTTPConnection(str(device["ip"]),int(device["port"]))
	# Setup Headers
	headers = {
		# TODO See if these 2 arguments are required.
		"Content-Type": "application/x-www-form-urlencoded;charset=\"utf-8\"",
		"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.57 Safari/537.36",
		# REQUIRED: This is the ID of the Chromecast extension 
		# on the Google Chrome store.  Changing this by 1 character
		# breaks it.  It appears that Chromecast checks for this 
		# string. They are probably gathering usuage data 
		# (ie Chrome vs IOS vs Android)
		# TODO: Look at wireshark for what iOS and Android uses
		"Origin":"chrome-extension://boadgeojelhgndaghljhdicfkmllpafd"
		}

	# The Data needs to contain a pairing code. A Random UUID works
	data = "pairingCode="+str(uuid.uuid1())

	# Send the Request
	conn.request("POST",device["app_path"]+app_id,data,headers)
	# Recv the response
	r = conn.getresponse()
	# This response doesnt contain anything interesting.

## Gets the App's status
def app_status(device,app_id):
	# Create an HTTP GET Request using the app Path
	conn = httplib.HTTPConnection(device["ip"],device["port"])
	conn.request("GET",device["app_path"]+app_id)
	# The Response contains XML info on the App's status
	r = conn.getresponse()
	print r.read()
	print r.status,r.reason

## Kill an App
def exit_app(device,app_id):
	# Create an HTTP DELETE request using the App Path
	conn = httplib.HTTPConnection(str(device["ip"]),int(device["port"]))
	conn.request("DELETE",device["app_path"]+app_id)
	r = conn.getresponse()
	
