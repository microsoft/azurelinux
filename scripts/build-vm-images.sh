#!/bin/bash
set -euxo pipefail

# Find the absolute path of the directory containing this script
SCRIPTS_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
. "$SCRIPTS_DIR/common.sh"

sudo rm -rf "$REPO_ROOT/base/build/work/vm-base/*"
sudo rm -rf "$REPO_ROOT/base/out/images/*"

# Build vm-base image using azldev
azldev image build vm-base --local-repo "$REPO_ROOT/base/out" --remote-repo "$REMOTE_KOJI_REPO_URL" --remote-repo-no-gpgcheck
