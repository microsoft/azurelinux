%global runtime_make_vars       DEFSTATICRESOURCEMGMT_CLH=true \\\
                                DEFSHAREDFS_CLH_SNP_VIRTIOFS=none \\\
                                SKIP_GO_VERSION_CHECK=1

%global agent_make_vars         LIBC=gnu \\\
                                AGENT_POLICY=yes

%global debug_package %{nil}

Name:         kata-containers-cc
Version:      0.6.2
Release:      2%{?dist}
Summary:      Kata Confidential Containers
License:      ASL 2.0
Vendor:       Microsoft Corporation
URL:          https://github.com/microsoft/kata-containers
Source0:      https://github.com/microsoft/kata-containers/archive/refs/tags/cc-%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:      https://github.com/microsoft/kata-containers/archive/refs/tags/%{name}-%{version}.tar.gz
Source2:      %{name}-%{version}-cargo.tar.gz
Source3:      mariner-coco-build-uvm.sh

ExclusiveArch: x86_64

BuildRequires:  golang
BuildRequires:  make
BuildRequires:  protobuf-compiler
BuildRequires:  dracut
BuildRequires:  cargo
BuildRequires:  rust
BuildRequires:  git
BuildRequires:  sudo
BuildRequires:  perl-FindBin
BuildRequires:  perl-lib
BuildRequires:  libseccomp-devel
BuildRequires:  openssl-devel
BuildRequires:  clang
BuildRequires:  device-mapper-devel
BuildRequires:  cmake
BuildRequires:  fuse-devel

# needed to build the tarfs module, see next comment - we currently build the tarfs module for both kernels
BuildRequires:  kernel-uvm-devel
BuildRequires:  kernel-uvm-cvm-devel

# kernel-uvm is required for allowing to test the kata-cc handler w/o SEV SNP but with the
# policy feature using kernel-uvm and the kata-cc shim/agent from this package with policy features
Requires:  kernel-uvm
Requires:  kernel-uvm-cvm
Requires:  moby-containerd-cc
Requires:  qemu-virtiofsd

%description
Kata Confidential Containers.

# This subpackage is used to build the uvm and therefore has dependencies on the kernel-uvm(-cvm) binaries
%package tools
Summary:        Kata CC tools package for building UVM components
Requires:       cargo
Requires:       qemu-img
Requires:       parted
Requires:       curl
Requires:       veritysetup
Requires:       opa >= 0.50.2
Requires:       kernel-uvm
Requires:       kernel-uvm-cvm

%description tools
This package contains the UVM osbuilder files

%prep
%autosetup -p1 -n %{name}-%{version}
pushd %{_builddir}/%{name}-%{version}
tar -xf %{SOURCE2}
popd

%build
export PATH=$PATH:"$(pwd)/go/bin"
export GOPATH="$(pwd)/go"
export OPENSSL_NO_VENDOR=1

# kata shim/runtime
pushd %{_builddir}/%{name}-%{version}/src/runtime
%make_build %{runtime_make_vars}
popd

# agent
pushd %{_builddir}/%{name}-%{version}/src/agent
%make_build %{agent_make_vars}
popd

# tardev snapshotter
pushd %{_builddir}/%{name}-%{version}/src/tardev-snapshotter
make
chmod +x target/release/tardev-snapshotter
popd

# overlay
pushd %{_builddir}/%{name}-%{version}/src/overlay
cargo build --release
popd

# utarfs
pushd %{_builddir}/%{name}-%{version}/src/utarfs
cargo build --release
popd

