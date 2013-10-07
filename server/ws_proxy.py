#!/usr/bin/env python

#----------------------
# Web Socket Proxy
#
# This script will handle communication between a Websocket and any tools
#-----------------------

#--------------------
# Imported Modules
#-------------------
import asyncore,socket
import re,hashlib,base64,struct
import os,time
import json
import libcommand_center as libcc

#-----------------
# Constants
#-----------------
# This is the WS port used by the Chomecast to connect to this server
CHROMECAST_IP_PORT = ("",50505)

# This is a template used for the WebSocket Handshake
HANDSHAKE_RESPONSE_TMPL="""HTTP/1.1 101 Switching Protocols\r
Upgrade: websocket\r
Connection: Upgrade\r
Sec-WebSocket-Accept: {0}\r
\r
"""



## Async WebSocket Server
#
# This class waits for WS connections to come from Chromecast devices.  Once a
# connection is created, a WS_Handler is created to maintain this connection
class WS_Server(asyncore.dispatcher):
	## Constructor
	#
	# @param cc - A reference to the Command Center Object
	def __init__(self,cc):
		# Create a TCP socket and listen to the WS port
		asyncore.dispatcher.__init__(self)
		self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
		self.bind(CHROMECAST_IP_PORT)
		self.listen(5)

		# Save a copy of the Command Center Reference
		self.command_center = cc

	## Handle New Connection
	#
	# When a new connection is attempted, this method handles it.  It creates
	# a WS_Handler object and forwards the new socket to the WS handler.  It 
	# also keepts track of this WS_Handler instance by adding it to the 
	# Command Center database
	def handle_accept(self):
		sock, addr = self.accept()
		# Create a WS handler from the connection socket
		ws_sock = WS_Handler(sock,self.command_center.remove_websocket)
		# Add this new socket to the Command Center Database
		self.command_center.add_websocket(addr[0], ws_sock)



