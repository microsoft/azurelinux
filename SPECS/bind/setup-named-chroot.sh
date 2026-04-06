#!/bin/bash

ROOTDIR="$1"
CONFIG_FILES="${3:-/etc/named-chroot.files}"

usage()
{
  echo
  echo 'This script setups chroot environment for BIND'
  echo 'Usage: setup-named-chroot.sh ROOTDIR <on|off> [chroot.files]'
}

if ! [ "$#" -ge 2 -a "$#" -le 3 ]; then
  echo 'Wrong number of arguments'
  usage
  exit 1
fi

# Exit if ROOTDIR doesn't exist
if ! [ -d "$ROOTDIR" ]; then
  echo "Root directory $ROOTDIR doesn't exist"
  usage
  exit 1
fi

if ! [ -r "$CONFIG_FILES" ]; then
  echo "Files list $CONFIG_FILES doesn't exist" 2>&1
  usage
  exit 1
fi

dev_create()
{
  DEVNAME="$ROOTDIR/dev/$1"
  shift
  if ! [ -e "$DEVNAME" ]; then
    /bin/mknod -m 0664 "$DEVNAME" $@
    /bin/chgrp named "$DEVNAME"
    if [ -x /usr/sbin/selinuxenabled -a -x /sbin/restorecon ]; then
      /usr/sbin/selinuxenabled && /sbin/restorecon "$DEVNAME" > /dev/null || :
    fi
  fi
}

dev_chroot_prep()
{
  dev_create random  c 1 8
  dev_create urandom c 1 9
  dev_create zero    c 1 5
  dev_create null    c 1 3
}

files_comment_filter()
{
  if [ -d "$1" ]; then
    grep -v '^[[:space:]]*#' "$1"/*.files
  else
    grep -v '^[[:space:]]*#' "$1"
  fi
}

mount_chroot_conf()
{
  if [ -n "$ROOTDIR" ]; then
    # Check devices are prepared
    dev_chroot_prep
    files_comment_filter "$CONFIG_FILES" | while read -r all; do
      # Skip nonexistant files
      [ -e "$all" ] || continue

      # If mount source is a file
      if ! [ -d "$all" ]; then
        # mount it only if it is not present in chroot or it is empty
        if ! [ -e "$ROOTDIR$all" ] || [ `stat -c'%s' "$ROOTDIR$all"` -eq 0 ]; then
          touch "$ROOTDIR$all"
          mount --bind "$all" "$ROOTDIR$all"
        fi
      else
        # Mount source is a directory. Mount it only if directory in chroot is
        # empty.
        if [ -e "$all" ] && [ `ls -1A $ROOTDIR$all | wc -l` -eq 0 ]; then
          mount --bind --make-private "$all" "$ROOTDIR$all"
        fi
      fi
    done
  fi
}

umount_chroot_conf()
{
  if [ -n "$ROOTDIR" ]; then
    files_comment_filter "$CONFIG_FILES" | while read -r all; do
      # Check if file is mount target. Do not use /proc/mounts because detecting
      # of modified mounted files can fail.
      if mount | grep -q '.* on '"$ROOTDIR$all"' .*'; then
        umount "$ROOTDIR$all"
        # Remove temporary created files
        [ -f "$all" ] && rm -f "$ROOTDIR$all"
      fi
    done
  fi
}

case "$2" in
  on)
    mount_chroot_conf
    ;;
  off)
    umount_chroot_conf
    ;;
  *)
    echo 'Second argument has to be "on" or "off"'
    usage
    exit 1
esac

exit 0
