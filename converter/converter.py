

## Convert to a Chromecast Friendly format
#
# Checks the video and makes sure the codecs and container are supported.  If 
# not, it converts them and put a copy in the video server folder
def convert(s,infile):
	# CHeck codecs and packaging
	"avconv -i infile"
	vc = ""
	ac = ""
	cont = ""
	if vc == "x264":
		if ac == "aac":
			if cont == "mp4":
				link(s,infile)
			else:
				repackage(s,infile)
		else:
			audio_repackage(s,infile)
	else:
		video_audio_repackage(s,infile)
	# When the convertion is complete, tell the command center to remove
	# this item from the queue
	send_update({"complete":infile})

## Link file to Video Server
#
# If not convertion is necesary, this will 
def link(infile):
	"ln -s infile /mnt/raid/www/media/infile"

## Repackge file to MP4
#
# If the Audio codec and Video codec are good but the container is bad, this
# will preserve the media streams and repackage as an MP4
def repackage(infile):
	"avconv -i infile -a:c copy -v:c copy /mnt/raid/www/media/infile"

## Transcode Audio to AAC and Repackage to MP4
#
# If the Video codec is good but Audio and Container are bad, this package 
# will preserve the video stream and transcode the audio.
def audio_repackage(infile):
	"avconv -i infile -a:c lib_fdk_aac -v:c copy /mnt/raid/www/media/infile"

## Transcode Audio and Video.  
#
# Transcodes video to H264 and audio to x264 and packages it as an MP4
def video_audio_repackage(infile):
	"avconv -i infile -a:c lib_fdk_aac -v:c libx264 /mnt/raid/www/media/infile"

## Runs a command and gets progress.
#
# Runs the command given in the cmd list.  Every 10 seconds, it parses the 
# STDOUT and figure out how much time is left.
def run_with_progress(s,cmd):
	p = subprocess.Popen(cmd,stdout=subprocess.PIPE)
	start_time = time.time()
	while(p.poll == None):
		time.sleep(10)
		stdo,stde = p.communicate()
		progress = {}
		# Jump to the last line.
		# Use RE to parse frames and time
		# If possible, calcualte percentage (time/totoal time)
		progress["percent"] = 0
		progress["conversion_time"] = time.time()-start_time 
		send_update(s,progress)

	# Return the REturn Code
	return p.poll() 


## Communicate with Command Center
#
# Sends a message back to the Command Center
def communicate(s,msg):
	try:
		s.connect(LOCAL_UNIX_SOCKET)
		if type(msg) != str:
			msg = json.dumps(msg)

		s.sendall(msg)
		data = s.recv(1024)
		ret = json.loads(data)
	except socket.timeout:
		ret = {"error":"timeout"}
	return ret

## Check the Transcoding Queue
#
# Asks the Command center if there are items left on the Queue
def check_queue(s):
	req = {
			"source":"converter",
			"request":"job"
		}
	return communicate(s,req)

## Sends a status update to the Command Center
def send_update(s,message):
	req = {
			"source":"converter",
			"status":message
			}
	return communicate(s,req)

def start_daemond():
	s = socket.socket(socket.AF_UNIX,socket.SOCK_STREAM)
	s.settimeout(5)
	while(1):
		# Ask if there are any jobs
		job = check_queue(s)
		# Close the connection
		s.close()

		# If so, convert them
		if "infile" in job:
			convert(s,job["infile"])


		time.sleep(5)
		

if __name__ == "__main__":
	start_daemon()
