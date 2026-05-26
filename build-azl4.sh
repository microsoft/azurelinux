#!/usr/bin/env bash
#
# build-azl4.sh — Build an Azure Linux 4 image end-to-end from this repo.
#
# Wraps the `azldev` workflow:
#   1. Ensure `azldev` is installed at the version pinned by `.azldev-version`.
#   2. Render specs (`azldev component render -a`).
#   3. Build the local RPMs required by the target image into ./base/out.
#   4. Build the image via `azldev image build` against the local repo.
#
# Run from the repository root.
#
# Usage:
#   ./build-azl4.sh [options]
#
# Options:
#   -i, --image <name>     Image to build (default: vm-base-dev).
#                          See `base/images/images.toml` for available names
#                          (e.g. vm-base-dev, vm-iso-installer-dev,
#                          container-base-dev, container-base, wsl-dev).
#   -c, --clean            Remove ./base/build and ./base/out before building.
#       --no-render        Skip `azldev component render -a` (use checked-in
#                          specs as-is).
#       --no-install-azldev
#                          Don't try to `go install` azldev; fail if the
#                          pinned version isn't already on PATH.
#       --remote-repo <url>
#                          Additional remote DNF repo to pull RPMs from
#                          during the image build (e.g. an internal Koji
#                          repo). Disables gpgcheck on that repo.
#       --skip-components  Don't pre-build the bootstrap RPM components;
#                          assume ./base/out already has what's needed.
#   -h, --help             Show this help.
#

set -euo pipefail

# ---------------------------------------------------------------------------
# Defaults
# ---------------------------------------------------------------------------

IMAGE="vm-base-dev"
CLEAN=0
DO_RENDER=1
INSTALL_AZLDEV=1
SKIP_COMPONENTS=0
REMOTE_REPO=""

# Components required to bootstrap a local repo capable of producing an image.
# Mirrors the ordered list from `scripts/demo-build.sh`.
BOOTSTRAP_COMPONENTS=(
    azurelinux-rpm-config
    azurelinux-release
    azurelinux-repos
    rpm
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

log()  { printf '[build-azl4] %s\n' "$*" >&2; }
die()  { printf '[build-azl4] ERROR: %s\n' "$*" >&2; exit 1; }

usage() {
    sed -n '2,/^set -euo pipefail$/p' "$0" | sed -n 's/^# \{0,1\}//p' | sed '$d'
}

# ---------------------------------------------------------------------------
# Argument parsing
# ---------------------------------------------------------------------------

while [[ $# -gt 0 ]]; do
    case "$1" in
        -i|--image)            IMAGE="${2:?--image requires a value}"; shift 2 ;;
        -c|--clean)            CLEAN=1; shift ;;
        --no-render)           DO_RENDER=0; shift ;;
        --no-install-azldev)   INSTALL_AZLDEV=0; shift ;;
        --skip-components)     SKIP_COMPONENTS=1; shift ;;
        --remote-repo)         REMOTE_REPO="${2:?--remote-repo requires a value}"; shift 2 ;;
        -h|--help)             usage; exit 0 ;;
        *)                     die "Unknown argument: $1 (try --help)" ;;
    esac
done

# ---------------------------------------------------------------------------
# Sanity checks
# ---------------------------------------------------------------------------

[[ -f azldev.toml ]] || die "Must be run from the repo root (azldev.toml not found)."
[[ -f .azldev-version ]] || die "Missing .azldev-version file."

AZLDEV_VERSION="$(cat .azldev-version)"
[[ -n "$AZLDEV_VERSION" ]] || die ".azldev-version is empty."

for prereq in kiwi createrepo_c; do
    command -v "$prereq" >/dev/null 2>&1 \
        || die "Missing prerequisite '$prereq' on PATH (required for image builds)."
done

# ---------------------------------------------------------------------------
# Ensure azldev is installed at the pinned version
# ---------------------------------------------------------------------------

ensure_azldev() {
    if command -v azldev >/dev/null 2>&1; then
        local current
        current="$(azldev version 2>/dev/null | awk '/^version:/ {print $2; exit}' || true)"
        if [[ -n "$current" && "$current" == "$AZLDEV_VERSION" ]]; then
            log "azldev $AZLDEV_VERSION already installed."
            return 0
        fi
        log "azldev on PATH (version='$current') does not match pinned '$AZLDEV_VERSION'."
    else
        log "azldev not found on PATH."
    fi

    if [[ "$INSTALL_AZLDEV" -eq 0 ]]; then
        die "Refusing to install azldev (--no-install-azldev). Install $AZLDEV_VERSION manually."
    fi

    command -v go >/dev/null 2>&1 \
        || die "Go toolchain required to install azldev (or pass --no-install-azldev)."

    log "Installing azldev@$AZLDEV_VERSION via 'go install'..."
    GOBIN="${GOBIN:-${GOPATH:-$HOME/go}/bin}" \
        go install "github.com/microsoft/azure-linux-dev-tools/cmd/azldev@${AZLDEV_VERSION}"

    case ":$PATH:" in
        *":$GOBIN:"*) : ;;
        *) export PATH="$GOBIN:$PATH" ;;
    esac

    command -v azldev >/dev/null 2>&1 \
        || die "azldev still not on PATH after install (check \$GOBIN=$GOBIN)."
}

ensure_azldev

# ---------------------------------------------------------------------------
# Validate requested image exists
# ---------------------------------------------------------------------------

if ! grep -qE "^\[images\.${IMAGE}\]" base/images/images.toml; then
    log "Image '$IMAGE' not found in base/images/images.toml. Available images:"
    grep -oE '^\[images\.[a-z0-9._-]+\]' base/images/images.toml \
        | sed 's/^\[images\./  - /; s/\]$//' >&2
    exit 1
fi

# ---------------------------------------------------------------------------
# Build steps
# ---------------------------------------------------------------------------

if [[ "$CLEAN" -eq 1 ]]; then
    log "Cleaning ./base/build and ./base/out..."
    sudo rm -rf ./base/build ./base/out
fi

if [[ "$DO_RENDER" -eq 1 ]]; then
    log "Rendering specs (azldev component render -a)..."
    azldev component render -a
else
    log "Skipping spec rendering (--no-render)."
fi

if [[ "$SKIP_COMPONENTS" -eq 0 ]]; then
    log "Building bootstrap components into ./base/out: ${BOOTSTRAP_COMPONENTS[*]}"
    azldev comp build --local-repo-with-publish ./base/out "${BOOTSTRAP_COMPONENTS[@]}"
else
    log "Skipping component build (--skip-components)."
fi

log "Building image '$IMAGE'..."
image_args=(image build "$IMAGE" --local-repo ./base/out)
if [[ -n "$REMOTE_REPO" ]]; then
    image_args+=(--remote-repo "$REMOTE_REPO" --remote-repo-no-gpgcheck)
fi
azldev "${image_args[@]}"

OUT_DIR="./base/out/images/${IMAGE}"
log "Done. Artifacts in: $OUT_DIR"
if [[ -d "$OUT_DIR" ]]; then
    find "$OUT_DIR" -maxdepth 2 -type f -printf '  %p\n' >&2 || true
fi
