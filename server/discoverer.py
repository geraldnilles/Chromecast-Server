#!/usr/bin/env python

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
		libcc.send_recv(msg)
		# Sleep for 60 minutes before we look again
		time.sleep(60*60)


if __name__ == "__main__":
	loop_forever()

