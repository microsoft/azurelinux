%global runtime_make_vars       DEFSTATICRESOURCEMGMT=true \\\
                                SKIP_GO_VERSION_CHECK=1

%global agent_make_vars         LIBC=gnu \\\
                                SECURITY_POLICY=yes

%global debug_package %{nil}

Name:         kata-containers-cc
Version:      0.6.0
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
BuildRequires:  kernel-uvm-devel
BuildRequires:  openssl-devel
BuildRequires:  clang
BuildRequires:  device-mapper-devel
BuildRequires:  cmake

Requires:  kernel-uvm
Requires:  moby-containerd-cc

%description
Kata Confidential Containers.

%package tools
Summary:        Kata CC Tools package for building UVM components
Requires:       cargo
Requires:       qemu-img
Requires:       parted
Requires:       curl
Requires:       opa >= 0.50.2
Requires:       kernel-uvm

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

# Runtime
pushd %{_builddir}/%{name}-%{version}/src/runtime
%make_build %{runtime_make_vars}
popd

# Tardev snapshotter
pushd %{_builddir}/%{name}-%{version}/src/tardev-snapshotter
make
chmod +x target/release/tardev-snapshotter
popd

pushd /usr/src/linux-headers*
header_dir=$(basename $PWD)
KERNEL_VER=${header_dir#"linux-headers-"}
KERNEL_MODULE_VER=${KERNEL_VER%%-*}
popd

# Kernel modules
pushd %{_builddir}/%{name}-%{version}/src/tarfs
make KDIR=/usr/src/linux-headers-${KERNEL_VER}
make KDIR=/usr/src/linux-headers-${KERNEL_VER} install
popd
%global KERNEL_MODULES_DIR %{_builddir}/%{name}-%{version}/src/tarfs/_install/lib/modules/${KERNEL_MODULE_VER}

# Agent
pushd %{_builddir}/%{name}-%{version}/src/agent
%make_build %{agent_make_vars}
popd

%install
%define coco_path     /opt/confidential-containers
%define coco_bin      %{coco_path}/bin
%define defaults_kata %{coco_path}/share/defaults/kata-containers
%define share_kata    %{coco_path}/share/kata-containers
%define osbuilder     /opt/mariner/share/uvm

mkdir -p %{buildroot}%{osbuilder}/tools/osbuilder/scripts
mkdir -p %{buildroot}%{osbuilder}/tools/osbuilder/rootfs-builder
mkdir -p %{buildroot}%{osbuilder}/tools/osbuilder/initrd-builder
mkdir -p %{buildroot}%{osbuilder}/tools/osbuilder/image-builder
mkdir -p %{buildroot}%{osbuilder}/ci

# Kernel modules
cp -aR %{KERNEL_MODULES_DIR} %{buildroot}%{osbuilder}

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

# Symlinks for cc binaries
mkdir -p %{buildroot}%{coco_bin}
mkdir -p %{buildroot}%{share_kata}
mkdir -p %{buildroot}%{coco_path}/libexec
mkdir -p %{buildroot}/etc/systemd/system/containerd.service.d/

# cloud-hypervisor is not intended for prod scenarios
ln -s /usr/bin/cloud-hypervisor               %{buildroot}%{coco_bin}/cloud-hypervisor
ln -s /usr/bin/cloud-hypervisor               %{buildroot}%{coco_bin}/cloud-hypervisor-snp
ln -s /usr/share/cloud-hypervisor/vmlinux.bin %{buildroot}%{share_kata}/vmlinux.container

ln -sf /usr/libexec/virtiofsd %{buildroot}/%{coco_path}/libexec/virtiofsd

find %{buildroot}/etc

# Agent
pushd %{_builddir}/%{name}-%{version}/src/agent

mkdir -p %{buildroot}%{osbuilder}/src/agent/samples/policy
cp -aR samples/policy/all-allowed         %{buildroot}%{osbuilder}/src/agent/samples/policy
install -D -m 0755 kata-containers.target %{buildroot}%{osbuilder}/kata-containers.target
install -D -m 0755 kata-agent.service.in  %{buildroot}%{osbuilder}/kata-agent.service.in
install -D -m 0755 coco-opa.service       %{buildroot}%{osbuilder}/coco-opa.service
install -D -m 0755 target/x86_64-unknown-linux-gnu/release/kata-agent %{buildroot}%{osbuilder}/kata-agent

popd 

# Runtime
pushd %{_builddir}/%{name}-%{version}/src/runtime
install -D -m 0755 containerd-shim-kata-v2 %{buildroot}/usr/local/bin/containerd-shim-kata-cc-v2
install -D -m 0755 kata-monitor %{buildroot}%{coco_bin}/kata-monitor
install -D -m 0755 kata-runtime %{buildroot}%{coco_bin}/kata-runtime
install -D -m 0755 data/kata-collect-data.sh %{buildroot}%{coco_bin}/kata-collect-data.sh

# configuration-clh.toml is not intended for prod scenarios
install -D -m 0644 config/configuration-clh.toml %{buildroot}/%{defaults_kata}/configuration-clh.toml
install -D -m 0644 config/configuration-clh-snp.toml %{buildroot}/%{defaults_kata}/configuration-clh-snp.toml
sed -i 's|/usr|/opt/confidential-containers|g' %{buildroot}/%{defaults_kata}/configuration-clh.toml
sed -i 's|/usr|/opt/confidential-containers|g' %{buildroot}/%{defaults_kata}/configuration-clh-snp.toml
popd

# Tardev-snapshotter
pushd %{_builddir}/%{name}-%{version}/src/tardev-snapshotter/
sed -i -e 's/containerd.service/kubelet.service/g' tardev-snapshotter.service
install -m 0644 -D -t %{buildroot}%{_unitdir} tardev-snapshotter.service
install -D -m 0755 target/release/tardev-snapshotter  %{buildroot}/usr/bin/tardev-snapshotter
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
%{_unitdir}/tardev-snapshotter.service
%{_prefix}/local/bin/containerd-shim-kata-cc-v2

%license LICENSE
%doc CONTRIBUTING.md
%doc README.md


%files tools
%dir %{osbuilder}/src/agent/samples/policy/all-allowed
%{osbuilder}/src/agent/samples/policy/all-allowed/all-allowed-data.json
%{osbuilder}/src/agent/samples/policy/all-allowed/all-allowed.rego

%{osbuilder}/mariner-coco-build-uvm.sh
%{osbuilder}/kata-containers.target
%{osbuilder}/kata-agent.service.in
%{osbuilder}/coco-opa.service
%{osbuilder}/kata-agent
%{osbuilder}/ci/install_yq.sh

%{osbuilder}/VERSION
%{osbuilder}/versions.yaml

%dir %{osbuilder}/modules
%dir %{osbuilder}/tools
%{osbuilder}/modules/*
%{osbuilder}/tools/*

# Remove some scripts we don't use
%exclude %{osbuilder}/tools/osbuilder/rootfs-builder/alpine
%exclude %{osbuilder}/tools/osbuilder/rootfs-builder/centos
%exclude %{osbuilder}/tools/osbuilder/rootfs-builder/clearlinux
%exclude %{osbuilder}/tools/osbuilder/rootfs-builder/debian
%exclude %{osbuilder}/tools/osbuilder/rootfs-builder/template
%exclude %{osbuilder}/tools/osbuilder/rootfs-builder/ubuntu


%changelog
* Mon Aug 07 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 0.6.0-2
- Bump release to rebuild with go 1.19.12

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
