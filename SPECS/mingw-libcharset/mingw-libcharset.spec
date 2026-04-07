# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%{?mingw_package_header}

%global pkgname libcharset

Name:          mingw-%{pkgname}
Version:       1.17
Summary:       MinGW Windows libcharset library
Release:       10%{?dist}

BuildArch:     noarch
# Automatically converted from old format: LGPLv2+ - review is highly recommended.
License:       LicenseRef-Callaway-LGPLv2+
URL:           http://www.haible.de/bruno/packages-libcharset.html
Source0:       https://ftp.gnu.org/pub/gnu/libiconv/libiconv-%{version}.tar.gz

BuildRequires: make
BuildRequires: automake autoconf libtool libtool-ltdl-devel bison flex

BuildRequires: mingw32-filesystem >= 95
BuildRequires: mingw32-gcc

BuildRequires: mingw64-filesystem >= 95
BuildRequires: mingw64-gcc


%description
MinGW Windows libcharset library.


%package -n mingw32-%{pkgname}
Summary:       MinGW Windows libcharset library

%description -n mingw32-%{pkgname}
MinGW Windows libcharset library.


%package -n mingw64-%{pkgname}
Summary:       MinGW Windows libcharset library

%description -n mingw64-%{pkgname}
MinGW Windows libcharset library.


%{?mingw_debug_package}


%prep
%autosetup -p1 -n libiconv-%{version}


%build
(
cd libcharset
%mingw_configure --disable-static
%mingw_make_build
)


%install
(
cd libcharset
%mingw_make_install
)

find %{buildroot} -name *.la -delete


%files -n mingw32-%{pkgname}
%license libcharset/COPYING.LIB
%{mingw32_bindir}/libcharset-1.dll
%{mingw32_includedir}/*.h
%{mingw32_libdir}/libcharset.dll.a

%files -n mingw64-%{pkgname}
%license libcharset/COPYING.LIB
%{mingw64_bindir}/libcharset-1.dll
%{mingw64_includedir}/*.h
%{mingw64_libdir}/libcharset.dll.a


%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.17-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.17-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Sep 02 2024 Miroslav Suchý <msuchy@redhat.com> - 1.17-8
- convert license to SPDX

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.17-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.17-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.17-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.17-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.17-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.17-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue May 31 2022 Sandro Mani <manisandro@gmail.com> - 1.17-1
- Update to 1.17

* Fri Mar 25 2022 Sandro Mani <manisandro@gmail.com> - 1.16-3
- Rebuild with mingw-gcc-12

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.16-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jan 05 2022 Sandro Mani <manisandro@gmail.com> - 1.16-1
- Use iconv versioning

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon May 11 2015 Sandro Mani <manisandro@gmail.com> - 1.4.0-1
- Initial package
