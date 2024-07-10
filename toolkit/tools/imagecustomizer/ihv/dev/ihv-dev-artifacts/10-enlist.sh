#!/bin/bash

set -x
set -e

cd ~
sudo chown $USER:$USER /home/$USER
mkdir -p git
pushd git
git clone git@github.com:microsoft/azurelinux.git
pushd azurelinux/toolkit
git checkout 3.0.20240624-3.0
sed -i 's/\/prod\//\/preview\//g' Makefile
# sed -i 's/\/prod\//\/preview\//g' scripts/sodiff/sodiff.repo
popd
popd
