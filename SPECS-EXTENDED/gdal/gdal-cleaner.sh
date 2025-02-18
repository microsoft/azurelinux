#!/bin/bash

if [ $# -lt 1 ]; then
	echo "Usage: $0 version"
	exit 1
fi

VERSION="$1"
PRE="$2"

if [ ! -f "gdal-"${VERSION}${PRE}".tar.xz" ]; then
    wget https://download.osgeo.org/gdal/${VERSION}/gdal-${VERSION}${PRE}.tar.xz
fi

if [ -d gdal-"${VERSION}" ] || [ -d gdal-"${VERSION}"-fedora ]; then
    echo "gdal-${VERSION} or gdal-${VERSION}-fedora in the way, please remove and rerun this script"
    exit 1
fi

tar xvf gdal-"${VERSION}${PRE}".tar.xz
mv gdal-"${VERSION}"{,-fedora} && pushd gdal-"${VERSION}"-fedora

rm data/cubewerx_extra.wkt
rm data/esri_StatePlane_extra.wkt
rm data/ecw_cs.wkt


sed -i 's|data/cubewerx_extra.wkt||' gdal.cmake
sed -i 's|data/esri_StatePlane_extra.wkt||' gdal.cmake
sed -i 's|data/ecw_cs.wkt||' gdal.cmake

popd


#TODO: Insert Provenance file

tar cvfJ gdal-"${VERSION}${PRE}"-fedora.tar.xz gdal-"${VERSION}"-fedora
