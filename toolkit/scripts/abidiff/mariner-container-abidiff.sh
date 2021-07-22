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
        #TODO P4: Add logfile as an option
        >>/dev/null dnf provides -Cq "$sofile"
        [[ $? -eq 0 ]] || echo "$rpmpackage" > "$abidiff_out"/"failed_${sofile}"
    done
done
