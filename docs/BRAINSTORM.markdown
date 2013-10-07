Brainstorm
==========

# Introduction
This page will act as a dropping zone for ideas, concepts, or data that has not been implemented yet.

# Process Manager
As of 9/9/2013, i have most of the individual peices of the project working.  I can launch Chromecast Apps via DIAL.  I created my own Chromecast app.  I can serve video to my Chromecast app.  And i can control the Chromecast app through Websockets.  When i start to think about comibning all of these peices, i am starting to realized that managing all of these separate peices will be tricky.  

In order to run well, this project will need multiple processes.  If this was a single process, we would have to wait while videos were transcoded before we could send a websocket command which would suck.  Unfortunately, with multithreading comes headache because of interprocess communication (IPC).

This section will contain my ideas for managing all of the peices of this project.  

## Command Center
Without thinking about it too much, i think i'll need a "COmmand Center" process.  This would essentially replace the 3 or 4 terminals worth of command lines processes i need to run the project currently.

Command Center Responsibilities
* Spawn and Kill other processes
* Be the Hub for all Interprocess communication (IPC).
* Maintain a shared database (in memory) that all processes can use to communicate status.
    * Pending message
    * Transcoding process
    * Discovered Chromecast Devices
    * Subprocess PIDs (to determine if they are still running)

### Brain Dump
* Device Discovery Daemon
    * Periodically Runs DIAL discovery to find new Chromecast devices
    * After a discovery is completed, the daemond will report the device list to the Command cetner.  The command center will keep this list in the database so other processes can access it.
    * If an "On-Demand" refresh is needed, the Command center can Kill and respawn the daemon.  
    * Communication is done using the Command Centers Unix Socket Server.  
* Transcoding Process
    * Transcodes Videa/Audio/Container to codec/format supported by Chromecast
    * The Transcoding process will be spawned by the Command Center.
    * The Progress of the transcoding will be sent backt to the Command Center using the Unix Socket server.
    * The Command center can stop transcoding by killing the process.  
* WebSocket Daemon
    * Keeps a WebSocket connection open with a Chromecast devices.  Keeps the connection alive.
    * Unlike the other cases, the Command center will act as a Unix Socket client when talking with thie process. 
* FastCGI Daemon
    * This hosts the dynamic portions of the Web Interface.
    * Command center will make sure this WebApp is running
    * This app will queery the Command Center's Unix Socket server for info
    * HTTP requests will be independant of the command center
* Media Indexer
    * Browses the folders for video, audio, and images. 
    * Items found will be added to the Command Center's database using the Unix Socket Server.

So based on this, we can share 1 Unix Socket Server for the majority of the communication.  The only exception is when communicating with the WebSocket Daemon (which will be a Unix Socket client).  Since the Main Unix socket is shared, all daemons should avoid keeping the socket open for an extended period of time. 

Pseudo Code:
	Setup Unix Socket
	Start Server ... allow for 10 listeners
	Set timeout to 5 seconds

	while(1):
		try:
			msg = sock.recv(1024)
			resp = "OK" #Set the default response to "OK"
			if msg is from Device Discovery Daemon:
				Parse Devices from msg
				Store devices in Database
			elif msg is from Transcoding Process:
				Update transcoding status in Database
			elif msg is from Media Indexer:
				Add new media files to the Database
			elif msg is from FastCGI Server (or CLI):
				Perform the action requested by the FastCGI server 
				 - or - 
				Use the database to prepare a response
			else:
				print an error to the log
		except socket.timeout:
			See if any subprocesses crashed and respawn if needed
			Write database to disk


Since we are sharing a unix socket, we will need a protocol that identifies the source of the  message.  I am thinking JSOn will be the simplest option

	{
		"source" : "discoverer",
		"devices" : "list of devices"
	}
	
 
	{
		"source":"transcoder",
		"progress": "50%"
	}

	{
		"source":"indexer",
		"media":[List of media dictionaries to add]
	}

	{
		"source":"webUI",
		"get":"devices"
		-- or --
		"get":"media",
		"filter":"Regex of a search filter"
		-- or --
		"control":"pause/play"
		-- or --
		...
	}

# Phone to Chromecast
Another thing people will want to do is send media files locally stored on their phone to the chromecast.  

One solution would be to add an "Upload" option to the Server's WebUI.  Then any video, audio, music can be uploaded, transcoded on the server, and added to the play queue.  

# Chromecast Supported Media Formats

The major downside of Chromecast (and probably the main reason its so cheap) is that it only supports a small number of codecs.  
* Video
    * H264, VP8
* Audio
    * AAC, OPUS, MP3
* Containers
    * MP4, WebM,MPEG-DASH, SmoothStreaming
* Containers
    * TTML
    * WebVTT

# Transcoding
You cannot assume that every media file will be the correct format.  Therefore, we will need some sort of transcoding engine that prepares video for Casting.

When an un-supported media file is selected, it will be put into a transcoding queue.  All transcoded files will be stored in a /tmp directory.  This /tmp directory will kind of act like a fixed-size FIFO.  When the size limit is exceeded, it will delete the oldest transcoded file.

If possible, i will also start streaming the partial video file as soon as transcoding starts.  That would avoid any lag between when the media file is selected and when it starts playing.  That would also allow me to stream Live video my my HDHomeRun Tuner in the future.

I also found that PCI decoder cards exist.  Broadcomm sells an H264 decoder card on Amazon for $12.  Im thinking that we could istall these PCI cards in the server and use them to transcode the video without drawing many watts of power.  

## Archiving Codec
Currently, I archieve all my video using the H264 codec.  This is because it is a relatively efficient codec that all of my frontend devices can decode.  If we add on-the-fly transcoding, we would be able to archive my video using the Next-Gen codecs (HEVC or VP9) before the HW support comes

## Transmitting Codec
The exact codec we transcode to (ie. the Target Codec) is currently TBD.

The safest choice would be MP4+H264+AAC.  However, the encoding tools are all non-free.

My thoughts are that since WebM is essentially an MKV container, why not put H264 and OPUS in there?  It wouldnt technically be a WebM file, but since the decoding engine is there, it is technically possible.  

# Encryption
Another service this server could provide is encryption.  All media files could be encrypted using AES256.  When the user opens the webpage, he/she will be asked to enter the encryption password.  If the password is correct, the webserver will be able to decrypt the data and serve it to the Chromecast or Computer.  

This would be useful for parental filtering.  You could give your children the password for the general content and hide the mature content from them.

This would also be useful for document backup.  You could encrypt all of your taxes and bill information.

## Separate Partitions
Each password will unlock a subset of content.  You could have 1 password for general content, a seprate password for R movies, and a separate password for Tax documents.  When the user enters the password, only the content that he/she has access to will show up.   

# Google API Examples
## Sender Application
This is the web application run on the phone or table.   

It will ask Google's servers for Chromecast devices on my network.  After it recieves the list, the user can select which device it wants to send to.  Finally, it will ask the user what video to play.

	https://developers.google.com/cast/chrome_sender

## Reciever Application

	https://developers.google.com/cast/developing_your_receiver


