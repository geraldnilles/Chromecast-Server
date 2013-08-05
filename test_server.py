
import wsgiref

# A relatively simple WSGI application. It's going to print out the
# environment dictionary after being updated by setup_testing_defaults
def simple_app(environ, start_response):
	if : #path is video
		return serve_video
	else: 
		return serve_html

def serve_main_page(start_response):
	headers = [('Content-type','text/html')]
	html = """
	<html>
	<head>
		<title>Test Video Player</title>
	</head>
	<body>
		<h2>Test Video Player</h2>
		<video src="/video"></video>
	</body>
	</html>
	"""
	headers.append(('Content-length',str(len(html))))

	start_response('200 OK',headers)
	return [html]

def serve_video(start_response,environ):
	headers = [('Content-type','video/mp4')]
	headers.append( ('Accept-Ranges','bytes') )
	
	f = open("bbb.mp4","r")
	
	# Figure out the range that was requested
	theRange = environ['Range'].split("-")
	start = int(theRange[0])
	stop = int(theRange[1])
	fs = len(f)



	headers.append( ('Content-Length',str(stop-start)) )
	headers.append( ('Content-Range',str(start)+"-"+str(stop)+"/"+str(fs)) )



	
	
	start_response('206 OK', header)

	return wsgiref.util.FileWrapper(f,2^16)
	


httpd = wsgiref.simple_server.make_server('', 8000, simple_app)
print "Serving on port 8000..."
httpd.serve_forever()

