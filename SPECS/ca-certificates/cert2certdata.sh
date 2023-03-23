#!/bin/bash
# Script converts a list of CRT/DER/PEM files into a certdata.txt file.
# On Ubuntu requires the package 'libnss3-tools'.

set -e

if [[ $# -lt 2 ]]; then
    echo "Usage: $0 <CA certificate in DER/PEM format> <trust flags in the format accepted by the '-t' argument for 'nss-addbuiltin'>" >&2
    exit 1
fi

cert_file="$1"
trust_flags="$2"

temp_dir=$(mktemp -d)
function cleanup {
    echo "Cleaning up temp directory '$temp_dir'."
    rm -rf "$temp_dir"
}
trap cleanup EXIT

if ! openssl x509 -in "$cert_file" -text -noout &>/dev/null
then
    echo "File '$cert_file' is not a valid certificate." >&2
    exit 1
fi

# The 'nss-addbuiltin' tool requires certificates in the DER format.
openssl x509 -in "$cert_file" -outform DER -out "$temp_dir/cert.der"
cert_file="$temp_dir/cert.der"

cert_label="$(openssl x509 -noout -subject -in "$cert_file" | grep -oP "(?<=CN = ).*")"

nss-addbuiltin -n "$cert_label" -t "$trust_flags" -i "$cert_file" >> "$temp_dir/certdata.txt"

mv "$temp_dir/certdata.txt" certdata.txt
