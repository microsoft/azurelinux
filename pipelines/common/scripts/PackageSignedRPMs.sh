#!/bin/bash

set -e

ROOT_DIR="$(git rev-parse --show-toplevel)"

# shellcheck source=../common/libs/build_tools.sh
source "$ROOT_DIR/pipelines/common/libs/build_tools.sh"

compress_rpms() {
    local artifacts_dir
    local compressed_dir
    local compressed_dir_lowercase
    local output_dir

    artifacts_dir="$1"
    output_dir="$2"

    mkdir -p "$output_dir"

    for compressed_dir in RPMS SRPMS
    do
        if [[ -d "$artifacts_dir/$compressed_dir" ]]
        then
            compressed_dir_lowercase="${compressed_dir,,}"

            echo "-- Compressing the '$compressed_dir' directory into ($output_dir)."
            tar -C "$artifacts_dir" -cf "$output_dir/$compressed_dir_lowercase.tar.gz" "$compressed_dir"
        fi
    done
}

validate_rpm_signatures() {
    local artifacts_dir
    local key_id
    local rpm_name
    local rpm_path
    local signatures_ok

    artifacts_dir="$1"
    key_id="$2"

    signatures_ok=true

    echo "-- Validating RPM signatures with key ID ($key_id)."

    while IFS= read -r -d '' rpm_path
    do
        rpm_name="$(basename "$rpm_path")"

        echo "-- Validating signature key for ($rpm_name)."

        verification_output="$(rpm -v --checksig "$rpm_path" 2>&1)"
        if ! grep -q "key ID $key_id: OK" <<< "$verification_output"
        then
            echo -e "ERROR: RPM signature key validation failed for ($rpm_name). Details:\n$verification_output" >&2
            signatures_ok=false
        fi
    done < <(find "$artifacts_dir" -name "*.rpm")

    $signatures_ok
}

# Script parameters:
#
# -a -> input artifacts directory path
# -k -> signing key ID to verify the RPMs' signatures
# -o -> output directory
while getopts "a:k:o:" OPTIONS
do
  case "${OPTIONS}" in
    a ) ARTIFACTS_DIR=$OPTARG ;;
    k ) EXPECTED_KEY_ID=$OPTARG ;;
    o ) OUTPUT_DIR=$OPTARG ;;

    \? )
        echo "ERROR: Invalid Option: -$OPTARG" 1>&2
        exit 1
        ;;
    : )
        echo "ERROR: Invalid Option: -$OPTARG requires an argument" 1>&2
        exit 1
        ;;
  esac
done

if [[ ! -d "$ARTIFACTS_DIR/RPMS" && ! -d "$ARTIFACTS_DIR/SRPMS" ]]
then
    echo "ERROR: input directory ($ARTIFACTS_DIR) must contain at least the 'RPMS' or 'SRPMS' subdirectory." >&2
    exit 1
fi

print_variables_with_check ARTIFACTS_DIR EXPECTED_KEY_ID OUTPUT_DIR

validate_rpm_signatures "$ARTIFACTS_DIR" "$EXPECTED_KEY_ID"

compress_rpms "$ARTIFACTS_DIR" "$OUTPUT_DIR"
