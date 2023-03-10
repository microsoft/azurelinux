#!/bin/bash

set -e

ROOT_DIR="$(git rev-parse --show-toplevel)"

# shellcheck source=../common/libs/build_tools.sh
source "$ROOT_DIR/pipelines/common/libs/build_tools.sh"

compress_rpms() {
    local artifacts_dir
    local publish_dir

    artifacts_dir="$1"
    publish_dir="$2"

    mkdir -p "$publish_dir"

    if [[ -d "$artifacts_dir/RPMS" ]]
    then
        echo "-- Compressing RPMs into ($publish_dir)."
        tar -C "$artifacts_dir" -cf "$publish_dir/rpms.tar.gz" RPMS
    fi

    if [[ -d "$artifacts_dir/SRPMS" ]]
    then
        echo "-- Compressing SRPMs into ($publish_dir)."
        tar -C "$artifacts_dir" -cf "$publish_dir/srpms.tar.gz" SRPMS
    fi
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
# -s -> use toolkit's RPMs snapshot to populate the packages cache
while getopts "a:k:p:" OPTIONS
do
  case "${OPTIONS}" in
    a ) ARTIFACTS_DIR=$OPTARG ;;
    k ) EXPECTED_KEY_ID=$OPTARG ;;
    p ) PUBLISH_DIR=$OPTARG ;;

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

print_variables_with_check ARTIFACTS_DIR EXPECTED_KEY_ID PUBLISH_DIR

validate_rpm_signatures "$ARTIFACTS_DIR" "$EXPECTED_KEY_ID"

compress_rpms "$ARTIFACTS_DIR" "$PUBLISH_DIR"
