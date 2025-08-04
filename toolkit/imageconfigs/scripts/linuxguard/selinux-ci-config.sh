#!/bin/bash

# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

set -eux

# import SELinux policy CI customizations.  This is installed by MIC
semanage import -f /etc/selinux/targeted/selinux-ci.semanage

# MIC expects customization scripts to be bash scripts.
python_script=$(cat << EOF
#!/usr/bin/python3

#
# Module disabling done by script instead of 'semanage import' so new
# modules are disabled by default
#

from semanage import (semanage_module_key_create,
                      semanage_module_key_set_name,
                      semanage_module_set_enabled)
import seobject

ENABLED_MODULES: set[str] = {
    "base",
    "application",
    "authlogin",
    "azureci",
    "azureci_deletions",
    "bootloader",
    "brctl",
    "clock",
    "cloudinit",
    "container",
    "container_compat",
    "crio",
    "cron",
    "chronyd",
    "dbus",
    "dmesg",
    "docker", # handles docker and containerd
    "fstools",
    "getty",
    "gpg",
    "hostname",
    "hotfix",
    "hypervkvp",
    "init", # systemd
    "iptables",
    "irqbalance",
    "kerberos",
    "kdump",
    "kubernetes",
    "locallogin",
    "logging",
    "libraries",
    "logrotate",
    "lvm", # includes dm, cryptsetup, etc.
    "miscfiles",
    "modutils",
    "mount",
    "mta",
    "netlabel",
    "netutils",
    "ntp",
    "oddjob",
    "openvswitch",
    "podman", # there is a hard dependency for this in crio
    "policykit",
    "qemu",
    "rdisc",
    "rngd",
    "rpm",
    "sasl",
    "selinuxutil",
    "setrans",
    "setroubleshoot",
    "shutdown",
    "slocate",
    "ssh",
    "su",
    "sudo",
    "sysnetwork",
    "systemd",
    "tpm2",
    "trident",
    "udev",
    "userdomain",
    "usermanage",
    "uuidd",
    "virt",
    "xdg", # required by systemd
}

records = seobject.moduleRecords()
handle = records.get_handle("targeted")

# name, disabled, priority, hll name
modules: set[str] = set(name for name, _, _, _ in records.get_all())
modules_to_disable: set[str] = modules - ENABLED_MODULES
modules_to_enable: set[str] = modules - modules_to_disable
missing_modules: set[str] = ENABLED_MODULES - modules

for name in modules_to_disable:
    rc, key = semanage_module_key_create(handle)
    if rc < 0:
        raise RuntimeError(f"Failed to create module key for {name}")

    semanage_module_key_set_name(handle, key, name)
    semanage_module_set_enabled(handle, key, 0)

if missing_modules:
    print(f"Warning: missing modules from enabling list: {', '.join(missing_modules)}")

# if this script is re-ran with a new enabled module, this is needed
for name in modules_to_enable:
    rc, key = semanage_module_key_create(handle)
    if rc < 0:
        raise RuntimeError(f"Failed to create module key for {name}")

    semanage_module_key_set_name(handle, key, name)
    semanage_module_set_enabled(handle, key, 1)

records.commit()
EOF
)

/usr/bin/python3 -c "$python_script"

# Move policy to /usr
if [ ! -d /usr/etc/selinux ]; then
    mkdir -p /usr/etc
    mv /etc/selinux /usr/etc/selinux
    # add backwards compatibility for /etc/selinux
    ln -sf ../usr/etc/selinux /etc/selinux
fi
