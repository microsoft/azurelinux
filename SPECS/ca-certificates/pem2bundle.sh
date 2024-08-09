#!/bin/bash
# Begin pem2bundle.sh
# Script extracted from Fedora 29 ca-certificates.spec
# The file certdata.txt must exist in the local directory
# Modifications by Paul Monson <paulmon@microsoft.com>

set -x
echo Parameters passed: $@

CERTDIR="$1"
P11_FORMAT_BUNDLE="$2"
TRUST_FIXES="$3"

pushd $CERTDIR
 (
   cat <<EOF
# This is a bundle of X.509 certificates of Microsoft-trusted Certificate
# Authorities. It was generated from a list of root CAs.
# These certificates and trust/distrust attributes use the file format accepted
# by the p11-kit-trust module.
EOF
 ) > $P11_FORMAT_BUNDLE

 P11FILES=$(find certs -name \*.tmp-p11-kit | wc -l)
 if [ $P11FILES -ne 0 ]; then
   for p in certs/*.tmp-p11-kit; do 
     cat "$p" >> $P11_FORMAT_BUNDLE
   done
 fi
 # Append our trust fixes
 cat $TRUST_FIXES >> $P11_FORMAT_BUNDLE
popd
