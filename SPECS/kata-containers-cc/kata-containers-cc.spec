%global debug_package %{nil}

Name:         kata-containers-cc
Version:      3.2.0.azl2
Release:      1%{?dist}
Summary:      Kata Confidential Containers package developed for Confidential Containers on AKS
License:      ASL 2.0
Vendor:       Microsoft Corporation
URL:          https://github.com/microsoft/kata-containers
Source0:      https://github.com/microsoft/kata-containers/archive/refs/tags/%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:      %{name}-%{version}-cargo.tar.gz

ExclusiveArch: x86_64

BuildRequires:  golang
BuildRequires:  protobuf-compiler
BuildRequires:  rust
BuildRequires:  libseccomp-devel
BuildRequires:  openssl-devel
BuildRequires:  clang
BuildRequires:  device-mapper-devel
BuildRequires:  cmake
BuildRequires:  fuse-devel

# kernel-uvm is used for testing in a debug configuration w/o SEV SNP enablement
Requires:  kernel-uvm
Requires:  moby-containerd-cc
# Must match the version specified by the `assets.virtiofsd.version` field in the source's versions.yaml.
Requires:  virtiofsd = 1.8.0

%description
The Kata Confidential Containers package ships the Kata components for Confidential Containers on AKS.
The package sources are based on a Microsoft fork of the kata-containers project and tailored to the use
for Mariner-based AKS node images.

%package tools
Summary:        Kata Confidential Containers tools package for building the UVM

%description tools
This package contains the scripts and files required to build the UVM

%prep
%autosetup -p1 -n %{name}-%{version}
pushd %{_builddir}/%{name}-%{version}
tar -xf %{SOURCE1}
popd

%build
pushd %{_builddir}/%{name}-%{version}/tools/osbuilder/node-builder/azure-linux
%make_build package-confpods
popd

%define kata_path     /opt/confidential-containers
%define osbuilder     %{kata_path}/uvm
%define kata_bin      %{kata_path}/bin
%define kata_shim_bin %{_prefix}/local/bin
%define defaults_kata %{kata_path}/share/defaults/kata-containers

%install
pushd %{_builddir}/%{name}-%{version}/tools/osbuilder/node-builder/azure-linux
START_SERVICES=no PREFIX=%{buildroot} %make_build deploy-confpods-package
popd

mkdir -p %{buildroot}%{osbuilder}
mkdir -p %{buildroot}%{osbuilder}/src/agent
mkdir -p %{buildroot}%{osbuilder}/src/kata-opa
mkdir -p %{buildroot}%{osbuilder}/tools/osbuilder/scripts
mkdir -p %{buildroot}%{osbuilder}/tools/osbuilder/rootfs-builder
mkdir -p %{buildroot}%{osbuilder}/tools/osbuilder/image-builder
mkdir -p %{buildroot}%{osbuilder}/tools/osbuilder/igvm-builder
mkdir -p %{buildroot}%{osbuilder}/tools/osbuilder/node-builder/azure-linux

pushd %{_builddir}/%{name}-%{version}
install -D -m 0644 tools/osbuilder/Makefile %{buildroot}%{osbuilder}/tools/osbuilder/Makefile

install -D -m 0644 src/agent/Makefile %{buildroot}%{osbuilder}/src/agent/
install -D -m 0644 src/agent/kata-containers.target %{buildroot}%{osbuilder}/src/agent/
install -D -m 0644 src/agent/kata-agent.service.in %{buildroot}%{osbuilder}/src/agent/
install -D -m 0755 src/agent/target/x86_64-unknown-linux-gnu/release/kata-agent %{buildroot}%{osbuilder}/src/agent/target/x86_64-unknown-linux-gnu/release/kata-agent

install -D -m 0644 src/kata-opa/allow-all.rego %{buildroot}%{osbuilder}/src/kata-opa/
install -D -m 0644 src/kata-opa/allow-set-policy.rego %{buildroot}%{osbuilder}/src/kata-opa/

install -D -m 0644 tools/osbuilder/scripts/lib.sh %{buildroot}%{osbuilder}/tools/osbuilder/scripts/lib.sh

install -D -m 0644 tools/osbuilder/rootfs-builder/rootfs.sh %{buildroot}%{osbuilder}/tools/osbuilder/rootfs-builder/rootfs.sh
cp -aR tools/osbuilder/rootfs-builder/cbl-mariner %{buildroot}%{osbuilder}/tools/osbuilder/rootfs-builder

install -D -m 0755 tools/osbuilder/image-builder/image_builder.sh %{buildroot}%{osbuilder}/tools/osbuilder/image-builder/image_builder.sh

cp -aR tools/osbuilder/igvm-builder %{buildroot}%{osbuilder}/tools/osbuilder

