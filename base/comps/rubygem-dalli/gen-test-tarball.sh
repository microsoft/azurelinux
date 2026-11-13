#!/bin/bash
# Build dalli-3.2.3-tests.txz the way the Fedora spec describes: the test/ directory of the
# upstream v3.2.3 tag (the gem does not ship the test suite).
set -euo pipefail
git clone --quiet --depth 1 --branch v3.2.3 https://github.com/petergoldstein/dalli.git /tmp/src
cp -a /tmp/src/test /azldev-gen/output/