# kernel modules
pushd /usr/src/linux-headers*cvm
header_dir=$(basename $PWD)
KERNEL_CVM_VER=${header_dir#"linux-headers-"}
KERNEL_CVM_MODULE_VER=${KERNEL_CVM_VER%%-*}
popd

pushd /usr/src/$(ls /usr/src | grep linux-header | grep -v cvm)
header_dir=$(basename $PWD)
KERNEL_VER=${header_dir#"linux-headers-"}
KERNEL_MODULE_VER=${KERNEL_VER%%-*}
popd

# make a copy of the tarfs folder for cvm modules
mkdir -p %{_builddir}/%{name}-%{version}/src/tarfs-cvm
cp -aR %{_builddir}/%{name}-%{version}/src/tarfs/* %{_builddir}/%{name}-%{version}/src/tarfs-cvm/

pushd %{_builddir}/%{name}-%{version}/src/tarfs
make KDIR=/usr/src/linux-headers-${KERNEL_VER}
make KDIR=/usr/src/linux-headers-${KERNEL_VER} install
popd
%global KERNEL_MODULES_DIR %{_builddir}/%{name}-%{version}/src/tarfs/_install/lib/modules/${KERNEL_MODULE_VER}

pushd %{_builddir}/%{name}-%{version}/src/tarfs-cvm
make KDIR=/usr/src/linux-headers-${KERNEL_CVM_VER}
make KDIR=/usr/src/linux-headers-${KERNEL_CVM_VER} install
popd
%global KERNEL_CVM_MODULES_DIR %{_builddir}/%{name}-%{version}/src/tarfs-cvm/_install/lib/modules/${KERNEL_CVM_MODULE_VER}

%install
%define coco_path     /opt/confidential-containers
%define coco_bin      %{coco_path}/bin
%define defaults_kata %{coco_path}/share/defaults/kata-containers
%define share_kata    %{coco_path}/share/kata-containers
%define osbuilder     %{coco_path}/uvm

mkdir -p %{buildroot}%{osbuilder}/tools/osbuilder/scripts
mkdir -p %{buildroot}%{osbuilder}/tools/osbuilder/rootfs-builder
mkdir -p %{buildroot}%{osbuilder}/tools/osbuilder/initrd-builder
mkdir -p %{buildroot}%{osbuilder}/tools/osbuilder/image-builder
mkdir -p %{buildroot}%{osbuilder}/ci

# kernel modules
cp -aR %{KERNEL_MODULES_DIR} %{buildroot}%{osbuilder}
cp -aR %{KERNEL_CVM_MODULES_DIR} %{buildroot}%{osbuilder}

# osbuilder
pushd %{_builddir}/%{name}-%{version}
rm tools/osbuilder/.gitignore
rm tools/osbuilder/rootfs-builder/.gitignore

install -D -m 0755 %{SOURCE3}           %{buildroot}%{osbuilder}/mariner-coco-build-uvm.sh
install -D -m 0644 VERSION              %{buildroot}%{osbuilder}/VERSION
install -D -m 0644 ci/install_yq.sh     %{buildroot}%{osbuilder}/ci/install_yq.sh
install -D -m 0644 versions.yaml        %{buildroot}%{osbuilder}/versions.yaml
install -D -m 0644 tools/osbuilder/Makefile  %{buildroot}%{osbuilder}/tools/osbuilder/Makefile

sed -i 's#distro_config_dir="${script_dir}/${distro}#distro_config_dir="${script_dir}/cbl-mariner#g' tools/osbuilder/rootfs-builder/rootfs.sh
cp -aR tools/osbuilder/rootfs-builder   %{buildroot}%{osbuilder}/tools/osbuilder
cp -aR tools/osbuilder/initrd-builder   %{buildroot}%{osbuilder}/tools/osbuilder
cp -aR tools/osbuilder/scripts          %{buildroot}%{osbuilder}/tools/osbuilder
popd

mkdir -p %{buildroot}%{coco_bin}
mkdir -p %{buildroot}%{share_kata}
mkdir -p %{buildroot}%{coco_path}/libexec
mkdir -p %{buildroot}/etc/systemd/system/containerd.service.d/

# for testing policy/snapshotter without SEV SNP we use CH (with kernel-uvm and initrd) instead of CH-CVM with IGVM
# Note: our kata-containers config toml expects cloud-hypervisor and kernel under a certain path/name, so we align this through symlinks here
ln -s /usr/bin/cloud-hypervisor               %{buildroot}%{coco_bin}/cloud-hypervisor
ln -s /usr/bin/cloud-hypervisor-cvm           %{buildroot}%{coco_bin}/cloud-hypervisor-snp

# this is again for testing without SEV SNP
ln -s /usr/share/cloud-hypervisor/vmlinux.bin %{buildroot}%{share_kata}/vmlinux.container

ln -sf /usr/libexec/virtiofsd %{buildroot}/%{coco_path}/libexec/virtiofsd

find %{buildroot}/etc

# agent
pushd %{_builddir}/%{name}-%{version}/src/agent
mkdir -p %{buildroot}%{osbuilder}/src/kata-opa
cp -a %{_builddir}/%{name}-%{version}/src/kata-opa/allow-all.rego %{buildroot}%{osbuilder}/src/kata-opa/
cp -a %{_builddir}/%{name}-%{version}/src/kata-opa/kata-opa.service.in %{buildroot}%{osbuilder}/src/kata-opa/
install -D -m 0755 kata-containers.target %{buildroot}%{osbuilder}/kata-containers.target
install -D -m 0755 kata-agent.service.in  %{buildroot}%{osbuilder}/kata-agent.service.in
install -D -m 0755 target/x86_64-unknown-linux-gnu/release/kata-agent %{buildroot}%{osbuilder}/kata-agent
popd

# runtime/shim
pushd %{_builddir}/%{name}-%{version}/src/runtime
install -D -m 0755 containerd-shim-kata-v2 %{buildroot}/usr/local/bin/containerd-shim-kata-cc-v2
install -D -m 0755 kata-monitor %{buildroot}%{coco_bin}/kata-monitor
install -D -m 0755 kata-runtime %{buildroot}%{coco_bin}/kata-runtime
install -D -m 0755 data/kata-collect-data.sh %{buildroot}%{coco_bin}/kata-collect-data.sh

# Note: we deploy two configurations - the additional one is for policy/snapshotter testing w/o SEV SNP or IGVM
install -D -m 0644 config/configuration-clh.toml %{buildroot}/%{defaults_kata}/configuration-clh.toml
install -D -m 0644 config/configuration-clh-snp.toml %{buildroot}/%{defaults_kata}/configuration-clh-snp.toml

# adapt upstream config files
# change paths with locations specific to our distribution
sed -i 's|/usr|/opt/confidential-containers|g' %{buildroot}/%{defaults_kata}/configuration-clh.toml
sed -i 's|/usr|/opt/confidential-containers|g' %{buildroot}/%{defaults_kata}/configuration-clh-snp.toml
popd

# tardev-snapshotter
pushd %{_builddir}/%{name}-%{version}/src/tardev-snapshotter/
sed -i -e 's/containerd.service/kubelet.service/g' tardev-snapshotter.service
install -m 0644 -D -t %{buildroot}%{_unitdir} tardev-snapshotter.service
install -D -m 0755 target/release/tardev-snapshotter  %{buildroot}/usr/bin/tardev-snapshotter
popd

# overlay
pushd %{_builddir}/%{name}-%{version}/src/overlay/
install -D -m 0755 target/release/kata-overlay  %{buildroot}/usr/bin/kata-overlay
popd

# utarfs
pushd %{_builddir}/%{name}-%{version}/src/utarfs/
install -D -m 0755 target/release/utarfs  %{buildroot}/usr/sbin/mount.tar
popd

install -D -m 0755 %{_builddir}/%{name}-%{version}/tools/osbuilder/image-builder/image_builder.sh   %{buildroot}%{osbuilder}/tools/osbuilder/image-builder/image_builder.sh
install -D -m 0755 %{_builddir}/%{name}-%{version}/tools/osbuilder/image-builder/nsdax.gpl.c        %{buildroot}%{osbuilder}/tools/osbuilder/image-builder/nsdax.gpl.c

%preun
%systemd_preun tardev-snapshotter.service

%postun
%systemd_postun tardev-snapshotter.service

%post
%systemd_post tardev-snapshotter.service

%files
%{share_kata}/vmlinux.container

%{coco_bin}/cloud-hypervisor
%{coco_bin}/cloud-hypervisor-snp
%{coco_bin}/kata-collect-data.sh
%{coco_bin}/kata-monitor
%{coco_bin}/kata-runtime

%{defaults_kata}/configuration*.toml
%{coco_path}/libexec/virtiofsd

%{_bindir}/tardev-snapshotter
%{_bindir}/kata-overlay
%{_sbindir}/mount.tar
%{_unitdir}/tardev-snapshotter.service
%{_prefix}/local/bin/containerd-shim-kata-cc-v2

%license LICENSE
%doc CONTRIBUTING.md
%doc README.md

%files tools
%dir %{osbuilder}/src/kata-opa
%{osbuilder}/src/kata-opa/allow-all.rego
%{osbuilder}/src/kata-opa/kata-opa.service.in

%{osbuilder}/mariner-coco-build-uvm.sh
%{osbuilder}/kata-containers.target
%{osbuilder}/kata-agent.service.in
%{osbuilder}/kata-agent
%{osbuilder}/ci/install_yq.sh

%{osbuilder}/VERSION
%{osbuilder}/versions.yaml

%dir %{osbuilder}/modules
%dir %{osbuilder}/tools
%{osbuilder}/modules/*
%{osbuilder}/tools/*

# remove some scripts we don't use
%exclude %{osbuilder}/tools/osbuilder/rootfs-builder/alpine
%exclude %{osbuilder}/tools/osbuilder/rootfs-builder/centos
%exclude %{osbuilder}/tools/osbuilder/rootfs-builder/clearlinux
%exclude %{osbuilder}/tools/osbuilder/rootfs-builder/debian
%exclude %{osbuilder}/tools/osbuilder/rootfs-builder/template
%exclude %{osbuilder}/tools/osbuilder/rootfs-builder/ubuntu

%changelog
*   Tue Dec 05 2023 Archana Choudhary <archana1@microsoft.com> - 0.6.2-2
-   Add qemu-virtiofsd as a requirement

*   Fri Nov 3 2023 Dallas Delaney <dadelan@microsoft.com> 0.6.2-1
-   Upgrade to version 0.6.2

*   Fri Nov 3 2023 Dallas Delaney <dadelan@microsoft.com> - 0.6.1-4
-   Add patch to retain UVM rootfs dependencies

*   Mon Oct 16 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 0.6.1-3
-   Bump release to rebuild with go 1.20.9

*   Tue Oct 10 2023 Dan Streetman <ddstreet@ieee.org> - 0.6.1-2
-   Bump release to rebuild with updated version of Go.

*   Mon Sep 18 2023 Dallas Delaney <dadelan@microsoft.com> 0.6.1-1
-   Update to use cloud-hypervisor-cvm and kernel-uvm-cm
-   Pull in latest source for genpolicy, utarfs, and overlay changes

*   Thu Sep 14 2023 Muhammad Falak <mwani@microsoft.com> - 0.6.0-4
-   Introduce patch to drop mut for immutable vars
-   Introduce patch enabling feature(impl_trait_in_assoc_type) to unblock build

*   Thu Sep 07 2023 Daniel McIlvaney <damcilva@microsoft.com> - 0.6.0-3
-   Bump package to rebuild with rust 1.72.0

*   Mon Aug 07 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 0.6.0-2
-   Bump release to rebuild with go 1.19.12

*   Tue Jul 11 2023 Dallas Delaney <dadelan@microsoft.com> 0.6.0-1
-   Upgrade to version 0.6.0

*   Thu Jul 13 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 0.4.2-2
-   Bump release to rebuild with go 1.19.11

*   Thu Jun 29 2023 Dallas Delaney <dadelan@microsoft.com> 0.4.2-1
-   Upgrade to version 0.4.2 for new snapshotter and policy features

*   Thu Jun 15 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 0.4.1-3
-   Bump release to rebuild with go 1.19.10

*   Wed May 24 2023 Dallas Delaney <dadelan@microsoft.com> 0.4.1-2
-   Enable static resource management and build with host's openssl

*   Wed May 10 2023 Dallas Delaney <dadelan@microsoft.com> 0.4.1-1
-   Add version 0.4.1 and fix CVEs

*   Wed Apr 26 2023 Dallas Delaney <dadelan@microsoft.com> 0.4.0-1
-   Remove containerd override and add dependency on moby-containerd-cc

*   Mon Apr 24 2023 Dallas Delaney <dadelan@microsoft.com> 0.4.0-1
-   Add vendored code and move UVM building out of base package

*   Wed Apr 5 2023 Dallas Delaney <dadelan@microsoft.com> 0.1.0-10
-   Rebase against 0.4.0 upstream tag
-   License verified.
-   Original version for CBL-Mariner

*   Thu Mar 2 2023 Dallas Delaney <dadelan@microsoft.com> 0.1.0-9
-   Fix configuration paths

*   Wed Mar 1 2023 Dallas Delaney <dadelan@microsoft.com> 0.1.0-8
-   Build from source code

*   Fri Feb 17 2023 Mitch Zhu <mitchzhu@microsoft.com> 0.1.0-7
-   Port over kata-cc spec update

*   Wed Jan 18 2023 Dan Mihai <dmihai@microsoft.com> 0.1.0-6
-   Build kata UVM image

*   Mon Jan 16 2023 Dan Mihai <dmihai@microsoft.com> 0.1.0-5
-   Build kata runtime from source code

*   Mon Jan 16 2023 Dan Mihai <dmihai@microsoft.com> 0.1.0-4
-   Build kata-agent from source code

*   Thu Jan 12 2023 Dan Mihai <dmihai@microsoft.com> 0.1.0-3
-   Install /usr/local/bin/containerd-shim-kata-clh-v2

*   Thu Jan 12 2023 Dan Mihai <dmihai@microsoft.com> 0.1.0-2
-   Mariner-based host configuration

*   Tue Oct 25 2022 Dallas Delaney <dadelan@microsoft.com> 0.1.0-1
-   Initial rpm data and spec added
