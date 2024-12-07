#!/bin/sh
type getarg > /dev/null 2>&1 || . /lib/dracut-lib.sh

# If SELinux is disabled exit now
getarg "selinux=0" > /dev/null && return 0

SELINUX="enforcing"
# shellcheck disable=SC1090
[ -e "$NEWROOT/etc/selinux/config" ] && . "$NEWROOT/etc/selinux/config"
[ "$SELINUX" == "disabled" ] && return 0

getargbool 0 rd.live.overlay.overlayfs && overlayfs="yes"

if [ -n "$overlayfs" ]; then

    # Get the current root folder context
    rootDirContext=$($NEWROOT/usr/sbin/matchpathcon -f $NEWROOT/etc/selinux/targeted/contexts/files/file_contexts -m dir /)

    # Parse the context to extract the label
    # The contextshould on the form: "/       system_u:object_r:root_t:s0"
    IFS='\t' read -r _ selinux <<< "$rootDirContext"
    echo "root folder context: ($selinux)"
    IFS=':' read -r _ _ dirLabel _ <<< "$selinux"
    echo "root folder label  : ($dirLabel)"

    # Set the labels on the target files
    [ -e /sysroot ] && chcon -t $dirLabel /sysroot
    [ -e /run/overlayfs ] && chcon -t $dirLabel /run/overlayfs
    [ -e /run/ovlwork ] && chcon -t $dirLabel /run/ovlwork
fi
