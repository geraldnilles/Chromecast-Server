#!/usr/bin/env python


import libcommand_center as libcc

from socket import timeout as TIMEOUT_ERROR

#--------------
# Constants
#--------------

class Update_Handler(asyncore.dispatcher):
	def __init__(self,sock,cc):
		asyncore.dispatcher.__init__(self,sock)
		self.read_buffer = ""
		self.write_buffer = ""

		# Keep track of the command center and the CC and DB
		self.command_center = cc
		self.db = cc.db

	def writable(self):
		if len(write_buffer) > 0:
			return True
		else:
			return False

	def handle_write(self):
		sent = self.send(self.write_buffer)
		self.write_buffer[sent:]

	
	def handle_read(self):
		# Add new data to the read buffer
		self.read_buffer += self.read(1024)
		# Attempt to decode the packet
		req, size = libcc.pkt_to_json(self.read_buffer)
		# If The Request oject is None, wait for more data
		if req == None:
			return
		else:
			# If Request packet is created, prepare a response
			self.prepare_response(req)
			# Adjust the read buffer accordingly
			self.read_buffer = self.read_buffer[size:]

	def prepare_response(self,req):
		resp = {
			"source":"command_center",
			"message":"OK"
		}
		if req["source"] == "discoverer":
			self.db["devices"] = req["devices"]
		elif req["source"] == "converter":
			if "progress" in req:
				pass
				# Update Progress for given item
			elif "complete" in req:
				pass
				# Remove Item from Queue
		elif req["source"] in ["cli","webui"]:
			# If an address is in the request, it is intneded for
			# a Chromecast Devices
			if "addr" in req:
				# Forward  Request to WebSocket Server
				resp = self.command_center.websocket_communicate(req)
			else:
				# If not address, it will be randome requests
				# to control the database or processes
		elif req["source"] == "scanner":
			# Overwrite the list of movies/tv on the database
			self.db["movies"] = req["movies"]
			self.db["tv"] = req["tv"]
		else:
			resp["msg"] = "Error"
			resp["error"] = "No Packet Source Given"

		self.write_buffer += libcc.json_to_pkt(resp)

## Main Command Center Unix Socket Server
#
# This is the main Command Center server.  It maintains a database and waits 
# for Unix Socket connections.  It also creates a WebSocket Server object
class Command_Center(asyncore.dispatcher):
	def __init__(self):
		asyncore.dispatcher.__init__(self)
		self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
		self.bind(libcc.PROCESS_UNIX_SOCKET)
		self.listen(5)

		self.db = {
			"devices":{},	# Dict of Chromecast Devices found
			"movies":[],	# List of Movies On Server
			"tv":[],	# List of TV series on Server
			"transcode_queue":[], # List of Videos to Transcode
			"websockets":{}, # Dict of Open WebSockets
			}

		self.start_websocket_proxy()

	def handle_accept(self):
		sock,addr = self.accept()
		Update_Handler(sock,self)

	def _write_db(self):
		pass	

	## Add a WebSocket to the Database
	#
	# When the WebSocket Proxy Server opens, it will add the socket 
	# instance to the database
	def add_websocket(self,addr,ws):
		self.db["websockets"][addr] = ws

	## Starts the WebSocket Proxy Server
	def start_websocket_proxy(self):
		# Create a WebSocket Proxy object.  Send the "self" variable
		# so that the WebSocket proxy has a pointer to the Command 
		# Center
		ws_proxy.WS_Server(self)
	

	## Communicate with a WebSocket
	#
	# Send a message to the websockets.  The target address should 
	# contained inside the req JSON object
	def websocket_communicate(self,req):
		if req["addr"] in self.db["websockets"]:
			wsock = self.db["websockets"][req["addr"]]
			wsock.send_msg(req)
			return wsock.recv_msg()
		else:
			return {"error":"No WS Connection for that address"}

# Start the Command center when this script is run indepen
if __name__ == '__main__':
	# Create a Command Center Object
	cc = Command_Center()

	# Initialize the list of processes
	ps = libcc.get_process_list()
	
	# Server Forever
	while(1):
		# Timeout after 10 seconds
		asyncore.loop(10)
		libcc.check_processes(ps)
		cc._write_db()


