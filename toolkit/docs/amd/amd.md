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
