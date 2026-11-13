#!/bin/bash
# Build activemodel-8.0.5.2-tests.tar.gz the way the Fedora spec describes (git archive of the
# upstream v8.0.5.2 tag); the gem does not ship these files.
set -euo pipefail
git clone --quiet --depth 1 --branch v8.0.5.2 --filter=blob:none --no-checkout https://github.com/rails/rails.git /tmp/src
git -C /tmp/src sparse-checkout set --no-cone /activemodel/test
git -C /tmp/src checkout --quiet
cd /tmp/src/activemodel
cp -a --parents test /azldev-gen/output/
