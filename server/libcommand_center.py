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
import time

#----------------
# Constants
#----------------

# Socket Constants
UNIX_SOCKET_PATH = "/tmp/CommandCenterSocket"
SERVER_TIMEOUT = 5
CLIENT_TIMEOUT = 5
SERVER_CONNECTIONS = 10
CHUNK_SIZE = 4096


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
def send_recv(msg,path=UNIX_SOCKET_PATH):
	s = socket.socket(socket.AF_UNIX,
			socket.SOCK_STREAM)

	try:
		# Connect to the Socket
		s.connect(path)

		# Convert JSON object to a packet
		pkt = json_to_pkt(msg)
		# Send message to Command Center
		while(1):
			# Send part (if not all) of the packet
			sent = s.send(pkt)
			if sent >= len(pkt):
				# If the whole packet was sent, break the loop
				break
			else:
				# If More is left, discard the sent characters
				# and try again
				pkt = pkt[sent:]

		# Read Loop
		pkt = ""
		while(1):
			pkt += s.recv(1024)
			# Attempt to decode the packet
			msg,size = pkt_to_json(pkt)
			# If a proper Msg was created, return
			if msg != None:
				return msg
			# If msg == none, continue the loop
				



	except socket.timeout:
		return {"error":"Unix Socket Timeout"}
 
## Convert IPC Packet to JSON object
#
# This function converts a n IPC packet into a JSON object.  The first 4 bytes
# contains the totle packet size.  
def pkt_to_json(pkt):
	# Grab the pkt length from the first 4 bytes
	if len(pkt) < 4:
		return (None, 0 )
	header = pkt[0:4]
	size = struct.unpack("<I",header)[0]

	# If the packet is shorter than the expected length, return None,0
	if len(pkt) < size+4:
		return (None,0 )

	# Convert the packet to JSON object
	payload = pkt[4:4+size]	
	obj = json.loads(payload)
	# Return how much of the string buffer was used
	return (obj,size+4)	

## Convert JSON object to an IPC packet
#
# Stringify's the JSON object and adds a 4byte unsigned interger to the 
# beginning of the packet to idenfiy the length
def json_to_pkt(obj):
	pkt = json.dumps(obj)

	header = struct.pack("<I",len(pkt))

	pkt = header+pkt
	return pkt

#---------------------------
# Daemon Launcher Functions
#----------------------------

def get_process_list():
	return processes

## Check Processes
#
# This will check the given list of processes and start the ones that have not
# started yet.
def check_processes(ps):
	for p in ps:
		if not running(p):
			start(p)
			# Return now if you only want to start 1 process at a 
			# time.  Otherwise, all subprocesses will be started
			# simultaniously
			# return 


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

