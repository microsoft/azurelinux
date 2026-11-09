#!/bin/bash

set -euo pipefail

case ",${kiwi_profiles:-}," in
    *,marketplace-gen2,*)
        /usr/bin/systemd-sysusers
        /usr/bin/systemd-hwdb update
        /usr/bin/journalctl --update-catalog
        /usr/sbin/ldconfig
        /usr/lib/systemd/systemd-update-done
        ;;
esac
