# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%{?mingw_package_header}

%global pkgname poppler

Name:          mingw-%{pkgname}
Version:       25.07.0
Release: 3%{?dist}
Summary:       MinGW Windows Poppler library

License:       (GPL-2.0-only OR GPL-3.0-only) AND GPL-2.0-or-later AND LGPL-2.0-or-later AND MIT
BuildArch:     noarch
URL:           http://poppler.freedesktop.org/
Source0:       http://poppler.freedesktop.org/%{pkgname}-%{version}.tar.xz

# Downstream fix for CVE-2017-9083 (#1453200)
Patch1:        poppler_CVE-2017-9083.patch
# Backport patch for CVE-2025-52885
Patch2:        https://gitlab.freedesktop.org/poppler/poppler/-/commit/4ce27cc826bf90cc8dbbd8a8c87bd913cccd7ec0.patch

BuildRequires: make
BuildRequires: cmake
BuildRequires: gettext-devel
BuildRequires: perl(File::Temp)

BuildRequires: mingw32-filesystem >= 95
BuildRequires: mingw32-boost
BuildRequires: mingw32-gcc-c++
BuildRequires: mingw32-libjpeg-turbo
BuildRequires: mingw32-libtiff
BuildRequires: mingw32-openjpeg2
BuildRequires: mingw32-openjpeg2-tools
BuildRequires: mingw32-cairo
BuildRequires: mingw32-gtk3
BuildRequires: mingw32-lcms2
BuildRequires: mingw32-qt5-qtbase-devel
BuildRequires: mingw32-qt6-qtbase
BuildRequires: mingw32-curl

BuildRequires: mingw64-filesystem >= 95
BuildRequires: mingw64-boost
BuildRequires: mingw64-gcc-c++
BuildRequires: mingw64-libjpeg-turbo
BuildRequires: mingw64-libtiff
BuildRequires: mingw64-openjpeg2
BuildRequires: mingw64-openjpeg2-tools
BuildRequires: mingw64-cairo
BuildRequires: mingw64-gtk3
BuildRequires: mingw64-lcms2
BuildRequires: mingw64-qt5-qtbase-devel
BuildRequires: mingw64-qt6-qtbase
BuildRequires: mingw64-curl


%description
MinGW Windows Poppler library.

###############################################################################

%package -n mingw32-%{pkgname}
Summary:       MinGW Windows Poppler library

%description -n mingw32-%{pkgname}
MinGW Windows Poppler library.

###############################################################################

%package -n mingw32-%{pkgname}-glib
Summary:       MinGW Windows Poppler-Glib library
Requires:      mingw32-%{pkgname} = %{version}-%{release}

%description -n mingw32-%{pkgname}-glib
MinGW Windows Poppler-Glib library.

###############################################################################

%package -n mingw32-%{pkgname}-qt5
Summary:       MinGW Windows Poppler-Qt5 library
Requires:      mingw32-%{pkgname} = %{version}-%{release}

%description -n mingw32-%{pkgname}-qt5
MinGW Windows Poppler-Qt5 library.

###############################################################################

%package -n mingw32-%{pkgname}-qt6
Summary:       MinGW Windows Poppler-Qt6 library
Requires:      mingw32-%{pkgname} = %{version}-%{release}

%description -n mingw32-%{pkgname}-qt6
MinGW Windows Poppler-Qt6 library.

###############################################################################

%package -n mingw32-%{pkgname}-cpp
Summary:       MinGW Windows C++ Poppler library
Requires:      mingw32-%{pkgname} = %{version}-%{release}

%description -n mingw32-%{pkgname}-cpp
MinGW Windows C++ Poppler library.

###############################################################################

%package -n mingw64-%{pkgname}
Summary:       MinGW Windows Poppler library

%description -n mingw64-%{pkgname}
MinGW Windows Poppler library.

###############################################################################

%package -n mingw64-%{pkgname}-glib
Summary:       MinGW Windows Poppler-Glib library
Requires:      mingw64-%{pkgname} = %{version}-%{release}

%description -n mingw64-%{pkgname}-glib
MinGW Windows Poppler-Glib library.

###############################################################################

%package -n mingw64-%{pkgname}-qt5
Summary:       MinGW Windows Poppler-Qt5 library
Requires:      mingw64-%{pkgname} = %{version}-%{release}

