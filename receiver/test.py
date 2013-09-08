#---------------------
# Test CLI
#
# This is a special script for testing out the receiver web app.  It will
# send websocket commands to the Chromecast after the app is launched.
#---------------------

import json, argparse

#--------------
# Templates
#--------------

WS_HANDSHAKE = """GET HTTP 1.1\r
x=1 \r
y=2 \r
z=3 \r
\r"""

## Send WebSocket Command
#
# Sends data to the given IP/Port using WebSocket
def send_ws_command(ip,port,data):
	#----------
	# Open a Websocket
	#----------
	# Open TCP Socket
	
	# Send handshake
	s.send(WS_HANDSHAKE)
	# Recieve Chromecasts handshake response.  Discard the response since
	# i dont care if the response is wrong
	data = s.recv()

	#-----------
	# Send Command
	#-----------
	# Add header to data
	#    Struct that concatenates opcode + length + data
	# Send our command
	s.send(data)

	#-----------
	# Recv Response
	#----------
	# Recieve Opcode and Length
	header = s.recv(2)
	# if second byte is 126:
		# size = s.recv(2)
	# elif second byte is 127:
		# size = s.recv(4)

	# Receive the rest of the packet
	packet = s.recv(size)
	# Convert to a Python Dict and return
	return json.loads(packet)


## Toggle between Play and Pause
#
# Sends command to Chromecast to Start and Stop playback
def play_pause(ip,port):
	send_ws_command(ip,port,encode({
			"cmd":"PLAYPAUSE"
		}))

## Load Video for Playback
#
## Sends a video URL to play in the Chromecast WebApp
def load(ip,port,video_path):
	send_ws_command(ip,port,encode({
			"cmd":"LOAD",
			"path":video_path
		}))

## Stop Playback
#
## Stops the playback of a device and displays the Homepage
def stop(ip,port):
	send_ws_command(ip,port,encode({
			"cmd":"STOP"
		}))


## Skip Playback
#
## Jumps to the specified point in the playback
def skip(ip,port,seconds=None,percent=None):
	cmd = {}
	cmd["cmd"] = "SKIP"
	if percent:
		cmd["percent"] = str(percent) 
	elif seconds:
		cmd["seconds"] = str(seconds)

	send_ws_command(ip,port,encode(cmd))

def status(ip,port):
	resp = send_ws_command(ip,port,encode({
			"cmd":"STATUS"
		}))

	print resp

## Encode Object for Transfer
#
# Encodes a dictionary (obj) into a JSON string for transferint over WebSocket
def encode(obj):
	return json.dumps(obj)


if __name__ == "__main__":
	parser = argparse....
