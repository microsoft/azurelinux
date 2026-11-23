#!/bin/bash
# Build actiontext-8.0.5.2-js.tar.gz the way the Fedora spec describes (git archive of the
# upstream v8.0.5.2 tag); the gem does not ship these files.
set -euo pipefail
git clone --quiet --depth 1 --branch v8.0.5.2 --filter=blob:none --no-checkout https://github.com/rails/rails.git /tmp/src
git -C /tmp/src sparse-checkout set --no-cone /actiontext/app/javascript /actiontext/rollup.config.js
git -C /tmp/src checkout --quiet
cd /tmp/src/actiontext
cp -a --parents app/javascript rollup.config.js /azldev-gen/output/
