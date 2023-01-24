#!/bin/sh

# args
dir="$1"

# cfg
shell="$dir/Shell.efi"
enroll="$dir/EnrollDefaultKeys.efi"
root="$dir/image"
vfat="$dir/shell.img"
iso="$dir/UefiShell.iso"

# create non-partitioned (1.44 MB floppy disk) FAT image
mkdir "$root"
mkdir "$root"/efi
mkdir "$root"/efi/boot
cp "$shell" "$root"/efi/boot/bootx64.efi
cp "$enroll" "$root"
qemu-img convert --image-opts \
	driver=vvfat,floppy=on,fat-type=12,label=UEFI_SHELL,dir="$root/" \
	$vfat

# build ISO with FAT image file as El Torito EFI boot image
genisoimage -input-charset ASCII -J -rational-rock \
	-efi-boot "${vfat##*/}" -no-emul-boot -o "$iso" -- "$vfat"
rm -rf "$root/" "$vfat"
