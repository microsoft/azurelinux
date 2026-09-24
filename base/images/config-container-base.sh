#!/bin/bash
# config.sh — Kiwi config.sh hook for container image minimization
#
# Invoked by /image/config.sh (see that file for the profile -> mode
# routing table) with a single --mode argument selecting one of two
# cleanup strategies:
#
#   --mode=strip (distroless-*, busybox-workload; runtime-package-management
#   = false profiles): strips the image down to only the packages declared
#   in the kiwi XML (plus their transitive dependencies), producing a
#   minimal, package-manager-less, shell-less container. Strategy:
#     1. Parse the kiwi XML to collect declared image packages
#        (shared base + profile-specific).
#     2. Resolve virtual Provides to real package names
#        (e.g., system-release → azurelinux-release).
#     3. Force-remove disallowed packages (bash, ca-certificates) while
#        preserving generated certificate files via snapshot/restore.
#     4. Mark all installed packages as auto-dependencies, re-mark
#        declared packages as user-installed, then dnf autoremove
#        strips everything else — including dnf and rpm themselves.
#     5. Post-autoremove cleanup via statically-linked busybox: remove
#        package manager state, locale stubs, docs, and leftover dirs.
#
#   --mode=runtime (single-purpose *-workload images): keeps only the
#   application, ContainerCore, and their runtime dependencies. Bash remains
#   available for diagnostics and entrypoint scripts, while DNF, RPM,
#   repositories, caches, and unrelated bootstrap packages are removed.
#
# Only type="image" packages are considered by the keep-list modes. Bootstrap
# packages are used by kiwi only during initial chroot setup and are not part
# of the final image definition.
#
# Output sections (for debugging):
#   "Packages to KEEP"       — resolved names from the kiwi XML
#   "Force-removing ..."     — disallowed packages stripped before autoremove
#   "All installed packages" — full list before stripping
#   "Performing autoremove"  — dnf's own transaction log

test -f /.profile && . /.profile
set -xuo pipefail

echo "config.sh: building profile(s): ${kiwi_profiles:-<none>}"

# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

# Print a message to stderr and exit with an error code.
die() {
    echo "ERROR: $*" >&2
    exit 1
}

# ---------------------------------------------------------------------------
# Mode selection
# ---------------------------------------------------------------------------
MODE=""
for arg in "$@"; do
    case "${arg}" in
        --mode=*) MODE="${arg#--mode=}" ;;
        *) die "unrecognized argument: ${arg}" ;;
    esac
done
[[ -n "${MODE}" ]] || die "missing required --mode=strip|runtime argument"
[[ "${MODE}" == "strip" || "${MODE}" == "runtime" ]] \
    || die "unknown --mode value: ${MODE} (expected strip or runtime)"

# Extract package names from a <packages type="image"> section of the kiwi
# XML definition.  Returns one package name per line.
# $1: XPath predicate to further filter the <packages> element
#     (e.g., 'not(@profiles)' or "@profiles='distroless-debug'")
get_image_packages() {
    xmllint --xpath \
        "//packages[@type='image' and ${1}]/package/@name" \
        /image/config.xml 2>/dev/null \
    | grep -oP 'name="\K[^"]+' \
    || true  # No matches is not an error — the profile may have no packages.
}

# ---------------------------------------------------------------------------
# 1. Collect declared image packages from the kiwi XML
# ---------------------------------------------------------------------------

# Shared packages (no profiles attribute) apply to all profiles.
KEEP_PKGS=$(get_image_packages 'not(@profiles)')

# Packages scoped to specific profiles.  kiwi_profiles is a comma-separated
# list of active profiles, set by kiwi at build time (e.g.,
# "distroless-debug,distroless-core,distroless-minimal").
# Note: the @profiles attribute in the XML may also be comma-separated
# (e.g., "distroless-minimal,distroless-base,distroless-debug"), so we
# use contains() with comma-wrapping for safe substring matching.
IFS=',' read -ra PROFILES <<< "${kiwi_profiles:-}"
for profile in "${PROFILES[@]}"; do
    KEEP_PKGS+=$'\n'$(get_image_packages "contains(concat(',',@profiles,','), ',${profile},')")
