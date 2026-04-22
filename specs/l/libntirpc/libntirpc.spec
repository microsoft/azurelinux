# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.


#%%global		dev rc3

Name:		libntirpc
Version:	7.2
Release: 2%{?dev:%{dev}}%{?dist}
Summary:	New Transport Independent RPC Library
License:	BSD-3-Clause
Url:		https://github.com/nfs-ganesha/ntirpc

%global prometh_ver_long	48d09c45ee6deb90e02579b03037740e1c01fd27
%global prometh_ver_short	48d09c45
Source0:	https://github.com/nfs-ganesha/ntirpc/archive/v%{version}/ntirpc-%{version}%{?dev:%{dev}}.tar.gz
Source1:	https://github.com/biaks/prometheus-cpp-lite/archive/%{prometh_ver_long}/prometheus-cpp-lite-%{prometh_ver_short}.tar.gz
Patch:		0001-CMakeLists.txt.patch

BuildRequires:	cmake gcc gcc-c++
%ifarch x86_64 aarch64
BuildRequires:	mold
%endif
BuildRequires:	librdmacm
BuildRequires:	rdma-core-devel
BuildRequires:	krb5-devel
BuildRequires:	userspace-rcu-devel
%if ( 0%{?fedora} && 0%{?fedora} > 27 )
BuildRequires:  libnsl2-devel
%endif
# libtirpc has /etc/netconfig, most machines probably have it anyway
# for NFS client
Requires:	libtirpc

%description
This package contains a new implementation of the original libtirpc, 
transport-independent RPC (TI-RPC) library for NFS-Ganesha. It has
the following features not found in libtirpc:
 1. Bi-directional operation
 2. Full-duplex operation on the TCP (vc) transport
 3. Thread-safe operating modes
 3.1 new locking primitives and lock callouts (interface change)
 3.2 stateless send/recv on the TCP transport (interface change)
 4. Flexible server integration support
 5. Event channels (remove static arrays of xprt handles, new EPOLL/KEVENT
    integration)

%package devel
Summary:	Development headers for %{name}
Requires:	%{name}%{?_isa} = %{version}

%description devel
Development headers and auxiliary files for developing with %{name}.

%prep
tar xpf %{SOURCE1}
%autosetup -p1 -n ntirpc-%{version}%{?dev:%{dev}}

