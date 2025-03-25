# AMD Repository Configuration

## Overview
The following documentation describes how to access Azure Linux packages from the AMD RPM repository at [packages.microsoft.com](https://packages.microsoft.com/azurelinux/3.0/prod/amd/)

## Instructions
The following instructions register the amd package store with the package manager and install the amdgpu package.
```ls
sudo tdnf install -y azurelinux-repos-amd
sudo tdnf repolist --refresh
sudo tdnf install -y amdgpu
```

## Notes
1. Packages earlier than March 2025 (amdgpu-6.10.5.60302_2109964-1_6.6.78.1.3.azl3.x86_64.rpm) require an additional step `sudo modprobe amdgpu` or reboot to load the kernel modules.
1. Installing for an older kernel may require the version, for example: `sudo tdnf install amdgpu-6.8.5.60202_2078359`.
