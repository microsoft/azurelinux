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
    # These single-purpose workload images declare runtime-package-management
    # = true and intentionally keep dnf5 + bash for runtime package
    # management, so the destructive keep-list strip must not run. Still
    # prune build-time-only byproducts (docs, locale data, dnf5 logs) that
    # are never needed at runtime regardless of package manager presence.
    *,nginx-workload,*|*,postgres-workload,*)
        exec /image/config-container-base.sh --mode=light
        ;;
esac
