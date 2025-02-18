%{?!python3_pkgversion:%global python3_pkgversion 3}
%global sover 31

Name:           openexr
Version:        3.2.4
Release:        3%{?dist}
Summary:        Provides the specification and reference implementation of the EXR file format

License:        BSD-3-Clause WITH AdditionRef-OpenEXR-Additional-IP-Rights OR Apache-2.0
URL:            https://www.openexr.com/
Source0:        https://github.com/AcademySoftwareFoundation/%{name}/archive/v%{version}/%{name}-%{version}.tar.gz
Source1:        tests.zip
# https://github.com/AcademySoftwareFoundation/openexr/pull/1507
Patch1:         march-x86-64-v3.patch
BuildRequires:  cmake gcc gcc-c++
BuildRequires:  boost-devel
BuildRequires:  imath-devel
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  zlib-devel
BuildRequires:  libdeflate-devel

Obsoletes:      OpenEXR < 2.5.3
Provides:       OpenEXR = %{version}-%{release}

%description
OpenEXR is an open-source high-dynamic-range floating-point image file format
for high-quality image processing and storage. This document presents a brief
overview of OpenEXR and explains concepts that are specific to this format.

This package containes the binaries for OpenEXR.


%package libs
Summary:        OpenEXR Libraries
Provides:       OpenEXR-libs = %{version}-%{release}
Obsoletes:      OpenEXR-libs < 2.5.3

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


%package devel
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}

Provides:       OpenEXR-devel = %{version}-%{release}
Provides:       OpenEXR-devel%{?_isa} = %{version}-%{release}
Obsoletes:      OpenEXR-devel < 2.5.3

Provides:       ilmbase-devel = %{version}-%{release}
Provides:       ilmbase-devel%{?_isa} = %{version}-%{release}
Obsoletes:      ilmbase-devel < 2.5.3

Summary:        Development files for %{name}

%description devel
%{summary}.


%prep
%autosetup -p1

%build
%cmake
unzip -o %{SOURCE1} -d redhat-linux-build/src/test/bin/
%cmake_build


%install
%cmake_install


%check
# Some tests fail on particular architectures
%ifarch aarch64
# https://github.com/AcademySoftwareFoundation/openexr/issues/1460
EXCLUDE_REGEX='DWA[AB]Compression'
%endif
%ifarch s390x
# https://github.com/AcademySoftwareFoundation/openexr/issues/1175
EXCLUDE_REGEX='ReadDeep|DWA[AB]Compression|testCompression|Rgba|SampleImages|SharedFrameBuffer'
%endif
%ctest --exclude-regex "$EXCLUDE_REGEX"


%files
%{_bindir}/exr2aces
%{_bindir}/exrenvmap
%{_bindir}/exrheader
%{_bindir}/exrinfo
%{_bindir}/exrmakepreview
%{_bindir}/exrmaketiled
%{_bindir}/exrmanifest
%{_bindir}/exrmultipart
%{_bindir}/exrmultiview
%{_bindir}/exrstdattr

%files libs
%doc CHANGES.md CONTRIBUTING.md GOVERNANCE.md SECURITY.md CODE_OF_CONDUCT.md CONTRIBUTORS.md README.md
%license LICENSE.md
%{_libdir}/libIex-3_2.so.%{sover}{,.*}
%{_libdir}/libIlmThread-3_2.so.%{sover}{,.*}
%{_libdir}/libOpenEXR-3_2.so.%{sover}{,.*}
%{_libdir}/libOpenEXRCore-3_2.so.%{sover}{,.*}
%{_libdir}/libOpenEXRUtil-3_2.so.%{sover}{,.*}

%files devel
%{_docdir}/OpenEXR/
%{_includedir}/OpenEXR/
%{_libdir}/libIex{,-3_2}.so
%{_libdir}/libIlmThread{,-3_2}.so
%{_libdir}/libOpenEXR{,-3_2}.so
%{_libdir}/libOpenEXRCore{,-3_2}.so
%{_libdir}/libOpenEXRUtil{,-3_2}.so
%{_libdir}/cmake/OpenEXR/
%{_libdir}/pkgconfig/OpenEXR.pc


