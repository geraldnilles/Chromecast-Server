GoogleCast Protocol
===================

# Introduction
The GoogleCast protocol is used to send Web Apps to Chromecast devices.  These web apps are written in HTML/JS/CSS and are capable of doing anything you do in a Web Browser.  

While Google has released APIs for iOS, Android, and Chrome, it has not openly released documentation on the protocol which Chromecast uses.  In this document, I will document my attempt to reverse engineer the protocol.  

# Device Services Overview
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

TODO Figure out if there is a spcial APP-ID that points to a local IP Address  

Note: If google doesnt give me an AppID, i could just setup Firewall that redirects one of the Test Apps to my local server.  

## Data Exchange
1. Chromecast Boots - Ready to Cast
    * DIAL Server Running
    * Chrome Running
2. Sender Searches for Chromecast device using the DIAL protocol
    * DIAL Service Discovery is used to find the Chromecast.  It is based on SSDP (UPnP)
3. Sender Attempts to Launch a WebApp on the Chromecast using the DIAL protocol
    * DIAL REST Serice is used to launch applications.  It is based on HTTP
    * The AppID of the app you wish to launch is sent to the Chromecast
4. Chromecast Fetches the WebApp form Google's Servers
    * Forwards the App ID to Google's server and recieves the appropriate URL
    * This use of Google Servers is what gives them control over the apps 
5. Chromecast Loads the WebApp usin the provided URL
    * Loads the HTML, CSS, and Javscript
    * Attemps to Start a WebSocket connection
6. Sender and Chromecast create a WebSocket connection.
    * Now the Sender can Play, Pause, Skip, Load new media, etc... 
            * This server allows sender devices on the network to discover the Chromecast device.  The sender broadcasts a multi-cast message to the entire network and looks for response.  This is based on SSDP.  
            * Once found, this server also launches applications on the Receiver's Chome Browser 
        * Chrome Browser 
            * This is a regular Chromebrowser.  The DIAL server receives a request to launch an App and the server loads the appropriate webapp on the browser. 
            * The exact URL for the webapp is stored on Google's servers.  When you whitelist your device, you provide URLs to your apps.  Google responds with an App ID.  When you ask to launch this App ID, the Chromecast, asks Google's Servers for the appropriate app URL.  This is how Google controls the available apps
            * Once the App is loaded, a websocket is opened between the Host and Reciever    

* Sender Device
    * HTTP Interface
        * Finds devices using the DIAL protocol
        * Launches Web Apps using DIAL protocol
    * UDP Socket Interface
        * Sends WebSocket communication once the Web App is laoded

TODO Figure out if there is a spcial APP-ID that points to a local IP Address  

Note: If google doesnt give me an AppID, i could just setup Firewall that redirects one of the Test Apps to my local server.  

## Data Exchange
1. Chromecast Boots - Ready to Cast
    * DIAL Server Running
    * Chrome Running
2. Sender Searches for Chromecast device using the DIAL protocol
    * DIAL Service Discovery is used to find the Chromecast.  It is based on SSDP (UPnP)
3. Sender Attempts to Launch a WebApp on the Chromecast using the DIAL protocol
    * DIAL REST Serice is used to launch applications.  It is based on HTTP
    * The AppID of the app you wish to launch is sent to the Chromecast
4. Chromecast Fetches the WebApp form Google's Servers
    * Forwards the App ID to Google's server and recieves the appropriate URL
    * This use of Google Servers is what gives them control over the apps 
5. Chromecast Loads the WebApp usin the provided URL
    * Loads the HTML, CSS, and Javscript
    * Attemps to Start a WebSocket connection
6. Sender and Chromecast create a WebSocket connection.
    * Now the Sender can Play, Pause, Skip, Load new media, etc...While Google has release APIs for iOS, Android, and Chrome, it has not openly released documentation on the protocol which Chromecast uses.

## Software
* Receiver Device (Chromecast)
    * Android Operating System
        * Web Server (DIAL Protocol) - 
            * This server allows sender devices on the network to discover the Chromecast device.  The sender broadcasts a multi-cast message to the entire network and looks for response.  This is based on SSDP.  
            * Once found, this server also launches applications on the Receiver's Chome Browser 
        * Chrome Browser 
            * This is a regular Chromebrowser.  The DIAL server receives a request to launch an App and the server loads the appropriate webapp on the browser. 
            * The exact URL for the webapp is stored on Google's servers.  When you whitelist your device, you provide URLs to your apps.  Google responds with an App ID.  When you ask to launch this App ID, the Chromecast, asks Google's Servers for the appropriate app URL.  This is how Google controls the available apps
            * Once the App is loaded, a websocket is opened between the Host and Reciever    

* Sender Device
    * HTTP Interface
        * Finds devices using the DIAL protocol
        * Launches Web Apps using DIAL protocol
    * UDP Socket Interface
        * Sends WebSocket communication once the Web App is laoded

TODO Figure out if there is a spcial APP-ID that points to a local IP Address  

Note: If google doesnt give me an AppID, i could just setup Firewall that redirects one of the Test Apps to my local server.  

## Data Exchange
1. Chromecast Boots - Ready to Cast
    * DIAL Server Running
    * Chrome Running
2. Sender Searches for Chromecast device using the DIAL protocol
    * DIAL Service Discovery is used to find the Chromecast.  It is based on SSDP (UPnP)
3. Sender Attempts to Launch a WebApp on the Chromecast using the DIAL protocol
    * DIAL REST Serice is used to launch applications.  It is based on HTTP
    * The AppID of the app you wish to launch is sent to the Chromecast
4. Chromecast Fetches the WebApp form Google's Servers
    * Forwards the App ID to Google's server and recieves the appropriate URL
    * This use of Google Servers is what gives them control over the apps 
5. Chromecast Loads the WebApp usin the provided URL
    * Loads the HTML, CSS, and Javscript
    * Attemps to Start a WebSocket connection
6. Sender and Chromecast create a WebSocket connection.
    * Now the Sender can Play, Pause, Skip, Load new media, etc...
