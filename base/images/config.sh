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
    # Single-purpose workload images keep their declared application runtime
    # and Bash, but remove DNF/RPM/repository state and unrelated bootstrap
    # packages. PostgreSQL also needs writable runtime/data directories before
    # the final image switches to the postgres user.
    *,postgres-workload,*)
        install -d -m 0700 -o postgres -g postgres /var/lib/pgsql/data
        install -d -m 3775 -o postgres -g postgres /var/lib/pgsql/run
        exec /image/config-container-base.sh --mode=runtime
        ;;
    *,nginx-workload,*|*,telegraf-workload,*|*,python-workload,*|*,nodejs-workload,*|*,pytorch-workload,*)
        exec /image/config-container-base.sh --mode=runtime
        ;;
esac
