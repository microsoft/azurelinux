# Build for azurelinux with gnuplot and without mingw support
%bcond_without gnuplot
%bcond_with mingw
 
Name:          leptonica
Version:       1.85.0
Release:       1%{?dist}
Summary:       C library for efficient image processing and image analysis operations
Vendor:        Microsoft Corporation
Distribution:  Azure Linux 
License:       Leptonica
URL:           https://github.com/danbloomberg/leptonica
Source0:       https://github.com/DanBloomberg/leptonica/archive/%{version}/%{name}-%{version}.tar.gz
# Use CMAKE_INSTALL_LIBDIR
# Fix library name on win32
# Don't add _<CONFIG> suffix to pkgconfig filename
Patch0:        leptonica_cmake.patch
BuildRequires: cmake
BuildRequires: gcc-c++
BuildRequires: giflib-devel
BuildRequires: libjpeg-devel
BuildRequires: libpng-devel
BuildRequires: libtiff-devel
BuildRequires: libtool
BuildRequires: libwebp-devel
BuildRequires: make
BuildRequires: zlib-devel
 
# Needed for several tests
%if %{with gnuplot}
BuildRequires: gnuplot
%endif
 
%if %{with mingw}
BuildRequires: mingw32-filesystem >= 95
BuildRequires: mingw32-gcc-c++
BuildRequires: mingw32-libjpeg-turbo
BuildRequires: mingw32-libtiff
BuildRequires: mingw32-libpng
BuildRequires: mingw32-zlib
BuildRequires: mingw32-giflib
BuildRequires: mingw32-libwebp
 
BuildRequires: mingw64-filesystem >= 95
BuildRequires: mingw64-gcc-c++
BuildRequires: mingw64-libjpeg-turbo
BuildRequires: mingw64-libtiff
BuildRequires: mingw64-libpng
BuildRequires: mingw64-zlib
BuildRequires: mingw64-giflib
BuildRequires: mingw64-libwebp
%endif
 
 
%description
The library supports many operations that are useful on
 * Document images
 * Natural images
 
Fundamental image processing and image analysis operations
 * Rasterop (aka bitblt)
 * Affine transforms (scaling, translation, rotation, shear)
   on images of arbitrary pixel depth
 * Projective and bi-linear transforms
 * Binary and gray scale morphology, rank order filters, and
   convolution
 * Seed-fill and connected components
 * Image transformations with changes in pixel depth, both at
   the same scale and with scale change
 * Pixelwise masking, blending, enhancement, arithmetic ops,
   etc.
 
 
%package devel
Summary:       Development files for %{name}
Requires:      %{name}%{?_isa} = %{version}-%{release}
 
%description devel
The %{name}-devel package contains header files for
developing applications that use %{name}.
 
 
%package tools
Summary:       Leptonica utility tools
Requires:      %{name}%{?_isa} = %{version}-%{release}
 
%description tools
The %{name}-tools package contains leptonica utility tools.
 
 
%if %{with mingw}
%package -n mingw32-%{name}
Summary:       MinGW Windows Leptonica library
Obsoletes:     mingw32-%{name}-static
BuildArch:     noarch
 
%description -n mingw32-%{name}
MinGW Windows Leptonica library.
 
 
%package -n mingw64-%{name}
Summary:       MinGW Windows Leptonica library
Obsoletes:     mingw64-%{name}-static
BuildArch:     noarch
 
%description -n mingw64-%{name}
MinGW Windows Leptonica library.
%endif
 
 
%{?mingw_debug_package}
 
 
%prep
%autosetup -p1
 
 
%build
mkdir build
cd build
# Native build
%cmake .. -DBUILD_PROG=ON
%cmake_build
%if %{with mingw}
# MinGW build
%mingw_cmake -DBUILD_PROG=ON -DSW_BUILD=OFF
%mingw_make_build
%endif
 
 
%install
cd build
%cmake_install
%if %{with mingw}
%mingw_make_install
%endif
 
# Compat symlinks
ln -s %{_libdir}/libleptonica.so %{buildroot}%{_libdir}/liblept.so
%if %{with mingw}
ln -s %{mingw32_libdir}/libleptonica.dll.a %{buildroot}%{mingw32_libdir}/liblept.dll.a
ln -s %{mingw64_libdir}/libleptonica.dll.a %{buildroot}%{mingw64_libdir}/liblept.dll.a
%endif
 
 
%{?mingw_debug_install_post}
 
 
%check
%ctest
 
%files
%license leptonica-license.txt
%doc README.html version-notes.html
%{_libdir}/libleptonica.so.6*
 
