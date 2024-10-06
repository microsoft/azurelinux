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

## cloud-init-local, cloud-config, cloud-final

These services require write access to certain directories, such as
`/var/lib/cloud`, which conflicts with the read-only nature of the
verity-protected root filesystem.

### Solution: Create a writable persistent partition

To provide the required write access, create a writable persistent partition for
`/var`. This will allow the `cloud-init-local`, `cloud-config`, and
`cloud-final` services to function correctly without issues caused by the
read-only root filesystem.

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

## docker

The `docker.service` requires write access to `/var/lib/docker`, which is
restricted by the read-only root filesystem.

### Solution: Create a writable persistent partition

To unblock `docker.service`, create a writable persistent partition for `/var`.
This allows Docker to write to `/var/lib/docker` without any issues caused by
the read-only root filesystem. 

Refer to the YAML layout under the
[cloud-init](#cloud-init-local-cloud-config-cloud-final) section for the
partition configuration.

## auditd, logrotate

The `auditd.service` and `logrotate.service` need write access to `/var/log` for
logging purposes. However, the root filesystem's read-only nature blocks these
services.

### Solution: Create a writable persistent partition

To unblock `auditd.service` and `logrotate.service`, ensure that `/var` is
mounted as a writable persistent partition, allowing write access to `/var/log`.

Refer to the YAML layout under the
[cloud-init](#cloud-init-local-cloud-config-cloud-final) section for the
partition configuration.

## sshd

The `sshd` service requires write access to the SSH host keys, which by default
are stored in `/etc/ssh`. However, with the root filesystem being read-only,
this prevents `sshd` from running correctly.

### Solution: Create a writable persistent partition and redirect SSH host keys

To resolve this, create a writable partition for `/var` and redirect the SSH
host keys from `/etc` to `/var`. This ensures that `sshd` can write and access
the necessary keys without encountering issues due to the read-only root
filesystem.

Refer to the YAML layout under the
[cloud-init](#cloud-init-local-cloud-config-cloud-final) section for the
partition configuration.

The following example script can be added to the `postCustomization` scripts to
automatically move the SSH host keys and update the `sshd_config` file:

```bash
# Move the SSH host keys off the read-only /etc directory, so that sshd can run.
SSH_VAR_DIR="/var/etc/ssh/"
mkdir -p "$SSH_VAR_DIR"
cat << EOF >> /etc/ssh/sshd_config
HostKey $SSH_VAR_DIR/ssh_host_rsa_key
HostKey $SSH_VAR_DIR/ssh_host_ecdsa_key
HostKey $SSH_VAR_DIR/ssh_host_ed25519_key
EOF
```
