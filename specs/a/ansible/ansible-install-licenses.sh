#!/usr/bin/bash -x

# SPDX-License-Identifier: MIT
# Copyright (C) Fedora Project Authors
# License Text: https://spdx.org/licenses/MIT.txt

set -euo pipefail

ansible_licensedir="${1}"
ansible_docdir="${2}"

# Install docs and licenses
mkdir -p "${ansible_licensedir}" "${ansible_docdir}"

# This finds the license file for each collection and moves it to
# `${ansible_licensedir}`

for f in $(find -mindepth 3 -iname 'LICENSES' -type d -printf '%P\n')
do
    dirname="$(dirname "${ansible_licensedir}/${f}")"
    mkdir -p "${dirname}"
    mv "${f}" "${ansible_licensedir}/${f}"
done

for f in $(
    find . -mindepth 3 -type f \
        \( -iname '*LICENSE*' -o -iname '*COPYING*' \) \
        -not -name '*.py' -not -name '*.pyc' \
        -not -name '*.license' -not -name '*.yaml' -not -name '*.yml' \
        -not -name '*.json' \
        -printf '%P\n' \
    | grep -vE '/docs/[^/]+_module\.rst$'
)
do
    dirname="$(dirname "${ansible_licensedir}/${f}")"
    mkdir -p "${dirname}"
    mv "${f}" "${dirname}"
done

# This does the same thing, but for READMEs.
for f in $(find . -mindepth 3 -type f -name 'README*' -printf '%P\n')
do
    dirname="$(dirname "${ansible_docdir}/${f}")"
    mkdir -p "${dirname}"
    mv "${f}" "${dirname}"
done
