Vendor:         Microsoft Corporation
Distribution:   Mariner
%global min_libpmemobj_ver 1.8
%global upstreamversion 1.9

Name:		libpmemobj-cpp
Version:	1.9
Release:	4%{?dist}
Summary:	C++ bindings for libpmemobj
# Note: tests/external/libcxx is dual licensed using University of Illinois "BSD-Like" license and the MIT license. It's used only during development/testing and is NOT part of the binary RPM.
License:	BSD
URL:		http://pmem.io/pmdk/cpp_obj/

Source0:	https://github.com/pmem/%{name}/archive/%{upstreamversion}.tar.gz#/%{name}-%{upstreamversion}.tar.gz

BuildRequires:	libpmemobj-devel >= %{min_libpmemobj_ver}
BuildRequires:	cmake >= 3.3
BuildRequires:	glibc-devel
BuildRequires:	gcc-c++
BuildRequires:	pkgconfig
BuildRequires:	doxygen
BuildRequires:	perl-Encode
BuildRequires:	gdb

# Test dependencies break the package build.
# Disabling until fixed.
# %if %{with_check}
# BuildRequires:	ncurses-devel
# BuildRequires:	libunwind-devel
# BuildRequires:	valgrind-devel
# BuildRequires:	tbb-devel

# Missing test dependencies:
# BuildRequires:	SFML-devel
# %endif

# There's nothing x86-64 specific in this package, but we have
# to duplicate what spec for pmdk/libpmemobj has at the moment.
# Relevant bug reports:
# https://bugzilla.redhat.com/show_bug.cgi?id=1340634
# https://bugzilla.redhat.com/show_bug.cgi?id=1340635
# https://bugzilla.redhat.com/show_bug.cgi?id=1340636
# https://bugzilla.redhat.com/show_bug.cgi?id=1340637
ExclusiveArch: x86_64

%description
This package contains header files for libpmemobj C++ bindings and C++
containers built on top of them.

# Specify a virtual Provide for libpmemobj++-static package, so the package
# usage can be tracked.
%package -n libpmemobj++-devel
Summary: C++ bindings for Persistent Memory Transactional Object Store library
Provides: libpmemobj++-static = %{version}-%{release}
Requires: libpmemobj-devel >= %{min_libpmemobj_ver}

%description -n libpmemobj++-devel
This package contains header files for libpmemobj C++ bindings and C++
containers built on top of them.

The libpmemobj library provides a transactional object store,
providing memory allocation, transactions, and general facilities for
persistent memory programming.

%files -n libpmemobj++-devel
%{_libdir}/pkgconfig/libpmemobj++.pc
%dir %{_includedir}/libpmemobj++
%{_includedir}/libpmemobj++/*.hpp
%dir %{_includedir}/libpmemobj++/detail
%{_includedir}/libpmemobj++/detail/*.hpp
%dir %{_includedir}/libpmemobj++/container
%{_includedir}/libpmemobj++/container/*.hpp
%dir %{_includedir}/libpmemobj++/container/detail
%{_includedir}/libpmemobj++/container/detail/*.hpp
%dir %{_includedir}/libpmemobj++/experimental
%{_includedir}/libpmemobj++/experimental/*.hpp
%dir %{_libdir}/libpmemobj++
%dir %{_libdir}/libpmemobj++/cmake
%{_libdir}/libpmemobj++/cmake/libpmemobj++-config-version.cmake
%{_libdir}/libpmemobj++/cmake/libpmemobj++-config.cmake

%license LICENSE

%doc ChangeLog README.md

%package -n libpmemobj++-doc
Summary: HTML documentation for libpmemobj++

%description -n libpmemobj++-doc
HTML documentation for libpmemobj++.

%files -n libpmemobj++-doc
%dir %{_docdir}/libpmemobj++
%{_docdir}/libpmemobj++/*

%license LICENSE

%doc ChangeLog README.md

%global debug_package %{nil}

%prep
%setup -q -n libpmemobj-cpp-%{upstreamversion}

%build
mkdir build
cd build
# CXX_STANDARD=17 matters only for tests, it can be safely disabled in distros without c++17-compliant compiler
%cmake .. -DCMAKE_INSTALL_DOCDIR=%{_docdir}/libpmemobj++ -DTESTS_USE_FORCED_PMEM=ON -DCXX_STANDARD=17
%make_build

%install
cd build
%make_install

%check
cd build
# https://github.com/pmem/libpmemobj-cpp/issues/469
ctest -V %{?_smp_mflags} -E concurrent_hash_map_rehash_0_helgrind -E concurrent_hash_map_insert_lookup_0_helgrind

%changelog
* Fri Sep 01 2023 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.9-4
- Disabling test dependencies due to build failures.

* Thu Aug 31 2023 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.9-3
- Disabling missing test dependency.
- License verified.

* Wed Jun 23 2021 Thomas Crain <thcrain@microsoft.com> - 1.9-2
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Conditionally require check dependencies at build time

* Wed Feb 12 2020 Marcin Ślusarz <marcin.slusarz@intel.com> - 1.9-1
- Update to version 1.9.

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Jan 27 2020 Marcin Ślusarz <marcin.slusarz@intel.com> - 1.8.1-1
- Update to version 1.8.1.

* Fri Oct 04 2019 Marcin Ślusarz <marcin.slusarz@intel.com> - 1.8-2
- Work around https://github.com/pmem/libpmemobj-cpp/issues/469.

* Fri Oct 04 2019 Marcin Ślusarz <marcin.slusarz@intel.com> - 1.8-1
- Update to version 1.8.

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Jun 26 2019 Marcin Ślusarz <marcin.slusarz@intel.com> - 1.7-1
- Update to version 1.7.

* Thu Mar 28 2019 Marcin Ślusarz <marcin.slusarz@intel.com> - 1.6-2
- Bump required PMDK version to 1.6.

* Mon Mar 18 2019 Marcin Ślusarz <marcin.slusarz@intel.com> - 1.6-1
- Update to version 1.6

* Fri Mar 08 2019 Marcin Ślusarz <marcin.slusarz@intel.com> - 1.5.1-1
- Update to version 1.5.1

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Dec 14 2018 Marcin Ślusarz <marcin.slusarz@intel.com> - 1.5-1
- Initial RPM release
