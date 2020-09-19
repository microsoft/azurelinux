#!/bin/bash

# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

set -e

INPUT_CERTDATA="certdata.microsoft.txt"
CA_CERTIFICATES_DIR="SPECS/ca-certificates"
CA_CERTIFICATES_SPEC="$CA_CERTIFICATES_DIR/ca-certificates.spec"
CA_CERTIFICATES_SIGNATURES="$CA_CERTIFICATES_DIR/ca-certificates.signatures.json"
CHANGE_DESCRIPTION="Updating Microsoft trusted root CAs."
MICROSOFT_CERTDATA_PATH="$CA_CERTIFICATES_DIR/certdata.microsoft.txt"
VERSION=$(grep -oP '(?<=Version:)\s+(.*)' $CA_CERTIFICATES_SPEC | tr -d '[:space:]')
CURRENT_RELEASE=$(grep -oP '(?<=Release:)\s+(\d+)' $CA_CERTIFICATES_SPEC | tr -d '[:space:]')
NEXT_RELEASE=$((CURRENT_RELEASE+1))

function update_signatures {
    local NEW_SIGNATURE=$(sha256sum "$MICROSOFT_CERTDATA_PATH" | cut -d ' ' -f1)

    sed -i -E "s/certdata.microsoft.txt[^,]*/certdata.microsoft.txt\": \"$NEW_SIGNATURE\"/" "$CA_CERTIFICATES_SIGNATURES"
}

function update_spec {
    local CHANGELOG_HEADER=`date "+%a %b %d %Y Pawel Winogrodzki <pawelwi@microsoft.com> - $VERSION-$NEXT_RELEASE"`

    sed -i -E "s/(Release:\s+)[0-9]+/\1$NEXT_RELEASE/" "$CA_CERTIFICATES_SPEC"
    sed -i "/%changelog.*/a * $CHANGELOG_HEADER\n- $CHANGE_DESCRIPTION\n" "$CA_CERTIFICATES_SPEC"
}

function update_manifests {
    find toolkit/resources/manifests/package -regextype posix-extended -regex ".*(pkggen_core|toolchain).*.txt" \
        -exec sed -i -E "s/(ca-certificates.*-$VERSION-)$CURRENT_RELEASE/\1$NEXT_RELEASE/" {} \;
}

function create_pull_request {
    local BRANCH_NAME="pawelwi/ca-certificates-microsoft_auto_update"

    git checkout -b "$BRANCH_NAME"
    git commit -am "$CHANGE_DESCRIPTION"
    git push -u origin "$BRANCH_NAME"

    hub pull-request -F pull_request_template.md -b dev -r microsoft/cbl-mariner-devs -d
}

function install_hub {
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
    /home/linuxbrew/.linuxbrew/bin/brew install hub
}

if [ ! -z "$1" ]; then
    INPUT_CERTDATA="$1"
fi

if [ ! -f "$INPUT_CERTDATA" ]; then
    echo "Cannot update certificates from \"$1\" - not a file."
    exit 1
fi

echo "Updating certificates from \"$INPUT_CERTDATA\""

cp "$INPUT_CERTDATA" "$MICROSOFT_CERTDATA_PATH"

update_signatures
update_spec
update_manifests
create_pull_request