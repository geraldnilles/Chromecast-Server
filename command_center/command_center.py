import socket
import launcher

#--------------
# Constants
#--------------

class command_center:
	def __init__(self):
		# Set the Unix Socket
		self.LOCAL_UNIX_SOCKET = "/tmp/CommandCenterUnixSocket"
		# Create a list of processes
		self.processes = launcher.get_process_list()
		# Init DB
		self.db = {
				"movies":[],
				"tv":[],
				"music":[],
				"transcoding_queue":[]
				}
		# TODO Open DB from 

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
				# TODO Create a loop for receiving large data
				req = conn.recv(1024)
				# Handle the request
				resp = self.request_handler(req)
				# Send the response back
				conn.sendall(resp)
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
			if not launcher.running(p):
				# TODO Get error code from process and log why
				# the process was ended
				# Start the process and update the list
				p = launcher.start(x)

	## Setup the Unix Socket
	#
	# Create a Unix Socket listener
	def setup_unix_socket(self):
		# Remove Previoulsy open Unix Socket
		os.remove(LOCAL_UNIX_SOCKET)

		# Create Socket
		self.listener = socket.socket(socket.AF_UNIX, 
				socket.SOCK_STREAM)
		self.listener.bind(LOCAL_UNIX_SOCKET)
		# Allo Queuing of 10 connection
		self.listener.listen(10)
		# Set a timeout of 5 seconds
		self.listener.settimeout(5)


# Start the Command center when this script is run indepen
if __name__ == '__main__':
	# Create a Command Center Object
	cc = command_center()
	# Setup the Unix Socket
	cc.setup_unix_socket()
	# Serve forever
	cc.serve_forever()


