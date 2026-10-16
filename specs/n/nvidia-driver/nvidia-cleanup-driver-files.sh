#!/bin/sh
# Adapted from NVIDIA's Azure driver packaging:
# https://gitlab.com/nvidia/packages/azure/nvidia-driver/-/blob/610/nvidia-driver/nvidia-generate-tarballs.sh
set -e

: "${VERSION:?VERSION must be set}"

# Remove content that is built separately or not shipped by these packages.
rm -rf \
    kernel kernel-open \
    nvidia-xconfig* \
    nvidia-persistenced* \
    nvidia-modprobe* \
    libnvidia-gtk* libnvidia-wayland-client* nvidia-settings* \
    libGLESv1_CM.so.* libGLESv2.so.* libGLdispatch.so.* libOpenGL.so.* libGLX.so.* libGL.so.1* libEGL.so.1* \
    libnvidia-egl-wayland.so.* libnvidia-egl-gbm.so.* libnvidia-egl-xcb.so.* libnvidia-egl-xlib.so.* \
    libnvidia-egl-wayland2.so.* \
    libOpenCL.so.1* \
    "libEGL.so.${VERSION}" \
    nvidia-installer* .manifest make* mk* libglvnd_install_checker \
    libEGL_nvidia.so.* libGLESv1_CM_nvidia.so.* libGLESv2_nvidia.so.* libGLX_nvidia.so.* libglxserver_nvidia.so.* \
    libnvidia-allocator.so.* libnvidia-api.so.* libnvidia-eglcore.so.* \
    libnvidia-fbc.so.* libnvidia-glcore.so.* libnvidia-glsi.so.* libnvidia-glvkspirv.so.* \
    libnvidia-ngx.so.* libnvidia-present.so.* libnvidia-rtcore.so.* libnvidia-tls.so.* libnvidia-vksc-core.so.* \
    libnvoptix.so.* libvdpau_nvidia.so.* \
    libnvidia-pkcs11.so.* \
    libnvidia-mncc.so.* \
    *.swidtag *nvidia*.json 32
