# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%{?mingw_package_header}

%global pkgname zstd

Name:          mingw-%{pkgname}
Version:       1.5.7
Release: 3%{?dist}
Summary:       MinGW Windows %{pkgname} library

BuildArch:     noarch
License:       BSD-3-Clause AND GPL-2.0-only
URL:           https://github.com/facebook/%{pkgname}
Source0:       https://github.com/facebook/%{pkgname}/archive/v%{version}/%{pkgname}-%{version}.tar.gz


BuildRequires: make
BuildRequires: cmake

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
%autosetup -p1 -n %{pkgname}-%{version}


%build
MINGW32_CMAKE_ARGS="-DCMAKE_INSTALL_INCLUDEDIR=%{mingw32_includedir}/%{pkgname}" \
MINGW64_CMAKE_ARGS="-DCMAKE_INSTALL_INCLUDEDIR=%{mingw64_includedir}/%{pkgname}" \
%mingw_cmake -DZSTD_BUILD_PROGRAMS=OFF -DZSTD_BUILD_STATIC=OFF ../build/cmake/
%mingw_make_build


%install
%mingw_make_install


%files -n mingw32-%{pkgname}
%license COPYING
%{mingw32_bindir}/lib%{pkgname}.dll
%{mingw32_libdir}/lib%{pkgname}.dll.a
%{mingw32_libdir}/cmake/%{pkgname}/
%{mingw32_libdir}/pkgconfig/lib%{pkgname}.pc
%{mingw32_includedir}/%{pkgname}/

%files -n mingw64-%{pkgname}
%license COPYING
%{mingw64_bindir}/lib%{pkgname}.dll
%{mingw64_libdir}/lib%{pkgname}.dll.a
%{mingw64_libdir}/cmake/%{pkgname}/
%{mingw64_libdir}/pkgconfig/lib%{pkgname}.pc
%{mingw64_includedir}/%{pkgname}/


%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Wed Feb 26 2025 Sandro Mani <manisandro@gmail.com> - 1.5.7-1
- Update to 1.5.7

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sun Mar 31 2024 Sandro Mani <manisandro@gmail.com> - 1.5.6-1
- Update to 1.5.6

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Apr 06 2023 Sandro Mani <manisandro@gmail.com> - 1.5.5-1
- Update to 1.5.5

* Wed Feb 15 2023 Sandro Mani <manisandro@gmail.com> - 1.5.4-1
- Update to 1.5.4

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Mar 25 2022 Sandro Mani <manisandro@gmail.com> - 1.5.2-2
- Rebuild with mingw-gcc-12

* Tue Jan 25 2022 Sandro Mani <manisandro@gmail.com> - 1.5.2-1
- Update to 1.5.2

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Dec 23 2021 Sandro Mani <manisandro@gmail.com> - 1.5.1-1
- Update to 1.5.1

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon May 17 2021 Sandro Mani <manisandro@gmail.com> - 1.5.0-1
- Update to 1.5.0

* Fri Mar 05 2021 Sandro Mani <manisandro@gmail.com> - 1.4.9-1
- Update to 1.4.9

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Dec 30 2020 Sandro Mani <manisandro@gmail.com> - 1.4.8-1
- Update to 1.4.8

* Thu Nov 12 2020 Sandro Mani <manisandro@gmail.com> - 1.4.5-2
- Fix source URL
- Fix license tag

* Thu Nov 12 2020 Sandro Mani <manisandro@gmail.com> - 1.4.5-1
- Initial package
