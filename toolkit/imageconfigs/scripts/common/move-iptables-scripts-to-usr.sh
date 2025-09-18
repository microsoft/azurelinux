#!/bin/bash

set -euxo pipefail

# Move iptables scripts to /usr/libexec/iptables, as /etc will be locked down by
# IPE and also is mounted with noexec.

START_SOURCE="/etc/systemd/scripts/iptables"
STOP_SOURCE="/etc/systemd/scripts/iptables.stop"

START_TARGET="/usr/libexec/iptables/iptables"
STOP_TARGET="/usr/libexec/iptables/iptables.stop"

mkdir -p /usr/libexec/iptables

mv "$START_SOURCE" "$START_TARGET"
mv "$STOP_SOURCE" "$STOP_TARGET"

# Create symlinks for compatibility
ln -s "$START_TARGET" "$START_SOURCE"
ln -s "$STOP_TARGET" "$STOP_SOURCE"
