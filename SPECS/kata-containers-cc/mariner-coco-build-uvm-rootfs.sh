#!/bin/bash
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

set -o errexit

[ -n "${DEBUG:-}" ] && set -o xtrace

readonly SCRIPT_DIR=$(dirname "$(readlink -f "$0")")
readonly ROOTFS_DIR=${SCRIPT_DIR}/tools/osbuilder/rootfs-builder/rootfs-cbl-mariner
readonly ROOTFS_TARGET=/opt/mariner/share/uvm
export AGENT_SOURCE_BIN=${SCRIPT_DIR}/kata-agent

# get kernel modules version
pushd modules/*
export KERNEL_MODULES_VER=$(basename $PWD)
export KERNEL_MODULES_DIR=${SCRIPT_DIR}/modules/${KERNEL_MODULES_VER}
popd

# build rootfs
sudo -E PATH=$PATH ./tools/osbuilder/rootfs-builder/rootfs.sh cbl-mariner

# run depmod for kernel modules
depmod -a -b ${ROOTFS_DIR} ${KERNEL_MODULES_VER}

# install other services
cp ${SCRIPT_DIR}/coco-opa.service        ${ROOTFS_DIR}/usr/lib/systemd/system/
cp ${SCRIPT_DIR}/kata-containers.target  ${ROOTFS_DIR}/usr/lib/systemd/system/
cp ${SCRIPT_DIR}/kata-agent.service.in   ${ROOTFS_DIR}/usr/lib/systemd/system/kata-agent.service
sudo sed -i 's/@BINDIR@\/@AGENT_NAME@/\/usr\/bin\/kata-agent/g'  ${ROOTFS_DIR}/usr/lib/systemd/system/kata-agent.service

pushd ${ROOTFS_TARGET}
sudo mv ${ROOTFS_DIR} .
popd
