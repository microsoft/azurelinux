#!/bin/bash
# Begin pem2bundle.sh
# Script extracted from Fedora 29 ca-certificates.spec
# The file certdata.txt must exist in the local directory
# Modifications by Paul Monson <paulmon@microsoft.com>

set -x
echo Parameters passed: $@

CERTDIR="$1"
NSSCKBI_H="$2"
P11_FORMAT_BUNDLE="$3"
LEGACY_DEFAULT_BUNDLE="$4"
LEGACY_DISABLE_BUNDLE="$5"
TRUST_FIXES="$6"

pushd $CERTDIR
 (
   cat <<EOF
# This is a bundle of X.509 certificates of public Certificate
# Authorities.  It was generated from a list of root CAs.
# These certificates and trust/distrust attributes use the file format accepted
# by the p11-kit-trust module.
#
# Source: nss/lib/ckfw/builtins/certdata.txt
# Source: nss/lib/ckfw/builtins/nssckbi.h
#
# Generated from:
EOF
   cat $NSSCKBI_H  |grep -w NSS_BUILTINS_LIBRARY_VERSION | awk '{print "# " $2 " " $3}';
   echo '#';
 ) > $P11_FORMAT_BUNDLE
 
  touch $LEGACY_DEFAULT_BUNDLE
 NUM_LEGACY_DEFAULT=`find certs/legacy-default -type f | wc -l`
 if [ $NUM_LEGACY_DEFAULT -ne 0 ]; then
     for f in certs/legacy-default/*.crt; do 
       echo "processing $f"
       tbits=`sed -n '/^# openssl-trust/{s/^.*=//;p;}' $f`
       alias=`sed -n '/^# alias=/{s/^.*=//;p;q;}' $f | sed "s/'//g" | sed 's/"//g'`
       targs=""
       if [ -n "$tbits" ]; then
          for t in $tbits; do
             targs="${targs} -addtrust $t"
          done
       fi
       if [ -n "$targs" ]; then
          echo "legacy default flags $targs for $f" >> info.trust
          openssl x509 -text -in "$f" -trustout $targs -setalias "$alias" >> $LEGACY_DEFAULT_BUNDLE
       fi
     done
 fi

 touch $LEGACY_DISABLE_BUNDLE
 NUM_LEGACY_DISABLE=`find certs/legacy-disable -type f | wc -l`
 if [ $NUM_LEGACY_DISABLE -ne 0 ]; then
     for f in certs/legacy-disable/*.crt; do 
       echo "processing $f"
       tbits=`sed -n '/^# openssl-trust/{s/^.*=//;p;}' $f`
       alias=`sed -n '/^# alias=/{s/^.*=//;p;q;}' $f | sed "s/'//g" | sed 's/"//g'`
       targs=""
       if [ -n "$tbits" ]; then
          for t in $tbits; do
             targs="${targs} -addtrust $t"
          done
       fi
       if [ -n "$targs" ]; then
          echo "legacy disable flags $targs for $f" >> info.trust
          openssl x509 -text -in "$f" -trustout $targs -setalias "$alias" >> $LEGACY_DISABLE_BUNDLE
       fi
     done
 fi

 P11FILES=`find certs -name \*.tmp-p11-kit | wc -l`
 if [ $P11FILES -ne 0 ]; then
   for p in certs/*.tmp-p11-kit; do 
     cat "$p" >> $P11_FORMAT_BUNDLE
   done
 fi
 # Append our trust fixes
 cat $TRUST_FIXES >> $P11_FORMAT_BUNDLE
popd
