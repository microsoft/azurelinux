---
layout: post
title:  "Introducing CBL-Mariner"
date:   2021-08-14 17:33:52 -0900
categories: Mariner
---

Mariner or more exactly CBL-Mariner where CBL stands for *Common Base Linux*, is a Linux distribution created by Microsoft's Linux System Group which is the same team at Microsoft which created the [Linux kernel used for Windows Subsystem for Linux version 2](https://github.com/microsoft/WSL2-Linux-Kernel), or WSL2. The goal of Mariner is to be used as an internal Linux distribution for Microsoft’s engineering teams to build cloud infrastructure and edge products and services. 

Of course Mariner is open source and it has its own repo under [Microsoft's GitHub](https://github.com/microsoft/CBL-Mariner) organization. No ISOs or images of Mariner are provided, however the repo has instructions to build them on Ubuntu 18.04. There are a series of prerequisites listed in this [GitHub page](https://github.com/microsoft/CBL-Mariner/blob/1.0/toolkit/docs/building/prerequisites.md) that roughly include Docker, RPM tools, ISO build tools and Golang, amongst others. 

The build process for an ISO is very straightforward, it relays on pre-compiled RPM packages from [CBL-Mariner package repository](https://github.com/microsoft/CBL-Mariner/blob/1.0/toolkit/docs/building/prerequisites.md). Since I wanted to install Mariner on my vSphere 7 homelab I choose to create the ISO.

```
git clone https://github.com/microsoft/CBL-Mariner.git
cd CBL-Mariner/toolkit
sudo make iso REBUILD_TOOLS=y REBUILD_PACKAGES=n CONFIG_FILE=./imageconfigs/full.json
```
