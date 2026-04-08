# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global somajor 23

Summary: Library for reading RAW files obtained from digital photo cameras
Name: LibRaw
Version: 0.21.5
Release: 1%{?dist}
License: BSD-3-Clause and (CDDL-1.0 or LGPL-2.1-only)
URL: https://www.libraw.org
Source0: %{url}/data/%{name}-%{version}.tar.gz
Patch0: LibRaw-pkgconfig.patch

BuildRequires: gcc-c++
BuildRequires: pkgconfig(lcms2)
BuildRequires: pkgconfig(jasper)
BuildRequires: pkgconfig(libjpeg)
BuildRequires: pkgconfig(zlib)
BuildRequires: autoconf automake libtool
BuildRequires: make

Provides: bundled(dcraw) = 9.25

%description
LibRaw is a library for reading RAW files obtained from digital photo
cameras (CRW/CR2, NEF, RAF, DNG, and others).

LibRaw is based on the source codes of the dcraw utility, where part of
drawbacks have already been eliminated and part will be fixed in future.

%package devel
Summary: LibRaw development libraries
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
LibRaw development libraries.

This package contains libraries that applications can use to build
against LibRaw.

%package static
Summary: LibRaw static development libraries
Requires: %{name}-devel%{?_isa} = %{version}-%{release}

%description static
LibRaw static development libraries.

%package samples
Summary: LibRaw sample programs
Requires: %{name}%{?_isa} = %{version}-%{release}

%description samples
LibRaw sample programs

%prep
%autosetup -p1 -n %{name}-%{version}

%build
autoreconf -if
%configure \
    --enable-examples=yes \
    --enable-jasper \
    --enable-jpeg \
    --enable-lcms \
    --enable-openmp \
    --enable-zlib

# https://fedoraproject.org/wiki/Packaging:Guidelines#Beware_of_Rpath
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

%make_build

