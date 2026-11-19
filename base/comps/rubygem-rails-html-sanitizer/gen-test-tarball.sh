#!/bin/bash
# Build rails-html-sanitizer-1.7.2-tests.tar.gz the way the Fedora spec describes (git archive of the
# upstream v1.7.2 tag); the gem does not ship these files.
set -euo pipefail
git clone --quiet --depth 1 --branch v1.7.2 --filter=blob:none --no-checkout https://github.com/rails/rails-html-sanitizer.git /tmp/src
git -C /tmp/src sparse-checkout set --no-cone /test
git -C /tmp/src checkout --quiet
cd /tmp/src
cp -a --parents test /azldev-gen/output/