%build
export VERBOSE=1
mv ../prometheus-cpp-lite-%{prometh_ver_long}/* ./src/monitoring/prometheus-cpp-lite
%cmake \
    -DOVERRIDE_INSTALL_PREFIX=/usr \
    -DCMAKE_BUILD_TYPE=RelWithDebInfo \
    -DCMAKE_COLOR_MAKEFILE:BOOL=OFF \
    -DTIRPC_EPOLL=1 \
    -DUSE_GSS=ON \
    -DUSE_RPC_RDMA=ON \
%ifarch x86_64 aarch64
    -DCMAKE_LINKER=%{_bindir}/ld.mold \
%endif
    "-GUnix Makefiles"

export GCC_COLORS=
%cmake_build

%install
## make install is broken in various ways
## make install DESTDIR=%%{buildroot}
mkdir -p %{buildroot}%{_libdir}/pkgconfig

%cmake_install
install -p -m 644 src/monitoring/include/monitoring.h %{buildroot}%{_includedir}/ntirpc
mv src/monitoring/prometheus-cpp-lite/core/include/prometheus %{buildroot}%{_includedir}/ntirpc
ln -s %{name}.so.%{version} %{buildroot}%{_libdir}/%{name}.so.7

%files
%{_libdir}/libntirpc.so.*
%{_libdir}/libntirpcmonitoring.so.*
%{!?_licensedir:%global license %%doc}
%license COPYING
%doc NEWS README

%files devel
%{_libdir}/libntirpc.so
%{_libdir}/libntirpcmonitoring.so
%{_includedir}/ntirpc/
%{_libdir}/pkgconfig/libntirpc.pc

%changelog
* Tue Sep 30 2025 Kaleb S. KEITHLEY <kkeithle at redhat.com> 7.2-1
- ntirpc-7.2 GA

* Tue Jul 29 2025 Kaleb S. KEITHLEY <kkeithle at redhat.com> 7.0-1
- ntirpc-7.0 GA

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 6.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jul 17 2025 Cristian Le <git@lecris.dev> - 6.3-4
- Fix CMake 4.0 patch

* Wed Jul 16 2025 Kaleb S. KEITHLEY <kkeithle at redhat.com> 6.3-3
- ntirpc-6.3, rhbz#2380748

* Mon Jan 20 2025 Fedora Release Engineering <releng@fedoraproject.org> - 6.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Nov 25 2024 Kaleb S. KEITHLEY <kkeithle at redhat.com> 6.3-1
- ntirpc-6.3 GA

* Wed Aug 28 2024 Kaleb S. KEITHLEY <kkeithle at redhat.com> 6.0-2
- ntirpc-6.0, enable RDMA

* Mon Aug 26 2024 Kaleb S. KEITHLEY <kkeithle at redhat.com> 6.0-1
- ntirpc-6.0 GA

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon May 20 2024 Kaleb S. KEITHLEY <kkeithle at redhat.com> 5.8-1
- ntirpc-5.8 GA
- N.B. there were no intervening 5.1-5.7 releases, sync w/ ganesha version

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Kaleb S. KEITHLEY <kkeithle at redhat.com> 5.0-3
- rebuild with gcc-14

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild
- rhbz#2225972

* Fri Apr 21 2023 Kaleb S. KEITHLEY <kkeithle at redhat.com> 5.0-1
- ntirpc-5.0 GA

* Fri Jan 20 2023 Kaleb S. KEITHLEY <kkeithle at redhat.com> 4.3-1
- ntirpc-4.3 GA

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Nov 22 2022 Kaleb S. KEITHLEY <kkeithle at redhat.com> 4.2-1
- ntirpc-4.2 GA

* Fri Nov 18 2022 Kaleb S. KEITHLEY <kkeithle at redhat.com> 4.1-1
- ntirpc-4.1 GA

* Fri Nov 11 2022 Kaleb S. KEITHLEY <kkeithle at redhat.com>
- SPDX migration

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Mar 4 2022 Kaleb S. KEITHLEY <kkeithle at redhat.com> - 4.0-5
- rebuild w/ cmake-2.23

* Wed Jan 26 2022 Kaleb S. KEITHLEY <kkeithle at redhat.com> - 4.0-4
- rebuild w/ modern linker (mold), this time for real

* Wed Jan 26 2022 Kaleb S. KEITHLEY <kkeithle at redhat.com> - 4.0-3
- rebuild w/ modern linker (mold)

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Dec 17 2021 Kaleb S. KEITHLEY <kkeithle at redhat.com> 4.0-1
- ntirpc-4.0 GA

* Wed Dec 15 2021 Kaleb S. KEITHLEY <kkeithle at redhat.com> 4.0-0.3rc3
- ntirpc-4.0 RC3

* Fri Dec 3 2021 Kaleb S. KEITHLEY <kkeithle at redhat.com> 4.0-0.2rc2
- ntirpc-4.0 RC2

* Mon Nov 8 2021 Kaleb S. KEITHLEY <kkeithle at redhat.com> 4.0-0.1rc1
- ntirpc-4.0 RC1

* Fri Jul 30 2021 Kaleb S. KEITHLEY <kkeithle at redhat.com> 3.5-5
- use %{_vpath_builddir}

* Thu Jul 29 2021 Kaleb S. KEITHLEY <kkeithle at redhat.com> 3.5-4
- bz#1987653, FTBFS

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jun 22 2021 Kaleb S. KEITHLEY <kkeithle at redhat.com> 3.5-2
- Rebuilt for userspace-rcu-0.13 again

* Tue Jun 15 2021 Kaleb S. KEITHLEY <kkeithle at redhat.com> 3.5-1
- libntirpc 3.5 GA

* Tue Jun 8 2021 Kaleb S. KEITHLEY <kkeithle at redhat.com> 3.4-3
- Rebuilt for userspace-rcu-0.13

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Dec 23 2020 Kaleb S. KEITHLEY <kkeithle at redhat.com> 3.4-1
- libntirpc 3.4 GA

* Thu Jul 30 2020 Kaleb S. KEITHLEY <kkeithle at redhat.com> 3.3-4
- missing version.h since 3.3-2

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 20 2020 Kaleb S. KEITHLEY <kkeithle at redhat.com> 3.3-2
- use %cmake_build

* Mon Jun 8 2020 Kaleb S. KEITHLEY <kkeithle at redhat.com> 3.3-1
- libntirpc 3.3 GA

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Dec 17 2019 Kaleb S. KEITHLEY <kkeithle at redhat.com> 3.2-1
- libntirpc 3.2 GA

* Fri Dec 13 2019 Kaleb S. KEITHLEY <kkeithle at redhat.com> 3.1-1
- libntirpc 3.1 GA (not built)

* Mon Nov 18 2019 Kaleb S. KEITHLEY <kkeithle at redhat.com> 3.0-2
- libntirpc 3.0, libntirpc.so.1 -> libntirpc.so.3

* Wed Nov 6 2019 Kaleb S. KEITHLEY <kkeithle at redhat.com> 3.0-1
- libntirpc 3.0 GA

* Sun Nov 3 2019 Kaleb S. KEITHLEY <kkeithle at redhat.com> 3.0-0.1rc2
- libntirpc 3.0 RC2

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu May 30 2019 Kaleb S. KEITHLEY <kkeithle at redhat.com> 1.8.0-1
- libntirpc 1.8.0 GA, bz#1715590

* Tue Apr 2 2019 Kaleb S. KEITHLEY <kkeithle at redhat.com> 1.7.3-1
- libntirpc 1.7.3 GA

* Wed Feb 27 2019 Kaleb S. KEITHLEY <kkeithle at redhat.com> 1.7.2-1
- libntirpc 1.7.2 GA

* Wed Feb 20 2019 Kaleb S. KEITHLEY <kkeithle at redhat.com> 1.7.1-1
- rebuild for f31/rawhide

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Oct 16 2018 Kaleb S. KEITHLEY <kkeithle at redhat.com> 1.7.1-1
- libntirpc 1.7.1 GA

* Mon Sep 17 2018 Kaleb S. KEITHLEY <kkeithle at redhat.com> 1.7.0-1
- libntirpc 1.7.0 GA

* Wed Aug 22 2018 Kaleb S. KEITHLEY <kkeithle at redhat.com> 1.6.3-1
- libntirpc 1.6.3 GA

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Mar 20 2018 Kaleb S. KEITHLEY <kkeithle at redhat.com> 1.6.2-1
- libntirpc 1.6.2 GA

* Mon Feb 19 2018 Kaleb S. KEITHLEY <kkeithle at redhat.com> 1.6.1-3
- gcc BuildRoot

* Thu Feb 15 2018 Kaleb S. KEITHLEY <kkeithle at redhat.com> 1.6.1-2
- ldconfig

* Fri Feb 9 2018 Kaleb S. KEITHLEY <kkeithle at redhat.com> 1.6.1-1
- libntirpc 1.6.1 GA

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jan 17 2018 Kaleb S. KEITHLEY <kkeithle at redhat.com> 1.6.0-1
- libntirpc 1.6.0 GA

* Thu Oct 19 2017 Kaleb S. KEITHLEY <kkeithle at redhat.com> 1.5.3-4
- libntirpc 1.5.3 PR https://github.com/nfs-ganesha/ntirpc/pull/85

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jul 19 2017 Kaleb S. KEITHLEY <kkeithle at redhat.com> 1.5.3-1
- libntirpc 1.5.3 GA

* Tue May 30 2017 Kaleb S. KEITHLEY <kkeithle at redhat.com> 1.5.2-1
- libntirpc 1.5.2 GA

* Mon May 8 2017 Kaleb S. KEITHLEY <kkeithle at redhat.com> 1.5.1-1
- libntirpc 1.5.1 GA

* Fri Apr 21 2017 Kaleb S. KEITHLEY <kkeithle at redhat.com> 1.5.0-1
- libntirpc 1.5.0 GA

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Oct 25 2016 Kaleb S. KEITHLEY <kkeithle at redhat.com> 1.4.3-1
- libntirpc 1.4.3 GA

* Tue Oct 25 2016 Kaleb S. KEITHLEY <kkeithle at redhat.com> 1.4.2-1
- libntirpc 1.4.2 GA

* Tue Sep 20 2016 Kaleb S. KEITHLEY <kkeithle at redhat.com> 1.4.1-1
- libntirpc 1.4.1 GA

* Mon Sep 19 2016 Kaleb S. KEITHLEY <kkeithle at redhat.com> 1.4.0-1
- libntirpc 1.4.0 GA

* Tue Sep 6 2016 Kaleb S. KEITHLEY <kkeithle at redhat.com> 1.4.0-0.4pre3
- libntirpc 1.4.0-pre3, without jemalloc

* Thu Aug 4 2016 Kaleb S. KEITHLEY <kkeithle at redhat.com> 1.4.0-0.3pre3
- libntirpc 1.4.0-pre3

* Mon Feb 29 2016 Kaleb S. KEITHLEY <kkeithle at redhat.com> 1.4.0-0.2pre2
- libntirpc 1.4.0-pre2

* Fri Feb 5 2016 Kaleb S. KEITHLEY <kkeithle at redhat.com> 1.4.0-0.1pre1
- libntirpc 1.4.0-pre1, correct release

* Fri Feb 5 2016 Kaleb S. KEITHLEY <kkeithle at redhat.com> 1.4.0-1pre1
- libntirpc 1.4.0-pre1

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Dec 9 2015 Kaleb S. KEITHLEY <kkeithle at redhat.com>
- Requires: libtirpc for /etc/netconfig (most already have it)

* Mon Oct 26 2015 Kaleb S. KEITHLEY <kkeithle at redhat.com> 1.3.1-1
- libntirpc 1.3.1 GA

* Fri Oct 9 2015 Kaleb S. KEITHLEY <kkeithle at redhat.com> 1.3.0-3
- libntirpc 1.3.0 GA, w/ -DTIRPC_EPOLL=ON

* Wed Sep 9 2015 Kaleb S. KEITHLEY <kkeithle at redhat.com> 1.3.0-2
- libntirpc 1.3.0 GA, w/ correct top-level CMakeList.txt

* Wed Sep 9 2015 Kaleb S. KEITHLEY <kkeithle at redhat.com> 1.3.0-1
- libntirpc 1.3.0 GA

* Thu Jul 16 2015 Kaleb S. KEITHLEY <kkeithle at redhat.com> 1.2.1-3
- RHEL 6 finally has new enough cmake
- use -isystem ... to ensure correct <rpc/rpc*.h> are used
- ensure -DTIRPC_EPOLL is defined for correct evchan functionality

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Mar 23 2015 Kaleb S. KEITHLEY <kkeithle at redhat.com> 1.2.1-1
- Initial commit
