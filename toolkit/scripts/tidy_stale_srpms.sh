#!/bin/bash
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

set -x
set -e

# Params:
#   --specs="..."       List of .spec file paths that we should consider
#   --list-files="..."  List of text files each containing a list of SRPMs to keep

# Parse params

for i in "$@"
do
case $i in
    --specs=*)
    SPECS="${i#*=}"
    shift # past argument=value
    ;;
    --list-files=*)
    KEEP_LISTS="${i#*=}"
    shift # past argument=value
    ;;
    *)
          # unknown option
    ;;
esac
done

for list in $KEEP_LISTS; do
    if [ -f "${list}" ]; then
        for srpm in $(cat ${list}); do
            echo "Keeping ${srpm}"
        done
    fi
done