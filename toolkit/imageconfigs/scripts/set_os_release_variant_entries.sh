#!/bin/bash
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

set -euo pipefail

DEFAULT_OS_RELEASE_FILE="/etc/os-release"

FLAG_ID=""
FLAG_NAME=""
FLAG_OS_RELEASE_FILE="$DEFAULT_OS_RELEASE_FILE"

print_help() {
    echo "Usage: $0 [flags]"
    echo ""
    echo "Flags:"
    echo "  -h, --help                              Show this help message and exit"
    echo "  -i ID, --id ID                          Value of VARIANT_ID to set in the os-release file"
    echo "  -n NAME, --name NAME                    Value of VARIANT to set in the os-release file"
    echo "  -o OS_RELEASE, --os-release OS_RELEASE  Path to the os-release file (default: '$DEFAULT_OS_RELEASE_FILE')"
}

parse_flags() {
    while [[ $# -gt 0 ]]; do
        local flag="$1"
        shift
        case "$flag" in
            -h|--help) print_help; exit 2;;
            -i|--id) FLAG_ID="$1"; shift;;
            -n|--name) FLAG_NAME="$1"; shift;;
            -o|--os-release) FLAG_OS_RELEASE_FILE="$1"; shift;;
            -*) echo "Error: Unknown flag: $flag" >&2; print_help; exit 1;;
            *) echo "Error: Unknown argument: $flag" >&2; print_help; exit 1;;
        esac
    done

    if [[ -z "$FLAG_ID" ]]; then
        echo "Error: Variant ID is required." >&2
        print_help
        exit 1
    fi

    if [[ -z "$FLAG_NAME" ]]; then
        echo "Error: Variant name is required." >&2
        print_help
        exit 1
    fi

    if [[ ! -e "$FLAG_OS_RELEASE_FILE" ]]; then
        echo "Error: OS release file '$FLAG_OS_RELEASE_FILE' does not exist." >&2
        exit 1
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

    set_os_release_entry "VARIANT_ID" "$FLAG_ID"
    set_os_release_entry "VARIANT" "$FLAG_NAME"
}

main "$@"
