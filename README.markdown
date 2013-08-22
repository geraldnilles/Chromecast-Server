Chromecast Server
=================

# Introduction

## Motivation
I have a local server with 7TB of storage (in a RAID5 Array).  This server contains thousands of media files (video, audio, and pictures).  Currently, I use OpenElec (a highly-optimized XBMC linux distribution) to play/display my media on each of my Televisions.  OpenElec is an amazingly project.  However, XBMC is designed to work with traditional remote controls so it needs a nice GUI.  

In a world of smartphones and tablets, there is no need for any UI on the TV.  Why not have the entire UI exist on the phone?  I frequently tooled around with the idea of creating my own "Zero-UI" media player to replace XBMC, but I usually abandoned the idea since I dont currently have the skill-set to develop such a product.  

When Chromecast was announced, it dawned on me that this could be the perfect Frontend for my "Zero-UI" concept.  Chromecast is essentially a $35 web browser that can be controlled with your smartphone.  That means i could code the majority of this project in HTML/CSS/JS.  This would make it much simpler to implement.

## Goal
Use Chromecast to display/playback all of my local media content.

On my storage server, i will host a special website that displays all of my media files.  Anyone on the network can access this website with any computer (Smartphone, tablet, laptop, desktop, etc...).  When they select a media file, the Website UI will ask where they want to play it (Any of the TVs or on the current device).  

# Overview
1. Server Hosts A WebUI showing all of the avaiable movies
2. User Selects a Movie to Watch.  
3. Chromecast Starts streaming that video directly from the local server.  

# Current Progress

## Complete
* Order Chromecast Device
* Whitelist Chromecast for Development usage
    * Success!
* Learn how the GoogleCast protocol works
* Python Script for Discovering Chromecast devices

## In Progress
1. Python Scrit for Launching Apps 
1. Launch a "Hello World" Web App on my Chromecast Device
    * No Video or Audio
2. Create Web Server that can stream video to a Chrome Browser.
    * It must allow for skipping (Support HTTP Byte Range headers)

## Future
2. Launch a Video Playback Web App on my Chromecast Device
    * Add a device
3. Create SImple WebUI for browsing and selecting Media files
4. Add abbility for Web Server to transcode video to a Chromecast Friendly format

## Way Out There
1. Live TV (HDHomeRun Prime)
    * Transcode a live TV stream and send it to the Chromecast in an HTML5 friendly format.


