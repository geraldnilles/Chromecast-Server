
import wsgiref
from wsgiref.simple_server import make_server

import re

# A relatively simple WSGI application. It's going to print out the
# environment dictionary after being updated by setup_testing_defaults
def simple_app(environ, start_response):
	

	#return [repr(environ)]

	path = environ['PATH_INFO']
	if path == "/video": 
		return serve_video(environ,start_response)
	else: 
		return serve_main_page(start_response)

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

def serve_video(environ,start_response):
	headers = [('Content-Type','video/mp4')]
	headers.append( ('Accept-Ranges','bytes') )
	
	f = open("bbb.mp4","rb")

	# Determine the file's size
	f.seek(0,2)   # Jump to the end
	fs = f.tell() # Get current file handle position
	f.seek(0,0)     # Jump to beginning

	chunk_size = 2**20
	start = 0;
	stop = fs-1;

	# Figure out the range that was requested
	if ("HTTP_RANGE" in environ and environ["HTTP_RANGE"] != ""):
		print "Range was detected"
		m = re.match("bytes=([0-9]*)-([0-9]*)",environ["HTTP_RANGE"])
		start = int(m.group(1))

		if m.group(2) != "":
			stop = int(m.group(2))

		if stop < start:
			stop=start

		print "stop:",stop
		print "start:",start

		f.seek(start)

		headers.append( ('Content-Range',str(start)+"-"+str(stop)+"/"+str(fs)) )
	

	headers.append( ('Content-Length',str(stop-start+1)) )

	if start != 0:
		start_response('206 Partial Content', headers)
	else:
		start_response("200 OK", headers)

	print f.tell()
	print repr(headers)
	return wsgiref.util.FileWrapper(f,stop-start+1)
	#return iter(lambda: f.read(2**20), "")
	


httpd = make_server('', 8000, simple_app)
print "Serving on port 8000..."
httpd.serve_forever()

