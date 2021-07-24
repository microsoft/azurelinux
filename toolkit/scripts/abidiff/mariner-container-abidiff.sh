#!/bin/bash

# This script assumes to be run on Mariner,
# as it leverages its .repo files

rpms_folder="$1"
abidiff_out="$rpms_folder"/abidiff

# Setup output dir
mkdir -p "$abidiff_out"

#TODO P2: Add option to pass your own repo

# Cache RPM metadata
dnf -y makecache

# Get packages from stdin
for rpmpackage in $(cat); do
    package_path=$(find "$rpms_folder" -name "$rpmpackage" -type f)
    package_provides=`rpm -qP "$package_path" | grep -E '[.]so[(.]'`

    for sofile in $package_provides; do
        # Query local metadata for provides
        >>/dev/null dnf provides -Cq "$sofile"

        if ! [[ $? -eq 0 ]] ; then
            # SO file not found, meaning this might be a new .SO
            # or a new version of a preexisting .SO.
            # Check if the previous version exists in the database.

            # Remove version part from .SO file
            sofile_no_ver=$(echo "$sofile" | sed -E 's/[.]so[(.].+/.so/')

            # check for generic .so in the repo
            >>/dev/null dnf provides -Cq "${sofile_no_ver}*"

            if ! [[ $? -eq 0 ]] ; then
                # Generic version of SO was found.
                # This means it's a new version of a preexisting SO.
                echo "$rpmpackage" > "$abidiff_out"/"failed_${sofile}"
            fi
        fi
    done
done
