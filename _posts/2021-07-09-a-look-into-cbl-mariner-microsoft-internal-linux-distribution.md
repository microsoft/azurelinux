---
title: A look into CBL-Mariner, Microsoft's internal Linux distribution
date: 2021-07-09 13:45:00 +0100
type: post
classes: wide
published: true
status: publish
categories:
- Microsoft
- Linux
tags:
- Microsoft
- Azure
- Linux
author: juan_manuel_rey
comments: false
---

Mariner or more exactly CBL-Mariner where CBL stands for *Common Base Linux*, is a Linux distribution created by Microsoft's Linux System Group which is the same team at Microsoft which created the [Linux kernel used for Windows Subsystem for Linux version 2](https://github.com/microsoft/WSL2-Linux-Kernel), or WSL2. The goal of Mariner is to be used as an internal Linux distribution for Microsoft’s engineering teams to build cloud infrastructure and edge products and services. 

Of course Mariner is open source and it has its own repo under [Microsoft's GitHub](https://github.com/microsoft/CBL-Mariner) organization. No ISOs or images of Mariner are provided, however the repo has instructions to build them on Ubuntu 18.04. There are a series of prerequisites listed in this [GitHub page](https://github.com/microsoft/CBL-Mariner/blob/1.0/toolkit/docs/building/prerequisites.md) that roughly include Docker, RPM tools, ISO build tools and Golang, amongst others. 

The build process for an ISO is very straightforward, it relays on pre-compiled RPM packages from [CBL-Mariner package repository](https://github.com/microsoft/CBL-Mariner/blob/1.0/toolkit/docs/building/prerequisites.md). Since I wanted to install Mariner on my vSphere 7 homelab I choose to create the ISO.

```
git clone https://github.com/microsoft/CBL-Mariner.git
cd CBL-Mariner/toolkit
sudo make iso REBUILD_TOOLS=y REBUILD_PACKAGES=n CONFIG_FILE=./imageconfigs/full.json
```

## Installation process

In my vSphere lab I created a couple of new VMs and set the guest OS to `Other 5.x or later Linux (64-bit)`, configure the hardware with 1 vCPU, 2GB of RAM and a 16GB disk. This would be enough for a simple test.

The installation process will give the option to do it in text or graphic mode, I choose graphic one since I was curious if it was based in Fedora's Anaconda or any other.

![]({{site.baseurl}}/assets/images/cbl-mariner-graphic-installer.png)

There are two types of installations:

- Core
- Full

The installation process is very fast in both cases, it took around 29 seconds for the Core and around 76 for the Full one. During the process it will ask you for the typical parameters like user, partitioning, etc.

- Partition configuration

![]({{site.baseurl}}/assets/images/cbl-mariner-partition-config.png)

- System configuration

![]({{site.baseurl}}/assets/images/cbl-mariner-system-install.png)

## CBL-Mariner overview

CBL-Mariner feels very similar to other Linux distros like Fedora or Photon-OS, which is expected since in the [Acknowledgments](https://github.com/microsoft/CBL-Mariner#acknowledgments) section of their GitHub repo they list both projects because the team used their SPEC files as starting point and reference. 

As anyone will expect in any modern Linux distro `systemd` it is used as CBL-Mariner system manager. After installing my Mariner VM I had to access it through vSphere console because there is no SSH daemon installed in the default installation, but it can be easily installed using `tdnf`.

```
sudo tdnf install -y openssh-server
sudo systemctl enable --now sshd.service
```

### Package and update system

CBL-Mariner package system is RPM-based. The package update system uses both `dnf` and `tdnf`, [Tiny DNF](https://github.com/vmware/tdnf) is a package manager based on `dnf` and coming from VMware's Photon OS. 

CBL-Mariner also supports an image-based update mechanism for atomic servicing and rollback using [RPM-OSTree](https://rpm-ostree.readthedocs.io/en/stable/), `rpm-ostree` is an open source tool based on [OSTree](https://ostreedev.github.io/ostree/introduction/) to manage bootable, immutable, versioned filesystem trees. The idea behind rpm-ostree is to use a client-server architecture to keep Linux hosts updated and in sync with the latest packages in a reliable manner.

In terms of software available after the installation there are two package repositories, `base` and `update`, configured in the system. 

```
vadmin@cbl-mariner [ ~ ]$ sudo tdnf repolist
Loaded plugin: tdnfrepogpgcheck
repo id             repo name                               status
mariner-official-baseCBL-Mariner Official Base 1.0 x86_64    enabled
mariner-official-updateCBL-Mariner Official Update 1.0 x86_64  enabled
vadmin@cbl-mariner [ ~ ]$
```
Around 3300 packages are available between both repositories. In my case it was a very pleasant surprise to find `open-vm-tools` package, since I run my CBL-Mariner instances on vSphere is fantastic to have the VMware Tools packages available. 

### Security by default

CBL-Mariner follows the secure-by-default principle, most aspects of the OS have been built with an emphasis on security. It comes with a hardened kernel, signed updates, ASLR, compiler-based hardening and tamper-resistant logs amongst many features.

All Mariner security features are listed in [CBL-Mariner's GitHub repository](https://github.com/microsoft/CBL-Mariner/blob/1.0/toolkit/docs/security/security-features.md). 

I hope this quick overview of CBL-Mariner has been interesting. I encourage you to look at Mariner's GitHub repo and to create your own ISO and/or VHDX images. 

This post is republished from the original with permission.

--Juanma