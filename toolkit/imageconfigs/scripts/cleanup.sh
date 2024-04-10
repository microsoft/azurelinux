#!/bin/bash

# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

set -eux

# cleanup symlinks created by the toolkit that are not needed for base images
if [ -L /srv ]; then
  echo "Removing /srv symlink"
  rm /srv
else
  echo "/srv symlink does not exist"
fi
