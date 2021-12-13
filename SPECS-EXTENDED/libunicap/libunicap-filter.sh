#!/bin/sh

# The original script name has been passed as the first argument:
"$@" | sed -e '/^libdcam.so/d' -e '/^libv4l.so/d' -e '/^libv4l2cpi.so/d' -e '/^libvid21394.so/d'
