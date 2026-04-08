## START: Set by rpmautospec
## (rpmautospec version 0.8.4)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 15;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Enabled by default
%bcond_without tests

# note ABI does not change in patch releases
# https://sourceforge.net/p/gdcm/mailman/message/36768376/

# Docs do not build on i686 because some LaTeX deps are unsatisfied. So skip
# these docs entirely.
%bcond_with texdocs

Name:       gdcm
Version:    3.0.24
Release:    %autorelease
Summary:    Grassroots DiCoM is a C++ library to parse DICOM medical files
# SPDX
License:    BSD-3-Clause
URL:        https://sourceforge.net/projects/gdcm/
# Use github release
Source0:    https://github.com/malaterre/%{name}/archive/v%{version}/%{name}-%{version}.tar.gz
Source1:    http://downloads.sourceforge.net/project/gdcm/gdcmData/gdcmData/gdcmData.tar.gz

Patch1: 0001-3.0.1-Use-copyright.patch
# Fix for 1687233
Patch2: 0002-Fix-export-variables.patch
Patch3: gdcm-3.0.24-c++20.patch

BuildRequires:  CharLS-devel >= 2.2
BuildRequires:  cmake
BuildRequires:  doxygen
BuildRequires:  libxslt-devel
BuildRequires:  dcmtk-devel
BuildRequires:  docbook5-style-xsl
BuildRequires:  docbook-style-xsl
BuildRequires:  expat-devel
BuildRequires:  fontconfig-devel
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  git-core
BuildRequires:  graphviz
BuildRequires:  gl2ps-devel
BuildRequires:  libogg-devel
BuildRequires:  libtheora-devel
BuildRequires:  libuuid-devel
BuildRequires:  mesa-libGL-devel
BuildRequires:  openssl-devel
BuildRequires:  pkgconfig(libopenjp2)
BuildRequires:  poppler-devel
BuildRequires:  python3-devel
BuildRequires:  swig
BuildRequires:  sqlite-devel
BuildRequires:  json-c-devel
BuildRequires:  libxml2-devel
BuildRequires:  make

# BuildRequires:  vtk-devel

# deps aren't available on i686, so we skip docs building entirely
%if %{with texdocs}
BuildRequires:  texlive-scheme-medium
BuildRequires:  tex(hanging.sty)
BuildRequires:  tex(tocloft.sty)
BuildRequires:  tex(newunicodechar.sty)
%endif


%description
Grassroots DiCoM (GDCM) is a C++ library for DICOM medical files.
It supports ACR-NEMA version 1 and 2 (huffman compression is not supported),
RAW, JPEG, JPEG 2000, JPEG-LS, RLE and deflated transfer syntax.
It comes with a super fast scanner implementation to quickly scan hundreds of
DICOM files. It supports SCU network operations (C-ECHO, C-FIND, C-STORE,
C-MOVE). PS 3.3 & 3.6 are distributed as XML files.
It also provides PS 3.15 certificates and password based mechanism to
anonymize and de-identify DICOM datasets.

%package    doc
Summary:    Includes html documentation for gdcm
BuildArch:  noarch
Provides:   %{name}-examples = %{version}-%{release}
Obsoletes:  %{name}-examples < %{version}-%{release}

%description doc
You should install the gdcm-doc package if you would like to
access upstream documentation for gdcm.
Includes CSharp, C++, Java, PHP and Python example programs for GDCM
in html pages

%package    applications
Summary:    Includes command line programs for GDCM
Requires:   %{name}%{?_isa} = %{version}-%{release}

%description applications
You should install the gdcm-applications package if you would like to
use command line programs part of GDCM. Includes tools to convert,
anonymize, manipulate, concatenate, and view DICOM files.

%package    devel
Summary:    Libraries and headers for GDCM
Requires:   %{name}%{?_isa} = %{version}-%{release}
Requires:   %{name}-applications%{?_isa} = %{version}-%{release}

%description devel
You should install the gdcm-devel package if you would like to
compile applications based on gdcm

%package -n python3-gdcm
Summary:    Python binding for GDCM
%{?python_provide:%python_provide python3-gdcm}
Requires:   %{name}%{?_isa} = %{version}-%{release}

%description -n python3-gdcm
You should install the python3-gdcm package if you would like to
used this library with python

%prep
%autosetup -n GDCM-%{version} -S git
# Data source
%setup -n GDCM-%{version} -q -T -D -a 1

