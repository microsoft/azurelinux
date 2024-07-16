# Quick Start Guide
  - [Install from ISO](#install-from-bootable-iso) [Fastest]
  - [Build and boot and Image](#build-and-boot-an-image)
    - [Install Prerequisites](#install-prerequisites)
    - [Clone Azure Linux](#clone-azure-linux)
    - [VHDX and VHD Images](#vhdx-and-vhd-images)
    - [Build ISO Image](#iso-image)

## **Install from Bootable ISO**
The Azure Linux ISO may work in some bare-metal scenarios, but is generally intended for installation to a Virtual Machine.  From a Windows PC:

First, download the [Azure Linux 3.0 x86_64 ISO](https://aka.ms/azurelinux-3.0-x86_64-iso)

Then follow these instructions

**Create VHD(X) Virtual Machine with Hyper-V**

1. From Hyper-V Select _Action->New->Virtual Machine_.
1. Provide a name for your VM and press _Next >_.
1. Select _Generation 1_ (VHD) or _Generation 2_ (VHDX), then press _Next >_.
1. Change Memory size if desired, then press _Next >_.
1. Select a virtual switch, then press _Next >_.
1. Select _Create a virtual hard disk_, choose a location for your VHD(X) and set your desired disk Size.  Then press _Next >_.
1. Select _Install an operating system from a bootable image file_ and browse to your Azure Linux ISO.
1. Press _Finish_.

**[Gen2/VHDX Only] Fix Boot Options**

1. Right click your virtual machine from Hyper-V Manager
1. Select _Settings..._
1. Select Security and under _Template:_ select _Microsoft UEFI Certificate Authority_.
1. Select Firmware and adjust the boot order so DVD is first and Hard Drive is second.
1. Select _Apply_ to apply all changes.

**Boot ISO**
1. Right click your VM and select _Connect..._.
1. Select _Start_.
1. Follow the Installer Prompts to Install your image
1. When installation completes, select restart to reboot the machine. The installation ISO will be automatically ejected.
1. When prompted sign in to your Azure Linux using the user name and password provisioned through the Installer.

## **Build and Boot an Image**

### **Install Prerequisites**
Install prerequisites [here](../building/prerequisites.md).

### **Clone Azure Linux**
From a bash terminal window, clone the Azure Linux Repository and check-out a stable build.

```bash
# Clone the Azure Linux repo
git clone https://github.com/microsoft/azurelinux.git
cd azurelinux

# Sync to the latest stable build
git checkout 3.0-stable

```
### **VHDX and VHD images**

The following builds a bootable, VHDX or VHD Azure Linux image from precompiled RPMs in the Azure Linux package repository at https://packages.microsoft.com/azurelinux/3.0/prod/.

No user account is provisioned by default.  To sign-in to these images, the sample meta-user-data.iso image must also be built and installed in your VM's CD drive.  The cloud-init service will detect the iso and provision a user account and password.

**Build a VHD or VHDX Image**
```bash
# Switch to the toolkit folder
cd toolkit

# Build VHDX Image
# Image is placed in ../out/images/core-efi
sudo make image -j8 REBUILD_TOOLS=y REBUILD_PACKAGES=n CONFIG_FILE=./imageconfigs/core-efi.json

# Build VHD Image
# Image is placed in ../out/images/core-legacy
sudo make image -j8 REBUILD_TOOLS=y REBUILD_PACKAGES=n CONFIG_FILE=./imageconfigs/core-legacy.json
```

**Build the cloud-init configuration image**

Note that the cloud-init configuration file does not build by default.  You will need to edit it to set a username and password or SSH Key.  The file is located in ./resources/assets/meta-user-data/user-data.

```Bash
# Build the cloud-init configuration image
# The output image is ../out/images/meta-user-data.iso
sudo make meta-user-data
```

**Copy VHD(X) and ISO Images to Your VM Host Machine**

Copy your binary image(s) to your VM Host Machine using your preferred technique.

**Create VHD(X) Virtual Machine with Hyper-V**

1. From Hyper-V Select _Action->New->Virtual Machine_.
1. Provide a name for your VM and press _Next >_.
1. For VHD select _Generation 1_. For VHDX select _Generation 2_, then press _Next >_.
1. Change Memory size if desired, then press _Next >_.
1. Select a virtual switch, then press _Next >_.
1. Select _Use an existing virtual hard disk_, then browse and select your VHD(X) file.
1. Press _Finish_.

**[Gen2/VHDX Only] Fix Boot Options**
1. Right click your virtual machine from Hyper-V Manager
1. Select _Settings..._.
1. Select Security and under _Template:_ select _Microsoft UEFI Certificate Authority_.
1. Select the SCSI Controller from the Hardware panel.
1. Select DVD Drive and press Add.

**Mount the Meta-User-Data.Iso Image**

1. Right click your virtual machine from Hyper-V Manager
1. Select _Settings..._.
choose DVD Drive and press Add.
1. Select the _DVD Drive_. For Gen1/VHD Images, this is nested under _IDE Controller 1_. For Gen2/VHDX Images, this is nested under _SCSI Controller_.
1. Select _Image File:_ and browse to the meta-user-data.iso file.
1. Select _Apply_ to apply all changes.

**Boot and Sign-In to your VHD**

1. Right click your VM and select _Connect..._.
1. Select _Start_.
1. Wait for Azure Linux to boot to the login prompt, then sign in with the username and password you provisioned in the meta-user-data.iso above.

### ISO Image

The following builds a bootable ISO image from precompiled RPMs in the Azure Linux package repository at https://packages.microsoft.com/azurelinux/3.0/prod/.

```bash
# Switch to the toolkit folder
cd toolkit

# Image is placed in ../out/images/full
sudo make iso -j8 REBUILD_TOOLS=y REBUILD_PACKAGES=n CONFIG_FILE=./imageconfigs/full.json
```
**Copy ISO Image to Your VM Host Machine**

Copy your binary image(s) to your VM Host Machine using your preferred technique and then follow these instructions
