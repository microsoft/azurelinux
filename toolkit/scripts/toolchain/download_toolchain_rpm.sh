#!/bin/bash
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

set -e

# Create a temporary work directory for RPM signature validation
work_dir=$(mktemp -d)
function cleanup() {
    rm -rf "$work_dir"
}
trap cleanup EXIT

# Usage print
function usage() {
    echo "Usage: $0 --downloader-tool <downloader_tool> --rpm-name <rpm_name> --dst <dst_file> --log-base <log_base>" \
    "--url-list <url_list> [--certificate <cert>] [--private-key <key>] [--enforce-signatures] [--allowable-gpg-keys <allowable_gpg_keys>]"

    echo "-t|--downloader-tool: Path to our go downloader tool"
    echo "-r|--rpm-name: Name of the RPM to download"
    echo "-d|--dst: Destination file path"
    echo "-l|--log-base: Base path for log files. Each attempt will have a log file named <log_base>.<attempt_num>"
    echo "--hydrate: Print alternate log message for hydrate operations"
    echo "-h|--help: Print this help message"
    echo "-u|--url-list: Space separated list of base URLs to attempt to download the RPM from. The URLs will be tried in order"
    echo "           until the RPM is successfully downloaded. Full URL will be <url>/<rpm_name>"
    echo "-c|--certificate: Optional path to a certificate file to use for the download"
    echo "-k|--private-key: Optional path to a private key file to use for the download"
    echo "-e|--enforce-signatures: Optional flag to enforce RPM signatures"
    echo "-g|--allowable-gpg-keys: Optional space separated list of GPG keys to allow for signature validation"
}

# Default values
downloader_tool=""
rpm_name=""
dst_file=""
log_file=""
hydrate=false
url_list=""
cert=""
key=""
enforce_signatures=false
allowable_gpg_keys=""

while (( "$#")); do
    case "$1" in
        -t|--downloader-tool)
            downloader_tool=$2
            shift 2
            ;;
        -r|--rpm-name)
            rpm_name=$2
            shift 2
            ;;
        -d|--dst)
            dst_file=$2
            shift 2
            ;;
        -l|--log-base)
            log_file=$2
            shift 2
            ;;
        --hydrate)
            hydrate=true
            shift
            ;;
        -u|--url-list)
            url_list=$2
            shift 2
            ;;
        -c|--certificate)
            cert=$2
            shift 2
            ;;
        -k|--private-key)
            key=$2
            shift 2
            ;;
        -e|--enforce-signatures)
            enforce_signatures=true
            shift
            ;;
        -g|--allowable-gpg-keys)
            allowable_gpg_keys=$2
            shift 2
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        *)
            echo "Unknown argument: $1"
            usage
            exit 1
            ;;
    esac
done

if [ -z "$downloader_tool" ]; then
    usage
    exit 1
fi

if [ -z "$rpm_name" ]; then
    usage
    exit 1
fi

if [ -z "$dst_file" ]; then
    usage
    exit 1
fi

if [ -z "$log_file" ]; then
    usage
    exit 1
fi

if [ -z "$url_list" ]; then
    usage
    exit 1
fi

if [ -n "$cert" ]; then
    cert="--certificate=$cert"
fi

if [ -n "$key" ]; then
    key="--private-key=$key"
fi

if $enforce_signatures; then
    if [ -z "$allowable_gpg_keys" ]; then
        echo "Must provide allowable GPG keys when enforcing signatures"
        usage
        exit 1
    fi
    for key in $allowable_gpg_keys; do
        if [ ! -f "$key" ]; then
            echo "GPG key file does not exist: $key"
            exit 1
        fi
    done
fi

function download() {
    # Ensure the destination directory exists
    dst_dir=$(dirname "$dst_file")
    mkdir -p "$dst_dir"

    if $hydrate; then
        echo Attempting to download toolchain RPM:  $rpm_name | tee "$log_file"
    else
        echo "Downloading toolchain RPM: $rpm_name" | tee "$log_file"
    fi

    log_num=0
    for url in $url_list; do
        log_num=$((log_num + 1))
        attempt_log_file="$log_file.$log_num"
        src_url="$url/$rpm_name"

        echo "$src_url -> $attempt_log_file" >> "$log_file"
        { $downloader_tool $cert $key --no-clobber --output-file="$dst_file" --log-file="$attempt_log_file" "$src_url" 1>/dev/null 2>&1 ; res=$? ; } || true

        if [ $res = 0 ]; then
            echo "Downloaded toolchain RPM: $rpm_name" >> "$attempt_log_file"

            echo "SUCCESS" >> "$log_file"
            touch "$dst_file"
            return
        else
            echo "Failed to download toolchain RPM: $rpm_name" >> "$attempt_log_file"
            echo "FAILURE" >> "$log_file"
        fi
    done

    exit 1
}

function validate_signatures() {
    echo "Validating toolchain RPM: $rpm_name" | tee -a "$log_file"

    for key in $allowable_gpg_keys; do
        echo "Adding key ($key) to empty workdir at ($work_dir)" >> "$log_file"
        rpmkeys --root "$work_dir" --import "$key" >> "$log_file"
    done

    if ! rpmkeys --root "$work_dir" --checksig --verbose "$dst_file" -D "%_pkgverify_level signature" >> "$log_file"; then
        echo "Failed to validate toolchain package $rpm_name signature, aborting." | tee -a "$log_file"
        exit 1
    fi
}

mkdir -p "$(dirname "$log_file")"

download

if $enforce_signatures; then
    validate_signatures
fi
