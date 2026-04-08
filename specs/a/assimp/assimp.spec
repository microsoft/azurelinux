# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%define soversion 6

Name:           assimp
Version:        6.0.4
Release:        1%{?dist}
Summary:        Library to import various 3D model formats into applications

# Assimp is BSD
# Bundled contrib/clipper is Boost
# Bundled contrib/Open3DGC is MIT
# Bundled contrib/openddlparser is MIT
# Bundled contrib/stb is MIT
# Bundled contrib/unzip is zlib
# Bundled contrib/zip is unlicense
# Bundled contrib/zlib is zlib
License:        BSD-3-Clause AND MIT AND BSL-1.0 AND Unlicense AND Zlib
URL:            https://github.com/assimp/assimp

# Github releases include nonfree models, source tarball must be re-generated
# using assimp_generate_tarball.sh
Source0:        %{name}-%{version}-free.tar.xz
Source1:        assimp_generate_tarball.sh

# Un-bundle poly2tri, pugixml, utf8cpp, RapidJSON, clipper
Patch0:         %{name}-unbundle.patch
# Add /usr/lib64 to library lookup paths for python modules
Patch1:         %{name}-pythonpath.patch
# Prevent export of bundled zlibstatic library
Patch2:         %{name}-nozlib.patch
# Exclude the build directory from the doxygen-generated documentation
# Fix HTML_OUTPUT dir in doxyfile
# Fix installing images from doc/architecture
Patch3:         %{name}-docs.patch
# Enable ctest
Patch4:         %{name}-tests.patch


BuildRequires:  boost-devel
BuildRequires:  cmake
BuildRequires:  doxygen
BuildRequires:  earcut-hpp-devel
BuildRequires:  gcc-c++
BuildRequires:  gtest-devel
BuildRequires:  make
BuildRequires:  pkgconfig(python3)
BuildRequires:  poly2tri-devel
BuildRequires:  pugixml-devel
BuildRequires:  python3-devel
BuildRequires:  zlib-devel
# Need to BR -static packages for header-only libraries for tracking, per
# guidelines
BuildRequires:  rapidjson-devel
BuildRequires:  rapidjson-static
BuildRequires:  stb_image-devel
BuildRequires:  stb_image-static
BuildRequires:  utf8cpp-devel
BuildRequires:  utf8cpp-static

# Incompatible - https://github.com/assimp/assimp/issues/788
#BuildRequires: pkgconfig(polyclipping)
Provides: bundled(polyclipping) = 4.8.8
Provides: bundled(open3dgc)
Provides: bundled(openddl-parser)
Provides: bundled(unzip)
Provides: bundled(minzip)


%description
Assimp, the Open Asset Import Library, is a free library to import
various well-known 3D model formats into applications.  Assimp aims
to provide a full asset conversion pipeline for use in game
engines and real-time rendering systems, but is not limited
to these applications.


%package devel
Summary: Header files and libraries for assimp
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: poly2tri-devel
Requires: pugixml-devel

%description devel
This package contains the header files and libraries
for assimp. If you would like to develop programs using assimp,
you will need to install assimp-devel.


%package -n python3-%{name}
Summary: Python 3 bindings for assimp
BuildArch: noarch
Requires: %{name} = %{version}-%{release}

%description -n python3-%{name}
This package contains the PyAssimp3 python bindings


%package doc
Summary: Assimp documentation
BuildArch: noarch

%description doc
%{summary}.


%prep
%autosetup -p1 -n %{name}-%{version}
# Get rid of bundled libs so we can't accidently build against them, except:
# - clipper: Unpackaged
# - Open3DGC: Unpackaged
# - openddlparser: Unpackaged
# - tinyusdz: Unpackaged
# - unzip: Modified minizip
# - zip: Modified minizip
find contrib/ -maxdepth 1 -mindepth 1 \
  | grep -Ev '(clipper|Open3DGC|openddlparser|tinyusdz|unzip|zip)' \
  | xargs rm -r

mv contrib/openddlparser/LICENSE contrib/openddlparser/LICENSE.openddlparser


%build
%cmake \
%ifarch s390x ppc64
 -DAI_BUILD_BIG_ENDIAN=TRUE \
