# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:		msgpack
Version:	3.1.0
Release: 21%{?dist}
Summary:	Binary-based efficient object serialization library

# Automatically converted from old format: Boost - review is highly recommended.
License:	BSL-1.0
URL:		http://msgpack.org
Source0:	https://github.com/msgpack/msgpack-c/releases/download/cpp-%{version}/%{name}-%{version}.tar.gz
Patch0:	0001-Fixed-724.patch
Patch1:     msgpack-cmake4.patch

BuildRequires: make
BuildRequires: cmake
BuildRequires: gcc-c++
BuildRequires: doxygen
# for %%check
BuildRequires: gtest-devel
BuildRequires: zlib-devel

%description
MessagePack is a binary-based efficient object serialization
library. It enables to exchange structured objects between many
languages like JSON. But unlike JSON, it is very fast and small.


%package devel
Summary:	Libraries and header files for %{name}
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description devel
Libraries and header files for %{name}


%prep
%autosetup -p1

# gtest 1.13.0 requires at least C++14
sed -i "s|-std=c++98|-std=gnu++14|g" CMakeLists.txt

%build
%cmake -DCMAKE_INSTALL_LIBDIR=%{_libdir} -Dlibdir=%{_libdir} -DBUILD_SHARED_LIBS=ON
%cmake_build

%check
# https://github.com/msgpack/msgpack-c/issues/697
export GTEST_FILTER=-object_with_zone.ext_empty
%ctest
cat %_vpath_builddir/Testing/Temporary/LastTest.log


%install
%cmake_install

%files
%license LICENSE_1_0.txt COPYING
%doc AUTHORS ChangeLog NOTICE README README.md
%{_libdir}/*.so.*

%files devel
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/msgpack.pc
%{_libdir}/cmake/msgpack


%changelog
* Sat Aug 02 2025 Antonio Trande <sagitter@fedoraproject.org> - 3.1.0-20
- Fix rhbz#2381079

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.0-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.0-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Jul 24 2024 Miroslav Suchý <msuchy@redhat.com> - 3.1.0-17
- convert license to SPDX

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.0-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.0-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.0-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jul 23 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 3.1.0-13
- Upgrade from C++11 to C++14 for gtest 1.13.0

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.0-6
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Aug 22 2018 Daiki Ueno <dueno@redhat.com> - 3.1.0-1
- new upstream release
- cmake configuration files no longer rely on nonexistent static libraries

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun  7 2018 Daiki Ueno <dueno@redhat.com> - 3.0.1-1
- new upstream release

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Feb 03 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.4.2-4
- Switch to %%ldconfig_scriptlets

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Feb 21 2017 Daiki Ueno <dueno@redhat.com> - 1.4.2-1
- new upstream release
- avoid FTBFS with GCC7

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Apr  7 2016 Daiki Ueno <dueno@redhat.com> - 1.4.1-1
- new upstream release

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Dec 10 2015 Neal Gompa <ngompa13{%}gmail{*}com> - 1.3.0-1
- Upgrade to 1.3.0 upstream release
- Drop unneeded patch

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 0.5.9-3
- Rebuilt for GCC 5 C++11 ABI change

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Jul 11 2014 Daiki Ueno <dueno@redhat.com> - 0.5.9-1
- new upstream release
- apply patch to fix int->float test failure

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Jan  9 2014 Daiki Ueno <dueno@redhat.com> - 0.5.8-1
- new upstream release
- remove patches that are no longer needed

* Tue Aug 27 2013 Dan Horák <dan[at]danny.cz> - 0.5.7-5
- apply upstream fix for big endians

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Feb 15 2012 Daiki Ueno <dueno@redhat.com> - 0.5.7-1
- initial packaging for Fedora

