#!/bin/sh

# Debuginfo repositories should remain disabled except during explicit opt-in.
# 1. Check Base's debug repository is disabled and targets this architecture.
# 2. Enable only that repository for one transaction and obtain symbols matching
#    the installed Bash version and architecture; check their origin and files.
# 3. Verify repository defaults were not changed. Remove symbols only if this
#    test installed them, and delete temporary files.

set -eu

repo=azurelinux-base-debuginfo
repo_file=/etc/yum.repos.d/azurelinux.repo
installed_here=0
tmp=$(mktemp -d)

cleanup() {
    rc=$1
    trap - 0 1 2 3 15
    set +e
    if [ "$installed_here" -eq 1 ]; then
        sudo dnf5 -y remove bash-debuginfo >/dev/null 2>&1
        [ $? -eq 0 ] || rc=1
    fi
    rm -rf "$tmp"
    [ "$rc" -eq 0 ] || rc=1
    exit "$rc"
}
trap 'cleanup $?' 0
trap 'cleanup 1' 1 2 3 15

fail() {
    echo "FAIL: $*" >&2
    exit 1
}

repo_value() {
    key=$1
    awk -v id="$repo" -v key="$key" '
        $0 == "[" id "]" { in_repo=1; next }
        /^\[/ { in_repo=0 }
        in_repo && $0 ~ "^[[:space:]]*" key "[[:space:]]*=" {
            sub("^[^=]*=[[:space:]]*", "")
            sub("[[:space:]]*$", "")
            print
            exit
        }
    ' "$repo_file"
}

[ -r "$repo_file" ] || fail "$repo_file is not readable"
rpm -q bash >/dev/null 2>&1 || fail "bash is not installed"

sudo dnf5 repo list --disabled >"$tmp/disabled-before" || \
    fail "cannot list disabled repositories"
awk -v id="$repo" '$1 == id { found=1 } END { exit(found ? 0 : 1) }' \
    "$tmp/disabled-before" || fail "$repo is not disabled initially"
[ "$(repo_value enabled)" = 0 ] || \
    fail "$repo does not have enabled=0 in $repo_file"
baseurl=$(repo_value baseurl)
case "$baseurl" in
    https://packages.microsoft.com/azurelinux/4/prod/base/debuginfo/'$basearch') ;;
    *) fail "$repo is not configured with the architecture-specific debuginfo endpoint" ;;
esac
repo_file_before=$(cksum "$repo_file")

bash_vr=$(rpm -q --qf '%{VERSION}-%{RELEASE}' bash) || \
    fail "cannot query bash version-release"
bash_arch=$(rpm -q --qf '%{ARCH}' bash) || fail "cannot query bash architecture"
debug_spec="bash-debuginfo-$bash_vr.$bash_arch"

if rpm -q bash-debuginfo >/dev/null 2>&1; then
    sudo dnf5 -y --disablerepo='*' --enablerepo="$repo" \
        reinstall "$debug_spec" >"$tmp/transaction" 2>&1 || {
            cat "$tmp/transaction" >&2
            fail "DNF could not reinstall $debug_spec solely from $repo"
        }
else
    installed_here=1
    sudo dnf5 -y --disablerepo='*' --enablerepo="$repo" \
        install "$debug_spec" >"$tmp/transaction" 2>&1 || {
            cat "$tmp/transaction" >&2
            fail "DNF could not install $debug_spec solely from $repo"
        }
fi

rpm -q bash-debuginfo >/dev/null 2>&1 || fail "bash-debuginfo is not installed"
debug_vr=$(rpm -q --qf '%{VERSION}-%{RELEASE}' bash-debuginfo) || \
    fail "cannot query bash-debuginfo version-release"
debug_arch=$(rpm -q --qf '%{ARCH}' bash-debuginfo) || \
    fail "cannot query bash-debuginfo architecture"
[ "$debug_vr" = "$bash_vr" ] || \
    fail "bash-debuginfo $debug_vr does not match bash $bash_vr"
[ "$debug_arch" = "$bash_arch" ] || \
    fail "bash-debuginfo architecture $debug_arch does not match bash architecture $bash_arch"

from_repo=$(sudo dnf5 -q repoquery --installed --qf '%{from_repo}' "$debug_spec") || \
    fail "cannot query the installed debuginfo package origin"
[ "$from_repo" = "$repo" ] || \
    fail "bash-debuginfo was recorded as coming from '$from_repo', not $repo"

rpm -ql bash-debuginfo | grep '^/usr/lib/debug/.*\.debug$' >"$tmp/debug-files" || \
    fail "bash-debuginfo provides no .debug files under /usr/lib/debug"
while IFS= read -r debug_file; do
    [ -f "$debug_file" ] || fail "listed debug symbol file is unavailable: $debug_file"
done <"$tmp/debug-files"

sudo dnf5 repo list --enabled >"$tmp/enabled-after" || \
    fail "cannot list enabled repositories after transient opt-in"
awk '$1 ~ /-debuginfo$/ { exit 1 }' "$tmp/enabled-after" || \
    fail "a debuginfo repository remained enabled after the one-command opt-in"
sudo dnf5 repo list --disabled >"$tmp/disabled-after" || \
    fail "cannot list disabled repositories after transient opt-in"
awk -v id="$repo" '$1 == id { found=1 } END { exit(found ? 0 : 1) }' \
    "$tmp/disabled-after" || fail "$repo did not return to the disabled repository list"
[ "$(repo_value enabled)" = 0 ] || \
    fail "$repo no longer has enabled=0 in $repo_file"
repo_file_after=$(cksum "$repo_file")
[ "$repo_file_after" = "$repo_file_before" ] || \
    fail "$repo_file was modified by transient repository enablement"

echo "PASS: DNF obtained matching Bash symbols solely from the transient architecture-specific debuginfo repository"
