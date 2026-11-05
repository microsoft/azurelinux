#!/bin/bash

set -euo pipefail

case ",${kiwi_profiles:-}," in
    *,core,*|*,distroless-minimal,*) ;;
    *) exit 0 ;;
esac

# KIWI's host-side DNF5 bootstrap does not read the target's RPM macros.
# Reinstall bootstrap packages in the chroot so RPM records
# excluded files as not installed, using the packaged bootstrap language policy.
dnf5 --config /kiwi_dnf5.config --assumeyes reinstall '*'
