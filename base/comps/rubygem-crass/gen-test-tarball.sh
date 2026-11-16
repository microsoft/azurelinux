#!/bin/bash
# Build crass-1.0.8-tests.tar.gz: the test/ directory of the upstream v1.0.8 tag
# (the gem does not ship the test suite since 1.0.5).
set -euo pipefail
git clone --quiet --depth 1 --branch v1.0.8 https://github.com/rgrove/crass.git /tmp/src
cp -a /tmp/src/test /azldev-gen/output/
