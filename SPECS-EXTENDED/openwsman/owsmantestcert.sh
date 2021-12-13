#!/bin/bash

if [ ! -f "/etc/openwsman/serverkey.pem" ]; then
  if [ -f "/etc/ssl/servercerts/servercert.pem" \
       -a -f "/etc/ssl/servercerts/serverkey.pem" ]; then
    echo "Using common server certificate /etc/ssl/servercerts/servercert.pem"
    ln -s /etc/ssl/servercerts/server{cert,key}.pem /etc/openwsman
    exit 0
  else
    echo "FAILED: Starting openwsman server"
    echo "There is no ssl server key available for openwsman server to use."
    echo -e "Please generate one with the following script and start the openwsman service again:\n"
    echo "##################################"
    echo "/etc/openwsman/owsmangencert.sh"
    echo "================================="
    
    echo "NOTE: The script uses /dev/random device for generating some random bits while generating the server key."
    echo "      If this takes too long, you can replace the value of \"RANDFILE\" in /etc/openwsman/ssleay.cnf with /dev/urandom. Please understand the implications of replacing the RNADFILE."
    exit 1
  fi
fi
