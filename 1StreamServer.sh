#!/usr/bin/bash
gst-launch-1.0 -vvvvv libcamerasrc ! video/x-raw,width=640,height=480,framerate=30/1 ! v4l2convert ! v4l2h264enc ! 'video/x-h264,level=(string)4.2,profile=(string)baseline' ! h264parse ! rtph264pay config-interval=-1 ! udpsink host=172.17.141.191 port=5000
