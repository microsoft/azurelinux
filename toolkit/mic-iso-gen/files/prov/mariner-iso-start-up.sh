#!/bin/bash

# Use a custom termcap for the Mariner installer in an ISO environment
# for a high contrast cursor. This is based on the "linux" termcap.
export TERMINFO=/usr/lib/mariner/terminfo
export TERM=mariner-installer

echo "Running mariner-iso-start-up script v1129-1110."

/bin/bash