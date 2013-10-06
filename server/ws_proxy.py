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

# This is the Unix Socket name used by other processes to connect to this proxy
# When multiple devices are connected at the same time, a number will be added
# to the end of this name
LOCAL_UNIX_SOCKET = "/tmp/WSUnixSocket"

HANDSHAKE_RESPONSE_TMPL="""HTTP/1.1 101 Switching Protocols\r
Upgrade: websocket\r
Connection: Upgrade\r
Sec-WebSocket-Accept: {0}\r
\r
"""



## WebSocket Server
#
# This class waits for WS connections to come from Chromecast devices.  Once a
# connection is created, a WS_Handler is created to maintain this connection
class WS_Server(asyncore.dispatcher):
	## Constructor
	#
	# @param cc - The Command Center object
	def __init__(self,cc):
		# Create a TCP socket and listen to the WS port
		asyncore.dispatcher.__init__(self)
		self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
		self.bind(CHROMECAST_IP_PORT)
		self.listen(5)

		# Save the Command Center socket in this object
		self.command_center = cc

		print "WS Server Created: ",CHROMECAST_IP_PORT
	
	def handle_accept(self):
		sock, addr = self.accept()
		print "Connection Attemp from", addr
		# Create a WS handler from the connection socket
		ws_sock = WS_Handler(sock)
		# Add this new socket to the Command Center Database
		self.command_center.add_websocket(addr[0], ws_sock)



## Websocket Handler
#
# Once a Websocket device connects, this will handle the connection.
class WS_Handler(asyncore.dispatcher):
	def __init__(self,sock):
		asyncore.dispatcher.__init__(self,sock)
		self.state = ""
		self.write_buffer = ""
		self.read_buffer = ""
		self.inbox = []
	
	def handle_connect(self):
		print "WS Connection Created"

	def handle_close(self):
		print "WS Connection Closed"
		self.write_buffer = ""
		self.read_buffer = ""
		self.close()
	
	def writable(self):
		if len(self.write_buffer) > 0:
			return True
		else:
			return False

	def handle_write(self):
		sent = self.send(self.write_buffer)
		self.write_buffer = self.write_buffer[sent:]

	def handle_read(self):
		# Recv a chunk of data
		self.read_buffer += self.recv(1024)
		if len(self.read_buffer) == 0:
			return
		# Attempt to complete a WebSocket Handshake
		if( self.ws_handshake()):
			# If it was a handshake, clear the buffer and return
			self.read_buffer = ""
		else:
			data = self.ws_decode()
			print data
			if data != False:
				try: 
					obj = json.loads(data)
					print obj
					self.inbox.append(obj)
					
				except:
					print "Issue with WS Read Buffer. Clearing it out"
					self.read_buffer = ""

	def ws_handshake(self):
		# Get the read buffer
		data = self.read_buffer
		#print data
		# Grab the WS Key using a RegEx (TODO Make this case-insensitive)
		m = re.search("Sec-WebSocket-Key: (\S*)",data)
		key = ""
		if m:
			key =  m.group(1)
			print repr(key)
		else:
			print "Not a Handshake"
			return False
		resp_key = base64.b64encode(hashlib.sha1(
		key+"258EAFA5-E914-47DA-95CA-C5AB0DC85B11").digest())

		resp =  HANDSHAKE_RESPONSE_TMPL.format(resp_key)
		print resp

		self.write_buffer = resp
		return True

	
	def ws_decode(self):
		p = self.read_buffer
		# Ignore Byte 0 for new (assume its all text)
		# Convert Byte 1 to an unsigned char
		size = struct.unpack("<B",p[1])[0]
		# Remove the first bit (We will assume its masked)
		size = size - 0x80
		index = 2
		if size == 126:
			# Convert Bytes 2 and 3 to an unsigned int
			index = 4
			size = struct.unpack("<H",p[2:3])[0]
		elif size == 127:
			# Convert Bytes 2 to 9 into an unsigned long
			index = 10
			size = struct.unpack("<Q",p[2:9])[0]

		# Grab the Mask
		mask = p[index:index+4]
		# Grab the Payload
		payload = p[index+4:]

		if len(payload) < size:
			return False

		# Unmask the payload
		decoded = ""
		for i in range(size):
			j = i%4
			# XOR the mask and the payload byte by byte
			decoded += chr(ord(mask[j])^ord(payload[i]))
		self.read_buffer = self.read_buffer[index+4+size:]
		return decoded	

	def ws_encode(self,data):
		# Send a single text packet
		packet = "\x81"
		# Always Use the extended packet
		packet += struct.pack('<B',len(data))
		# Payload
		packet += data

		#print packet.encode("hex")
		return packet
	
	
	def recv_msg(self,attempts = 10,t=0.1):
		if len(self.inbox) > 0:
			return self.inbox.pop(0)
		elif attempts > 0:
			time.sleep(t)
			return self.recv_msg(attempts -1)
		else:
			return {"error":"timeout"}

	def send_msg(self,msg):
		data = json.dumps(msg)
		pkt = self.ws_encode(data)
		self.write_buffer += pkt
		


if __name__ == "__main__":
	server = WS_Server()
	asyncore.loop()	

