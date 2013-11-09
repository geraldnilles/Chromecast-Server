#!/usr/bin/env python

#------------------
# Discoverer
#
# This daemon process uses the DIAL protocol to periodically search for devices
# on the local network.  Device info is sent back to the command center
#-------------------

import dial.discover
import libcommand_center as libcc
import time

def loop_forever():
	while(1):
		# Create a message to send to the Command Center
		msg = {}
		msg["source"] = "discoverer"
		msg["devices"]= dial.discover.discover_devices()

		# Send message to devices
		resp = libcc.send_recv(msg)

		if resp["message"] == "OK":
			# If everything went well, sleep for an hour
			time.sleep(60*60)
		else:
			# If there was an error, try again in 10
			time.sleep(10)


if __name__ == "__main__":
	loop_forever()