%description -n mingw64-%{pkgname}-qt5
MinGW Windows Poppler-Qt5 library.

###############################################################################

%package -n mingw64-%{pkgname}-qt6
Summary:       MinGW Windows Poppler-Qt6 library
Requires:      mingw64-%{pkgname} = %{version}-%{release}

%description -n mingw64-%{pkgname}-qt6
MinGW Windows Poppler-Qt6 library.

###############################################################################

%package -n mingw64-%{pkgname}-cpp
Summary:       MinGW Windows C++ Poppler library
Requires:      mingw64-%{pkgname} = %{version}-%{release}

%description -n mingw64-%{pkgname}-cpp
MinGW Windows C++ Poppler library.

###############################################################################

%{?mingw_debug_package}


%prep
%autosetup -p1 -n %{pkgname}-%{version}


%build
export MINGW32_CXXFLAGS="%{mingw32_cflags} -msse2"
export MINGW64_CXXFLAGS="%{mingw64_cflags} -msse2"

%mingw_cmake \
  -DENABLE_CMS=lcms2 \
  -DENABLE_DCTDECODER=libjpeg \
  -DENABLE_LIBOPENJPEG=openjpeg2 \
  -DENABLE_UNSTABLE_API_ABI_HEADERS=ON \
  -DENABLE_NSS3=OFF \
  -DENABLE_GPGME=OFF \
  -DENABLE_ZLIB=OFF \

%mingw_make_build


%install
%mingw_make_install

# Delete man files
rm -rf %{buildroot}%{mingw32_mandir}
rm -rf %{buildroot}%{mingw64_mandir}

