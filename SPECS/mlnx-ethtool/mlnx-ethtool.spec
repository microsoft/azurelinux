Name:		 mlnx-ethtool
Version:	 6.9
Release:	 4%{?dist}
Group:		 Utilities
Summary:	 Settings tool for Ethernet and other network devices
License:	 GPLv2
Vendor:          Microsoft Corporation
Distribution:    Azure Linux
URL:		 https://ftp.kernel.org/pub/software/network/ethtool/
Buildroot:	 /var/tmp/%{name}-%{version}-build
Source0:         https://linux.mellanox.com/public/repo/mlnx_ofed/24.10-0.7.0.0/SRPMS/mlnx-ethtool-6.9.tar.gz#/%{name}-%{version}.tar.gz

BuildRequires:  libmnl-devel

# Virtual capability
Provides:       ethtool-capability

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
%doc AUTHORS NEWS README
%license COPYING


%changelog
* Tue Nov 11 2025 Mayank Singh <mayansingh@microsoft.com> - 6.9-4
- Make kexec-tools depend on a capability instead of a specific package name.
  Lets the user (or image build) choose either ethtool or mlnx-ethtool at install time,
  while preventing file conflicts by making the providers mutually exclusive.

* Mon Sep 15 2025 Elaheh Dehghani <edehghani@microsoft.com> - 6.9-3
- Enable ARM64 build by removing ExclusiveArch
* Tue Dec  17 2024 Binu Jose Philip <bphilip@microsoft.com> - 6.9-2
- Initial Azure Linux import from NVIDIA (license: GPLv2)
- License verified
