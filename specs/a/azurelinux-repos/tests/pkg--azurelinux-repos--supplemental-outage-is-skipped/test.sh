#!/bin/sh

# azurelinux-repos makes Cloud Native and Microsoft supplemental repositories
# optional: their outages should not block packages from healthy repositories.
# 1. Build local repositories with distinct dummy packages and query them as a
#    disposable user, with fresh caches to avoid hiding missing repositories.
# 2. Make each optional repository unavailable in turn, leaving the others usable.
# 3. Require success, an outage warning, and only the healthy repositories'
#    packages in the results. Remove the temporary user and fixtures on exit.

set -eu

. ../helper.sh

work=$(mktemp -d)
test_user="azlrepo$$"
user_created=0
cleanup() {
    if [ "$user_created" -eq 1 ]; then
        sudo userdel -r "$test_user" >/dev/null 2>&1 || :
    fi
    sudo rm -rf "$work"
}
trap cleanup 0
trap 'exit 1' 1 2 3 15

sudo useradd -m -s /bin/sh "$test_user"
user_created=1

mkdir -p "$work/repos/base" "$work/repos/cloud-native" "$work/repos/microsoft"
azl_make_rpm azl-base-pkg 1.0 "$work/repos/base"
azl_make_rpm azl-cn-pkg 1.0 "$work/repos/cloud-native"
azl_make_rpm azl-ms-pkg 1.0 "$work/repos/microsoft"
azl_make_repo "$work/repos/base"
azl_make_repo "$work/repos/cloud-native"
azl_make_repo "$work/repos/microsoft"
sudo chown -R "$test_user" "$work"

failed=0

run_query() {
    case_name=$1
    cloud_url=$2
    microsoft_url=$3
    stdout_file="$work/$case_name.stdout"
    stderr_file="$work/$case_name.stderr"
    log_file="$work/$case_name.dnf5.log"

    set +e
    sudo su - "$test_user" -c "
        rm -f \"\$HOME/.local/state/dnf5.log\"
        LC_ALL=C dnf5 --refresh --setopt=cachedir=$work/cache-$case_name --setopt=azurelinux-base.baseurl=file://$work/repos/base --setopt=azurelinux-cloud-native.baseurl=$cloud_url --setopt=azurelinux-microsoft.baseurl=$microsoft_url repoquery --available --qf '%{name}\\n' azl-base-pkg azl-cn-pkg azl-ms-pkg
        query_status=\$?
        if [ -f \"\$HOME/.local/state/dnf5.log\" ]; then
            cp \"\$HOME/.local/state/dnf5.log\" '$log_file'
        fi
        exit \$query_status
    " >"$stdout_file" 2>"$stderr_file"
    case_status=$?
    set -e

    if [ "$case_status" -ne 0 ]; then
        printf '%s\n' "FAIL: $case_name exited with status $case_status"
        failed=1
    fi
}

expect_package() {
    if ! grep -Fqx "$2" "$1"; then
        printf '%s\n' "FAIL: expected package $2 was not offered"
        failed=1
    fi
}

reject_package() {
    if grep -Fqx "$2" "$1"; then
        printf '%s\n' "FAIL: package $2 was offered by an unavailable repository"
        failed=1
    fi
}

expect_skip_warning() {
    stderr_file=$1
    log_file=$2
    repo_id=$3
    missing_url_id=$4

    log_names_repo=1
    log_names_skip=1
    if [ -f "$log_file" ]; then
        grep -F "Error loading repo \"$repo_id\"" "$log_file" >/dev/null && log_names_repo=0
        grep -iF 'skip' "$log_file" >/dev/null && log_names_skip=0
    fi

    if [ "$log_names_repo" -eq 0 ] && [ "$log_names_skip" -eq 0 ]; then
        return
    fi
    if grep -F "$missing_url_id" "$stderr_file" >/dev/null; then
        return
    fi

    printf '%s\n' "FAIL: no skip warning identified repository $repo_id"
    printf '%s\n' "--- $repo_id dnf5.log tail ---"
    if [ -f "$log_file" ]; then
        tail -n 40 "$log_file" | sed 's/^/  /'
    else
        printf '%s\n' '  (dnf5.log was not created)'
    fi
    failed=1
}

missing_cloud_id="nonexistent-azurelinux-cloud-native-$$"
missing_cloud="file:///$missing_cloud_id"
run_query cloud-native-outage "$missing_cloud" "file://$work/repos/microsoft"
expect_skip_warning "$work/cloud-native-outage.stderr" "$work/cloud-native-outage.dnf5.log" azurelinux-cloud-native "$missing_cloud_id"
expect_package "$work/cloud-native-outage.stdout" azl-base-pkg
expect_package "$work/cloud-native-outage.stdout" azl-ms-pkg
reject_package "$work/cloud-native-outage.stdout" azl-cn-pkg

missing_microsoft_id="nonexistent-azurelinux-microsoft-$$"
missing_microsoft="file:///$missing_microsoft_id"
run_query microsoft-outage "file://$work/repos/cloud-native" "$missing_microsoft"
expect_skip_warning "$work/microsoft-outage.stderr" "$work/microsoft-outage.dnf5.log" azurelinux-microsoft "$missing_microsoft_id"
expect_package "$work/microsoft-outage.stdout" azl-base-pkg
expect_package "$work/microsoft-outage.stdout" azl-cn-pkg
reject_package "$work/microsoft-outage.stdout" azl-ms-pkg

if [ "$failed" -ne 0 ]; then
    printf '%s\n' '--- cloud-native outage stdout ---'
    sed 's/^/  /' "$work/cloud-native-outage.stdout"
    printf '%s\n' '--- cloud-native outage stderr ---'
    sed 's/^/  /' "$work/cloud-native-outage.stderr"
    printf '%s\n' '--- microsoft outage stdout ---'
    sed 's/^/  /' "$work/microsoft-outage.stdout"
    printf '%s\n' '--- microsoft outage stderr ---'
    sed 's/^/  /' "$work/microsoft-outage.stderr"
    exit 1
fi

printf '%s\n' 'Supplemental repository outages were warned about and skipped; available repositories remained usable.'
exit 0
