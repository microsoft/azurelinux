#!/bin/sh

# Ensure that the 'dracut-lib' is present and loaded.
type getarg >/dev/null 2>&1 || . /lib/dracut-lib.sh

VERITY_MOUNT="systemd_verity/verity_mnt"
OVERLAYS_TMPFS="systemd_verity/overlays"
OVERLAYS_MNT_OPTS="rw,nodev,nosuid,nouser,noexec"

# Retrieve the verity root. It is expected to be predefined by the dracut cmdline module.
[ -z "$root" ] && root=$(getarg root=)
[ "$root" = "/dev/mapper/root" ] || exit 0
# Retrieve the Overlays parameters.
[ -z "${overlays}" ] && overlays=$(getarg rd.overlays=)
[ -z "${overlaysize}" ] && overlaysize=$(getarg rd.overlaysize=)

# Verify that an overlay size is specified when using overlay file systems.
if [ -n "${overlays}" ]; then
    [ -z "${overlaysize}" ] && die "rd.overlaysize= must be set if using rd.overlays="
fi

create_overlay() {
    local _dir=$1
    local _mounted_dir="${VERITY_MOUNT}/${_dir}"
    local _upper_dir=$2
    local _work_dir=$3
    local _upper="${OVERLAYS_TMPFS}/${_upper_dir}"
    local _work="${OVERLAYS_TMPFS}/${_work_dir}"

    [ -d "$_mounted_dir" ] || die "Unable to create overlay as $_dir does not exist"

    [ ! -d "${_upper}" ] || die "Conflict in naming with ${_upper}"
    [ ! -d "${_work}" ] || die "Conflict in naming with ${_work}"

    mkdir -p "${_upper}" && \
    mkdir -p "${_work}" && \
    mount -t overlay overlay -o ${OVERLAY_MNT_OPTS},lowerdir="${_mounted_dir}",upperdir="${_upper}",workdir="${_work}" "${_mounted_dir}" || \
        die "Failed to mount overlay in ${_mounted_dir}"
}

mount_root() {
    info "Mounting DM-Verity Target"
    mkdir -p "${VERITY_MOUNT}"
    mount -o ro,defaults "/dev/mapper/root" "${VERITY_MOUNT}" || \
        die "Failed to mount dm-verity root target"
    
    info "Creating Overlays"
    mkdir -p "${OVERLAYS_TMPFS}"
    mount -t tmpfs tmpfs -o ${OVERLAYS_MNT_OPTS},size=${overlaysize} "${OVERLAYS_TMPFS}" || \
            die "Failed to create overlay tmpfs at ${OVERLAYS_TMPFS}"

    for _group in ${overlays}; do
        IFS=',' read -r overlay upper work <<< "$_group"
        create_overlay "$overlay" "$upper" "$work"
    done

    info "Done Verity Root Mounting and Overlays Mounting"
    # Re-mount the verity mount along with all overlays to the sysroot.
    mount --rbind "${VERITY_MOUNT}" "${NEWROOT}"
}

mount_root
