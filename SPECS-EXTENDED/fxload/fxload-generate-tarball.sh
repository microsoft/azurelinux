#!/bin/sh

VERSION=$1

tar -xzvf fxload-${VERSION}.tar.gz
rm fxload-${VERSION}/a3load.hex
tar -czvf fxload-${VERSION}-noa3load.tar.gz fxload-${VERSION}

