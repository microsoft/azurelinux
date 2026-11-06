#!/bin/bash
# KIWI config.sh hook for the bootc-base profile (invoked by /image/config.sh).
#
# The package set alone is not a valid bootc image: `bootc container lint`
# rejects it, and `bootc install` expects a layout that rpm-ostree normally
# produces when it composes an image. This script applies the subset of that
# layout that is needed here, on top of the root tree kiwi has just populated.

set -euo pipefail

# bootc ships a reference layout (/sysroot, /ostree, composefs enabled in
# prepare-root.conf, and a kernel-install config that leaves the initramfs to
# us). Apply it verbatim rather than re-creating it here.
baseimage=/usr/share/doc/bootc/baseimage
cp -a "${baseimage}/base/." /
cp -a "${baseimage}/systemd/." /

# The reference dracut config (generic initramfs with the ostree and bootc
# modules) ships in /usr/lib/dracut.conf.d, which the dracut in this
# distribution does not read. Install it where dracut does look, so it also
# applies when a derived image rebuilds the initramfs after a kernel update.
install -D -m 0644 "${baseimage}/dracut/usr/lib/dracut.conf.d/10-bootc-base.conf" \
    /usr/lib/dracut/dracut.conf.d/10-bootc-base.conf

# bootc requires exactly one kernel, with its initramfs next to it under
# /usr/lib/modules/<kver>/. The kernel package already installs vmlinuz there;
# the initramfs that kernel-install wrote to /boot is a host-specific one
# without the ostree and bootc modules, so build the real one now.
kernels=(/usr/lib/modules/*/)
if [[ ${#kernels[@]} -ne 1 ]]; then
    echo "error: bootc images need exactly one kernel, found ${#kernels[@]}" >&2
    exit 1
fi
kver=$(basename "${kernels[0]}")
dracut --force --reproducible --kver "${kver}" "/usr/lib/modules/${kver}/initramfs.img"

# bootupd installs the bootloader that `bootc install` writes to disk, and
# updates it later. It reads the loader files from /usr/lib/ostree-boot/efi,
# maps each one to its package with `rpm -qf` on the /boot/efi path, and stores
# the payload under /usr/lib/efi. So /boot/efi has to stay in place until the
# metadata is generated.
mkdir -p /usr/lib/ostree-boot
cp -a /boot/efi /usr/lib/ostree-boot/efi
bootupctl backend generate-update-metadata
rm -rf /usr/lib/ostree-boot

# /boot belongs to the installed system: bootc populates it at install time.
find /boot -mindepth 1 -delete

# The deployment root is read-only, so home directories and service data need
# a writable home. Point them into /var, where ostree keeps persistent state.
# /opt and /usr/local stay regular directories, which is what the bootc
# filesystem guidance recommends for base images.
#
# systemd's home.conf and provision.conf expect /home, /srv and /root to be
# directories and log an error for each of them at every boot. Declare the
# symlinks in a file that sorts before those: tmpfiles.d keeps the first line
# for a path and only notes the later duplicates.
tmpfiles=/usr/lib/tmpfiles.d/azurelinux-bootc.conf
: > "${tmpfiles}"
for dir in home:home root:roothome srv:srv mnt:mnt; do
    path=${dir%%:*}
    target=${dir##*:}
    mv "/${path}" "/var/${target}"
    ln -s "var/${target}" "/${path}"
    echo "L /${path} - - - - var/${target}" >> "${tmpfiles}"
done

# Package manager leftovers. Only dnf's own paths are removed: kiwi keeps its
# shared cache under /var/cache/kiwi while this script runs.
rm -rf /var/cache/libdnf5 /var/log/dnf5.log*

# Fail the build here, rather than at `bootc install` time, if the result is
# not a valid bootc image.
bootc container lint
