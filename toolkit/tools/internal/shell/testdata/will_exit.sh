#!/bin/bash

# $1 name
# $2 file to write to
echo "$1" > "$2"
echo "START"  >> "$2"
sleep 1
echo "MIDDLE"  >> "$2"
sleep 10
echo "END"  >> "$2"
