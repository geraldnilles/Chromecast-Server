import subprocess

#-------------
# Constants
#-------------

## The default process list
processes = [
	{
		"name":"test",
		"cmd":["C:\Python2.7\python.exe","test.py"],
		"proc":None
	}	
	]


def get_process_list():
	return processes


# Checks if a process is running
def running(process):
	if process["proc"].poll()== None:
		return True
	else:
		return False

# Starts the process
def start(process):
	# Launch process
	p = subprocess.Popen(process["cmd"])
	# Add the Popen object to the process object
	process["proc"] = p


def teminate(process):
	process["proc"].terminate()

def kill(process):
	process["proc"].kill()


