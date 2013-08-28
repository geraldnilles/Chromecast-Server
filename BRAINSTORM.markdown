Brainstorm
==========

# Introduction
This page will act as a dropping zone for ideas, concepts, or data that has not been implemented yet.


# Phone to Chromecast
Another thing people will want to do is send media files locally stored on their phone to the chromecast.  

One solution would be to add an "Upload" option to the Server's WebUI.  Then any video, audio, music can be uploaded, transcoded on the server, and added to the play queue.  

# HTTP Byte Ranges
This is needed if we want to skip ahead in video streams

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


