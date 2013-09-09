Chromecast WebApp
=================

# Introdution
This HTML is loaded onto the Chromecast's browser.  This page will contain the video player.

# Apps

## Hello World
The goal of this app is just to display a message on my TV via Chromecast.

## main.html
This will be the main video playing app

# Page Style
By default, the background color is black.  Therefore, if your app uses black text without changing the background color, you wont see anything.  

# Custom WebSocket Protocol
WebSockets are used to control the WebApp.  Google Cast's API uses its own protocol based on WebSockets.  Instead of reverse engineeering thier API, i will just use my own protocol.  Eventually, i may spend the time to reverse engineer the Chromecast protocol, but I'm lazy.

In general, WebSockets is built on TCP packets.  TCP is a continuous communication protocol.  By itself, TCP does not communicate how large the message will be.  Other TCP based protocols (like HTTP) get around this by sending a header that communicates how large the message is.  WebSocket also adds a header to communicate the header size.  WebSocket uses a fixed size binanry header.

The rest of the packet (after the fixed-sized header) will consist of a JSON string.  In general, it will have the following format

	{
		cmd:[Command String],
		[arg1_key]:[arg1_value],
		[arg2_key]:[arg2_value],
		...
		[argN_key]:[argN_value]
	}

Every JSON packet will contain a "cmd" entry.  This will communicate which command they want to run on the Chomecast.  The number of other entries will depend on which command is sent.


It will support the following commands:
* PLAY/PAUSE
    * Toggles the playback of the video stream
    * Arguments
        * None
    * Returns
        * "OK" if successful
        * [ERROR Message] if not successful

* LOAD
    * Loads a video file to the Webapp Player
    * Arguments
        * path - Path to the video URL
    * Returns
        * "OK" if successful
        * [ERROR Message] if not successful

* STOP
    * Stops the playback completely
    * Arguments
        * None
    * Returns
        * "OK" if successful
        * [ERROR Message] if not successful

* SKIP
    * Jumps to a specific point in the video stream
    * Arguments
	* You must send one of the following arguments
        * percent - Percent of the stream you want to jump to (optional)
	* seconds - Number of seconds you want to jump to (optional)
    * Returns
        * "OK" if successful
        * [ERROR Message] if not successful

* STATUS
    * Gets the status of the playback 
    * Arguments
        * None
    * Returns
        * playback - Play or Pause
        * percent - Percent into the video
        * seconds - Number of seconds into the video
        * path - Current video path being played


