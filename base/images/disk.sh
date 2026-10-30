#!/bin/bash

set -euo pipefail

case ",${kiwi_profiles:-}," in
    *,BootableCore,*)
        # KIWI initially creates a generic initrd. Rebuild on the mounted image
        # so host-only discovery uses the image's root filesystem and fstab.
        dracut --force --regenerate-all --hostonly --no-hostonly-cmdline --fstab
        ;;
esac