done

# Deduplicate.
KEEP_PKGS=$(echo "${KEEP_PKGS}" | sort -u | grep -v '^$') || true

if [[ -z "${KEEP_PKGS}" ]]; then
    die "no packages found to keep — aborting to avoid stripping the entire image"
fi

# ---------------------------------------------------------------------------
# 2. Resolve virtual Provides to installed package names
# ---------------------------------------------------------------------------
# Some kiwi entries reference virtual provides (e.g., "system-release")
# rather than concrete package names (e.g., "azurelinux-release"). Resolve
# them so that dnf mark operates on real package names.

RESOLVED_KEEP_PKGS=""
while IFS= read -r pkg; do
    if rpm -q "${pkg}" &>/dev/null; then
        # Concrete package name — already installed.
        RESOLVED_KEEP_PKGS+="${pkg}"$'\n'
    elif resolved=$(rpm -q --whatprovides "${pkg}" --qf '%{NAME}\n' 2>/dev/null); then
        # Virtual provide — resolve to the package that owns it.
        RESOLVED_KEEP_PKGS+="${resolved}"$'\n'
    else
        die "'${pkg}' is neither installed nor provided by any installed package"
    fi
done <<< "${KEEP_PKGS}"

# Deduplicate (rpm --whatprovides may return duplicates for multi-arch).
RESOLVED_KEEP_PKGS=$(echo "${RESOLVED_KEEP_PKGS}" | sort -u | grep -v '^$') || true

if [[ -z "${RESOLVED_KEEP_PKGS}" ]]; then
    die "none of the keep-list packages could be resolved — aborting"
fi

# ---------------------------------------------------------------------------
# 3. Strip the image
# ---------------------------------------------------------------------------
# Overview:
#   a. Force-remove disallowed packages (bash; ca-certificates with cert
#      bundle snapshot/restore and artifact cleanup).
#   b. Mark packages as auto-deps, re-mark keep list as user, autoremove.
#   c. Post-autoremove cleanup via busybox (pkg manager state, locale, docs).

echo "=== Packages to KEEP (from kiwi XML) ==="
echo "${RESOLVED_KEEP_PKGS}"
echo ""

# ---------------------------------------------------------------------------
# 3a. Force-remove disallowed packages
# ---------------------------------------------------------------------------
echo "=== Force-removing disallowed packages ==="

if [[ "${MODE}" == "strip" ]]; then
    # --- ca-certificates ---
    # We need the cert bundles generated by update-ca-trust at install time,
    # but not the package itself or its runtime tooling (p11-kit). Snapshot
    # the generated files, remove the package, restore them, then prune
    # artifacts that aren't needed at runtime.
    if echo "${RESOLVED_KEEP_PKGS}" | grep -qxF ca-certificates; then
        die "'ca-certificates' is on the keep list but must be removed for distroless"
    fi

    CERT_PATHS=(
        /etc/pki/tls/cert.pem
        /etc/pki/tls/certs
        /etc/pki/ca-trust/extracted
        /etc/pki/java/cacerts
    )

    CERT_SNAPSHOT=$(mktemp -d /tmp/cert-snapshot.XXXXXX) \
        || die "failed to create cert snapshot directory"
    for path in "${CERT_PATHS[@]}"; do
        if [[ -e "${path}" ]]; then
            target_dir="${CERT_SNAPSHOT}$(dirname "${path}")"
            mkdir -p "${target_dir}"
            cp -a "${path}" "${target_dir}/"
        fi
    done

    find "${CERT_SNAPSHOT}" -name README -delete 2>/dev/null || true
    rm -rf "${CERT_SNAPSHOT}/etc/pki/ca-trust/extracted/pem/directory-hash"
    find "${CERT_SNAPSHOT}/etc/pki/tls/certs" -maxdepth 1 -name '*.0' -exec rm -f {} + 2>/dev/null || true

    if rpm -q ca-certificates &>/dev/null; then
        echo "  ca-certificates"
        rpm -e --nodeps ca-certificates 2>&1
    fi

    cp -a "${CERT_SNAPSHOT}/." /
    rm -rf "${CERT_SNAPSHOT}"

    # Remove last — ca-certificates scriptlets need Bash. The running process
    # is memory-resident so removing the package mid-execution is safe.
    if echo "${RESOLVED_KEEP_PKGS}" | grep -qxF bash; then
        die "'bash' is on the keep list but must be removed for distroless"
    fi
    if rpm -q bash &>/dev/null; then
        echo "  bash"
        rpm -e --nodeps bash 2>&1
    fi
