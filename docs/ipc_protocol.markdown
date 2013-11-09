IPC Protocol
============

# Introduction
The command center communicates with its other daemon processes using Inter process communication.  It sends JSON string over Unix sockets.  This document will detail the protocol.

# Format

	{
		"source":"<daemon_name>",
		"[arg1]":"[data1]",
		"[arg2]":"[data2]",
		"[arg3]":"[data3]"
	}

Every packet must contain the "source" key-value pair.  The remaining args depend on the source of the packet.

## Command Center

All messages from the Command center will have the following format:

	"source": "command_center",
	"message":"<string describing message>",
	["data":JSON Object containing the requested data"]

All messages will have the "command\_center" source and a message.  The message will contain "OK" if all went well or an Error code if not.  If additional data is requested, the optional "data" field can contain hold it.  

## CLI/Web UI

The Command Center and the WebUI both control the command center.  Therefore, their arguments will be very similar (if not exactly the same)

The source string for the CLI will be:

	"source":"cli"

The source string for the Web Ui will be:

	"source":"webui"

As for the arguments, there will be subcategories of commands: Database commands and Chromecast Commands

### Database Commands

All of these packets send commands to the Command Center Database.

* Stop a Daemon

Kill the daemon process sepecified by the "process" field.  Keep in mind that the Command Center will auto-start all processes that have stopped.  Therefore, all stopped daemons will automaticaly restart. If the process field is "all", all daemons will be killed and restarted.

	"cmd":"kill",
	"process":"<name of process>"

* Fetch Movies

Fetches the list of movies from the database.

	"cmd":"fetch",
	"type":"movies",

The response will populate the "data" field will a list of Movie dictionaries.

* Fetch TV

Fetches the list of TV shows from the database

	"cmd":"fetch",
	"type":"tv"

The response will populate the "data" field with a list of TV dictionaries.

* Fetch Devices

Fetches the list of Discovered Chromecast Devices

	"cmd":"fetch",
	"type":"devices"

The response will populate the "data" filed with a list of devices dictionaries.


* Add to Transcoding Queue

Adds a media file to the transcoding queue. This queue is used by the Converter daemon to determine which videos to work on

	"cmd":"conv",
	"path":"/path/to/movie.mp4"


* Remove from Transcoding Queue

Removes an item from the Transcoding Queue.  

	"cmd":"conv_cancel",
	"path":"/path/to/movie.mp4"

* Check Transcoding Status

Checks the status of the current conversion queue.

	"cmd":"conv_status"

The response populates the data field with a list of items in the conversion queue as well as the current conversion status (Percent complete)

### Chromecast Commands
All of these packets send commands to a specific chromecast device

* Play/Pause Chromecast Video

Toggles between Play and Pause on the selected Chromecast Device

	"cmd":"play_pause"
	"addr":"<Chromecast IP address>"

* Load URL to Chromecast Device

Sends a URL to the chromecast device

	"cmd":"load"
	"addr":"<Chromecast IP address>"
	"src":"</url/path/to/video.mp4>"

* Skip Video Playback

Skips in the video stream to the specificed percentage

	"cmd":"skip"
	"addr":"<Chromecast IP address>"
	"percent":"<0 to 100>"

* Get Playback Status

Reads the current playback stats from the chromecast device specified.

	"cmd":"status"
	"addr":"<Chromecast IP address>"

The response will populate the data field with a playback statistics.  The data includes current url being played, whether or not its paused, and the percent played.

* Launch the Custom Web App

Launches the Custom WebApp on the specified Chromecast Device

	"cmd":"launch"
	"addr":"<Chromecast IP address>"

* Exit the Custom Web App

Kills the WebApp on the the specified Chromecast device and returns it to the "Ready To Cast" screen
	
	"cmd":"exit"
	"addr":"<Chromecast IP address>"



## Converter

The Converter is used to to convert video files to a Chromcast Friendly format.

The source string will look like this:

	"source":"converter"

* Fetch an Item from the Queue

Asks the command center if there is a file that needs transcoding.

	"cmd":"fetch"

The response will populate the data field with a path to the file being transcoded.  

* Update the Transcoding Progress

Updates the command center's transcoding queue with convesion status.  This allows the command center to know how long until a device is ready to cast.

	"cmd":"update"
	"path":"/path/to/source/video/being/converted"
	"percent":[percent complete],

* Mark a Transcoding job as complete

Notifies the command center that transcoding has completed.

	"cmd":"complete"
	"path":"/path/to/the/infile"


## Media Scanner
The Media Scanner is used to search the filesystem for new media files that can be streamed to the chromecast.  This daemon periodically scans the filesystem looking for specific file extensions.  It generates a JSON object containing all of the database info and sends it back to the command center.  

The source string will look like this 

	"source":"scanner"

There is only one type of communication so there is no need for a 'cmd" field.

* Update Database

Sends a database object to the command center.  
	
	"movies":[list of movie dictionaries]
	"tv":[list of tv dictionaries]
	"music:["list of music dictionaries"]
	"pictures:["list of picture dictionaries"]


## Discoverer
The discoverer daemon is used to search for Chromecast devices on the network.  After finding devices, it returns a list back to the command center.

The source string will look like this

	"source":"discoverer"

There is only one type of communication, so there is no need for a "cmd" field.

* Update Database

Sends a list of devices to the command center.  

	"devices":[list of device dicts]


