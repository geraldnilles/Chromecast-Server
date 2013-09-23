#!/usr/bin/env python

import os
import libcommand_center as libcc
import time

#-----------------
# Constants 
#-----------------

MOVIE_FOLDER = "/mnt/raid/Movies/Features"


## Fine Files by Extention
#
# Scans a folder (recusively), finds files with the given extension(s) and
# returns a list of files that match the extension(s)
#
# @param path - Folder path you want to scan
# @param exts - A List of file extensions to look for
# @return - A list of files (with their full path) that match the extensions
def find_files_by_extention(path,exts):
	# Generate the return list object
	files = []
	# Scan each file/folder
	for fn in os.listdir(path):
		# Extract the Extension
		ext = fn.rsplit(".")[-1]
		# Create the entire filepath
		fp = path+"/"+fn

		if os.path.isdir(fp):
			# If a directory, recurse and add the results to the 
			# output list object
			files += find_files_by_extention(fp,exts)
		else:
			# If a file, check if the extensions match
			if ext in exts:
				files.append(fp)
	return files

def scan_movies(db):
	movies = find_files_by_extention(MOVIE_FOLDER,["mkv","mp4","avi"])
	for path in movies:
		# Split the filename from the path
		fn = path.split("/")[-1]

		# Create a new entry
		entry = {}
		entry["path"] = path
		entry["title"] = fn.rsplit(".",1)[0]

		# Add entry to the database
		db.append(entry)

def scan_tv(db):
	pass

def scan_music(db):
	pass

def scan_pictures(db):
	pass

def loop_forever():
	while(1):
		# Create an Empty Database object
		db = {
			"source":"scanner",
			"movies":[],
			"tv":[],
			"music":[],
			"pictures":[]
			}

		# Scan the Movie Folder
		scan_movies(db["movies"])

		# Scan the TV Folder
		scan_tv(db["tv"])

		# Scan the Music Folder
		scan_music(db["music"])

		# Scan the Picutre Folder
		scan_pictures(db["pictures"])

		# Send database to the command cetner
		ret = libcc.client_send_recv(db)

		# Wait 10 minutes before the next scan
		time.sleep(60)
		

	return -1

if __name__ == "__main__":
	loop_forever()

