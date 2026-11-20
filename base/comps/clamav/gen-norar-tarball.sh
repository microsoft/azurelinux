#!/bin/bash
# Build clamav-1.4.7-norar.tar.xz the way Fedora's update_clamav.sh does: verify the signed
# upstream release and drop everything under libclamunrar/ (the unRAR licence is not allowed in
# Fedora), keeping the empty libclamunrar/ directory as `tar --delete '*/libclamunrar/*'` does.
set -euo pipefail

VERSION=1.4.7
TARBALL=clamav-${VERSION}.tar.gz
SHA512=779caaa789f8ef7bef92f9ea3dfcd246b5aa1db138d16a5fd712e3521ff5640a30684db9975fce2168b192ed3ca8baacceba00082393c8259e9a90820f3fe2d2
# Talos (Cisco) release signing key, the same key that signed 1.4.6.
FINGERPRINT=5BADCA2665EF59DCF8A23D8B707F0DB480836771

work=$(mktemp -d "${HOME:-/builddir}/clamav-norar.XXXXXX")
cd "$work"

fetch() {
    curl -sSfL --retry 3 -o "$1" "https://github.com/Cisco-Talos/clamav/releases/download/clamav-${VERSION}/$1" ||
        curl -sSfL --retry 3 -o "$1" "https://www.clamav.net/downloads/production/$1"
}
fetch "$TARBALL"
fetch "$TARBALL.sig"

echo "$SHA512  $TARBALL" | sha512sum -c -

export GNUPGHOME="$work/gnupg"
mkdir -m 700 "$GNUPGHOME"
gpg --batch --quiet --import <<'KEY'
-----BEGIN PGP PUBLIC KEY BLOCK-----

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
=BW1T
-----END PGP PUBLIC KEY BLOCK-----
KEY
status=$(gpg --batch --status-fd 1 --verify "$TARBALL.sig" "$TARBALL" 2>/dev/null || true)
grep -Eq "^\[GNUPG:\] VALIDSIG .* ${FINGERPRINT}\$" <<<"$status" ||
    { echo "clamav-${VERSION}: no valid signature from ${FINGERPRINT}" >&2; exit 1; }

tar -xzf "$TARBALL"
find "clamav-${VERSION}/libclamunrar" -mindepth 1 -delete
cp -a "clamav-${VERSION}" /azldev-gen/output/