%endif
 -DASSIMP_WARNINGS_AS_ERRORS=OFF \
 -DASSIMP_BUILD_ASSIMP_TOOLS=ON \
 -DASSIMP_BUILD_DOCS=ON \
 -DASSIMP_IGNORE_GIT_HASH=ON \
 -DHAVE_POLY2TRI=ON \
 -DPOLY2TRI_INCLUDE_PATH=%{_includedir}/poly2tri \
 -DPOLY2TRI_LIB=poly2tri \
 -DHTML_OUTPUT=out/html \
 -DCMAKE_INSTALL_DOCDIR=%{_defaultdocdir}/%{name}

%cmake_build


%install
%cmake_install
mkdir -p %{buildroot}%{python3_sitelib}/pyassimp/
install -m0644 port/PyAssimp/pyassimp/*.py %{buildroot}%{python3_sitelib}/pyassimp/


%check
# Exclude tests that rely on nonbsd models
exclude="utMD5Importer.importBoarMan|utMD5Importer.importBob|utMD2Importer.importDolphin|utMD2Importer.importFlag|utMD2Importer.importHorse|utQ3BSPImportExport.importerTest|utBlenderImporter.importBob|utBlenderImporter.importFleurOptonl|utPMXImporter.importTest|utXImporter.importDwarf|utDXFImporterExporter.importRifle|utX3DImportExport.importX3DChevyTahoe|ut3DSImportExport.importGranate|ut3DSImportExport.importJeep1|ut3DSImportExport.importMp5Sil|ut3DSImportExport.importMarRifle|ut3DSImportExport.importPyramob|ut3DImportExport.importMarRifle|ut3DImportExport.importMarRifleA|ut3DImportExport.importMarRifleD|ut3DSImportExport.importCartWheel"
%ifarch s390x aarch64
%ctest --exclude-regex $exclude || :
%else
%ctest --exclude-regex $exclude || :
%endif


%files
%license LICENSE
%license contrib/clipper/License.txt
%license contrib/openddlparser/LICENSE.openddlparser
%license contrib/zip/UNLICENSE
%doc Readme.md CREDITS
%{_bindir}/assimp
%{_libdir}/libassimp.so.6
%{_libdir}/libassimp.so.6.0.4

%files devel
%{_includedir}/assimp/
%{_libdir}/libassimp.so
%{_libdir}/pkgconfig/assimp.pc
%{_libdir}/cmake/assimp-*/

