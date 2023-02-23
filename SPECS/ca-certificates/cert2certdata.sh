#!/bin/bash
# Script converts a list of CRT/DER/PEM files into a certdata.txt file.
# On Ubuntu requires the package 'libnss3-tools'.

set -e

if [[ $# -eq 0 ]]; then
    echo "Usage: $0 <space-separated list of CRT/DER/PEM files>" >&2
    exit 1
fi

temp_dir=$(mktemp -d)
function cleanup {
    echo "Cleaning up temp directory '$temp_dir'."
    rm -rf "$temp_dir"
}
trap cleanup EXIT

for cert_file in "$@"
do
    if ! openssl x509 -in "$cert_file" -text -noout &>/dev/null
    then
        echo "File '$cert_file' is not a valid certificate." >&2
        exit 1
    fi

    # The 'nss-addbuiltin' tool requires certificates in the DER format.
    openssl x509 -in "$cert_file" -outform DER -out "$temp_dir/cert.der"
    cert_file="$temp_dir/cert.der"

    cert_label="$(openssl x509 -noout -subject -in "$cert_file" | grep -oP "(?<=CN = ).*")"

    # We always want to set "CKA_TRUST_SERVER_AUTH" to "CKT_NSS_TRUSTED_DELEGATOR".
    server_auth_flag="C"

    email_protection_flag="C"
    if ! openssl x509 -in "$cert_file" -purpose -text -noout | grep -q "Any Purpose CA : Yes"
    then
        email_protection_flag=""
    fi

    # We always want to set "CKA_TRUST_CODE_SIGNING" to "CKT_NSS_MUST_VERIFY_TRUST".
    code_signing_flag=""

    nss-addbuiltin -n "$cert_label" -t "$server_auth_flag,$email_protection_flag,$code_signing_flag" -i "$cert_file" >> "$temp_dir/certdata.txt"
done

mv "$temp_dir/certdata.txt" certdata.txt
