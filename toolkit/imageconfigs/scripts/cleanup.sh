#!/bin/bash

set -eux

# cleanup symlinks created by the toolkit that are not needed for base images
if [ -L /srv ]; then
  echo "Removing /srv symlink"
  rm /srv
else
  echo "/srv symlink does not exist"
fi

# cleanup any logs that may have been created during the build
if [ -d /var/log ]; then
  echo "Clearing /var/log"
  rm -rf /var/log/*
else
  echo "/var/log does not exist"
fi
