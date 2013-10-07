Server-WebApp Communication
======================

# Introduction

In order to control the video player, you will need a way of sending messages between the Chromecast WebApp and the Server.

# Methods
Here are the possible ways to send and recieve messages.

## Pure HTTP
The WebApp will periodically (once every second) send a GET request to the WebServer. This GET request will contain status info in the URL (playback status, etc..).  The HTTP response from the server will contain commands (such as Play, Pause, Skip, and Load)

Pros
* Only requires 1 server (the HTTP server)
* Simple.  Doesnt require a whole lot of multithreading

Cons  
* The "reaction time" of a command will be slow (dpeending on the period of the HTTP requests)

## WebSockets
A Websocket will be opened between the WebApp and the Server.  From there, text messages will be sent via TCP packets.  These messages will contain the commands and responses.  

Pros
* Fast response time
* More flexibile bidirectional communication

Cons
* Complex Multiprocessing

### Processes
* WebSocket Servers
    * There will need to be 1 WebSocket server per chromecast device
* Unix Socket Server
    * THere will need to be a Unix Socket server that waits for local applications to send commands.

### Communication Example

Command Line Interface
* CLI is executed from the BASH and asked to pause the video stream
* CLI Attempts to open a Unix socket with Proxy Server 1but it NAKs
* CLI Attemps to open a Unixh Socket with Proxy Server 2 and its succesfful.
* CLI Checks if the IP address matches Proxy Server 2's IP but it doesnt
* CLI Closes connect to Proxy Server 2
* CLI Attempts to open a Unix socket with proxy Server 3 and its succesful.
* CLI Check if the Ip address matches and it does
* CLI Sends command to Unix Socket
* CLI Recieves Unix Socket Response and parses it accordingly

Proxy Server 3
* Proxy server is Spawned
* Proxy Server binds itself to the predetermined WebSocket port and waits for a connection.
* Proxy Server Recieves a connection
* Proxy Server Performs a TCP handshake 
* Proxy Server Creates a Unix Socket Server for /tmp/WSProxy3 and waits for a command.  This socket will have a timeout of 5 seconds.
* Timeout Occurs.  Sets WebSocket timeout to 0s and atempts to recv command
* Error occurs since there is not data avaiable.
* Proxy server listens to the Unix Socket server again with a 5 second timeout
* Proxy Server receives a message from the CLI process 
* Proxy Server forwards that message to the WebSocket
* Proxy Server recieves the response
* Proxy Server sends the response over Unix Socket.


