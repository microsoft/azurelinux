# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%{?mingw_package_header}

%global pkgname fribidi

Name:          mingw-%{pkgname}
Version:       1.0.16
Release:       3%{?dist}
Summary:       MinGW Windows %{pkgname} library

License:       LGPL-2.0-or-later
BuildArch:     noarch
URL:           https://github.com/%{pkgname}/%{pkgname}
Source0:       https://github.com/%{pkgname}/%{pkgname}/releases/download/v%{version}/%{pkgname}-%{version}.tar.xz

# Drop bundled gnulib
Patch0:        fribidi-drop-bundled-gnulib.patch


BuildRequires: meson
BuildRequires: gcc

BuildRequires: mingw32-filesystem >= 95
BuildRequires: mingw32-gcc

BuildRequires: mingw64-filesystem >= 95
BuildRequires: mingw64-gcc


%description
MinGW Windows %{pkgname} library.


%package -n mingw32-%{pkgname}
Summary:       MinGW Windows %{pkgname} library

%description -n mingw32-%{pkgname}
MinGW Windows %{pkgname} library.


%package -n mingw32-%{pkgname}-static
Summary:       Static version of the MinGW Windows %{pkgname} library
Requires:      mingw32-%{pkgname} = %{version}-%{release}

%description -n mingw32-%{pkgname}-static
Static version of the MinGW Windows %{pkgname} library.


%package -n mingw64-%{pkgname}
Summary:       MinGW Windows %{pkgname} library

%description -n mingw64-%{pkgname}
MinGW Windows %{pkgname} library.


%package -n mingw64-%{pkgname}-static
Summary:       Static version of the MinGW Windows %{pkgname} library
Requires:      mingw64-%{pkgname} = %{version}-%{release}

%description -n mingw64-%{pkgname}-static
Static version of the MinGW Windows %{pkgname} library.


%{?mingw_debug_package}


%prep
%autosetup -p1 -n %{pkgname}-%{version}


%build
%mingw_meson --default-library=both -Ddocs=false
%mingw_ninja


%install
%mingw_ninja_install


%files -n mingw32-%{pkgname}
%license COPYING
%{mingw32_bindir}/fribidi.exe
%{mingw32_bindir}/libfribidi-0.dll
%{mingw32_includedir}/fribidi
%{mingw32_libdir}/libfribidi.dll.a
%{mingw32_libdir}/pkgconfig/fribidi.pc

%files -n mingw32-%{pkgname}-static
%{mingw32_libdir}/libfribidi.a

%files -n mingw64-%{pkgname}
%license COPYING
%{mingw64_bindir}/fribidi.exe
%{mingw64_bindir}/libfribidi-0.dll
%{mingw64_includedir}/fribidi
%{mingw64_libdir}/libfribidi.dll.a
%{mingw64_libdir}/pkgconfig/fribidi.pc

%files -n mingw64-%{pkgname}-static
%{mingw64_libdir}/libfribidi.a


%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.16-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.16-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sun Sep 29 2024 Sandro Mani <manisandro@gmail.com> - 1.0.16-1
- Update to 1.0.16

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Jun 11 2024 Sandro Mani <manisandro@gmail.com> - 1.0.15-1
- Update to 1.0.15

* Wed May 08 2024 Sandro Mani <manisandro@gmail.com> - 1.0.14-1
- Update to 1.0.14

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.13-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.13-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri May 19 2023 Sandro Mani <manisandro@gmail.com> - 1.0.13-1
- Update to 1.0.13

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.12-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Apr 21 2022 Sandro Mani <manisandro@gmail.com> - 1.0.12-1
- Update to 1.0.12

* Mon Mar 28 2022 Sandro Mani <manisandro@gmail.com> - 1.0.11-4
- Backport patches for CVE-2022-25310, CVE-2022-25309, CVE-2022-25308

* Fri Mar 25 2022 Sandro Mani <manisandro@gmail.com> - 1.0.11-3
- Rebuild with mingw-gcc-12

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Sep 28 2021 Sandro Mani <manisandro@gmail.com> - 1.0.11-1
- Update to 1.0.11

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.10-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 06 2020 Sandro Mani <manisandro@gmail.com> - 1.0.10-1
- Update to 1.0.10

* Thu Mar 05 2020 Sandro Mani <manisandro@gmail.com> - 1.0.9-1
- Update to 1.0.9

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Dec 13 2019 Sandro Mani <manisandro@gmail.com> - 1.0.8-1
- Update to 1.0.8

* Sat Sep 28 2019 Sandro Mani <manisandro@gmail.com> - 1.0.7-1
- Update to 1.0.7

* Wed Aug 28 2019 Sandro Mani <manisandro@gmail.com> - 1.0.5-1
- Initial package
