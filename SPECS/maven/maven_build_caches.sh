#!/bin/bash
## Helper script to generate maven build caches.
## CBL-MARINER builds do not have access to internet when building rpms.
## Generating build cache as tarballs to be used when buidling offline.
set -e

# Maven version used to build caches.
VERSION=""
# Architecture to build for, either (x86_64 | aarch64)
BUILDARCH=""

function usage {
	echo "Script to generate maven build caches."
	echo "Usage: ./maven_build_caches.sh -v|-version <Version String> -a|-abi <ABI>"
	echo "Options:"
	echo "-v|version: Maven version for generating caches."
	echo "-a|abi    : Architecture to build maven. x86_64 | aarch64"
}

if [[ $# -lt 1 ]];then
	usage
	exit 1
fi

while getopts "v:h" options; do
	case "${options}" in
		h)
			usage
			exit;;
		v|version)
			VERSION="$OPTARG"
			echo $VERSION
			;;
		\?)
			echo "Empty Value provide."
			usage
			exit 1
			;;
	esac
done

BUILDARCH=$(rpm --eval '%{_arch}')

# Source URL to extract the sources.
SOURCEURL="https://archive.apache.org/dist/maven/maven-3/${VERSION}/source/apache-maven-${VERSION}-src.tar.gz"
# Maven binary dependency to download from pmc.
# NOTE: Version IN THIS IS HARDCODED.
MAVENBINARY="https://cblmarinerstorage.blob.core.windows.net/sources/core/maven-3.8.7-3.cm2.${BUILDARCH}.rpm"

maven_m2_cache_tarball_name="apache-maven-${VERSION}-m2.tar.gz"
maven_licenses_tarball_name="apache-maven-${VERSION}-licenses.tar.gz"

tempDir=$(mktemp -d)

mkdir -p "$HOME/mavenCaches"

mavenCacheDir="$HOME/mavenCaches"

function dieIfError {
	if [ $? -ne 0 ];then
		echo "Error $?, exiting build."
		exit $?
	fi
}

function installUtils {
	echo "Installing wget."
	tdnf install -y wget | dieIfError
	pushd "/tmp"
	wget $MAVENBINARY -O maven.rpm
	echo "Installing pre-built PMC 1.0 maven rpm to provide maven binary needed to build maven itself."
	rpm -i --nodeps maven.rpm
	mvn -v
	echo "Installing msopenjdk-11."
	tdnf install -y msopenjdk-11 | dieIfError
}

function buildMaven {
	echo "Downloading maven sources from $SOURCEURL."
	pushd $tempDir
	wget $SOURCEURL -O mavensrc.tar.gz
	tar -xf mavensrc.tar.gz
	cd apache-maven-$VERSION

	export JAVA_HOME="/usr/lib/jvm/msopenjdk-11"
	export LD_LIBRARY_PATH="/usr/lib/jvm/msopenjdk-11/lib/jli"
	sed -i 's/www.opensource/opensource/g' DEPENDENCIES
	mvn -DskipTests clean package
	popd
}

function createBuildCaches {
	echo "Creating build cache tarballs."
	pushd $mavenCacheDir
	tar -C $HOME/.m2 -cpvz -f ${maven_m2_cache_tarball_name} repository

	tar -C $tempDir/apache-maven-$VERSION/apache-maven -cpvz -f ${maven_licenses_tarball_name} target/licenses/lib
	
	ls -al .
	popd
}

echo "Building maven caches for version:${VERSION} and abi:${BUILDARCH}."

installUtils

buildMaven

createBuildCaches

echo "Created caches at $mavenCacheDir. Done."
