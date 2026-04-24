# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global sover 25
%global imfsover 26
%global srcname openexr
%global pkgname %{srcname}2

Name:           %{pkgname}
Version:        2.5.8
Release: 12%{?dist}
Summary:        Provides the specification and reference implementation of the EXR file format

License:        BSD-3-Clause
URL:            https://www.openexr.com/
Source0:        https://github.com/AcademySoftwareFoundation/%{srcname}/archive/v%{version}/%{srcname}-%{version}.tar.gz
# Backport updated binary files for the tests.
Source1:        https://github.com/AcademySoftwareFoundation/%{srcname}/raw/v3.1.11/src/test/OpenEXRTest/v1.7.test.interleaved.exr
Source2:        https://github.com/AcademySoftwareFoundation/%{srcname}/raw/v3.1.11/src/test/OpenEXRTest/v1.7.test.planar.exr
Source3:        https://github.com/AcademySoftwareFoundation/%{srcname}/raw/v3.1.11/src/test/OpenEXRTest/v1.7.test.tiled.exr

Patch0:         openexr-gcc11.patch
Patch1:         openexr2-cstdint.patch
# Backport of commit 25a11d9a34fcf3c70f7f32680bdbe910a84d85d5 to v2.5.8.
# The binary files got removed from the patch as they are not supported by the
# patch command.
Patch2:         0001-use-NO_COMPRESSION-in-OpenEXTest-testBackwardCompati.patch

BuildRequires:  cmake
BuildRequires:  gcc gcc-c++
BuildRequires:  boost-devel
BuildRequires:  zlib-devel

%description
OpenEXR is an open-source high-dynamic-range floating-point image file format
for high-quality image processing and storage. This document presents a brief
overview of OpenEXR and explains concepts that are specific to this format.

NOTE: This is a compatibility package for projects that don't yet support
OpenEXR 3.0.


%package libs
Summary:        OpenEXR Libraries

%description libs
OpenEXR is an open-source high-dynamic-range floating-point image file format
for high-quality image processing and storage. This document presents a brief
overview of OpenEXR and explains concepts that are specific to this format.

OpenEXR Features:

* High dynamic range and color precision.  Support for 16-bit floating-point,
* 32-bit floating-point, and 32-bit integer pixels.
* Multiple image compression algorithms, both lossless and lossy. Some of
  the included codecs can achieve 2:1 lossless compression ratios on images
  with film grain.  The lossy codecs have been tuned for visual quality and
  decoding performance.
* Extensibility. New compression codecs and image types can easily be added
  by extending the C++ classes included in the OpenEXR software distribution.
  New image attributes (strings, vectors, integers, etc.) can be added to
  OpenEXR image headers without affecting backward compatibility with existing
  OpenEXR applications.
* Support for stereoscopic image workflows and a generalization
  to multi-views.
* Flexible support for deep data: pixels can store a variable-length list
  of samples and, thus, it is possible to store multiple values at different
  depths for each pixel. Hard surfaces and volumetric data representations are
  accommodated.
* Multipart: ability to encode separate, but related, images in one file.
  This allows for access to individual parts without the need to read other
  parts in the file.
* Versioning: OpenEXR source allows for user configurable C++
  namespaces to provide protection when using multiple versions of the library
  in the same process space.

The IlmBase Library:

Also a part of OpenEXR, the IlmBase library is a basic, light-weight, and
efficient representation of 2D and 3D vectors and matrices and other simple but
useful mathematical objects, functions, and data types common in computer
graphics applications, including the “half” 16-bit floating-point type.

NOTE: This is a compatibility package for projects that don't yet support
OpenEXR 3.0.


%package devel
Conflicts:      openexr-devel
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}

Summary:        Development files for %{name}

%description devel
%{summary}.


%prep
%autosetup -p1 -n %{srcname}-%{version}
mv %{SOURCE1} %{SOURCE2} %{SOURCE3} OpenEXR/IlmImfTest/


%build
%cmake -DPYILMBASE_ENABLE=OFF \
       -DOPENEXR_BUILD_UTILS=OFF 
%cmake_build


%install
%cmake_install

# Remove extraneous documentation since this is a compat package.
rm -rf %{buildroot}%{_docdir}/OpenEXR/


%check
# Test 4 currently fails on aarch64 and sometimes times out on armv7hl
# https://github.com/AcademySoftwareFoundation/openexr/issues/876
%ifnarch armv7hl aarch64 s390x i686 ppc64le riscv64
%ctest
%endif


%files libs
%doc CHANGES.md CONTRIBUTING.md GOVERNANCE.md SECURITY.md CODE_OF_CONDUCT.md CONTRIBUTORS.md README.md
%license LICENSE.md
%{_libdir}/libHalf-2_5.so.%{sover}{,.*}
%{_libdir}/libIex-2_5.so.%{sover}{,.*}
%{_libdir}/libIexMath-2_5.so.%{sover}{,.*}
%{_libdir}/libIlmImf-2_5.so.%{imfsover}{,.*}
%{_libdir}/libIlmImfUtil-2_5.so.%{imfsover}{,.*}
%{_libdir}/libIlmThread-2_5.so.%{sover}{,.*}
%{_libdir}/libImath-2_5.so.%{sover}{,.*}


%files devel
%{_includedir}/OpenEXR/
%{_libdir}/libHalf{,-2_5}.so
%{_libdir}/libIex{,-2_5}.so
%{_libdir}/libIexMath{,-2_5}.so
%{_libdir}/libIlmImf{,-2_5}.so
%{_libdir}/libIlmImfUtil{,-2_5}.so
%{_libdir}/libIlmThread{,-2_5}.so
%{_libdir}/libImath{,-2_5}.so
%{_libdir}/cmake/IlmBase/
%{_libdir}/pkgconfig/IlmBase.pc
%{_libdir}/cmake/OpenEXR/
%{_libdir}/pkgconfig/OpenEXR.pc


%changelog
* Thu Dec 04 2025 Marcin Juszkiewicz <mjuszkiewicz@redhat.com> - 2.5.8-11
- disable tests on riscv64

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.8-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.8-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.8-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.8-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.8-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Dec 15 2023 Tulio Magno Quites Machado Filho <tuliom@redhat.com> - 2.5.8-5
- Fix test with zlib-ng-compat

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Mar 08 2023 Gwyn Ciesla <gwync@protonmail.com> - 2.5.8-3
- migrated to SPDX license

* Thu Feb 23 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 2.5.8-2
- Be more explicit about which libraries are packaged (and with which .so
  versions)

* Wed Feb 22 2023 Gwyn Ciesla <gwync@protonmail.com> - 2.5.8-1
- 2.5.8

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue Mar 08 2022 Gwyn Ciesla <gwync@protonmail.com> - 2.5.7-1
- 2.5.7

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jul 07 2021 Richard Shaw <hobbes1069@gmail.com> - 2.5.5-3
- Undo rename of cmake and pkgconfig files and use version requirements instead.

* Wed Jul 07 2021 Richard Shaw <hobbes1069@gmail.com> - 2.5.5-2
- Rename pkgconfig and cmake files to not conflict.

* Sun Jul 04 2021 Richard Shaw <hobbes1069@gmail.com> - 2.5.5-1
- Initial packaging of compat package.
