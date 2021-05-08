#!/bin/bash
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

set -x

echo Adding certs to user-data
echo Parameters passed: $@

USER_DATA=$1
TLS_CERT=$2
TLS_KEY=$3
CA_CERT=$4
USER_DATA_TEMP=$USER_DATA.tmp
TLS_CERT_BASENAME=$(basename $TLS_CERT)
TLS_KEY_BASENAME=$(basename $TLS_KEY)
CA_CERT_BASENAME=$(basename $CA_CERT)

while IFS= read -r line || [ -n "$line" ]; do
    echo $line
    echo "$line" >> $USER_DATA_TEMP
    if  [ $line = "#cloud-config" ]; then
        echo 'write_files:' >> $USER_DATA_TEMP
        # TLS_CERT
        echo '- encoding: gzip' >> $USER_DATA_TEMP
        echo '  content: !!binary |' >> $USER_DATA_TEMP
        gzip -f < $TLS_CERT | base64 | sed 's/^/    /' >> $USER_DATA_TEMP
        echo "  path: /etc/tdnf/$TLS_CERT_BASENAME" >> $USER_DATA_TEMP
        echo "  permissions: '0644'" >> $USER_DATA_TEMP
        # TLS_KEY
        echo '- encoding: gzip' >> $USER_DATA_TEMP
        echo '  content: !!binary |' >> $USER_DATA_TEMP
        gzip -f < $TLS_KEY | base64 | sed 's/^/    /' >> $USER_DATA_TEMP
        echo "  path: /etc/tdnf/$TLS_KEY_BASENAME" >> $USER_DATA_TEMP
        echo "  permissions: '0644'" >> $USER_DATA_TEMP
        # CA_CERT
        echo '- encoding: gzip' >> $USER_DATA_TEMP
        echo '  content: !!binary |' >> $USER_DATA_TEMP
        gzip -f < $CA_CERT | base64 | sed 's/^/    /' >> $USER_DATA_TEMP
        echo "  path: /etc/tdnf/$CA_CERT_BASENAME" >> $USER_DATA_TEMP
        echo "  permissions: '0644'" >> $USER_DATA_TEMP

        echo "" >> $USER_DATA_TEMP
    fi
done < $USER_DATA

rm $USER_DATA
mv $USER_DATA_TEMP $USER_DATA
