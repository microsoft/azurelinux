%global debug_package %{nil}

Name:           kata-containers
Version:        3.19.1.kata2
Release:        6%{?dist}
Summary:        Kata Containers package developed for Pod Sandboxing on AKS
License:        ASL 2.0
URL:            https://github.com/microsoft/kata-containers
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Source0:        https://github.com/microsoft/kata-containers/archive/refs/tags/%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:        %{name}-%{version}-cargo.tar.gz
Patch0:         CVE-2026-24054.patch
Patch1:         rust-1.90-fixes.patch

BuildRequires:  azurelinux-release
BuildRequires:  golang
BuildRequires:  protobuf-compiler
BuildRequires:  rust >= 1.85.0
BuildRequires:  libseccomp-devel
BuildRequires:  openssl-devel
BuildRequires:  clang
BuildRequires:  device-mapper-devel
BuildRequires:  cmake

Requires:       kernel-uvm
# Must match the version specified by the `assets.virtiofsd.version` field in the source's versions.yaml.
Requires:       virtiofsd = 1.8.0
Requires:       containerd2

%description
The Kata Containers package ships the Kata components for Pod Sandboxing on AKS.
The package sources are based on a Microsoft fork of the kata-containers project and tailored to the use
for Mariner-based AKS node images.

%package tools
Summary:        Kata Containers tools package for building the UVM

%description tools
This package contains the scripts and files required to build the UVM

%prep
%autosetup -p1 -n %{name}-%{version}
pushd %{_builddir}/%{name}-%{version}
tar -xf %{SOURCE1}
popd

%build
pushd %{_builddir}/%{name}-%{version}/tools/osbuilder/node-builder/azure-linux
%make_build package
popd

%define kata_path     /opt/kata-containers
%define kata_bin      %{_prefix}/local/bin
%define kata_shim_bin %{_prefix}/local/bin
%define defaults_kata %{_prefix}/share/defaults/kata-containers
%define tools_pkg     %{kata_path}/uvm

%install
pushd %{_builddir}/%{name}-%{version}/tools/osbuilder/node-builder/azure-linux
START_SERVICES=no PREFIX=%{buildroot} %make_build deploy-package
PREFIX=%{buildroot} %make_build deploy-package-tools
popd

%files
%{kata_bin}/kata-collect-data.sh
%{kata_bin}/kata-monitor
%{kata_bin}/kata-runtime

%{defaults_kata}/configuration.toml
%{defaults_kata}/configuration-clh-debug.toml

%{kata_shim_bin}/containerd-shim-kata-v2

%license LICENSE
%doc CONTRIBUTING.md
%doc README.md

%files tools
%dir %{kata_path}
%dir %{tools_pkg}
%dir %{tools_pkg}/tools
%dir %{tools_pkg}/tools/osbuilder
%{tools_pkg}/tools/osbuilder/Makefile

%dir %{tools_pkg}/tools/osbuilder/scripts
%{tools_pkg}/tools/osbuilder/scripts/lib.sh

%dir %{tools_pkg}/tools/osbuilder/rootfs-builder
%{tools_pkg}/tools/osbuilder/rootfs-builder/rootfs.sh
%dir %{tools_pkg}/tools/osbuilder/rootfs-builder/cbl-mariner
%{tools_pkg}/tools/osbuilder/rootfs-builder/cbl-mariner/config.sh
%{tools_pkg}/tools/osbuilder/rootfs-builder/cbl-mariner/rootfs_lib.sh

%dir %{tools_pkg}/tools/osbuilder/image-builder
%{tools_pkg}/tools/osbuilder/image-builder/image_builder.sh
%{tools_pkg}/tools/osbuilder/image-builder/nsdax.gpl.c

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
* Wed Feb 11 2026 BinduSri Adabala <v-badabala@microsoft.com> - 3.19.1.kata2-6
- Bump release to rebuild with rust

* Mon Feb 02 2026 Archana Shettigar <v-shettigara@microsoft.com> - 3.19.1.kata2-5
- Bump release to rebuild with rust

* Fri Jan 29 2026 Kavya Sree Kaitepalli <kkaitepalli@microsoft.com> - 3.19.1.kata2-4
- Bump release to rebuild with rust
- Add patch to suppress dead_code warnings and add explicit lifetime for U32Set iterator

* Thu Jan 22 2026 Aurelien Bombo <abombo@microsoft.com> - 3.19.1.kata2-3
- Patch CVE-2026-24054

* Thu Oct 09 2025 Saul Paredes <saulparedes@microsoft.com> - 3.19.1.kata2-2
- Enable build on aarch64

* Mon Sep 08 2025 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 3.19.1.kata2-1
- Auto-upgrade to 3.19.1.kata2

* Wed Aug 27 2025 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 3.19.1.kata1-1
- Auto-upgrade to 3.19.1.kata1

