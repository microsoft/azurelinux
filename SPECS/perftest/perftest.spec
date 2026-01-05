%global         extended_release 0.104.g0c03534
%global         MLNX_OFED_VERSION 25.07-0.9.7.1
Summary:        IB Performance tests
Name:           perftest
# Update extended_release with version updates
Version:        25.07.0
Release:        1%{?dist}
License:        BSD or GPLv2
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Group:          Productivity/Networking/Diagnostic
URL:            https://www.openfabrics.org
# DOCA OFED feature sources come from the following MLNX_OFED_SRC tgz.
# This archive contains the SRPMs for each feature and each SRPM includes the source tarball and the SPEC file.
# https://linux.mellanox.com/public/repo/doca/3.1.0/SOURCES/mlnx_ofed/MLNX_OFED_SRC-25.07-0.9.7.0.tgz
Source0:        %{_distro_sources_url}/%{name}-%{version}-%{extended_release}.tar.gz
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
* Tue Nov 04 2025 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 25.07.0-1
- Upgrade version to 25.07.0.
- Update source path

* Wed Jan 08 2025 Alberto David Perez Guevara <aperezguevar@microsoft.com> - 24.10.0-1
- Upgrade version to 24.10.0

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
