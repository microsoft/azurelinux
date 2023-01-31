#!/usr/bin/env bash

#set -x

#set -euf

echo "Creating ekcert for $1 => $3"
echo "Creating ekcert for $2 => $4"

ROOTCRT=$6.crt
ROOTCRTPEM=$6.pem
INTERMEDCRT=$5.crt
ROOTCRL=$6.crl
INTERMEDCRL=$5.crl

OS=$(uname)
DATE_FMT_BEFORE=""
DATE_FMT_AFTER=""
SED_CMD=""

if [ "$OS" == "Linux" ]; then
    DATE_FMT_BEFORE="+%y%m%d000000Z -u -d -1day"
    DATE_FMT_AFTER="+%y%m%d000000Z -u -d +10years+1day"
    SED_CMD="sed -i"
elif [ "$OS" == "FreeBSD" ]; then
    DATE_FMT_BEFORE="-u -v-1d +%y%m%d000000Z"
    DATE_FMT_AFTER="-u -v+10y +%y%m%d000000Z"
    SED_CMD="sed -i '' -e"
fi

EKCADIR="$(dirname $(realpath ${0}))/"

CA_DIR="$(mktemp -d ekca-XXXXXX)"

pushd "$CA_DIR"

mkdir root-ca
pushd root-ca

mkdir certreqs certs crl newcerts private
touch root-ca.index
echo 00 > root-ca.crlnum
echo 1000 > root-ca.serial
echo "123456" > pass.txt

cp "${EKCADIR}/root-ca.cnf" ./
export OPENSSL_CONF=./root-ca.cnf
ROOT_URL="file:$ROOTCRT"
${SED_CMD} "s|ROOTCRT|$ROOT_URL|g" $OPENSSL_CONF
ROOT_URL="file:$ROOTCRL"
${SED_CMD} "s|ROOTCRL|$ROOT_URL|g" $OPENSSL_CONF
openssl req -new -out root-ca.req.pem -passout file:pass.txt

#
# Create self signed root certificate
#

openssl ca -selfsign \
    -in root-ca.req.pem \
    -out root-ca.cert.pem \
    -extensions root-ca_ext \
    -startdate `date ${DATE_FMT_BEFORE}` \
    -enddate `date ${DATE_FMT_AFTER}` \
    -passin file:pass.txt -batch

openssl x509 -outform der -in  root-ca.cert.pem -out root-ca.cert.crt

openssl verify -verbose -CAfile root-ca.cert.pem \
        root-ca.cert.pem

openssl ca -gencrl  -cert root-ca.cert.pem \
        -out root-ca.cert.crl.pem -passin file:pass.txt
openssl crl -in root-ca.cert.crl.pem -outform DER -out root-ca.cert.crl

popd #root-ca

#
# Create intermediate certificate
#
mkdir intermed-ca
pushd intermed-ca

mkdir certreqs certs crl newcerts private
touch intermed-ca.index
echo 00 > intermed-ca.crlnum
echo 2000 > intermed-ca.serial
echo "abcdef" > pass.txt

cp "${EKCADIR}/intermed-ca.cnf" ./
export OPENSSL_CONF=./intermed-ca.cnf

# Adapt CRT URL to current test directory
${SED_CMD} "s|ROOTCRT|$ROOT_URL|g" $OPENSSL_CONF

openssl req -new -out intermed-ca.req.pem -passout file:pass.txt

openssl rsa -inform PEM -in private/intermed-ca.key.pem \
        -outform DER -out private/intermed-ca.key.der -passin file:pass.txt

cp intermed-ca.req.pem  \
   ../root-ca/certreqs/

INTERMED_URL="file:$INTERMEDCRT"
${SED_CMD} "s|INTERMEDCRT|$INTERMED_URL|g" $OPENSSL_CONF

pushd ../root-ca
export OPENSSL_CONF=./root-ca.cnf

openssl ca \
    -in certreqs/intermed-ca.req.pem \
    -out certs/intermed-ca.cert.pem \
    -extensions intermed-ca_ext \
    -startdate `date ${DATE_FMT_BEFORE}` \
    -enddate `date ${DATE_FMT_AFTER}` \
    -passin file:pass.txt -batch

