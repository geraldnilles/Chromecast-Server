import libcommand_center as libcc


## Convert to a Chromecast Friendly format
#
# Checks the video and makes sure the codecs and container are supported.  If 
# not, it converts them and put a copy in the video server folder
#
# @param s - Socket object pointing to the Command Center.  This will be used 
# 	to send updates
# @param infile - The filename of the video file you are converting
# @return - 
def convert(infile):
	# CHeck codecs and packaging
	"avconv -i infile"
	vc = ""
	ac = ""
	cont = ""
	if vc == "x264":
		if ac == "aac":
			if cont == "mp4":
				link(infile)
			else:
				repackage(infile)
		else:
			audio_repackage(infile)
	else:
		video_audio_repackage(infile)
	# When the convertion is complete, tell the command center to remove
	# this item from the queue
	send_update({"complete":infile})

## Link file to Video Server
#
# If not convertion is necesary, this will creates a soft link between the 
# infile and the outfile.
#
# @param s - Socket object pointing to the Command Center (probably not needed)
# @param infile - Input file you are linking to the http server folder.
# @return the return code of th "ln" command
def link(infile):
	# Tell the Command Center that The file is being linked
	send_update("Linking file to http folder")
	#
	outfile = "%s/%s.mp4" % (HTTP_SERVER_MEDIA_FOLDER,infile)
	# Run Command
	ret_code = run_with_progress(["ln","-s","infile",outfile])
	return ret_code

## Repackge file to MP4
#
# If the Audio codec and Video codec are good but the container is bad, this
# will preserve the media streams and repackage as an MP4
#
# @param s - Socket Object pointing to the Command Center
# @param infile - Input file being repackaged as an MP4
# @return return code of the convertion
def repackage(infile):
	send_update("Repackaging file to MP4 (No transcoding)")
	outfile = "%s/%s.mp4" % (HTTP_SERVER_MEDIA_FOLDER,infile)
	ret_code = run_with_progress(["avconv","-i",infile,"-a:c","copy",
			"-v:c","copy",outfile])
	return ret_code

## Transcode Audio to AAC and Repackage to MP4
#
# If the Video codec is good but Audio and Container are bad, this package 
# will preserve the video stream and transcode the audio.
#
# @param s - Socket Object pointing to the command center
# @param infile - Input file being transcoded
# @return return code of the convertion process
def audio_repackage(infile):
	send_update("Transcoding Audio to AAC.")
	outfile = "%s/%s.mp4" % (HTTP_SERVER_MEDIA_FOLDER,infile)
	ret_code = run_with_progress(	["avconv","-i",infile,"-a:c",
		"lib_fdk_aac","-vbr","3","-v:c","copy",outfile])
	return ret_code

## Transcode Audio and Video.  
#
# Transcodes video to H264 and audio to x264 and packages it as an MP4
#
# @param s - Socket Object pointing to the command center
# @param infile - Input file being transcoded
# @return return code of the convertion process
def video_audio_repackage(infile):
	send_update("Transcoding Audio to AAC and Video to H264.")
	outfile = "%s/%s.mp4" % (HTTP_SERVER_MEDIA_FOLDER,infile)
	ret_code = run_with_progress(	["avconv","-i",infile,"-a:c",
		"lib_fdk_aac","-vbr","3","-v:c","libx264","-cbr","23",outfile])
	return ret_code

## Runs a command and gets progress.
#
# Runs the command given in the cmd list.  Every 10 seconds, it parses the 
# STDOUT and figure out how much time is left.
#
# @param s - Socket Object pointing to the command center
# @param cmd - A list of command line program and arguments
# @return return code of the convertion process
def run_with_progress(cmd):
	# Start the process
	p = subprocess.Popen(cmd,stdout=subprocess.PIPE)
	# Record when the process started
	start_time = time.time()
	# Continue this loop until the process is complete.
	while(p.poll == None):
		# Sleep for 10 seconds
		time.sleep(10)
		# Grab the Standard output and error text
		stdo,stde = p.communicate()
		# Create a progress object
		progress = {}
		# Jump to the last line of the standard output
		# Use RE to parse frames and time
		# If possible, calcualte percentage (time/totoal time)
		progress["percent"] = 0
		progress["conversion_time"] = time.time()-start_time
		# Send progress to Command Center
		send_update(progress)

	# Return the REturn Code
	return p.poll() 

def new_msg():
	msg = {}
	msg["source"] = "converter"
	return msg

## Check the Transcoding Queue
#
# This is a wrapper for the communicate function.  It Asks for a file to 
# transcode.  This file is popped from the transcoding queue
#
# @param s - Socket object pointing to the command center
# @return the file to convert.  If no file, returns None
def check_queue():
	req = new_msg()
	req["request"]="jobs"

	resp = libcc.client_send_recv(req)
	if "infile" in resp:
		return resp
	else:
		print "Error Communicating with Command Center: "+repr(resp)
		return resp

## Sends a status update to the Command Center
def send_update(message):
	req = new_msg()
	req["status"]=message

	resp = libcc.client_send_recv(req)
	return resp


def start_daemond():
	while(1):
		# Ask if there are any jobs
		job = check_queue()

		# If so, convert them
		if "infile" in job:
			convert(job["infile"])


		time.sleep(5)
		

if __name__ == "__main__":
	start_daemon()
