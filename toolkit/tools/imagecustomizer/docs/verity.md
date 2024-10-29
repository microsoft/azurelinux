# Verity Image Recommendations

The Verity-enabled root filesystem is always mounted as read-only. Its root hash
and hash tree are computed at build time and verified by systemd during the
initramfs phase on each boot. When enabling the Verity feature, it is
recommended to create a writable persistent partition for any directories that
require write access. Critical files and directories can be redirected to the
writable partition using symlinks or similar methods.

Please also note that some services and programs on Azure Linux may require
specific handling when using Verity. Depending on user needs, there are
different configuration options that offer tradeoffs between convenience and
security. Some configurations can be made flexible to allow changes, while
others may be set as immutable for enhanced security.

## Writable `/var` Partition

Many services  (e.g., auditd, docker, logrotate, etc.) require write access to
the /var directory.

### Solution: Create a Writable Persistent /var Partition

To provide the required write access, create a separate writable partition for
/var. Here is an example of how to define the partitions and filesystems in your
configuration:

```yaml
storage:
  disks:
  - partitionTableType: gpt
    maxSize: 5120M
    partitions:
    - id: boot
      start: 1M
      end: 1024M
    - id: root
      start: 1024M
      end: 3072M
    - id: roothash
      start: 3072M
      end: 3200M
    - id: var
      start: 3200M
  filesystems:
  - deviceId: boot
    type: ext4
    mountPoint:
      path: /boot
  - deviceId: root
    type: ext4
    mountPoint:
      path: /
  - deviceId: var
    type: ext4
    mountPoint:
      path: /var
```

## Network Configuration for Verity Images

In non-verity images, usually user can leverage cloud-init to provide default
networking settings. However, cloud-init fails to provision the network in
verity images since /etc is not writable.

### Solution: Specify Network Settings Manually

For verity images, it's recommended to specify network settings manually. Here
is an example network configuration that can be added to the `additionalFiles`
in your configuration YAML file:

```yaml
os:
  additionalFiles:
  - content: |
      # SPDX-License-Identifier: MIT-0
      #
      # This example config file is installed as part of systemd.
      # It may be freely copied and edited (following the MIT No Attribution license).
      #
      # To use the file, one of the following methods may be used:
      # 1. add a symlink from /etc/systemd/network to the current location of this file,
      # 2. copy the file into /etc/systemd/network or one of the other paths checked
      #    by systemd-networkd and edit it there.
      # This file should not be edited in place, because it'll be overwritten on upgrades.

      # Enable DHCPv4 and DHCPv6 on all physical ethernet links
      [Match]
      Kind=!*
      Type=ether

      [Network]
      DHCP=yes
    destination: /etc/systemd/network/89-ethernet.network
    permissions: "664"
```

## cloud-init

cloud-init has various features to configure the system (e.g., user accounts,
networking, etc.), but many of these require the /etc directory to be writable.
In verity-protected images with a read-only root filesystem, cloud-init cannot
perform these configurations effectively.

### Solution: Disable cloud-init

Given the limitations, the general recommendation is to disable cloud-init in
verity images to prevent potential issues.

```yaml
os:
  services:
    disable:
    - cloud-init
```

## sshd

The `sshd` service requires write access to the SSH host keys, which by default
are stored in `/etc/ssh`. However, with the root filesystem being read-only,
this prevents `sshd` from running correctly.

### Solution: Create a writable persistent partition and redirect SSH host keys

To resolve this, create a writable partition for `/var` and redirect the SSH
host keys from `/etc` to `/var`. This ensures that `sshd` can write and access
the necessary keys without encountering issues due to the read-only root
filesystem.

Example Image Config:

```yaml
storage:
  disks:
  - partitionTableType: gpt
    maxSize: 5120M
    partitions:
    - id: boot
      start: 1M
      end: 1024M
    - id: root
      start: 1024M
      end: 3072M
    - id: roothash
      start: 3072M
      end: 3200M
    - id: var
      start: 3200M
  verity:
  - id: verityroot
    name: root
    dataDeviceId: root
    hashDeviceId: roothash
    corruptionOption: panic
  filesystems:
  - deviceId: boot
    type: ext4
    mountPoint:
      path: /boot
  - deviceId: verityroot
    type: ext4
    mountPoint:
      path: /
  - deviceId: var
    type: ext4
    mountPoint:
      path: /var
os:
  additionalFiles:
    # Change the directory that the sshd-keygen service writes the SSH host keys to.
  - content: |
      [Unit]
      Description=Generate sshd host keys
      ConditionPathExists=|!/var/etc/ssh/ssh_host_rsa_key
      ConditionPathExists=|!/var/etc/ssh/ssh_host_ecdsa_key
      ConditionPathExists=|!/var/etc/ssh/ssh_host_ed25519_key
      Before=sshd.service

      [Service]
      Type=oneshot
      RemainAfterExit=yes
      ExecStart=/usr/bin/ssh-keygen -A -f /var

      [Install]
      WantedBy=multi-user.target
    destination: /usr/lib/systemd/system/sshd-keygen.service
    permissions: "664"
  services:
    enable:
    - sshd
scripts:
  postCustomization:
    # Move the SSH host keys off of the read-only /etc directory, so that sshd can run.
  - content: |
      # Move the SSH host keys off the read-only /etc directory, so that sshd can run.
      SSH_VAR_DIR="/var/etc/ssh/"
      mkdir -p "$SSH_VAR_DIR"

      cat << EOF >> /etc/ssh/sshd_config

      HostKey $SSH_VAR_DIR/ssh_host_rsa_key
      HostKey $SSH_VAR_DIR/ssh_host_ecdsa_key
      HostKey $SSH_VAR_DIR/ssh_host_ed25519_key
      EOF
  name: ssh-move-host-keys.sh
```

## systemd-growfs-root

This service attempts to resize the root filesystem, which fails since verity
makes the root filesystem readonly and a fixed size.

### Solution 1: Do nothing

Since the root filesystem is readonly, the `systemd-growfs-root` service will
fail. However, the only impact will be an error in the boot logs.

### Solution 2: Disable service

Disabling the service removes the error from the boot logs.

```yaml
os:
  services:
    disable:
    - systemd-growfs-root
```
