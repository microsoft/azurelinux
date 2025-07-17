#!/bin/sh

echo "Running mountbootpartition.sh"

type getarg > /dev/null 2>&1 || . /lib/dracut-lib.sh

bootPartitionUuid=$(getarg pre.verity.mount)

if [[ -n "$bootPartitionUuid"  ]]; then
    mkdir -p /boot
    mount -U $bootPartitionUuid /boot
fi

echo "done" > /run/boot-parition-mount-complete.sem
