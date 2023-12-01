# Fedora spec file for libmemcached-awesome from
#
# remirepo spec file for libmemcached-awesome
#
# Copyright (c) 2009-2021 Remi Collet
# License: CC-BY-SA
# https://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global libname libmemcached
Summary:        Client library and command line tools for memcached server
Name:           %{libname}-awesome
Version:        1.1.1
Release:        4%{?dist}
License:        BSD
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/awesomized/libmemcached
Source0:        https://github.com/awesomized/libmemcached/archive/refs/tags/%{version}.tar.gz#/%{libname}-%{version}.tar.gz
BuildRequires:  bison
BuildRequires:  cmake >= 3.9
BuildRequires:  cyrus-sasl-devel
BuildRequires:  flex
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  libevent-devel > 2
BuildRequires:  memcached
BuildRequires:  openssl-devel
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-sphinx
BuildRequires:  systemtap-sdt-devel
Provides:       bundled(bobjenkins-hash)
# package rename
Provides:       %{libname}-libs = %{version}-%{release}
Provides:       %{libname}-libs%{?_isa} = %{version}-%{release}

%description
%{name} is a C/C++ client library and tools for the memcached
server (https://memcached.org/). It has been designed to be light
on memory usage, and provide full access to server side methods.

This is a resurrection of the original work from Brian Aker at libmemcached.org.

%package        devel
Summary:        Header files and development libraries for %{name}
Requires:       %{name} = %{version}-%{release}
Requires:       cyrus-sasl-devel
# package rename
Provides:       %{libname}-devel = %{version}-%{release}
Provides:       %{libname}-devel%{?_isa} = %{version}-%{release}

%description devel
This package contains the header files and development libraries
for %{name}. If you like to develop programs using %{name},
you will need to install %{name}-devel.

Documentation: https://awesomized.github.io/libmemcached

%package        tools
Summary:        %{name} tools
Requires:       %{name} = %{version}-%{release}
# package rename
Provides:       %{libname} = %{version}-%{release}
Provides:       %{libname}%{?_isa} = %{version}-%{release}

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
%autosetup -n %{libname}-%{version}

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
rm -r %{buildroot}%{_docdir}/%{name}/

%check
%ctest

%files
%license LICENSE
%{_libdir}/libhashkit.so.2*
%{_libdir}/libmemcached.so.11*
%{_libdir}/libmemcachedprotocol.so.0*
%{_libdir}/libmemcachedutil.so.2*

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
%{_libdir}/cmake/%{name}
%{_datadir}/aclocal/ax_libmemcached.m4
%{_mandir}/man3/libmemcached*
%{_mandir}/man3/libhashkit*
%{_mandir}/man3/memcached*
%{_mandir}/man3/hashkit*

%files tools
%{_bindir}/mem*
%{_mandir}/man1/mem*

%changelog
* Sun Feb 13 2022 Jon Slobodzian <joslobo@microsoft.com> - 1.1.1-4
- Adding python-devel to fix python-sphinx build issue

* Mon Jan 24 2022 Olivia Crain <oliviacrain@microsoft.com> - 1.1.1-3
- Initial CBL-Mariner import from Fedora 36 (license: CC-BY-SA)
- Lint spec
- License verified

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
