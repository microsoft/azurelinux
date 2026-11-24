Summary:        Metapackage for Kata UVM components for GPU and HPC workloads
Name:           kata-packages-uvm-hpc
Version:        1.0.0
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Group:          System Environment/Base
URL:            https://aka.ms/mariner

# The GPU UVM is built on top of the regular Kata UVM package set. Its init process is
# NVRC (kata-nvrc, which starts the NVIDIA services and then the kata-agent), so systemd
# is installed but not run as PID 1. The kata-agent, the NVIDIA userspace and the NVIDIA
# kernel modules are added to the rootfs by the image builder, not by this metapackage.
Requires:       e2fsprogs
Requires:       kata-nvrc
Requires:       kata-packages-uvm

%description
Metapackage to install the set of packages inside a Kata containers UVM running GPU and HPC workloads.

%package        debug
Summary:        Metapackage to install the set of packages inside a Kata containers debug UVM running GPU and HPC workloads.
Requires:       %{name} = %{version}-%{release}
Requires:       kata-packages-uvm-debug
# Traces failing syscalls of the NVIDIA services (e.g. fabric manager) inside the UVM
Requires:       strace

%description    debug
Metapackage to install the set of packages inside a Kata containers UVM running GPU and HPC workloads, includes extra debug utilities.

%package        build
Summary:        Metapackage to install the set of packages for building a Kata UVM for GPU and HPC workloads.
# Builds the NVIDIA open GPU kernel modules against kernel-uvm-hpc-devel
Requires:       build-essential
Requires:       cargo
Requires:       clang
# The GPU UVM rootfs image is an erofs file system
Requires:       erofs-utils
Requires:       file
Requires:       kernel-uvm-hpc
Requires:       kernel-uvm-hpc-devel
Requires:       make
Requires:       parted
Requires:       qemu-img
# The GPU UVM rootfs image is dm-verity protected
Requires:       veritysetup

%description    build

%prep

%build

%files

%files debug

%files build

%changelog
* Thu Nov 05 2026 Jocelyn Berrendonner <jocelynb@microsoft.com> - 1.0.0-1
- Introduce kata meta-package for the components of Kata UVMs running GPU and HPC workloads.
- License verified
- Original version for Azure Linux
