# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%undefine __cmake_in_source_build
# https://github.com/georgmartius/vid.stab/commit/05829db776069b7478dd2d90b6e0081668a41abc
%global commit 05829db776069b7478dd2d90b6e0081668a41abc
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global commitdate 20230603

Name:           vid.stab
Version:        1.1.1
Release:        7%{?dist}
Summary:        Video stabilize library for fmpeg, mlt or transcode
# Automatically converted from old format: GPLv2+ - review is highly recommended.
License:        GPL-2.0-or-later
URL:            http://public.hronopik.de/vid.stab
Source0:        https://github.com/georgmartius/vid.stab/archive/%{commit}/%{name}-%{shortcommit}.tar.gz

BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  cmake
BuildRequires:  orc-devel
Requires:       glibc
#To be removed more or less in Fedora 32
Provides:	%{name}-libs = %{version}-%{release}
Obsoletes:	%{name}-libs < %{version}-%{release}

%description
Vidstab is a video stabilization library which can be plugged-in with Ffmpeg
and Transcode.

%package devel
Summary:        Development files for vid.stab
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
This package contains the development files (library and header files).

%prep
%setup -q -n %{name}-%{commit}
# remove SSE2 flags
sed -i 's|-DUSE_SSE2 -msse2||' tests/CMakeLists.txt
# fxi warning _FORTIFY_SOURCE requires compiling with optimization (-O)
sed -i 's|-Wall -O0|-Wall -O|' tests/CMakeLists.txt
# use macros EXIT_SUCCESS and EXIT_FAILURE instead for portability reasons.
sed -i 's|return units_failed==0;|return units_failed>0;|' tests/testframework.c

%build
# TODO: Please submit an issue to upstream (rhbz#2381628)
export CMAKE_POLICY_VERSION_MINIMUM=3.5
%cmake
%cmake_build

# build the tests program
pushd tests
%cmake
%cmake_build
popd

%install
%cmake_install

%check
LD_LIBRARY_PATH=%{buildroot}%{_libdir} tests/tests || :

%ldconfig_scriptlets -n %{name}

%files
%doc README.md
%license LICENSE
%{_libdir}/libvidstab.so.*

%files devel
%{_includedir}/vid.stab/
%{_libdir}/libvidstab.so
%{_libdir}/pkgconfig/vidstab.pc

%changelog
* Tue Nov 11 2025 Cristian Le <git@lecris.dev> - 1.1.1-7
- Allow to build with CMake 4.0 (rhbz#2381628)

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 26 2024 Miroslav Suchý <msuchy@redhat.com> - 1.1.1-4
- convert license to SPDX

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Sep 23 2023 Sérgio Basto <sergio@serjux.com> - 1.1.1-1
- Update vid.stab to 1.1.1

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-22.20201110gitf9166e9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-21.20201110gitf9166e9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-20.20201110gitf9166e9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-19.20201110gitf9166e9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Dec 14 2021 Martin Gansser <martinkg@fedoraproject.org> - 1.1.0-18.20201110gitf9166e9
- Update to 1.1.0-18.20201110gitf9166e9

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-17.20190213gitaeabc8d
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-16.20190213gitaeabc8d
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-15.20190213gitaeabc8d
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild
- Fix cmake build

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-14.20190213gitaeabc8d
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-13.20190213gitaeabc8d
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-12.20190213gitaeabc8d
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Feb 03 2019 Martin Gansser <martinkg@fedoraproject.org> - 1.1.0-11.20190213gitaeabc8d
- Update to 1.1.0-11.20190213gitaeabc8d

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-10.20180529git38ecbaf
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Oct 01 2018 Sérgio Basto <sergio@serjux.com> - 1.1.0-9.20180529git38ecbaf
- Obsoletes: vid.stab-libs

* Sat Sep 29 2018 Sérgio Basto <sergio@serjux.com> - 1.1.0-1.20180529git38ecbaf
- Fix version number and update the source code

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1-5.20170830gitafc8ea9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1-4.20170830gitafc8ea9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Oct 04 2017 Martin Gansser <martinkg@fedoraproject.org> - 1.1-3.20170830gitafc8ea9
- change license tag to GPLv2
- fix warning _FORTIFY_SOURCE requires compiling with optimization (-O)

* Sun Oct 01 2017 Martin Gansser <martinkg@fedoraproject.org> - 1.1-2.20170830gitafc8ea9
- use macros EXIT_SUCCESS and EXIT_FAILURE instead for portability reasons

* Sat Sep 30 2017 Martin Gansser <martinkg@fedoraproject.org> - 1.1-1.20170830gitafc8ea9
- Initial build rpm
