#!/bin/bash

set -euo pipefail

case ",${kiwi_profiles:-}," in
    # distroless-* and busybox-workload declare runtime-package-management =
    # false: no package manager (or shell) is meant to survive into the
    # shipped image, so run the full keep-list-driven strip (removes
    # bash/dnf5/rpm down to just the profile's declared packages).
    *,distroless-minimal,*|*,distroless-base,*|*,distroless-debug,*|*,busybox-workload,*)
        exec /image/config-container-base.sh --mode=strip
        ;;
esac
