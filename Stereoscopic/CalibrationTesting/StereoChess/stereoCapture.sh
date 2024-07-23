#!/usr/bin/bash

# Capture from camera 0
libcamera-still -n --camera 0 --width 640 --height 480 -o left$1.jpg &

# Capture from camera 1
libcamera-still -n --camera 1 --width 640 --height 480 -o right$1.jpg &

# Wait for both processes to complete
wait
