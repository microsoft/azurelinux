#!/bin/bash
ls -l /dev/null
sudo rm -rf /dev/null
sudo mknod -m 0666 /dev/null c 1 3
ls -l /dev/null
