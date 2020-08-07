#!/bin/bash
# cleanup
rm -rf /boot/*
rm -rf /usr/src/
rm -rf /home/*
rm -rf /var/log/*
# set TERM to linux
echo "export TERM=linux" >> /etc/bash.bashrc