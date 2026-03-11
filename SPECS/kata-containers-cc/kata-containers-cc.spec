%global debug_package %{nil}
%define sourceName kata-containers

Name:         kata-containers-cc
Version:      3.15.0.aks0
Release:      7%{?dist}
Summary:      Kata Confidential Containers package developed for Confidential Containers on AKS
License:      ASL 2.0
URL:          https://github.com/microsoft/kata-containers
Vendor:       Microsoft Corporation
Distribution: Azure Linux
Source0:      https://github.com/microsoft/kata-containers/archive/refs/tags/%{version}.tar.gz#/%{sourceName}-%{version}.tar.gz
Source1:      %{sourceName}-%{version}-cargo.tar.gz
Patch0:       rust-1.90-fixes.patch
ExclusiveArch: x86_64

BuildRequires:  azurelinux-release
BuildRequires:  golang
BuildRequires:  protobuf-compiler
BuildRequires:  rust >= 1.85.0
BuildRequires:  libseccomp-devel
BuildRequires:  openssl-devel
BuildRequires:  clang
BuildRequires:  device-mapper-devel
BuildRequires:  cmake
BuildRequires:  fuse-devel

# kernel-uvm is required for debuggability, exercising confidential guest (confidential_guest=true)
# code paths without actual SEV SNP enablement (sev_snp_guest=false)
Requires:  kernel-uvm
Requires:  containerd2
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
%autosetup -p1 -n %{sourceName}-%{version}
pushd %{_builddir}/%{sourceName}-%{version}
tar -xf %{SOURCE1}
popd

%build
pushd %{_builddir}/%{sourceName}-%{version}/tools/osbuilder/node-builder/azure-linux
%make_build package-confpods
popd

%define kata_path     /opt/confidential-containers
%define kata_bin      %{kata_path}/bin
%define kata_shim_bin %{_prefix}/local/bin
%define defaults_kata %{kata_path}/share/defaults/kata-containers
%define tools_pkg     %{kata_path}/uvm

%install
pushd %{_builddir}/%{sourceName}-%{version}/tools/osbuilder/node-builder/azure-linux
START_SERVICES=no PREFIX=%{buildroot} %make_build deploy-confpods-package
PREFIX=%{buildroot} %make_build deploy-confpods-package-tools
popd

%preun
%systemd_preun tardev-snapshotter.service

%postun
%systemd_postun tardev-snapshotter.service

%post
%systemd_post tardev-snapshotter.service
if [ $1 -eq 1 ]; then # Package install
	systemctl enable tardev-snapshotter.service > /dev/null 2>&1 || :
	systemctl start tardev-snapshotter.service > /dev/null 2>&1 || :
fi

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

%license LICENSE
%doc CONTRIBUTING.md
%doc README.md

%files tools
%dir %{kata_path}
%dir %{tools_pkg}
%dir %{tools_pkg}/tools
%dir %{tools_pkg}/tools/osbuilder
%{tools_pkg}/tools/osbuilder/Makefile

%dir %{tools_pkg}/src
%dir %{tools_pkg}/src/kata-opa
%{tools_pkg}/src/kata-opa/allow-all.rego
%{tools_pkg}/src/kata-opa/allow-set-policy.rego
%dir %{tools_pkg}/src/tarfs
%{tools_pkg}/src/tarfs/Makefile
%{tools_pkg}/src/tarfs/tarfs.c

%dir %{tools_pkg}/tools/osbuilder/scripts
%{tools_pkg}/tools/osbuilder/scripts/lib.sh

%dir %{tools_pkg}/tools/osbuilder/rootfs-builder
%{tools_pkg}/tools/osbuilder/rootfs-builder/rootfs.sh
%dir %{tools_pkg}/tools/osbuilder/rootfs-builder/cbl-mariner
%{tools_pkg}/tools/osbuilder/rootfs-builder/cbl-mariner/config.sh
%{tools_pkg}/tools/osbuilder/rootfs-builder/cbl-mariner/rootfs_lib.sh

%dir %{tools_pkg}/tools/osbuilder/image-builder
%{tools_pkg}/tools/osbuilder/image-builder/image_builder.sh

%dir %{tools_pkg}/tools/osbuilder/igvm-builder
%{tools_pkg}/tools/osbuilder/igvm-builder/igvm_builder.sh
%dir %{tools_pkg}/tools/osbuilder/igvm-builder/azure-linux
%{tools_pkg}/tools/osbuilder/igvm-builder/azure-linux/config.sh
%{tools_pkg}/tools/osbuilder/igvm-builder/azure-linux/igvm_lib.sh

