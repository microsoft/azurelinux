#!/bin/sh

# azurelinux-repos marks Base, the core system repository, as required.
# 1. Redirect the other production repositories to tiny local fixtures and
#    confirm a fresh, unprivileged DNF query can read them.
# 2. Query the default repository set with only Base pointing at a missing path.
#    Local fixtures make this outage deliberate, not dependent on the network.
# 3. Require a failed query that names Base and its metadata error, rather than
#    silently incomplete results. Remove the temporary user and fixtures.

. ../helper.sh

repo_file=/etc/yum.repos.d/azurelinux.repo
tmp=
test_user=

cleanup() {
    status=$?
    trap - 0 1 2 15
    if [ -n "$test_user" ]; then
        sudo userdel -r "$test_user" >/dev/null 2>&1 || :
    fi
    if [ -n "$tmp" ]; then
        sudo rm -rf "$tmp"
    fi
    exit "$status"
}
trap cleanup 0 1 2 15

fail() {
    echo "FAIL: $*" >&2
    exit 1
}

[ -r "$repo_file" ] || fail "cannot read the shipped repository configuration: $repo_file"
awk '
    $0 == "[azurelinux-base]" { in_base = 1; next }
    /^\[/ { in_base = 0 }
    in_base && /^[[:space:]]*enabled[[:space:]]*=[[:space:]]*1[[:space:]]*$/ {
        enabled = 1
    }
    in_base && /^[[:space:]]*skip_if_unavailable[[:space:]]*=[[:space:]]*False[[:space:]]*$/ {
        required = 1
    }
    END { exit !(enabled && required) }
' "$repo_file" || fail "azurelinux-base is not enabled with skip_if_unavailable=False"

tmp=$(mktemp -d) || fail "could not create a temporary directory"
cloud_repo=$tmp/cloud-native
microsoft_repo=$tmp/microsoft
cache=$tmp/cache
control_output=$tmp/control-output
failure_output=$tmp/failure-output
sudo mkdir -p "$cloud_repo" "$microsoft_repo" "$cache" || fail "could not create test directories"

azl_make_rpm azurelinux-cloud-native-fixture 1 "$cloud_repo" || fail "could not build the Cloud Native fixture"
azl_make_repo "$cloud_repo" || fail "could not create the Cloud Native repository"
azl_make_rpm azurelinux-microsoft-fixture 1 "$microsoft_repo" || fail "could not build the Microsoft fixture"
azl_make_repo "$microsoft_repo" || fail "could not create the Microsoft repository"

test_user=azlrepo$$
sudo useradd --create-home --shell /bin/sh "$test_user" || fail "could not create the disposable user"
# mktemp creates its directory as 0700. Make the complete path traversable while
# retaining a private cache owned by the user that exercises DNF.
sudo chmod 755 "$tmp" || fail "could not make the fixture root traversable"
sudo chmod -R a+rX "$cloud_repo" "$microsoft_repo" || fail "could not make fixture repositories readable"
sudo chown "$test_user" "$cache" || fail "could not prepare the private DNF cache"

common_opts="--setopt=cachedir=$cache --setopt=azurelinux-base.baseurl=file:///nonexistent-$$ --setopt=azurelinux-cloud-native.baseurl=file://$cloud_repo --setopt=azurelinux-microsoft.baseurl=file://$microsoft_repo --refresh"

# Prove that the two non-Base repositories and the user's cache are usable.
sudo su - "$test_user" -c "dnf5 $common_opts --repo=azurelinux-cloud-native --repo=azurelinux-microsoft repoquery --available" >"$control_output" 2>&1
control_status=$?
if [ "$control_status" -ne 0 ]; then
    cat "$control_output" >&2
    fail "the non-Base repositories did not load successfully"
fi
for fixture in azurelinux-cloud-native-fixture azurelinux-microsoft-fixture; do
    if ! grep -F "$fixture" "$control_output" >/dev/null 2>&1; then
        cat "$control_output" >&2
        fail "positive control did not list $fixture"
    fi
done

# Use the shipped enabled-repository set: Base is the only invalid endpoint.
sudo su - "$test_user" -c "dnf5 $common_opts repoquery --available" >"$failure_output" 2>&1
dnf_status=$?
if [ "$dnf_status" -eq 0 ]; then
    cat "$failure_output" >&2
    fail "DNF silently continued after the required Base repository failed"
fi
if ! grep -F 'Failed to download metadata' "$failure_output" >/dev/null 2>&1; then
    cat "$failure_output" >&2
    fail "DNF failed without reporting a metadata download failure"
fi
if ! grep -F 'azurelinux-base' "$failure_output" >/dev/null 2>&1; then
    cat "$failure_output" >&2
    fail "DNF did not identify azurelinux-base as the failing repository"
fi

echo "PASS: DNF reported the unavailable required Base repository and failed the operation"
exit 0
