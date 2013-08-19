#-------------------
# DIAL Discovery
#
# This module will be used to discover Chromecast devices
#-------------------

## Template for M-Search Request
#
# This is sent via Multicast to all of the chromecast devices.  The USER-AGENT
# might need to change.
TMPL_M_SEARCH_REQUEST = """M-SEARCH * HTTP/1.1\r
HOST: 239.255.255.250:1900\r
MAN: "ssdp:discover"\r
MX: seconds to delay response\r
ST: urn:dial-multiscreen-org:service:dial:1\r
USER-AGENT: OS/version product/version\r
\r
"""


## Discovers Chromecast Devices 
#
# This uses the DIAL Service Discovery protocol to find all Chromecast devices
# on the network.
#
# @return A list of Chromecast's IP address and Friendly name
def discover_devices():
	# Send M-SEARCH Request and make a list of all the responses
	device_ips = m_search_request()
	
	# Make a list of device descriptions
	device_descs = []
	for d in device_ips:
		device_descs.append(device_description_request(d))
	
	return device_descs


## M Search Request
#
# Sends an M-Search Multicast request.  It also sets up a response handler that
# parses the M-Search Response and creats a list
def m_search_request():
	# Deivice Location  List
	dev_loc = []

	# Setup Multi-cast.  Responses will be handled by m_search_handler()
	# Send TMPL_M_SEARCH_REQEUST

	return dev_loc

## M Search Response Handler
#
# After the M-Serach Multicast request, this function will handle the responses
def m_search_handler(dev_loc):
	# Extract LOCATION: from header
	dev_loc.append(header["LOCATION"])


def device_description_request(d):
	# Send and recieve GET request 
	HTTPRequest(d["ip"]+port+"/dd.xml")

	# Parse the XMl reponse
		# Get Friendly name
		# Get App URL, etc...



