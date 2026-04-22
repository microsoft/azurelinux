#!/bin/bash
set -e

if [ $# -lt 1 ]; then
	echo "Usage: $0 version pre"
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
mv gdal-"${VERSION}${PRE}"{,-fedora} && pushd gdal-"${VERSION}${PRE}"-fedora

rm ogr/data/cubewerx_extra.wkt
rm ogr/data/esri_StatePlane_extra.wkt
rm ogr/data/ecw_cs.wkt


sed -i 's|${CMAKE_CURRENT_SOURCE_DIR}/data/cubewerx_extra.wkt||' ogr/CMakeLists.txt
sed -i 's|${CMAKE_CURRENT_SOURCE_DIR}/data/esri_StatePlane_extra.wkt||' ogr/CMakeLists.txt
sed -i 's|${CMAKE_CURRENT_SOURCE_DIR}/data/ecw_cs.wkt||' ogr/CMakeLists.txt

popd


#TODO: Insert Provenance file

tar cvfJ gdal-"${VERSION}${PRE}"-fedora.tar.xz gdal-"${VERSION}${PRE}"-fedora
