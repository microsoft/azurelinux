#!/bin/bash
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

# Usage: safeunmount.sh <dir1> <dir2> ...
# e.g.
#   `safeunmount.sh /mnt/resource /mnt/scratch` will attempt to unmount all mount points under /mnt/resource and /mnt/scratch in parallel
#   `safeunmount.sh "/mnt/"*` will use bash expansion to unmount all mount points under /mnt/ in parallel

function clean_dir {
    dir=${1}
    for dir in $(find "${dir}" -type d | sort) ; do
        if [[ -d $dir ]]; then
            if  mountpoint -q "${dir}" ; then
                echo "WARNING: Removing mountpoint at '$dir'"
                umount -l "${dir}"
                sleep 0.5
            fi
            retries=10
            while mountpoint -q "${dir}" ; do
                echo "ERROR: Mountpoint still present at '$dir', retrying unmount ${retries} times"
                umount -l "${dir}"
                retries=$(( "${retries}" - 1))
                sleep 1
                if [ ${retries} -eq 0 ] ; then echo "ERROR: Unable to unmount '$dir'"; return 1 ; fi
            done
        fi
    done || ( echo "ERROR: failed to unmount directories under '$dir'" ; return 1)

    return 0
}

# For each argument, pass it to clean_dir in parallel then wait for all to finish and return the exit code
pids=()
for dir in "$@" ; do
    if [[ ! -d $dir ]]; then
        echo "Warning: $dir is not a directory, skipping safe unmount"
    else
        echo "Cleaning $dir" 
        (clean_dir "${dir}") & pids+=( $! )
    fi
done

for pid in "${pids[@]}" ; do
    wait "${pid}" || (echo "ERROR: Failed to unmount a directory" ; exit 1)
done

exit 0