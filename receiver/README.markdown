Chromecast WebApp
=================

# Introdution


# WebSocket Protocol
WebSockets are used to control the WebApp.  Google Cast's API uses its own protocol based on WebSockets.  Instead of reverse engineeering thier API, i will just use my own protocol.

The datagrams send to the WebApp will be URL encoded.  It will have the following format:

	cmd=[COMMAND]&arg1=[Argument1]&arg2=...&arg3=...

It will support the following commands:
* PLAY/PAUSE
    * Toggles the playback of the video stream
    * No Arguments Needed
* LOAD
    * Loads a video file to the Webapp Player
    * Arguments
        * path - Path to media file you are loading
* STOP
    * Stops the playback completely
    * No Arguments
* SKIP
    * Jumps to a specific point
    * Arguments
        * location - It will be in the following format [Number][Unit].  The following units will be supported:  
            * "%" - Percentage from 0 to 100
            * "s" - Seconds from 0 to video length
            * "m" - minutes from 0 to video length
* STATUS
    * Requests the current playback information
    * No Arguments
    * Returns Playback Status of the video being played


