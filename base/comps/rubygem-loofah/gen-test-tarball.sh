#!/bin/bash
# Build loofah-2.25.3-test.tar.gz the way the Fedora spec describes (git archive of the
# upstream v2.25.3 tag); the gem does not ship these files.
set -euo pipefail
git clone --quiet --depth 1 --branch v2.25.3 --filter=blob:none --no-checkout https://github.com/flavorjones/loofah.git /tmp/src
git -C /tmp/src sparse-checkout set --no-cone /test
git -C /tmp/src checkout --quiet
cd /tmp/src
cp -a --parents test /azldev-gen/output/
