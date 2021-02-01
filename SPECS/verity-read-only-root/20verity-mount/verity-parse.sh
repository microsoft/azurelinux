#!/bin/sh
# Portions Copyright (c) 2020 Microsoft Corporation

# Overview:
#   The verity-mount module is responsible for mounting a dm-verity protected read-only
#   root file system. (see https://gitlab.com/cryptsetup/cryptsetup/-/wikis/DMVerity)
#   To load a dm-verity disk both a hash tree and root hash must be available. The
#   verity-mount module may load the hash tree from a device or as a file inside the
#   initramfs. The root hash is expected as a file in the initramfs.
#
# Error Correction:
#   Optionally forward error correction (FEC) may also be used. dm-verity will use the
#   FEC to patch any corrupted data at run time (but will not repair the underlying data).
#   Error correction normally happens only as required (when blocks are read). The
#   rd.verityroot.validateonboot argument will force a full validation of all blocks
#   at boot and print any issues as dracut warnings (This can take several minutes if
#   the disk is degraded)
#
# Signing:
#   The expectation is that the initramfs (and its enclosed root hash) will be signed.
#   The root hash can then be trusted because the initramfs was validated during boot.
#   dm-verity also supports cryptographically signing the root hash, the signature file is
#   expected to be part of the initramfs and will be validated against the kernel key-ring.
#
# Overlays:
#   Many packages expect to be able to write files to disk during day-to-day operations. To
#   accomodate these programs the verity-mount module can create tmpfs overlays in targeted
#   locations. These overlays are not persistant and will be created fresh on every boot.
#
# Debugging:
#   The verity-mount module will mount a read-only view of the tmpfs overlays into 
#   rd.verityroot.overlays_debug_mount=/path/to/mount if set. This is an easy way to see
#   what files are being modified during runtime.

# Parameters:
#   Required:
#       rd.verityroot.devicename=desired_device_mapper_name
#       rd.verityroot.hashtree=/path/to/hashtree | <DEVICE_TYPE>=<DEVICE_ID>
#       rd.verityroot.roothash=<SHA256_HASH>
#           or
#       rd.verityroot.roothashfile=/path/to/roothash

#   Optional
#       rd.verityroot.roothashsig=/path/to/file
#       rd.verityroot.verityerrorhandling=ignore|restart|panic
#       rd.verityroot.validateonboot=true/false
#       rd.verityroot.fecdata=/path/to/fecdata | <DEVICE_TYPE>=<DEVICE_ID>
#       rd.verityroot.fecroots=#
#       rd.verityroot.overlays="/path/to/overlay/directory /other/path"
#       rd.verityroot.overlays_debug_mount=/path/to/mount/debug/info

# Make sure we have dracut-lib and loaded
type getarg >/dev/null 2>&1 || . /lib/dracut-lib.sh

# Look for a root device parameter of the form: root=verityroot:<DEVICE_TYPE>=<DEVICE_ID>
[ -z "$root" ] && root=$(getarg root=)
if [ "${root%%:*}" = "verityroot" ] ; then
    verityroot=$root
fi

# Bail early if no 'verityroot' root is found
[ "${verityroot%%:*}" = "verityroot" ] || exit 0

# Get all other required parameters
[ -z "${veritydevicename}" ] && veritydevicename=$(getarg rd.verityroot.devicename=)
[ -n "${veritydevicename}" ] || veritydevicename="verity_root"
[ -z "${verityhashtree}" ] && verityhashtree=$(getarg rd.verityroot.hashtree=)
[ -z "${verityroothash}" ] && verityroothash=$(getarg rd.verityroot.roothash=)
[ -z "${verityroothashfile}" ] && verityroothashfile=$(getarg rd.verityroot.roothashfile=)

# Get the optional parameters
[ -z "${verityroothashsig}" ] && verityroothashsig=$(getarg rd.verityroot.roothashsig=)
[ -z "${verityerrorhandling}" ] && verityerrorhandling=$(getarg rd.verityroot.verityerrorhandling=)
[ -z "${validateonboot}" ] && validateonboot=$(getarg rd.verityroot.validateonboot=)
[ -z "${verityfecdata}" ] && verityfecdata=$(getarg rd.verityroot.fecdata=)
[ -z "${verityfecroots}" ] && verityfecroots=$(getarg rd.verityroot.fecroots=)
[ -z "${verityoverlays}" ] && overlays=$(getarg rd.verityroot.overlays=)
[ -z "${verityoverlaysize}" ] && overlaysize=$(getarg rd.verityroot.overlaysize=)
[ -z "${overlays_debug_mount}" ] && overlays_debug_mount=$(getarg rd.verityroot.overlays_debug_mount=)

# Check the required parameters are pressent
[ -n "${veritydevicename}" ] || die "verityroot requires rd.verityroot.devicename="
[ -n "${verityhashtree}" ] || die "verityroot requires rd.verityroot.hashtree="
[ -n "${verityroothash}" ] || [ -n "${verityroothashfile}" ] || die "verityroot requires rd.verityroot.roothash= or rd.verityroot.roothashfile="
[ -n "${verityroothash}" -a -n "${verityroothashfile}" ] && die "verityroot does not support using both rd.verityroot.roothash= and rd.verityroot.roothashfile= at the same time"

# Validate the optional paramters
# Make sure we have either both or neither FEC arguments (xor)
[ -n "${verityfecdata}" -a -z "${verityfecroots}" ] && die "verityroot FEC requires both rd.verityroot.fecdata= and rd.verityroot.fecroots="
[ -z "${verityfecdata}" -a -n "${verityfecroots}" ] && die "verityroot FEC requires both rd.verityroot.fecdata= and rd.verityroot.fecroots="

# Make sure we have set an overlay size if we are using overlays
if [ -n "${verityoverlays}" ]; then
    [ -z "${verityoverlaysize}" ] && die "verityroot rd.verityroot.overlaysize= must be set if using rd.verityroot.overlays="
fi

# Check we have a valid error handling option
if [ -n "${verityerrorhandling}" ]; then 
    [ "${verityerrorhandling}" == "ignore" -o \
    "${verityerrorhandling}" == "restart" -o \
    "${verityerrorhandling}" == "panic" ] || die "verityroot rd.verityroot.verityerrorhandling= must be one of [ignore,restart,panic]"
fi
# Same for full validation during boot option
if [ -n "${validateonboot}" ]; then 
    [ "${validateonboot}" == "true" -o \
    "${validateonboot}" == "false" ] || die "verityroot rd.verityroot.validateonboot= must be one of [true,false]"
fi

# dracut-functions.sh is only available during initramfs creation,
# keep a copy of this function here.
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

# Get paths to the various devices/files we might need to wait for.
veritydisk=$(expand_persistent_dev "${verityroot#verityroot:}")
verityhashtree=$(expand_persistent_dev "${verityhashtree}")
verityroothashfile=$(expand_persistent_dev "${verityroothashfile}")
verityfecdata=$(expand_persistent_dev "${verityfecdata}")

info "Going to try to mount '$verityroot' with '$verityhashtree' and '$verityroothash$verityroothashfile'"
rootok=1
unset root
root="${verityroot}"

# Queue up a wait for each device/file
if [ "${root%%:*}" = "verityroot" ]; then
    for _dev in ${veritydisk} ${verityhashtree} ${verityroothashfile} ${verityfecdata}; do
        wait_for_dev "${_dev}"
    done
fi
