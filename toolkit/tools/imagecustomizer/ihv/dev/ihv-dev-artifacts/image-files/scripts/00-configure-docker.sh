#!/bin/bash

set -x
set -e

sudo usermod -aG docker $USER
sudo systemctl enable docker
sudo systemctl start docker
