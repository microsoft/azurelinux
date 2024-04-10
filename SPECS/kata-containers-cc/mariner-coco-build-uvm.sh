#!/bin/bash
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

set -o errexit

[ -n "${DEBUG:-}" ] && set -o xtrace

readonly SCRIPT_DIR=$(dirname "$(readlink -f "$0")")
readonly ROOTFS_DIR=${SCRIPT_DIR}/tools/osbuilder/rootfs-builder/rootfs-cbl-mariner
readonly OSBUILDER_DIR=${SCRIPT_DIR}/tools/osbuilder
export AGENT_SOURCE_BIN=${SCRIPT_DIR}/kata-agent

# build rootfs
pushd ${OSBUILDER_DIR}
sudo make clean
rm -rf ${ROOTFS_DIR}
sudo -E PATH=$PATH AGENT_POLICY=yes CONF_GUEST=yes AGENT_POLICY_FILE=allow-set-policy.rego make -B DISTRO=cbl-mariner rootfs
popd

MODULE_ROOTFS_DEST_DIR="${ROOTFS_DIR}/lib/modules"
mkdir -p ${MODULE_ROOTFS_DEST_DIR}

pushd modules/*
# get kernel modules version
export KERNEL_MODULES_VER=$(basename $PWD)
export KERNEL_MODULES_DIR=${SCRIPT_DIR}/modules/${KERNEL_MODULES_VER}
# copy kernel modules to rootfs
cp -a ${KERNEL_MODULES_DIR} "${MODULE_ROOTFS_DEST_DIR}/"
# run depmod
depmod -a -b ${ROOTFS_DIR} ${KERNEL_MODULES_VER}
popd

# Install other services.
#
# This is needed because we don't use `make install-services` (which installs
# the service files on the host by default), therefore the rootfs builder can't
# symlink the services from the host into the rootfs.
cp ${SCRIPT_DIR}/kata-containers.target  ${ROOTFS_DIR}/usr/lib/systemd/system/kata-containers.target
cp ${SCRIPT_DIR}/kata-agent.service.in   ${ROOTFS_DIR}/usr/lib/systemd/system/kata-agent.service
sed -i 's/@BINDIR@\/@AGENT_NAME@/\/usr\/bin\/kata-agent/g'  ${ROOTFS_DIR}/usr/lib/systemd/system/kata-agent.service

# build image
pushd ${OSBUILDER_DIR}
mv rootfs-builder/rootfs-cbl-mariner cbl-mariner_rootfs
sudo -E PATH=$PATH make DISTRO=cbl-mariner MEASURED_ROOTFS=yes DM_VERITY_FORMAT=kernelinit image
popd