%files devel
%{_includedir}/%{name}
%{_libdir}/liblept.so
%{_libdir}/libleptonica.so
%{_libdir}/pkgconfig/lept.pc
%{_libdir}/cmake/leptonica/
 
%files tools
%{_bindir}/*
 
%if %{with mingw}
%files -n mingw32-%{name}
%license leptonica-license.txt
%{mingw32_bindir}/*.exe
%{mingw32_bindir}/libleptonica-6.dll
%{mingw32_includedir}/leptonica/
%{mingw32_libdir}/liblept.dll.a
%{mingw32_libdir}/libleptonica.dll.a
%{mingw32_libdir}/pkgconfig/lept.pc
%{mingw32_libdir}/cmake/leptonica/
 
 
%files -n mingw64-%{name}
%license leptonica-license.txt
%{mingw64_bindir}/*.exe
%{mingw64_bindir}/libleptonica-6.dll
%{mingw64_includedir}/leptonica/
%{mingw64_libdir}/liblept.dll.a
%{mingw64_libdir}/libleptonica.dll.a
%{mingw64_libdir}/pkgconfig/lept.pc
%{mingw64_libdir}/cmake/leptonica/
%endif
 
 
%changelog
* Tue Nov 11 2025 Sandeep Karambelkar <skarambelkar@microsoft.com> - 1.85.0-1
- Initial Azure Linux import from Fedora 42 (license: MIT).
- Modified for building in azurelinux
- License verified

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.85.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild
 
* Fri Oct 18 2024 Sandro Mani <manisandro@gmail.com> - 1.85.0-1
- Update to 1.85.0
 
* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.84.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild
 
* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.84.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild
 
* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.84.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild
 
* Fri Jan 05 2024 Sandro Mani <manisandro@gmail.com> - 1.84.1-1
- Update to 1.84.1
 
* Wed Dec 27 2023 Michael J Gruber <mjg@fedoraproject.org> - 1.84.0-2
- Fix pkgconfig file regression (rhbz#2255937)
 
* Sun Dec 24 2023 Sandro Mani <manisandro@gmail.com> - 1.84.0-1
- Update to 1.84.0
 
* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.83.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild
 
* Sat Jan 28 2023 Sandro Mani <manisandro@gmail.com> - 1.83.1-1
- Update to 1.83.1
 
* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.83.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild
 
* Wed Dec 21 2022 Sandro Mani <manisandro@gmail.com> - 1.83.0-1
- Update to 1.83.0
 
* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.82.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild
 
* Fri Mar 25 2022 Sandro Mani <manisandro@gmail.com> - 1.82.0-7
- Rebuild with mingw-gcc-12
 
* Thu Feb 24 2022 Sandro Mani <manisandro@gmail.com> - 1.82.0-6
- Fix broken pkg-config file
 
* Thu Feb 24 2022 Sandro Mani <manisandro@gmail.com> - 1.82.0-5
- Make mingw subpackages noarch
 
* Thu Feb 24 2022 Sandro Mani <manisandro@gmail.com> - 1.82.0-4
- Make mingw subpackages noarch
 
* Sat Feb 19 2022 Sandro Mani <manisandro@gmail.com> - 1.82.0-3
- Add mingw subpackage
- Port to cmake
 
* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.82.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild
 
* Thu Sep 23 2021 Sandro Mani <manisandro@gmail.com> - 1.82.0-1
- Update to 1.82.0
 
* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.81.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild
 
* Mon Jun 21 2021 Sandro Mani <manisandro@gmail.com> - 1.81.1-1
- Update to 1.81.1
 
* Mon Jun 07 2021 Sandro Mani <manisandro@gmail.com> - 1.81.0-1
- Update to 1.81.0
 
* Tue Feb  9 2021 Pavel Cahyna <pcahyna@redhat.com> - 1.80.0-3
- Make gnuplot build dependency optional, used only by tests
 
* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.80.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild
 
* Thu Jul 30 2020 Sandro Mani <manisandro@gmail.com> - 1.80.0-1
- Update to 1.80.0
 
* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.79.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild
 
* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.79.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild
 
* Fri Jan 03 2020 Sandro Mani <manisandro@gmail.com> - 1.79.0-1
- Update to 1.79.0
 
* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.78.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild
 
* Wed Mar 27 2019 Sandro Mani <manisandro@gmail.com> - 1.78.0-1
- Update to 1.78.0
 
* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.77.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild
 
* Wed Dec 19 2018 Sandro Mani <manisandro@gmail.com> - 1.77.0-1
- Update to 1.77.0
 
* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.76.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild
 
* Thu May 03 2018 Sandro Mani <manisandro@gmail.com> - 1.76.0-1
- Update to 1.76.0
 
* Tue Feb 27 2018 Sandro Mani <manisandro@gmail.com> - 1.75.3-2
- Make test-failures on big-endian fatal again
 
* Thu Feb 22 2018 Sandro Mani <manisandro@gmail.com> - 1.75.3-1
- Update to 1.75.3
 
* Sun Feb 11 2018 Sandro Mani <manisandro@gmail.com> - 1.75.2-1
- Update to 1.75.2
 
* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.74.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild
 
* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.74.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild
 
* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.74.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild
 
* Sun Jun 11 2017 Sandro Mani <manisandro@gmail.com> - 1.74.4-1
- Update to 1.74.4
 
* Sun Jun 11 2017 Sandro Mani <manisandro@gmail.com> - 1.74.3-1
- Update to 1.74.3
 
* Sat Jun 03 2017 Sandro Mani <manisandro@gmail.com> - 1.74.2-2
- Backport 069bbc0897e8b939e93db8730b3f10b18e9d0885
 
* Sat Jun 03 2017 Sandro Mani <manisandro@gmail.com> - 1.74.2-1
- Update to 1.74.2
 
* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.74.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild
 
* Wed Feb 01 2017 Sandro Mani <manisandro@gmail.com> - 1.74.1-2
- Rebuild (libwebp)
 
* Tue Jan 03 2017 Sandro Mani <manisandro@gmail.com> - 1.74.1-1
- Update to 1.74.1
 
* Sun Dec 25 2016 Sandro Mani <manisandro@gmail.com> - 1.74.0-1
- Update to 1.74.0
- Add tools subpackage
- Enable tests
 
* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.73-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild
 
* Tue Jan 26 2016 Sandro Mani <manisandro@gmail.com> - 1.73-1
- Update to 1.73
 
* Mon Dec 28 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 1.72-3
- Rebuilt for libwebp soname bump
 
* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.72-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild
 
* Mon Apr 27 2015 Sandro Mani <manisandro@gmail.com> - 1.72-1
- Update to 1.72
 
* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.71-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild
 
* Tue Aug 05 2014 Sandro Mani <manisandro@gmail.com> - 1.71-1
- Update to 1.71
 
* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.69-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild
 
* Fri Jan 03 2014 Kalev Lember <kalevlember@gmail.com> - 1.69-11
- Rebuilt for libwebp soname bump
 
* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.69-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild
 
* Fri Mar 08 2013 Ding-Yi Chen <dchen at redhat.com> - 1.69-9
- Fixed Bug 904805 - [PATCH] Provide pkg-config file
 
 
* Fri Mar 08 2013 Ding-Yi Chen <dchen at redhat.com> - 1.69-8
- Rebuild to resolves #914124
 
* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.69-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild
 
* Thu Jan 24 2013 Ding-Yi Chen <dchen at redhat.com> - 1.69-6
- Rebuild for dependency libwebp-0.2.1-1
 
* Fri Jan 18 2013 Adam Tkac <atkac redhat com> - 1.69-5
- rebuild due to "jpeg8-ABI" feature drop
 
* Fri Dec 28 2012 Richard W.M. Jones <rjones@redhat.com> - 1.69-4
- Rebuild, see
  http://lists.fedoraproject.org/pipermail/devel/2012-December/175685.html
 
* Fri Dec 21 2012 Adam Tkac <atkac redhat com> - 1.69-3
- rebuild against new libjpeg
 
* Thu Aug 02 2012 Ding-Yi Chen <dchen at redhat.com> - 1.69-2
- Fixed issues addressed in Review Request comment #8.
 
* Wed Jul 25 2012 Ding-Yi Chen <dchen at redhat.com> - 1.69-1
- Upstream update to 1.69
- Add program-prefix in configure.
 
* Wed Jun 20 2012 Ding-Yi Chen <dchen at redhat.com> - 1.68-4
- Remove util package and its binary files.
 
* Mon Jun 11 2012 Ding-Yi Chen <dchen at redhat.com> - 1.68-3
- Split the binary into util package
 
* Wed May 09 2012 Ding-Yi Chen <dchen at redhat.com> - 1.68-2
- Add zlib.h to fix the koji build
 
* Wed May 09 2012 Ding-Yi Chen <dchen at redhat.com> - 1.68-1
- Initial import.
