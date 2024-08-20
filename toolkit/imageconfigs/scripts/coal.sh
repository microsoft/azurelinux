#!/bin/bash
set -xe

# Ensure data partition is mounted in initrd along with overlay
# sed -i "s/data ext4 defaults/data ext4 defaults,x-initrd.mount,x-systemd.growfs/" /etc/fstab
# echo "overlay /etc overlay noauto,x-systemd.automount,lowerdir=/sysroot/etc,upperdir=/sysroot/data/overlays/etc/upper,workdir=/sysroot/data/overlays/etc/work 0 0" >> /etc/fstab
# echo "overlay /home overlay noauto,x-systemd.automount,lowerdir=/sysroot/home,upperdir=/sysroot/data/overlays/home/upper,workdir=/sysroot/data/overlays/home/work 0 0" >> /etc/fstab
# echo "overlay /var overlay noauto,x-systemd.automount,lowerdir=/sysroot/var,upperdir=/sysroot/data/overlays/var/upper,workdir=/sysroot/data/overlays/var/work 0 0" >> /etc/fstab
# echo "overlay /root overlay noauto,x-systemd.automount,lowerdir=/sysroot/root,upperdir=/sysroot/data/overlays/root/upper,workdir=/sysroot/data/overlays/root/work 0 0" >> /etc/fstab
# echo "/data/containerd /var/lib/containerd none bind 0 0" >> /etc/fstab

# UKI logic

# maybe symlink /boot/efi to ../
cp -a /boot/efi/. /efi
rm -rf /boot/efi
ln -s ../efi /boot/efi

# The shim has its default boot-loader filename built in as grubx64.efi.
# To switch to systemd-boot, we overwrite that file location with the
# sd-boot EFI binary as a workaround.
cp /lib/systemd/boot/efi/systemd-bootx64.efi /efi/EFI/BOOT/grubx64.efi

# remove DPS partitions from /etc/fstab file
# sed -i '/\/ ext4/d' /etc/fstab
# sed -i '/\/efi vfat/d' /etc/fstab
# echo "" > /etc/fstab

KERNEL_VERSION=""
get_kernel_version() {
    kernel_modules_dir="/usr/lib/modules"
    KERNEL_VERSION="$(ls $kernel_modules_dir)"
}

mkdir -p /efi/EFI/Linux
get_kernel_version
echo "Kernel version = $KERNEL_VERSION"
cp /lib/modules/$KERNEL_VERSION/vmlinuz-uki.efi /efi/EFI/Linux/vmlinuz-uki-$KERNEL_VERSION.efi

systemd-repart

sgdisk -A 2:show:60 /dev/sda
# END UKI Logic