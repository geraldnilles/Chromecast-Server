import libcommand_center as libcc

#--------------
# Constants
#--------------

class command_center:
	def __init__(self):
		# Set the Unix Socket
		self.listener = libcc.server_setup()

		# Create a list of processes
		self.processes = libcc.get_process_list()
		# Init DB
		self.db = {
				"movies":[],
				"tv":[],
				"music":[],
				"transcoding_queue":[]
				}
		# TODO Open DB from file and load existing data

	def _write_db():
		# Write DB to disk
		pass

	def request_handler(self,data):
		# Set Default Response to "OK"
		resp = "OK"
		# Load JSON object
		obj = json.loads(data)
		if obj["source"] == "discover":
			# Add devices to database
			for d in obj["devices"]:
				# TODO Check if device is in database

		elif obj["source"] == "converter":
			pass
		elif obj["source"] == "indexer":
			pass
		elif obj["source"] in ["webui","cli"]:
			pass
		
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

			except socket.timeout:
				# Check the processes
				self.check_processes()
				_write_db()

	## Check that all the processes are running.
	#
	# If a process is not running, it will be relaunched
	def check_processes():
		for p in self.processes:
			if not libcc.running(p):
				# TODO Get error code from process and log why
				# the process was ended
				# Start the process and update the list
				p = libcc.start(x)

# Start the Command center when this script is run indepen
if __name__ == '__main__':
	# Create a Command Center Object
	cc = command_center()
	# Serve forever
	cc.serve_forever()