fi

echo ""

# ---------------------------------------------------------------------------
# 3b. Remove workload-inappropriate package payloads
# ---------------------------------------------------------------------------

prune_package_payload() {
    local package_name="$1"
    rpm -q "${package_name}" &>/dev/null || return 0

    echo "  ${package_name}"
    rpm -ql "${package_name}" \
        | while IFS= read -r path; do
            case "${path}" in
                /usr/share/licenses/*) continue ;;
            esac
            if [[ -f "${path}" || -L "${path}" ]]; then
                rm -f -- "${path}"
            fi
        done
}

if [[ ",${kiwi_profiles:-}," == *,pytorch-workload,* ]]; then
    echo "=== Removing PyTorch development package payloads ==="
    for package_name in \
        binutils \
        git \
        git-core \
        git-core-doc \
        hipcc \
        rocm-clang \
        rocm-clang-devel \
        rocm-clang-runtime-devel \
        rocm-comgr-devel \
        rocm-hip-devel \
        rocm-libc++-devel \
        rocm-lld \
        rocm-llvm \
        rocm-llvm-devel \
        rocm-llvm-static \
        rocm-runtime-devel \
        rocrand-devel \
        zlib-ng-compat-devel
    do
        prune_package_payload "${package_name}"
    done
fi

# ---------------------------------------------------------------------------
# 3c. dnf autoremove
# ---------------------------------------------------------------------------

# Print the full package list for build log analysis.  A developer (or CI)
# can diff this against the autoremove transaction to determine exactly
# which packages survived.
echo "=== All installed packages ==="
rpm -qa --qf '%{NAME}\n' | sort
echo ""

# Mark every package as an auto-installed dependency, then re-mark only the
# keep list as user-installed.  autoremove removes anything not transitively
# required by a user-installed package.
#
# dnf5 note: packages installed externally (by kiwi's bootstrap) get reason
# "External User" and are NOT tracked in packages.toml.  `dnf mark dependency`
# forces them into packages.toml so that autoremove can evaluate them.
rpm -qa --qf '%{NAME}\n' | xargs -r dnf mark dependency -y --quiet 2>&1 \
    || die "failed to mark packages as dependencies"
echo "${RESOLVED_KEEP_PKGS}" | xargs -r dnf mark user -y --quiet 2>&1 \
    || die "failed to mark keep-list packages as user-installed"

# Stash busybox (statically linked) so we can clean up after autoremove
# removes coreutils + glibc.  Kiwi excludes /tmp/* from the final image.
# NOTE: the copy must be named "busybox" — busybox dispatches applets
# based on argv[0], so a different name causes "applet not found".
cp /usr/bin/busybox /tmp/busybox \
    || die "failed to stash busybox — is it in the bootstrap packages?"

echo ""
echo "=== Performing autoremove ==="
# protected_packages= clears the protected list so dnf can remove itself.
dnf autoremove -y \
    --setopt=protected_packages= \
    --setopt=tsflags=noscripts \
    2>&1 \
|| die "dnf autoremove failed"

# ---------------------------------------------------------------------------
# 3d. Post-autoremove cleanup (busybox)
# ---------------------------------------------------------------------------
# All external commands are gone at this point (coreutils, glibc removed).
# busybox is statically linked so it works without any shared libraries.
echo "=== Pruning artifacts (post-autoremove) ==="

# Package manager state (rpmdb, libdnf5, dnf config, caches, logs).
/tmp/busybox rm -rf /usr/lib/sysimage/libdnf5
/tmp/busybox rm -rf /usr/lib/sysimage/rpm
/tmp/busybox rm -rf /var/lib/rpm
/tmp/busybox rm -rf /var/lib/rpm-state
/tmp/busybox rm -rf /var/lib/dnf
/tmp/busybox rm -rf /var/cache/dnf
/tmp/busybox rm -rf /var/log/dnf5.log
/tmp/busybox rm -rf /etc/dnf
/tmp/busybox rm -rf /etc/yum.repos.d
/tmp/busybox rm -rf /usr/share/dnf5

# Locale stub directories (empty, from filesystem package).
/tmp/busybox rm -rf /usr/share/locale
if [[ "${MODE}" == "strip" ]]; then
    /tmp/busybox rm -rf /usr/lib/locale
fi

# Documentation is not needed at runtime.
/tmp/busybox rm -rf /usr/share/doc
if [[ "${MODE}" == "strip" ]]; then
    /tmp/busybox rm -rf /usr/share/licenses
fi

# Systemd (removed by autoremove, but dirs/presets may linger).
/tmp/busybox rm -rf /usr/lib/systemd

# PyTorch is a runtime image, not a ROCm SDK. Some ROCm runtime RPMs pull in
# compiler and development packages through overly broad dependencies. Keep
# the shared libraries needed by precompiled PyTorch, but remove static
# archives, headers, build metadata, and compiler frontends.
if [[ ",${kiwi_profiles:-}," == *,pytorch-workload,* ]]; then
    echo "=== Pruning PyTorch development toolchain ==="
    /tmp/busybox find /usr/lib /usr/lib64 -type f -name '*.a' -delete 2>/dev/null || true
    /tmp/busybox rm -rf /usr/include
    /tmp/busybox rm -rf /usr/lib/cmake /usr/lib64/cmake
    /tmp/busybox rm -rf /usr/lib/pkgconfig /usr/lib64/pkgconfig
    /tmp/busybox rm -rf /usr/share/cmake /usr/share/pkgconfig
    /tmp/busybox rm -rf /usr/lib64/rocm/llvm/bin
    /tmp/busybox rm -rf /usr/lib64/rocm/llvm/include
    /tmp/busybox rm -rf /usr/lib64/rocm/llvm/lib/cmake
    /tmp/busybox rm -rf /usr/lib64/rocm/llvm/lib/clang
    /tmp/busybox rm -rf /usr/lib64/rocm/llvm/share/clang
    /tmp/busybox rm -rf /usr/lib64/rocm/llvm/share/clang-doc
    /tmp/busybox rm -rf /usr/lib64/rocm/llvm/share/libc++
    /tmp/busybox rm -rf /usr/lib64/rocm/llvm/share/opt-viewer
    /tmp/busybox rm -f /usr/bin/hipcc /usr/bin/hipcc.pl
    /tmp/busybox rm -f /usr/bin/hipconfig /usr/bin/hipconfig.pl
fi

# ---------------------------------------------------------------------------
# 3e. busybox-workload only: install applet symlinks
# ---------------------------------------------------------------------------
# When the "busybox" package itself is on the keep list (busybox-workload),
# the shared runtime test harness still needs a `sh`/`sleep`/`echo` on PATH
# to start and exec into the container (it runs `sleep infinity` as the
# keep-alive command and `echo`/a shell for exec calls) -- busybox does not
# install applet symlinks itself. Wire up the minimum set the harness
# needs; busybox dispatches on argv[0], so these are just symlinks, not
# separate binaries.
if printf '%s\n' "${RESOLVED_KEEP_PKGS}" | /tmp/busybox grep -qxF busybox; then
    echo "=== Installing busybox applet symlinks (sh, sleep, echo) ==="
    for applet in sh sleep echo; do
        /tmp/busybox ln -sf /bin/busybox "/bin/${applet}"
    done
fi

# Clean up busybox itself.
/tmp/busybox rm -f /tmp/busybox
