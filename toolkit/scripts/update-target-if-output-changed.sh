#!/bin/bash
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

# $1 path to flag file that will be created if needed.
# $2 path to the old output file.
# $3 path to the new output file.
flagFile=${1}
oldOutputFile=${2}
newOutputFile=${3}

usage() {
	echo
	echo "./update-target-if-output-changed.sh <flag-file> <old-output-file> <new-output-file>"
	echo
	echo "This is a helper script to create/update make flag files if the contents of an output file has changed."
	echo
    exit 1
}

[[ -z "$flagFile" || -z "$oldOutputFile" || -z "$newOutputFile" ]] && usage

if [[ ! -f $flagFile ]] || [[ ! -f $oldOutputFile ]]; then
	echo "Creating $flagFile"
	touch $flagFile
	exit 0
fi

cmp --silent $oldOutputFile $newOutputFile
comparisonResult=$?

if [[ $comparisonResult != 0 ]]; then
	echo "Creating $flagFile"
	touch $flagFile
fi
rm $oldOutputFile
