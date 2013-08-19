#------------------------
# DIAL REST
#
# This module is used to launch Chromecast Apps
#--------------------------


## Launches an App Given the App-ID
def launch_app_from_id(device,app_id,args=None):
	# Send Post Request to device["path"]+app_id with args as the body
	# Content Type is text/plain; charset="utf-8


## Ask Chromecast for Application Staus
def application_info_request(device,app_id):
	# Send GET request to device["path"]+app_id
	# Parse the XML response