# deps not available
%if %{with texdocs}
sed -i.backup 's/^GENERATE_LATEX.*=.*YES/GENERATE_LATEX = NO/' Utilities/doxygen/doxyfile.in
%endif

# Remove bundled utilities (we use Fedora's ones)
rm -rf Utilities/gdcmexpat
rm -rf Utilities/gdcmopenjpeg-v1
rm -rf Utilities/gdcmopenjpeg-v2
rm -rf Utilities/gdcmzlib
rm -rf Utilities/gdcmuuid
rm -rf Utilities/gdcmcharls

# Remove bundled utilities (we don't use them)
rm -rf Utilities/getopt
rm -rf Utilities/pvrg
rm -rf Utilities/rle
rm -rf Utilities/wxWidgets

# Needed for testing:
#rm -rf Utilities/gdcmmd5

# cmake version changed, need to update minimum version
sed -i -e 's@cmake_minimum_required(VERSION 2.8.7)@cmake_minimum_required(VERSION 3.5)@' Examples/CMakeLists.txt

%build
%cmake \
    -DCMAKE_VERBOSE_MAKEFILE=ON \
    -DGDCM_INSTALL_PACKAGE_DIR=%{_libdir}/cmake/%{name} \
    -DGDCM_INSTALL_INCLUDE_DIR=%{_includedir}/%{name} \
    -DGDCM_INSTALL_DOC_DIR=%{_docdir}/%{name} \
    -DGDCM_INSTALL_MAN_DIR=%{_mandir} \
    -DGDCM_INSTALL_LIB_DIR=%{_libdir} \
    -DGDCM_BUILD_TESTING:BOOL=ON \
    -DGDCM_DATA_ROOT=../gdcmData/ \
    -DGDCM_BUILD_EXAMPLES:BOOL=ON \
    -DGDCM_DOCUMENTATION:BOOL=OFF \
    -DGDCM_WRAP_PYTHON:BOOL=ON \
    -DPYTHON_EXECUTABLE=%{python3} \
    -DGDCM_INSTALL_PYTHONMODULE_DIR=%{python3_sitearch} \
    -DGDCM_WRAP_JAVA:BOOL=OFF \
    -DGDCM_WRAP_CSHARP:BOOL=OFF \
    -DGDCM_BUILD_SHARED_LIBS:BOOL=ON \
    -DGDCM_BUILD_APPLICATIONS:BOOL=ON \
    -DCMAKE_BUILD_TYPE:STRING="RelWithDebInfo" \
    -DGDCM_USE_VTK:BOOL=OFF \
    -DGDCM_USE_SYSTEM_CHARLS:BOOL=ON \
    -DGDCM_USE_SYSTEM_EXPAT:BOOL=ON \
    -DGDCM_USE_SYSTEM_OPENJPEG:BOOL=ON \
    -DGDCM_USE_SYSTEM_ZLIB:BOOL=ON \
    -DGDCM_USE_SYSTEM_UUID:BOOL=ON \
    -DGDCM_USE_SYSTEM_LJPEG:BOOL=OFF \
    -DGDCM_USE_SYSTEM_OPENSSL:BOOL=ON \
    -DGDCM_USE_JPEGLS:BOOL=ON \
    -DGDCM_USE_SYSTEM_LIBXML2:BOOL=ON \
    -DGDCM_USE_SYSTEM_JSON:BOOL=ON \
    -DGDCM_USE_SYSTEM_POPPLER:BOOL=ON

#Cannot build wrap_java:
#   -DGDCM_VTK_JAVA_JAR:PATH=/usr/share/java/vtk.jar no found!
#   yum provides */vtk.jar -> No results found

%cmake_build

%install
%cmake_install

%if %{with tests}
%check
# Making the tests informative only for now. Several failing tests (27/228):
# 11,40,48,49,107-109,111-114,130-135,146,149,,151-154,157,194,216,219
make test -C %{__cmake_builddir} || exit 0
%endif