* Fri Aug 08 2025 Azure Linux Security Servicing Account <azurelinux-security@microsoft.com> - 3.18.0.kata0-4
- Bump release to rebuild with rust

* Tue Jul 22 2025 Jyoti Kanase <v-jykanase@microsoft.com> - 3.18.0.kata0-3
- Bump release to rebuild with rust

* Mon Jul 21 2025 Saul Paredes <saulparedes@microsoft.com> - 3.18.0.kata0-2
- Add dependency on containerd2

* Wed Jun 25 2025 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 3.18.0.kata0-1
- Auto-upgrade to 3.18.0.kata0

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

* Fri Oct 25 2024 Saul Paredes <saulparedes@microsoft.com> - 3.2.0.azl3-2
- Only build for x86_64

* Fri Sep 20 2024 Manuel Huber <mahuber@microsoft.com> - 3.2.0.azl3-1
- Upgrade to 3.2.0.azl3 release, refactor build instructions

* Tue Sep 03 2024 Neha Agarwal <nehaagarwal@microsoft.com> - 3.2.0.azl2-5
- Add missing Distribution tag.

* Fri Jul 19 2024 Cameron Baird <cameronbaird@microsoft.com> 3.2.0.azl2-4
- Explicitly set OS_VERSION=3.0 for invocations of rootfs builder

* Mon Jul 15 2024 Manuel Huber <mahuber@microsoft.com> - 3.2.0.azl2-3
- Call make clean with OS distro variable

* Mon Jun 17 2024 Mitch Zhu <mitchzhu@microsoft.com> 3.2.0.azl2-2
- Enable sandbox_cgroup_only configuration
- Remove cgroupv1 kernel parameters

* Wed May 29 2024 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 3.2.0.azl2-1
- Auto-upgrade to 3.2.0.azl2

* Thu May 02 2024 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 3.2.0.azl1-1
- Auto-upgrade to 3.2.0.azl1

* Tue Mar 12 2024 Aurelien Bombo <abombo@microsoft.com> - 3.2.0.azl0-2
- Build using system OpenSSL.

* Mon Feb 12 2024 Aurelien Bombo <abombo@microsoft.com> - 3.2.0.azl0-1
- Use Microsoft sources based on upstream version 3.2.0.

* Wed Feb 07 2024 Mykhailo Bykhovtsev <mbykhovtsev@microsoft.com> - 3.1.3-2
- Update the build dependency from mariner-release to azurelinux-release

* Fri Feb 02 2024 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 3.1.0-11
- Bump release to rebuild with go 1.21.6

* Tue Dec 05 2023 Archana Choudhary <archana1@microsoft.com> - 3.1.0-10
- Drop qemu-kvm-core dependency
- Define explicit dependency on qemu-virtiofsd

* Mon Nov 06 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 3.1.3-1
- Auto-upgrade to 3.1.3 - Azure Linux 3.0 - package upgrades

* Mon Oct 16 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 3.1.0-9
- Bump release to rebuild with go 1.20.10

* Tue Oct 10 2023 Dan Streetman <ddstreet@ieee.org> - 3.1.0-8
- Bump release to rebuild with updated version of Go.

* Wed Sep 27 2023 Dallas Delaney <dadelan@microsoft.com> 3.1.0-7
- Refactor UVM build script and add -tools subpackage

* Thu Sep 14 2023 Muhammad Falak <mwani@microsoft.com> - 3.1.0-6
- Introduce patch to drop mut for variables to unblock build

* Thu Sep 07 2023 Daniel McIlvaney <damcilva@microsoft.com> - 3.1.0-5
- Bump package to rebuild with rust 1.72.0

* Mon Aug 07 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 3.1.0-4
- Bump release to rebuild with go 1.19.12

* Thu Jul 13 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 3.1.0-3
- Bump release to rebuild with go 1.19.11

* Thu Jun 15 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 3.1.0-2
- Bump release to rebuild with go 1.19.10

* Wed Apr 12 2023 Saul Paredes <saulparedes@microsoft.com> - 3.1.0-1
- Update to version 3.1.0

* Wed Apr 5 2023 Saul Paredes <saulparedes@microsoft.com> - 3.0.0-9
- Update kernel uvm image location

* Wed Apr 05 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 3.0.0-8
- Bump release to rebuild with go 1.19.8

* Tue Mar 28 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 3.0.0-7
- Bump release to rebuild with go 1.19.7

* Wed Mar 22 2023 Manuel Huber <mahuber@microsoft.com> - 3.0.0-6
- Integrate fix to reduce UVM memory consumption

* Wed Mar 15 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 3.0.0-5
- Bump release to rebuild with go 1.19.6

* Fri Feb 03 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 3.0.0-4
- Bump release to rebuild with go 1.19.5

* Wed Jan 18 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 3.0.0-3
- Bump release to rebuild with go 1.19.4

