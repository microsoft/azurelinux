#!/bin/sh
# Adapted from NVIDIA's Azure driver packaging:
# https://gitlab.com/nvidia/packages/azure/nvidia-driver/-/tree/610?ref_type=heads
set -e

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)

set_vars() {
    VERSION=${VERSION:-610.43.02}
   DL_SITE=${DL_SITE:-http://download.nvidia.com/XFree86}
   TEMP_UNPACK=${ARCH}
   PLATFORM=Linux-${ARCH}
   RUN_FILE=NVIDIA-${PLATFORM}-${VERSION}.run
}

run_file_get() {
    printf "Downloading installer ${RUN_FILE}... "
    [[ -f $RUN_FILE ]] || wget -c -q ${DL_SITE}/${PLATFORM}/${VERSION}/$RUN_FILE
    printf "OK\n"
}

run_file_extract() {
    rm -fr ${TEMP_UNPACK}
    sh ${RUN_FILE} --extract-only --target ${TEMP_UNPACK}
}

cleanup_folder() {

    printf "Cleaning up binaries... "

    (
        cd "${TEMP_UNPACK}"
        VERSION="${VERSION}" sh "${SCRIPT_DIR}/nvidia-cleanup-driver-files.sh"
    )

    printf "OK\n"
}

create_tarball() {

    KMOD_COMMON=nvidia-kmod-common-${VERSION}
    USR_64=nvidia-driver-${VERSION}-${ARCH}

    mkdir ${KMOD_COMMON} ${USR_64}
    mv ${TEMP_UNPACK}/firmware ${KMOD_COMMON}/
    mv ${TEMP_UNPACK}/* ${USR_64}/

    rm -fr ${TEMP_UNPACK}

    for tarball in ${KMOD_COMMON} ${USR_64}; do

        printf "Creating tarball $tarball... "

        XZ_OPT='-T0' tar --remove-files -cJf $tarball.tar.xz $tarball

        printf "OK\n"

    done
}

ARCHES=${ARCHES:-"x86_64 aarch64"}

for ARCH in $ARCHES; do
    set_vars
    run_file_get
    run_file_extract
    cleanup_folder
    create_tarball
done
