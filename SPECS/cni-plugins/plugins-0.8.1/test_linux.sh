#!/usr/bin/env bash
#
# Run CNI plugin tests.
# 
# This needs sudo, as we'll be creating net interfaces.
#
set -e

# switch into the repo root directory
cd "$(dirname $0)"

# Build all plugins before testing
source ./build_linux.sh

echo "Running tests"

function testrun {
    sudo -E bash -c "umask 0; cd ${GOPATH}/src; PATH=${GOROOT}/bin:$(pwd)/bin:${PATH} go test $@"
}

COVERALLS=${COVERALLS:-""}

if [ -n "${COVERALLS}" ]; then
    echo "with coverage profile generation..."
else
    echo "without coverage profile generation..."
fi

PKG=${PKG:-$(cd ${GOPATH}/src/${REPO_PATH}; go list ./... | xargs echo)}

# coverage profile only works per-package
i=0
for t in ${PKG}; do
    if [ -n "${COVERALLS}" ]; then
        COVERFLAGS="-covermode set -coverprofile ${i}.coverprofile"
    fi
    testrun "${COVERFLAGS:-""} ${t}"
    i=$((i+1))
done

# Submit coverage information
if [ -n "${COVERALLS}" ]; then
    gover
    goveralls -service=travis-ci -coverprofile=gover.coverprofile
fi

echo "Checking gofmt..."
fmtRes=$(go fmt $PKG)
if [ -n "${fmtRes}" ]; then
	echo -e "go fmt checking failed:\n${fmtRes}"
	exit 255
fi

echo "Checking govet..."
vetRes=$(go vet $PKG)
if [ -n "${vetRes}" ]; then
	echo -e "govet checking failed:\n${vetRes}"
	exit 255
fi
