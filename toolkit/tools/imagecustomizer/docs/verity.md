# Verity Filesystem Layout Recommendations

This document provides recommendations for the Verity-enabled Azure Linux OS
filesystem.

## Filesystem

Below is a list of paths in the Azure Linux OS image filesystem, along with
their properties and recommended usage:

| Path      | Properties                                 | Purpose                                                                                             |
|-----------|--------------------------------------------|-----------------------------------------------------------------------------------------------------|
| /         | • read-only<br>• executable                | The Verity-enabled root filesystem is always mounted as read-only.<br>Its root hash and hash tree are computed at build time and verified by systemd during the initramfs phase on each boot. |
| /boot/efi | • writable<br>• executable<br>• persistent | The EFI System Partition (ESP) is required for booting UEFI-based systems and stores the bootloader and related files. |
| /boot     | • writable<br>• executable<br>• persistent | The `/boot` partition holds the kernel, initramfs, and other files required for booting the system. |
| /var      | • writable<br>• executable<br>• persistent | The `/var` directory contains files that are modified by various services during system operation. It provides a writable space for these services to function properly.<br> - **/var/lib**: Unblocks `systemd-networkd.service`, `accounts-daemon.service`.<br> - **/var/lib/cloud**: Unblocks `cloud-init-local.service`, `cloud-config.service`, `cloud-final.service`.<br> - **/var/lib/docker**: Unblocks `docker.service`.<br> - **/var/log**: Unblocks `auditd.service`, `logrotate.service`. |
