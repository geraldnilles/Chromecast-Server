#!/usr/bin/env python

import dial.discover
import libcommand_center as libcc
import time

def loop_forever():
	while(1):
		msg = {}
		msg["source"] = "discoverer"
		msg["devices"]= dial.discover.discover_devices()

		libcc.client_send_recv(msg)

		time.sleep(60*10)


if __name__ == "__main__":

	loop_forever()
