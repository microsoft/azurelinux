# Supported Variants

This document provides an overview of the supported variants for Azure Linux and
explains their primary use cases. Each variant is optimized for a specific
environment, with configurations tailored to ensure performance, compatibility,
and feature support in its intended deployment context.

## 1. Baremetal

**Variant Configuration File**: `baremetal.yaml`

### Description:
The `baremetal` variant is designed to run directly on physical hardware. It
includes the necessary drivers and configurations for initializing hardware
components like RAID controllers, making it ideal for environments where direct
hardware access is required, such as enterprise servers and data centers.

## 2. QEMU Guest

**Variant Configuration File**: `qemu-guest.yaml`

### Description:
The `qemu-guest` variant is optimized for virtual machines running in
**QEMU/KVM** environments. It includes specific packages that enhance guest-host
communication and optimize performance for virtualized hardware.

## 3. Hyper-V Guest

**Variant Configuration File**: `hyperv-guest.yaml`

### Description:
The `hyperv-guest` variant is specifically designed for virtual machines running
in **Hyper-V** environments, such as **Microsoft Azure**. It includes drivers
and daemons to optimize performance and communication between the guest VM and
the Hyper-V hypervisor.


## 4. Azure Container Host Gen 1 (Legacy Boot)

**Variant Configuration File**: `azure-container-host-gen1.yaml`

### Description:
The `azure-container-host-gen1` variant is optimized for running container
workloads on Azure Virtual Machines that use the **legacy BIOS boot method**. It
includes Azure-specific agents and packages to ensure full integration with the
Azure platform.

## 5. Azure Container Host Gen 2 (EFI Boot)

**Configuration File**: `azure-container-host-gen2.yaml`

### Description:
The `azure-container-host-gen2` variant is similar to
`azure-container-host-gen1` but is optimized for VMs that use the modern **EFI
boot method**. EFI provides better security features, faster boot times, and
support for potential larger disk partitions.