%install
cp -pr doc manual
chmod 644 LICENSE.CDDL LICENSE.LGPL COPYRIGHT Changelog.txt
chmod 644 manual/*.html

# The Libraries
%make_install

rm -rfv samples/.deps
rm -fv samples/.dirstamp
rm -fv samples/*.o

rm -fv %{buildroot}%{_libdir}/lib*.la

%files
%doc Changelog.txt
%license LICENSE.CDDL LICENSE.LGPL COPYRIGHT
%{_libdir}/libraw.so.%{somajor}{,.*}
%{_libdir}/libraw_r.so.%{somajor}{,.*}

%files static
%{_libdir}/libraw.a
%{_libdir}/libraw_r.a

%files devel
%doc manual
%doc samples
%{_includedir}/libraw/
%{_libdir}/libraw.so
%{_libdir}/libraw_r.so
%{_libdir}/pkgconfig/libraw.pc
%{_libdir}/pkgconfig/libraw_r.pc
%exclude %{_docdir}/libraw/*

%files samples
%{_bindir}/*


%changelog
* Fri Jan 02 2026 Gwyn Ciesla <gwync@protonmail.com> - 0.21.5-1
- 0.21.5

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.21.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Apr 14 2025 Gwyn Ciesla <gwync@protonmail.com> - 0.21.4-1
- 0.21.4

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.21.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Sep 20 2024 Gwyn Ciesla <gwync@protonmail.com> - 0.21.3-1
- 0.21.3

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.21.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.21.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.21.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jan 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.21.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Jan 09 2024 Gwyn Ciesla <gwync@protonmail.com> - 0.21.2-2
- CR3-Qstep table: avoid wrong 64-bit code generation patch

* Thu Dec 21 2023 Gwyn Ciesla <gwync@protonmail.com> - 0.21.2-1
- 0.21.2, enable zlib support.

* Tue Nov 28 2023 Orion Poplawski <orion@nwra.com> - 0.21.1-7
- Rebuild for jasper 4.1

* Tue Oct 10 2023 Neal Gompa <ngompa@fedoraproject.org> - 0.21.1-6
- Clean and simplify spec and drop EL7 stuff
- Use official released tarball

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.21.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon May 08 2023 Gwyn Ciesla <gwync@protonmail.com> - 0.21.1-4
- Patch for CVE-2023-1729

* Mon Mar 13 2023 Gwyn Ciesla <gwync@protonmail.com> - 0.21.1-3
- migrate to SPDX license

* Wed Jan 18 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.21.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jan 05 2023 Gwyn Ciesla <gwync@protonmail.com> - 0.21.1-1
- 0.21.1

* Mon Dec 19 2022 Gwyn Ciesla <gwync@protonmail.com> - 0.21.0-1
- 0.21.0

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.20.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sun Feb 13 2022 Josef Ridky <jridky@redhat.com> - 0.20.2-6
- Rebuilt for libjasper.so.6

* Wed Jan 19 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.20.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Dec 13 2021 Debarshi Ray <rishi@fedoraproject.org> - 0.20.2-4
- CDDL is not an approved license, but CDDL-1.0 is

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.20.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Jan 25 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.20.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Oct 15 2020 Gwyn Ciesla <gwync@protonmail.com> - 0.20.2-1
- 0.20.2

* Wed Oct 14 2020 Gwyn Ciesla <gwync@protonmail.com> - 0.20.1-1
- 0.20.1

* Thu Sep 24 2020 Gwyn Ciesla <gwync@protonmail.com> - 0.20.0-3
- Patch for CVE-2020-24890.

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.20.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jul 23 2020 Gwyn Ciesla <gwync@protonmail.com> - 0.20.0-1
- 0.20.0 final.

* Thu Jul 02 2020 Gwyn Ciesla <gwync@protonmail.com> - 0.20-0.rc1.3
- RC1

* Mon Jun 29 2020 Gwyn Ciesla <gwync@protonmail.com>- 0.20-0.beta1.2
- Patch for CVE-2020-15365

* Wed May 13 2020 Kalev Lember <klember@redhat.com> - 0.20-0.beta1.1
- Add back pkgconfig patch lost in the previous commit

* Thu May 07 2020 Gwyn Ciesla <gwync@protonmail.com> - 0.20-0.beta1
- 0.20 Beta 1

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.19.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Aug 20 2019 Gwyn Ciesla <gwync@protonmail.com> - 0.19.5-1
- 0.19.5

* Mon Aug 05 2019 Gwyn Ciesla <gwync@protonmail.com> - 0.19.4-1
- 0.19.4

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.19.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Jul 03 2019 Gwyn Ciesla <gwync@protonmail.com> - 0.19.3-1
- 0.19.3

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.19.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Jan 02 2019 Debarshi Ray <rishi@fedoraproject.org> - 0.19.2-2
- Remove the samples subpackage from RHEL 7

* Wed Dec 26 2018 Gwyn Ciesla <limburgher@gmail.com> - 0.19.2-1
- 0.19.2

* Thu Nov 22 2018 Debarshi Ray <rishi@fedoraproject.org> - 0.19.1-1
- 0.19.1

* Mon Oct 08 2018 Debarshi Ray <rishi@fedoraproject.org> - 0.19.0-6
- Remove the build artifacts for the samples

* Mon Oct 08 2018 Debarshi Ray <rishi@fedoraproject.org> - 0.19.0-5
- Bind the samples sub-package more tightly to the main package

* Tue Jul 31 2018 Debarshi Ray <rishi@fedoraproject.org> - 0.19.0-4
- Fix License
- Explicitly enable JPEG and OpenMP support to avoid surprises

* Thu Jul 19 2018 Rex Dieter <rdieter@fedoraproject.org> - 0.19.0-3
- tighten %%files, mostly so api/soname changes will no longer be a surpise
- use %%make_build %%ldconfig_scriptlets

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.19.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jun 29 2018 Gwyn Ciesla <limburgher@gmail.com> - 0.19.0-1
- 0.19.0.

* Mon Jun 11 2018 Gwyn Ciesla <limburgher@gmail.com> - 0.18.12-1
- 0.18.12.

* Thu May 10 2018 Gwyn Ciesla <limburgher@gmail.com> - 0.18.11-1
- 0.18.11.

* Thu May 03 2018 Gwyn Ciesla <limburgher@gmail.com> - 0.18.10-1
- 0.18.10.

* Wed Apr 25 2018 Gwyn Ciesla <limburgher@gmail.com> - 0.18.9-1
- 0.18.9.

* Sat Feb 24 2018 Gwyn Ciesla <limburgher@gmail.com> - 0.18.8-1
- 0.18.8.

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.18.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Feb 02 2018 Gwyn Ciesla <limburgher@gmail.com> - 0.18.7-2
- Patch for updated glibc.

* Fri Jan 19 2018 Gwyn Ciesla <limburgher@gmail.com> - 0.18.7-1
- 0.18.7
- Patch for ambiguous function call.

* Wed Dec 06 2017 Gwyn Ciesla <limburgher@gmail.com> - 0.18.6-1
- 0.18.6

* Fri Sep 22 2017 Gwyn Ciesla <limburgher@gmail.com> - 0.18.5-1
- 0.18.5

* Fri Sep 15 2017 Gwyn Ciesla <limburgher@gmail.com> - 0.18.4-2
- Patch for CVE-2017-14348.

* Tue Sep 12 2017 Gwyn Ciesla <limburgher@gmail.com> - 0.18.4-1
- 0.18.4

* Mon Sep 11 2017 Gwyn Ciesla <limburgher@gmail.com> - 0.18.3-1
- 0.18.3

* Wed Sep 06 2017 Gwyn Ciesla <limburgher@gmail.com> - 0.18.2-5
- Patch for CVE-2017-13735.

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.18.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.18.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Apr 14 2017 Rex Dieter <rdieter@fedoraproject.org> - 0.18.2-2
- fix rpath, tighten subpkg dependencies, use %%license

* Thu Mar 09 2017 Jon Ciesla <limburgher@gmail.com> - 0.18.2-1
- 0.18.2.

* Mon Feb 13 2017 Jon Ciesla <limburgher@gmail.com> - 0.18.1-1
- 0.18.1.

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.18.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Dec 27 2016 Jon Ciesla <limburgher@gmail.com> - 0.18.0-1
- 0.18.0.

* Thu Dec  1 2016 Tom Callaway <spot@fedoraproject.org> - 0.17.2-2
- rebuild for deps

* Sun May 15 2016 Jon Ciesla <limburgher@gmail.com> - 0.17.2-1
- 0.17.2.

* Mon Feb 22 2016 Jon Ciesla <limburgher@gmail.com> - 0.17.1-4
- Patch to fix FTBFS, BZ 1307280.

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.17.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Dec 01 2015 Jon Ciesla <limburgher@gmail.com> - 0.17.1-2
- Patch for CVE-2015-8366 and CVE-2015-8367, BZ 1287057.

* Sun Nov 29 2015 Jon Ciesla <limburgher@gmail.com> - 0.17.1-1
- 0.17.1.

* Mon Aug 17 2015 Jon Ciesla <limburgher@gmail.com> - 0.17.0-1
- 0.17.0.

* Tue Jun 16 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.16.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 16 2015 Jon Ciesla <limburgher@gmail.com> - 0.16.2-1
- 0.16.2, BZ 1222258.

* Thu May 14 2015 Jon Ciesla <limburgher@gmail.com> - 0.16.1-7
- Add provides for bundled dcraw, https://fedorahosted.org/fpc/ticket/530
- Fix EVR in changelog.

* Mon May 11 2015 Jon Ciesla <limburgher@gmail.com> - 0.16.1-6
- 0.16.1, BZ 1220382.

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 0.16.0-5
- Rebuilt for GCC 5 C++11 ABI change

* Fri Aug 15 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.16.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Jun 06 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.16.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Feb 20 2014 Jon Ciesla <limburgher@gmail.com> - 0.16.0-2
- Fix pkg-config flags, BZ 837248.

* Tue Jan 21 2014 Jon Ciesla <limburgher@gmail.com> - 0.16.0-1
- 0.16.0, BZ 1055281.

* Fri Aug 30 2013 Jon Ciesla <limburgher@gmail.com> - 0.15.4-1
- 0.15.4, CVE-2013-1439, BZ 1002717.

* Wed Aug 07 2013 Jon Ciesla <limburgher@gmail.com> - 0.15.3-3
- Enable samples, BZ 991514,

* Fri Aug 02 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.15.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 09 2013 Jon Ciesla <limburgher@gmail.com> - 0.15.3-1
- 0.15.3.

* Wed May 29 2013 Jon Ciesla <limburgher@gmail.com> - 0.15.2-1
- Latest upstream, two security fixes.

* Wed May 29 2013 Jon Ciesla <limburgher@gmail.com> - 0.14.8-2
- Patch for double free, CVE-2013-2126, BZ 968387.

* Wed May 29 2013 Jon Ciesla <limburgher@gmail.com> - 0.14.8-1
- Latest upstream, fixes gcc 4.8 issues.

* Thu Apr 11 2013 Jon Ciesla <limburgher@gmail.com> - 0.14.7-4
- Revert prior patch.

* Thu Apr 11 2013 Jon Ciesla <limburgher@gmail.com> - 0.14.7-3
- Patch for segfault, BZ 948628.

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.14.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Nov 26 2012 Jon Ciesla <limburgher@gmail.com> - 0.14.7-1
- New upstream 0.14.7

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.14.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jun  2 2012 Siddhesh Poyarekar <siddhesh.poyarekar@gmail.com> - 0.14.6-2
- Use lcms2.

* Sat Jun  2 2012 Siddhesh Poyarekar <siddhesh.poyarekar@gmail.com> - 0.14.6-1
- New upstream 0.14.6

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.14.3-4
- Rebuilt for c++ ABI breakage

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.14.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Dec  9 2011 Siddhesh Poyarekar <siddhesh.poyarekar@gmail.com> - 0.14.3-2
- Add demosaic packs (bz #760638)
- Change license to GPLv3+ due to above change

* Wed Nov 16 2011 Siddhesh Poyarekar <siddhesh.poyarekar@gmail.com> - 0.14.3-1
- Rebase to upstream 0.14.3

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Dec 12 2010 Siddhesh Poyarekar <siddhesh.poyarekar@gmail.com> 0.11.3-2
- Of course, you need to upload the new sources.

* Sun Dec 12 2010 Siddhesh Poyarekar <siddhesh.poyarekar@gmail.com> 0.11.3-1
- upstream 0.11.3

* Sat Nov 13 2010 Siddhesh Poyarekar <siddhesh.poyarekar@gmail.com> 0.9.1-9
- Build position independent object code

* Thu Jul 08 2010 Siddhesh Poyarekar <siddhesh.poyarekar@gmail.com> 0.9.1-8
- Remove LibRaw license since we're not distributing LibRaw under its terms

* Wed Jul 07 2010 Siddhesh Poyarekar <siddhesh.poyarekar@gmail.com> 0.9.1-7
- Buildroot is unnecessary
- Corrected license to LGPLv2 or CDDL

* Sun Jul 04 2010 Siddhesh Poyarekar <siddhesh.poyarekar@gmail.com> 0.9.1-6
- Do not impose -O4 and -w in build options
- Change package group to Development/Libraries
- Corrected license to LGPLv2
- setup macro no longer needs the name and version arguments
- Rename patches to include name and version

* Wed Jun 30 2010 Siddhesh Poyarekar <siddhesh.poyarekar@gmail.com> 0.9.1-5
- Use optflags for build
- Install the documentation in a cleaner way

* Tue Jun 29 2010 Siddhesh Poyarekar <siddhesh.poyarekar@gmail.com> 0.9.1-4
- Use upstream package name (libRaw) instead of libraw

* Tue Jun 29 2010 Siddhesh Poyarekar <siddhesh.poyarekar@gmail.com> 0.9.1-3
- Remove the clean section since it is not needed in F-13 and later
- Correct installation of docs into defaultdocdir instead of docdir

* Thu Jun 10 2010 Siddhesh Poyarekar <siddhesh.poyarekar@gmail.com> 0.9.1-2
- Disable lcms and openmp support by default so that we're in line with
  upstream default

* Fri Jun 04 2010 Siddhesh Poyarekar <siddhesh.poyarekar@gmail.com> 0.9.1-1
- New package

