#!/bin/bash

set -euo pipefail

case ",${kiwi_profiles:-}," in
    *,core,*|*,distroless-minimal,*) ;;
    *) exit 0 ;;
esac

# KIWI's host-side DNF5 bootstrap does not read the target's RPM macros.
# Reinstall its language-bearing packages in the chroot so RPM records
# excluded files as not installed, using the packaged bootstrap language policy.
language_packages=$(rpm -qa --qf '[%{FILELANGS} %{=NEVRA}\n]' |
    sed -n '/^[^ ]/s/^[^ ]* //p' | sort -u)
if [[ -n "${language_packages}" ]]; then
    mapfile -t packages <<< "${language_packages}"
    dnf5 --config /kiwi_dnf5.config --assumeyes reinstall "${packages[@]}"
fi
