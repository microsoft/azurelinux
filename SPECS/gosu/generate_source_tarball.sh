#!/bin/bash
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

set -euo pipefail

script_directory=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
source_tarball=""
package_version=""
output_directory="$script_directory"

while (( $# )); do
    case "$1" in
        --srcTarball)
            source_tarball="${2:?--srcTarball requires a value}"
            shift 2
            ;;
        --pkgVersion)
            package_version="${2:?--pkgVersion requires a value}"
            shift 2
            ;;
        --outFolder)
            output_directory="${2:?--outFolder requires a value}"
            shift 2
            ;;
        *)
            printf 'Unsupported argument: %s\n' "$1" >&2
            exit 2
            ;;
    esac
done

if [[ -z "$source_tarball" || -z "$package_version" ]]; then
    printf 'Usage: %s --srcTarball FILE --pkgVersion VERSION [--outFolder DIR]\n' "$0" >&2
    exit 2
fi

source_tarball=$(realpath -e -- "$source_tarball")
output_directory=$(realpath -e -- "$output_directory")
if [[ ! -f "$source_tarball" || ! -d "$output_directory" ]]; then
    printf 'Source must be a regular file and output folder must be an existing directory.\n' >&2
    exit 2
fi
if [[ "$(basename -- "$source_tarball")" != "gosu-${package_version}.tar.gz" ]]; then
    printf 'Expected source filename gosu-%s.tar.gz\n' "$package_version" >&2
    exit 2
fi

generated_tarball="$output_directory/gosu-${package_version}-${package_version}-govendor-v1.tar.gz"
vendor_tarball="$output_directory/gosu-${package_version}-vendor.tar.gz"
if [[ -e "$generated_tarball" || -e "$vendor_tarball" ]]; then
    printf 'Refusing to overwrite an existing gosu vendor archive in %s\n' "$output_directory" >&2
    exit 1
fi

(
    # The shared helper checks the source basename in the current directory.
    cd -- "$(dirname -- "$source_tarball")"
    GOTOOLCHAIN=local GOWORK=off bash "$script_directory/../../toolkit/scripts/build_go_vendor_cache.sh" \
        --srcTarball "$source_tarball" \
        --outFolder "$output_directory" \
        --pkgVersion "$package_version" \
        --vendorVersion 1
)

mv -- "$generated_tarball" "$vendor_tarball"
sha256sum "$vendor_tarball"
