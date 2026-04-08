# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# CGAL is a header-only library, with dependencies.
%global debug_package %{nil}

# Min dependencies
%global boost_version 1.72
%global qt_version 6.4
%global cmake_version 3.22

%global fullversion %{version}
#global fullversion 5.6-beta1


Name:           CGAL
Version:        6.0.3
Release:        1%{?dist}
Summary:        Computational Geometry Algorithms Library

# Automatically converted from old format: LGPLv3+ and GPLv3+ and Boost - review is highly recommended.
License:        LGPL-3.0-or-later AND GPL-3.0-or-later AND BSL-1.0
URL:            http://www.cgal.org/
Source0:        https://github.com/CGAL/cgal/releases/download/v%{fullversion}/%{name}-%{fullversion}.tar.xz

# Required devel packages.
BuildRequires: cmake >= %{cmake_version}
BuildRequires: gcc-c++
BuildRequires: gmp-devel
BuildRequires: boost-devel >= %{boost_version}
BuildRequires: mpfr-devel
BuildRequires: qt6-qtbase-devel >= %{qt_version}
BuildRequires: qt6-qtsvg-devel >= %{qt_version}
BuildRequires: qt6-qtdeclarative-devel >= %{qt_version}
BuildRequires: qt6-qttools-devel >= %{qt_version}
BuildRequires: make

%description
Libraries for CGAL applications.
CGAL is a collaborative effort of several sites in Europe and
Israel. The goal is to make the most important of the solutions and
methods developed in computational geometry available to users in
industry and academia in a C++ library. The goal is to provide easy
access to useful, reliable geometric algorithms.


%package devel
Summary:        Development files and tools for CGAL applications
Provides:       CGAL-static = %{version}-%{release}
Requires:       cmake
Requires:       boost-devel%{?_isa} >= %{boost_version}
Requires:       gmp-devel%{?_isa}
Requires:       mpfr-devel%{?_isa}
Recommends:     zlib-devel%{?_isa}
Recommends:     eigen3-devel
%description devel
Libraries for CGAL applications.
CGAL is a collaborative effort of several sites in Europe and
Israel. The goal is to make the most important of the solutions and
methods developed in computational geometry available to users in
industry and academia in a C++ library. The goal is to provide easy
access to useful, reliable geometric algorithms.
The %{name}-devel package provides the headers files and tools you may need to
develop applications using CGAL.



%package qt6-devel
Summary:        Development files and tools for CGAL applications using CGAL_qt6
Requires:       %{name}-devel = %{version}-%{release}
Requires:       qt6-qtbase-devel%{?_isa} >= %{qt_version}
Requires:       qt6-qtsvg-devel%{?_isa} >= %{qt_version}
Requires:       qt6-qtdeclarative-devel%{?_isa} >= %{qt_version}
Requires:       qt6-qttools-devel%{?_isa} >= %{qt_version}
%description qt6-devel
The %{name}-qt6-devel package provides the headers files and tools you
may need to develop applications using the CGAL_qt6 component of CGAL.


%package demos-source
BuildArch:      noarch
Summary:        Examples and demos of CGAL algorithms
Requires:       %{name}-devel = %{version}-%{release}
%description demos-source
The %{name}-demos-source package provides the sources of examples and demos of
CGAL algorithms.


%prep
%setup -q -n %{name}-%{fullversion}

# Fix some file permissions
#chmod a-x include/CGAL/export/ImageIO.h

# Install README.Fedora here, to include it in %%doc
cat << 'EOF' > ./README.Fedora
Header-only
-----------
CGAL is a header-only library since version 5.0.

Packages
--------
In Fedora, the CGAL tarball is separated in several packages:
  - CGAL is empty since CGAL-5.0
  - CGAL-devel contains header files, and several files and tools needed to
  develop CGAL applications,
  - CGAL-demos-source contains the source of examples and demos of CGAL.


Documentation
-------------
Note that the CGAL documentation cannot be packaged for Fedora due to unclear
license conditions. The complete documentation in PDF and HTML is
available at http://www.cgal.org/Manual/index.html
EOF

%build

%cmake -DCGAL_DO_NOT_WARN_ABOUT_CMAKE_BUILD_TYPE=ON -DCGAL_INSTALL_LIB_DIR=%{_datadir} -DCGAL_INSTALL_DOC_DIR=
%cmake_build

%install
rm -rf %{buildroot}

%cmake_install

# Install demos and examples
mkdir -p %{buildroot}%{_datadir}/CGAL
touch -r demo %{buildroot}%{_datadir}/CGAL/
cp -a demo %{buildroot}%{_datadir}/CGAL/demo
cp -a examples %{buildroot}%{_datadir}/CGAL/examples

