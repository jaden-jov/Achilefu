#!/bin/bash
gst-launch-1.0 udpsrc port=5000 caps=application/x-rtp ! rtph264depay ! h264parse ! avdec_h264 ! videoconvert ! autovideosink
