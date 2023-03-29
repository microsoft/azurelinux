#!/bin/sh
set -e

name=maven-surefire
PKG_VERSION=""
OUT_FOLDER="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Source is downloaded from the web

# parameters:
# --outFolder   : folder where to copy the new tarball(s)
# --pkgVersion  : package version
#
PARAMS=""
while (( "$#" )); do
    case "$1" in
        --outFolder)
        if [ -n "$2" ] && [ ${2:0:1} != "-" ]; then
            OUT_FOLDER=$2
            shift 2
        else
            echo "Error: Argument for $1 is missing" >&2
            exit 1
        fi
        ;;
        --pkgVersion)
        if [ -n "$2" ] && [ ${2:0:1} != "-" ]; then
            PKG_VERSION=$2
            shift 2
        else
            echo "Error: Argument for $1 is missing" >&2
            exit 1
        fi
        ;;
        -*|--*=) # unsupported flags
        echo "Error: Unsupported flag $1" >&2
        exit 1
        ;;
        *) # preserve positional arguments
        PARAMS="$PARAMS $1"
        shift
        ;;
  esac
done

echo "--outFolder    -> $OUT_FOLDER"
echo "--pkgVersion   -> $PKG_VERSION"

if [ -z "$PKG_VERSION" ]; then
    echo "--pkgVersion parameter cannot be empty"
    exit 1
fi
echo $PKG_VERSION
version=$PKG_VERSION
upstream_version="${version/'~'/'-'}" 
version_main=$(sed "s/-M[0-9]//" <<< ${upstream_version})

echo $version_main
#RETRIEVE
wget "https://repo1.maven.org/maven2/org/apache/maven/surefire/surefire/${upstream_version}/surefire-${upstream_version}-source-release.zip" -O "${name}-${version}.orig.zip"

rm -rf tarball-tmp
mkdir tarball-tmp
cd tarball-tmp
unzip "../${name}-${version}.orig.zip"

# CLEAN TARBALL
find -name '*.jar' -delete
find -name '*.class' -delete

NEW_TARBALL="$OUT_FOLDER/${name}-${version_main}.tar.gz"
tar --sort=name --mtime="2021-11-10 00:00Z" \
    --owner=0 --group=0 --numeric-owner \
    --pax-option=exthdr.name=%d/PaxHeaders/%f,delete=atime,delete=ctime \
    -zcf ${NEW_TARBALL} *   
cd ..
rm -r tarball-tmp "${name}-${version}.orig.zip"
