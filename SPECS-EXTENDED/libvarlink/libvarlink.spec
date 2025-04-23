Vendor:         Microsoft Corporation
Distribution:   Azure Linux
%global _hardened_build 1

Name:           libvarlink
Version:        23
Release:        10%{?dist}
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
* Tue Nov 19 2024 Sreenivasulu Malavathula <v-smalavathu@microsoft.com> - 23-10
- Initial Azure Linux import from Fedora 41 (license: MIT)
- License verified

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 23-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri May 17 2024 Davide Cavalca <dcavalca@fedoraproject.org> - 23-8
- Convert license tag to SPDX
- Update spec to the latest packaging guidelines
- Disable broken test on ppc64le; Fixes: RHBZ#2261345

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 23-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 23-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 23-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 23-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 23-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 23-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 22-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Mar 02 2021 Packit Service <user-cont-team+packit-service@redhat.com> - 22-1
- version 22
- libvarlink now includes and passes most of the JSONTestSuite tests.

* Tue Feb 23 2021 Harald Hoyer <harald@redhat.com> - 21-2
- fixed changelog date inserted by packit with de_DE locale

* Tue Feb 23 2021 Harald Hoyer <harald@redhat.com> - 21-1
- ci: add .packit.yaml (Harald Hoyer)
- version 21 (Harald Hoyer)
- fix: use strtod_l (Harald Hoyer)
- fix: return VARLINK_ERROR_PANIC on float Inf or NaN (Harald Hoyer)
- tests: add test with de_DE.UTF-8 locale (Harald Hoyer)
- ci: install de_DE.UTF-8 locale (Harald Hoyer)
- fix: correct the float number parsing for some locales (Harald Hoyer)
- tests: print error log on `make check` (Harald Hoyer)
- docs: update README.md (Harald Hoyer)

* Thu Feb 18 2021 Harald Hoyer <harald@redhat.com> - 20-1
- libvarlink 20

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 19-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Dec 10 2020 Stephen Gallagher <sgallagh@redhat.com> - 19-4
- Fix builds when git is present in the buildroot
- Fixes https://github.com/varlink/libvarlink/issues/22

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 19-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 30 2020 Jeff Law <law@redhat.com> - 19-2
Disable LTO

* Fri Mar 06 2020 Harald Hoyer <harald@redhat.com> - 19-1
- libvarlink 19

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

