# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%{?mingw_package_header}

%global pkgname libimagequant

# does not support out-of-tree builds
%global w64_dir %{_builddir}/mingw64-%{pkgname}-%{version}-%{release}

Name:           mingw-%{pkgname}
Version:        2.17.0
Release: 13%{?dist}
Summary:        MinGW Windows %{pkgname} library

BuildArch:      noarch
# Automatically converted from old format: GPLv3+ and MIT - review is highly recommended.
License:        GPL-3.0-or-later AND LicenseRef-Callaway-MIT
URL:            https://github.com/ImageOptim/libimagequant
Source0:        %{url}/archive/%{version}/%{pkgname}-%{version}.tar.gz

# MinGW build fixes
Patch0:         libimagequant_mingw.patch

BuildRequires:  make

BuildRequires:  mingw32-filesystem >= 95
BuildRequires:  mingw32-gcc
BuildRequires:  mingw32-libgomp

BuildRequires:  mingw64-filesystem >= 95
BuildRequires:  mingw64-gcc
BuildRequires:  mingw64-libgomp


%description
MinGW Windows %{pkgname} library.


%package -n mingw32-%{pkgname}
Summary:       MinGW Windows %{pkgname} library

%description -n mingw32-%{pkgname}
MinGW Windows %{pkgname} library.


%package -n mingw64-%{pkgname}
Summary:       MinGW Windows %{pkgname} library

%description -n mingw64-%{pkgname}
MinGW Windows %{pkgname} library.


%{?mingw_debug_package}


%prep
%autosetup -p1 -n %{pkgname}-%{version}

cp -a . %{w64_dir}


%build
%mingw32_configure --with-openmp
%mingw32_make dll %{?_smp_mflags}

(
cd %{w64_dir}
%mingw64_configure --with-openmp
%mingw64_make dll %{?_smp_mflags}
)


%install
install -Dpm 0755 %{pkgname}.dll %{buildroot}%{mingw32_bindir}/%{pkgname}.dll
install -Dpm 0755 %{pkgname}.dll.a %{buildroot}%{mingw32_libdir}/%{pkgname}.dll.a
install -Dpm 0644 %{pkgname}.h %{buildroot}%{mingw32_includedir}/%{pkgname}.h

(
cd %{w64_dir}
install -Dpm 0755 %{pkgname}.dll %{buildroot}%{mingw64_bindir}/%{pkgname}.dll
install -Dpm 0755 %{pkgname}.dll.a %{buildroot}%{mingw64_libdir}/%{pkgname}.dll.a
install -Dpm 0644 %{pkgname}.h %{buildroot}%{mingw64_includedir}/%{pkgname}.h
)


%files -n mingw32-%{pkgname}
%license COPYRIGHT
%{mingw32_bindir}/%{pkgname}.dll
%{mingw32_libdir}/%{pkgname}.dll.a
%{mingw32_includedir}/%{pkgname}.h

%files -n mingw64-%{pkgname}
%license COPYRIGHT
%{mingw64_bindir}/%{pkgname}.dll
%{mingw64_libdir}/%{pkgname}.dll.a
%{mingw64_includedir}/%{pkgname}.h


%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.17.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.17.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Sep 02 2024 Miroslav Suchý <msuchy@redhat.com> - 2.17.0-10
- convert license to SPDX

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.17.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.17.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.17.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.17.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.17.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.17.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Mar 25 2022 Sandro Mani <manisandro@gmail.com> - 2.17.0-3
- Rebuild with mingw-gcc-12

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.17.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Nov 16 2021 Sandro Mani <manisandro@gmail.com> - 2.17.0-1
- Update to 2.17.0

* Tue Sep 21 2021 Sandro Mani <manisandro@gmail.com> - 2.16.0-1
- Update to 2.16.0

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.15.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sat May 15 2021 Sandro Mani <manisandro@gmail.com> - 2.15.1-1
- Update to 2.15.1

* Wed Mar 03 2021 Sandro Mani <manisandro@gmail.com> - 2.14.1-1
- Update to 2.14.1

* Thu Jan 28 2021 Sandro Mani <manisandro@gmail.com> - 2.14.0-1
- Update to 2.14.0

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.13.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sun Nov 22 2020 Sandro Mani <manisandro@gmail.com> - 2.13.1-1
- Update to 2.13.1

* Mon Oct 19 2020 Sandro Mani <manisandro@gmail.com> - 2.13.0-1
- Update to 2.13.0

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.12.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu May 21 2020 Sandro Mani <manisandro@gmail.com> - 2.12.6-1
- Update to 2.12.6

* Tue Sep 05 2017 Sandro Mani <manisandro@gmail.com> - 2.10.2-1
- Update to 2.10.2
