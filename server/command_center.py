#!/usr/bin/env python


import libcommand_center as libcc
import asyncore
import socket
import ws_proxy
from socket import timeout as SOCK_TIMEOUT
from socket import error as SOCK_ERROR
import os.path
import time
import dial.rest

## Update Handler
#
# This Socket handler is used to talk to the subprocesses.  When requests come in 
# from the various sub-processes, it will handle the request accordingly.
class Update_Handler(asyncore.dispatcher):
	## Constructor
	#
	# Initializes the Update Handler
	#
	# @param sock - Socket Instance that is being handled
	# @param cc - Reference to Command Center
	def __init__(self,sock,cc):
		asyncore.dispatcher.__init__(self,sock)
		# Intitialize the read/write buffers
		self.read_buffer = ""
		self.write_buffer = ""

		# Keep track of the command center and the CC Database
		self.command_center = cc
		self.db = cc.db

	## Check if A Write is pending
	#
	# Checks if the writebuffer is empty. Also checks if any of the 
	# Websockets have new messages in the Inbox
	#
	# @return - True if data is ready to be sent
	def writable(self):
		# Check if the current write-buffer is not empty
		if len(self.write_buffer) > 0:
			return True
		# Check if any of the Websockets proxy's have messages waiting
		ws = self.db["websockets"]
		for key in ws:
			if len(ws[key].inbox) > 0:
				return True		

		# If not data is queued, return false
		return False

	## Handles the Write
	#
	# This method actually writes a chunk of data
	def handle_write(self):
		# Check the Websockets for pending messages
		ws = self.db["websockets"]
		for key in ws:
			# Check if the Websocket is not empty
			if len(ws[key].inbox) > 0:
				# Create a Response object
				resp = {
					"source":"command_center",
					"message":ws[key].recv_msg()
				}
				# Add it to the Write Buffer
				self.write_buffer += libcc.json_to_pkt(resp)
	
		# Send a chunk of data from the write buffer
		sent = self.send(self.write_buffer)
		# Clear the data the was sent from the buffer
		self.write_buffer[sent:]

	## Handle a Read event
	# 
	# This function reads a chunk of data and attemps to process it. If
	# it cannot decode the data, it exits and waits for more data
	def handle_read(self):
		# Add new data to the read buffer
		self.read_buffer += self.recv(1024)
		# Attempt to decode the packet
		req, size = libcc.pkt_to_json(self.read_buffer)
		# If The Request oject is None, return and wait for more data
		if req == None:
			return
		else:
			# If Request packet is created, prepare a response
			self.prepare_response(req)
			# Adjust the read buffer accordingly
			self.read_buffer = self.read_buffer[size:]

	## Prepare a Response
	# 
	# This method generates a response based ont he request object.  If a
	# proper response can be generated, it adds the data to the write buffer
	# If more data is needed before a response can be made, it returns None
	# and watis for th next chunk of data.
	def prepare_response(self,req):
		# Setup a default response object
		resp = {
			"source":"command_center",
			"message":"OK"
			}
		#-----
		# Determine the source of the request
		#-----
		
		# Check if a source is not given
		if "source" not in req:
			resp["message"] = "Error - Source Not Given"
		# If the request if from the device discoverer daemon
		elif req["source"] == "discoverer":
			# Add each device to the Command Center Database
			for d in req["devices"]:
				self.db["devices"][d["ip"]] = d	

		# If the request is from the Media Converter (transcoder)
		elif req["source"] == "converter":
			# If a progress bar is given...
			if "progress" in req:
				# .. transcoding is still in progress.  Update
				# the database accordingly
				pass
			# if job is complete...
			elif "complete" in req:
				# Remove that item from the transcode queue
				# and update the Video database to show that this
				# item is ready to cast
				pass
			else:
				resp["message"] = "Invalide Converter Check-in"
		
		# If the request is comeing from the CLI or the WebUI
		elif req["source"] in ["cli","webui"]:
			# If an address is in the request, it is intneded for
			# a Chromecast Devices
			if "addr" in req:
				# Break off to a seprate method for this
				resp["message"] = self.chromecast_command(req)
			# If no command was given, return an error
			elif "cmd" not in req:
				resp["message"] = "CLI Error - No Comand Given"


			# The remaining commands are looking for database stuff
			elif req["cmd"] == "movies":
				# Retrn a list of movies
				resp["movies"] = self.db["movies"]
			elif req["cmd"] == "devices":
				# Return a list of Devices
				resp["devices"] = self.db["devices"]
			else:
				resp["message"] = "CLI Error - Bad Command"				
		# If the request is coming from the Filesystem scanner
		elif req["source"] == "scanner":
			# Overwrite the list of movies/tv on the database
			self.db["movies"] = req["movies"]
			self.db["tv"] = req["tv"]
		#  If the source is something else, return an error
		else:
			resp["message"] = "Source is invalid"

		# If a message was given, respond. 
		if resp["message"] != None:
			self.write_buffer += libcc.json_to_pkt(resp)
		# If the message was None, wait for a response

	## Chromecast Specific Commands
	#
	# This function looks at requests intended for Chromecasts and generates
	# a response
	def chromecast_command(self,req):
		# Create shorter Variables
		addr = req["addr"]
		cmd = req["cmd"]
		app_id = "e7689337-7a7a-4640-a05a-5dd2bd7699f9_1"

		# Check if the provided address is valid
		if addr in self.db["devices"]:
			device = self.db["devices"][addr]
		else:
			device = None
		# Do the same for WebSockets
		if addr in self.db["websockets"]:
			ws = self.db["websockets"][addr]
		else:
			ws = None

		## Check the type of command

		# If a launch Command
		if cmd == "launch":
			# Check if the device is valid
			if device == None:
				return "Invalid IP address"
			else:
				# Launch device using REST protocol
				dial.rest.launch_app(device, app_id)
				# Return a successful message
				return "Launch Successful"
		# If Exit command
		elif cmd == "exit":
			# check if the device is valid
			if device == None:
				return "Invalide IP address"
			else:	
				# Exit App using REST protocol
				dial.rest.exit_app(device, app_id)
				return "Exit successful"
		# If a Playback command
		elif cmd in ["play_pause","status","load","skip"]:
			# Check if the Websocekt is valid
			if ws == None:
				# If not, the websocket the app is likely not 
				# launched yet
				return "App has not been launched yet"
			else:
				# Forward the command through the websocket proxy
				ws.send_msg(req)
				# Return None.  The response will go t the WS's
				# inbox so we will check that later.  
				return None 
		


