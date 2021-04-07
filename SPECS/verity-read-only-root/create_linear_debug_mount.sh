#!/bin/bash
# Portions Copyright (c) 2020 Microsoft Corporation

# Tool which attempts to mount the dm-verity overlays into an accessible
# location.

set -e

VERITY_NAME=$(cd /dev/mapper/ && ls verity-*)
SIZE=$(blockdev --getsz /dev/mapper/$VERITY_NAME)

# Get the device verity is pulling data from
DATA_DEV=$(dmsetup table $VERITY_NAME | cut -d " " -f 5)

# Freeze verity
echo "Root FS from /dev/mapper/$VERITY_NAME is being suspended"
dmsetup suspend $VERITY_NAME

# Create a writable mapping
dmsetup create $VERITY_NAME-RW --table "0 $SIZE linear $DATA_DEV 0"

# Mount it
mount /dev/mapper/$VERITY_NAME-RW /mnt/verity_writable_debug
echo "Writable root is now avialable at /mnt/verity_writable_debug"
echo "WARNING: /dev/mapper/$VERITY_NAME is still frozen, system may hang unexpectedly until it is resumed"
echo "    run 'dmsetup resume $VERITY_NAME' to unfreeze"