%dir %{tools_pkg}/tools/osbuilder/node-builder
%dir %{tools_pkg}/tools/osbuilder/node-builder/azure-linux
%{tools_pkg}/tools/osbuilder/node-builder/azure-linux/Makefile
%{tools_pkg}/tools/osbuilder/node-builder/azure-linux/clean.sh
%{tools_pkg}/tools/osbuilder/node-builder/azure-linux/common.sh
%{tools_pkg}/tools/osbuilder/node-builder/azure-linux/uvm_build.sh
%{tools_pkg}/tools/osbuilder/node-builder/azure-linux/uvm_install.sh

%dir %{tools_pkg}/tools/osbuilder/node-builder/azure-linux/agent-install
%dir %{tools_pkg}/tools/osbuilder/node-builder/azure-linux/agent-install/usr
%dir %{tools_pkg}/tools/osbuilder/node-builder/azure-linux/agent-install/usr/bin
%{tools_pkg}/tools/osbuilder/node-builder/azure-linux/agent-install/usr/bin/kata-agent
%dir %{tools_pkg}/tools/osbuilder/node-builder/azure-linux/agent-install/usr/lib
%dir %{tools_pkg}/tools/osbuilder/node-builder/azure-linux/agent-install/usr/lib/systemd
%dir %{tools_pkg}/tools/osbuilder/node-builder/azure-linux/agent-install/usr/lib/systemd/system
%{tools_pkg}/tools/osbuilder/node-builder/azure-linux/agent-install/usr/lib/systemd/system/kata-containers.target
%{tools_pkg}/tools/osbuilder/node-builder/azure-linux/agent-install/usr/lib/systemd/system/kata-agent.service

%changelog
* Mon Feb 02 2026 Archana Shettigar <v-shettigara@microsoft.com> - 3.15.0-aks0-7
- Bump release to rebuild with rust

* Wed Oct 15 2025 Kavya Sree Kaitepalli <kkaitepalli@microsoft.com> - 3.15.0-aks0-6
- Bump release to rebuild with rust
- Add patch to suppress dead_code warnings and add explicit lifetime for U32Set iterator

* Fri Aug 08 2025 Azure Linux Security Servicing Account <azurelinux-security@microsoft.com> - 3.15.0-aks0-5
- Bump release to rebuild with rust

* Tue Jul 22 2025 Jyoti Kanase <v-jykanase@microsoft.com> - 3.15.0.aks0-4
- Bump release to rebuild with rust

* Mon Jul 21 2025 Saul Paredes <saulparedes@microsoft.com> - 3.15.0.aks0-3
- Update dependency on containerd2

* Fri Jun 13 2025 Kavya Sree Kaitepalli <kkaitepalli@microsoft.com> - 3.15.0.aks0-2
- Bump release to rebuild with rust

* Mon Apr 28 2025 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 3.15.0.aks0-1
- Auto-upgrade to 3.15.0.aks0

* Mon Apr 21 2025 Kavya Sree Kaitepalli <kkaitepalli@microsoft.com> - 3.2.0.azl5-2
- Pin rust version

* Fri Mar 28 2025 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 3.2.0.azl5-1
- Auto-upgrade to 3.2.0.azl5

* Wed Jan 22 2025 Saul Paredes <saulparedes@microsoft.com> - 3.2.0.azl4-1
- Upgrade to 3.2.0.azl4 release

* Fri Sep 20 2024 Manuel Huber <mahuber@microsoft.com> - 3.2.0.azl3-1
- Upgrade to 3.2.0.azl3 release, refactor build instructions

* Tue Sep 03 2024 Neha Agarwal <nehaagarwal@microsoft.com> - 3.2.0.azl2-7
- Add missing Distribution tag.

* Fri Jul 19 2024 Cameron Baird <cameronbaird@microsoft.com> 3.2.0.azl2-6
- Explicitly set OS_VERSION=3.0 for invocations of rootfs builder

* Mon Jul 15 2024 Manuel Huber <mahuber@microsoft.com> - 3.2.0.azl2-5
- Call make clean with OS distro variable

* Fri Jul 12 2024 Manuel Huber <mahuber@microsoft.com> - 3.2.0.azl2-4
- Adapt make install target parameters to cope with upstream
  fork Makefile changes

* Tue Jul 02 2024 Mitch Zhu <mitchzhu@microsoft.com> 3.2.0.azl2-3
- Enable and start tardev-snapshotter.service after installation

* Mon Jun 17 2024 Mitch Zhu <mitchzhu@microsoft.com> 3.2.0.azl2-2
- Enable sandbox_cgroup_only configuration

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
-   Bump release to rebuild with go 1.20.10

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

*   Fri Jul 28 2023 Dallas Delaney <dadelan@microsoft.com> 0.6.0-1
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
