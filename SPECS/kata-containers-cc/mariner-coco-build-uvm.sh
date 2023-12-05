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
sudo -E PATH=$PATH SECURITY_POLICY=yes AGENT_POLICY_FILE=../../../src/agent/samples/policy/set-policy-allowed/set-policy-allowed.rego make -B DISTRO=cbl-mariner rootfs
popd

# include both kernel-uvm and kernel-uvm-cvm modules in rootfs
# TODO once kernel-uvm and kernel-uvm-cvm are re-aligned:
# - remove this code
# - define and export a KERNEL_MODULE_DIR variable above make rootfs
# - this will cause the make rootfs command to copy the modules and call dempod
# - the current version of rootfs.sh does not support adding multiple module folder for different kernel versions
MODULE_ROOTFS_DEST_DIR="${ROOTFS_DIR}/lib/modules"
mkdir -p ${MODULE_ROOTFS_DEST_DIR}
for d in modules/*;
do
    MODULE_DIR_NAME=$(basename $d)
    cp -a "modules/${MODULE_DIR_NAME}" "${MODULE_ROOTFS_DEST_DIR}/"
    depmod -a -b "${ROOTFS_DIR}" ${MODULE_DIR_NAME}
done

# install other services
cp ${SCRIPT_DIR}/coco-opa.service        ${ROOTFS_DIR}/usr/lib/systemd/system/coco-opa.service
cp ${SCRIPT_DIR}/kata-containers.target  ${ROOTFS_DIR}/usr/lib/systemd/system/kata-containers.target
cp ${SCRIPT_DIR}/kata-agent.service.in   ${ROOTFS_DIR}/usr/lib/systemd/system/kata-agent.service
sed -i 's/@BINDIR@\/@AGENT_NAME@/\/usr\/bin\/kata-agent/g'  ${ROOTFS_DIR}/usr/lib/systemd/system/kata-agent.service

# build image
pushd ${OSBUILDER_DIR}
mv rootfs-builder/rootfs-cbl-mariner cbl-mariner_rootfs
sudo -E PATH=$PATH make DISTRO=cbl-mariner KATA_BUILD_CC=yes DM_VERITY_FORMAT=kernelinit image
popd
