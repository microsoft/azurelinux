# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%{?mingw_package_header}

%global pkgname imath

Name:          mingw-%{pkgname}
Version:       3.2.1
Release:       1%{?dist}
Summary:       MinGW Windows %{pkgname} library

License:       BSD-3-Clause
URL:           http://www.openexr.com/
BuildArch:     noarch
Source0:       https://github.com/AcademySoftwareFoundation/Imath/archive/v%{version}/%{pkgname}-%{version}.tar.gz


BuildRequires: cmake
BuildRequires: make

BuildRequires: mingw32-filesystem >= 95
BuildRequires: mingw32-gcc-c++

BuildRequires: mingw64-filesystem >= 95
BuildRequires: mingw64-gcc-c++

%description
MinGW Windows %{pkgname} library.


%package -n mingw32-%{pkgname}
Summary:       MinGW Windows %{pkgname} library

%description -n mingw32-%{pkgname}
%{summary}.


%package -n mingw64-%{pkgname}
Summary:       MinGW Windows %{pkgname} library

%description -n mingw64-%{pkgname}
%{summary}.


%{?mingw_debug_package}


%prep
%autosetup -p1 -n Imath-%{version}


%build
%mingw_cmake -DIMATH_INSTALL_PKG_CONFIG=ON -DBUILD_TESTING=OFF
%mingw_make_build


%install
%mingw_make_install


%files -n mingw32-%{pkgname}
%license LICENSE.md
%{mingw32_bindir}/libImath-3_2.dll
%{mingw32_includedir}/Imath/
%{mingw32_libdir}/libImath-3_2.dll.a
%{mingw32_libdir}/cmake/Imath/
%{mingw32_libdir}/pkgconfig/Imath.pc

%files -n mingw64-%{pkgname}
%license LICENSE.md
%{mingw64_bindir}/libImath-3_2.dll
%{mingw64_includedir}/Imath/
%{mingw64_libdir}/libImath-3_2.dll.a
%{mingw64_libdir}/cmake/Imath/
%{mingw64_libdir}/pkgconfig/Imath.pc


%changelog
* Sat Aug 16 2025 Sandro Mani <manisandro@gmail.com> - 3.2.1-1
- Update to 3.2.1

* Sun Aug 10 2025 Sandro Mani <manisandro@gmail.com> - 3.2.0-1
- Update to 3.2.0

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.12-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Sep 10 2024 Sandro Mani <manisandro@gmail.com> - 3.1.12-1
- Update to 3.1.12

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Mar 15 2024 Sandro Mani <manisandro@gmail.com> - 3.1.11-1
- Update to 3.1.11

* Mon Feb 12 2024 Sandro Mani <manisandro@gmail.com> - 3.1.10-1
- Update to 3.1.10

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sat Jun 03 2023 Sandro Mani <manisandro@gmail.com> - 3.1.9-1
- Update to 3.1.9

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Nov 12 2022 Sandro Mani <manisandro@gmail.com> - 3.1.6-1
- Update to 3.1.6

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sun Apr 17 2022 Sandro Mani <manisandro@gmail.com> - 3.1.5-1
- Update to 3.1.5

* Fri Mar 25 2022 Sandro Mani <manisandro@gmail.com> - 3.1.4-2
- Rebuild with mingw-gcc-12

* Tue Jan 25 2022 Sandro Mani <manisandro@gmail.com> - 3.1.4-1
- Update to 3.1.4

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Nov 03 2021 Sandro Mani <manisandro@gmail.com> - 3.1.3-1
- Update to 3.1.3

* Sat Aug 14 2021 Sandro Mani <manisandro@gmail.com> - 3.1.2-1
- Update to 3.1.2
- Rename mingw-Imath -> mingw-imath

* Fri Jul 30 2021 Sandro Mani <manisandro@gmail.com> - 3.0.2-1
- Initial package
