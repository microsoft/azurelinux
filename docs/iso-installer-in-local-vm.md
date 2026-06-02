# ISO Installer in Local VM

The Azure Linux ISO may work in some bare-metal scenarios, but is generally intended for installation to a Virtual Machine.

The ISO boots the [Anaconda](https://anaconda-installer.readthedocs.io/) installer (run in text mode). Follow its prompts to partition disks, set a root password, create a user, and complete the installation. A serial console is preconfigured at `ttyS0/115200`.

> _Note: Azure Linux 4.0 ISOs are currently in Preview and not Secure Boot signed. Disable Secure Boot in your VM's firmware settings before booting the installer._

This guide covers two local virtualization options:

- [Using ISO Installer in Hyper-V VM](#using-iso-installer-in-hyper-v-vm) (Windows host)
- [Using ISO Installer in QEMU/KVM](#using-iso-installer-in-qemukvm) (Linux host)

## Using ISO Installer in Hyper-V VM
From a Windows PC:

**Create Generation 2 Virtual Machine with Hyper-V**

1. From Hyper-V Manager, select _Action->New->Virtual Machine_.
1. Provide a name for your VM and press _Next >_.
1. Select _Generation 2_, then press _Next >_.
1. Uncheck _Use Dynamic Memory for this virtual machine_, then press _Next >_.
1. Select a virtual switch, then press _Next >_.
1. Select _Create a virtual hard disk_, choose a location for your VHDX and set your desired disk size.  Then press _Next >_.
1. Select _Install an operating system from a bootable image file_ and browse to your Azure Linux ISO.
1. Press _Finish_.

**Adjust VM Settings**

1. Right click your virtual machine from Hyper-V Manager.
1. Select _Settings..._
1. Select Security and uncheck _Enable Secure Boot_.
   - _Note: Secure Boot will be supported in a future release of Azure Linux._
1. Select _Apply_ to apply all changes.

**Boot ISO Installer**
1. Right click your VM and select _Connect..._.
1. Select _Start_.
1. Follow the installer prompts to install your image.
   - During installation menu, ensure all `[!]` are addressed in order to continue.
1. When installation completes, press Enter to reboot the machine.
1. When prompted, sign in to your new Azure Linux installation using the username and password provisioned through the installer.

## Using ISO Installer in QEMU/KVM

On a Linux host you can boot the ISO with QEMU using KVM acceleration and UEFI
firmware (OVMF/edk2). This example uses the `x86_64` ISO; for `aarch64`, install
the matching firmware and use `qemu-system-aarch64`.

### Prerequisites

- An `x86_64` host with KVM available (`/dev/kvm` accessible to your user).
- `qemu-system-x86_64` and OVMF/edk2 firmware installed. The commands below
  assume firmware at `/usr/share/edk2/ovmf/`; adjust if your distro installs it
  elsewhere (common alternative: `/usr/share/OVMF/`).
- Recommended sizing: 2+ vCPUs, 16 GiB+ disk.

### Setup

Create an empty virtual disk and a private, writable copy of the UEFI variable store:

```bash
qemu-img create -f qcow2 azl4.qcow2 16G
cp /usr/share/edk2/ovmf/OVMF_VARS.fd ./azl4_VARS.fd
```

### Boot the ISO

```bash
qemu-system-x86_64 \
  -name azl4-live \
  -machine q35,accel=kvm \
  -cpu host \
  -smp 2 \
  -m 4096 \
  -drive if=pflash,format=raw,readonly=on,file=/usr/share/edk2/ovmf/OVMF_CODE.fd \
  -drive if=pflash,format=raw,file=./azl4_VARS.fd \
  -device virtio-blk-pci,drive=disk0,bootindex=0 \
  -drive id=disk0,if=none,file=azl4.qcow2,format=qcow2 \
  -device ide-cd,drive=cd0,bootindex=1 \
  -drive id=cd0,if=none,file=azurelinux-4.0-x86_64.iso,media=cdrom,readonly=on \
  -netdev user,id=net0 -device virtio-net-pci,netdev=net0 \
  -nographic \
  -serial mon:stdio
```

Notes:

- `-nographic -serial mon:stdio` attaches your terminal to the guest serial
  console. GRUB and the Anaconda text installer appear inline.
  - `Ctrl-a c` — switch to the QEMU monitor
  - `Ctrl-a x` — quit QEMU

Follow the [Anaconda](https://anaconda-installer.readthedocs.io/) installer
prompts to complete the installation:

* During installation menu, ensure all `[!]` are addressed in order to continue.
* When installation completes, press Enter to reboot the machine.
* When prompted, sign in to your new Azure Linux installation using the username and password provisioned through the installer.

### Boot the installed system

After installation completes, you can safely boot from the virtual disk without
the ISO, e.g.:

```bash
qemu-system-x86_64 \
  -name azl4 \
  -machine q35,accel=kvm \
  -cpu host \
  -smp 2 \
  -m 4096 \
  -drive if=pflash,format=raw,readonly=on,file=/usr/share/edk2/ovmf/OVMF_CODE.fd \
  -drive if=pflash,format=raw,file=./azl4_VARS.fd \
  -device virtio-blk-pci,drive=disk0 \
  -drive id=disk0,if=none,file=azl4.qcow2,format=qcow2 \
  -netdev user,id=net0 -device virtio-net-pci,netdev=net0 \
  -nographic \
  -serial mon:stdio
```
