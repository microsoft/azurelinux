#!/bin/sh
# Portions Copyright (c) 2020 Microsoft Corporation

# See verity-parse.sh for documentation.

# Make sure we have dracut-lib and loaded
type getarg >/dev/null 2>&1 || . /lib/dracut-lib.sh

VERITY_MOUNT="/verity_root/verity_mnt"
OVERLAY_TMPFS="/verity_root/overlays"
OVERLAY_MNT_OPTS="rw,nodev,nosuid,nouser,noexec"

# Get verity root. This should already be set by the dracut cmdline module
[ -n "$root" ] || root=$(getarg root=)
# Bail early if no 'verityroot' root is found
[ "${root%%:*}" = "verityroot" ] || exit 0
verityroot="$root"

# Double check we have all other parameters
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
[ -z "${verityoverlays}" ] && verityoverlays=$(getarg rd.verityroot.overlays=)
[ -z "${verityoverlaysize}" ] && verityoverlaysize=$(getarg rd.verityroot.overlaysize=)
[ -z "${overlaysdebugmount}" ] && overlaysdebugmount=$(getarg rd.verityroot.overlays_debug_mount=)

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

# create_overlay <path>
#
# Create a writable overlay for a folder <path> inside the verity disk.
# The path must already exist in the verity disk for an overlay to be added.
#	$1: Path relative to the rootfs (ie '/var')
create_overlay() {
    local _folder=$1
    local _mounted_folder="${VERITY_MOUNT}/${_folder}"
    local _overlay_name="$(str_replace ${_mounted_folder} '/' '_')"
    local _overlay_folder="$(mkuniqdir ${OVERLAY_TMPFS} ${_overlay_name})"
    local _working="${_overlay_folder}/working"
    local _upper="${_overlay_folder}/upper"

    [ -d "${_overlay_folder}" ] || die "Failed to create overlay base folder '${_overlay_folder}'"
    
    info "Creating a R/W overlay for $_folder"
    [ -d "$_mounted_folder" ] || die "$_folder does not exist, cannot create overlay"
    
    [ ! -d "${_working}" ] || die "Name collision with ${_working}"
    [ ! -d "${_upper}" ] || die "Name collision with ${_upper}"
    
    mkdir -p "${_working}" && \
    mkdir -p "${_upper}" && \
    mount -t overlay overlay -o ${OVERLAY_MNT_OPTS},lowerdir="${_mounted_folder}",upperdir="${_upper}",workdir="${_working}" "${_mounted_folder}" || \
        die "Failed to mount overlay in ${_mounted_folder}"
}

# Mount the verity disk to $NEWROOT, create a dummy device at /dev/root to
# satisfy wait_for_dev
mount_root() {
    info "Mounting verity root"
    mkdir -p "${VERITY_MOUNT}"

    # Convert error handling options into argument
    if [ "${verityerrorhandling}" == "restart" ]; then
        errorarg="--restart-on-corruption"
    elif [ "${verityerrorhandling}" == "panic" ]; then
        errorarg="--panic-on-corruption"
    elif [ "${verityerrorhandling}" == "ignore" ]; then
        errorarg="--ignore-corruption"
    fi

    # Convert FEC options to argument
    if [ -n "${verityfecdata}" -a -n "${verityfecroots}" ]; then
        fecargs="--fec-device=${verityfecdata} --fec-roots=${verityfecroots}"
    fi

    # Convert root hash signature to argument
    if [ -n "${verityroothashsig}" ]; then
        roothashsigargs="--root-hash-signature=${verityroothashsig}"
    fi

    # Get the root hash itself
    if [ -n "${verityroothash}" ]; then
        roothashval="${verityroothash}"
    else
        roothashval=$(cat "${verityroothashfile}")
    fi

    if [ "${validateonboot}" == "true" ]; then
        # verify does not support error handling args, ommit
        info "rd.verityroot.validateonboot is set, validating full read-only root device"
        info "This could take several minutes if forward error correction is being used to rebuild corrupted blocks"
        veritysetup --debug --verbose ${roothashsigargs} ${fecargs} verify ${veritydisk} ${verityhashtree} ${roothashval} > verity.log 2>&1 || \
            { warn "Failed to validate verity disk" ; cat verity.log | vwarn ; }

        # Report any FEC activity, this indicates possible disk failure
        if grep "# Verification failed, trying to repair with FEC device." verity.log; then
            warn "Verity disk is corrupted, proceding while using forward error correction"
            grep "Found [0-9]* repairable errors with FEC device" verity.log | vwarn
        fi
    fi

    info "Creating dm-verity read-only root"
    veritysetup --debug --verbose ${roothashsigargs} ${errorarg} ${fecargs} open ${veritydisk} ${veritydevicename} ${verityhashtree} ${roothashval} > verity.log 2>&1 || \
        { cat verity.log | vwarn ; die "Failed to create verity root" ; }
    
    mount -o ro,defaults "/dev/mapper/${veritydevicename}" "${VERITY_MOUNT}" || \
        die "Failed to mount verity root"
    
    if [ -n "${verityoverlays}" ]; then
        # Create working directories for overlays
        mkdir -p "${OVERLAY_TMPFS}"
        mount -t tmpfs tmpfs -o ${OVERLAY_MNT_OPTS},size=${verityoverlaysize} "${OVERLAY_TMPFS}" || \
            die "Failed to create overlay tmpfs at ${OVERLAY_TMPFS}"
        
        for _folder in ${verityoverlays}; do
            create_overlay "${_folder}"
        done
        
        if [ -n "${overlaysdebugmount}" ]; then
            info "Adding overlay debug mount to ${overlaysdebugmount}"
            mount -o ro --bind "${OVERLAY_TMPFS}" "${VERITY_MOUNT}/${overlaysdebugmount}" || warn "Couldn't mount overlay debug (Does '${overlaysdebugmount}' exist?)"
        fi
    else
        info "No verity RW overlays set, mounting fully read-only"
    fi

    # Remount the verity disk and any overlays into the destination root
    mount --rbind "${VERITY_MOUNT}" "${NEWROOT}"

    # Signal completion 
    ln -s /dev/null /dev/root
}

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

if [ -n "$verityroot" -a -z "${verityroot%%verityroot:*}" ]; then
    veritydisk=$(expand_persistent_dev "${verityroot#verityroot:}")
    verityhashtree=$(expand_persistent_dev "${verityhashtree}")
    verityroothashfile=$(expand_persistent_dev "${verityroothashfile}")
    verityfecdata=$(expand_persistent_dev "${verityfecdata}")
    mount_root
fi
