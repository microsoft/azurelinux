#!/bin/sh

# azurelinux-repos ships Preview repositories disabled to avoid accidental use
# of prerelease packages; DNF can explicitly select them for one operation.
# 1. Use a disposable user and private caches; verify Preview Base is disabled.
# 2. Explicitly query and download a real Preview package, checking the resolved
#    URL matches the machine architecture. Downloads do not install the package.
# 3. Confirm default queries exclude Preview and the opt-in did not change its
#    disabled setting. Delete the user's downloads, caches, and workspace.

set -u

for command_name in sudo useradd userdel su dnf5 awk grep uname mktemp; do
    if ! command -v "$command_name" >/dev/null 2>&1; then
        echo "Required command is unavailable: $command_name" >&2
        exit 1
    fi
done

workdir=$(mktemp -d) || {
    echo "Unable to create a temporary directory" >&2
    exit 1
}
test_user="azlprv$$"
user_created=0

cleanup()
{
    status=$?
    trap - 0 1 2 15
    if [ "$user_created" -eq 1 ]; then
        sudo userdel -r "$test_user" >/dev/null 2>&1 || :
    fi
    sudo rm -rf "$workdir"
    exit "$status"
}
trap cleanup 0
trap 'exit 1' 1 2 15

if ! sudo useradd -m "$test_user"; then
    echo "Unable to create disposable user $test_user" >&2
    exit 1
fi
user_created=1

cat >"$workdir/check-preview.sh" <<'INNER'
#!/bin/sh

set -eu

repo=azurelinux-preview-base
repo_file=/etc/yum.repos.d/azurelinux-preview.repo
cache_dir=$HOME/dnf-cache
state_dir=$HOME/dnf-state
log_dir=$HOME/dnf-log
download_dir=$HOME/download
mkdir -p "$cache_dir" "$state_dir" "$log_dir" "$download_dir"

dnf_private()
{
    dnf5 -q \
        --setopt="cachedir=$cache_dir" \
        --setopt="persistdir=$state_dir" \
        --setopt="logdir=$log_dir" \
        "$@"
}

repo_is_persistently_disabled()
{
    awk -v wanted="$repo" '
        $0 == "[" wanted "]" {
            in_section = 1
            found = 1
            next
        }
        /^\[/ { in_section = 0 }
        in_section && /^[[:space:]]*enabled[[:space:]]*=/ {
            value = $0
            sub(/^[^=]*=/, "", value)
            gsub(/[[:space:]]/, "", value)
            count++
            if (value == "0")
                disabled++
            else
                bad = 1
        }
        END { exit !(found && count == 1 && disabled == 1 && !bad) }
    ' "$repo_file"
}

repo_list_contains()
{
    awk -v wanted="$repo" '$1 == wanted { found = 1 } END { exit !found }' "$1"
}

if [ ! -r "$repo_file" ]; then
    echo "Stock preview repository definition is missing or unreadable: $repo_file" >&2
    exit 1
fi
if ! repo_is_persistently_disabled; then
    echo "$repo is not persisted with enabled=0 before the operation" >&2
    exit 1
fi

dnf_private repo list --disabled >"$HOME/disabled-before"
if ! repo_list_contains "$HOME/disabled-before"; then
    echo "$repo is not listed among disabled repositories" >&2
    exit 1
fi

dnf_private repo list --enabled >"$HOME/enabled-before"
if repo_list_contains "$HOME/enabled-before"; then
    echo "$repo is unexpectedly enabled by default" >&2
    exit 1
fi

# A fresh private cache proves that explicit opt-in reaches the binary Preview
# Base repository rather than merely displaying its installed configuration.
dnf_private --repo="$repo" repoquery \
    --available --qf '%{name}\n' >"$HOME/preview-packages"
pkg=$(awk 'NF { print; exit }' "$HOME/preview-packages")
if [ -z "$pkg" ]; then
    echo "$repo returned no available packages" >&2
    exit 1
fi

# A package may also exist in Production, but default selection must never
# return a copy from a disabled Preview repository.
dnf_private repoquery --available --qf '%{repoid}\n' "$pkg" >"$HOME/default-results"
if awk '$1 ~ /^azurelinux-preview-/ { found = 1 } END { exit !found }' "$HOME/default-results"; then
    echo "Default discovery selected Preview content for $pkg" >&2
    exit 1
fi

# Explicit selection must discover the chosen package in Preview Base.
dnf_private --repo="$repo" repoquery \
    --available --qf '%{repoid}\n' "$pkg" >"$HOME/preview-results"
if ! awk -v wanted="$repo" '
    NF {
        seen = 1
        if ($1 != wanted)
            wrong = 1
    }
    END { exit !(seen && !wrong) }
' "$HOME/preview-results"; then
    echo "Explicit discovery did not return $pkg solely from $repo" >&2
    exit 1
fi

arch=$(uname -m)
dnf_private --repo="$repo" repo info "$repo" >"$HOME/repo-info"
if ! grep -F "/preview/base/$arch" "$HOME/repo-info" >/dev/null; then
    echo "Explicit opt-in did not load the architecture-specific Preview Base endpoint" >&2
    exit 1
fi

dnf_private --repo="$repo" download \
    --destdir="$download_dir" "$pkg"
set -- "$download_dir"/*.rpm
if [ ! -f "$1" ]; then
    echo "No RPM was downloaded for $pkg from $repo" >&2
    exit 1
fi

# Per-operation enablement must not alter later default selection or the
# installed repository definition.
dnf_private repo list --enabled >"$HOME/enabled-after"
if repo_list_contains "$HOME/enabled-after"; then
    echo "$repo remained enabled after the opted-in operations" >&2
    exit 1
fi
dnf_private repo list --disabled >"$HOME/disabled-after"
if ! repo_list_contains "$HOME/disabled-after"; then
    echo "$repo is no longer listed as disabled" >&2
    exit 1
fi
if ! repo_is_persistently_disabled; then
    echo "$repo_file no longer persists $repo with enabled=0" >&2
    exit 1
fi

echo "Preview package $pkg was discovered and downloaded without enabling Preview by default"
INNER
chmod 0755 "$workdir/check-preview.sh"
sudo chown -R "$test_user" "$workdir"

if ! sudo su - "$test_user" -c "/bin/sh '$workdir/check-preview.sh'"; then
    echo "Preview repository opt-in behavior did not meet expectations" >&2
    exit 1
fi

exit 0
