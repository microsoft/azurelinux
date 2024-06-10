%global debug_package %{nil}

Name:           kata-containers
Version:        3.2.0.azl2
Release:        1%{?dist}
Summary:        Kata Containers package developed for Pod Sandboxing on AKS
License:        ASL 2.0
Vendor:         Microsoft Corporation
URL:            https://github.com/microsoft/kata-containers
Source0:        https://github.com/microsoft/kata-containers/archive/refs/tags/%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:        %{name}-%{version}-cargo.tar.gz

BuildRequires:  golang
BuildRequires:  protobuf-compiler
BuildRequires:  rust
BuildRequires:  libseccomp-devel
BuildRequires:  openssl-devel
BuildRequires:  clang
BuildRequires:  device-mapper-devel
BuildRequires:  cmake

Requires:       kernel-uvm
# Must match the version specified by the `assets.virtiofsd.version` field in the source's versions.yaml.
Requires:       virtiofsd = 1.8.0

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

%define kata_path     /usr
%define osbuilder     %{kata_path}/uvm
%define kata_bin      %{kata_path}/local/bin
%define kata_shim_bin %{_prefix}/local/bin
%define defaults_kata %{kata_path}/share/defaults/kata-containers

%install
pushd %{_builddir}/%{name}-%{version}/tools/osbuilder/node-builder/azure-linux
START_SERVICES=no PREFIX=%{buildroot} %make_build deploy-package
popd

mkdir -p %{buildroot}%{osbuilder}
mkdir -p %{buildroot}%{osbuilder}/src/agent
mkdir -p %{buildroot}%{osbuilder}/tools/osbuilder/scripts
mkdir -p %{buildroot}%{osbuilder}/tools/osbuilder/rootfs-builder
mkdir -p %{buildroot}%{osbuilder}/tools/osbuilder/initrd-builder
mkdir -p %{buildroot}%{osbuilder}/tools/osbuilder/node-builder/azure-linux

pushd %{_builddir}/%{name}-%{version}
install -D -m 0644 tools/osbuilder/Makefile %{buildroot}%{osbuilder}/tools/osbuilder/Makefile

install -D -m 0644 src/agent/Makefile %{buildroot}%{osbuilder}/src/agent/
install -D -m 0644 src/agent/kata-containers.target %{buildroot}%{osbuilder}/src/agent/
install -D -m 0644 src/agent/kata-agent.service.in %{buildroot}%{osbuilder}/src/agent/
install -D -m 0755 src/agent/target/x86_64-unknown-linux-gnu/release/kata-agent %{buildroot}%{osbuilder}/src/agent/target/x86_64-unknown-linux-gnu/release/kata-agent

install -D -m 0644 tools/osbuilder/scripts/lib.sh %{buildroot}%{osbuilder}/tools/osbuilder/scripts/lib.sh

install -D -m 0644 tools/osbuilder/rootfs-builder/rootfs.sh %{buildroot}%{osbuilder}/tools/osbuilder/rootfs-builder/rootfs.sh
cp -aR tools/osbuilder/rootfs-builder/cbl-mariner %{buildroot}%{osbuilder}/tools/osbuilder/rootfs-builder

install -D -m 0755 tools/osbuilder/initrd-builder/initrd_builder.sh %{buildroot}%{osbuilder}/tools/osbuilder/initrd-builder/initrd_builder.sh

install -D -m 0755 tools/osbuilder/node-builder/azure-linux/clean.sh %{buildroot}%{osbuilder}/tools/osbuilder/node-builder/azure-linux/clean.sh
install -D -m 0755 tools/osbuilder/node-builder/azure-linux/common.sh %{buildroot}%{osbuilder}/tools/osbuilder/node-builder/azure-linux/common.sh
install -D -m 0755 tools/osbuilder/node-builder/azure-linux/uvm_build.sh %{buildroot}%{osbuilder}/tools/osbuilder/node-builder/azure-linux/uvm_build.sh
popd

%files
%{kata_bin}/kata-collect-data.sh
%{kata_bin}/kata-monitor
%{kata_bin}/kata-runtime

%{defaults_kata}/configuration-clh.toml

%{kata_shim_bin}/containerd-shim-kata-v2

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

%dir %{osbuilder}/tools/osbuilder/scripts
%{osbuilder}/tools/osbuilder/scripts/lib.sh

%dir %{osbuilder}/tools/osbuilder/rootfs-builder
%{osbuilder}/tools/osbuilder/rootfs-builder/rootfs.sh
%dir %{osbuilder}/tools/osbuilder/rootfs-builder/cbl-mariner
%{osbuilder}/tools/osbuilder/rootfs-builder/cbl-mariner/*

%dir %{osbuilder}/tools/osbuilder/initrd-builder
%{osbuilder}/tools/osbuilder/initrd-builder/initrd_builder.sh

%dir %{osbuilder}/tools/osbuilder/node-builder/azure-linux
%{osbuilder}/tools/osbuilder/node-builder/azure-linux/clean.sh
%{osbuilder}/tools/osbuilder/node-builder/azure-linux/common.sh
%{osbuilder}/tools/osbuilder/node-builder/azure-linux/uvm_build.sh

%changelog
* Wed May 29 2024 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 3.2.0.azl2-1
- Auto-upgrade to 3.2.0.azl2

* Thu May 02 2024 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 3.2.0.azl1-1
- Auto-upgrade to 3.2.0.azl1

* Tue Mar 12 2024 Aurelien Bombo <abombo@microsoft.com> - 3.2.0.azl0-2
- Build using system OpenSSL.

* Mon Feb 12 2024 Aurelien Bombo <abombo@microsoft.com> - 3.2.0.azl0-1
- Use Microsoft sources based on upstream version 3.2.0.

* Fri Feb 02 2024 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 3.1.0-11
- Bump release to rebuild with go 1.21.6

* Tue Dec 05 2023 Archana Choudhary <archana1@microsoft.com> - 3.1.0-10
- Drop qemu-kvm-core dependency
- Define explicit dependency on qemu-virtiofsd

* Mon Oct 16 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 3.1.0-9
- Bump release to rebuild with go 1.20.9

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