## Websocket Handler
#
# Once a Websocket device connects, this will handle the connection.
class WS_Handler(asyncore.dispatcher):
	## Constructor
	#
	# This initializes the socket and creates read/write buffers
	#
	# @param db_remove - A reference to a function that removes a ws
	# from the database.  This allows the WS to nicely erase itself 
	# from the database
	def __init__(self,sock,db_remove):
		# Forward the new socket to the Super-class
		asyncore.dispatcher.__init__(self,sock)
		# Create a Read/Write buffer
		self.write_buffer = ""
		self.read_buffer = ""
		# Create place to keep Recived packets that have not yet been
		# read by the Command Center
		self.inbox = []
		# Save the reference to the database removal function
		self.db_remove = db_remove
	
	
	## Close handler
	# 
	# Clear the Read/Write buffers when a Close-Event is detected
	# otherwise, there will be an infinante loop of attempting to 
	# send the rest of the data in the write-buffer
	def handle_close(self):
		self.write_buffer = ""
		self.read_buffer = ""
		
		# Fetch the WS IP address and remove itself from the database
		self.db_remove(self.getpeername()[0])

		self.close()
	
	## Check if a Write is pending
	#
	# Simply check if the writebuffer is empty or not
	def writable(self):
		if len(self.write_buffer) > 0:
			return True
		else:
			return False
	
	## Handle a Write event
	#
	# Sends a chunk of data from the write buffer.  Clears the amount of data
	# sent from the beginning of the write buffer.
	def handle_write(self):
		sent = self.send(self.write_buffer)
		self.write_buffer = self.write_buffer[sent:]

	## Handle a Read Event
	
	def handle_read(self):
		# Recv a chunk of data into the Read buffer
		self.read_buffer += self.recv(1024)
		# If the Read Buffer is empty, do nothing
		if len(self.read_buffer) == 0:
			return

		# Attempt to complete a WebSocket Handshake
		if( self.ws_handshake()):
			# If it was a handshake, clear the buffer and return
			self.read_buffer = ""
			return
		
		else:
			# If not a handshake, decode the WS packet. 
			data = self.ws_decode()
			if data == False:
				# If the WS decode returns false, the packet
				# is still waiting on more data.  By returning now,
				# we can wait for more added to be added to
				# the read buffer.
				return
			try:
				# Attempt to convert the data to JSON 
				obj = json.loads(data)
				# Add the received data to the Inbox.  The 
				# Command center will check the inbox for data
				self.inbox.append(obj)
					
			except:
				# If there was an error, something must have been
				# corrupted.  Clear the read-buffer and try again
				print "Issue with WS Read Buffer. Clearing it out"
				self.read_buffer = ""

	## Complete a WebSocket handshake
	#
	# This method completes a WebSocket handshake.  This is used to 
	# initialize commuication between the Chromecast Browser App and the
	# server. 
	def ws_handshake(self):
		# Get the read buffer
		data = self.read_buffer
		# Grab the WS Key using a RegEx (TODO Make this case-insensitive)
		m = re.search("Sec-WebSocket-Key: (\S*)",data)
		key = ""
		# Check if this packet has a WebSocket key
		if m:
			key =  m.group(1)
		else:
			# If no key, this is not a handshake.  Return False
			return False
		# Generate a Respone key.  This follows the WebSocket definition
		resp_key = base64.b64encode(hashlib.sha1(
			key+"258EAFA5-E914-47DA-95CA-C5AB0DC85B11").digest())

		# Put this response key into the response template
		resp =  HANDSHAKE_RESPONSE_TMPL.format(resp_key)
		
		# Add this response to the Write buffer for sending
		self.write_buffer = resp
		# Return true to communicate that this was a handshake packet
		return True

	## WebSocket Decode
	#
	# This function decodes WebSocket data into Plain Text data
	def ws_decode(self):
		p = self.read_buffer
		# Ignore Byte 0 for new (assume we are always recieving text)
		# Convert Byte 1 to an unsigned char
		size = struct.unpack("<B",p[1])[0]
		# Remove the first bit to get the packet size
		size = size - 0x80
		# We will use 'index' to keep track of where we are in 'p'
		index = 2 

		# Size 126 and 127 are special cases that the packet is large
		if size == 126:
			# Convert Bytes 2 and 3 to an unsigned int
			index = 4 # Move the index
			size = struct.unpack("<H",p[2:3])[0]
		elif size == 127:
			# Convert Bytes 2 to 9 into an unsigned long
			index = 10 # Move the Index
			size = struct.unpack("<Q",p[2:9])[0]

		# Grab the Mask
		mask = p[index:index+4]
		# Grab the Payload
		payload = p[index+4:]

		# If the Payload is too small, return false.  This will force the
		# handler to wait for more data before continuing to decode
		if len(payload) < size:
			return False

		# Unmask the payload 4 bytes at a time
		decoded = ""
		for i in range(size):
			j = i%4
			# XOR the mask and the payload byte by byte
			decoded += chr(ord(mask[j])^ord(payload[i]))
		# Remove this portion of the payload from the read buffer
		self.read_buffer = self.read_buffer[index+4+size:]
		# Return the decoded string
		return decoded	

	## Encode a Websocket packet
	#
	# This packet converts a string of text into a WebSocket packet
	def ws_encode(self,data):
		# Send a single text packet
		packet = "\x81"
		# Always Use the extended packet (i dont care about the
		# added 8 bytes of overhead)
		packet += struct.pack('<B',len(data))
		# Payload
		packet += data
		# We will not mask the output data.  

		return packet
	

	## Receive a Message from the Inbox
	#
	# The Command Center will use this method to receive data from the 
	# WebSocket proxy.  It will remove 1 item from the Inbox list
	def recv_msg(self):
		if len(self.inbox) > 0:
			# If Inbox is not empty, remove 1 item and return
			return self.inbox.pop(0)
		else:
			# If inbox is empty, let em know
			return {"error":"Inbox Empty"}

	## Add a message to the Write Buffer
	#
	# This message takes a JSON object, converts it to a string, encodes
	# it to WS formate, and adds it to the Write buffer
	#
	# @param msg - a JSOn object to be sent to the Chromecast device
	def send_msg(self,msg):
		# Convert from JSON to string
		data = json.dumps(msg)
		# Encode to WS format
		pkt = self.ws_encode(data)
		# Add to Write buffer
		self.write_buffer += pkt
		

