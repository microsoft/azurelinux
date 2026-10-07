#!/bin/bash

set -euo pipefail

case ",${kiwi_profiles:-}," in
    *,1p-vm-base-gen2-cvm,*)
        # KIWI's systemd_boot cannot install shim or use Azure Linux's packaged kernel-uki-virt layout.
        exec /image/config-cvm.sh
        ;;
    *,distroless-minimal,*|*,distroless-base,*|*,distroless-debug,*)
        exec /image/config-container-base.sh
        ;;
esac