%check
rm -rf include/
mkdir build-example
cd build-example
cmake -L "-DCMAKE_PREFIX_PATH=%{buildroot}/usr" %{buildroot}%{_datadir}/CGAL/examples/Triangulation_2
make constrained_plus
ldd ./constrained_plus
./constrained_plus

%files devel
%license AUTHORS LICENSE LICENSE.BSL LICENSE.RFL LICENSE.LGPL LICENSE.GPL
%doc CHANGES.md README.Fedora
%{_includedir}/CGAL
%exclude %{_includedir}/CGAL/Qt
%dir %{_datadir}/CGAL
%{_datadir}/cmake/CGAL
%exclude %{_datadir}/cmake/CGAL/demo
%{_bindir}/*
%{_mandir}/man1/cgal_create_cmake_script.1.gz

%files qt6-devel
%{_includedir}/CGAL/Qt
%{_datadir}/cmake/CGAL/demo

%files demos-source
%{_datadir}/CGAL/demo
%{_datadir}/CGAL/examples
%exclude %{_datadir}/CGAL/*/*/skip_vcproj_auto_generation

%changelog
* Mon Jan 26 2026 Laurent Rineau <laurent.rineau@cgal.org> - 6.0.3-1
- New upstream release 6.0.3

* Thu Sep 18 2025 Laurent Rineau <laurent.rineau@cgal.org> - 6.0.2-1
- New upstream release 6.0.2

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Oct 22 2024 Laurent Rineau <laurent.rineau@cgal.org> - 6.0.1-1
- Update to new upstream version 6.0.1 (#2321007)

* Tue Oct 15 2024 Laurent Rineau <laurent.rineau@cgal.org> - 6.0-1
- Update CGAL to version 6.0 and adjust dependencies

* Wed Aug  7 2024 Miroslav Suchý <msuchy@redhat.com> - 5.6.1-3
- convert license to SPDX

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Mar 13 2024 Fedora Release Monitoring <release-monitoring@fedoraproject.org> - 5.6.1-1
- Update to 5.6.1 (#2269356)

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jan 18 2024 Jonathan Wakely <jwakely@redhat.com> - 5.6-3
- Rebuilt for Boost 1.83

* Thu Jan 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 28 2023 Laurent Rineau <laurent.rineau@cgal.org> - 5.6-1
- New upstream release

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 5.6-0.2.beta1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 20 2023 Laurent Rineau <laurent.rineau@cgal.org> - 5.6-0.1.beta1
- New upstream release

* Tue Feb 28 2023 Laurent Rineau <laurent.rineau@cgal.org> - 5.5.2-2
- Update to 5.5.2 (#2174148)
- CGAL-demos-source is now noarch

* Wed Jan 18 2023 Fedora Release Engineering <releng@fedoraproject.org> - 5.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Oct 12 2022 Fedora Release Monitoring <release-monitoring@fedoraproject.org> - 5.5.1-1
- Update to 5.5.1 (#2134129)

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 5.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jul 15 2022 Fedora Release Monitoring <release-monitoring@fedoraproject.org> - 5.5-1
- Update to 5.5 (#2107703)

* Mon Jun 13 2022 Laurent Rineau <laurent.rineau@cgal.org> - 5.5-0.1.beta1
- New upstream beta release

* Tue Jun  7 2022 Laurent Rineau <laurent.rineau@cgal.org> - 5.4.1
- New upstream release
- Updates for new CMake RPM macros

* Mon Jan 31 2022 Fedora Release Monitoring <release-monitoring@fedoraproject.org> - 5.4-1
- Update to 5.4 (#2048685)

* Wed Jan 19 2022 Fedora Release Engineering <releng@fedoraproject.org> - 5.4-0.2.beta1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Dec 29 2021 Laurent Rineau <laurent.rineau@cgal.org> - 5.4-0.1.beta1
- New upstream release

* Tue Dec 28 2021 Laurent Rineau <laurent.rineau@cgal.org> - 5.3.1-1
- New upstream release
- Remove patch `CGAL-5.3-armv7.patch` (integrated upstream)

* Tue Nov 16 2021 Paul Wouters <paul.wouters@aiven.io> - 5.3-3
- Resolves: rhbz#1967742 SFCGAL does not compile on ARM due to bug in CGAL

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 5.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jul  6 2021 Laurent Rineau <laurent.rineau@cgal.org> - 5.3-1
- New upstream release

* Fri Jun  4 2021 Laurent Rineau <laurent.rineau@cgal.org> - 5.3-0.1.beta1
- New upstream release

* Wed Jun  2 2021 Laurent Rineau <laurent.rineau@cgal.org> - 5.2.2-1
- New upstream release

* Wed Mar 17 2021 Laurent Rineau <laurent.rineau@cgal.org> - 5.2.1-1
- New upstream release

* Mon Jan 25 2021 Fedora Release Engineering <releng@fedoraproject.org> - 5.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Dec 22 2020 Laurent Rineau <laurent.rineau@cgal.org> - 5.2-1
- New upstream release

* Wed Nov 18 2020 Laurent Rineau <laurent.rineau@cgal.org> - 5.2-0.1.beta1
- New upstream release

* Mon Nov 16 2020 Laurent Rineau <laurent.rineau@cgal.org> - 5.1.1-1
- New upstream release

* Tue Sep  8 2020 Laurent Rineau <laurent.rineau@cgal.org> - 5.1-1
- New upstream release

* Tue Jul 28 2020 Laurent Rineau <laurent.rineau@cgal.org> - 5.1-0.2.beta2
- Install CMake files in `/usr/share/cmake/CGAL/`.
- Add a `%%check` section.

* Tue Jul 28 2020 Laurent Rineau <laurent.rineau@cgal.org> - 5.1-0.1-beta2
- New upstream release 5.1-beta2

* Mon Jul 27 2020 Laurent Rineau <laurent.rineau@cgal.org> - 5.0.2-4
- Fix for Fedora 33

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Mar  9 2020 Laurent Rineau <laurent.rineau@cgal.org> - 5.0.2-2
- Fix Bug 1811647:
      %%{?_isa} qualifier unnecessary / broken for BuildRequires
  https://bugzilla.redhat.com/show_bug.cgi?id=1811647

* Tue Feb 25 2020 Laurent Rineau <laurent.rineau@cgal.org> - 5.0.2-1
- New upstream release
- Remove the Source10 (replaced by a heredoc)

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Jan 27 2020 Laurent Rineau <laurent.rineau@cgal.org> - 5.0.1-1
- New upstream release

* Fri Nov  8 2019 Laurent Rineau <laurent.rineau@cgal.org> - 5.0-1
- New upstream release

* Thu Oct 31 2019 Laurent Rineau <laurent.rineau@cgal.org> - 5.0-0.4.beta2
- New upstream beta release, 5.0-beta2
- Re-add the dependency to zlib with `Recommends:`
- Add a sub-package CGAL-qt5-devel, that requires Qt5 devel packages

* Tue Oct  1 2019 Laurent Rineau <laurent.rineau@cgal.org> - 5.0-0.3.beta1
- CGAL-devel is now noarch

* Tue Oct  1 2019 Laurent Rineau <laurent.rineau@cgal.org> - 5.0-0.2.beta1
- Remove the CGAL main package
- Add Provides: CGAL-static

* Tue Oct  1 2019 Laurent Rineau <laurent.rineau@cgal.org> - 5.0-0.1.beta1
- New upstream beta release, header-only
- Remove the dependency on Qt5 and Zlib

* Tue Oct  1 2019 Laurent Rineau <laurent.rineau@cgal.org> - 4.14.1-1
- New upstream release

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Apr  1 2019 Laurent Rineau <laurent.rineau@cgal.org> - 4.14-1
- New upstream release

* Wed Mar 27 2019 Laurent Rineau <laurent.rineau@cgal.org> - 4.14-0.3beta3
- New upstream release

* Mon Mar 25 2019 Laurent Rineau <laurent.rineau@cgal.org> - 4.14-0.1beta2
- New upstream release

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.13-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jan 24 2019 Jonathan Wakely <jwakely@redhat.com> - 4.13-2
- Rebuilt for Boost 1.69

* Tue Oct  9 2018 Laurent Rineau <laurent.rineau@cgal.org> - 4.13-1
- New upstream version

- Add `CGAL_DO_NOT_WARN_ABOUT_CMAKE_BUILD_TYPE` in the CMake
  configuration, to suppress a warning.

* Wed Aug 22 2018 Laurent Rineau <laurent.rineau@cgal.org> - 4.13-0.2.beta1
- add weak dependency to eigen3-devel

* Wed Aug 22 2018 Laurent Rineau <laurent.rineau@cgal.org> - 4.13-0.1.beta1
- New upstream release

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Apr 27 2018 Laurent Rineau <laurent.rineau@cgal.org> - 4.12-1
- New upstream version

* Tue Feb 27 2018 Laurent Rineau <laurent.rineau@cgal.org> - 4.12-0.2beta2
- New upstream release

* Tue Feb 27 2018 Laurent Rineau <laurent.rineau@cgal.org> - 4.11.1-2
- Restore the SPEC file changelog

* Tue Feb 27 2018 Laurent Rineau <laurent.rineau@cgal.org> - 4.11.1-1
- New upstream release

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Jan 22 2018 Jonathan Wakely <jwakely@redhat.com> - 4.11-2
- Rebuilt for Boost 1.66
