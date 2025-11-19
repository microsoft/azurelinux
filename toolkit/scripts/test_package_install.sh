#!/bin/bash
# Copyright (c) Microsoft Corporation.

set -e

DAILY_BUILD_ID=""

# parse script parameters:
#
# -p -> folder where built RPMs/SRPMs are published
# -s -> packages to test for install and uninstall functionality
# -i -> packages to not install
# -u -> packages to not uninstall
# -y -> daily build ID
# -d -> dist tag
# -v -> verbose output

while getopts ":p:s:i:u:y:d:v" OPTIONS; do
  case "${OPTIONS}" in
    p ) RPM_DIRECTORY=$OPTARG;;
    s ) RPMS_TO_INSTALL=${OPTARG//,/ } ;;
    i ) PACKAGES_TO_NOT_INSTALL=${OPTARG//,/ } ;;
    u ) PACKAGES_TO_NOT_UNINSTALL=${OPTARG//,/ } ;;
    y ) DAILY_BUILD_ID=$OPTARG ;;
    d ) DIST_TAG=$OPTARG ;;
    v ) set -x ;;

    \? )
        echo "Error - Invalid Option: -$OPTARG" 1>&2
        exit 1
        ;;
    : )
        echo "Error - Invalid Option: -$OPTARG requires an argument" 1>&2
        exit 1
        ;;
  esac
done

ARCHITECTURE=$(uname -p)

# Determine LKG_BASE_URL
if [[ -n $DAILY_BUILD_ID &&
      $DAILY_BUILD_ID == "latest" &&
      $DIST_TAG == ".azl3" ]]; then
    echo "Determine LKG_BASE_URL directly from lkg-3.0-dev.json"
    wget -nv https://mariner3dailydevrepo.blob.core.windows.net/lkg/lkg-3.0-dev.json
    LKG_BASE_URL=$(cat lkg-3.0-dev.json | jq -r .repo.$ARCHITECTURE)
else
    echo "Determine LKG_BASE_URL from provided DAILY_BUILD_ID"
    if [[ $ARCHITECTURE == "x86_64" ]]; then
        DAILY_BUILD_ARCH="-x86-64"
    else
        DAILY_BUILD_ARCH="-aarch64"
    fi
    LKG_BASE_URL=https://mariner3dailydevrepo.blob.core.windows.net/daily-repo-$DAILY_BUILD_ID$DAILY_BUILD_ARCH
fi

echo "---------------------------------------------------------------"
echo "-- Install packages in provided folder --"
echo "---------------------------------------------------------------"
echo "-- RPM_DIRECTORY                            -> $RPM_DIRECTORY"
echo "-- RPMS_TO_INSTALL                          -> $RPMS_TO_INSTALL"
echo "-- LKG_BASE_URL                             -> '$LKG_BASE_URL'"
echo "-- DAILY_BUILD_ID                           -> '$DAILY_BUILD_ID'"
echo "-- DAILY_BUILD_ARCH                         -> '$DAILY_BUILD_ARCH'"
echo "-- DIST_TAG                                 -> '$DIST_TAG'"
echo "-- PACKAGES_TO_NOT_INSTALL                  -> $PACKAGES_TO_NOT_INSTALL"
echo "-- PACKAGES_TO_NOT_UNINSTALL                -> $PACKAGES_TO_NOT_UNINSTALL"
echo ""

echo "##[debug]Installing these space separated packages:"
echo "$RPMS_TO_INSTALL"
echo ""

RPMS_TO_INSTALL=($RPMS_TO_INSTALL)
PACKAGES_TO_NOT_INSTALL=($PACKAGES_TO_NOT_INSTALL)
PACKAGES_TO_NOT_UNINSTALL=($PACKAGES_TO_NOT_UNINSTALL)


exists_in_list() {
    local VALUE=$1
    shift
    local LIST=("$@")

    for x in "${LIST[@]}"; do
        if [ "$x" = "$VALUE" ]; then
            return 0
        fi
    done
    return 1
}

# Add built packages as a local repo for tdnf
sudo createrepo --compatibility "$RPM_DIRECTORY"

