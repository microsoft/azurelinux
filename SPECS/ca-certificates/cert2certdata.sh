#!/bin/bash
# Script converts a list of CRT/DER/PEM files into a certdata.txt file.
# On Ubuntu requires the package 'libnss3-tools'.

set -e

if [[ $# -lt 2 ]]; then
    echo "Usage: $0 <CA certificate in DER/PEM format> <trust flags in the format accepted by the '-t' argument for 'nss-addbuiltin'>" >&2
    echo "See here for more details: https://access.redhat.com/documentation/en-us/red_hat_directory_server/12/html/securing_red_hat_directory_server/assembly_changing-the-ca-trust-flagssecuring-rhds" >&2
    exit 1
fi

input_path="$1"
trust_flags="$2"

temp_dir=$(mktemp -d)
function cleanup {
    echo "Cleaning up temp directory '$temp_dir'."
    rm -rf "$temp_dir"
}
trap cleanup EXIT

function convert_cert {
    local file_path="$1"

    if ! openssl x509 -in "$file_path" -text -noout &>/dev/null; then
        echo "File '$file_path' is not a valid certificate." >&2
        exit 1
    fi

    echo "Converting certificate '$file_path'."

    # The 'nss-addbuiltin' tool requires certificates in the DER format.
    openssl x509 -in "$file_path" -outform DER -out "$temp_dir/cert.der"
    file_path="$temp_dir/cert.der"

    cert_label="$(openssl x509 -noout -subject -in "$file_path" | grep -oP "(?<=CN = ).*")"

    nss-addbuiltin -n "$cert_label" -t "$trust_flags" -i "$file_path" >>"$temp_dir/certdata.txt"
}

if [[ -d "$input_path" ]]; then
    # Convert only CRT/DER/PEM files.
    while read -r -d '' file; do
        convert_cert "$file"
    done < <(find "$input_path" -type f -regextype posix-extended -regex '.*\.(crt|der|pem)$' -print0)
else
    convert_cert "$input_path"
fi

mv "$temp_dir/certdata.txt" certdata.txt

echo "Done. Output in 'certdata.txt'."
