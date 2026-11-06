#!/bin/bash

set -euo pipefail

case ",${kiwi_profiles:-}," in
    *,core,*) ;;
    *) exit 0 ;;
esac

# Host-side DNF5 bootstrap does not read KIWI's target-root RPM locale macro.
# Reinstall in the chroot so RPM filters bootstrap payloads and records the
# excluded files as not installed. KIWI removes its macro during final cleanup.
dnf5 --config /kiwi_dnf5.config --assumeyes reinstall '*'
