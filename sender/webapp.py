

def WebApp(environ, start_response):
	return main_page(environ,start_response)




def main_page(e,s):
	# Set Type to HTML
	s("200 OK", [("Content-Type","text/html")])
	# Open Main HTML file
	# Read it to output
	output = "<h2>Welcome to HTML</h2>"
	return [output]


def list_video(e,s):
	# Check if the "q" Get Variable is set
	# Print a list of videos that match the filter




# Launch the FCGI Server
if __name__ == '__main__':
	# Use the "Fork" type to break it out
	from flup.server.fcgi_fork import WSGIServer
	# Run the application
	WSGIServer(WebApp,bindAddress="/tmp/Chromecast/ui").run()



