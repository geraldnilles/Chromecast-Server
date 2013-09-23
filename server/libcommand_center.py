# This is a library that other apps can use to communicate with the command
# center

#--------------
# Imported Modules
#--------------

import socket
import struct
import subprocess
import os
import json

#----------------
# Constants
#----------------

# Socket Constants
UNIX_SOCKET_PATH = "/tmp/CommandCenterSocket"
SERVER_TIMEOUT = 5
CLIENT_TIMEOUT = 5
SERVER_CONNECTIONS = 10

# List of Daemon Processes
processes = [
		{
			"name":"Media Scanner",
			"cmd":["./media_scanner.py"],
			"proc":None
		},{
			"name":"Device Discoverer",
			"cmd":["./discoverer.py"],
			"proc":None
		}	
	]

#-----------------
# Socket Server Functions
#
# This should only be used by the command center
#-----------------

def server_setup(force=False):
	if force:
		# Remove Previoulsy open Unix Socket
		os.remove(UNIX_SOCKET_PATH)
	
	# Create Socket
	s = socket.socket(socket.AF_UNIX, 
			socket.SOCK_STREAM)

	s.bind(UNIX_SOCKET_PATH)
	# Allo Queuing of 10 connection
	s.listen(SERVER_CONNECTIONS)
	# Set a timeout of 5 seconds
	s.settimeout(SERVER_TIMEOUT)

	return s


#--------------
# Socket Client Functions
#---------------

## Send and Recieve JSON to Command Center
#
# Main Client function for communicating with the Command Center.  JSON object
# is converted to string, a size header is added, and the string is transmitted
# using TCP.  The rerse happens when a packet is received. 
#
# @param msg - A JSOn Object
# @return - A JSON Object response form the command center.
def client_send_recv(msg):
	s = socket.socket(socket.AF_UNIX,
			socket.SOCK_STREAM)

	try:
		# Connect to the Socket
		s.connect(UNIX_SOCKET_PATH)

		# Convert JSON object and send over TCP
		send_json(s,msg)

		# Recieve JSON object from TCP
		return recv_json(s)


	except socket.timeout:
		return {"error":"Unix Socket Timeout"}
 
## Prepare the JSON string for TCP
#
# Since TCP doesnt communicate packet length, We will add 4 bytes to the 
# beginning of the packet.  This will be an unsigned integer containing the 
# length of the packet.
def send_json(s,msg):
	data = json.dumps(msg)
	if type(data) != str:
		# If not a string, create en empty JSOn object to send
		return pack_string("{}")
	
	header = struct.pack("<I",len(data))

	s.sendall(header+data)


## Figures out the packet length
#
# Uses the first 4 bytes of the packet to determine the packet length.  
# From there, we know how many more bytes to recieve
def recv_json(s):

	header = s.recv(4)

	size = struct.unpack("<I",header)[0]

	data = s.recv(size)

	return json.loads(data)



#---------------------------
# Daemon Launcher Functions
#----------------------------

def get_process_list():
	return processes


# Checks if a process is running
def running(process):
	if process["proc"] == None:
		return False
	elif process["proc"].poll()== None:
		return True
	else:
		return False

# Starts the process
def start(process):
	print "Starting Process %s"%process["name"]
	# Launch process
	p = subprocess.Popen(process["cmd"],stdin=subprocess.PIPE)
	# Add the Popen object to the process object
	process["proc"] = p


def terminate(process):
	print "Terminating %s"%process["name"]
	process["proc"].terminate()

def kill(process):
	print "Killing %s"%process["name"]
	process["proc"].kill()
