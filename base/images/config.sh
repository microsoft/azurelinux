#!/bin/bash

set -euo pipefail

case ",${kiwi_profiles:-}," in
    *,distroless-minimal,*|*,distroless-base,*|*,distroless-debug,*)
        exec /image/config-container-base.sh
        ;;
esac
