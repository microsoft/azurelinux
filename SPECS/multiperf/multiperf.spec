Name:		 multiperf
Summary:	 IB Performance tests
Version:	 3.0
Release:	 1_3.0.2410068
License:	 BSD 3-Clause, GPL v2 or later
Vendor:		 Microsoft Corporation
Distribution:	 Azure Linux
Group:		 Productivity/Networking/Diagnostic
# Source:        https://linux.mellanox.com/public/repo/mlnx_ofed/latest/SRPMS/multiperf-3.0.tar.gz
Source:		 %{name}-%{version}.tar.gz
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
%doc README COPYING
%_bindir/*

%changelog
* Tue Dec  3 2024 Binu Jose Philip <bphilip@microsoft.com>
- Moving to proprietary repo and add minor release prefix
* Thu Nov 07 2024 Suresh Babu Chalamalasetty <schalam@microsoft.com>
- Initial version Azure Linux
* Sun Feb 08 2015 - gilr@mellanox.com
- Initial Package, Version 3.0