%files
%doc AUTHORS README.md
%license Copyright.txt README.Copyright.txt
%{_libdir}/libgdcmCommon.so.3.0
%{_libdir}/libgdcmCommon.so.3.0.24
%{_libdir}/libgdcmDICT.so.3.0
%{_libdir}/libgdcmDICT.so.3.0.24
%{_libdir}/libgdcmDSED.so.3.0
%{_libdir}/libgdcmDSED.so.3.0.24
%{_libdir}/libgdcmIOD.so.3.0
%{_libdir}/libgdcmIOD.so.3.0.24
%{_libdir}/libgdcmMEXD.so.3.0
%{_libdir}/libgdcmMEXD.so.3.0.24
%{_libdir}/libgdcmMSFF.so.3.0
%{_libdir}/libgdcmMSFF.so.3.0.24
%{_libdir}/libgdcmjpeg12.so.3.0
%{_libdir}/libgdcmjpeg12.so.3.0.24
%{_libdir}/libgdcmjpeg16.so.3.0
%{_libdir}/libgdcmjpeg16.so.3.0.24
%{_libdir}/libgdcmjpeg8.so.3.0
%{_libdir}/libgdcmjpeg8.so.3.0.24
%{_libdir}/libgdcmmd5.so.3.0
%{_libdir}/libgdcmmd5.so.3.0.24
%{_libdir}/libsocketxx.so.1.2
%{_libdir}/libsocketxx.so.1.2.0
%dir %{_datadir}/%{name}-3.0/
%{_datadir}/%{name}-3.0/XML/

%files doc
%doc %{_docdir}/%{name}

