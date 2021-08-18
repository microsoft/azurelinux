#!/usr/bin/env bash
set -xe

SRC_DIR="${SRC_DIR:-$PWD}"
DOCKER="${DOCKER:-docker}"

TAG=$(git describe --tags --dirty)
RELEASE_DIR=release-${TAG}

BUILDFLAGS="-ldflags '-extldflags -static -X github.com/containernetworking/plugins/pkg/utils/buildversion.BuildVersion=${TAG}'"

OUTPUT_DIR=bin

# Always clean first
rm -Rf ${SRC_DIR}/${RELEASE_DIR}
mkdir -p ${SRC_DIR}/${RELEASE_DIR}
mkdir -p ${OUTPUT_DIR}

$DOCKER run -ti -v ${SRC_DIR}:/go/src/github.com/containernetworking/plugins --rm golang:1.12-alpine \
/bin/sh -xe -c "\
    apk --no-cache add bash tar;
    cd /go/src/github.com/containernetworking/plugins; umask 0022;

    for arch in amd64 arm arm64 ppc64le s390x; do \
        rm -f ${OUTPUT_DIR}/*; \
        CGO_ENABLED=0 GOARCH=\$arch ./build_linux.sh ${BUILDFLAGS}; \
        for format in tgz; do \
            FILENAME=cni-plugins-linux-\$arch-${TAG}.\$format; \
            FILEPATH=${RELEASE_DIR}/\$FILENAME; \
            tar -C ${OUTPUT_DIR} --owner=0 --group=0 -caf \$FILEPATH .; \
        done; \
    done;

    rm -rf ${OUTPUT_DIR}/*; \
    CGO_ENABLED=0 GOARCH=amd64 ./build_windows.sh ${BUILDFLAGS}; \
    for format in tgz; do \
        FILENAME=cni-plugins-windows-amd64-${TAG}.\$format; \
        FILEPATH=${RELEASE_DIR}/\$FILENAME; \
        tar -C ${OUTPUT_DIR} --owner=0 --group=0 -caf \$FILEPATH .; \
    done;


    cd ${RELEASE_DIR};
      for f in *.tgz; do sha1sum \$f > \$f.sha1; done;
      for f in *.tgz; do sha256sum \$f > \$f.sha256; done;
      for f in *.tgz; do sha512sum \$f > \$f.sha512; done;
    cd ..
    chown -R ${UID} ${OUTPUT_DIR} ${RELEASE_DIR}"
