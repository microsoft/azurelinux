#!/bin/bash
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

# $1 path to recursively scan for mount points which must be cleaned up
dir=${1}

# If dir does not exist, exit
if [ ! -d "${dir}" ] ; then exit 0 ; fi

for dir in $(find ${dir} -type d | sort) ; do
    if [[ -d $dir ]]; then
        if  mountpoint -q ${dir} ; then
            echo "WARNING: Removing mountpoint at $dir"
            umount -l ${dir}
            sleep 0.5
        fi
        retries=10
        while mountpoint -q ${dir} ; do
            echo "ERROR: Mountpoint still present at $dir, retrying unmount ${retries} times"
            umount -l ${dir}
            retries=$(( ${retries} - 1))
            sleep 1
            if [ ${retries} -eq 0 ] ; then exit 1 ; fi
        done
    fi
done
exit 0