openssl x509 -outform der -in certs/intermed-ca.cert.pem \
        -out certs/intermed-ca.cert.crt

openssl verify -verbose -CAfile root-ca.cert.pem \
        certs/intermed-ca.cert.pem

cp certs/intermed-ca.cert.pem \
   ../intermed-ca

cp certs/intermed-ca.cert.crt \
   ../intermed-ca

popd #root-ca

export OPENSSL_CONF=./intermed-ca.cnf
openssl ca -gencrl  -cert ../root-ca/certs/intermed-ca.cert.pem \
        -out intermed-ca.crl.pem -passin file:pass.txt
openssl crl -in intermed-ca.crl.pem -outform DER -out intermed-ca.crl

popd #intermed-ca

#
# Create RSA EK certificate
#
mkdir ek
pushd ek

cp "${EKCADIR}/ek.cnf" ./
export OPENSSL_CONF=ek.cnf
echo "abc123" > pass.txt

# Adapt CRT and CRL URL to current test directory

INTERMED_URL="file:$INTERMEDCRT"
${SED_CMD} "s|INTERMEDCRT|$INTERMED_URL|g" $OPENSSL_CONF

INTERMED_URL="file:$INTERMEDCRL"
${SED_CMD} "s|INTERMEDCRL|$INTERMED_URL|g" $OPENSSL_CONF

cp "$1" ../intermed-ca/certreqs/ek.pub.pem

openssl req -new -nodes -newkey rsa:2048 -passin file:pass.txt -out ../intermed-ca/certreqs/nonsense.csr.pem

pushd ../intermed-ca
export OPENSSL_CONF=./intermed-ca.cnf

openssl x509 -req -in certreqs/nonsense.csr.pem -force_pubkey certreqs/ek.pub.pem -out certs/ek.cert.der \
    -outform DER -extfile ../ek/ek.cnf -extensions ek_ext -set_serial 12345 \
    -CA intermed-ca.cert.pem -CAkey private/intermed-ca.key.pem -passin file:pass.txt

cp certs/ek.cert.der ../ek

popd #intermed-ca

popd #EK

#
# Create ECC EK Certificate
#
mkdir ekecc
pushd ekecc

cp "${EKCADIR}/ek.cnf" ./
export OPENSSL_CONF=ek.cnf
echo "abc123" > pass.txt

# Adapt CRT and CRL URL to current test directory

INTERMED_URL="file:$INTERMEDCRT"
${SED_CMD} "s|INTERMEDCRT|$INTERMED_URL|g" $OPENSSL_CONF

INTERMED_URL="file:$INTERMEDCRL"
${SED_CMD} "s|INTERMEDCRL|$INTERMED_URL|g" $OPENSSL_CONF

cp "$2" ../intermed-ca/certreqs/ekecc.pub.pem

openssl req -new -nodes -newkey rsa:2048 -passin file:pass.txt -out ../intermed-ca/certreqs/nonsense.csr.pem

pushd ../intermed-ca
export OPENSSL_CONF=./intermed-ca.cnf

openssl x509 -req -in certreqs/nonsense.csr.pem -force_pubkey certreqs/ekecc.pub.pem -out certs/ekecc.cert.der \
    -outform DER -extfile ../ek/ek.cnf -extensions ek_ext -set_serial 12345 \
    -CA intermed-ca.cert.pem -CAkey private/intermed-ca.key.pem -passin file:pass.txt

cp certs/ekecc.cert.der ../ekecc

popd #intermed-ca

popd #EK

popd #CA_DIR

# Copy used CRL and CRT files to test directory.

cp "${CA_DIR}/ek/ek.cert.der" "$3"
cp "${CA_DIR}/ekecc/ekecc.cert.der" "$4"
cp "${CA_DIR}/intermed-ca/intermed-ca.cert.crt" "$INTERMEDCRT"
cp "${CA_DIR}/intermed-ca/intermed-ca.crl" "$INTERMEDCRL"
cp "${CA_DIR}/root-ca/root-ca.cert.crt" "$ROOTCRT"
cp "${CA_DIR}/root-ca/root-ca.cert.crl" "$ROOTCRL"
cp "${CA_DIR}/root-ca/root-ca.cert.pem" "$ROOTCRTPEM"

rm -rf $CA_DIR
