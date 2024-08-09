#!/bin/bash

# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

set -e

if [ ! -f $1 ]
then
    echo "Input argument '$1' is not a file."
    error 1
fi

TARGET_DIR="$( cd "$(dirname "$1")" > /dev/null 2>&1 ; pwd -P )"
BUNDLE_NAME="$(basename "$1")"

pushd "$(mktemp -d)" > /dev/null

echo "-----EXTRACTING SINGLE CERTS FROM BUNDLE-----"

# Splitting bundle into separate files with following content each:
#
# # [Certificate's Common Name]
# -----BEGIN CERTIFICATE-----
# [Base64 certificate data]
# -----END CERTIFICATE-----
csplit --quiet --elide-empty-files --prefix "" --suffix "%d.pem" "$TARGET_DIR/$BUNDLE_NAME" '/^#/' '{*}'

for pem_file in *.pem
do
    HASH=$(openssl x509 -noout -hash -inform PEM -in $pem_file)
    PEM_FILE_NAME=$HASH.pem

    if [ -f $PEM_FILE_NAME ]
    then
        echo "SKIPPING '$(head -n 1 $pem_file | tr -d '# ')' - the same as '$(head -n 1 $PEM_FILE_NAME | tr -d '# ')'"
    else
        mv $pem_file $PEM_FILE_NAME
        ln -s $PEM_FILE_NAME $HASH.0
    fi
done

echo "-----REMOVING PREVIOUS SINGLE CERTS-----"
rm -f "$TARGET_DIR"/*.{0,pem}

echo "-----INSTALLING EXTRACTED SINGLE CERTS-----"
mv *.{0,pem} "$TARGET_DIR"

popd > /dev/null
