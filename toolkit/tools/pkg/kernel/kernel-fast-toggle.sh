#!/bin/bash
# Toggle fast-iteration kernel build settings.
#
# Usage:
#   ./base/comps/kernel/kernel-fast-toggle.sh on   # enable fast build
#   ./base/comps/kernel/kernel-fast-toggle.sh off   # restore default
#   ./base/comps/kernel/kernel-fast-toggle.sh       # show current state
#
# "on" replaces the without list with a minimal-subpackage set.
# "off" restores the upstream default (only skip debug variant).

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")" && git rev-parse --show-toplevel)"
COMP_TOML="$REPO_ROOT/base/comps/kernel/kernel.comp.toml"

FAST_WITHOUT='without = [
    "debug",         # skip debug kernel variant
    "debuginfo",     # skip debuginfo/debugsource RPMs
    "perf",          # skip perf subpackages
    "tools",         # skip kernel-tools subpackages
    "selftests",     # skip selftests
    "doc",           # skip kernel-doc
    "cross_headers", # skip cross-compiled headers
]'

DEFAULT_WITHOUT='without = ["debug"]'

# Marker comment injected/removed with the fast block
MARKER="# >>> kernel-fast-toggle: fast-iteration overrides <<<"

status() {
    if grep -qF "$MARKER" "$COMP_TOML" 2>/dev/null; then
        echo "fast-iteration: ON"
    else
        echo "fast-iteration: OFF (default)"
    fi
}

enable_fast() {
    if grep -qF "$MARKER" "$COMP_TOML"; then
        echo "Already enabled."
        status
        return
    fi
    # Replace the single-line without with the expanded block + marker
    # Use perl for reliable multi-line insertion
    perl -i -pe "s|^without = \[\"debug\"\]|${MARKER}\n${FAST_WITHOUT}|" "$COMP_TOML"
    echo "Enabled fast-iteration kernel build."
    status
}

disable_fast() {
    if ! grep -qF "$MARKER" "$COMP_TOML"; then
        echo "Already disabled."
        status
        return
    fi
    # Remove marker line and replace the multi-line without block with the default
    # First remove the marker
    sed -i "/${MARKER}/d" "$COMP_TOML"
    # Replace the multi-line without block with the single-line default
    # Use perl for multi-line replacement
    perl -i -0pe "s|without = \[\n.*?\]|${DEFAULT_WITHOUT}|s" "$COMP_TOML"
    echo "Restored default kernel build settings."
    status
}

case "${1:-}" in
    on)  enable_fast ;;
    off) disable_fast ;;
    *)   status ;;
esac
