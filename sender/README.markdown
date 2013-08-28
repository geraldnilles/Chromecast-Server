Sender Application
==================

# Introduction

The sender application will be a Python web server.  The web server will display the media files currently on the NAS server.  When the user selects the media file, it will push it to a Chromecast device on the network.


# Server Video Request
Currently, my server app does not work.  

After looking at an example (see below), i realized how many request Chrome is trying to make.  First, i downloads the first couple kbs.  Then it jumps to the last couple KBs.  Then i resumes from the beginning.  

Its likely that all of this jumping around is confusing my server (which can only handle a single thread).  Perhaps i need to add multiple threads to handle this?

## Example
Using this page as a source: http://media.w3.org/2010/05/bunny/movie.mp4
For this example, i loaded the web page.  Waited a few second, skipped to about the half-way point  and then pressed pause (as it loaded the rest of the movie)

Chrome's Network manager shows the first page load as 5 HTTP GET requests.
* A Standard HTTP GET Request.  
    * The browser cannot make any assumtions about the page until it looks at the headers.  This request looks normal.
    * However, WHen the Browser sees the Accept-Ranges option, it Cancells this request
 
	Request URL:http://media.w3.org/2010/05/bunny/movie.mp4
	Request Method:GET
	Status Code:200 OK

	Request Header
	Accept:text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
	Accept-Encoding:gzip,deflate,sdch
	Accept-Language:en-US,en;q=0.8
	Connection:keep-alive
	Host:media.w3.org
	User-Agent:Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.57 Safari/537.36

	Response Headers
	Accept-Ranges:bytes
	Cache-Control:max-age=21600
	Connection:Keep-Alive
	Content-Length:249224577
	Content-Type:video/mp4
	Date:Fri, 23 Aug 2013 20:37:31 GMT
	ETag:"edadd81-4867d5d962e80"
	Expires:Sat, 24 Aug 2013 02:37:31 GMT
	Keep-Alive:timeout=2, max=100
	Last-Modified:Thu, 13 May 2010 17:48:26 GMT
	P3P:policyref="http://www.w3.org/2001/05/P3P/p3p.xml"
	Server:Apache/2

* A Pending Request
    * THis request goes though but it stays in the "Pending" mode forever...

	Request URL:http://media.w3.org/2010/05/bunny/movie.mp4
	Request Headersview source
	User-Agent:Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.57 Safari/537.36

* First Byte Range Request
    * This Request uses the byte ranges, but is cancelled shortly into it (58kBytes in)
    * I am guessing Chrome is reading the META data at the first part of the the MP4


	Request URL:http://media.w3.org/2010/05/bunny/movie.mp4
	Request Method:GET
	Status Code:206 Partial Content

	Request Headersview source
	Accept:*/*
	Accept-Encoding:identity;q=1, *;q=0
	Accept-Language:en-US,en;q=0.8
	Connection:keep-alive
	Host:media.w3.org
	Range:bytes=0-
	Referer:http://media.w3.org/2010/05/bunny/movie.mp4
	User-Agent:Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.57 Safari/537.36

	Response Headersview source
	Accept-Ranges:bytes
	Cache-Control:max-age=21600
	Connection:Keep-Alive
	Content-Length:249224577
	Content-Range:bytes 0-249224576/249224577
	Content-Type:video/mp4
	Date:Fri, 23 Aug 2013 20:37:31 GMT
	ETag:"edadd81-4867d5d962e80"
	Expires:Sat, 24 Aug 2013 02:37:31 GMT
	Keep-Alive:timeout=2, max=100
	Last-Modified:Thu, 13 May 2010 17:48:26 GMT
	P3P:policyref="http://www.w3.org/2001/05/P3P/p3p.xml"
	Server:Apache/2

* End Byte Range Request
    * Next, it appears that the Browser is requesting the last chunk of the file
    * I am guessing there is data stored at the end of the MP4 that Chrome need to play the video
    * This request is completed, but since it jumped to the end, it only grabbed a total of 441 kb

	Request URL:http://media.w3.org/2010/05/bunny/movie.mp4
	Request Method:GET
	Status Code:206 Partial Content
	Request Headersview source
	Accept:*/*
	Accept-Encoding:identity;q=1, *;q=0
	Accept-Language:en-US,en;q=0.8
	Connection:keep-alive
	Host:media.w3.org
	If-Range:"edadd81-4867d5d962e80"
	Range:bytes=248773025-249224576
	Referer:http://media.w3.org/2010/05/bunny/movie.mp4
	User-Agent:Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.57 Safari/537.36
	Response Headersview source
	Accept-Ranges:bytes
	Cache-Control:max-age=21600
	Connection:Keep-Alive
	Content-Length:451552
	Content-Range:bytes 248773025-249224576/249224577
	Content-Type:video/mp4
	Date:Fri, 23 Aug 2013 20:37:31 GMT
	ETag:"edadd81-4867d5d962e80"
	Expires:Sat, 24 Aug 2013 02:37:31 GMT
	Keep-Alive:timeout=2, max=100
	Last-Modified:Thu, 13 May 2010 17:48:26 GMT
	P3P:policyref="http://www.w3.org/2001/05/P3P/p3p.xml"
	Server:Apache/2

