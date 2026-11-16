%global         MLNX_OFED_VERSION 26.07.0.7.7.0
Summary:        IB Performance tests
Name:           perftest
Version:        26.07.7
Release:        1%{?dist}
License:        BSD or GPLv2
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Group:          Productivity/Networking/Diagnostic
URL:            https://www.openfabrics.org
# DOCA OFED feature sources come from the following MLNX_OFED_SRC tgz.
# This archive contains the SRPMs for each feature and each SRPM includes the source tarball and the SPEC file.
# https://linux.mellanox.com/public/repo/doca/3.5.0/SOURCES/mlnx_ofed/MLNX_OFED_SRC-26.07-0.7.7.0.tgz
Source0:        %{_distro_sources_url}/perftest-%{version}.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc-c++
BuildRequires:  libibumad-devel
BuildRequires:  libibverbs-devel
BuildRequires:  librdmacm-devel
BuildRequires:  libtool
BuildRequires:  pciutils-devel

%global __requires_exclude_from ^%{_libdir}/libperftest_kernels\.so$

%description
gen3 uverbs microbenchmarks

%prep
%autosetup -p1

%build
%configure
%{__make}
chmod -x runme

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=%{buildroot} install
echo "" > perftest-cuda.files
if [ -f libperftest_kernels.so ]; then
    install -d %{buildroot}%{_libdir}
    install -m 755 libperftest_kernels.so %{buildroot}%{_libdir}/
    echo "%{_libdir}/libperftest_kernels.so" > perftest-cuda.files
fi

%clean
rm -rf ${RPM_BUILD_ROOT}

%files -f perftest-cuda.files
%defattr(-, root, root)
%doc README runme
%license COPYING
%_bindir/*
%_mandir/man1/*.1*
%_libexecdir/perftest/cluster_mode/*.py

%changelog
* Sat Nov 14 2026 Azure Linux Team - 26.07.7-1
- Upgrade to DOCA 3.5.0 (OFED 26.07-0.7.7.0)

* Mon May 11 2026 Azure Linux Team <azurelinux@microsoft.com> - 26.01.5-1
- Upgrade to DOCA 3.3.0 (OFED 26.01-1.0.0.0)

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