## Main Command Center Unix Socket Server
#
# This is the main Command Center server.  It maintains a database and waits 
# for Unix Socket connections.  It also creates a WebSocket Server object
class Command_Center(asyncore.dispatcher):
	def __init__(self):
		# Init the generic dispatcher
		asyncore.dispatcher.__init__(self)

		if(os.path.exists(libcc.UNIX_SOCKET_PATH)):
			os.remove(libcc.UNIX_SOCKET_PATH)

		# Create a Unix socket to listen to
		self.create_socket(socket.AF_UNIX, socket.SOCK_STREAM)
		self.bind(libcc.UNIX_SOCKET_PATH)
		self.listen(5)

		# Create a JSON database in Memory to keep track of all of the
		# sub processes
		self.db = {
			"devices":{},	# Dict of Chromecast Devices found
			"movies":[],	# List of Movies On Server
			"tv":[],	# List of TV series on Server
			"transcode_queue":[], # List of Videos to Transcode
			"websockets":{}, # Dict of currently Open WebSockets
			}

		# Start the Websocket Proxy
		self.start_websocket_proxy()

	# This method is called whenever a socket connection is made
	def handle_accept(self):
		# Create a handler object to deal with the socket
		sock,addr = self.accept()
		Update_Handler(sock,self)

	# Write the Memory database to disk
	def _write_db(self):
		# We will do nothing for now
		pass	

	## Add a WebSocket to the Database
	#
	# When the WebSocket Proxy Server opens, it will add the socket 
	# instance to the database
	def add_websocket(self,addr,ws):
		self.db["websockets"][addr] = ws

	## Remove a WebSocket from the Database
	#
	# When a Websocket Proxy is closed, this should be called to remove
	# it from the command center database
	def remove_websocket(self,addr):
		del self.db["websockets"][addr]

	## Starts the WebSocket Proxy Server
	def start_websocket_proxy(self):
		# Create a WebSocket Proxy object.  Send the "self" variable
		# so that the WebSocket proxy has a pointer to the Command 
		# Center
		ws_proxy.WS_Server(self)
	

# Start the Command center when this script is run indepen
if __name__ == '__main__':
	# Create a Command Center Object
	cc = Command_Center()

	# Initialize the list of processes
	ps = libcc.get_process_list()
	
	# Server Forever
	watchdog_length = 10
	watchdog_time = time.time() + watchdog_length 
	while(1):
		# Timeout after at most 10 seconds
		asyncore.loop(timeout=1,count=10)
		# Verify that the timeout is at least 10 seconds
		if time.time() > watchdog_time:
			# Update the watchdog
			watchdog_time = time.time()+watchdog_length
			# Check processes and write to db
			libcc.check_processes(ps)
			cc._write_db()

			# Print DB stats
			print "Current DB stats:"
			for key in cc.db:
				print "\t"+key+": "+str(len(cc.db[key]))



