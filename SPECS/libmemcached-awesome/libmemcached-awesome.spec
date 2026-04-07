# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Fedora spec file for libmemcached-awesome from
#
# remirepo spec file for libmemcached-awesome
#
# Copyright (c) 2009-2023 Remi Collet
# License: CC-BY-SA-4.0
# https://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#

%bcond_without               tests

%global libname              libmemcached

%global gh_commit            92d18858b417309f6bdee6bce464a4f3d6a375fd
%global gh_short             %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner             awesomized
%global gh_project           libmemcached

%global upstream_version     1.1.4
#global upstream_prever      beta3

Name:      %{libname}-awesome
Summary:   Client library and command line tools for memcached server
Version:   %{upstream_version}%{?upstream_prever:~%{upstream_prever}}
Release:   7%{?dist}
# SPDX:
License:   BSD-3-Clause
URL:       https://github.com/%{gh_owner}/%{gh_project}
Source0:   https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}-%{gh_short}.tar.gz

BuildRequires: cmake >= 3.9
BuildRequires: gcc
BuildRequires: gcc-c++
BuildRequires: python3-sphinx
BuildRequires: cyrus-sasl-devel
BuildRequires: flex
BuildRequires: bison
BuildRequires: memcached
BuildRequires: systemtap-sdt-devel
BuildRequires: libevent-devel > 2
BuildRequires: openssl-devel

Provides:      bundled(bobjenkins-hash)
# package rename
Obsoletes:     %{libname}-libs         < 1.1
Provides:      %{libname}-libs         = %{version}-%{release}
Provides:      %{libname}-libs%{?_isa} = %{version}-%{release}


