# Confidential Virtual Machines (CVM)

- [Confidential Virtual Machines (CVM)](#confidential-virtual-machines-cvm)
  - [Overview](#overview)
  - [How CVMs work](#how-cvms-work)
  - [Azure Linux CVM image](#azure-linux-cvm-image)
    - [Key packages](#key-packages)
    - [Disk layout](#disk-layout)
    - [Boot flow](#boot-flow)
  - [Building a CVM image](#building-a-cvm-image)

## Overview

A **Confidential Virtual Machine (CVM)** is a virtual machine that uses hardware-based
[Trusted Execution Environments (TEEs)](https://en.wikipedia.org/wiki/Trusted_execution_environment)
to protect the confidentiality and integrity of data and code in use, even from the
underlying cloud infrastructure operator.

Azure CVMs are built on top of hardware attestation technologies such as:

- **AMD SEV-SNP** (Secure Encrypted Virtualization – Secure Nested Paging): provides
  hardware-enforced memory encryption and integrity protection, and generates a hardware
  attestation report that proves the VM's identity and launch state to a remote verifier.
- **Intel TDX** (Trust Domain Extensions): isolates VMs from the hypervisor and other
  software using hardware-enforced trust domains with memory encryption.

These technologies ensure that:

1. VM memory is encrypted with a key that is controlled by the hardware and inaccessible
   to the host/hypervisor.
2. The VM's initial state (firmware, bootloader, OS, and kernel command line) is measured
   into a hardware-rooted log whose integrity can be verified remotely through attestation.
3. Secrets can be provisioned into the VM only after successful attestation.

For more information about Azure Confidential VMs, see the
[Azure confidential computing documentation](https://learn.microsoft.com/azure/confidential-computing/confidential-vm-overview).

## How CVMs work

The trust chain in an Azure CVM runs from hardware through firmware and into the OS:

1. The hardware measures the virtual firmware (vTPM-backed UEFI) into hardware registers.
2. UEFI measures the bootloader (shim → systemd-boot) into TPM PCRs.
3. The bootloader verifies and measures the Unified Kernel Image (UKI) into TPM PCRs.
4. The UKI packages the kernel, initramfs, and the kernel command line into a single
   PE/COFF binary that is signed and verified by Secure Boot before execution.
5. A remote relying party can request an attestation report from the hardware (via
   `tpm2-tools` or the Azure Attestation service) that covers all the measured values,
   confirming the entire boot chain has not been tampered with.

Because the kernel command line is embedded and signed inside the UKI, an attacker who
gains access to the ESP cannot silently alter boot parameters to weaken security.

## Azure Linux CVM image

Azure Linux ships a pre-defined image configuration for CVMs:
[`toolkit/imageconfigs/marketplace-gen2-cvm.json`](../../imageconfigs/marketplace-gen2-cvm.json).

### Key packages

| Package | Role |
|:--------|:-----|
| `shim` | First-stage UEFI bootloader; carries the Microsoft Secure Boot certificate that allows Azure Linux's own key to be trusted |
| `systemd-boot` | Second-stage UEFI bootloader; chainloads the UKI |
| `kernel-uki` | Linux kernel packaged as a Unified Kernel Image (UKI); the kernel, initramfs, and kernel command line are combined into a single signed binary |
| `tpm2-tools` | Utilities for interacting with the TPM 2.0 device; used for attestation and sealing secrets to the measured boot state |
| `ca-certificates` | Root CA bundle; required for TLS connections to attestation and key-release services |

### Disk layout

The CVM image uses a GPT disk with two partitions:

| Partition | Size | Type | Mount point | Purpose |
|:----------|:-----|:-----|:------------|:--------|
| `efi` | 512 MiB | ESP (`esp` + `boot` flags, type UUID `C12A7328-F81F-11D2-BA4B-00A0C93EC93B`) | `/efi` | Stores the UKI and the systemd-boot loader entries |
| `rootfs` | Remainder | Linux root x86-64 (type UUID `4F68BCE3-E8CD-4DB1-96E7-FBCAF984B709`) | `/` | Root filesystem |

Using the standardized `linux-root-amd64` partition type UUID allows `systemd` and
`systemd-gpt-auto-generator` to discover and mount the root partition automatically,
without requiring entries in `/etc/fstab`.

### Boot flow

1. UEFI firmware loads `shim` from the ESP.
2. `shim` verifies and loads `systemd-boot`.
3. `systemd-boot` reads loader entries under `/efi/loader/` (configured by
   [`additionalconfigs/sdboot-loader.conf`](../../imageconfigs/additionalconfigs/sdboot-loader.conf))
   and loads the signed UKI.
4. The UKI extracts the embedded initramfs, mounts the root filesystem, and executes
   `systemd` as PID 1.

Because `/etc/fstab` is intentionally left empty (see
[`scripts/setup_cvm_image.sh`](../../imageconfigs/scripts/setup_cvm_image.sh)),
root-filesystem discovery relies entirely on the GPT partition type UUID. This keeps the
measured boot state stable across disk reattachments.

## Building a CVM image

To build the CVM VHD image, run:

```bash
sudo make image CONFIG_FILE=imageconfigs/marketplace-gen2-cvm.json
```

The resulting artifact is named `cblmariner-gen2-cvm.vhd` (as specified by the `Name` field
in the image configuration) and can be uploaded to Azure as a custom image for a
[Confidential VM](https://learn.microsoft.com/azure/confidential-computing/confidential-vm-overview).
