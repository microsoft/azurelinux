%global debug_package %{nil}
# The upstream GitHub tag uses dashes (e.g. 3.27.0-preview1) while RPM uses
# tilde notation for pre-release sorting.
%global upstream_ver 3.27.0-preview1

Name:           kata-containers-preview
Version:        3.27.0~preview1
Release:        1%{?dist}

Summary:        Kata Containers preview package developed for Pod Sandboxing on AKS
License:        ASL 2.0
URL:            https://github.com/microsoft/kata-containers
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Source0:        https://github.com/microsoft/kata-containers/archive/refs/tags/%{upstream_ver}.tar.gz#/%{name}-%{upstream_ver}.tar.gz
Source1:        %{name}-%{upstream_ver}-cargo.tar.gz
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

Conflicts:      kata-containers

%description
The Kata Containers preview package ships pre-release Kata components for Pod Sandboxing on AKS.
The package sources are based on the msft-preview branch of the Microsoft fork of the kata-containers
project and tailored to the use for Azure Linux-based AKS node images.

%package tools
Summary:        Kata Containers preview tools package for building the UVM

%description tools
This package contains the scripts and files required to build the UVM

%prep
%autosetup -p1 -n kata-containers-%{upstream_ver} -a 1

%build
pushd %{_builddir}/kata-containers-%{upstream_ver}/tools/osbuilder/node-builder/azure-linux
%make_build package
popd

%define kata_path     /opt/kata-containers
%define kata_bin      %{_prefix}/local/bin
%define kata_shim_bin %{_prefix}/local/bin
%define defaults_kata %{_prefix}/share/defaults/kata-containers
%define tools_pkg     %{kata_path}/uvm

%install
pushd %{_builddir}/kata-containers-%{upstream_ver}/tools/osbuilder/node-builder/azure-linux
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
* Mon Mar 10 2026 Roman Mohyla <romoh@microsoft.com> - 3.27.0~preview1-1
- Initial kata-containers-preview package based on msft-preview branch (upstream 3.27.0)
