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

The command center source string is as shown below:

	"source": "command_center"

The default argument will be a "message" argument which either says "OK" if all went well or it will contain an Error message if somethign went wrong.

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
Kill one of the Daemon processes


	"cmd":"kill",
	"process":"<name of process>"

* Fetch Movies
Fetches the list of movies from the database


	"cmd":"fetch",
	"type":"movies",

* Fetch TV
Fetches the list of TV shows from the database

	"cmd":"fetch",
	"type":"tv"

* Fetch Devices
    * Fetches the list of Discovered Chromecast Devices

	"cmd":"fetch",
	"type":"devices"

For all of the Fetch Oarguments,tThe Command Center's response will have the following format

	"source":"command_center",
	"data":[list of movies/tv/devices/etc...]

* Add to Transcoding Queue
    * Adds a media file to the transcoding queue.
    * This queue is used by the Converter daemon

	"cmd":"conv",
	"path":"/path/to/movie.mp4"
resp = cc_communicate(obj)
        return resp["message"]

* Remove from Transcoding Queue
    * Removes an item from the Transcoding Queue

	"cmd":"conv_cancel",
	"path":"/path/to/movie.mp4"

* Check Transcoding Status
    * Checks the conversion's status

	"cmd":"conv_status"

### Chromecast Commands
All of these packets send commands to a specific chromecast device

* Play/Pause Chromecast Video
    * Toggles between Play and Pause on the selected Chromecast Device

	"cmd":"play_pause"
	"addr":"<Chromecast IP address>"

* Load URL to Chromecast Device
    * Sends a URL to the chromecast device

	"cmd":"load"
	"addr":"<Chromecast IP address>"
	"src":"</url/path/to/video.mp4>"

* Skip Video Playback
    * Skips in the video stream to the specificed percentage

	"cmd":"skip"
	"addr":"<Chromecast IP address>"
	"percent":"<0 to 100>"

* Launch the Custom Web App
    * Launches the Custom WebApp on the specified Chromecast Device

	"cmd":"launch"
	"addr":"<Chromecast IP address>"

* Exit the Custom Web App
    * Kills the WebApp on the the specified Chromecast device and returns it to the "Ready To Cast" screen
	
	"cmd":"exit"
	"addr":"<Chromecast IP address>"

## Converter

The Converter is used to to convert video files to a Chromcast Friendly format.

The source string will look like this:

	"source":"converter"

* Fetch an Item from the Queue
    * Fetch one object from the Transcoding queue

	"cmd":"fetch"

This will return the object

	"source":"command_center",
	"data":[]

* Update the Transcoding Progress
    * Update the transcoding progress to the command center

	"cmd":"update"
	"path":"/path/to/source/video/being/converted"

* Mark a Transcoding job as complete
    * Notify the command center that the device is done

	"cmd":"complete"
	"path":"/path/to/the/infile"
	"out":"/path/to/the/outfile"



# Example
