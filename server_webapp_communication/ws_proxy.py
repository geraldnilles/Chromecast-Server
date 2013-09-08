# Shebang

#----------------------
# Web Socket Proxy
#
# This script will handle communication between a Websocket and any tools
#-----------------------

#--------------------
# Imported Modules
#-------------------
import socket,re,hashlib,base64,struct

#-----------------
# Constants
#-----------------
CHROMECAST_IP_PORT = ("",50505)
LOCAL_IP_PORT = ("",40404)

HANDSHAKE_RESPONSE_TMPL="""HTTP/1.1 101 Switching Protocols\r
Upgrade: websocket\r
Connection: Upgrade\r
Sec-WebSocket-Accept: {0}\r
\r
"""
#Sec-WebSocket-Protocol: chat\r

def setup_chromecast_listener():
	s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	s.bind(CHROMECAST_IP_PORT)
	s.listen(1)
	return s

def wait_for_chromecast(sock,timeout=None):
	print "Waiting for a Chomecast to Connect..."
	conn,addr = sock.accept()
	print "Connection Established with ",addr
	return conn


def complete_handshake(conn):
	# Grap the WebSocket Handshake Request
	data = chrome_conn.recv(1024)
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
	print decoded

def encode_ws_packet(string):
	# Send a single text packet
	packet = "\x81"
	# Always Use the extended packet
	packet += struct.pack('<B',len(string))
	# Payload
	packet += string
	
	print packet.encode("hex")
	return packet

	


# Create a connection
chrome_conn = wait_for_chromecast(setup_chromecast_listener())
# Perform WS handshake
complete_handshake(chrome_conn)


# Print the next incomming message
decode_ws_packet(chrome_conn.recv(1024))

chrome_conn.sendall(encode_ws_packet("Oh Hey"))

# Close
chrome_conn.close()

""" Backup
# Create Chromecast Server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("127.0.0.1",50505))
s.listen(1)
conn,addr = s.accept()
print "Connected by",addr
conn.settimeout(0)

# Create a CLI Server
c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
c.bind(("127.0.0.1",40404))
c.listen(1)
c.settimeout(5)

while 1:
	# Check for a Handshake or for a Ping

	try:
		data = conn.recv(1)
		# If a handshake is received, respond accordingly
		if data == "H":
			print "Responding to a Handshake"
			conn.sendall("R")
		# If a Ping is received, repond with a Pong
		elif data == "P":
			print "Respondin to a Ping"
			conn.sendall("O")
	except socket.error:
		pass

	# Wait 5 seconds for a CLI before giving up
	try:
		print "Waiting for a command"
		# Accept a connection from the CLI
		cli,addr = c.accept()
		conn.settimeout(10)
		# Receive the Command from CLI
		data = cli.recv(1)
		# Send the Command to the Chromecast
		conn.sendall(data)
		# Get the response from the Chromecast
		resp = conn.recv(1)
		# Send the response to the CLI
		cli.sendall(resp)

		conn.settimeout(0)
	except socket.timeout:
		pass
"""	
