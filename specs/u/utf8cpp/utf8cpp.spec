# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%undefine __cmake_in_source_build
# This package only contains header files.
%global debug_package %{nil}
%global ftest_commit c4ad4af0946b73ce1a40cbc72205d15d196c7e06
%global ftest_shortcommit %(c=%{ftest_commit}; echo ${c:0:7})

Name:       utf8cpp
Version:    4.0.8
Release:    1%{?dist}
Summary:    A simple, portable and lightweight library for handling UTF-8 encoded strings
License:    BSL-1.0
URL:        https://github.com/nemtrif/utfcpp
Source0:    https://github.com/nemtrif/utfcpp/archive/v%{version}/utfcpp-%{version}.tar.gz
# put cmake import file in correct directory
Patch0:     %{name}-cmake.patch
BuildRequires: cmake
BuildRequires: gcc-c++

%description
%{summary}.

Features include:
 - iterating through UTF-8 encoded strings
 - converting between UTF-8 and UTF-16/UTF-32
 - detecting invalid UTF-8 sequences

This project currently only contains header files, which can be found in the
%{name}-devel package.

%package    devel
Summary:    Header files for %{name}
BuildArch:  noarch
Provides:   %{name}-static = %{version}-%{release}
Requires:   cmake-filesystem

%description devel
%{summary}.

Features include:
 - iterating through UTF-8 encoded strings
 - converting between UTF-8 and UTF-16/UTF-32
 - detecting invalid UTF-8 sequences

This project currently only contains header files, which can be found in the
%{name}-devel package.

%prep
%autosetup -n utfcpp-%{version} -p1

%build
%cmake \
   %{nil}
%cmake_build
pushd tests
%cmake
%cmake_build
popd

%install
%cmake_install
pushd %{buildroot}%{_includedir}
ln -s utf8cpp/utf8.h ./
mkdir utf8
for f in {{un,}checked,core,cpp{11,17,20}}.h ; do
    ln -s ../utf8cpp/utf8/${f} utf8/
done
popd

%check
pushd tests
%ctest
popd

%files devel
%doc README.md
%license LICENSE
%{_includedir}/utf8.h
%dir %{_includedir}/utf8
%{_includedir}/utf8/checked.h
%{_includedir}/utf8/core.h
%{_includedir}/utf8/cpp11.h
%{_includedir}/utf8/cpp17.h
%{_includedir}/utf8/cpp20.h
%{_includedir}/utf8/unchecked.h
%{_includedir}/utf8cpp
%{_datadir}/cmake/utf8cpp

%changelog
* Sat Sep 20 2025 Dominik Mierzejewski <dominik@greysector.net> - 4.0.8-1
- update to 4.0.8 (resolves rhbz#2395010)

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sun Nov 17 2024 Dominik Mierzejewski <dominik@greysector.net> - 4.0.6-1
- update to 4.0.6 (resolves rhbz#2323791)

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jan 03 2024 Dominik Mierzejewski <dominik@greysector.net> - 4.0.5-1
- update to 4.0.5 (resolves rhbz#2245744)
- include license text

* Sun Oct 08 2023 Dominik Mierzejewski <dominik@greysector.net> - 3.2.5-1
- update to 3.2.5 (resolves rhbz#2240785)

* Thu Aug 31 2023 Dominik Mierzejewski <dominik@greysector.net> - 3.2.4-1
- update to 3.2.4 (resolves rhbz#2231660)
- switch to SPDX expression in License tag
- use modern autosetup and plain cmake dependency and macros

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Jan 03 2023 Dominik 'Rathann' Mierzejewski <dominik@greysector.net> - 3.2.3-1
- update to 3.2.3 (#2157206)

* Wed Dec 07 2022 Dominik 'Rathann' Mierzejewski <dominik@greysector.net> - 3.2.2-1
- update to 3.2.2 (#2140879)

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Jun 07 2021 Dominik 'Rathann' Mierzejewski <rpm@greysector.net> - 3.2.1-1
- update to 3.2.1 (#1968224)

* Wed May 19 2021 Dominik 'Rathann' Mierzejewski <rpm@greysector.net> - 3.2-2
- add missed compatibility link for cpp17.h

* Tue May 04 2021 Dominik 'Rathann' Mierzejewski <rpm@greysector.net> - 3.2-1
- update to 3.2 (#1956027)

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Oct 05 2020 Dominik 'Rathann' Mierzejewski <rpm@greysector.net> - 3.1.2-1
- update to 3.1.2 (#1883049)

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Oct 22 2019 Dominik 'Rathann' Mierzejewski <rpm@greysector.net> - 3.1-1
- update to 3.1
- include cmake import file
- symlink headers in the previous location for compatibility

* Mon Oct 21 2019 Dominik 'Rathann' Mierzejewski <rpm@greysector.net> - 2.3.6-1
- update to 2.3.6
- new upstream location
- use cmake and run tests
- switch main package to archful per
  https://docs.fedoraproject.org/en-US/packaging-guidelines/#_do_not_use_noarch

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.4-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.4-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.4-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.4-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.4-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.4-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Apr 30 2014 Jamie Nguyen <jamielinux@fedoraproject.org> - 2.3.4-4
- fix docs macro

* Wed Apr 30 2014 Jamie Nguyen <jamielinux@fedoraproject.org> - 2.3.4-3
- drop base package

* Wed Apr 30 2014 Jamie Nguyen <jamielinux@fedoraproject.org> - 2.3.4-2
- add Provides: utf8cpp-static
- fix Source0 URL
- add missing BuildArch: noarch

* Sat Mar 15 2014 Jamie Nguyen <jamielinux@fedoraproject.org> - 2.3.4-1
- initial package
