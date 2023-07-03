#!/bin/bash
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

set -o errexit

[ -n "${DEBUG:-}" ] && set -o xtrace

readonly SCRIPT_DIR=$(dirname "$(readlink -f "$0")")
readonly ROOTFS_DIR=${SCRIPT_DIR}/tools/osbuilder/rootfs-builder/rootfs-cbl-mariner
readonly OSBUILDER_DIR=${SCRIPT_DIR}/tools/osbuilder
export AGENT_SOURCE_BIN=${SCRIPT_DIR}/kata-agent

# get kernel modules version
pushd modules/*
export KERNEL_MODULES_VER=$(basename $PWD)
export KERNEL_MODULES_DIR=${SCRIPT_DIR}/modules/${KERNEL_MODULES_VER}
popd

# build rootfs
pushd ${OSBUILDER_DIR}
sudo make clean
rm -rf ${ROOTFS_DIR}
sudo -E PATH=$PATH make -B DISTRO=cbl-mariner rootfs
popd

# run depmod for kernel modules
depmod -a -b ${ROOTFS_DIR} ${KERNEL_MODULES_VER}

# install other services
cp ${SCRIPT_DIR}/coco-opa.service        ${ROOTFS_DIR}/usr/lib/systemd/system/coco-opa.service
cp ${SCRIPT_DIR}/kata-containers.target  ${ROOTFS_DIR}/usr/lib/systemd/system/kata-containers.target
cp ${SCRIPT_DIR}/kata-agent.service.in   ${ROOTFS_DIR}/usr/lib/systemd/system/kata-agent.service
sed -i 's/@BINDIR@\/@AGENT_NAME@/\/usr\/bin\/kata-agent/g'  ${ROOTFS_DIR}/usr/lib/systemd/system/kata-agent.service

# build initrd
pushd ${OSBUILDER_DIR}
sudo -E PATH=$PATH make DISTRO=cbl-mariner TARGET_ROOTFS=${ROOTFS_DIR} initrd
popd
