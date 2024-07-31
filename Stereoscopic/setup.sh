#!/usr/bin/bash
# set up moverio glasses for sbs 3d

sudo modprobe usbserial vendor=0x04b8 product=0x0d12
python3 test_conn.py