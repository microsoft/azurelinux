#!/bin/sh

# Verify the shipped production repository configuration works end to end.
# 1. Check that only the three production repositories are enabled, with the
#    expected architecture-specific URLs, signing keys, and cache lifetime.
# 2. Refresh real repository metadata, then install a small package not already
#    present. This checks usable repositories, not just configuration text.
# 3. Confirm the installed RPM carries a signature; remove the test-installed
#    package and temporary files on exit.

fail()
{
    echo "FAIL: $*" >&2
    exit 1
}

workdir=$(mktemp -d) || exit 1
installed_pkg=

cleanup()
{
    rc=$?
    trap - 0 1 2 3 15

    if [ -n "$installed_pkg" ] && rpm -q "$installed_pkg" >/dev/null 2>&1; then
        if ! sudo dnf5 -y remove "$installed_pkg" >/dev/null 2>&1; then
            echo "FAIL: could not remove test-installed package $installed_pkg" >&2
            if [ "$rc" -eq 0 ]; then
                rc=1
            fi
        fi
    fi

    rm -f "$workdir/repo-list.json" \
        "$workdir/makecache.log" \
        "$workdir/repo-info.json" \
        "$workdir/repo-info-normalized.json" \
        "$workdir/query.out" \
        "$workdir/install.log" \
        "$workdir/signature.txt"
    rmdir "$workdir" 2>/dev/null || :
    exit "$rc"
}

trap cleanup 0
trap 'exit 1' 1 2 3 15

arch=$(uname -m) || fail "cannot determine the machine architecture"
case "$arch" in
    x86_64|aarch64) ;;
    *) fail "unsupported Azure Linux repository architecture: $arch" ;;
esac

if ! sudo dnf5 -q repo list --enabled --json >"$workdir/repo-list.json" 2>&1; then
    cat "$workdir/repo-list.json" >&2
    fail "DNF could not list enabled repositories"
fi

actual_ids=$(sed -n 's/^[[:space:]]*"id":[[:space:]]*"\([^"]*\)".*/\1/p' \
    "$workdir/repo-list.json" | LC_ALL=C sort)
expected_ids=$(printf '%s\n' \
    azurelinux-base \
    azurelinux-cloud-native \
    azurelinux-microsoft | LC_ALL=C sort)
if [ "$actual_ids" != "$expected_ids" ]; then
    echo "Enabled repository IDs:" >&2
    printf '%s\n' "$actual_ids" >&2
    fail "the enabled repositories are not exactly the three production channels"
fi

key=/etc/pki/rpm-gpg/RPM-GPG-KEY-azurelinux-4.0-$arch
[ -f "$key" ] || fail "architecture-specific signing key is missing: $key"
[ -r "$key" ] || fail "architecture-specific signing key is not readable: $key"

if ! sudo dnf5 --refresh makecache >"$workdir/makecache.log" 2>&1; then
    cat "$workdir/makecache.log" >&2
    fail "DNF could not refresh production repository metadata"
fi

if ! sudo dnf5 -q repo info --enabled --json >"$workdir/repo-info.json" 2>&1; then
    cat "$workdir/repo-info.json" >&2
    fail "DNF could not report resolved production repository information"
fi
sed 's#\\/#/#g' "$workdir/repo-info.json" >"$workdir/repo-info-normalized.json" || \
    fail "could not normalize DNF repository information"

for channel in base cloud-native microsoft; do
    endpoint="https://packages.microsoft.com/azurelinux/4/prod/$channel/$arch"
    grep -Fq "\"$endpoint\"" "$workdir/repo-info-normalized.json" || \
        fail "DNF did not resolve azurelinux-$channel to $endpoint"
done

if ! awk -F: '
    /"metadata_expire"[[:space:]]*:/ {
        value = $2
        gsub(/[^0-9]/, "", value)
        seen++
        if (value == 21600) correct++
    }
    END { exit !(seen == 3 && correct == 3) }
' "$workdir/repo-info-normalized.json"; then
    fail "each production repository must have a 21600-second (six-hour) metadata expiration"
fi

configured_key="file:///etc/pki/rpm-gpg/RPM-GPG-KEY-azurelinux-4.0-$arch"
key_count=$(grep -Fc "\"$configured_key\"" "$workdir/repo-info-normalized.json")
[ "$key_count" -eq 3 ] || \
    fail "all three production repositories must resolve the architecture-specific signing key"

gpgcheck_count=$(grep -c '"pkg_gpgcheck":[[:space:]]*true' \
    "$workdir/repo-info-normalized.json")
[ "$gpgcheck_count" -eq 3 ] || \
    fail "package signature checking is not enabled for all production repositories"

if ! awk -F: '
    /"available_pkgs"[[:space:]]*:/ {
        value = $2
        gsub(/[^0-9]/, "", value)
        seen++
        if (value + 0 > 0) populated++
    }
    END { exit !(seen == 3 && populated == 3) }
' "$workdir/repo-info-normalized.json"; then
    fail "DNF did not load package metadata from every production repository"
fi

pkg=
for candidate in tree which time attr acl jq; do
    if rpm -q "$candidate" >/dev/null 2>&1; then
        continue
    fi
    if ! sudo dnf5 -q repoquery --available --latest-limit=1 \
        --qf '%{name}|%{repoid}' "$candidate" >"$workdir/query.out" 2>&1; then
        continue
    fi
    if grep -Eq "^${candidate}\|(azurelinux-base|azurelinux-cloud-native|azurelinux-microsoft)$" \
        "$workdir/query.out"; then
        pkg=$candidate
        break
    fi
done
[ -n "$pkg" ] || fail "no small uninstalled package was available from a production repository"

installed_pkg=$pkg
if ! sudo dnf5 -y install "$pkg" >"$workdir/install.log" 2>&1; then
    cat "$workdir/install.log" >&2
    fail "DNF could not install $pkg from the production repositories"
fi
rpm -q "$pkg" >/dev/null 2>&1 || fail "$pkg is not installed after a successful DNF transaction"

if ! rpm -q --qf '%{SIGPGP:pgpsig} %{RSAHEADER:pgpsig}\n' "$pkg" \
    >"$workdir/signature.txt" 2>&1; then
    cat "$workdir/signature.txt" >&2
    fail "could not inspect the installed package signature"
fi
if ! grep -Eq 'Key ID [[:xdigit:]]{8,}' "$workdir/signature.txt"; then
    cat "$workdir/signature.txt" >&2
    fail "the installed production package does not carry an RPM signature key ID"
fi

echo "PASS: DNF refreshed all three production channels and installed signed package $pkg"