%description
%{name} is a C/C++ client library and tools for the memcached
server (https://memcached.org/). It has been designed to be light
on memory usage, and provide full access to server side methods.

This is a resurrection of the original work from Brian Aker at libmemcached.org.


%package devel
Summary:    Header files and development libraries for %{name}

Requires:   cyrus-sasl-devel%{?_isa}
Requires:   %{name}%{?_isa} = %{version}-%{release}
# package rename
Obsoletes:  %{libname}-devel         < 1.1
Provides:   %{libname}-devel         = %{version}-%{release}
Provides:   %{libname}-devel%{?_isa} = %{version}-%{release}

%description devel
This package contains the header files and development libraries
for %{name}. If you like to develop programs using %{name}, 
you will need to install %{name}-devel.

Documentation: https://awesomized.github.io/libmemcached


%package tools
Summary:    %{name} tools

Requires:   %{name}%{?_isa} = %{version}-%{release}
# package rename
Obsoletes:  %{libname}         < 1.1
Provides:   %{libname}         = %{version}-%{release}
Provides:   %{libname}%{?_isa} = %{version}-%{release}

%description tools
This package contains the %{libname}-awesome command line tools:

memaslap    Load testing and benchmarking a server
memcapable  Checking a Memcached server capibilities and compatibility
memcat      Copy the value of a key to standard output
memcp       Copy data to a server
memdump     Dumping your server
memerror    Translate an error code to a string
memexist    Check for the existance of a key
memflush    Flush the contents of your servers
memparse    Parse an option string
memping     Test to see if a server is available.
memrm       Remove a key(s) from the server
memslap     Generate testing loads on a memcached cluster
memstat     Dump the stats of your servers to standard output
memtouch    Touches a key


%prep
%setup -q -n %{gh_project}-%{gh_commit}

# drop test hanging in mock
# and requiring some memcached build options
rm test/tests/memcached/sasl.cpp
rm test/tests/memcached/regression/lp_001-630-615.cpp
# temporarily ignore with erratic failure
rm test/tests/memcached/udp.cpp
rm test/tests/memcached/regression/lp_000-583-031.cpp
rm test/tests/memcached/regression/gh-php-memcached_0531.cpp


%build
%cmake \
  -DBUILD_TESTING:BOOL=ON \
  -DBUILD_DOCS_MAN:BOOL=ON \
  -DBUILD_DOCS_MANGZ:BOOL=OFF \
  -DENABLE_SASL:BOOL=ON \
  -DENABLE_DTRACE:BOOL=ON \
  -DENABLE_OPENSSL_CRYPTO:BOOL=ON \
  -DENABLE_HASH_HSIEH:BOOL=ON \
  -DENABLE_HASH_FNV64:BOOL=ON \
  -DENABLE_HASH_MURMUR:BOOL=ON \
  -DENABLE_MEMASLAP:BOOL=ON

%cmake_build


%install
%cmake_install

mv %{buildroot}%{_datadir}/%{name}/example.cnf support

rm -r %{buildroot}%{_datadir}/doc/%{name}/


%check
%if %{with tests}
: Run test suite
%ctest
%else
: Skip test suite
%endif


%files tools
%{_bindir}/mem*
%{_mandir}/man1/mem*

%files
%license LICENSE
%{_libdir}/libhashkit.so.2*
%{_libdir}/libmemcached.so.11*
%{_libdir}/libmemcachedprotocol.so.0*
%{_libdir}/libmemcachedutil.so.2*
%exclude %{_libdir}/libp9y.a

%files devel
%doc example
%doc *.md
%doc AUTHORS
%doc support/example.cnf
%{_includedir}/libmemcached
%{_includedir}/libmemcached-1.0
%{_includedir}/libhashkit
%{_includedir}/libhashkit-1.0
%{_includedir}/libmemcachedprotocol-0.0
%{_includedir}/libmemcachedutil-1.0
%{_libdir}/libhashkit.so
%{_libdir}/libmemcached.so
%{_libdir}/libmemcachedprotocol.so
%{_libdir}/libmemcachedutil.so
%{_libdir}/pkgconfig/libmemcached.pc
%{_datadir}/aclocal/ax_libmemcached.m4
%{_mandir}/man3/libmemcached*
%{_mandir}/man3/libhashkit*
%{_mandir}/man3/memcached*
%{_mandir}/man3/hashkit*
%dir     %{_libdir}/cmake/%{name}
         %{_libdir}/cmake/%{name}/lib*
%exclude %{_libdir}/cmake/%{name}/p9y*


%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jan 20 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon Mar  6 2023 Remi Collet <remi@remirepo.net> - 1.1.4-1
- update to 1.1.4

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Nov  9 2022 Remi Collet <remi@remirepo.net> - 1.1.3-1
- update to 1.1.3

* Wed Aug 10 2022 Remi Collet <remi@remirepo.net> - 1.1.2-1
- update to 1.1.2

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Feb  2 2022 Remi Collet <remi@remirepo.net> - 1.1.1-3
- rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Sep 20 2021 Remi Collet <remi@remirepo.net> - 1.1.1-1
- update to 1.1.1

* Tue Sep 14 2021 Sahana Prasad <sahana@redhat.com> - 1.1.0-9
- Rebuilt with OpenSSL 3.0.0

* Thu Sep  9 2021 Remi Collet <remi@remirepo.net> - 1.1.0-8
- devel requires cyrus-sasl-devel, fix #2002541

* Tue Jul 27 2021 Remi Collet <remi@remirepo.net> - 1.1.0-6
- add LIBMEMCACHED_AWESOME macro from
  https://github.com/awesomized/libmemcached/pull/115

* Mon Jul 26 2021 Remi Collet <remi@remirepo.net> - 1.1.0-5
- fix missing HAVE_SSIZE_T macro using patch from
  https://github.com/awesomized/libmemcached/pull/117

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jul 13 2021 Remi Collet <remi@remirepo.net> - 1.1.0-3
- use upstream patch for libcrypto

* Fri Jun 25 2021 Remi Collet <remi@remirepo.net> - 1.1.0-2
- remove internal AES implementation and use libcrypto
  https://github.com/awesomized/libmemcached/pull/114
- fix build ussing upstream patch to update catch version

* Thu Jun 24 2021 Remi Collet <remi@remirepo.net> - 1.1.0-1
- Initial RPM from libmemcached-awesome
  from old libmemcached spec file
