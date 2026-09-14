#!/bin/bash

set -euo pipefail

case ",${kiwi_profiles:-}," in
    *,cvm-poc,*)
        exec /image/config-cvm.sh
        ;;
    *,distroless-minimal,*|*,distroless-base,*|*,distroless-debug,*)
        exec /image/config-container-base.sh
        ;;
esac
