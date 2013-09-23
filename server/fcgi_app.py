#!/usr/bin/env python

# Import Modules
from string import Template
import libcommand_center as libcc

# Templates
TMPL_VIDEO_LIST = """
<div class="video" key="$key">
	<a>Video Poster</a>
	<a>$name</a>
	<div>
		Play Count: 0 <br />
		Year: 0000 <br />
		Actors: X,Y,Z </br>
		Plot: In a world...</br>
		Rotten Tomatoes: X% </br>
	</div>
</div>
"""

# Create a new message object
def new_msg():
	msg = {}
	msg["source"] = "webui"
	return msg


def app():
	# Look at path and call appropriate function
	pass

# Creates a list of movies.
def list_videos(filter):
	# Get a list of moves from the Control Center
	# Filter the Movies using the filter parameter
	output += ""
	for v in video:
		s = Template(TMPL_VIDEO_LIST).substitute(v)
		output += s
	return output

# Loads a video to the Chromecast Devices
def load_video(device,key):
	# Create "LOAD" message
	msg = new_msg()
	msg["cmd"] = "LOAD"
	msg["key"] = key
	msg["device"] = device

	# Send message to Command Center and get response
	ret = libcc.client_send_recv(msg)

	if "error" in ret:
		return "Error Loading Video: "+repr(ret)
	else:
		return "Video Loaded"
		

# Sends Toggles Play/Pause for device
def play_pause(device):
	# Create PLAY/PAUSE message
	msg = new_msg()
	msg["cmd"] = "PLAYPAUSE"
	msg["device"] = device

	# Send message to Command Center
	ret = libcc.client_send_recv(msg)
	if "error" in ret:
		return "Error Toggling Playback: "+repr(ret)
	else:
		return "Playback Toggled"

# Playback jumps to a specified percentage
def skip(device,percent):
	# Create Jump message
	msg = new_msg()
	msg["cmd"] = "SKIP"
	msg["percent"] = percent
	msg["device"] = device

	# Send message to Command Center
	ret = libcc.client_send_recv(msg)
	if "error" in ret:
		return "Error Skipping: "+repr(ret)
	else:
		return "Skipped to percent: "+str(percent)

def status(device):
	# Create PLAY/PAUSE message
	msg = new_msg()
	msg["cmd"]="STATUS"
	msg["device"]=device 

	# Send message to Command Center
	s = libcc.client_send_recv(msg)

	# Return String version of JSON packet
	return json.dumps(s)


if __name__ == "__main__":
	print "Serving FastCGI app over WebSocket"


