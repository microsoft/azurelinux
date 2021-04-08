#!/bin/bash
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

# $1 path to expand RPM macros into
# $2 is the directory of RPMs to consume for macros
# $3 is the file that contains a list of rpm names to search for
dir=${1}
rpmdir=${2}
manifest=${3}

usage() {
    echo "./preparemacros.sh <macro directory> <input rpm directory> <macro rpm manifest>"
    echo "    Expand the rpms specified in the rpm manifest into the macro directory"
    exit 1
}

[[ -z "$1" || -z "$2" || -z "$3" ]] && usage
[ ! -f $3 ] && echo "Invalid rpm manifest $3" && usage
[ ! -d $2 ] && echo "Input rpm directory $2 does not exist" && usage

mkdir -p ${dir}
cd ${dir}

echo "Expanding rpms into MACRO_DIR ${dir}"
while read p || [ -n "$p" ]; do
    # Regex find for rpms with the correct package name
    # Reverse sort the list so the highest version/revision is the top result
    exact=`find ${rpmdir} -regextype sed -regex ".*/$p-[^-]*-[^-]*.rpm" | sort -r | head -1`

    if test -z "$exact"
    then
        echo "ERROR: No macro package match found for $p in ${rpmdir}"
        exit 1
    fi

    echo "Extracting $exact"
    rpm2cpio $exact | cpio -idm 2>/dev/null
done < $3

echo "Copying correct version of rpmpopt from host into macrodir"
cp /usr/lib/rpm/rpmpopt* ${dir}/usr/lib/rpm/

echo "Finished expanding rpms into MACRO_DIR ${dir}"

exit 0