* Continuing the First ByteRange Request
    * This one does not have a new set of headers.  I am guessing it just continued off the previous BYteRange request that started at the beginning

	Request URL:http://media.w3.org/2010/05/bunny/movie.mp4
	Request Method:GET
	Status Code:206 Partial Content

* Middle ByteRange Request
    * After skipping to the middle, this Byte Range request occurs.  It is more or less normal looking

	Request URL:http://media.w3.org/2010/05/bunny/movie.mp4
	Request Method:GET
	Status Code:206 Partial Content
	Request Headersview source
	Accept:*/*
	Accept-Encoding:identity;q=1, *;q=0
	Accept-Language:en-US,en;q=0.8
	Connection:keep-alive
	Host:media.w3.org
	If-Range:"edadd81-4867d5d962e80"
	Range:bytes=112384682-248773024
	Referer:http://media.w3.org/2010/05/bunny/movie.mp4
	User-Agent:Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.57 Safari/537.36
	Response Headersview source
	Accept-Ranges:bytes
	Cache-Control:max-age=21600
	Connection:Keep-Alive
	Content-Length:136388343
	Content-Range:bytes 112384682-248773024/249224577
	Content-Type:video/mp4
	Date:Fri, 23 Aug 2013 20:37:42 GMT
	ETag:"edadd81-4867d5d962e80"
	Expires:Sat, 24 Aug 2013 02:37:42 GMT
	Keep-Alive:timeout=2, max=100
	Last-Modified:Thu, 13 May 2010 17:48:26 GMT
	P3P:policyref="http://www.w3.org/2001/05/P3P/p3p.xml"
	Server:Apache/2


# NGINX Setup
The NGINX configuration will look like this:


	http {
		include conf/mime.types

		server {
			listen 80;

			location /chromecast {
				root /path/to/chromecast;
			}
			location /mediacenter/ {
				fastcgi_pass localhost:9771;
				//fastcgi_pass unix:/tmp/mediacenter.socket
			}
		}

		server {
			listen 9770;
			location /video {
				root /path/to/video/files;
			}
			location /audio {
				root /path/to/audio/files;
			}
			location /images {
				root /path/to/picture/files;
			}
		}
	}

The first server will run on port 80.  The chomecast app path will be statically handled by NGINX.  The mediacenter path will be passed to a fastcgi application.

The second server will be run on port 9770.  This port was arbitrarily chosen.  Since its not 80, it will make it slightly more protected from the outside world.  The Video, Audio, and Images will be directly hosted by NGINX.  THis will keep it simple for now.  In the future, id like to host it via a FastCGI app in order to add authentication and encryption . 
