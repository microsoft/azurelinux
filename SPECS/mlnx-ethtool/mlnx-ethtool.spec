Name:		 mlnx-ethtool
Version:	 6.14
Release:	 1%{?dist}
Group:		 Utilities
Summary:	 Settings tool for Ethernet and other network devices
License:	 GPLv2
Vendor:          Microsoft Corporation
Distribution:    Azure Linux
URL:		 https://ftp.kernel.org/pub/software/network/ethtool/
Buildroot:	 /var/tmp/%{name}-%{version}-build
# DOCA OFED feature sources come from the following MLNX_OFED_SRC tgz.
# This archive contains the SRPMs for each feature and each SRPM includes the source tarball and the SPEC file.
# https://linux.mellanox.com/public/repo/doca/3.1.0/SOURCES/mlnx_ofed/MLNX_OFED_SRC-25.07-0.9.7.0.tgz
Source0:         %{_distro_sources_url}/%{name}-%{version}.tar.gz

BuildRequires:  libmnl-devel

Provides:       ethtool
# To avoid file conflicts
Conflicts:      ethtool

%description
This utility allows querying and changing settings such as speed,
port, auto-negotiation, PCI locations and checksum offload on many
network devices, especially Ethernet devices.

%prep
%setup -q


%build
CFLAGS="${RPM_OPT_FLAGS}" ./configure --prefix=%{_prefix} --mandir=%{_mandir}
make


%install
make install DESTDIR=${RPM_BUILD_ROOT}


%files
%defattr(-,root,root)
%{_sbindir}/ethtool
%{_mandir}/man8/ethtool.8*
%{_datadir}/bash-completion/completions/ethtool
%{_datadir}/metainfo/org.kernel.software.network.ethtool.metainfo.xml
%doc AUTHORS NEWS README
%license COPYING


%changelog
* Thu Dec 11 2025 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 6.14-1
- Upgrade version to 6.14.
- Update source path
* Tue Nov 11 2025 Mayank Singh <mayansingh@microsoft.com> - 6.9-4
- Updated dependency handling for kexec-tools:
  Changed from hard dependency on a single package.
  Allows installation to satisfy dependency with either `ethtool` or `mlnx-ethtool`.
  Ensures flexibility for image builds and user choice at install time.
  Added mutual exclusivity between providers to prevent file conflicts.
* Mon Sep 15 2025 Elaheh Dehghani <edehghani@microsoft.com> - 6.9-3
- Enable ARM64 build by removing ExclusiveArch
* Tue Dec  17 2024 Binu Jose Philip <bphilip@microsoft.com> - 6.9-2
- Initial Azure Linux import from NVIDIA (license: GPLv2)
- License verified