install -D -m 0755 tools/osbuilder/node-builder/azure-linux/clean.sh %{buildroot}%{osbuilder}/tools/osbuilder/node-builder/azure-linux/clean.sh
install -D -m 0755 tools/osbuilder/node-builder/azure-linux/common.sh %{buildroot}%{osbuilder}/tools/osbuilder/node-builder/azure-linux/common.sh
install -D -m 0755 tools/osbuilder/node-builder/azure-linux/uvm_build.sh %{buildroot}%{osbuilder}/tools/osbuilder/node-builder/azure-linux/uvm_build.sh
popd

%preun
%systemd_preun tardev-snapshotter.service

%postun
%systemd_postun tardev-snapshotter.service

%post
%systemd_post tardev-snapshotter.service

%files
%{_sbindir}/mount.tar
%{_bindir}/kata-overlay
%{_bindir}/tardev-snapshotter
%{_unitdir}/tardev-snapshotter.service

%{kata_bin}/kata-collect-data.sh
%{kata_bin}/kata-monitor
%{kata_bin}/kata-runtime

%{defaults_kata}/configuration-clh-snp.toml
%{defaults_kata}/configuration-clh-snp-debug.toml

%{kata_shim_bin}/containerd-shim-kata-cc-v2

#%license LICENSE
#%doc CONTRIBUTING.md
#%doc README.md

%files tools
%{osbuilder}/tools/osbuilder/Makefile

%dir %{osbuilder}/src/agent
%{osbuilder}/src/agent/Makefile
%{osbuilder}/src/agent/kata-containers.target
%{osbuilder}/src/agent/kata-agent.service.in
%dir %{osbuilder}/src/agent/target/x86_64-unknown-linux-gnu/release
%{osbuilder}/src/agent/target/x86_64-unknown-linux-gnu/release/kata-agent

%dir %{osbuilder}/src/kata-opa
%{osbuilder}/src/kata-opa/allow-all.rego
%{osbuilder}/src/kata-opa/allow-set-policy.rego

%dir %{osbuilder}/tools/osbuilder/scripts
%{osbuilder}/tools/osbuilder/scripts/lib.sh

%dir %{osbuilder}/tools/osbuilder/rootfs-builder
%{osbuilder}/tools/osbuilder/rootfs-builder/rootfs.sh
%dir %{osbuilder}/tools/osbuilder/rootfs-builder/cbl-mariner
%{osbuilder}/tools/osbuilder/rootfs-builder/cbl-mariner/*

%dir %{osbuilder}/tools/osbuilder/image-builder
%{osbuilder}/tools/osbuilder/image-builder/image_builder.sh

%dir %{osbuilder}/tools/osbuilder/igvm-builder
%{osbuilder}/tools/osbuilder/igvm-builder/*

%dir %{osbuilder}/tools/osbuilder/node-builder/azure-linux
%{osbuilder}/tools/osbuilder/node-builder/azure-linux/clean.sh
%{osbuilder}/tools/osbuilder/node-builder/azure-linux/common.sh
%{osbuilder}/tools/osbuilder/node-builder/azure-linux/uvm_build.sh

%changelog
* Wed May 29 2024 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 3.2.0.azl2-1
- Auto-upgrade to 3.2.0.azl2
- Update cloud-hypervisor-snp symlink to also point to /usr/bin/cloud-hypervisor

* Thu May 02 2024 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 3.2.0.azl1-1
- Auto-upgrade to 3.2.0.azl1
- Remove opa

*   Wed Mar 13 2024 Aurelien Bombo <abombo@microsoft.com> - 3.2.0.azl0-3
-   Specify correct virtiofsd dependency

*   Thu Feb 29 2024 Dallas Delaney <dadelan@microsoft.com> - 3.2.0.azl0-2
-   Bump release to rebuild against kernel-uvm for LSG v2402.26.1

*   Mon Feb 12 2024 Aurelien Bombo <abombo@microsoft.com> - 3.2.0.azl0-1
-   Use Microsoft sources based on upstream Kata version 3.2.0.

*   Fri Feb 02 2024 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 0.6.3-4
-   Bump release to rebuild with go 1.21.6

*   Tue Jan 30 2024 Archana Choudhary <archana1@microsoft.com> - 0.6.3-3
-   Remove kernel-uvm-cvm(-devel) dependency
-   Remove kernel-uvm-cvm modules/sources/files
-   Remove instructions to build kernel-uvm-cvm related binaries

*   Wed Jan 24 2024 Manuel Huber <mahuber@microsoft.com> - 0.6.3-2
-   Enforce a restrictive security policy

*   Mon Jan 08 2024 Dallas Delaney <dadelan@microsoft.com> - 0.6.3-1
-   Upgrade to version 0.6.3

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

*   Thu Jul 13 2023 Dallas Delaney <dadelan@microsoft.com> 0.6.0-1
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
