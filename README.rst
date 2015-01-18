###################
 Chromecast Server
###################

Update
======

I am changing the direction of this project because of the new Chrome Browser for Android.  Now, any HTML5 video on the web can be Google Casted to a chromecast.  In other words, most of the work has been done.  Now, we just need to make our server look like an Android Chrome browser and we can send any video (with the right codecs) to the chromecast.


Packet Sniffing
===============

Projection
----------

I havent busted out Wireshark yet, but just by looking at the protocol, i can guess how the handshake works.

1. Server Searchs for Chromecast
2. Chromecast Responds and Provides device details
3. Server Requests that the Chomecast launches the Chome Video app. This request contains a URL to the video we want to watch
4. Chromecast gets the Chrome Video App from Google's Servers and begins video playback
5. WebSocket Link is established between the the Chrome App and the Server that allows volume/seek/play/pause functionality. 