%files doc
%{_docdir}/*

%files -n python3-%{name}
%doc port/PyAssimp/README.md
%{python3_sitelib}/pyassimp/


%changelog
* Tue Jan 27 2026 Sandro Mani <manisandro@gmail.com> - 6.0.4-1
- Update to 6.0.4

* Tue Jan 20 2026 Sandro Mani <manisandro@gmail.com> - 6.0.3-1
- Update to 6.0.3

* Fri Jan 16 2026 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Fri Jan 16 2026 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Sat Dec 27 2025 Sandro Mani <manisandro@gmail.com> - 6.0.2-5
- PyAssimp: Re-add 'aiProcess_Triangulate' (#2423174)

* Sun Dec 14 2025 Sandro Mani <manisandro@gmail.com> - 6.0.2-4
- Backport fix for CVE-2025-11277

* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 6.0.2-3
- Rebuilt for Python 3.14.0rc3 bytecode

* Mon Aug 18 2025 Sandro Mani <manisandro@gmail.com> - 6.0.2-2
- Fix pugixml::pugixml dependency ending up in link interface of assimp::assimp

* Fri Aug 15 2025 Sandro Mani <manisandro@gmail.com> - 6.0.2-1
- Update to 6.0.2

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 5.4.3-4
- Rebuilt for Python 3.14.0rc2 bytecode

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 5.4.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 5.4.3-2
- Rebuilt for Python 3.14

* Sat Mar 15 2025 Rich Mattes <richmattes@gmail.com> - 5.4.3-1
- Update to release 5.4.3
- Resolves: #2274012

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 5.3.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Aug 28 2024 Miroslav Suchý <msuchy@redhat.com> - 5.3.1-4
- convert license to SPDX

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Jun 08 2024 Python Maint <python-maint@redhat.com> - 5.3.1-2
- Rebuilt for Python 3.13

* Sun Mar 31 2024 Rich Mattes <richmattes@gmail.com> - 5.3.1-1
- Update to release 5.3.1
- Resolves: rhbz#2256587

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.2.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.2.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jan 03 2024 Scott K Logan <logans@cottsay.net> - 5.2.5-2
- Add pugixml and poly2tri devel dependencies to assimp-devel

* Fri Nov 24 2023 Rich Mattes <richmattes@gmail.com> - 5.2.5-1
- Add check section and fix ctest configuration

* Thu Oct 26 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 5.2.5-1
- Ensure stb_image contains the latest CVE patches

* Fri Jul 28 2023 Scott K Logan <logans@cottsay.net> - 5.2.5-1
- Update to release 5.2.5

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 5.0.1-11
- Rebuilt for Python 3.12

* Wed Jan 18 2023 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 5.0.1-8
- Rebuilt for Python 3.11

* Sat Apr 23 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 5.0.1-7
- Security fix for CVE-2022-28041
- Drop dependency on pkgconfig(zzip-zlib-config), no longer available in
  zziplib; use zlib directly instead

* Wed Jan 19 2022 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Dec 30 2021 Rich Mattes <richmattes@gmail.com> - 5.0.1-5
- Correct Unlicense shortname (rhbz#2036000)

* Sat Sep 11 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 5.0.1-4
- Unbundle stb_image
- Add -static BR’s for header-only libraries utf8cpp and rapidjson

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.1-30
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 3.3.1-29
- Rebuilt for Python 3.10

* Mon Mar 29 2021 Rich Mattes <richmattes@gmail.com> - 5.0.1-3
- Fix library install dir specification (rhbz#1943862)
- Remove un-needed build dependency on ILUT

* Tue Mar 23 2021 Scott K Logan <logans@cottsay.net> - 5.0.1-2
- Add an upstream patch to fix imported library locations

* Sat Feb 27 2021 Rich Mattes <richmattes@gmail.com> - 5.0.1-1
- Update to release 5.0.1

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.1-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Aug 18 2020 Jeff Law <law@redhat.com> - 3.3.1-27
- Fix minor C++17 issues

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.1-26
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.1-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 3.3.1-24
- Rebuilt for Python 3.9

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.1-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 3.3.1-22
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 3.3.1-21
- Rebuilt for Python 3.8

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.1-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.1-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jan 14 2019 Miro Hrončok <mhroncok@redhat.com> - 3.3.1-18
- Subpackage python2-assimp has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Tue Aug 28 2018 Patrik Novotný <panovotn@redhat.com> - 3.3.1-17
- update requires to minizip-compat(-devel), rhbz#1609830, rhbz#1615381

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.1-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jul 02 2018 Miro Hrončok <mhroncok@redhat.com> - 3.3.1-15
- Rebuilt for Python 3.7

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.1-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Oct 02 2017 Troy Dawson <tdawson@redhat.com> - 3.3.1-13
- Cleanup spec file conditionals

* Sun Aug 06 2017 Björn Esser <besser82@fedoraproject.org> - 3.3.1-12
- Rebuilt for AutoReq cmake-filesystem

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jul 03 2017 Jonathan Wakely <jwakely@redhat.com> - 3.3.1-9
- Rebuilt for Boost 1.64

* Thu May 18 2017 Helio Chissini de Castro <helio@kde.org> - 3.3.1-8
- Fix invalid pkgconfig generation

* Mon May 15 2017 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_27_Mass_Rebuild

* Sat May 13 2017 Orion Poplawski <orion@cora.nwra.com> - 3.3.1-6
- Properly find poly2tri and note use of bundled polyclipping

* Fri May 05 2017 Than Ngo <than@redhat.com> - 3.3.1-5
- fixed build issue on bigendian platform s390x/ppc64
- dropped excludearch s390x ppc64

* Fri May 05 2017 Helio Chissini de Castro <helio@kde.org> - 3.3.1-4
- Disable ppc64le and s390x arches due bigendian issue not yet solved

* Sat Apr 29 2017 Helio Chissini de Castro <helio@kde.org> - 3.3.1-3
- Compile assimp with current exterbal irrXML

* Wed Apr 19 2017 Helio Chissini de Castro <helio@kde.org> - 3.3.1-2
- Revamp assimp with new upstream release 3.3.1 plus new upstreamed doc patches

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Jan 27 2017 Jonathan Wakely <jwakely@redhat.com> - 3.2.0-6
- Rebuilt for Boost 1.63

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 3.2.0-5
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.0-4
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Fri Jul 01 2016 Dan Horák <dan[at]danny.cz> - 3.2.0-3
- Fix build on big endian platforms

* Fri Jun 03 2016 Rich Mattes <richmattes@gmail.com> - 3.2.0-2
- Fix pkgconfig and cmake files (rhbz#1340656)

* Mon May 09 2016 Rich Mattes <richmattes@gmail.com> - 3.2.0-1
- Update to release 3.2.0 (rhbz#1332434)

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jan 14 2016 Jonathan Wakely <jwakely@redhat.com> - 3.1.1-8
- Rebuilt for Boost 1.60

* Wed Dec 09 2015 Rich Mattes <richmattes@gmail.com> - 3.1.1-7
- Add patch to fix build on big-endian architectures

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.1-6
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Thu Sep 17 2015 Rich Mattes <richmattes@gmail.com> - 3.1.1-5
- Fix assimp-config paths (rhbz#1263698)
- Build against system boost instead of using included workaround

* Thu Aug 27 2015 Jonathan Wakely <jwakely@redhat.com> - 3.1.1-4
- Rebuilt for Boost 1.59

* Wed Jul 29 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/F23Boost159

* Wed Jul 22 2015 David Tardon <dtardon@redhat.com> - 3.1.1-2
- rebuild for Boost 1.58

* Fri Jul 03 2015 Rich Mattes <richmattes@gmail.com> - 3.1.1-1
- Update to release 3.1.1 (rhbz#1206371)
- Remove upstreamed patches
- Correct python package names
- Use license macro

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.1270-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 3.0.1270-10
- Rebuilt for GCC 5 C++11 ABI change

* Mon Jan 26 2015 Petr Machata <pmachata@redhat.com> - 3.0.1270-9
- Rebuild for boost 1.57.0

* Fri Aug 15 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.1270-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.1270-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 28 2014 Kalev Lember <kalevlember@gmail.com> - 3.0.1270-6
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Thu May 22 2014 Petr Machata <pmachata@redhat.com> - 3.0.1270-5
- Rebuild for boost 1.55.0

* Sun Mar 02 2014 Scott K Logan <logans@cottsay.net> - 3.0.1270-4
- Changed upstream source to Github
- Un-commented assimp-python, added python-devel to build deps
- Added assimp-python3 subpackage

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.1270-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 30 2013 Petr Machata <pmachata@redhat.com> - 3.0.1270-2
- Rebuild for boost 1.54.0

* Wed May 01 2013 Rich Mattes <richmattes@gmail.com> 3.0.1270-1
- Update to release 3.0.1270

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.863-9.20110824svn
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Oct 25 2012 Rich Mattes <richmattes@gmail.com> - 2.0.863-8.20110824svn
- Install python bindings

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.863-7.20110824svn
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul  3 2012 Tom Callaway <spot@fedoraproject.org> - 2.0.863-6.20110824svn
- rebuild against new irrlicht/irrxml

* Wed Apr 11 2012 Rich Mattes <richmattes@gmail.com> - 2.0.863-5.20110824svn
- Changed spec to use buildroot macro

* Sat Dec 17 2011 Rich Mattes <richmattes@gmail.com> - 2.0.863-4.20110824svn
- Fixed pkgconfig paths

* Wed Aug 24 2011 Rich Mattes <richmattes@gmail.com> - 2.0.863-3.20110824svn
- Upgrade to latest svn snapshot
- Port changes to link against system irrXML
- Removed upstreamed zlib/unzip unbundling patches

* Thu Mar 24 2011 Rich Mattes <richmattes@gmail.com> - 2.0.863-2.20110324svn
- Upgrade to latest svn snapshot
- Port changes to link against libIrrXML

* Sat Dec 18 2010 Rich Mattes <richmattes@gmail.com> - 2.0.863-1
- Upgrade to release 2.0

* Mon Sep 20 2010 Rich Mattes <richmattes@gmail.com> - 1.1.700-3
- Remove extra buildrequires
- Generate doxygen docs manually

* Mon Sep 20 2010 Rich Mattes <richmattes@gmail.com> - 1.1.700-2
- Included doxygen-generated docs
- Using original .zip file from project download page

* Sun Sep 19 2010 Rich Mattes <richmattes@gmail.com> - 1.1.700-1
- First build
