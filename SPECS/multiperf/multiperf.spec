Name:		 multiperf
Summary:	 IB Performance tests
Version:	 3.0
Release:	 2%{?dist}
License:	 BSD 3-Clause, GPL v2 or later
Vendor:          Microsoft Corporation
Distribution:    Azure Linux
Group:		 Productivity/Networking/Diagnostic
Source0:         https://linux.mellanox.com/public/repo/mlnx_ofed/24.10-0.7.0.0/SRPMS/multiperf-3.0.tar.gz#/%{name}-%{version}.tar.gz
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
* Mon Sep 15 2025 Elaheh Dehghani <edehghani@microsoft.com> - 3.0-2
- Enable ARM64 build by removing ExclusiveArch
* Tue Dec  17 2024 Binu Jose Philip <bphilip@microsoft.com> - 3.0-1
- Initial Azure Linux import from NVIDIA (license: GPLv2)
- License verified
* Sun Feb 08 2015 - gilr@mellanox.com
- Initial Package, Version 3.0
