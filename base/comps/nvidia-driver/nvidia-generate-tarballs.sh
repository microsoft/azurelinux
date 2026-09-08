#!/bin/sh
set -e

set_vars() {
   VERSION=${VERSION:-610.57.04}
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

    cd ${TEMP_UNPACK}

    # Stuff not needed for packages:
    #   - Compiled from source
    #   - Interactive installer files
    #   - GLVND GL libraries
    #   - Internal development only libraries
    #   - Desktop libraries
    #   - Desktop libraries for 32 bit compatibility
    #   - Kernel module sources
    rm -fr \
        kernel kernel-open \
        nvidia-xconfig* \
        nvidia-persistenced* \
        nvidia-modprobe* \
        libnvidia-gtk* libnvidia-wayland-client* nvidia-settings* \
        libGLESv1_CM.so.* libGLESv2.so.* libGLdispatch.so.* libOpenGL.so.* libGLX.so.* libGL.so.1* libEGL.so.1* \
        libnvidia-egl-wayland.so.* libnvidia-egl-gbm.so.* libnvidia-egl-xcb.so.* libnvidia-egl-xlib.so.* \
        libnvidia-egl-wayland2.so.* \
        libOpenCL.so.1* \
        libEGL.so.${VERSION} \
        nvidia-installer* .manifest make* mk* libglvnd_install_checker \
        libEGL_nvidia.so.* libGLESv1_CM_nvidia.so.* libGLESv2_nvidia.so.* libGLX_nvidia.so.* libglxserver_nvidia.so.* \
        libnvidia-allocator.so.* libnvidia-api.so.* libnvidia-eglcore.so.* \
        libnvidia-fbc.so.* libnvidia-glcore.so.* libnvidia-glsi.so.* libnvidia-glvkspirv.so.* \
        libnvidia-ngx.so.* libnvidia-present.so.* libnvidia-rtcore.so.* libnvidia-tls.so.* libnvidia-vksc-core.so.* \
        libnvoptix.so.* libvdpau_nvidia.so.* \
        libnvidia-pkcs11.so.* \
        libnvidia-mncc.so.* \
        *.swidtag *nvidia*.json 32

    cd ..

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
