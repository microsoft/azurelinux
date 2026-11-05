#!/bin/sh

# Source repositories should remain disabled except during explicit opt-in.
# 1. Check that Base's source repository is disabled in configuration and DNF.
# 2. As a disposable user with private caches, explicitly query and download
#    Bash's source RPM. This proves source content is actually accessible.
# 3. Confirm later default operations still leave source repositories disabled.
#    Remove the temporary user, downloaded sources, and caches on exit.

repo_id=azurelinux-base-source
repo_file=/etc/yum.repos.d/azurelinux.repo
test_user=azlsrc$$
user_created=0
test_home=

cleanup() {
    if [ "$user_created" -eq 1 ]; then
        sudo userdel -r "$test_user" >/dev/null 2>&1 || :
        user_created=0
    fi
}

fail() {
    printf 'FAIL: %s\n' "$*" >&2
    exit 1
}

trap 'cleanup' 0
trap 'cleanup; exit 1' 1 2 3 15

for command_name in dnf5 sudo useradd userdel su awk grep mkdir cat; do
    command -v "$command_name" >/dev/null 2>&1 || fail "required command is unavailable: $command_name"
done

[ -r "$repo_file" ] || fail "repository configuration is not readable: $repo_file"

repo_file_has_disabled_source() {
    awk -v wanted="$repo_id" '
        /^[[:space:]]*\[/ {
            section = $0
            sub(/^[[:space:]]*\[/, "", section)
            sub(/\][[:space:]]*$/, "", section)
            in_wanted = (section == wanted)
            if (in_wanted) {
                seen_section = 1
            }
            next
        }
        in_wanted && /^[[:space:]]*enabled[[:space:]]*=/ {
            value = $0
            sub(/^[^=]*=[[:space:]]*/, "", value)
            sub(/[[:space:]]*$/, "", value)
            if (value == "0") {
                seen_disabled = 1
            } else {
                bad_value = 1
            }
        }
        END { exit(seen_section && seen_disabled && !bad_value ? 0 : 1) }
    ' "$repo_file"
}

repo_file_has_disabled_source || fail "$repo_id is not persisted with enabled=0"

if ! sudo useradd -m "$test_user"; then
    fail "could not create disposable user $test_user"
fi
user_created=1

test_home=$(awk -F: -v user="$test_user" '$1 == user { print $6; exit }' /etc/passwd)
[ -n "$test_home" ] && [ -d "$test_home" ] || fail "could not determine the disposable user's home directory"

if ! su - "$test_user" -c 'mkdir -p "$HOME/dnf-cache" "$HOME/default-cache" "$HOME/downloads"'; then
    fail "could not prepare the disposable user's private directories"
fi

if ! su - "$test_user" -c 'dnf5 -q --setopt=cachedir="$HOME/dnf-cache" repo list --disabled >"$HOME/disabled-before.out" 2>"$HOME/disabled-before.err"'; then
    cat "$test_home/disabled-before.err" >&2
    fail "DNF could not list disabled repositories"
fi
if ! grep -Eq '(^|[[:space:]])azurelinux-base-source([[:space:]]|$)' "$test_home/disabled-before.out"; then
    cat "$test_home/disabled-before.out" >&2
    fail "$repo_id is not reported as disabled by default"
fi

if ! su - "$test_user" -c 'dnf5 -q --setopt=cachedir="$HOME/dnf-cache" --repo=azurelinux-base-source repoquery --arch=src bash >"$HOME/query.out" 2>"$HOME/query.err"'; then
    cat "$test_home/query.err" >&2
    fail "explicit source-repository query failed"
fi
if ! grep -Eq '^bash-.*\.src[[:space:]]*$' "$test_home/query.out"; then
    cat "$test_home/query.out" >&2
    fail "the selected source repository did not return a Bash source-package result"
fi

if ! su - "$test_user" -c 'dnf5 -q --setopt=cachedir="$HOME/dnf-cache" --enablerepo=azurelinux-base-source download --srpm --destdir "$HOME/downloads" bash >"$HOME/download.out" 2>"$HOME/download.err"'; then
    cat "$test_home/download.err" >&2
    fail "explicit Bash source-package download failed"
fi

download_found=0
for source_rpm in "$test_home"/downloads/bash-*.src.rpm; do
    if [ -f "$source_rpm" ]; then
        download_found=1
        break
    fi
done
[ "$download_found" -eq 1 ] || fail "DNF did not create a bash-*.src.rpm file"

repo_file_has_disabled_source || fail "the explicit operations changed the persisted enabled=0 setting"

if ! su - "$test_user" -c 'dnf5 -q --setopt=cachedir="$HOME/default-cache" repo list --enabled >"$HOME/enabled-after.out" 2>"$HOME/enabled-after.err"'; then
    cat "$test_home/enabled-after.err" >&2
    fail "DNF could not list repositories enabled for a later default operation"
fi
if grep -Eq '(^|[[:space:]])[[:alnum:]_.+:-]*-source([[:space:]]|$)' "$test_home/enabled-after.out"; then
    cat "$test_home/enabled-after.out" >&2
    fail "a source repository remained enabled for a later default operation"
fi

printf 'PASS: explicit source access queried and downloaded the Bash SRPM without persistently enabling source repositories\n'
exit 0
