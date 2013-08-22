#------------------------
# DIAL REST
#
# This module is used to launch Chromecast Apps
#--------------------------

import httplib

## Launches an App Given the App-ID
def launch_app(device,app_id,args=None):

	# Setup HTTP Connection
	conn = httplib.HTTPConnection(device["ip"],device["port"])
	# Setup Headers
	headers = {
			"Content-Type": "application/x-www-form-urlencoded; charset=\"utf-8\"",
			"User-Agent":"...",
			}
	# Setup DATA.  it looks like they add some sort of pairing code.  
	# It look randomely generated so im guessing its just a UUID to ID
	# the same session
	data = "pairingCode="+uuid.uuid()
	conn.request("POST",device["app_path"]+app_id,"",headers)
	r = conn.getresponse()
	data = r.read()
	hs = r.getheaders()
	print hs,data


