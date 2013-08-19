GoogleCast Protocol
===================

# Introduction
The GoogleCast protocol is used to send Web Apps to Chromecast devices.  These web apps are written in HTML/JS/CSS and are capable of doing anything you do in a Web Browser.  

While Google has released APIs for iOS, Android, and Chrome, it has not openly released documentation on the protocol which Chromecast uses.  In this document, I will document my attempt to reverse engineer the protocol.  

## Disclaimer
The information below has not been confirmed.  The sections below are based on a what i have found when searching the web.  Some of the info has been confirmed by looking at source code, some has been confirmed through experimentation, and some is simply an educated guess.  Please do not quote me on any of this.

# Overviews 

## Device Services Overview
First, we will analyze what services are currently being run on each device

* Receiver Device (Chromecast)
    * Android Operating System
        * DIAL Server  
            * **DIAL Service Discovery** - This is used to discovery the Chromecast device.
            * **DIAL REST Service** -  This is used to launch Web Apps on the Chromecast device.
        * Chrome Browser 
            * This is a regular Chrome browser.  Once the Web App is loaded, it is ran in this browser. 

* Sender Device
    * DIAL Client
        * This is used to disover Chromecast devices and Launch apps on the Chromecast devices
    * UDP Socket Interface
        * This is used to interface with the Web App's WebSockets.  Play, Pause, and Seek commands are sent via WebSockets


## Launching A Web App Overview
This section will cover all of the steps required to launch a WebApp on A Chromecast Device.

1. Chromecast boots
    * DIAL Server is Running and waiting to receive a Web App
    * Chrome Browser is running and displaying the "Ready to Cast" screen
2. Sender Searches for Chromecast devices using DIAL Service Discovery
    * Sender sends an M-SEARCH request.   
3. Chomecast responds to search request using DIAL Service Discovery 
    * The device responds to inform the Sender of its IP address and Friendly name (ie "Family Room Chromcast")
3. Sender Attempts to Launch a Web App on the Chromecast using the DIAL REST protocol
    * The App-ID is sent to the Chomecast Device
4. Chromecast fetches the Web App URL from Google's Servers
    * The App-ID is sent to Google's server and Google's server responds with the Web App's URL
    * The use of Google Servers is what gives them control over the apps that people and use 
5. Chromecast Loads the Web App URL using the Chromecast Web Browser
    * Loads the HTML, CSS, and Javscript
6. Sender and Chromecast create a WebSocket connection.
    * This connection is used to send playback commands to the Chromecast

# Protocol Details

## Chromecast Discovery
The DIAL discovery is used to discovery new Chromecast device on the network 

* M-Search Request
    * This is sent over UDP on the multicast address 239.255.255.250 and port 1900.
* M-Search Response
    * Chromecast responds with a LOCATION header that contains the Chromecasts IPv4 address
* Device Description Request
    * Sender asks for more information about the device
* Device Description Response
    * Chomecast responds with details.  including the Chromecast's name

## Web App Launch
The DIAL REST is used to launch Web applications on the Chromecast.

* Launch Request
    * Sender asks for the Chromecast to Launch the provided App
    * The App-ID is used
* Fetch Web App URL
    * Chromecast sends App-ID to google's servers.  Google responds with the Web App's URL
* Load Web App's URL
    * URL is loaded into the Chromecast Browser
* Launch Response
    * Chromecast confirms that the App was launced

## WebSocket Commands
Once the Web App is loaded on the Chromecast, WebSockets are used to send playback commands to the Chromecast device.  Some examples of playback commands are Play, Pause, and Seek.

The exact commands are no known at this time, but we can probably figure them out by looking at the GoogleCast Chrome App source code.  The Chrome App is 100% javascript. However, the variables are renamed to make it difficult to read.  Its kind of annoying, but it'll work.
  
Google provides an API for these playback commands. However, it is technically possible to create your own API for controlling yoru Web App.  

# Potential Road Blocks

## App ID 
In order to launch applications, you will need Google to assign you an App ID.  The App ID is essentially a look-up code.  When the Chromecast is given an App ID, it gives a Google Server the App ID and google provides the Web App's URL.  This means that Google controls the platform and could potentailly block this product from happening.   

### Workaround
One way to get around this would be to setup a DNS or Proxy server.  When Chromecast attempts to fetch Web App URLs, you could intercept the request and respond with your app.  This is a little jenky, but it is possible.

Also, if google provides an App ID that redirects to a Local URL (192.168.\*.\*), that would also be cool since multiple people could use the same. 

The finally option would be to wait for Chromecast to get hacked and modify the app lauching code to skip this portion of the code.


