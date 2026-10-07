#!/bin/bash

set -euo pipefail

case ",${kiwi_profiles:-}," in
    *,1p-vm-base-gen2-cvm,*)
        exec /image/config-cvm.sh
        ;;
    *,distroless-minimal,*|*,distroless-base,*|*,distroless-debug,*)
        exec /image/config-container-base.sh
        ;;
esac
