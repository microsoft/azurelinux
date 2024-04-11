#!/bin/bash

# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

# Failure can be ignored.
set +e
set -x

function log_disk_space() {
  echo "Disk space"
  du -h --max-depth=2 | sort -rh | head -n 20
  wait
}

# cleanup symlinks created by the toolkit that are not needed for base images
if [ -L /srv ]; then
  echo "Removing /srv symlink"
  rm /srv
else
  echo "/srv symlink does not exist"
fi

log_disk_space

# clear tdnf cache
tdnf clean all

# remove all python py cache files
find /usr/lib/python* -type d -name '__pycache__' -exec rm -rf {} +

# clear any journal logs
journalctl --vacuum-time=1s

log_disk_space
