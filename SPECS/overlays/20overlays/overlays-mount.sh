#!/bin/sh

# Ensure that the 'dracut-lib' is present and loaded.
type getarg >/dev/null 2>&1 || . /lib/dracut-lib.sh

VERITY_MOUNT="/verity_mnt"
OVERLAY_MNT_OPTS="rw,nodev,nosuid,nouser,noexec"

# Retrieve Overlays parameters.
[ -z "${overlays}" ] && overlays=$(getarg rd.overlays=)

create_overlay() {
    local _dir=$1
    local _upper=$2
    local _work=$3
    local _mounted_dir="${VERITY_MOUNT}/${_dir}"

    info "Creating a R/W overlay for $_dir"
    [ -d "$_mounted_dir" ] || die "$_dir does not exist, cannot create overlay"

    # Assume upper and work layer will be prepared here.
    [ ! -d "${_upper}" ] || die "Name collision with ${_upper}"
    [ ! -d "${_work}" ] || die "Name collision with ${_work}"

    mkdir -p "${_upper}" && \
    mkdir -p "${_work}" && \
    mount -t overlay overlay -o ${OVERLAY_MNT_OPTS},lowerdir="${_mounted_dir}",upperdir="${_upper}",workdir="${_work}" "${_mounted_dir}" || \
        die "Failed to mount overlay in ${_mounted_dir}"
}

mount_root() {
    info "Mounting dm-verity root"
    mkdir -p "${VERITY_MOUNT}"
    mount -o ro,defaults "/dev/mapper/root" "${VERITY_MOUNT}" || \
        die "Failed to mount dm-verity root"
    
    for _group in ${overlays}; do
        IFS=',' read -r overlay upper work <<< "$_group"
        create_overlay "$overlay" "$upper" "$work"
    done

    # Re-mount the verity mount along with all overlays to the sysroot.
    mount --rbind "${VERITY_MOUNT}" "${NEWROOT}"
}
