#!/bin/bash

set -x
set -e

repoTag=3.0.20240624-3.0

pushd ~
# not sure why the user home folder is initially owned by root.
# need to fix that:
sudo chown $USER:$USER /home/$USER

# clone
mkdir -p git
pushd git
git clone git@github.com:microsoft/azurelinux.git

# checkout
pushd azurelinux/toolkit
git checkout $repoTag

# apply temporary fix
sed -i 's/\/prod\//\/preview\//g' Makefile

popd
popd
popd
