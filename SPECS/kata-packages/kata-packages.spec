Summary:        Metapackage for Kata
Name:           kata-packages-uvm
Version:        1.1.0
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Base
URL:            https://aka.ms/mariner

%description
Metapackage for Kata.

%package        uvm
Summary:        Metapackage to install the set of packages inside a Kata containers UVM.
Requires:       bash
Requires:       ca-certificates
Requires:       chrony
Requires:       cpio
Requires:       cryptsetup
Requires:       curl
Requires:       dbus
Requires:       elfutils-libelf
Requires:       filesystem
Requires:       grep
Requires:       gzip
Requires:       iptables
Requires:       iproute
Requires:       iputils
Requires:       irqbalance
Requires:       lvm2
Requires:       lz4
Requires:       procps-ng
Requires:       readline
Requires:       sed
Requires:       tar
Requires:       tzdata
Requires:       util-linux
Requires:       zlib

%description    uvm
%{summary}

%package        coco-uvm
Summary:        Metapackage to install the set of packages inside a Kata confidential containers UVM.
Requires:       %{name}-uvm = %{version}-%{release}
Requires:       device-mapper
Requires:       opa

%description    coco-uvm
%{summary}

%package        uvm-build
Summary:        Metapackage to install the set of packages for building a Kata UVM.
Requires:       acpica-tools
Requires:       clang
Requires:       kata-containers-tools
Requires:       kata-containers-cc-tools
Requires:       kernel-uvm
Requires:       kernel-uvm-cvm
# Uncomment and remove duplicates once msigvm is available
#Requires:       msigvm
# Python dependencies for non-packaged IGVM tool
Requires:       python3
Requires:       python3-pip
Requires:       python3-frozendict
Requires:       python3-ecdsa
Requires:       python3-pyelftools
Requires:       python3-cached_property
Requires:       python3-cstruct
Requires:       python3-devel
Requires:       python3-libs
Requires:       python3-setuptools
Requires:       python3-pytest 
Requires:       python3-libclang
Requires:       python3-tomli    
Requires:       veritysetup 

%description    uvm-build
%{summary}

%package        coco-uvm-sign
Summary:        Metapackage to install the set of packages for building the signing tool for Kata confidential containers UVM.
Requires:       build-essential
# Uncomment and remove duplicates once cosesign1go is available
#Requires:       cosesign1go
Requires:       golang

%description    coco-uvm-sign
%{summary}

%prep

%build

%files uvm

%files coco-uvm

%files uvm-build

%files coco-uvm-sign

%changelog
* Tue Dec 19 2023 Mitch Zhu <mitchzhu@microsoft.com> - 1.1.0-1
- Introduce kata meta-package to CBL-Mariner.
