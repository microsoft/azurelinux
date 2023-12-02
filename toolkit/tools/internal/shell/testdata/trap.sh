#!/bin/bash

# $1 name
# $2 file to write to
trap "echo trapped!" SIGTERM

echo "$1" > "$2"
echo "START"  >> "$2"
sleep 1
echo "MIDDLE"  >> "$2"
sleep 6000
echo "END"  >> "$2"