%files applications
%{_bindir}/gdcmanon
%{_bindir}/gdcmconv
%{_bindir}/gdcmclean
%{_bindir}/gdcmdiff
%{_bindir}/gdcmdump
%{_bindir}/gdcmgendir
%{_bindir}/gdcmimg
%{_bindir}/gdcminfo
%{_bindir}/gdcmpap3
%{_bindir}/gdcmpdf
%{_bindir}/gdcmraw
%{_bindir}/gdcmscanner
%{_bindir}/gdcmscu
%{_bindir}/gdcmtar
%{_bindir}/gdcmxml
%doc %{_mandir}/man1/*.1*

%files devel
%{_includedir}/%{name}/
%{_libdir}/libgdcmCommon.so
%{_libdir}/libgdcmDICT.so
%{_libdir}/libgdcmDSED.so
%{_libdir}/libgdcmIOD.so
%{_libdir}/libgdcmMEXD.so
%{_libdir}/libgdcmMSFF.so
%{_libdir}/libgdcmjpeg12.so
%{_libdir}/libgdcmjpeg16.so
%{_libdir}/libgdcmjpeg8.so
%{_libdir}/libgdcmmd5.so
%{_libdir}/libsocketxx.so
%{_libdir}/cmake/%{name}/

%files -n python3-gdcm
%{python3_sitearch}/%{name}*.py
%{python3_sitearch}/_%{name}swig.so
%{python3_sitearch}/__pycache__/%{name}*

%changelog
## START: Generated by rpmautospec
* Mon Apr 06 2026 azldev <> - 3.0.24-15
- Latest state for gdcm

* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 3.0.24-14
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 3.0.24-13
- Rebuilt for Python 3.14.0rc2 bytecode

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.24-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jul 17 2025 Ankur Sinha (Ankur Sinha Gmail) <sanjay.ankur@gmail.com> - 3.0.24-11
- Rebuild for poppler 25.07.0

* Fri Jun 06 2025 Python Maint <python-maint@redhat.com> - 3.0.24-10
- Rebuilt for Python 3.14

* Fri May 30 2025 Karolina Surma <ksurma@redhat.com> - 3.0.24-9
- mesa-libOSMesa-devel was renamed to mesa-libGL-devel

* Mon Mar 03 2025 Tom Rix <Tom.Rix@amd.com> - 3.0.24-8
- cmake version changed

* Wed Feb 19 2025 Ankur Sinha (Ankur Sinha Gmail) <sanjay.ankur@gmail.com> - 3.0.24-7
- Rebuild for dcmtk 3.6.9

* Tue Feb 11 2025 Ankur Sinha (Ankur Sinha Gmail) <sanjay.ankur@gmail.com> - 3.0.24-6
- Rebuild for poppler 25.02.0

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.24-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Aug 22 2024 Marek Kasik <mkasik@redhat.com> - 3.0.24-4
- Rebuild for poppler 24.08.0

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.24-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jun 24 2024 Ankur Sinha (Ankur Sinha Gmail) <sanjay.ankur@gmail.com> - 3.0.24-2
- chore: mark data as source too (fixes rhbz#2278879)

* Mon Jun 24 2024 Ankur Sinha (Ankur Sinha Gmail) <sanjay.ankur@gmail.com> - 3.0.24-1
- feat: update to 3.0.24 (fixes rhbz#2278879)

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 3.0.23-7
- Rebuilt for Python 3.13

* Mon May 27 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 3.0.23-6
- Fix unowned directory /usr/share/gdcm-3.0/

* Fri Apr 26 2024 Sandro <devel@penguinpee.nl> - 3.0.23-5
- Apply security patches
- Fix TALOS-2024-1924, CVE-2024-22391 (RHBZ#2277288)
- Fix TALOS-2024-1935, CVE-2024-22373 (RHBZ#2277292)
- Fix TALOS-2024-1944, CVE-2024-25569 (RHBZ#2277296)

* Fri Apr 19 2024 Sandro <devel@penguinpee.nl> - 3.0.23-4
- Replace deprecated PyEval_CallObject() (RHBZ#2245816)

* Fri Mar 22 2024 Sérgio M. Basto <sergio@serjux.com> - 3.0.23-3
- Update URL

* Mon Feb 26 2024 Sandro <devel@penguinpee.nl> - 3.0.23-2
- Migrate to SPDX license

* Mon Feb 26 2024 Sandro <devel@penguinpee.nl> - 3.0.23-1
- Update to 3.0.23 (RHBZ#2257639)
- Drop `157.patch` (merged upstream)
- Bump soname

* Tue Feb 06 2024 Ankur Sinha (Ankur Sinha Gmail) <sanjay.ankur@gmail.com> - 3.0.22-7
- Rebuild for poppler 24.02.0

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.22-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.22-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Aug 07 2023 Marek Kasik <mkasik@redhat.com> - 3.0.22-4
- Rebuild for poppler 23.08.0

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.22-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 3.0.22-2
- Rebuilt for Python 3.12

* Sat Jun 10 2023 Orion Poplawski <orion@nwra.com> - 3.0.22-1
- Update to 3.0.22

* Mon Feb 06 2023 Ankur Sinha (Ankur Sinha Gmail) <sanjay.ankur@gmail.com> - 3.0.21-3
- chore: rebuild for poppler 23.02.0

* Mon Jan 30 2023 Ankur Sinha (Ankur Sinha Gmail) <sanjay.ankur@gmail.com> - 3.0.21-2
- fix: disable TeX doc generation

* Mon Jan 30 2023 Ankur Sinha (Ankur Sinha Gmail) <sanjay.ankur@gmail.com> - 3.0.21-1
- feat: update to 3.0.21 (fixes rhbz#2100773)

* Mon Jan 30 2023 Ankur Sinha (Ankur Sinha Gmail) <sanjay.ankur@gmail.com> - 3.0.20-2
- chore: upload sources

* Mon Jan 30 2023 Sérgio M. Basto <sergio@serjux.com> - 3.0.20-1
- Update GDCM to 3.0.20

* Mon Jan 30 2023 Sérgio M. Basto <sergio@serjux.com> - 3.0.12-7
- Make documentation again

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.12-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Aug 02 2022 Ankur Sinha (Ankur Sinha Gmail) <sanjay.ankur@gmail.com> - 3.0.12-5
- chore: rebuild for poppler 22.08.0

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.12-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 3.0.12-3
- Rebuilt for Python 3.11

* Fri May 20 2022 Sandro Mani <manisandro@gmail.com> - 3.0.12-2
- Rebuild for gdal-3.5.0 and/or openjpeg-2.5.0

* Sat Apr 02 2022 Ankur Sinha (Ankur Sinha Gmail) <sanjay.ankur@gmail.com> - 3.0.12-1
- feat: update to 3.0.12 (fixes rhbz#2068208)

* Tue Feb 08 2022 Ankur Sinha (Ankur Sinha Gmail) <sanjay.ankur@gmail.com> - 3.0.10-1
- feat: to 3.0.10 (fixes #2011596)

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.9-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Sep 14 2021 Sahana Prasad <sahana@redhat.com> - 3.0.9-3
- Rebuilt with OpenSSL 3.0.0

* Sat Aug 14 2021 Orion Poplawski <orion@nwra.com> - 3.0.9-2
- Rebuild for latest poppler

* Sat Aug 07 2021 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 3.0.9-1
- Update to latest patch release

* Mon Aug 02 2021 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 3.0.8-8
- Rebuild for poppler update

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.8-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sat Jul 10 2021 Björn Esser <besser82@fedoraproject.org> - 3.0.8-6
- Rebuild for versioned symbols in json-c

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 3.0.8-5
- Rebuilt for Python 3.10

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jan 11 2021 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 3.0.8-3
- Rebuild for poppler 21.01.0

* Sun Jan 10 2021 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 3.0.8-2
- Fix build for F < 33

* Sat Dec 05 2020 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 3.0.8-1
- Update to new minor release

* Wed Oct 14 2020 Jeff Law <law@redhat.com> - 3.0.7-5
- Fix missing #include for gcc-11

* Sun Sep 13 2020 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 3.0.7-4
- use cmake macros and fix build
- Enable tests

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.7-3
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 15 2020 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 3.0.7-1
- Update to 3.0.7
- drop unneeded patches.
- Rebuild for poppler 0.90.0

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 3.0.1-8
- Rebuilt for Python 3.9

* Tue Apr 21 2020 Björn Esser <besser82@fedoraproject.org> - 3.0.1-7
- Rebuild (json-c)

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Jan 20 2020 Marek Kasik <mkasik@redhat.com> - 3.0.1-5
- Rebuild for poppler-0.84.0

* Sat Nov 23 2019 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 3.0.1-4
- Fix exported variables
- https://bugzilla.redhat.com/show_bug.cgi?id=1687233

* Sat Sep 14 2019 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 3.0.1-3
- Add patch to fix build
- Temporarily disable doc building

* Sat Sep 07 2019 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 3.0.1-2
- Bump spec

* Fri Sep 06 2019 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 3.0.1-1
- Update to 3.0.1: contains soname bump
- Rebase copyright patch
- Remove unneeded patches

* Fri Sep 06 2019 Devrim Gündüz <devrim@gunduz.org> - 2.8.9-4
- Rebuild for new CharLS

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 2.8.9-3
- Rebuilt for Python 3.8

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Apr 11 2019 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 2.8.9-1
- Update to 2.8.9

* Sat Mar 09 2019 Antonio Trande <sagitterATfedoraproject.org> - 2.8.8-5
- Rebuild for dcmtk-3.6.4

* Tue Feb 26 2019 Sérgio Basto <sergio@serjux.com> - 2.8.8-4
- New fix for BTFS on unsigned-char arches, EOF is not a char is an int.

* Mon Feb 25 2019 Sérgio Basto <sergio@serjux.com> - 2.8.8-3
- Manually-specified variables were not used by the project:
  GDCM_PDF_DOCUMENTATION
- Patch for poppler breaks builds for previous releases.
- Fix BTFS on unsigned-char arches

* Mon Feb 18 2019 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 2.8.8-2
- Enable tests

* Sun Feb 17 2019 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 2.8.8-1
- Update to latest upstream release
- use autosetup
- rebase patches
- add dcmtk and sqlite deps
- add patch to use add_subdirectories
- explicitly list binaries and shared objects

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.4-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jan 25 2019 Marek Kasik <mkasik@redhat.com> - 2.8.4-12
- Rebuild for poppler-0.73.0

* Mon Sep 17 2018 Miro Hrončok <mhroncok@redhat.com> - 2.8.4-11
- Remove Python 2 subpackage (#1627322)

* Tue Aug 14 2018 Marek Kasik <mkasik@redhat.com> - 2.8.4-10
- Rebuild for poppler-0.67.0

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.4-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 2.8.4-8
- Rebuilt for Python 3.7

* Wed May 02 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.8.4-7
- Rebuild for openssl 1.1

* Fri Mar 23 2018 Marek Kasik <mkasik@redhat.com> - 2.8.4-6
- Rebuild for poppler-0.63.0

* Sat Mar 10 2018 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 2.8.4-5
- Add g++ to BR

* Tue Mar 06 2018 Björn Esser <besser82@fedoraproject.org> - 2.8.4-4
- Rebuilt for libjson-c.so.4 (json-c v0.13.1)

* Wed Feb 14 2018 David Tardon <dtardon@redhat.com> - 2.8.4-3
- rebuild for poppler 0.62.0

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Jan 09 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.8.4-1
- Update to 2.8.4

* Sun Dec 10 2017 Björn Esser <besser82@fedoraproject.org> - 2.6.5-19
- Rebuilt for libjson-c.so.3

* Wed Nov 08 2017 David Tardon <dtardon@redhat.com> - 2.6.5-18
- rebuild for poppler 0.61.0

* Fri Oct 06 2017 David Tardon <dtardon@redhat.com> - 2.6.5-17
- rebuild for poppler 0.60.1

* Fri Sep 08 2017 David Tardon <dtardon@redhat.com> - 2.6.5-16
- rebuild for poppler 0.59.0

* Sun Aug 20 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2.6.5-15
- Add Provides for the old name without %%_isa

* Sat Aug 19 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2.6.5-14
- Python 2 binary package renamed to python2-gdcm
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3

* Mon Aug 07 2017 Björn Esser <besser82@fedoraproject.org> - 2.6.5-13
- Rebuilt for AutoReq cmake-filesystem

* Thu Aug 03 2017 David Tardon <dtardon@redhat.com> - 2.6.5-12
- rebuild for poppler 0.57.0

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.5-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.5-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Jul 07 2017 Igor Gnatenko <ignatenko@redhat.com> - 2.6.5-9
- Rebuild due to bug in RPM (RHBZ #1468476)

* Tue Mar 28 2017 David Tardon <dtardon@redhat.com> - 2.6.5-8
- rebuild for poppler 0.53.0

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 2.6.5-6
- Rebuild for Python 3.6

* Fri Dec 16 2016 David Tardon <dtardon@redhat.com> - 2.6.5-5
- rebuild for poppler 0.50.0

* Thu Nov 24 2016 Orion Poplawski <orion@cora.nwra.com> - 2.6.5-4
- Rebuild for poppler 0.49.0

* Sun Nov 13 2016 Peter Robinson <pbrobinson@fedoraproject.org> 2.6.5-3
- Build against openssl 1.0

* Fri Oct 21 2016 Marek Kasik <mkasik@redhat.com> - 2.6.5-2
- Rebuild for poppler-0.48.0

* Sun Aug 28 2016 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 2.6.5-1
- Update to latest upstream release 2.6.5
- remove surplus narrowing patch

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.3-5
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Mon Jul 18 2016 Marek Kasik <mkasik@redhat.com> - 2.6.3-4
- Rebuild for poppler-0.45.0

* Tue May  3 2016 Marek Kasik <mkasik@redhat.com> - 2.6.3-3
- Rebuild for poppler-0.43.0

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Feb 01 2016 Sebastian Pölsterl <sebp@k-d-w.org> - 2.6.3-1
- Update to 2.6.3 (#1302493)

* Fri Jan 22 2016 Marek Kasik <mkasik@redhat.com> - 2.6.2-2
- Rebuild for poppler-0.40.0

* Sun Jan 03 2016 Sebastian Pölsterl <sebp@k-d-w.org> - 2.6.2-1
- Update to 2.6.2 (#1293895)
- Add libxslt and docbook-style-xsl to build requirements (http://sourceforge.net/p/gdcm/bugs/366/)

* Sun Nov 15 2015 Sebastian Pölsterl <sebp@k-d-w.org> - 2.6.1-5
- Fix paths in GDCMConfig.cmake

* Sun Nov 15 2015 Sebastian Pölsterl <sebp@k-d-w.org> - 2.6.1-4
- Build with poppler, json and libxml2 support
- Add applications subpackage as requirement to devel subpackage

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.1-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Mon Nov 02 2015 Sebastian Pölsterl <sebp@k-d-w.org> - 2.6.1-2
- Install *.cmake files to _libdir/cmake/ directory
- Move command line programs to applications sub-package

* Sat Oct 31 2015 Sebastian Pölsterl <sebp@k-d-w.org> - 2.6.1-1
- Update to 2.6.1
- Remove obsolete patch to allow inplace build
- Drop dependency on PostgreSQL and MySQL

* Sat Aug 29 2015 Sebastian Pölsterl <sebp@k-d-w.org> - 2.4.5-1
- Update to 2.4.5
- Update patch to allow inplace build
- Remove gdcm-as.patch which has been applied upstream

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Apr 20 2015 Ralf Corsépius <corsepiu@fedoraproject.org> - 2.4.4-5
- Rebuild for GCC-5.0.1 ABI changes.
- Fix broken %%changelog entries.

* Wed Feb 25 2015 Orion Poplawski <orion@cora.nwra.com> - 2.4.4-4
- Use upstream patch for python keyword conflict

* Tue Feb 24 2015 Orion Poplawski <orion@cora.nwra.com> - 2.4.4-3
- Add patch to fix FTBFS due to variable name/python keyword conflict (bug #1195879)

* Tue Feb 24 2015 Orion Poplawski <orion@cora.nwra.com> - 2.4.4-2
- Rebuild for gcc 5 C++11 ABI

* Thu Sep 25 2014 Sebastian Pölsterl <sebp@k-d-w.org> - 2.4.4-1
- Update to 2.4.4

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Mon Aug 04 2014 Sebastian Pölsterl <sebp@k-d-w.org> - 2.4.3-2
- Exclude documentation files from base package

* Mon Aug 04 2014 Sebastian Pölsterl <sebp@k-d-w.org> - 2.4.3-1
- Update to 2.4.3

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 28 2014 Kalev Lember <kalevlember@gmail.com> - 2.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Sat Apr 05 2014 Sebastian Pölsterl <sebp@k-d-w.org> - 2.4.2-1
- Update to 2.4.2

* Sun Dec 15 2013 Michael Schwendt <mschwendt@fedoraproject.org> - 2.4.1-2
- Include license file and a few doc files in base package
- Include directory /usr/share/gdcm in base package
- Remove obsolete cleaning of buildroot
- Add %%?_isa to base package deps
- Remove empty lines at beginning of %%descriptions
- Fix base package Group tag to "System Environment/Libraries"

* Wed Dec 11 2013 Sebastian Pölsterl <sebp@k-d-w.org> - 2.4.1-1
- Update to 2.4.1

* Wed Dec 11 2013 Mario Ceresa <mrceresa AT fedoraproject DOT org> - 2.4.0-4
- Fixes #1001298
- Minor fixes on the spec

* Tue Nov 19 2013 Sebastian Pölsterl <sebp@k-d-w.org> - 2.4.0-3
- More duplicate documentation files fixes
- Move examples to new subpackage

* Tue Nov 19 2013 Sebastian Pölsterl <sebp@k-d-w.org> - 2.4.0-2
- Fixed duplicate documentation files:
- https://bugzilla.redhat.com/show_bug.cgi?id=1001298

* Sun Oct 20 2013 Sebastian Pölsterl <sebp@k-d-w.org> - 2.4.0-1
- Update to 2.4.0
- Added python3-gdcm package

* Tue Aug 13 2013 Mario Ceresa <mrceresa AT fedoraproject DOT org> - 2.2.4-5
- Still getting "vtkImageData has no member named 'GetWholeExtent" with vtk-devel
- Added additional debug symbols
- Enabled testing (for now informational only)
- Enabled build of gdcmd5 because its needed by tests
- Re-added graphviz BR

* Mon Aug 05 2013 Mario Ceresa <mrceresa AT fedoraproject DOT org> - 2.2.4-4
- Fixed doc generation
- Disabled pdf generation util texlive problems are solved in Rawhide
- Fixed bogus dates

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 16 2013 Mario Ceresa <mrceresa@fedoraproject.org> - 2.2.4-2
- Add support for vtk 6.0.0

* Fri Jul 12 2013 Orion Poplawski <orion@cora.nwra.com> - 2.2.4-1
- Update to 2.2.4
- Rebuild for vtk 6.0.0

* Sun Jun 30 2013 Bruno Wolff III <bruno@wolff.to> - 2.2.3-3
- Rebuild for poppler soname bump

* Wed May 1 2013 Mario Ceresa <mrceresa@fedoraproject.org> - 2.2.3-1
- Upgrade to 2.2.3
- Drop upstreamed patches
- Added doc package
- Various fixes to spec file
- Dropped pdf documentation because cmake scripts still search for pdfopt

* Mon Feb 4 2013 Mario Ceresa <mrceresa@fedoraproject.org> - 2.0.18-8
- Added missing BR for pdflatex

* Fri Jan  25 2013 Mario Ceresa <mrceresa@fedoraproject.org> - 2.0.18-7
- Rebuild (poppler-0.22.0)

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.18-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul  2 2012 Marek Kasik <mkasik@redhat.com> - 2.0.18-5
- Rebuild (poppler-0.20.1)

* Wed May 16 2012 Marek Kasik <mkasik@redhat.com> - 2.0.18-4
- Rebuild (poppler-0.20.0)

* Thu Feb 09 2012 Rex Dieter <rdieter@fedoraproject.org> 2.0.18-3
- rebuild (openjpeg)

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.18-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Nov 01 2011 Orion Poplawski <orion@cora.nwra.com> - 2.0.18-1
- Update to 2.0.18
- Drop upstreamed patches
- Add -DGDCM_USE_SYSTEM_CHARLS=ON
- Add patch to fix charls include

* Fri Oct 28 2011 Rex Dieter <rdieter@fedoraproject.org> - 2.0.17-9
- rebuild(poppler)

* Wed Oct 19 2011 Mario Ceresa <mrceresa@fedoraproject.org> - 2.0.17-8
- Rebuild for vtk

* Fri Sep 30 2011 Marek Kasik <mkasik@redhat.com> - 2.0.17-7
- Rebuild (poppler-0.18.0)

* Mon Sep 19 2011 Marek Kasik <mkasik@redhat.com> - 2.0.17-6
- Rebuild (poppler-0.17.3)

* Mon Jul 25 2011 Rahul Sundaram <sundaram@fedoraproject.org> - 2.0.17-5
- Rebuild for cmake
- Clean up spec to match current guidelines

* Fri Jul 15 2011 Marek Kasik <mkasik@redhat.com> - 2.0.17-4
- Rebuild (poppler-0.17.0)

* Wed Apr 20 2011 Mario Ceresa <mrceresa@fedoraproject.org> - 2.0.17-3
- Bump release

* Sun Mar 27 2011 Mario Ceresa mrceresa gmailcom - 2.0.17-2
- Fixed BR mysql-libs

* Sat Mar 19 2011 Mario Ceresa mrceresa gmailcom - 2.0.17-1
- Updated to version 2.0.17

* Thu Mar 17 2011 Marek Kasik <mkasik@redhat.com> - 2.0.16-17
- Fix BuildRequires

* Sun Mar 13 2011 Marek Kasik <mkasik@redhat.com> - 2.0.16-16
- Rebuild (poppler-0.16.3)

* Sun Feb 20 2011 Orion Poplawski <orion@cora.nwra.com> - 2.0.16-15
- Rebuild for new vtk with fixed sonames

* Mon Feb 14 2011 Mario Ceresa <mrceresa@gmail.com> - 2.0.16-13
- Adapted to new version of CharLS lib (v 1.0)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.16-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Feb 02 2011 Mario Ceresa <mrceresa@gmail.com> - 2.0.16-11
- Removed python bindings because they fail to build with gcc 4.6

* Wed Feb 02 2011 Mario Ceresa <mrceresa@gmail.com> - 2.0.16-10
- Added patch to fix upstream bug #3169784

* Sun Jan 02 2011 Rex Dieter <rdieter@fedoraproject.org> - 2.0.16-11
- rebuild (poppler)

* Wed Dec 15 2010 Rex Dieter <rdieter@fedoraproject.org> - 2.0.16-8
- rebuild (poppler)

* Mon Nov 22 2010 Mario Ceresa <mrceresa@gmail.com> 2.0.16-7
- Fixed bug 655738

* Fri Nov 19 2010 Mario Ceresa <mrceresa@gmail.com> 2.0.16-6
- Enabled VTK support

* Tue Oct 19 2010 Mario Ceresa <mrceresa@gmail.com> 2.0.16-5
- Filtered out private python extension lib
- Added documentation

* Tue Oct 19 2010 Mario Ceresa <mrceresa@gmail.com> 2.0.16-4
- Changed directory ownership

* Fri Oct 15 2010 Mario Ceresa <mrceresa@gmail.com> 2.0.16-3
- Rearranged directory layout to remove version in dir names

* Sat Sep 18 2010 Mario Ceresa <mrceresa@gmail.com> 2.0.16-2
- Added ExcludeArch for ppc and ppc64 because of a bug in doxygen
see https://bugzilla.redhat.com/show_bug.cgi?id=566725#c9

* Sat Sep 18 2010 Mario Ceresa <mrceresa@gmail.com> 2.0.16-1
- Updated to release 2.0.16
- Removed patch "stack_namespace" and "poppler_breaks_api" because
already included upstream
- Added swig and texlive-pdflatex to BuildRequires
- Moved python files to a separate package

* Sun Apr 11 2010 Mario Ceresa <mrceresa@gmail.com> 2.0.14-5
- Fixed some issues pointed out by Martin Gieseking. In details:
- BR to build documentation (tex + graphviz)
- Changed man page inclusion
- Fixed changelog format
- Removed VTK support because cmake 2.8 is needed to recognize vtk 5.4!
- Fixed python support

* Thu Mar 25 2010 Mario Ceresa <mrceresa@gmail.com> 2.0.14-4
- Added VTK support
- Added python support

* Sun Mar 21 2010 Mario Ceresa <mrceresa@gmail.com> 2.0.14-3
- Added BuildRequires fontconfig-devel
- Fixed lib /lib64 issue with base CMakeLists.txt

* Mon Mar 15 2010 Mario Ceresa <mrceresa@gmail.com> 2.0.14-2
- Added BuildRequires CharLS-devel

* Wed Feb 17 2010 Mario Ceresa <mrceresa@gmail.com> 2.0.14
- Initial RPM Release


## END: Generated by rpmautospec
