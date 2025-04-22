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

    # Parse the context to extract the root folder '/' context type.
    # The line should be on the form: "/       system_u:object_r:root_t:s0"

    # Split folder and context
    IFS='\t' read -r _ selinuxContext <<< "$rootDirContext"
    echo "root folder context: ($selinuxContext)"

    # Split context and extract its type
    IFS=':' read -r _ _ contextType _ <<< "$selinuxContext"
    echo "root folder label  : ($contextType)"

    # Set the type on the target folders
    CHCON_TOOL=$NEWROOT/usr/bin/chcon
    [ -e /sysroot ] && $CHCON_TOOL -t $contextType /sysroot
    [ -e /run/overlayfs ] && $CHCON_TOOL -t $contextType /run/overlayfs
    [ -e /run/ovlwork ] && $CHCON_TOOL -t $contextType /run/ovlwork
fi