%changelog
* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed May 15 2024 Josef Ridky <jridky@redhat.com> - 3.2.4-2
- fix SPDX license (https://gitlab.com/fedora/legal/fedora-license-data/-/merge_requests/570)

* Mon Apr 22 2024 Joser Ridky <jridky@redhat.com> - 3.2.4-1
- Update to 3.2.4 and fix FTBFS (#2261422)

* Wed Feb 14 2024 Josef Ridky <jridky@redhat.com> - 3.2.2-1
- Update to 3.2.2 (#2232224)

* Mon Feb 05 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 3.1.10-5
- Backport proposed fix for CVE-2023-5841 to 3.1.10 (fix RHBZ#2262406)

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.10-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Aug 04 2023 Yaakov Selkowitz <yselkowi@redhat.com> - 3.1.10-2
- Fix build for x86-64-v3
- Run all tests on i686, ppc64le, x86_64

* Fri Aug 04 2023 Richard Shaw <hobbes1069@gmail.com> - 3.1.10-1
- Update to 3.1.10.

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jul 18 2023 Josef Ridky <jridky@redhat.com> - 3.1.9-2
- Migrate to SPDX license format

* Mon Jun 26 2023 Richard Shaw <hobbes1069@gmail.com> - 3.1.9-1
- Upgrade to 3.1.9.

* Mon Jun 19 2023 Florian Weimer <fweimer@redhat.com> - 3.1.8-2
- Disable F16C intrinsics on x86-64 (#2212579)

* Wed Jun 07 2023 Richard Shaw <hobbes1069@gmail.com> - 3.1.8-1
- Update to 3.1.8.

* Tue May 16 2023 Richard Shaw <hobbes1069@gmail.com> - 3.1.7-1
- Update to 3.1.7.

* Mon Mar 20 2023 Richard Shaw <hobbes1069@gmail.com> - 3.1.6-1
- Update to 3.1.6.

* Thu Feb 23 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 3.1.5-4
- Do not use broad globs in shared directories

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue Apr 12 2022 Richard Shaw <hobbes1069@gmail.com> - 3.1.5-1
- Update to 3.1.5.

* Thu Mar 10 2022 Josef Ridky <jridky@redhat.com> - 3.1.4-1
- Update to 3.1.4

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Nov 03 2021 Richard Shaw <hobbes1069@gmail.com> - 3.1.3-1
- Update to 3.1.3.

* Wed Oct 06 2021 Richard Shaw <hobbes1069@gmail.com> - 3.1.2-1
- Update to 3.1.2.

* Wed Aug 11 2021 Richard Shaw <hobbes1069@gmail.com> - 3.1.1-1
- Update to 3.1.1.

* Thu Aug 05 2021 Richard Shaw <hobbes1069@gmail.com> - 3.0.5-3
- Remove Threads::Threads from link libraries in f35+

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jul 20 2021 Richard Shaw <hobbes1069@gmail.com> - 3.0.5-1
- Update to 3.0.5.

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 2.5.5-2
- Rebuilt for Python 3.10

* Mon Mar 15 2021 Richard Shaw <hobbes1069@gmail.com> - 2.5.5-1
- Update to 2.5.5.

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Jan 22 2021 Jonathan Wakely <jwakely@redhat.com> - 2.5.4-3
- Rebuilt for Boost 1.75

* Mon Jan 18 2021 Richard Shaw <hobbes1069@gmail.com> - 2.5.4-2
- Fix Provides/Obsoletes of OpenEXR package.

* Wed Jan 06 2021 Richard Shaw <hobbes1069@gmail.com> - 2.5.4-1
- Update to 2.5.4.

* Wed Dec  9 2020 Richard Shaw <hobbes1069@gmail.com> - 2.5.3-1
- Repackaged due to massive changes in build system and inclusion of IlmBase.
