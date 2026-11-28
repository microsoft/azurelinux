#!/bin/bash
set -euo pipefail

source_dir=$(realpath "${1:?Usage: test-fips-selftests.sh <dracut source directory>}")
workdir=$(mktemp -d)
trap 'rm -rf -- "$workdir"' EXIT

run_case() (
    local name=$1 config=$2 tcrypt=$3 expected=$4
    local runtime_fips=${5:-1} runtime_kernel=${6:-6.18-test} location=${7:-boot}
    local crypto=${8:-available} owner=${9:-kernel-hwe}
    local dracutsysrootdir="$workdir/$name/root" initdir="$workdir/$name/init"
    local kernel=6.18-test hostonly='' DRACUT_SYSTEMD=1
    local srcmods="$dracutsysrootdir/lib/modules/$kernel"
    local trace="$initdir/trace" status

    mkdir -p "$srcmods" "$dracutsysrootdir/boot" "$initdir/etc" \
        "$initdir/proc/sys/crypto" "$initdir/tmp"
    if [[ $location == boot ]]; then
        printf '%s\n' "$config" > "$dracutsysrootdir/boot/config-$kernel"
    elif [[ $location == modules ]]; then
        printf '%s\n' "$config" > "$srcmods/config"
    elif [[ $location == rebuild ]]; then
        printf '%s\n' "$kernel" > "$initdir/etc/fips-kernel-selftests"
    fi
    printf 'sha256 tcrypt\0' > "$srcmods/modules.fips"
    printf '%s\n' "$runtime_fips" > "$initdir/proc/sys/crypto/fips_enabled"
    : > "$initdir/proc/crypto"
    if [[ $crypto == builtin ]]; then
        printf 'name : sha256\n' > "$initdir/proc/crypto"
    fi
    : > "$trace"

    dinfo() { :; }
    dwarn() { printf '%s\n' "$*" >&2; }
    rpm() {
        [[ $# == 6 && $1 == --root && $2 == "$dracutsysrootdir" \
            && $3 == -qf && $4 == --qf && $5 == '%{NAME}\n' \
            && $6 == "/boot/vmlinuz-$kernel" ]] || return 2
        if [[ $owner == unowned ]]; then
            printf 'Kernel image has no verified RPM owner\n' >&2
            return 1
        fi
        printf '%s\n' "$owner"
    }
    instmods() {
        local module=$3
        printf 'install %s\n' "$module" >> "$trace"
        [[ $module != tcrypt || $tcrypt == available ]]
    }
    # shellcheck source=/dev/null
    source "$source_dir/modules.d/01fips/module-setup.sh"
    installkernel

    getarg() { return 1; }
    warn() { printf '%s\n' "$*" >&2; }
    uname() { printf '%s\n' "$runtime_kernel"; }
    modprobe() {
        printf 'load %s\n' "$1" >> "$trace"
        if [[ $1 == sha256 && $crypto != available ]]; then
            printf 'modprobe: FATAL: Module %s not found\n' "$1" >&2
            return 1
        fi
        [[ $1 != tcrypt || $tcrypt == available ]]
    }
    rmmod() { printf 'unload %s\n' "$1" >> "$trace"; }
    # Redirect filesystem access, not FIPS logic, into this test's private root.
    sed -e "s|/tmp/|$initdir/tmp/|g" \
        -e "s|/etc/|$initdir/etc/|g" \
        -e "s|/proc/|$initdir/proc/|g" \
        -e "s|/run/|$initdir/run/|g" \
        "$source_dir/modules.d/01fips/fips.sh" > "$initdir/runtime.sh"
    # shellcheck source=/dev/null
    source "$initdir/runtime.sh"
    set +o pipefail
    if fips_load_crypto; then
        status=0
    else
        status=$?
    fi
    if [[ $status != "$expected" ]]; then
        printf 'FAIL: %s: expected status %s, got %s\n' "$name" "$expected" "$status" >&2
        exit 1
    fi
    if [[ $status == 0 ]]; then
        grep -qx 'load sha256' "$trace"
    fi
    if [[ -f "$initdir/etc/fips-kernel-selftests" ]]; then
        if grep -q tcrypt "$trace"; then
            printf 'FAIL: %s: kernel self-tests still requested tcrypt\n' "$name" >&2
            exit 1
        fi
    else
        grep -qx 'load tcrypt' "$trace"
        if [[ $status == 0 ]]; then
            grep -qx 'unload tcrypt' "$trace"
        fi
    fi
    printf 'PASS: %s\n' "$name"
)

modern=$'CONFIG_CRYPTO_SELFTESTS=y\nCONFIG_CRYPTO_FIPS=y\nCONFIG_CRYPTO_MANAGER=y'
legacy=$'CONFIG_CRYPTO_TEST=m\nCONFIG_CRYPTO_FIPS=y\nCONFIG_CRYPTO_MANAGER=y'

run_case modern "$modern" absent 0
run_case modern-missing-crypto "$modern" absent 1 1 6.18-test boot missing
run_case modern-builtin-crypto "$modern" absent 0 1 6.18-test boot builtin
run_case non-hwe-missing-tcrypt "$modern" absent 1 1 6.18-test boot available kernel
run_case non-hwe-selftests "$modern" available 0 1 6.18-test boot available kernel
run_case unverified-kernel-owner "$modern" absent 1 1 6.18-test boot available unowned
run_case legacy "$legacy" available 0
run_case legacy-missing-tcrypt "$legacy" absent 1
run_case selftests-disabled "${modern/CONFIG_CRYPTO_SELFTESTS=y/CONFIG_CRYPTO_SELFTESTS=n}" absent 1
run_case fips-disabled "${modern/CONFIG_CRYPTO_FIPS=y/CONFIG_CRYPTO_FIPS=n}" absent 1
run_case manager-not-builtin "${modern/CONFIG_CRYPTO_MANAGER=y/CONFIG_CRYPTO_MANAGER=m}" absent 1
run_case missing-config "$modern" absent 1 1 6.18-test missing
run_case rebuild-without-config "$modern" absent 1 1 6.18-test rebuild
run_case module-config "$modern" absent 0 1 6.18-test modules
run_case runtime-not-fips "$modern" absent 1 0
run_case wrong-running-kernel "$modern" absent 1 1 6.6-test