* Fri Dec 16 2022 Daniel McIlvaney <damcilva@microsoft.com> - 3.0.0-2
- Bump release to rebuild with go 1.18.8 with patch for CVE-2022-41717

* Tue Nov 15 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 3.0.0-1
- Update to v3.0.0, apply patches for compatibility with Cloud-hypervisor v27.0.60.

* Tue Nov 01 2022 Olivia Crain <oliviacrain@microsoft.com> - 2.5.0-7
- Bump release to rebuild with go 1.18.8

* Thu Sep 15 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 2.5.0-6
- Add patch to avoid memory hotplug timeout, add libseccomp.

* Mon Sep 12 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 2.5.0-5
- Generate initrd on reload.

* Tue Sep 06 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 2.5.0-4
- Set DEFSANDBOXCGROUPONLY="false".

* Fri Sep 02 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 2.5.0-3
- Add kernel config to match guest and host cgroup setup.
- Add patch to expose devices from kata.

* Wed Aug 31 2022 Andrew Phelps <anphel@microsoft.com> - 2.5.0-2
- Fix arm64 build issue by excluding configuration-acrn.toml

* Fri Aug 19 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 2.5.0-1
- Initial CBL-Mariner import from Fedora 37 (license: MIT).
- License verified.

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.2-1.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sat Jun 18 2022 Robert-AndrĂ© Mauchin <zebob.m@gmail.com> - 2.4.2-1.1
- Rebuilt for CVE-2022-1996, CVE-2022-24675, CVE-2022-28327, CVE-2022-27191,
  CVE-2022-29526, CVE-2022-30629

* Tue Jun 14 2022 Eduardo Lima (Etrunko) <etrunko@redhat.com> - 2.4.2-1
- kata-containers-2.4.2

* Thu May 12 2022 Eduardo Lima (Etrunko) <etrunko@redhat.com> - 2.4.1-1
- kata-containers-2.4.1

* Fri Apr 01 2022 Eduardo Lima (Etrunko) <etrunko@redhat.com> - 2.4.0-1
- kata-containers-2.4.0

* Wed Mar 09 2022 Eduardo Lima (Etrunko) <etrunko@redhat.com> - 2.3.3-1
- kata-containers-2.3.3

* Thu Feb 10 2022 Cole Robinson <crobinso@redhat.com> - 2.3.2-2
- Add explicit dep on /usr/libexec/virtiofsd

* Thu Feb 03 2022 Eduardo Lima (Etrunko) <etrunko@redhat.com> - 2.3.2-1
- kata-containers-2.3.2

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.0-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Nov 29 2021 Eduardo Lima (Etrunko) <etrunko@redhat.com> - 2.3.0-1
- kata-containers-2.3.0

* Mon Nov 08 2021 Eduardo Lima (Etrunko) <etrunko@redhat.com> - 2.2.3-1
- kata-containers-2.2.3

* Mon Oct 18 2021 Eduardo Lima (Etrunko) <etrunko@redhat.com> - 2.2.2-1
- kata-containers-2.2.2

* Mon Sep 27 2021 Eduardo Lima (Etrunko) <etrunko@redhat.com> - 2.2.1-1
- kata-containers-2.2.1

* Fri Sep 17 2021 Jakob Naucke <jakob.naucke@ibm.com> - 2.2.0-3
- Add an s390x build target

* Thu Sep 02 2021 Eduardo Lima (Etrunko) <etrunko@redhat.com> - 2.2.0-2
- Provide vendored code as a tarball instead of patch

* Wed Sep 01 2021 Eduardo Lima (Etrunko) <etrunko@redhat.com> - 2.2.0-1
- kata-containers-2.2.0

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-2.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu May 27 2021 Eduardo Lima (Etrunko) <etrunko@redhat.com> - 2.1.0-2
- Add the CRI-O drop-in file to the package
  Resolves: rhbz#1967594
- qemu: Update QEMU binary & its location
  Resolves: rhbz#1967602

* Thu May 27 2021 Eduardo Lima (Etrunko) <etrunko@redhat.com> - 2.1.0-1
- kata-containers 2.1.0

* Fri Apr 09 2021 Eduardo Lima (Etrunko) <etrunko@redhat.com> - 2.0.3-1
- kata-containers 2.0.3

* Tue Apr 06 2021 Eduardo Lima (Etrunko) <etrunko@redhat.com> - 2.0.2-1
- kata-containers 2.0.2

* Mon Mar 08 2021 Eduardo Lima (Etrunko) <etrunko@redhat.com> - 2.0.1-1
- Kata-containers 2.0.1

* Thu Dec 17 2020 Eduardo Lima (Etrunko) <etrunko@redhat.com> - 2.0.0-1
- Adjust package for Fedora review.

* Thu Nov 26 2020 Fabiano FidĂȘncio <fabiano@fidencio.org> - 2.0.0-0
- Initial packaging
