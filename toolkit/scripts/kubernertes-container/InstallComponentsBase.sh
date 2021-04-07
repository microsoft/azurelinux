#!/bin/bash
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

set -e

# parse script parameters:
#
# -c -> component to install
# -r -> repo file
#
while getopts ":c:r:" OPTIONS; do
    case ${OPTIONS} in
    c ) COMPONENT=$OPTARG ;;
    r ) REPO_FILE=$OPTARG ;;

    \? )
        echo " ---> Error - Invalid Option: -$OPTARG" 1>&2
        exit 1
        ;;
    : )
        echo " ---> Error - Invalid Option: -$OPTARG requires an argument" 1>&2
        exit 1
        ;;
    esac
done

if [[ -f $REPO_FILE ]]; then
    cp $REPO_FILE /etc/yum.repos.d
else
    echo " ---> Error - no repo file"
fi

echo " ---> install $COMPONENT"
tdnf -y install $COMPONENT

FILE_NAME=$(basename $REPO_FILE)
rm /etc/yum.repos.d/$FILE_NAME