repo_content=$(cat << EOF
[builtpackages]
name=Local Built Packages($ARCHITECTURE)
baseurl=file://$RPM_DIRECTORY
enabled=1
priority=0
skip_if_unavailable=True
enabled=1
EOF
)

# create the repo metadata file
echo "$repo_content" | sudo tee /etc/yum.repos.d/builtpackages.repo > /dev/null

echo "##[debug]Created repo file with content:"
sudo cat /etc/yum.repos.d/builtpackages.repo
echo ""

# Add daily 3.0 repo if available
repo_content_daily=$(cat << EOF
[daily3]
name=Daily 3.0 repo
baseurl=$LKG_BASE_URL
gpgkey=file:///etc/pki/rpm-gpg/MICROSOFT-RPM-GPG-KEY file:///etc/pki/rpm-gpg/MICROSOFT-METADATA-GPG-KEY
gpgcheck=0
repo_gpgcheck=0
enabled=1
skip_if_unavailable=True
sslverify=0
EOF
)

if [[ $DIST_TAG == ".azl3" ]]; then
    echo "$repo_content_daily" | sudo tee /etc/yum.repos.d/daily3.repo > /dev/null
    echo "##[debug]Created daily repo file with content:"
    sudo cat /etc/yum.repos.d/daily3.repo
    echo ""
else
    echo "Mariner 3.0 was not detected, so skipping daily repo setup"
fi

# update the cached binary metadata.
sudo tdnf makecache

sudo tdnf repolist --refresh

PACKAGES_FAIL_INSTALL=()
PACKAGES_FAIL_UNINSTALL=()

for rpm_to_install in "${RPMS_TO_INSTALL[@]}"; do
    path_to_rpm=$(find $RPM_DIRECTORY -name "$rpm_to_install")
    package_name_to_install=$(rpm -qp --queryformat "%{name}" "$path_to_rpm" 2>/dev/null)

    if exists_in_list "$package_name_to_install" "${PACKAGES_TO_NOT_INSTALL[@]}"; then
        echo "##[debug]Skipping package $package_name_to_install for installation test"
        continue
    fi

    echo "------------------------------------------------"
    echo "About to tdnf install package '$package_name_to_install' ('$rpm_to_install')"
    # we are using package files instead of names to include subpackages produces with %{name}-{subpackage_name}
    if ! sudo tdnf install -y "$path_to_rpm"; then
        PACKAGES_FAIL_INSTALL+=("$package_name_to_install")
        # package did not install, skip uninstall test
        echo "The following package failed to install: '$package_name_to_install'"
        continue
    fi

    if exists_in_list "$package_name_to_install" "${PACKAGES_TO_NOT_UNINSTALL[@]}"; then
        echo "##[debug]Skipping package $package_name_to_install for uninstallation test"
        continue
    fi

    # tdnf cannot accept the package rpm for uninstalling, only name. So we cannot test uninstalling of subpackages
    echo "About to tdnf remove package '$package_name_to_install'"
    if ! sudo tdnf remove -y "$package_name_to_install"; then
        PACKAGES_FAIL_UNINSTALL+=("$package_name_to_install")
    fi
    echo ""
    echo ""
done

echo ""
echo "------------------------------------------------"
echo "-- Printing install + uninstall error details --"
echo "------------------------------------------------"
echo ""

if [ "${#PACKAGES_FAIL_INSTALL[@]}" -gt 0 ]; then
    echo "##vso[task.logissue type=error]Error, ${#PACKAGES_FAIL_INSTALL[@]} packages failed to install, check logs to see the list"
    echo "Failed installed packages:"
    echo "${PACKAGES_FAIL_INSTALL[@]}"
    echo ""
fi

if [ "${#PACKAGES_FAIL_UNINSTALL[@]}" -gt 0 ]; then
    echo "##vso[task.logissue type=error]Error, ${#PACKAGES_FAIL_UNINSTALL[@]} packages failed to uninstall, check logs to see the list"
    echo "Failed installed packages:"
    echo "${PACKAGES_FAIL_UNINSTALL[@]}"
fi

if [[ "${#PACKAGES_FAIL_UNINSTALL[@]}" -gt 0 || "${#PACKAGES_FAIL_INSTALL[@]}" -gt 0 ]]; then
    exit 1
fi
