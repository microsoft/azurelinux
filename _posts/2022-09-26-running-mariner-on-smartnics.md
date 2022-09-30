---
title: Running Mariner on SmartNICs
date: 2022-09-26
type: post
published: true
status: publish
author: Rachel
comments: false
---

We are excited to share the new CBL-Mariner based repository for SmartNICs, [CBL-Mariner-SmartNIC](https://github.com/microsoft/CBL-Mariner-SmartNIC).

 
## A Brief Background on SmartNICs 

Smart Network Interface Cards(SmartNICs), also known as DPUs or IPUs, vary between vendors, but in general what makes SmartNICs "Smart" is that they have CPU core complex that will run its own OS separate from the host system. The CPU can be in the form of a DPU and can be used to offload and/or accelerate key functions and stacks from the host. In the case of networking, this includes the packet processing and filtering, virtualization, load balancing, and data path optimization. These features allow SmartNICs to offload networking tasks from the host CPU, therefore acclerating networking and improving security. The SmartNIC also enables users to extend network policy rules to Single Root I/O Virtualization (SR-IOV) through Generic Flow Table (GFT) offload.


## CBL-Mariner-SmartNIC Overview

CBL-Mariner has released the CBL-Mariner-SmartNIC repository to enable users to use CBL-Mariner as the operating system running on their SmartNIC.

The goal of the repository is to provide configurations and instructions for producing CBL-Mariner images for SmartNICs. These images are composed of CBL-Mariner RPMs crafted with sources pulled from various open-source projects needed to support networking features. Once flashed onto the device, these images can perform SmartNIC networking functions and be serviced through updates to both the firmware and OS.  

Currently this repository supports the creation of BlueField bootstream (BFBs) files which are part of the [NVIDIA DOCA software framework](https://developer.nvidia.com/networking/doca)  for [NVIDIA BlueField DPUs](https://www.nvidia.com/en-us/networking/products/data-processing-unit/).

Key Features of the repository include:

 * Integration with [NVIDIA DOCA BFB](https://github.com/microsoft/CBL-Mariner-SmartNIC/blob/main/create_bfb)
 * New set of supported rpms containing network features
 * [Instructions for generating bfbs](https://github.com/microsoft/CBL-Mariner-SmartNIC/blob/main/README.md)

## Integration with NVIDIA DOCA BFB tools

NVIDIA DOCA software framework uses images called BFBs to flash the BlueField DPU. These BFBs contain the firmware (ATF+UEFI), bootloaders (SHIM+GRUB), and CBL-Mariner OS.


![BFB image Layout and Boot Flow diagram](/CBL-Mariner/assets/images/bfb-flow.png)


NVIDIA maintains a set of BFB tools used to create BFB images: [github.com/Mellanox/bfb-build](https://github.com/Mellanox/bfb-build) (generic) and [github.com/Mellanox/bfb-mariner](https://github.com/Mellanox/bfb-mariner) (for Mariner 2.0) and is coordinating with CBL-Mariner developers to integrate these tools with CBL-Mariner on the CBL-Mariner-SmartNIC repository. 

These tools utilize the CBL-Mariner ARM64 container. A Dockerfile first creates the container and installs the needed DPURPMs. Create-bfb then constructs the BFB by establishing the grub configs, initial systemd scripts, rebuilding the initramfs, creating a workspace with the kernel, firmware and initramfs, and then calling the mlx-mkbfb tool. Mlx-mkbfb packages everything in the workspace as a bfb.


## New set of supported RPMs containing networking features

To support all the BlueField DPU networking features, Mariner is adding more RPMs to its core set of packages. These packages will contain DOCA drivers and tools needed by the SmartNIC and can be found on Microsoft's official package repo on packages.microsoft.com. As with all CBL-Mariner RPMs, they will enter the CVE monitoring and update flow.

## Instructions on generating BFBs

To build a BFB, all you need to do is clone the repository and run sudo ./bfb-build . There is tooling present to rebuild the modules to match the kernel version within the container. If rebuilding the modules is needed, the build takes around 4.5 hours. If not rebuilding the modules, the build will take around 1 hour. 


## Future Improvements

This is an active repository so potential future improvements include adding more customizability for which RPMs are included in the BFB, using CBL-Mariner’s given grub configs so that features such as kernel lockdown are enabled by default and enabling Secure boot for extra security. If you have any suggestions or run across issues, please file them on the CBL-Mariner-SmartNIC issues page.

To get started, simply run the following command on your Linux machine:

```
git clone https://github.com/microsoft/CBL-Mariner-SmartNIC.git
cd CBL-Mariner-SmartNIC
sudo ./bfb-build
```
