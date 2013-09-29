#!/usr/bin/env python

#----------------------
# Web Socket Proxy
#
# This script will handle communication between a Websocket and any tools
#-----------------------

#--------------------
# Imported Modules
#-------------------
import asyncore,socket,re,hashlib,base64,struct,os

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



def complete_handshake(conn):
	# Grap the WebSocket Handshake Request
	data = conn.recv(1024)
	#print data
	# Grab the WS Key using a RegEx (TODO Make this case-insensitive)
	m = re.search("Sec-WebSocket-Key: (\S*)",data)
	key = ""
	if m:
		key =  m.group(1)
		print repr(key)
	else:
		print "Not a Handshake"
		return None
	resp_key = base64.b64encode(hashlib.sha1(
			key+"258EAFA5-E914-47DA-95CA-C5AB0DC85B11").digest())

	resp =  HANDSHAKE_RESPONSE_TMPL.format(resp_key)
	print resp

	conn.sendall(resp)
	return 1

def decode_ws_packet(p):
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

	# Unmask the payload
	decoded = ""
	for i in range(size):
		j = i%4
		# XOR the mask and the payload byte by byte
		decoded += chr(ord(mask[j])^ord(payload[i]))
	return decoded

def encode_ws_packet(string):
	# Send a single text packet
	packet = "\x81"
	# Always Use the extended packet
	packet += struct.pack('<B',len(string))
	# Payload
	packet += string
	
	#print packet.encode("hex")
	return packet

def service_ws(ws_conn):
	try:
		# Reset the WebSocket timeout to We dont want to waste 
		# time waiting for unexpected WS packets
		ws_conn.settimeout(0)
		data = ws_conn.recv(1024)
		# TODO Identify the Packet Type
		# For now, just print the raw data
		print repr(data)
		# If the WS returns an empty frame, the WebApp was 
		# closed.
		if data == "":
			print "WS Connection Closed by WebApp"
			# Close the Connections
			return False
	except socket.error as msg:
		# If Error is due to no data being ready, ignore
		if msg.errno == 10035:
			pass
		# Temporarily Unavaiable.  Not sure what this means but i'll
		# ignore it for now
		if msg.errno == 11:
			pass
		else:
			# If the error is different, exit the loop
			print repr(msg)
			return False
	
	return True

#---------------------
# IPC Functions
#---------------------

## Create the IPC Port
#
# THis socket will be used to collect commmands from other processes on this
# machine.  For testing purposes, this will be a IP address.  In the future,
# it will use Unix sockets.
def setup_ipc_listener():
	s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
	s.bind(LOCAL_UNIX_SOCKET)
	s.listen(1)
	s.settimeout(5)
	return s

def service_ipc(ipc_list,ws_conn):
	ipc_conn, addr = ipc_list.accept()
	# Give the WebSocket 10 secondds to respond
	ws_conn.settimeout(5)
	# Receive data chunk from IPC
	data = ipc_conn.recv(1024)
	if data == "CLOSE":
		return True
	# TODO Check that it is the entire packet
	# Encode and Send data through WebSocket Connection
	ws_conn.sendall(encode_ws_packet(data))
	# Receive and decode Response
	resp = decode_ws_packet(ws_conn.recv(1024))
	# Send Response back to IPC connection
	ipc_conn.sendall(resp)


def serve_forever():
	# Create a WebSocket Listener
	ws_list = setup_chromecast_listener()
	# WS Loop
	while 1:
		try:
			# Create a Connection with the Browser via WebSockets 
			ws_conn = wait_for_chromecast(ws_list)
			# Perform WS handshake
			complete_handshake(ws_conn)

			# Create an IPC listener
			ipc_list = setup_ipc_listener()
		except KeyboardInterrupt:
			break

		# IPC Loop
		while 1:
			# Wait 5 seconds for an IPC command
			try:
				# Wait for a IPC connect and service it
				service_ipc(ipc_list,ws_conn)
			
			except socket.timeout as msg:
				# If it does timeout, service the WS. 
				if not service_ws(ws_conn):
					# break WS Server returns false 
					break
			except KeyboardInterrupt:
				break
	
	
		ws_conn.close()
		os.remove(LOCAL_UNIX_SOCKET)
		ipc_list.shutdown(socket.SHUT_RDWR)
		ipc_list.close()

	ws_list.shutdown(socket.SHUT_RDWR)
	ws_list.close()

## WebSocket Server
#
# This class waits for WS connections to come from Chromecast devices.  Once a
# connection is created, a WS_Handler is created to maintain this connection
class WS_Server(asyncore.dispatcher):
	def __init__(self):
		asyncore.dispatcher.__init__(self)
		self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
		self.bind(CHROMECAST_IP_PORT)
		self.listen(5)
		print "Listening to port",CHROMECAST_IP_PORT
	
	def handle_accept(self):
		sock, addr = self.accept()
		print "Connection Attemp from", addr
		ws_sock = WS_Handler(sock)
		ux_sock = UX_Handler(sock)	


class UX_Handler(asyncor.dispatcher):
	def __init__(self,sock):
		asyncore.dispatcher.__init__(self)
		self.ws_proxy = sock
		self.create_socket(socket.AF_UNIX, socket.SOCK_STREAM)
		self.bind(UNIX_LOCAL_PORT)

## Websocket Handler
#
# Once a Websocket device connects, this will handle the connection.
class WS_Handler(asyncore.dispatcher):
	def __init__(self,sock):
		asyncore.dispatcher.__init__(self,sock)
		self.state = ""

	def handle_write(self):
		pass

	def handle_read(self):
		# Recv a chunk of data
		chunk = self.recv(1024)
		# Check if this ia a Handshake request
		if(self.is_handshake(chunk)):
			# Complete the handshake
			resp = self.complete_handshake(chunk)
			self.send(resp)
			return

		
		


if __name__ == "__main__":
	server = WS_Server()
	asyncore.loop()	

