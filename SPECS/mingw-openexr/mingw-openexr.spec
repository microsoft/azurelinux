# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%{?mingw_package_header}

%global pkgname openexr

Name:          mingw-%{pkgname}
Version:       3.3.6
Release:       1%{?dist}
Summary:       MinGW Windows %{pkgname} library

License:       BSD-3-Clause
URL:           http://www.openexr.com/
BuildArch:     noarch
Source0:       https://github.com/AcademySoftwareFoundation/%{pkgname}/archive/v%{version}/%{pkgname}-%{version}.tar.gz


BuildRequires: cmake
BuildRequires: make

BuildRequires: mingw32-filesystem >= 95
BuildRequires: mingw32-gcc
BuildRequires: mingw32-gcc-c++
BuildRequires: mingw32-imath
BuildRequires: mingw32-libdeflate
BuildRequires: mingw32-zlib

BuildRequires: mingw64-filesystem >= 95
BuildRequires: mingw64-gcc
BuildRequires: mingw64-gcc-c++
BuildRequires: mingw64-imath
BuildRequires: mingw64-libdeflate
BuildRequires: mingw64-zlib

%description
MinGW Windows %{pkgname} library.


%package -n mingw32-%{pkgname}
Summary:       MinGW Windows %{pkgname} library
Provides:      mingw32-OpenEXR = %{version}-%{release}
Provides:      mingw32-ilmbase = %{version}-%{release}
Obsoletes:     mingw32-OpenEXR < 2.5.3
Obsoletes:     mingw32-OpenEXR-static < 2.5.3
Obsoletes:     mingw32-ilmbase < 2.5.3

%description -n mingw32-%{pkgname}
%{summary}.



%package -n mingw32-%{pkgname}-tools
Summary:       Tools for the MinGW Windows %{pkgname} library
Requires:      mingw32-%{pkgname} = %{version}-%{release}
Provides:      mingw32-OpenEXR-tools = %{version}-%{release}
Provides:      mingw32-ilmbase-tools = %{version}-%{release}
Obsoletes:     mingw32-OpenEXR-tools < 2.5.3
Obsoletes:     mingw32-ilmbase-tools < 2.5.3

%description -n mingw32-%{pkgname}-tools
%{summary}.


%package -n mingw64-%{pkgname}
Summary:       MinGW Windows %{pkgname} library
Provides:      mingw64-OpenEXR = %{version}-%{release}
Provides:      mingw64-ilmbase = %{version}-%{release}
Obsoletes:     mingw64-OpenEXR < 2.5.3
Obsoletes:     mingw64-OpenEXR-static < 2.5.3
Obsoletes:     mingw64-ilmbase < 2.5.3

%description -n mingw64-%{pkgname}
%{summary}.


%package -n mingw64-%{pkgname}-tools
Summary:       Tools for the MinGW Windows %{pkgname} library
Requires:      mingw64-%{pkgname} = %{version}-%{release}
Provides:      mingw64-OpenEXR-tools = %{version}-%{release}
Provides:      mingw64-ilmbase-tools = %{version}-%{release}
Obsoletes:     mingw64-OpenEXR-tools < 2.5.3
Obsoletes:     mingw64-ilmbase-tools < 2.5.3

%description -n mingw64-%{pkgname}-tools
%{summary}.


%{?mingw_debug_package}


%prep
%autosetup -p1 -n %{pkgname}-%{version}


%build
%mingw_cmake -DOPENEXR_INSTALL_PKG_CONFIG=ON -DBUILD_TESTING=OFF
%mingw_make_build


%install
%mingw_make_install

# Don't install doc
rm -rf %{buildroot}%{mingw32_docdir}/OpenEXR
rm -rf %{buildroot}%{mingw64_docdir}/OpenEXR


%files -n mingw32-%{pkgname}
%license LICENSE.md
%{mingw32_bindir}/libIex-3_3.dll
%{mingw32_bindir}/libIlmThread-3_3.dll
%{mingw32_bindir}/libOpenEXR-3_3.dll
%{mingw32_bindir}/libOpenEXRCore-3_3.dll
%{mingw32_bindir}/libOpenEXRUtil-3_3.dll
%{mingw32_includedir}/OpenEXR/
%{mingw32_libdir}/libIex-3_3.dll.a
%{mingw32_libdir}/libIlmThread-3_3.dll.a
%{mingw32_libdir}/libOpenEXR-3_3.dll.a
%{mingw32_libdir}/libOpenEXRCore-3_3.dll.a
%{mingw32_libdir}/libOpenEXRUtil-3_3.dll.a
%{mingw32_libdir}/cmake/OpenEXR/
%{mingw32_libdir}/pkgconfig/OpenEXR.pc


%files -n mingw32-%{pkgname}-tools
%{mingw32_bindir}/exr2aces.exe
%{mingw32_bindir}/exrenvmap.exe
%{mingw32_bindir}/exrheader.exe
%{mingw32_bindir}/exrinfo.exe
%{mingw32_bindir}/exrmakepreview.exe
%{mingw32_bindir}/exrmaketiled.exe
%{mingw32_bindir}/exrmanifest.exe
%{mingw32_bindir}/exrmetrics.exe
%{mingw32_bindir}/exrmultipart.exe
%{mingw32_bindir}/exrmultiview.exe
%{mingw32_bindir}/exrstdattr.exe

