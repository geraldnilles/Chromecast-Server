#---------------------
# Test CLI
#
# This is a special script for testing out the receiver web app.  It will
# send websocket commands to the Chromecast after the app is launched.
#---------------------

import json, argparse

## Send WebSocket Command
#
## Sends data to the given IP/Port using WebSocket
def send_ws_command(ip,port,data):
	pass


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
def skip(ip,port,point):
	send_ws_command(ip,port,encode({
			"cmd":"SKIP",
			"point":point
		}))

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
