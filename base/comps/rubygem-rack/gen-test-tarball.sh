#!/bin/bash
# Build rack-3.1.23-tests.tar.gz the way the Fedora spec describes: the test/ directory of the
# upstream v3.1.23 tag (the gem does not ship the test suite).
set -euo pipefail
git clone --quiet --depth 1 --branch v3.1.23 https://github.com/rack/rack.git /tmp/src
cp -a /tmp/src/test /azldev-gen/output/
