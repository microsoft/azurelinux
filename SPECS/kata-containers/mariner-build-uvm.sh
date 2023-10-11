#!/bin/bash

readonly SCRIPT_DIR=$(dirname "$(readlink -f "$0")")
readonly OSBUILDER_DIR=${SCRIPT_DIR}/tools/osbuilder
readonly ROOTFS_DIR=${SCRIPT_DIR}/tools/osbuilder/rootfs-builder/rootfs-cbl-mariner
readonly INITRD_DIR="/var/cache/kata-containers/osbuilder-images/kernel-uvm"

export AGENT_SOURCE_BIN=${SCRIPT_DIR}/agent/usr/bin/kata-agent

rm -rf ${ROOTFS_DIR}

# build rootfs
pushd ${OSBUILDER_DIR}
sudo make clean
rm -rf ${ROOTFS_DIR}
sudo -E PATH=$PATH make -B DISTRO=cbl-mariner rootfs
popd

# copy service files
cp ${SCRIPT_DIR}/agent/usr/lib/systemd/system/kata-containers.target  ${ROOTFS_DIR}/usr/lib/systemd/system/kata-containers.target
cp ${SCRIPT_DIR}/agent/usr/lib/systemd/system/kata-agent.service   ${ROOTFS_DIR}/usr/lib/systemd/system/kata-agent.service

# build initrd
pushd ${OSBUILDER_DIR}
sudo -E PATH=$PATH make DISTRO=cbl-mariner TARGET_ROOTFS=${ROOTFS_DIR} initrd
popd
