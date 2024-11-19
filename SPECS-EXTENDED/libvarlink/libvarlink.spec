Vendor:         Microsoft Corporation
Distribution:   Azure Linux
# SPDX-License-Identifier: Apache-2.0 AND BSD-3-Clause
%global _hardened_build 1

Name:           libvarlink
Version:        23
Release:        1%{?dist}
Summary:        Varlink C Library
License:        Apache-2.0 AND BSD-3-Clause
URL:            https://github.com/varlink/%{name}
Source:         %{url}/archive/%{version}/%{name}-%{version}.tar.gz
BuildRequires:  meson
BuildRequires:  gcc

%description
Varlink C Library

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package        util
Summary:        Varlink command line tools

%description    util
The %{name}-util package contains varlink command line tools.

%prep
%autosetup

%build
%meson
%meson_build

%check
export LC_CTYPE=C.utf8
# https://github.com/varlink/libvarlink/issues/63
%ifarch ppc64le
test_list=$(%meson_test --list) 2> /dev/null
test_list=${test_list//test-symbols}
%meson_test $test_list
%else
%meson_test
%endif

%install
%meson_install

%files
%license LICENSE
%{_libdir}/libvarlink.so.*

%files util
%{_bindir}/varlink
%{_datadir}/bash-completion/completions/varlink
%{_datadir}/vim/vimfiles/after/*

%files devel
%{_includedir}/varlink.h
%{_libdir}/libvarlink.so
%{_libdir}/pkgconfig/libvarlink.pc

%changelog
* Tue Nov 19 2024 Sreenivasulu Malavathula <v-smalavathu@microsoft.com> - 23-1
- Udpdate Azure-Linux import from Fedora 41 (license: Apache-2.0 AND BSD-3-Clause).
- License verified.

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 18-4
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 18-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 18-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed May 22 2019 Harald Hoyer <harald@redhat.com> - 18-1
- libvarlink 18

* Fri Feb 15 2019 Harald Hoyer <harald@redhat.com> - 17-1
- libvarlink 17

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Oct  9 2018 <info@varlink.org> 15-1
- libvarlink 15

* Mon Oct  8 2018 <info@varlink.org> 14-1
- libvarlink 14

* Mon Jul 16 2018 <kay@redhat.com> - 12-1
- libvarlink 12

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sun Jun 17 2018 <kay@redhat.com>
- libvarlink 11

* Sat May 12 2018  <kay@redhat.com>
- libvarlink 10

* Fri Apr 13 2018 <kay@redhat.com>
- libvarlink 9

* Thu Apr 12 2018 <kay@redhat.com>
- libvarlink 8

* Mon Mar 26 2018 <kay@redhat.com>
- libvarlink 7

* Mon Mar 26 2018 <kay@redhat.com>
- libvarlink 6

* Fri Mar 23 2018 <kay@redhat.com>
- libvarlink 5

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Feb 02 2018 Harald Hoyer <harald@redhat.com> - 1-2
- bump release

* Fri Feb  2 2018 <kay@redhat.com>
- libvarlink 1
