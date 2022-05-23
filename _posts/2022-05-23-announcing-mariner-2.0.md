---
title: Announcing CBL-Mariner 2.0
date: 2022-05-23
type: post
published: true
status: publish
author: jperrin
comments: false
---

We’re pleased to announce the General Availability of Mariner 2.0, with generational updates to packages and feature improvements to help you build the most performant and secure Azure services and Edge appliances. Thank you to all the component and partner teams around Microsoft who helped make this release successful!
 
With the release of Mariner 2.0, we will have roughly 7000 packages total in the distro across all repositories. Many of the 1.0 packages have been updated to current versions and are available in 2.0. The base and extended 2.0 packages are available on packages.microsoft.com. 
 
## Highlights 

* Languages
  * OpenJDK 11
  * NodeJS 16.14.2 (Upstream LTS series v16)
  * Python 3.9.10 
  * Ruby 3.1.2 (Latest upstream release)
  * Golang 1.17.8 (Released upstream on 2022-03-03)
  * Rust 1.59.0 (Released upstream on 2022-02-24)
  * Glibc 2.35 (Current upstream stable release)

* Core components
  * Systemd 250.3 (Upstream stable release)
  * Kernel 5.15 (Most recent upstream LTS version)
  * Moby-containerd 1.6.1

* RPM Database (Rpmdb)
  * This release also marks the transition of the RPM Database from Berkeley DB to SQLite which provides a more robust database and make use of modern SQLite features.
  * Because of the change in the rpmdb backend, this is considered a breaking change. Please do not attempt to update an existing instance directly from 1.0 to 2.0
 
## Container Images

The Mariner 2.0 base container is reduced to ~67MB. Size reduction of the base image was achieved by removing additional packages and dependencies (e.g., rpm utility). Tdnf is present by default.
 
* Base container
  * mcr.microsoft.com/cbl-mariner/base/core:2.0
* Distroless containers
  * mcr.microsoft.com/cbl-mariner/distroless/base:2.0
  * mcr.microsoft.com/cbl-mariner/distroless/debug:2.0
  * mcr.microsoft.com/cbl-mariner/distroless/minimal:2.0
* App containers
  * NodeJS - mcr.microsoft.com/cbl-mariner/base/nodejs:16
 
## Marketplace VMs
* Gen1: MicrosoftCBLMariner:cbl-mariner:cbl-mariner-2:latest
* Gen2: MicrosoftCBLMariner:cbl-mariner:cbl-mariner-2-gen2:latest
 
# ISO Download
* [https://aka.ms/mariner-2.0-x86_64-iso](https://osrelease.download.prss.microsoft.com/pr/download/Mariner-2.0-x86_64.iso)
 
 
## Kernel Updates
* Mariner 2.0 utilizes the latest Microsoft LSG 5.15 kernel. 5.15 is the latest upstream Long-Term Support (LTS) kernel version, as decided by the upstream Linux kernel release maintainer.
* Mariner 2.0 brings full-featured eBPF support to Mariner, allowing for greater observability, debug for Kubernetes environments, as well as other tooling.
 
 
## Security
* Major package version upgrades, removing any packages that have reached end of life and are no longer being maintained by upstream contributors
* Mariner 2.0 features improved SELinux support, allowing for better MAC security in managed environments.
* Hardening: Built additional packages with RELRO and Stack Canary enabled.
* Mariner 2.0 Kernel: improved security around ebpf: We disabled the bpf interpreter and unprivileged bpfs
 
## Improving developer experience
* Improved developer experience when rebuilding packages by skipping chroot recreation.  Useful to speed up build time when iterating on a package. Can invoked with new “REFRESH_WORKER_CHROOT=n” argument 
 
## Removed Packages
* Python 2
* NodeJS 14
* .NET 5.0 and 3.1.  
 
## New Repository Structure
The Mariner 2.0 release contains several repositories broken out by purpose.

|Repository Name |        Purpose and Intent                                       |
|----------------|-----------------------------------------------------------|
|Base             | Open Source packages released with Mariner 2.0 and their updates. |
|Extended                | Mariner 2.0 packages not considered part of core. Generally, view this as experimental or for development purposes.  |
|Microsoft               | Open Source packages built by other Microsoft teams. |
|NVIDIA                        | Proprietary packages required to support Nvidia hardware and CUDA. |
|Extras          | Mariner 2.0 packages built by Microsoft (either Mariner or other Microsoft teams) considered closed source or have proprietary licensing. |
 


## What does this mean for Mariner 1.0?
Mariner 1.0 will continue to be maintained for approximately 6 months following Mariner 2.0’s GA.
