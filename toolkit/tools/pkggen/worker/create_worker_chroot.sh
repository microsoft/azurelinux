#!/bin/bash
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

set -e
set -o pipefail

# $1 path to create worker base
# $2 path to text file containing the worker core packages
# $3 path to find RPMs. May be in PATH/<arch>/*.rpm
# $4 path to log directory

[ -n "$1" ] && [ -n "$2" ] && [ -n "$3" ] && [ -n "$4" ] || { echo "Usage: create_worker.sh <./worker_base_folder> <rpms_to_install.txt> <./path_to_rpms> <./log_dir>"; exit; }

chroot_base=$1
packages=$2
rpm_path=$3
log_path=$4

chroot_name="worker_chroot"
chroot_builder_folder=$chroot_base/$chroot_name
chroot_archive=$chroot_base/$chroot_name.tar.gz
chroot_log="$log_path"/$chroot_name.log

# We have two major steps per entry in the packages file: install the RPM, then add to database
total_steps=$(wc -l < "$packages")
total_steps=$((total_steps * 2))
current_step=0
# Print "<progress>%" and increment current_step
function increment_progress() {
    # Increment global counter current_step
    current_step=$((current_step + 1))
}
function format_progress() {
    progress=$((current_step * 100 / total_steps))
    printf "%s%%" "$progress"
}

install_one_toolchain_rpm () {
    error_msg_tail="Inspect $chroot_log for more info. Did you hydrate the toolchain?"

    echo "Adding RPM to worker chroot $(format_progress): $1." | tee -a "$chroot_log"
    increment_progress

    full_rpm_path=$(find "$rpm_path" -name "$1" -type f 2>>"$chroot_log")
    if [ ! $? -eq 0 ] || [ -z "$full_rpm_path" ]
    then
        echo "Failed to locate package $1 in ($rpm_path), aborting. $error_msg_tail" | tee -a "$chroot_log"
        exit 1
    fi

    echo "Found full path for package $1 in $rpm_path: ($full_rpm_path)" >> "$chroot_log"
    rpm -i -v --nodeps --noorder --force --root "$chroot_builder_folder" --define '_dbpath /var/lib/rpm' "$full_rpm_path" &>> "$chroot_log"

    if [ ! $? -eq 0 ]
    then
        echo "Elevated install failed for package $1, aborting. $error_msg_tail" | tee -a "$chroot_log"
        exit 1
    fi
}

rm -rf "$chroot_builder_folder"
rm -f "$chroot_archive"
rm -f "$chroot_log"
mkdir -p "$chroot_builder_folder"
mkdir -p "$log_path"

ORIGINAL_HOME=$HOME
HOME=/root

# These nodes are required in the chroot for certain tools (most importantly, gpg key import when installing 'mariner-repos-shared' package)
# This is also required to check the rpm db version to see if rebuilding the db is necessary
mkdir -pv $chroot_builder_folder/dev
mknod -m 600 $chroot_builder_folder/dev/console c 5 1
mknod -m 666 $chroot_builder_folder/dev/null c 1 3
mknod -m 444 $chroot_builder_folder/dev/urandom c 1 9

while read -r package || [ -n "$package" ]; do
    install_one_toolchain_rpm "$package"
done < "$packages"

# If the host machine rpm version is >= 4.16 (such as Mariner 2.0), it will create an "sqlite" rpm database backend incompatible with Mariner 1.0 (which uses "bdb")
# To resolve this, enter the 1.0 chroot after the packages are installed, and use the older rpm tool in the chroot to re-create the database in "bdb" format.
HOST_RPM_VERSION="$(rpm --version)"
HOST_RPM_DB_BACKEND="$(rpm -E '%{_db_backend}')"
GUEST_RPM_VERSION="$(chroot "$chroot_builder_folder" rpm --version)"
GUEST_RPM_DB_BACKEND="$(chroot "$chroot_builder_folder" rpm -E '%{_db_backend}')"
echo "Current host '$HOST_RPM_VERSION' with rpm db '$HOST_RPM_DB_BACKEND', guest has '$GUEST_RPM_VERSION' with rpm db '$GUEST_RPM_DB_BACKEND'" | tee -a "$chroot_log"

if [[ "$HOST_RPM_DB_BACKEND" == "$GUEST_RPM_DB_BACKEND" ]]; then
    echo "The host rpm db '$HOST_RPM_DB_BACKEND' matches the guest. Not rebuilding the database." | tee -a "$chroot_log"
else
    echo "The host rpm db ('$HOST_RPM_DB_BACKEND') differs from the guest ('$GUEST_RPM_DB_BACKEND'). Rebuilding database for compatibility" | tee -a "$chroot_log"
    TEMP_DB_PATH="/temp_db"
    chroot "$chroot_builder_folder" mkdir -p "$TEMP_DB_PATH"
    chroot "$chroot_builder_folder" rpm --initdb --dbpath="$TEMP_DB_PATH"
    # Populating the SQLite database with package info.
    while read -r package || [ -n "$package" ]; do
        full_rpm_path=$(find "$rpm_path" -name "$package" -type f 2>>"$chroot_log")
        cp $full_rpm_path $chroot_builder_folder/$package
        echo "Adding RPM DB entry to worker chroot $(format_progress): $package." | tee -a "$chroot_log"
        increment_progress
        chroot "$chroot_builder_folder" rpm -i -v --nodeps --noorder --force --dbpath="$TEMP_DB_PATH" --justdb "$package" &>> "$chroot_log"
        chroot "$chroot_builder_folder" rm $package
    done < "$packages"
    echo "Overwriting old RPM database with the results of the conversion." | tee -a "$chroot_log"
    chroot "$chroot_builder_folder" rm -rf /var/lib/rpm
    chroot "$chroot_builder_folder" mv "$TEMP_DB_PATH" /var/lib/rpm
fi

echo "Importing CBL-Mariner GPG keys." | tee -a "$chroot_log"
for gpg_key in $(chroot "$chroot_builder_folder" rpm -q -l mariner-repos-shared | grep "rpm-gpg")
do
    echo "Importing GPG key: $gpg_key" | tee -a "$chroot_log"
    chroot "$chroot_builder_folder" rpm --import "$gpg_key"
done

HOME=$ORIGINAL_HOME

# In case of Docker based build do not add the below folders into chroot tarball
# otherwise safechroot will fail to "untar" the tarball
DOCKERCONTAINERONLY=/.dockerenv
if [[ -f "$DOCKERCONTAINERONLY" ]]; then
    rm -rf "${chroot_base:?}/$chroot_name"/dev
    rm -rf "${chroot_base:?}/$chroot_name"/proc
    rm -rf "${chroot_base:?}/$chroot_name"/run
    rm -rf "${chroot_base:?}/$chroot_name"/sys
fi

echo "Done installing all packages, creating $chroot_archive." | tee -a "$chroot_log"
if command -v pigz &>/dev/null ; then
    tar --warning='no-file-ignored' -I pigz -cvf "$chroot_archive" -C "$chroot_base/$chroot_name" . >> "$chroot_log"
else
    tar --warning='no-file-ignored' -I gzip -cvf "$chroot_archive" -C "$chroot_base/$chroot_name" . >> "$chroot_log"
fi
echo "Done creating $chroot_archive." | tee -a "$chroot_log"
