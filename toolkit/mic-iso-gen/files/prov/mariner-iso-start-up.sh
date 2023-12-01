#!/bin/bash

# Use a custom termcap for the Mariner installer in an ISO environment
# for a high contrast cursor. This is based on the "linux" termcap.
export TERMINFO=/usr/lib/mariner/terminfo
export TERM=mariner-installer

echo "Running mariner-iso-start-up script v231130-1811."

function wait_for_mount {
    local mount_point="$1"
    for i in {1..60}; do # Wait up to 60 seconds
        if mountpoint -q "$mount_point"; then
            echo "$mount_point has been mounted."
            return
        fi
        sleep 1s # Check every second
    done
    echo "Error: $mount_point was not mounted after waiting 60 seconds."
    exit 1
}

function run_user_script {
    local iso_media_mount_dir=$1

    iso_custom_installer_script=$iso_media_mount_dir/artifacts/iso-custom-installer.sh
    echo "Searching for $iso_custom_installer_script..."
    if [[ -f $iso_custom_installer_script ]]; then
        echo "Found."
        echo "-------------------------------------------------------------------------------"
        source $iso_custom_installer_script
        return
    fi

    iso_image_installer=$iso_media_mount_dir/artifacts/iso-image-installer.sh
    echo "Searching for $iso_image_installer..."
    if [[ -f $iso_image_installer ]]; then
        echo "Found."
        echo "-------------------------------------------------------------------------------"
        source $iso_image_installer
        return
    fi

    echo "No user scripts found."
    /bin/bash
}

function mount_iso_media () {
    local iso_media_label=$1
    local iso_media_mount_dir=$2

    # Find the iso media device (retry because it might not be online)
    iso_media_device=
    while [[ -z $iso_media_device ]]
    do
        echo "Searching for block device with $iso_media_label label..."
        iso_media_device=$(blkid | grep $iso_media_label | cut -d : -f 1)
        sleep 1s # Check every second
    done

    echo "Boot media found at:" $iso_media_device
    echo "Mounting block device at $iso_media_mount_dir..."
    mkdir -p $iso_media_mount_dir
    mount $iso_media_device $iso_media_mount_dir
    wait_for_mount "$iso_media_mount_dir"
}

#------------------------------------------------------------------------------
# main()

iso_media_label="baremetal-iso"
iso_media_mount_dir=/mnt/baremetal-iso

mount_iso_media $iso_media_label $iso_media_mount_dir
run_user_script $iso_media_mount_dir
