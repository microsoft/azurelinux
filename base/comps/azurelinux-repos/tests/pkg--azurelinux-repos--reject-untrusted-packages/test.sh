#!/bin/sh

# azurelinux-repos enables RPM signature checks to reject untrusted packages.
# 1. Build an unsigned dummy RPM and local repository, then redirect only Base's
#    URL to that fixture, retaining the shipped signature and signing-key policy.
# 2. Attempt installation with a fresh cache, so no remote service or stale
#    metadata can determine the outcome.
# 3. Require a signature-specific failure and no installed fixture, not merely
#    any failed command. Remove temporary files and any accidentally installed RPM.

pkg=azl-trust-fixture
tmp=$(mktemp -d) || exit 1
cleanup_package=0

cleanup() {
    rc=$?
    trap - 0 1 2 3 15
    if [ "$cleanup_package" -eq 1 ] && rpm -q "$pkg" >/dev/null 2>&1; then
        sudo rpm -e "$pkg" >/dev/null 2>&1 || :
    fi
    sudo rm -rf "$tmp"
    exit "$rc"
}
fail() {
    echo "FAIL: $*" >&2
    exit 1
}
trap cleanup 0
trap 'exit 1' 1 2 3 15

[ -r ../helper.sh ] || fail "shared RPM fixture helper is unavailable"
. ../helper.sh

rpm -q "$pkg" >/dev/null 2>&1 && fail "fixture package is already installed"
cleanup_package=1

azl_make_rpm "$pkg" 1.0 "$tmp/repo" || fail "could not build unsigned RPM fixture"
azl_make_repo "$tmp/repo" || fail "could not create local repository metadata"

output=$tmp/dnf-output
status=0
sudo env LC_ALL=C dnf5 -y \
    --setopt="cachedir=$tmp/cache" \
    --repo=azurelinux-base \
    --setopt="azurelinux-base.baseurl=file://$tmp/repo" \
    install "$pkg" >"$output" 2>&1 || status=$?
cat "$output"

[ "$status" -ne 0 ] || fail "DNF accepted the unsigned package"
grep -F "$pkg" "$output" >/dev/null 2>&1 || \
    fail "DNF output does not identify the selected package"
grep -Ei '(not[[:space:]]+signed|does[[:space:]]+not[[:space:]]+verify|no[[:space:]]+signature|(GPG|OpenPGP|signature)[^[:cntrl:]]*(failed|failure|invalid|missing|problem|error|verification|verify|check|not[[:space:]]+correct|not[[:space:]]+trusted|untrusted))' "$output" >/dev/null 2>&1 || \
    fail "DNF did not report a package-signature verification problem"
if rpm -q "$pkg" >/dev/null 2>&1; then
    fail "the untrusted package was installed despite the failed transaction"
fi

echo "PASS: DNF rejected the unsigned package and left it uninstalled"
exit 0
