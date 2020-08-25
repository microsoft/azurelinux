#!/bin/bash

set -e

if [ ! -f $1 ]
then
    echo "Input argument '$1' is not a file."
    error 1
fi

PREFIX="temp_cert"

pushd $(dirname $1)

# Splitting bundle into separate files with following content each:
#
# # [Certificate's Common Name]
# -----BEGIN CERTIFICATE-----
# [Base64 certificate data]
# -----END CERTIFICATE-----
csplit --elide-empty-files --prefix "$PREFIX" --suffix "%d.pem" $1 '/^#/' '{*}'

for pem_file in $PREFIX*
do
    echo "Working on $pem_file"

    HASH=$(openssl x509 -noout -hash -inform PEM -in $pem_file)
    PEM_FILE_NAME=$HASH.pem

    mv $pem_file $PEM_FILE_NAME
    ln -s $PEM_FILE_NAME $HASH.0
done

popd