#!/bin/bash

set -euo pipefail

# Create service users and groups required by installed packages.
/usr/bin/systemd-sysusers

# Compile package-provided hardware information into /etc/udev/hwdb.bin.
/usr/bin/systemd-hwdb update

# Compile package-provided journal message descriptions into the catalog database.
/usr/bin/journalctl --update-catalog

# Rebuild /etc/ld.so.cache from shared libraries in the final image.
/usr/sbin/ldconfig

# Record that /etc and /var are current with the final /usr state.
# Keep this last so markers are written only after all generators succeed.
/usr/lib/systemd/systemd-update-done
