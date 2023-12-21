#!/bin/bash

set -x
set -e

pushd ~/git/CBL-Mariner-POC/toolkit/tools/imagecustomizer
go build
popd
