#-------------------
# DIAL Discovery Module
#
# This module will be used to discover Chromecast devices
#-------------------

import socket
import httplib
import struct
import time
import re

#-----------------
# Constants
#-----------------

## Template for M-Search Request
#
# This is sent via Multicast to all of the chromecast devices.  The USER-AGENT
# might need to change.
TMPL_M_SEARCH_REQUEST = """M-SEARCH * HTTP/1.1\r
HOST:239.255.255.250:1900\r
MAN:"ssdp:discover"\r
MX:2\r
ST:urn:dial-multiscreen-org:service:dial:1\r
USER-AGENT:Google Chrome/28.0.1500.95 Windows\r
\r
"""

MCAST_ADDR = "239.255.255.250"
MCAST_PORT = 1900


#--------------------
# Functions
#---------------------

## Discovers Chromecast Devices 
#
# This uses the DIAL Service Discovery protocol to find all Chromecast devices
# on the network.
#
# @return A list of Chromecast's IP address and Friendly name
def discover_devices():
	# Send M-SEARCH Request and make a list of all the responses
	devices = m_search_request()
	# Get the friendly names for each device	
	for d in devices:
		add_device_name(d)
			
	return devices


## M Search Request
#
# Sends an M-Search Multicast request.  It also sets up a response handler that
# parses the M-Search Response and creats a list
def m_search_request():


	# Create the Multicast Socket
	send_sock = socket.socket(
			socket.AF_INET, 	# Use Internet Socket 
			socket.SOCK_DGRAM, 	# Specify UDP Protocol
			socket.IPPROTO_UDP) 	# Allow setting sock opts??
	send_sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
	# Send Multicast Message
	send_sock.sendto(TMPL_M_SEARCH_REQUEST, (MCAST_ADDR,MCAST_PORT))
	# Figure out the "source" port of your Multicast.  This is different 
	# that the "destination" port.  After Chromecast receives 
	# the Multicast, it will respond with a unicast on THIS port
	UCAST_PORT = send_sock.getsockname()[1]
	# Close the socket after sending the Multicast so you can reuse the port
	send_sock.close()	


	# Setup Unicast Listener
	recv_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 
			socket.IPPROTO_UDP)
	# Allow re-use of the same address for this socket
	recv_sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
	# Set a timeout just in case
	recv_sock.settimeout(2)
	# Bind this socket to the same source port as the Multi-cast	
	recv_sock.bind(("",UCAST_PORT))

	# Fetch all devices
	devices = []
	# Limit the number of devices to 10
	for i in range(10):
		try:
			# Recieve a UDP datagram packet
			data = recv_sock.recv(10000);
			d = {
					"data":data
					}
			# Parse the LOCATION info using RegExs
			m = re.search("LOCATION: http://(.*?):([0-9]*)(.*)\r"
					,data)
			d["ip"] = m.group(1)
			d["port"] = m.group(2)
			d["info_path"] = m.group(3)
			# Add it to the device list
			devices.append(d)

		except( socket.timeout):
			break
	# print the number of devices
	print "%d devices found"% len(devices)
	return devices
	

## Verify Device Still Exists
#
# If you already have the IP address of a Chromecast device, you can verify 
# that it is still active by sending a Unicast of the same port.  This is 
# faster and less messy than a Multicast
def device_check(ip):
	sock = socket.socket(
			socket.AF_INET,
			socket.SOCK_DGRAM)
	sock.sendto(TMPL_M_SEARCH_REQUEST,(ip,MCAST_PORT))
	packet = sock.recv(10000)
	print packet
	# Parse Packet for location header



def add_device_name(d):
	# Setup HTTP Connection object
	conn = httplib.HTTPConnection(d["ip"],d["port"])
	conn.request("GET",d["info_path"])
	r = conn.getresponse()
	data = r.read()
	
	m = re.search("<friendlyName>(.*)</friendlyName>",data)
	d["name"] = m.group(1)






