#!/bin/bash
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

# $1 path to create worker base
# $2 path to text file containing the worker core packages
# $3 path to find RPMs. May be in PATH/<arch>/*.rpm
# $4 path to log directory

[ -n "$1" ] && [ -n "$2" ] && [ -n "$3" ] && [ -n "$4" ] && [ -n "$5" ] && [ -n "$6" ] || { echo "Usage: create_worker.sh <./worker_base_folder> <rpms_to_install.txt> <./path_to_rpms> <./log_dir> <./bldtracker> <./timestamp_output_directory>"; exit; }

chroot_base=$1
packages=$2
rpm_path=$3
log_path=$4
bldtracker=$5
timestamp_dir=$6

chroot_name="worker_chroot"
script_name="$(basename $0)"
chroot_builder_folder=$chroot_base/$chroot_name
chroot_archive=$chroot_base/$chroot_name.tar.gz
chroot_log="$log_path"/$chroot_name.log

$bldtracker \
    --script-name=script_name \
    --step-name="start running the script" \
    --dir-path="$timestamp_dir" \
    --log-file="$chroot_log" \
    --mode="i"

install_one_toolchain_rpm () {
    error_msg_tail="Inspect $chroot_log for more info. Did you hydrate the toolchain?"

    echo "Adding RPM to worker chroot: $1." | tee -a "$chroot_log"

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

record_timestamp () {
    $bldtracker \
        --script-name=script_name \
        --step-name="$1" \
        --dir-path="$timestamp_dir" \
        --log-file="$chroot_log" \
        --mode="r"
}

rm -rf "$chroot_builder_folder"
rm -f "$chroot_archive"
rm -f "$chroot_log"
mkdir -p "$chroot_builder_folder"
mkdir -p "$log_path"

ORIGINAL_HOME=$HOME
HOME=/root

record_timestamp "start adding RPMs to worker chroot"

while read -r package || [ -n "$package" ]; do
    install_one_toolchain_rpm "$package"
done < "$packages"

record_timestamp "finish adding RPMs to worker chroot"

record_timestamp "start adding RPM DB entries"

TEMP_DB_PATH=/temp_db
echo "Setting up a clean RPM database before the Berkeley DB -> SQLite conversion under '$TEMP_DB_PATH'." | tee -a "$chroot_log"
chroot "$chroot_builder_folder" mkdir -p "$TEMP_DB_PATH"
chroot "$chroot_builder_folder" rpm --initdb --dbpath="$TEMP_DB_PATH"

# Popularing the SQLite database with package info.
while read -r package || [ -n "$package" ]; do
    full_rpm_path=$(find "$rpm_path" -name "$package" -type f 2>>"$chroot_log")
    cp $full_rpm_path $chroot_builder_folder/$package

    echo "Adding RPM DB entry to worker chroot: $package." | tee -a "$chroot_log"

    chroot "$chroot_builder_folder" rpm -i -v --nodeps --noorder --force --dbpath="$TEMP_DB_PATH" --justdb "$package" &>> "$chroot_log"
    chroot "$chroot_builder_folder" rm $package
done < "$packages"

record_timestamp "finish adding RPM DB entries"

record_timestamp "start overwriting old RPM database"

echo "Overwriting old RPM database with the results of the conversion." | tee -a "$chroot_log"
chroot "$chroot_builder_folder" rm -rf /var/lib/rpm
chroot "$chroot_builder_folder" mv "$TEMP_DB_PATH" /var/lib/rpm

record_timestamp "finish overwriting old RPM database"

record_timestamp "start importing GPG keys"

echo "Importing CBL-Mariner GPG keys." | tee -a "$chroot_log"
for gpg_key in $(chroot "$chroot_builder_folder" rpm -q -l mariner-repos-shared | grep "rpm-gpg")
do
    echo "Importing GPG key: $gpg_key" | tee -a "$chroot_log"
    chroot "$chroot_builder_folder" rpm --import "$gpg_key"
done

record_timestamp "finish importing GPG keys"

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

record_timestamp "done installing all packages"

record_timestamp "start packing the chroot"

if command -v pigz &>/dev/null ; then
    tar -I pigz -cvf "$chroot_archive" -C "$chroot_base/$chroot_name" . >> "$chroot_log"
else
    tar -I gzip -cvf "$chroot_archive" -C "$chroot_base/$chroot_name" . >> "$chroot_log"
fi
echo "Done creating $chroot_archive." | tee -a "$chroot_log"

record_timestamp "done packing the chroot"

