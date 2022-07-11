#! /bin/bash

set -eux pipefail

# NOTE: EXECUTING with id=0 (root) CAUSES REAPER BUILD TO FAIL.
# Cassandra reaper version for which to generate build caches.
# Set this to the required version.
VERSION="3.1.1"
# URL to download the sources to build
SOURCE_URL="https://github.com/thelastpickle/cassandra-reaper/archive/refs/tags/${VERSION}.tar.gz"

# Build cache names
BOWER_COMPONENTS="reaper-bower-components-${VERSION}.tar.gz"
SRC_UI_NODE_MODULES="reaper-srcui-node-modules-${VERSION}.tar.gz"
BOWER_CACHE="reaper-bower-cache-${VERSION}.tar.gz"
MAVEN_CACHE="reaper-m2-cache-${VERSION}.tar.gz"
NPM_CACHE="reaper-npm-cache-${VERSION}.tar.gz"
LOCAL_LIB_NODE_MODULES="reaper-local-lib-node-modules-${VERSION}.tar.gz"
LOCAL_N="reaper-local-n-${VERSION}.tar.gz"

tempDir=$(mktemp -d)

mkdir -p ${tempDir}/mariner_caches

marinerCacheDir=${tempDir}/mariner_caches

function checkInternet {
	sudo tdnf install -y nc
	nc -z 8.8.8.8 443
	if [ $? -eq 0 ]; then
		echo "Online."
	else
		echo "Offline, reaper needs internet connectivity to download and build cache."
		exit 1
	fi
}

function dieIfError {
	if [ $? -ne 0 ];then
		echo "Error $?, exiting build."
		exit $?
	fi
}

function installNodeModules {
	echo "Installing node modules."
	sudo tdnf install -y nodejs | dieIfError
	# Default node/npm versions in Mariner fails to build dependency node module versions due to known
	# incompatibilities.
	# Backward compatible with node@v14.18.0
	# When installing modules via npm to default prefix='/usr/local' in mariner, the permissions for 'others'
	# is incoorectly set that causes 'which' to still point to older path, as access/newfstatat fail with -ENOPERM
	# Setting a new global npm folder for fixing permission issues.
	# (works well with id=0, but reaper build will fail.)
	mkdir --mode 0777 $HOME/.npm-global
	echo $HOME
	npm config set prefix "$HOME/.npm-global"
	echo $HOME
	npm config get prefix
	export PATH="$HOME/.npm-global/bin":$PATH
	npm install -g n
	export N_PREFIX="$HOME/.npm-global"
	n 14.18.0
	npm install -g bower
	# Clear bash hash tables for node/npm paths
	hash -r
	bower -v
	node -v
	npm -v
}

function buildReaperSources {
	pushd $tempDir
	sudo tdnf install -y wget | dieIfError
	wget $SOURCE_URL -O reaper.tar.gz
	tar -xf reaper.tar.gz
	cd cassandra-reaper-${VERSION}
	export JAVA_HOME="/usr/lib/jvm/msopenjdk-11"
	export LD_LIBRARY_PATH="/usr/lib/jvm/msopenjdk-11/lib/jli"
	echo "Building reaper in online mode."
	mvn -DskipTests package
	popd
}

function createCacheTars {
	echo "Creating build caches."
	pushd ${HOME}
	echo "creating bower_cache tar..."
	tar -cf ${BOWER_CACHE} .cache
	cp ${BOWER_CACHE} ${marinerCacheDir}

	echo "creating maven_cache tar..."
	tar -cf ${MAVEN_CACHE} .m2
	cp ${MAVEN_CACHE} ${marinerCacheDir}

	echo "creating npm_cache tar..."
	tar -cf ${NPM_CACHE} .npm
	cp ${NPM_CACHE} ${marinerCacheDir}
	popd

	pushd ${tempDir}/cassandra-reaper-${VERSION}/src/ui
	echo "creating bower_components tar..."
	tar -cf ${BOWER_COMPONENTS} bower_components
	cp ${BOWER_COMPONENTS} ${marinerCacheDir}

	echo "creating node_modules tar..."
	tar -cf ${SRC_UI_NODE_MODULES} node_modules
	cp ${SRC_UI_NODE_MODULES} ${marinerCacheDir}
	popd

	pushd $HOME/.npm-global/lib
	echo "creating local_lib_node_modules tar..."
	tar -cf ${LOCAL_LIB_NODE_MODULES} node_modules
	cp ${LOCAL_LIB_NODE_MODULES} ${marinerCacheDir}
	popd

	pushd $HOME/.npm-global
	echo "creating local node tar..."
	tar -cf ${LOCAL_N} n
	cp ${LOCAL_N} ${marinerCacheDir}
	popd
}

echo "Generate cassandra reaper build caches..."

checkInternet

echo "Installing msopenjdk-11."
sudo tdnf install -y msopenjdk-11 | dieIfError

echo "Installing maven modules."
sudo tdnf install -y maven | dieIfError

installNodeModules

buildReaperSources

createCacheTars

cp -a ${marinerCacheDir} $HOME

echo "Copied cache tars to $HOME/mariner_caches/ .Exiting."
