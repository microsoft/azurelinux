#!/bin/bash
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

set -e

SPECS_DIR="$(git rev-parse --show-toplevel)/SPECS"
SCRIPT_FOLDER="$(realpath "$(dirname "${BASH_SOURCE[0]}")")"

echo "Updating livepatch specs."

"$SCRIPT_FOLDER"/generate_livepatch_spec.sh

for livepatch_spec in "$SPECS_DIR"/livepatch-*/*.spec
do
    "$SCRIPT_FOLDER"/generate_livepatch-signed_spec.sh "$livepatch_spec"
done
