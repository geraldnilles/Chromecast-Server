#!/usr/bin/env python


import libcommand_center as libcc

from socket import timeout as TIMEOUT_ERROR

#--------------
# Constants
#--------------

class Update_Handler(asyncore.dispatcher):
	def __init__(self,sock,db):
		asyncore.dispatcher.__init__(self,sock)
		self.db = db
		self.read_buffer = ""
		self.write_buffer = ""

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
			pass
		elif req["source"] == "converter":
			pass
		elif req["source"] in ["cli","webui"]:
			pass
		elif req["source"] == "scanner":
			pass
		#...

		self.write_buffer += libcc.json_to_pkt(resp)


class Command_Center(asyncore.dispatcher):
	def __init__(self):
		asyncore.dispatcher.__init__(self)
		self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
		self.bind(libcc.PROCESS_UNIX_SOCKET)
		self.listen(5)

		self.db = {
				"devices":[],
				"movies":[],
				"tv":[],
				"transcode_queue":[]			
			}

	
	def handle_accept(self):
		sock,addr = self.accept()
		Update_Handler(sock,self.db)

	def _write_db(self):
		pass		
		

# Start the Command center when this script is run indepen
if __name__ == '__main__':
	# Create a Command Center Object
	cc = command_center()

	# Initialize the list of processes
	ps = libcc.get_process_list()
	
	# Server Forever
	while(1):
		# Timeout after 10 seconds
		asyncore.loop(10)
		libcc.check_processes(ps)
		cc._write_db()


