%bcond_without static_libs # don't build static libraries
Summary:        Library providing binary-decimal and decimal-binary routines for IEEE doubles
Name:           double-conversion
Version:        3.1.5
Release:        9%{?dist}
License:        BSD
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/google/double-conversion
Source0:        https://github.com/google/double-conversion/archive/v%{version}/%{name}-%{version}.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
%undefine __cmake_in_source_build

%description
Provides binary-decimal and decimal-binary routines for IEEE doubles.
The library consists of efficient conversion routines that have been
extracted from the V8 JavaScript engine. The code has been re-factored
and improved so that it can be used more easily in other projects.

%package devel
Summary:        Library providing binary-decimal and decimal-binary routines for IEEE doubles
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Contains header files for developing applications that use the %{name}
library.

There is extensive documentation in src/double-conversion.h. Other
examples can be found in test/cctest/test-conversions.cc.

%package static
Summary:        Library providing binary-decimal and decimal-binary routines for IEEE doubles
Requires:       %{name}-devel%{?_isa} = %{version}-%{release}

%description static
Static %{name} library.

%prep
%setup -q

%build
%global _vpath_builddir build-shared
%cmake -DBUILD_TESTING=ON
%cmake_build

%if %{with static_libs}
%global _vpath_builddir build-static
CXXFLAGS="%{optflags} -fPIC" %cmake -DBUILD_SHARED_LIBS=NO
%cmake_build
%endif

%install
%if %{with static_libs}
%global _vpath_builddir build-static
%cmake_install
%endif

%global _vpath_builddir build-shared
%cmake_install

%check
%ctest

%ldconfig_scriptlets

%files
%license LICENSE
%doc README.md AUTHORS Changelog
%{_libdir}/libdouble-conversion.so.3*

%files devel
%{_libdir}/libdouble-conversion.so
%{_libdir}/cmake/%{name}
%{_includedir}/%{name}

%if %{with static_libs}
%files static
%{_libdir}/libdouble-conversion.a
%endif

%changelog
* Wed Nov 22 2023 Sindhu Karri <lakarri@microsoft.com> - 3.1.5-9
- Initial CBL-Mariner import from Fedora 38 (license: MIT)
- Source license verified: BSD

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.5-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sun Sep 22 2019 Orion Poplawski <orion@nwra.com> - 3.1.5-1
- Update to 3.1.5

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Sep 4 2017 Milan Bouchet-Valat <nalimilan@club.fr> - 3.0.0-1
- New upstream release.

* Sun Aug 06 2017 Björn Esser <besser82@fedoraproject.org> - 2.0.1-11
- Rebuilt for AutoReq cmake-filesystem

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Mar 13 2015 Orion Poplawski <orion@cora.nwra.com> - 2.0.1-5
- Use github source

* Wed Mar 11 2015 Orion Poplawski <orion@cora.nwra.com> - 2.0.1-4
- Build with cmake

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Feb 8 2014 Milan Bouchet-Valat <nalimilan@club.fr> - 2.0.1-1
- New upstream version.
- Drop no longer needed custom SConstruct file and use new upstream SONAME.

* Tue Dec 17 2013 Milan Bouchet-Valat <nalimilan@club.fr> - 2.0.0-4
- Drop libstdc++-devel from BuildRequires.
- Move %%check after %%install.

* Sat Dec 14 2013 Milan Bouchet-Valat <nalimilan@club.fr> - 2.0.0-3
- Remove gcc-c++ from BuildRequires as it is an exception.
- Fix command in %%check and pass CXXFLAGS to scons.
- Use %%global instead of %%define.

* Thu Dec 12 2013 Milan Bouchet-Valat <nalimilan@club.fr> - 2.0.0-2
- Fix building when "--without static_libs" is passed.
- Remove %%ghost with libdouble-conversion.so.2.
- Drop BuildRoot.
- Use rm instead of %%{__rm} for consistency
- Use %%{?dist} in Release.

* Wed Dec 11 2013 Milan Bouchet-Valat <nalimilan@club.fr> - 2.0.0-1
- Initial Fedora package based on a PLD Linux RPM by Elan Ruusamäe <glen@delfi.ee>:
  http://git.pld-linux.org/gitweb.cgi?p=packages/double-conversion.git
