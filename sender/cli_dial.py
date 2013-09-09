#!/usr/bin/env python

import dial_discover
import dial_rest
import json
import argparse


#---------------
# Constants
#--------------
DEVICE_LIST = "/tmp/ChromecastDevices"

## Discover Devices
#
# Search for Chromecast devices and writes them to a temp file
def discover_devices():
	ds = dial_discover.discover_devices()

	# If Number of devices is non-zero write to disk
	if len(ds) > 0:
		f = open(DEVICE_LIST,'w')
		json.dump(ds,f)
		f.close()

	return ds

## Read Device List form Temp File
def get_device_list():
	f = open(DEVICE_LIST,'r')
	ds = json.load(f)
	f.close()
	return ds

##
def launch_webapp():
	launch_generic_app("e7689337-7a7a-4640-a05a-5dd2bd7699f9_1")

def launch_generic_app(appID):
	d = get_device_list()[0]
	dial_rest.launch_app(d,appID)

def webapp_status():
	d = get_device_list()[0]
	dial_rest.app_status(d,"e7689337-7a7a-4640-a05a-5dd2bd7699f9_1")


def print_devices():
	print repr(get_device_list())


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Chromecast App Launcher")
	parser.add_argument("-d","--discover",action="store_true")
	parser.add_argument("-p","--print-devices",action="store_true")
	parser.add_argument("-l","--launch", action="store_true")
	parser.add_argument("-a","--app-id")

	args = parser.parse_args()

	if args.discover:
		discover_devices()
		

	if args.print_devices:
		print_devices()
	elif args.launch:
		if args.app_id:
			launch_generic_app(args.app_id)
		else:
			launch_webapp()
	else:
		if not args.discover:	
			parser.print_help()


