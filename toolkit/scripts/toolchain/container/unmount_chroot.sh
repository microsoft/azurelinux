#!/bin/bash
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

if [[ -z "$LFS" ]]; then
    echo "Must define LFS in environment" 1>&2
    exit 1
fi
echo LFS root is: $LFS

umount -v $LFS/dev/pts
umount -v $LFS/dev/shm || true
umount -v $LFS/run
umount -v $LFS/proc
umount -v $LFS/sys
umount -v $LFS/dev || exit 1  # so we don't clobber the real /dev
rm -v $LFS/dev/console
rm -v $LFS/dev/null
