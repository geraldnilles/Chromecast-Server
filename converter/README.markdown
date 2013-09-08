Media Manager
===============

# Introduction
The Media Manager will be a daemon process that prepares media files for Chromecasting.  It will have 2 major function:

1. Look for Media files on the server
2. COnvert media files for streaming when requested

## Big Picture
A user will look for a video to play.  When the user clicks a video, a message will be sent to this daemon process to prepare that video for Chromecasting.  The user can then ask for status of the conversion (this will allow us to add a status bar in the WebUI).

Once the process is complete, the user will be able to stream the video.

# IPC
Unix ports will be used to send messages to this daemon.

The protocol will likely be UDP and contain a JSON string containing the request and response data. 

# Media Database

# Conversions

## Link to Streaming Directory
If the Audio codec, video codec, and container are all valid, this will simply create a soft link from the source file to the streaming directory.

## Repackage
If the codecs are right but the container is wrong, this type of conversion will repackage the media file accordingly.  It will essentailly strip the audio and video data, put them into a supported container (likely MP4) and store it in a temp folder. 

The target time for repackaging a movie is 30 seconds. 

## Audio Transcode
If the video codec is right, but the audio codec is wrong, we will need to transcode the audio track.  

The target time for transcoding the audio is 2 minutes.

## Full Transcode


