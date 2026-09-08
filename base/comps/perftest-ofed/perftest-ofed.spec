%global upstream_name perftest

Name:           perftest-ofed
Summary:        IB Performance tests
Version: 26.04.16
Release: 1%{?dist}
Conflicts:      perftest
License:        BSD 3-Clause, GPL v2 or later
Group:          Productivity/Networking/Diagnostic
Source6000:     MLNX_OFED_SRC-26.04-0.8.5.0.tgz
Url:            http://www.openfabrics.org
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildRequires:  rdma-core-ofed-devel
BuildRequires:  pciutils-devel
BuildRequires:  autoconf automake gcc-c++ libtool

%global __requires_exclude_from ^%{_libdir}/libperftest_kernels\.so$

%description
gen3 uverbs microbenchmarks

%prep
tar -xf %{SOURCE6000}
_perftest_srpm=$(find MLNX_OFED_SRC-* -path '*/SRPMS/perftest-%{version}-*.src.rpm' -print -quit)
if [ -z "$_perftest_srpm" ]; then
    echo "ERROR: perftest source RPM not found inside %{SOURCE6000}" >&2
    exit 1
fi
rpm2cpio "$_perftest_srpm" | cpio -idm './perftest-%{version}.tar.gz'
rm -rf MLNX_OFED_SRC-*
tar -xf perftest-%{version}.tar.gz
%setup -q -T -D -n %{upstream_name}-%{version}

%build
%configure \
%if %{?_cuda_h_path:1}0
        CUDA_H_PATH=%{_cuda_h_path}
%endif
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
%doc README COPYING runme
%_bindir/*
%_mandir/man1/*.1*

%changelog
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
