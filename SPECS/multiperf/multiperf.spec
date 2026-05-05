Name:		 multiperf
Summary:	 IB Performance tests
Version:	 3.0
Release:        1%{?dist}
License:	 BSD 3-Clause, GPL v2 or later
Vendor:          Microsoft Corporation
Distribution:    Azure Linux
Group:		 Productivity/Networking/Diagnostic
# DOCA OFED feature sources come from the following MLNX_OFED_SRC tgz.
# This archive contains the SRPMs for each feature and each SRPM includes the source tarball and the SPEC file.
# https://linux.mellanox.com/public/repo/doca/3.2.2/SOURCES/mlnx_ofed/OFED-internal-25.10-2.4.1.tgz
Source0:         %{_distro_sources_url}/multiperf-3.0-3.2.2.tar.gz
Url:		 ""
BuildRoot:      /var/tmp/%{name}-%{version}-build

BuildRequires:  libibverbs-devel

%description
gen3 uverbs microbenchmarks

%prep
%setup -q

%build
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=%{buildroot} install

%clean
rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-, root, root)
%doc README
%license COPYING
%_bindir/*

%changelog
* Thu Apr 17 2026 Azure Linux Team - 3.0-1
- Upgrade to DOCA 3.2.2 (OFED 25.10-2.4.1)

* Mon Sep 15 2025 Elaheh Dehghani <edehghani@microsoft.com> - 3.0-2
- Enable ARM64 build by removing ExclusiveArch
* Tue Dec  17 2024 Binu Jose Philip <bphilip@microsoft.com> - 3.0-1
- Initial Azure Linux import from NVIDIA (license: GPLv2)
- License verified
* Sun Feb 08 2015 - gilr@mellanox.com
- Initial Package, Version 3.0
