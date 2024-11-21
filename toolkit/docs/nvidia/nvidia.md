# Nvidia Repository Configuration

## Overview
The following documentation describes how to access Azure Linux packages from the NVIDIA RPM repository at [packages.microsoft.com](https://packages.microsoft.com/azurelinux/3.0/prod/nvidia/)

## Licensing
The software in the NVIDIA RPM repository is subject to the following:

> NVIDIA Software. The software may include components developed and owned by NVIDIA Corporation or its licensors. The use of these components is governed by the NVIDIA end user license agreement located at [https://www.nvidia.com/content/DriverDownload-March2009/licence.php?lang=us](https://www.nvidia.com/content/DriverDownload-March2009/licence.php?lang=us). 

## Instructions
The following instructions register the nvidia package store with the package manager.
```ls
# Navigate to the package manager configuration file directory
cd /etc/yum.repos.d

# Copy the configuration to your directory to register the NVIDIA RPM repository with your package manager
sudo wget https://raw.githubusercontent.com/microsoft/Azure Linux/2.0/toolkit/docs/nvidia/mariner-nvidia.repo
```
