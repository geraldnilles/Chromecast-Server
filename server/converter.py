#!/usr/bin/env python

import libcommand_center as libcc
import hashlib
import subprocess
import re
import time


#----------------
# Constants
#----------------

HTTP_SERVER_MEDIA_FOLDER = "/mnt/raid/www/media"


## Convert to a Chromecast Friendly format
#
# Checks the video and makes sure the codecs and container are supported.  If 
# not, it converts them and put a copy in the video server folder
#
# @param infile - A path to the input file (video being converted)
# @return - None
def convert(infile):

	# Create a Hash of the inFile path and use that as the filename for
	# the converted file
	name = hashlib.sha224(infile).hexdigest()
	outfile = "%s/%s.mp4" % (HTTP_SERVER_MEDIA_FOLDER,name)

	# CHeck codecs and packaging
	p = subprocess.Popen(["avconv","-i",infile],stderr=subprocess.PIPE)
	vid_info = p.stderr.read()

	print "Input Path: "+infile
	print "Output Path: "+outfile

	# Use RegEx to determine the Video/Audio/Container info
	m = re.search("Input #[0-9], (.*?),",vid_info)
	cont = m.group(1)

	m = re.search("Stream.*?Video: ([a-zA-Z0-9]*)",vid_info)
	vc = m.group(1)

	m = re.search("Stream.*?Audio: ([a-zA-Z0-9]*)",vid_info)
	ac = m.group(1)	

	m = re.search("Duration:\s([\d]*):([\d]*):([\d]*)",vid_info)
	hours = int(m.group(1))
	minutes = int(m.group(2))
	seconds = int(m.group(3))
	duration = (hours*60*60) + (minutes*60) + seconds

	print cont,ac,vc,duration


	# Based on the Codec/Containers, pick the right conversion function
	if vc == "h264":
		if ac == "aac":
			if cont in ["mov","mp4"]:
				link(infile,outfile)
			else:
				repackage(infile,outfile,duration)
		else:
			audio_repackage(infile,outfile,duration)
	else:
		video_audio_repackage(infile,outfile,duration)
	# When the convertion is complete, tell the command center to remove
	# this item from the queue

	req = {
		"cmd":"complete",
		"path":infile,
		"out":outfile
		}

	cc_communicate(req)


## Link file to Video Server
#
# If not convertion is necesary, this will creates a soft link between the 
# infile and the outfile.
#
# @param infile - Input file you are linking to the http server folder.
# @param outfile - Output path and filename
# @return the return code of th "ln" command
def link(infile,outfile):
	print "Linking File"
	# Run Command
	p = subprocess.Popen(["ln","-s",infile,outfile])
	
	return p.wait()

## Repackge file to MP4
#
# If the Audio codec and Video codec are good but the container is bad, this
# will preserve the media streams and repackage as an MP4
#
# @param infile - Input file being repackaged as an MP4
# @param outfile - Ouput file path and name
# @param duration - Duration of Input Video File (used for Percent Calculation)
# @return return code of the convertion
def repackage(infile,outfile,duration):
	
	print "Repackaging File"

	ret_code = run_with_progress(["avconv",
			"-y", # Overwrite Output File
			"-i",infile, # Specify Input File
			"-c:a","copy", # Set Audio/Video codecs to Copy
			"-c:v","copy",
			outfile], # Specify the Outpu File
			duration) # Specify the video duration
	return ret_code

## Transcode Audio to AAC and Repackage to MP4
#
# If the Video codec is good but Audio and Container are bad, this package 
# will preserve the video stream and transcode the audio.
#
# @param infile - Input file being transcoded
# @param outfile - Ouput file path and name
# @param duration - Duration of Input Video File (used for Percent Calculation)
# @return return code of the convertion process
def audio_repackage(infile,outfile,duration):
	print "Convering Audio and Repackaging"

	ret_code = run_with_progress(	["avconv",
				"-y", # Overvite output File
				"-i",infile, # Specify Infile
				"-c:a",	"libfdk_aac", # Sepecify Audio Codec
				"-vbr","3", # Specify Audio Quality
				"-c:v","copy", # Copy Video Stream
				outfile], # Specify Output File
				duration) # Specify Duration
	return ret_code

## Transcode Audio and Video.  
#
# Transcodes video to H264 and audio to x264 and packages it as an MP4
#
# @param infile - Input file being transcoded
# @param outfile - Ouput file path and name
# @param duration - Duration of Input Video File (used for Percent Calculation)
# @return return code of the convertion process
def video_audio_repackage(infile,outfile,duration):
	print "Convering Audio/Video and Repackaging"

	ret_code = run_with_progress(	["avconv",
				"-y",	# Overwrite Output File
				"-i",infile, # Specify Input File
				"-c:a",	"libfdk_aac", # AAC Audio Codec
				"-vbr","3", # Set Audio Quality to 3
				"-c:v","libx264", # h264 Video codec
				"-cbr","23", # Set Video Quality to 23
				outfile], # Specify Output File
				duration) # Specify Duration
	print ret_code

	return ret_code

## Runs a command and gets progress.
#
# Runs the command given in the cmd list.  Every 10 seconds, it parses the 
# STDOUT and figure out how much time is left.
#
# @param cmd - A list of command line program and arguments
# @return return code of the convertion process
def run_with_progress(cmd,duration):
	# Start the process
	p = subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
	# Record when the process started
	start_time = time.time()
	# Continue this loop until the process is complete.
	while(p.poll() == None):
		# Read the STDERR for 10 seconds
		out = timed_read(p,10)
		# Create a progress object
		req = {"cmd":"update"}
		req["path"] = cmd[3]
		# Use RE to parse frames and time
		m = re.search("time=\s*([\.\d]*)",out)
		if (m):	
			t = float(m.group(1))	
			req["time"] = t
			req["percent"] = t/duration*100
			req["conversion_time"] = int(time.time()-start_time)  
		else:
			# If you cant read the input
			continue
		# Send progress to Command Center, discard the response
		cc_communicate(req)
	print "Process done: "+repr(p.poll())
	# Return the REturn Code
	return p.poll() 


## Timed File Read
#
# Reads the provided file object for a set period of time.  And then returns 
# the last 100 characters.
#
# @param p - POpen object
# @param t - timeout (in seconds)
# @return The last 100 characters of the stream.
def timed_read(p,t):
	# Make the timeout with respect to Unix time
	t += time.time()
	# Output variable
	out = ""
	# Read stdout for t seconds or unitl the process is finished
	while(t > time.time() and p.poll() == None):
		out += p.stderr.read(1)

	# Trim output to be less than 100 characters
	if len(out) > 100:
		return out[-99:]
	else:
		return out


## Check the Transcoding Queue
#
# This is a wrapper for the communicate function.  It Asks for a file to 
# transcode.  This file is popped from the transcoding queue
#
# @return the file to convert.  If no file, returns None
def check_queue():
	req = {"cmd":"fetch"}

	resp = cc_communicate(req)

	return resp

def cc_communicate(req):
	req["source"] = "converter"
	print req
	# resp = libcc.send_recv(req)
	#return resp


def loop_forever():
	while(1):
		# Ask if there are any jobs
		resp = check_queue()

		# If so, convert them
		if "infile" in resp:
			convert(resp["infile"])

		# Wait 10 seconds before queueing the queu again
		time.sleep(10)
		

if __name__ == "__main__":
	loop_forever()