# Delete exe files
rm -f %{buildroot}%{mingw32_bindir}/*.exe
rm -f %{buildroot}%{mingw64_bindir}/*.exe


%files -n mingw32-%{pkgname}
%license COPYING
%doc README.md
%{mingw32_bindir}/libpoppler-151.dll
%{mingw32_includedir}/poppler/
%exclude %{mingw32_includedir}/poppler/cpp/
%exclude %{mingw32_includedir}/poppler/glib/
%exclude %{mingw32_includedir}/poppler/qt5/
%{mingw32_libdir}/libpoppler.dll.a
%{mingw32_libdir}/pkgconfig/poppler.pc

%files -n mingw32-%{pkgname}-glib
%{mingw32_bindir}/libpoppler-glib-8.dll
%{mingw32_includedir}/poppler/glib/
%{mingw32_libdir}/libpoppler-glib.dll.a
%{mingw32_libdir}/pkgconfig/poppler-glib.pc

%files -n mingw32-%{pkgname}-qt5
%{mingw32_bindir}/libpoppler-qt5-1.dll
%{mingw32_includedir}/poppler/qt5/
%{mingw32_libdir}/libpoppler-qt5.dll.a
%{mingw32_libdir}/pkgconfig/poppler-qt5.pc

%files -n mingw32-%{pkgname}-qt6
%{mingw32_bindir}/libpoppler-qt6-3.dll
%{mingw32_includedir}/poppler/qt6/
%{mingw32_libdir}/libpoppler-qt6.dll.a
%{mingw32_libdir}/pkgconfig/poppler-qt6.pc

%files -n mingw32-%{pkgname}-cpp
%{mingw32_bindir}/libpoppler-cpp-2.dll
%{mingw32_includedir}/poppler/cpp/
%{mingw32_libdir}/libpoppler-cpp.dll.a
%{mingw32_libdir}/pkgconfig/poppler-cpp.pc

%files -n mingw64-%{pkgname}
%license COPYING
%doc README.md
%{mingw64_bindir}/libpoppler-151.dll
%{mingw64_includedir}/poppler/
%exclude %{mingw64_includedir}/poppler/cpp/
%exclude %{mingw64_includedir}/poppler/glib/
%exclude %{mingw64_includedir}/poppler/qt5/
%{mingw64_libdir}/libpoppler.dll.a
%{mingw64_libdir}/pkgconfig/poppler.pc

%files -n mingw64-%{pkgname}-glib
%{mingw64_bindir}/libpoppler-glib-8.dll
%{mingw64_includedir}/poppler/glib/
%{mingw64_libdir}/libpoppler-glib.dll.a
%{mingw64_libdir}/pkgconfig/poppler-glib.pc

%files -n mingw64-%{pkgname}-qt5
%{mingw64_bindir}/libpoppler-qt5-1.dll
%{mingw64_includedir}/poppler/qt5/
%{mingw64_libdir}/libpoppler-qt5.dll.a
%{mingw64_libdir}/pkgconfig/poppler-qt5.pc

%files -n mingw64-%{pkgname}-qt6
%{mingw64_bindir}/libpoppler-qt6-3.dll
%{mingw64_includedir}/poppler/qt6/
%{mingw64_libdir}/libpoppler-qt6.dll.a
%{mingw64_libdir}/pkgconfig/poppler-qt6.pc

%files -n mingw64-%{pkgname}-cpp
%{mingw64_bindir}/libpoppler-cpp-2.dll
%{mingw64_includedir}/poppler/cpp/
%{mingw64_libdir}/libpoppler-cpp.dll.a
%{mingw64_libdir}/pkgconfig/poppler-cpp.pc


%changelog
* Wed Oct 29 2025 Sandro Mani <manisandro@gmail.com> - 25.07.0-2
- Backport patch for CVE-2025-52885

* Thu Jul 31 2025 Sandro Mani <manisandro@gmail.com> - 25.07.0-1
- Update to 25.07.0

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 25.02.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Apr 15 2025 Sandro Mani <manisandro@gmail.com> - 25.02.0-2
- Backport fixes for CVE-2025-32364 and CVE-2025-32365

* Wed Feb 26 2025 Sandro Mani <manisandro@gmail.com> - 25.02.0-1
- Update to 25.02.0

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 24.08.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Jan 01 2025 Sandro Mani <manisandro@gmail.com> - 24.08.0-2
- Backport fix for CVE-2024-56378

* Fri Aug 23 2024 Sandro Mani <manisandro@gmail.com> - 24.08.0-1
- Update to 24.08.0

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 24.02.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 21 2024 Sandro Mani <manisandro@gmail.com> - 24.02.0-2
- Backport fix for CVE-2024-6239

* Fri Feb 02 2024 Sandro Mani <manisandro@gmail.com> - 24.02.0-1
- Update to 24.02.0

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 23.08.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 23.08.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Aug 12 2023 Sandro Mani <manisandro@gmail.com> - 23.08.0-1
- Update to 23.08.0

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 23.02.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sun Mar 26 2023 Orion Poplawski <orion@nwra.com> - 23.02.0-2
- Remove all ExcludeArch: s390x lines

* Tue Feb 07 2023 Sandro Mani <manisandro@gmail.com> - 23.02.0-1
- Update to 23.02.0

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 22.08.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Aug 03 2022 Sandro Mani <manisandro@gmail.com> - 22.08.0-1
- Update to 22.08.0

* Thu Jul 21 2022 Sandro Mani <manisandro@gmail.com> - 22.01.0-6
- Backport fix for CVE-2022-27337

* Fri May 20 2022 Sandro Mani <manisandro@gmail.com> - 22.01.0-5
- Rebuild for gdal-3.5.0 and/or openjpeg-2.5.0

* Wed Mar 30 2022 Sandro Mani <manisandro@gmail.com> - 22.01.0-4
- Drop ExclusiveArch: s390x

* Fri Mar 25 2022 Sandro Mani <manisandro@gmail.com> - 22.01.0-3
- Rebuild with mingw-gcc-12

* Tue Jan 18 2022 Sandro Mani <manisandro@gmail.com> - 22.01.0-2
- Add -qt6 subpackage

* Fri Jan 14 2022 Sandro Mani <manisandro@gmail.com> - 22.01.0-1
- Update to 22.01.0

* Mon Aug 02 2021 Sandro Mani <manisandro@gmail.com> - 21.08.0-1
- Update to 21.08.0

* Mon Aug 02 2021 Sandro Mani <manisandro@gmail.com> - 21.07.0-1
- Update 21.07.0

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 21.04.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Apr 07 2021 Sandro Mani <manisandro@gmail.com> - 21.04.0-1
- Update to 21.04.0

* Thu Mar 04 2021 Sandro Mani <manisandro@gmail.com> - 21.03.0-1
- Update to 21.03.0

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 21.01.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jan 11 2021 Sandro Mani <manisandro@gmail.com> - 21.01.0-1
- Update to 21.01.0

* Wed Aug 12 13:45:03 GMT 2020 Sandro Mani <manisandro@gmail.com> - 0.90.1-3
- Rebuild (mingw-gettext)

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.90.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 21 2020 Sandro Mani <manisandro@gmail.com> - 0.90.1-1
- Update to 0.90.1

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.84.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jan 17 2020 Sandro Mani <manisandro@gmail.com> - 0.84.0-1
- Update to 0.84.0

* Wed Nov 13 2019 Sandro Mani <manisandro@gmail.com> - 0.73.0-6
- Install XPDF headers again
- Drop old Obsoletes

* Tue Oct 08 2019 Sandro Mani <manisandro@gmail.com> - 0.73.0-5
- Rebuild (Changes/Mingw32GccDwarf2)

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.73.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Feb 20 2019 Sandro Mani <manisandro@gmail.com> - 0.73.0-3
- Backport security fixes: CVE-2018-20662, CVE-2019-7310

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.73.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jan 26 2019 Sandro Mani <manisandro@gmail.com> - 0.73.0-1
- Update to 0.73.0

* Thu Dec 20 2018 Sandro Mani <manisandro@gmail.com> - 0.67.0-2
- Backport security fixes:
  CVE-2018-16646, CVE-2018-19058, CVE-2018-19059, CVE-2018-19060, CVE-2018-19149

* Tue Aug 14 2018 Sandro Mani <manisandro@gmail.com> - 0.67.0-1
- Update to 0.67.0

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.63.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Apr 11 2018 Sandro Mani <manisandro@gmail.com> - 0.63.0-1
- Update to 0.63

* Wed Feb 14 2018 Sandro Mani <manisandro@gmail.com> - 0.62.0-1
- Update to 0.62
- Drop qt4 frontend

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.61.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Nov 14 2017 Sandro Mani <manisandro@gmail.com> - 0.61.1-1
- Update to 0.61.1

* Wed Nov 08 2017 Sandro Mani <manisandro@gmail.com> - 0.61.0-1
- Update to 0.61.0

* Sun Oct 08 2017 Sandro Mani <manisandro@gmail.com> - 0.60.1-1
- Update to 0.60.1

* Mon Oct 02 2017 Sandro Mani <manisandro@gmail.com> - 0.59.0-2
- Add patch for CVE-2017-14520 (#1494584)

* Fri Sep 08 2017 Sandro Mani <manisandro@gmail.com> - 0.59.0-1
- Update to 0.59.0

* Fri Aug 04 2017 Sandro Mani <manisandro@gmail.com> - 0.57.0-1
- Update to 0.57.0

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.56.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Jul 14 2017 Sandro Mani <manisandro@gmail.com> - 0.56.0-2
- Add patch for CVE-2017-9865 (#1466435)
- Add patch for CVE-2017-7515 (#1459066)

* Mon Jun 26 2017 Sandro Mani <manisandro@gmail.com> - 0.56.0-1
- Update to 0.56.0

* Tue May 30 2017 Sandro Mani <manisandro@gmail.com> - 0.55.0-2
- Add patches for CVE-2017-7511 (#1456829) and CVE-2017-9083 (#1453200)

* Thu May 25 2017 Sandro Mani <manisandro@gmail.com> - 0.55.0-1
- Update to 0.55.0

* Tue Mar 28 2017 Sandro Mani <manisandro@gmail.com> - 0.53.0-1
- Update to 0.53.0

* Sun Feb 19 2017 Sandro Mani <manisandro@gmail.com> - 0.52.0-1
- Update to 0.52.0

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.51.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun Jan 22 2017 Sandro Mani <manisandro@gmail.com> - 0.51.0-2
- Rebuild for Qt5-5.7.1

* Mon Jan 16 2017 Sandro Mani <manisandro@gmail.com> - 0.51.0-1
- Update to 0.51.0

* Sat Dec 17 2016 Sandro Mani <manisandro@gmail.com> - 0.50.0-2
- Build against openjpeg2

* Fri Dec 16 2016 Sandro Mani <manisandro@gmail.com> - 0.50.0-1
- Update to 0.50.0

* Wed Nov 23 2016 Sandro Mani <manisandro@gmail.com> - 0.49.0-1
- Update to 0.49.0

* Sat Oct 22 2016 Sandro Mani <manisandro@gmail.com> - 0.48.0-1
- Update to 0.48.0

* Tue Jul 19 2016 Sandro Mani <manisandro@gmail.com> - 0.45.0-1
- Update to 0.45.0

* Tue May 03 2016 Sandro Mani <manisandro@gmail.com> - 0.43.0-1
- Update to 0.43

* Wed Mar 09 2016 Sandro Mani <manisandro@gmail.com> - 0.41.0-1
- Update to 0.41

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.40.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sat Jan 23 2016 Sandro Mani <manisandro@gmail.com> - 0.40.0-1
- Update to 0.40

* Wed Jul 22 2015 Sandro Mani <manisandro@gmail.com> - 0.34.0-1
- Update to 0.34

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.33.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 06 2015 Sandro Mani <manisandro@gmail.com> - 0.33.0-1
- Update to 0.33.0

* Mon May 11 2015 Sandro Mani <manisandro@gmail.com> - 0.30.0-3
- Fix includes listed multiple times
- --enable-xpdf-headers

* Tue Jan 27 2015 Sandro Mani <manisandro@gmail.com> - 0.30.0-2
- Re-enable openjpeg support

* Tue Jan 27 2015 Sandro Mani <manisandro@gmail.com> - 0.30.0-1
- Update to 0.30.0

* Thu Nov 27 2014 Sandro Mani <manisandro@gmail.com> - 0.28.1-1
- Update to 0.28.1

* Mon Sep 29 2014 Sandro Mani <manisandro@gmail.com> - 0.26.5-1
- Update to 0.26.5

* Sat Aug 23 2014 Sandro Mani <manisandro@gmail.com> - 0.26.4-1
- Update to 0.26.4

* Mon Jul 21 2014 Sandro Mani <manisandro@gmail.com> - 0.26.3-1
- Update to 0.26.3

* Thu Jun 19 2014 Sandro Mani <manisandro@gmail.com> - 0.26.2-1
- Update to 0.26.2

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.26.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon May 26 2014 Sandro Mani <manisandro@gmail.com> - 0.26.1-1
- Update to 0.26.1

* Wed May 14 2014 Sandro Mani <manisandro@gmail.com> - 0.26.0-1
- Update to 0.26.0

* Fri Apr 25 2014 Sandro Mani <manisandro@gmail.com> - 0.24.5-2
- Add poppler_pkgconfig_private_libs.patch

* Fri Jan 03 2014 Sandro Mani <manisandro@gmail.com> - 0.24.5-1
- Update to 0.24.5, fixes #1048203

* Wed Nov 27 2013 Sandro Mani <manisandro@gmail.com> - 0.24.4-1
- Update to 0.24.4

* Mon Oct 28 2013 Sandro Mani <manisandro@gmail.com> - 0.24.3-2
- Add patch to fix Qt5 detection

* Mon Oct 28 2013 Sandro Mani <manisandro@gmail.com> - 0.24.3-1
- Update to 0.24.3

* Mon Sep 30 2013 Sandro Mani <manisandro@gmail.com> - 0.24.2-1
- Update to 0.24.2

* Tue Aug 27 2013 Sandro Mani <manisandro@gmail.com> - 0.24.1-1
- Update to 0.24.1
- Enable qt5 build

* Mon Aug 19 2013 Sandro Mani <manisandro@gmail.com> - 0.24.0-1
- Update to 0.24.0

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.22.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Jul 13 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 0.22.5-2
- Rebuild against libpng 1.6

* Mon Jun 17 2013 Sandro Mani <manisandro@gmail.com> - 0.22.5-1
- Update to 0.22.5

* Sat May 11 2013 Sandro Mani <manisandro@gmail.com> - 0.22.1-2
- Use versioned BuildRequires for mingw32/64-filesystem
- Remove unused mingw_build_win32/64 macros
- Remove tools subpackage (and do not ship exes)

* Wed May 08 2013 Sandro Mani <manisandro@gmail.com> - 0.22.1-1
- Initial Fedora package
