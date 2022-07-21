#! /bin/bash

set -euo pipefail

# NOTE: EXECUTING with id=0 (root) CAUSES REAPER BUILD TO FAIL.
if [[ $(id -u) -eq 0 ]]; then
    echo "Must run script as non-root user!" >&2
    exit 1
fi

# Cassandra reaper version for which to generate build caches.
# (a) Modify VERSION="x.x.x" in script.
# (b) Pass arguments to command line: ./reaper_build_caches.sh 3.1.1
VERSION="3.1.1"
if [ $# -ge 1 ]; then
    VERSION=$1
fi

echo "Building Cassandra cache for version '$VERSION'."

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

function cleanup {
	exit_code=$?
	set +e
	if [[ -n $tempDir ]];then
		rm -Rf $tempDir
		echo "Deleted $tempDir."
	fi
	exit $exit_code
}

trap cleanup EXIT SIGINT SIGTERM

reaperCacheDir=${tempDir}/reaper_caches
homeCacheDir=${tempDir}/cache

mkdir -p ${reaperCacheDir}
mkdir -p ${homeCacheDir}

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

function installNodeModules {
	echo "Installing node modules."
	sudo tdnf install -y nodejs
	npm config set cache "$homeCacheDir/.npm" --global
	# Default node/npm versions in Mariner fails to build dependency node module versions due to known
	# incompatibilities.
	# Backward compatible with node@v14.18.0
	# When installing modules via npm to default prefix='/usr/local' in mariner, the permissions for 'others'
	# is incoorectly set that causes 'which' to still point to older path, as access/newfstatat fail with -ENOPERM
	# Setting a new global npm folder for fixing permission issues.
	# (works well with id=0, but reaper build will fail.)
	mkdir --mode 0777 $homeCacheDir/.npm-global
	npm config set prefix "$homeCacheDir/.npm-global"
	export PATH="$homeCacheDir/.npm-global/bin":$PATH
	npm install -g n
	export N_PREFIX="$homeCacheDir/.npm-global"
	n 14.18.0
	export XDG_CACHE_HOME=$homeCacheDir/.cache
	npm install -g bower
	# Clear bash hash tables for node/npm paths
	hash -r
	bower -v
	node -v
	npm -v
}

function buildReaperSources {
	pushd $tempDir
	sudo tdnf install -y wget
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
	pushd ${homeCacheDir}
	echo "creating bower_cache tar..."
	tar -cf ${BOWER_CACHE} .cache
	mv ${BOWER_CACHE} ${reaperCacheDir}

	echo "creating maven_cache tar..."
	tar -cf ${MAVEN_CACHE} .m2
	mv ${MAVEN_CACHE} ${reaperCacheDir}

	echo "creating npm_cache tar..."
	tar -cf ${NPM_CACHE} .npm
	mv ${NPM_CACHE} ${reaperCacheDir}
	popd

	pushd ${tempDir}/cassandra-reaper-${VERSION}/src/ui
	echo "creating bower_components tar..."
	tar -cf ${BOWER_COMPONENTS} bower_components
	mv ${BOWER_COMPONENTS} ${reaperCacheDir}

	echo "creating node_modules tar..."
	tar -cf ${SRC_UI_NODE_MODULES} node_modules
	mv ${SRC_UI_NODE_MODULES} ${reaperCacheDir}
	popd

	pushd $homeCacheDir/.npm-global/lib
	echo "creating local_lib_node_modules tar..."
	tar -cf ${LOCAL_LIB_NODE_MODULES} node_modules
	mv ${LOCAL_LIB_NODE_MODULES} ${reaperCacheDir}
	popd

	pushd $homeCacheDir/.npm-global
	echo "creating local node tar..."
	tar -cf ${LOCAL_N} n
	mv ${LOCAL_N} ${reaperCacheDir}
	popd
}

echo "Generate cassandra reaper build caches..."

checkInternet

echo "Installing msopenjdk-11."
sudo tdnf install -y msopenjdk-11

echo "Installing maven modules."
sudo tdnf install -y maven
export MAVEN_OPTS="-Dmaven.repo.local=$homeCacheDir/.m2/repository"

installNodeModules

buildReaperSources

createCacheTars

mkdir "$HOME/reaper_caches"

cp -a ${reaperCacheDir} "$HOME/reaper_caches"

echo "Copied cache tars to $HOME/reaper_caches/ .Exiting."
