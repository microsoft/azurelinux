#!/bin/bash
# config.sh — Kiwi config.sh hook for the Azure Linux WSL image.
#
# WSL owns networking, DNS resolution, the console/TTY, /tmp and early /dev
# setup on behalf of the distribution. systemd units that duplicate that
# management cause DNS/boot breakage, and console units (systemd-vconsole-setup,
# getty@tty1) fail when several distros try to claim the TTY in parallel. WSL's
# distribution validator rejects some of these (validate-modern.py:
# DISCOURAGED_SYSTEM_UNITS) and WSL maintainers flagged the rest. Mask them, per
# the WSL systemd recommendations:
#   https://learn.microsoft.com/windows/wsl/build-custom-distro#systemd-recommendations
#
# systemd-tmpfiles-setup.service is intentionally left enabled: wsl-setup relies
# on it to materialize the WSLg X11/Wayland/PulseAudio socket links, so masking
# it would break GUI application support.
set -euo pipefail

echo "config.sh: masking systemd units discouraged in WSL"

systemctl mask \
    systemd-networkd.service \
    systemd-networkd-wait-online.service \
    systemd-resolved.service \
    systemd-vconsole-setup.service \
    getty@tty1.service \
    tmp.mount \
    systemd-tmpfiles-setup-dev.service \
    systemd-tmpfiles-setup-dev-early.service
