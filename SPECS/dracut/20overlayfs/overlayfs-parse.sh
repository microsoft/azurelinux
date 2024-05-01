#!/bin/bash
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

# See overlayfs-setup.sh for documentation.

# Make sure we have dracut-lib and loaded.
type getarg >/dev/null 2>&1 || . /lib/dracut-lib.sh

# Retrieve the verity root or regular root.
[ -z "$root" ] && root=$(getarg root=)
if [[ "$root" == *"/dev/mapper/root"* ]]; then
    wait_for_dev "/dev/mapper/root"
else
    # Remove 'block:' prefix if present.
    root_device=$(expand_persistent_dev "${root#block:}")
    wait_for_dev root_device
fi

# Retrieve the OverlayFS parameters.
[ -z "${overlayfs}" ] && overlayfs=$(getarg rd.overlayfs=)

for _group in ${overlayfs}; do
    IFS=',' read -r overlay upper work volume <<< "$_group"

    # Resolve volume to its full device path.
    volume=$(expand_persistent_dev "$volume")

    if [[ "$volume" == "" ]]; then
        
    else
        wait_for_dev "$volume"
    fi
done

# Keep a copy of this function here from verity-read-only-root package.
expand_persistent_dev() {
    local _dev=$1

    case "$_dev" in
        LABEL=*)
            _dev="/dev/disk/by-label/${_dev#LABEL=}"
            ;;
        UUID=*)
            _dev="${_dev#UUID=}"
            _dev="${_dev,,}"
            _dev="/dev/disk/by-uuid/${_dev}"
            ;;
        PARTUUID=*)
            _dev="${_dev#PARTUUID=}"
            _dev="${_dev,,}"
            _dev="/dev/disk/by-partuuid/${_dev}"
            ;;
        PARTLABEL=*)
            _dev="/dev/disk/by-partlabel/${_dev#PARTLABEL=}"
            ;;
    esac
    printf "%s" "$_dev"
}
