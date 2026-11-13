#!/bin/bash
# Build concurrent-ruby-1.3.7-specs.tar.gz the way the Fedora spec describes: the spec/ directory of the
# upstream v1.3.7 tag (the gem does not ship the test suite).
set -euo pipefail
git clone --quiet --depth 1 --branch v1.3.7 https://github.com/ruby-concurrency/concurrent-ruby.git /tmp/src
cp -a /tmp/src/spec /azldev-gen/output/
