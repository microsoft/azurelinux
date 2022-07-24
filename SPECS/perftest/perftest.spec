%global extended-release 0.14.gd962d8c.56068 

Summary:        IB Performance tests
Name:           perftest
Version:        4.5
Release:        1%{?dist}
License:        BSD 3-Clause, GPL v2 or later
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Productivity/Networking/Diagnostic
URL:            http://www.openfabrics.org
#Source0:       https://linux.mellanox.com/public/repo/doca/1.3.0/extras/mlnx_ofed/5.6-1.0.3.3/SOURCES/perftest_4.5.orig.tar.gz
Source0:        perftest-%{version}.tar.gz
BuildRequires:  libibumad-devel
BuildRequires:  libibverbs-devel
BuildRequires:  librdmacm-devel 
BuildRequires:  pciutils-devel

%description
gen3 uverbs microbenchmarks

%prep
%autosetup -p1

%build
%configure \
%{__make}
chmod -x runme

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install

%clean
rm -rf %{buildroot}

%files
%defattr(-, root, root)
%doc README runme
%license COPYING
%_bindir/*

%changelog
* Thu Jun 23 2022 Rachel Menge <rachelmenge@microsoft.com> - 4.5-1
- Initial CBL-Mariner import from NVIDIA (license: ASL 2.0)
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
