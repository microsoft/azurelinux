#!/bin/bash
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

# $1 path to recursively scan for mount points which must be cleaned up
dir=${1}
for dir in $(find ${dir} -type d) ; do
    retries=10
    while mountpoint -q ${dir} ; do
        echo "ERROR: Mountpoint still present at $dir, retrying unmount ${retries} times"
        umount -l ${dir}
        retries=$(( ${retries} - 1))
        sleep 1
        if [ ${retries} -eq 0 ] ; then exit 1 ; fi
    done
done
exit 0