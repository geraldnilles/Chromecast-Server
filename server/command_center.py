#!/usr/bin/env python


import libcommand_center as libcc

from socket import timeout as TIMEOUT_ERROR

#--------------
# Constants
#--------------

class command_center:
	def __init__(self):
		# Set the Unix Socket
		self.listener = libcc.server_setup(True)

		# Create a list of processes
		self.processes = libcc.get_process_list()
		# Init DB
		self.db = {
				"movies":[],
				"tv":[],
				"music":[],
				"transcoding_queue":[],
				"devices":[]
				}
		# TODO Open DB from file and load existing data

	def _write_db(self):
		# Write DB to disk
		pass

	def request_handler(self,req):
		# Set Default Response to "OK"
		resp = {"source":"command_center",
			"message":"ok"}
		# Load JSON object
		if req["source"] == "discoverer":
			print "Update from Device Discoverer"
			# Add devices to database
			for d in req["devices"]:
				exists = False
				# For all devices currently in the database
				for db_d in self.db["devices"]:
					# If the same IP already exists
					if db_d["ip"] == d["ip"]:
						# Update the info
						for key in d:
							db_d[key] = d[key]
						# Break the loop
						exists = True

				# If the devices doesnt exist, add to db
				if not exists:
					self.db["devices"].append(d)
			print "Number of Devices: %d"%len(self.db["devices"])
	
		elif req["source"] == "converter":
			print "Update from converter"
		elif req["source"] == "scanner":
			print "Update from Scanner"
			self.db["movies"] = req["movies"]
			print "Number of Movies: %d"%len(self.db["movies"])	
		elif req["source"] in ["webui","cli"]:
			print "Update from WebUI/CLI"
	
		#print req
	
		return resp


	## Main Server Loop
	#
	# Main server loop.  It waits from communication from the subprocesses
	def serve_forever(self):
		while(True):
			try:
				# Accept a connection
				conn,addr = self.listener.accept()	

				# Recieve a data packet
				req = libcc.recv_json(conn)
				# Add the IP address to the request
				req["ip"] = addr

				# Handle the request
				resp = self.request_handler(req)
				# Send the response back
				libcc.send_json(conn,resp)
				# Close this connection
				conn.close()

			except TIMEOUT_ERROR:
				# Check the processes
				self.check_processes()
				self._write_db()
			except KeyboardInterrupt:
				for p in self.processes:
					libcc.terminate(p)
				break

	## Check that all the processes are running.
	#
	# If a process is not running, it will be relaunched
	def check_processes(self):
		for p in self.processes:
			if not libcc.running(p):
				# TODO Get error code from process and log why
				# the process was ended
				# Start the process and update the list
				p = libcc.start(p)
				# Break so 1 process is started at a time
				break

# Start the Command center when this script is run indepen
if __name__ == '__main__':
	# Create a Command Center Object
	cc = command_center()
	# Serve forever
	cc.serve_forever()


