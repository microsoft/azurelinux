#!/bin/bash

set -euo pipefail

case ",${kiwi_profiles:-}," in
    *,BootableCore,*)
        # KIWI initially creates a generic initrd for the image's kernel.
        # Rebuild in host-only mode against the mounted image and its fstab
        # to reduce initrd size.
        dracut --force --regenerate-all --hostonly --no-hostonly-cmdline --fstab
        ;;
esac
