%global         extended_release 0.38.gd185c9b
%global         MLNX_OFED_VERSION 24.01-0.3.3.1
Summary:        IB Performance tests
Name:           perftest
# Update extended_release with version updates
Version:        24.01.0
Release:        1%{?dist}
License:        BSD or GPLv2
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Group:          Productivity/Networking/Diagnostic
URL:            https://www.openfabrics.org
Source0:        https://linux.mellanox.com/public/repo/mlnx_ofed/%{MLNX_OFED_VERSION}/SRPMS/%{name}-%{version}-%{extended_release}.tar.gz#/%{name}-%{version}.tar.gz
BuildRequires:  libibumad-devel
BuildRequires:  libibverbs-devel
BuildRequires:  librdmacm-devel
BuildRequires:  pciutils-devel

%description
gen3 uverbs microbenchmarks release: %extended_release

%prep
%autosetup -p1

%build
%configure
%{__make}
chmod -x runme

%install
%make_install

%files
%defattr(-, root, root)
%doc README runme
%license COPYING
%_bindir/*
%_mandir/man1/*.1*

%changelog
* Wed Apr 03 2024 Juan Camposeco <juanarturoc@microsoft.com> - 24.01.0-1
- Upgrade version to 24.01.0

* Wed Sep 20 2023 Jon Slobodzian <joslobo@microsoft.com> - 4.5-2
- Recompile with stack-protection fixed gcc version (CVE-2023-4039)

* Thu Jun 23 2022 Rachel Menge <rachelmenge@microsoft.com> - 4.5-1
- Initial CBL-Mariner import from NVIDIA (license: GPLv2)
- License verified

* Wed Jan 09 2013 - idos@mellanox.com
- Use autotools for building package.

* Sun Dec 30 2012 - idos@mellanox.com
- Added raw_ethernet_bw to install script.

* Sun Oct 21 2012 - idos@mellanox.com
- Removed write_bw_postlist (feature contained in all BW tests)

* Sat Oct 20 2012 - idos@mellanox.com
- Version 2.0 is underway

* Mon May 14 2012 - idos@mellanox.com
- Removed (deprecated) rdma_bw and rdma_lat tests

* Thu Feb 02 2012 - idos@mellanox.com
- Updated to 1.4.0 version (no compability with older version).

* Thu Feb 02 2012 - idos@mellanox.com
- Merge perftest code for Linux & Windows

* Sun Jan 01 2012 - idos@mellanox.com
- Added atomic benchmarks

* Sat Apr 18 2009 - hal.rosenstock@gmail.com
- Change executable names for rdma_lat and rdma_bw

* Mon Jul 09 2007 - hvogel@suse.de
- Use correct version

* Wed Jul 04 2007 - hvogel@suse.de
- Add GPL COPYING file [#289509]

* Mon Jul 02 2007 - hvogel@suse.de
- Update to the OFED 1.2 version

* Fri Jun 22 2007 - hvogel@suse.de
- Initial Package, Version 1.1
