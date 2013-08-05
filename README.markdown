Chromecast Server
=================

# Goal
Create a server applications that sends video files to my Chromecast device.

# Overview
1. Server Hosts A WebUI showing all of the avaiable movies
2. User Selects a Movie to Watch.  
3. Chromecast Starts streaming that video from the local server.  

# Roll-Out Plan
1. Create Web Server that uses Byte Ranges
2. Send Video to my ChromeCast
    * Use Chromecast API
    * Launch Video
3. Control PLayback of Video (Play, Pause, Volume)
4. Create SImple UI for selecting and sending a video
5. Create a convertion script
    * Automatically repackages video as an MP4 for streaming

# HTTP Ranges
1. User Requests a Video File
    * Range: 0-
        * Request the entire video
2. Server Respondse by Sending the begining to send video file
    * Status Code is 206 - Partial Content
    * Accept-Ranges: bytes
        * Tells the player that it accepts byte ranges
    * Content-Length: 5000
        * Tell the player how big the video is
    * Content-Range 0-4999/5000
3. User Requests a specific byte range (skipping ahead)
    * Range: 1000-5000
        * Player tells the server where it jumped to
4. Server Sends Byte Range
    * Content-Range: bytes 1000-4999/5000
        * Server tells the player how much it is sending
    * Content-Length: 4000

Note:  The "Connection: Keep-Alive" might be important.  According to Wikipedia, its always enabled. 

 
# Sender Application
This is the web application run on the phone or table.   

It will ask Google's servers for Chromecast devices on my network.  After it recieves the list, the user can select which device it wants to send to.  Finally, it will ask the user what video to play.

	https://developers.google.com/cast/chrome_sender

# Reciever Application

	https://developers.google.com/cast/developing_your_receiver

