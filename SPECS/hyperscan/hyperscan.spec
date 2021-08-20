%global __cmake_in_source_build 1
Name:           hyperscan
Version:        5.4.0
Release:        2%{?dist}
Summary:        High-performance regular expression matching library
License:        BSD
Group:          Development/Libraries
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://www.hyperscan.io/
Source0:        https://github.com/intel/%{name}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Patch0:         hyperscan-fix-missed-symbols.patch

BuildRequires:  gcc
BuildRequires:  libstdc++-devel
BuildRequires:  libstdc++
BuildRequires:  boost-devel
BuildRequires:  cmake
BuildRequires:  pcre-devel
BuildRequires:  python3
BuildRequires:  ragel
BuildRequires:  sqlite-devel >= 3.0
BuildRequires:  libpcap-devel
Requires:       pcre

#package requires SSE support and fails to build on non x86_64 archs
ExclusiveArch: x86_64

%description
Hyperscan is a high-performance multiple regex matching library. It
follows the regular expression syntax of the commonly-used libpcre
library, but is a standalone library with its own C API.

Hyperscan uses hybrid automata techniques to allow simultaneous
matching of large numbers (up to tens of thousands) of regular
expressions and for the matching of regular expressions across streams
of data.

Hyperscan is typically used in a DPI library stack.

%package devel
Summary: Libraries and header files for the hyperscan library
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
Hyperscan is a high-performance multiple regex matching library. It
follows the regular expression syntax of the commonly-used libpcre
library, but is a standalone library with its own C API.

Hyperscan uses hybrid automata techniques to allow simultaneous
matching of large numbers (up to tens of thousands) of regular
expressions and for the matching of regular expressions across streams
of data.

Hyperscan is typically used in a DPI library stack.

This package provides the libraries, include files and other resources
needed for developing Hyperscan applications.

%prep
%autosetup -p1

%build
# LTO seems to be losing the target prefix on ifunc targets leading to
# multiply defined symbols.  This seems like a GCC bug
# Disable LTO
%define _lto_cflags %{nil}
%cmake -DBUILD_SHARED_LIBS:BOOL=ON -DBUILD_STATIC_AND_SHARED:BOOL=OFF .
%make_build

%install
%make_install

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc %{_defaultdocdir}/%{name}/examples/README.md
%doc %{_defaultdocdir}/%{name}/examples/*.cc
%doc %{_defaultdocdir}/%{name}/examples/*.c
%license COPYING
%license LICENSE
%{_libdir}/*.so.*

%files devel
%{_libdir}/*.so
%{_libdir}/pkgconfig/libhs.pc
%{_includedir}/hs/

%changelog
* Fri Jul 02 2021 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 5.4.0-2
- Initial CBL-Mariner import from Fedora 33 (license: MIT)
- License verified

* Tue Jan 26 2021 Jason Taylor <jtfas90@gmail.com> - 5.4.0-1
- Updated to latest upstream release

* Mon Aug 10 2020 Jason Taylor <jtfas90@gmail.com> - 5.3.0-5
- Updated to new cmake macros

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.3.0-4
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 08 2020 Jeff Law <law@redhat.com> - 5.3.0-2
- Disable LTO

* Thu May 28 2020 Jason Taylor <jtfas90@gmail.com> - 5.3.0-1
- Latest upstream release

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Oct 30 2019 Jason Taylor <jtfas90@gmail.com> - 5.2.1-1
- Latest upstream release

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Apr 10 2019 Jason Taylor <jtfas90@gmail.com> - 5.1.1-1
- Latest upstream version (#1698365)
- Removed patch added for FTBFS (#1675120)

* Tue Feb 12 2019 Björn Esser <besser82@fedoraproject.org> - 5.1.0-1
- Latest upstream version (#1671192)
- Add patch to fix build (#1675120)

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jul 09 2018 Jason Taylor <jtfas90@gmail.com> - 5.0.0-1
- Latest upstream version

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.7.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jan 25 2018 Jason Taylor <jtfas90@gmail.com> - 4.7.0-1
- upstream bugfix release

* Fri Sep 22 2017 Jason Taylor <jtfas90@gmail.com> - 4.6.0-1
- latest upstream release

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.5.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Jason Taylor <jtfas90@gmail.com> - 4.5.2-1
- upstream bugfix release

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Jun 16 2017 Jason Taylor <jtfas90@gmail.com> - 4.5.1-1
- upstream bugfix release

* Fri Jun 09 2017 Jason Taylor <jtfas90@gmail.com> - 4.5.0-1
- Update to latest upstream
- Removed CMakeLists.txt patch, moved into upstream

* Fri May 12 2017 Jason Taylor <jtfas90@gmail.com> - 4.4.1-1
- Update to latest upstream
- Add CMakeLists.txt path patch
- Spec file updates to meet packaging standards

* Fri Sep 2 2016 Jason Taylor <jtfas90@gmail.com> - 4.3.1-1
- Updated to latest upstream release.

* Fri Jul 1 2016 Jason Ish <ish@unx.ca> - 4.2.0-1
- Initial package of Hyperscan.
