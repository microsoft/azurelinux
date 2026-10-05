#!/bin/sh
# SPDX-License-Identifier: GPL-2.0-only OR Linux-OpenIB
# Fetches the upstream mstflint release tarball and repacks it with the
# non-free, prebuilt libdpa_elf blobs removed, so that those blobs never
# end up in our source RPM (not even transiently, as %prep would allow).
#
# The result is named after the upstream tarball with a ".free" suffix
# inserted before the extension, to make clear it is not the pristine
# upstream artifact. It is meant to be uploaded to the lookaside cache
# as Source0:
#
#   ./generate-tarball.sh
#   fedpkg new-sources mstflint-4.37.0-1.1.free.tar.gz

set -eu

scriptdir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
spec="$scriptdir/mstflint.spec"

mainver=$(sed -n 's/^%global mainver[[:space:]]\+//p' "$spec")
subver=$(sed -n 's/^%global subver[[:space:]]\+//p' "$spec")
if [ -z "$mainver" ] || [ -z "$subver" ]; then
	echo "Could not parse mainver/subver from $spec" >&2
	exit 1
fi

name=mstflint
tarball="${name}-${mainver}-${subver}.tar.gz"
out_tarball="${name}-${mainver}-${subver}.free.tar.gz"
url="https://github.com/Mellanox/${name}/releases/download/v${mainver}-${subver}/${tarball}"

workdir=$(mktemp -d)
trap 'rm -rf "$workdir"' EXIT

curl -fL -o "$workdir/$tarball" "$url"
tar -C "$workdir" -xzf "$workdir/$tarball"

# Non-free, prebuilt ELF blobs. mstflint builds and works fine without
# them; only the ability to embed a default DPA ELF via mstflint-format
# is lost, which we don't need.
find "$workdir/${name}-${mainver}" -path '*/mlxdpa/dpa_elf/*/libdpa_elf' -print -delete

tar -C "$workdir" \
	--sort=name --owner=0 --group=0 --numeric-owner --mtime='UTC 1970-01-01' \
	-czf "$out_tarball" "${name}-${mainver}"

echo "Wrote $(pwd)/$out_tarball"
