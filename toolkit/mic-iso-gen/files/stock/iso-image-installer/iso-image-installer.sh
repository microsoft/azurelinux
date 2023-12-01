#!/bin/bash

echo "Running iso-image-installer.sh v231201-1145."

image_file_path=$(cat $iso_media_mount_dir/artifacts/host-configuration.json | jq -r '.imaging.images[0].url')
image_target_device=$(cat $iso_media_mount_dir/artifacts/host-configuration.json | jq -r '.storage.disks[0].device')

echo "Installing $image_file_path to $image_target_device..."
dd if=$image_file_path of=$image_target_device bs=4M

# Copy file to the rootfs
#
# rootfs_target_partition=${image_target_device}2
# rootfs_mount_dir=/mnt/sda2
# mkdir -p $rootfs_mount_dir
# mount $rootfs_target_partition $rootfs_mount_dir
# cp $iso_media_mount_dir/artifacts/host-configuration.yaml $rootfs_mount_dir/etc/
# sleep 1s
# umount $rootfs_target_partition

echo "Ejecting the CD-ROM..."
umount /dev/cdrom
eject /dev/cdrom

# echo "Rebooting..."
echo "Sleeping for 5 seconds before rebooting..."
sleep 5s
reboot
# /bin/bash
