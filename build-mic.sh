#!/bin/bash

set -x
set -e

scriptPath=$(realpath ${BASH_SOURCE[0]})
scriptDir=$(dirname "$scriptPath")

pushd $scriptDir/toolkit
sudo make go-tidy-all
popd

pushd ~/git/CBL-Mariner-POC/toolkit/tools/imagecustomizer
go build
popd
