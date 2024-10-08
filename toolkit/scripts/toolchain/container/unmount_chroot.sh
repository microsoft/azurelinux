#!/bin/bash
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

if [[ -z "$LFS" ]]; then
    echo "Must define LFS in environment" 1>&2
    exit 1
fi
echo LFS root is: $LFS

umount -v $LFS/dev/pts || umount -lv $LFS/dev/pts
umount -v $LFS/dev || umount -lv $LFS/dev
umount -v $LFS/run || umount -lv $LFS/run
umount -v $LFS/proc || umount -lv $LFS/proc
umount -v $LFS/sys || umount -lv $LFS/sys
rm -v $LFS/dev/console
rm -v $LFS/dev/null