%files -n mingw64-%{pkgname}
%license LICENSE.md
%{mingw64_bindir}/libIex-3_3.dll
%{mingw64_bindir}/libIlmThread-3_3.dll
%{mingw64_bindir}/libOpenEXR-3_3.dll
%{mingw64_bindir}/libOpenEXRCore-3_3.dll
%{mingw64_bindir}/libOpenEXRUtil-3_3.dll
%{mingw64_includedir}/OpenEXR/
%{mingw64_libdir}/libIex-3_3.dll.a
%{mingw64_libdir}/libIlmThread-3_3.dll.a
%{mingw64_libdir}/libOpenEXR-3_3.dll.a
%{mingw64_libdir}/libOpenEXRCore-3_3.dll.a
%{mingw64_libdir}/libOpenEXRUtil-3_3.dll.a
%{mingw64_libdir}/cmake/OpenEXR/
%{mingw64_libdir}/pkgconfig/OpenEXR.pc


%files -n mingw64-%{pkgname}-tools
%{mingw64_bindir}/exr2aces.exe
%{mingw64_bindir}/exrenvmap.exe
%{mingw64_bindir}/exrheader.exe
%{mingw64_bindir}/exrinfo.exe
%{mingw64_bindir}/exrmakepreview.exe
%{mingw64_bindir}/exrmaketiled.exe
%{mingw64_bindir}/exrmanifest.exe
%{mingw64_bindir}/exrmetrics.exe
%{mingw64_bindir}/exrmultipart.exe
%{mingw64_bindir}/exrmultiview.exe
%{mingw64_bindir}/exrstdattr.exe


%changelog
* Sat Jan 17 2026 Sandro Mani <manisandro@gmail.com> - 3.3.6-1
- Update to 3.3.6

* Sun Aug 10 2025 Sandro Mani <manisandro@gmail.com> - 3.3.5-2
- Rebuild (imath)

* Sun Jul 27 2025 Sandro Mani <manisandro@gmail.com> - 3.3.5-1
- Update to 3.3.5

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jun 09 2025 Sandro Mani <manisandro@gmail.com> - 3.3.4-1
- Update to 3.3.4

* Fri Mar 28 2025 Sandro Mani <manisandro@gmail.com> - 3.3.3-1
- Update to 3.3.3

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Nov 14 2024 Sandro Mani <manisandro@gmail.com> - 3.3.2-1
- Update to 3.3.2

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sun Apr 28 2024 Sandro Mani <manisandro@gmail.com> - 3.2.4-1
- Update to 3.2.4

* Fri Feb 16 2024 Sandro Mani <manisandro@gmail.com> - 3.1.10-4
- Backport patch for CVE-2023-5841

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Aug 04 2023 Sandro Mani <manisandro@gmail.com> - 3.1.10-1
- Update to 3.1.10

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jul 18 2023 Sandro Mani <manisandro@gmail.com> - 3.1.9-1
- Update to 3.1.9

* Fri May 19 2023 Sandro Mani <manisandro@gmail.com> - 3.1.7-1
- Update to 3.1.7

* Mon Mar 20 2023 Sandro Mani <manisandro@gmail.com> - 3.1.6-1
- Update to 3.1.6

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sun Apr 17 2022 Sandro Mani <manisandro@gmail.com> - 3.1.5-1
- Update to 3.1.5

* Fri Mar 25 2022 Sandro Mani <manisandro@gmail.com> - 3.1.4-2
- Rebuild with mingw-gcc-12

* Mon Mar 14 2022 Sandro Mani <manisandro@gmail.com> - 3.1.4-1
- Update to 3.1.4

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Nov 03 2021 Sandro Mani <manisandro@gmail.com> - 3.1.3-1
- Update to 3.1.3

* Thu Oct 07 2021 Sandro Mani <manisandro@gmail.com> - 3.1.2-1
- Update to 3.1.2

* Mon Aug 16 2021 Sandro Mani <manisandro@gmail.com> - 3.1.1-1
- Update to 3.1.1

* Fri Jul 30 2021 Sandro Mani <manisandro@gmail.com> - 3.0.5-1
- Update to 3.0.5

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 11 2021 Sandro Mani <manisandro@gmail.com> - 2.5.5-3
- Backport patch for CVE-2021-3598
- Backport fix for heap buffer overflow

* Sat May 01 2021 Sandro Mani <manisandro@gmail.com> - 2.5.5-2
- Backport patch for CVE-2021-23169

* Wed Mar 24 2021 Sandro Mani <manisandro@gmail.com> - 2.5.5-1
- Update to 2.5.5

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Jan 07 2021 Sandro Mani <manisandro@gmail.com> - 2.5.4-1
- Update to 2.5.4

* Thu Dec 17 2020 Sandro Mani <manisandro@gmail.com> - 2.5.3-1
- Initial package to replace mingw-OpenEXR and mingw-ilmbase
