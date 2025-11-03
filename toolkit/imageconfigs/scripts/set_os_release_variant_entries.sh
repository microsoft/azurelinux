#!/bin/bash
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

set -euo pipefail

DEFAULT_OS_RELEASE_FILE="/etc/os-release"

FLAG_VARIANT_ID=""
FLAG_VARIANT=""
FLAG_OS_RELEASE_FILE="$DEFAULT_OS_RELEASE_FILE"

exit_help() {
    local error_message=""
    if [[ $# -gt 0 ]]; then
        error_message="$1"
    fi

    echo "Usage: $0 [flags]"
    echo ""
    echo "This script sets the VARIANT and VARIANT_ID entries in the os-release file."
    echo ""
    echo "See https://www.freedesktop.org/software/systemd/man/latest/os-release.html for more information and the"
    echo "latest details on these entries."
    echo ""
    echo "Flags:"
    echo "  -h, --help"
    echo "    Show this help message and exit."
    echo ""
    echo "  -i VARIANT_ID, --variant-id VARIANT_ID"
    echo "    Value of VARIANT_ID to set in the os-release file. It must be a lower-case string (no spaces or other"
    echo "    characters outside of 0-9, a-z, '.', '_' and '-')."
    echo ""
    echo "  -n VARIANT, --variant VARIANT"
    echo "    Value of VARIANT to set in the os-release file. It will be enclosed in double quotes if it contains"
    echo "    anything outside of A-Z, a-z, 0-9."
    echo ""
    echo "  -o OS_RELEASE, --os-release OS_RELEASE  Path to the os-release file (default: '$DEFAULT_OS_RELEASE_FILE')"

    if [[ -n "$error_message" ]]; then
        echo ""
        echo "Error: $error_message"
    fi

    exit 1
}

parse_flags() {
    while [[ $# -gt 0 ]]; do
        local flag="$1"
        shift
        case "$flag" in
            -h|--help) exit_help;;
            -i|--variant-id) FLAG_VARIANT_ID="$1"; shift;;
            -n|--variant) FLAG_VARIANT="$1"; shift;;
            -o|--os-release) FLAG_OS_RELEASE_FILE="$1"; shift;;
            -*) echo "Error: Unknown flag: $flag" >&2; exit_help;;
            *) echo "Error: Unknown argument: $flag" >&2; exit_help;;
        esac
    done

    if [[ -z "$FLAG_VARIANT_ID" ]]; then
        exit_help "--variant-id is required"
    fi

    if [[ "$FLAG_VARIANT_ID" =~ [^a-z0-9._-] ]]; then
        exit_help "Value of VARIANT_ID must be a lower-case string (no spaces or other characters outside of 0-9, a-z, '.', '_' and '-')."
    fi

    if [[ -z "$FLAG_VARIANT" ]]; then
        exit_help "--variant is required"
    fi

    if [[ "$FLAG_VARIANT" =~ \" ]]; then
        exit_help "Value of VARIANT cannot contain double quotes"
    fi

    # This script only double-quotes, even though systemd also specifies that values may be single-quoted.
    if [[ "$FLAG_VARIANT" =~ [^A-Za-z0-9] ]]; then
        FLAG_VARIANT="\"$FLAG_VARIANT\""
    fi

    if [[ ! -e "$FLAG_OS_RELEASE_FILE" ]]; then
        exit_help "OS release file '$FLAG_OS_RELEASE_FILE' does not exist"
    fi
}

set_os_release_entry() {
    local key="$1"
    local value="$2"

    if grep -q "^$key=" $FLAG_OS_RELEASE_FILE; then
        sed -i "s/^$key=.*/$key=$value/" $FLAG_OS_RELEASE_FILE
    else
        echo "$key=$value" >> $FLAG_OS_RELEASE_FILE
    fi
}

main() {
    parse_flags "$@"

    set_os_release_entry "VARIANT_ID" "$FLAG_VARIANT_ID"
    set_os_release_entry "VARIANT" "$FLAG_VARIANT"
}

main "$@"
