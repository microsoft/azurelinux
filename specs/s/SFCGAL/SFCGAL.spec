# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Summary: C++ wrapper library around CGAL for PostGIS
Name: SFCGAL
Version: 2.0.0
Release: 3%{?dist}
License: LGPL-2.0-or-later
URL: https://gitlab.com/Oslandia/SFCGAL/
Source: https://gitlab.com/sfcgal/SFCGAL/-/archive/v%{version}/SFCGAL-v%{version}.tar.bz2

BuildRequires: CGAL-devel >= 5.6
BuildRequires: gcc-c++
BuildRequires: cmake
BuildRequires: doxygen
BuildRequires: boost-devel
BuildRequires: mpfr-devel
BuildRequires: gmp-devel

%description
SFCGAL is a C++ wrapper library around CGAL with the aim of supporting
ISO 19107:2013 and OGC Simple Features Access 1.2 for 3D operations.

SFCGAL provides standard compliant geometry types and operations, that
can be accessed from its C or C++ APIs. PostGIS uses the C API, to
expose some SFCGAL's functions in spatial databases (cf. PostGIS
manual).

Geometry coordinates have an exact rational number representation and
can be either 2D or 3D.

%package devel
Summary: The development files for SFCGAL
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
Development headers and libraries for SFCGAL.

%prep
%autosetup -p0 -n SFCGAL-v%{version}

%build
%cmake -D LIB_INSTALL_DIR=%{_lib} -DBoost_NO_BOOST_CMAKE=BOOL:ON -DCMAKE_SKIP_RPATH:BOOL=YES -DSFCGAL_BUILD_DOC:BOOL=YES
%cmake_build
(cd doc; doxygen)

%install
%cmake_install

%files
%doc AUTHORS README.md NEWS
%license LICENSE
%{_libdir}/libSFCGAL.so.2*

%files devel
%{_includedir}/SFCGAL
%{_libdir}/libSFCGAL.so
%{_libdir}/pkgconfig/sfcgal.pc
%{_bindir}/sfcgal-config
%doc example/ doc/html

%changelog
* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jan 16 2025 Zenon Panoussis <oracle@provocation.net> - 2.0.0-1
- Bump to 2.0.0
- migrate the License tag to SPDX

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Sep 04 2024 Miroslav Suchý <msuchy@redhat.com> - 1.5.0-2
- convert license to SPDX

* Tue Aug 27 2024 Paul Wouters <paul.wouters@aiven.io> - 1.5.0-1
- Update to 1.5.0

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jan 17 2024 Jonathan Wakely <jwakely@redhat.com> - 1.4.1-4
- Rebuilt for Boost 1.83

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon Feb 20 2023 Jonathan Wakely <jwakely@redhat.com> - 1.4.1-2
- Rebuilt for Boost 1.81

* Thu Jan 19 2023 Paul Wouters <paul.wouters@aiven.io - 1.4.1-1
- Update to 1.4.1
- Resolves: rhbz#2045184 SFCGAL: FTBFS in Fedora rawhide/f36

* Wed Jan 18 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed May 04 2022 Thomas Rodgers <trodgers@redhat.com> - 1.4.0-3
- Rebuilt for Boost 1.78

* Wed Jan 19 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Nov 22 2021 Paul Wouters <paul.wouters@aiven.io> - 1.4.0-1
- Resolves: rhbz#2023547 update to version 1.4.0

* Tue Nov 16 2021 Paul Wouters <paul.wouters@aiven.io> - 1.3.10-8
- rebuilt against CGAL that was fixed for arm build

* Fri Aug 06 2021 Jonathan Wakely <jwakely@redhat.com> - 1.3.10-7
- Rebuilt for Boost 1.76

* Tue Jul 27 2021 Paul Wouters <paul.wouters@aiven.io> - 1.3.10-6
- Patch for CGAL 5.3 (https://gitlab.com/Oslandia/SFCGAL/-/merge_requests/246)

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.10-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon May 31 2021 Paul Wouters <paul.wouters@aiven.io> - 1.3.10-4
- Resolves: rhbz#1965111 package review items (build and ship html docs)

* Sun May 30 2021 Paul Wouters <paul.wouters@aiven.io> - 1.3.10-3
- Resolves: rhbz#1965111 package review items (don't ship docs/, skip check)

* Wed May 26 2021 Paul Wouters <paul.wouters@aiven.io> - 1.3.10-1
- Initial packaging for Fedora
- Cleanup for Fedora 34+
- Merged debian patches to support CGAL 5.x as per https://github.com/Oslandia/SFCGAL/pull/219

* Fri Oct 2 2020 Devrim Gündüz <devrim@gunduz.org> - 1.3.9-2
- We don't need CGAL dependency for CGAL >= 5.0 (Fedora 32 and above)

* Thu Oct 1 2020 Devrim Gündüz <devrim@gunduz.org> - 1.3.9-1
- Update to 1.3.9 for Fedora 33 (CGAL 5.1)

* Wed Aug 19 2020 Devrim Gündüz <devrim@gunduz.org> - 1.3.8-1
- Update to 1.3.8

* Thu Apr 23 2020 Devrim Gündüz <devrim@gunduz.org> - 1.3.7-4
- Add two patches for CGAL 5 builds

* Tue Mar 31 2020 Devrim Gündüz <devrim@gunduz.org> - 1.3.7-3
- Clarify dependencies on RHEL 8, per Talha Bin Rizwan.
- Depend on pgdg-srpm-macros

* Fri Jul 19 2019 John K. Harvey <john.harvey@crunchydata.com> - 1.3.7-2
- Fix broken macro

* Mon Jun 3 2019 Devrim Gündüz <devrim@gunduz.org> - 1.3.7-1
- Update to 1.3.7

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 1.3.2-1.1
- Rebuild against PostgreSQL 11.0

* Wed Sep 13 2017 Devrim Gündüz <devrim@gunduz.org> 1.3.2-1
- Update to 1.3.2 to support CGAL >= 4.10.1 on Fedora 26+

* Wed Jul 19 2017 Devrim Gündüz <devrim@gunduz.org> 1.2.2-2
- Also Requires CGAL, per Fahar Abbas (EDB QA)

* Thu Nov 19 2015 Oskari Saarenmaa <os@ohmu.fi> 1.2.2-1
- Update to 1.2.2 to support newer CGAL versions

* Fri Oct 30 2015 Devrim Gündüz <devrim@gunduz.org> 1.2.0-1
- Initial build for PostgreSQL YUM Repository.
