# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%{?mingw_package_header}

%global pkgname minizip

Name:          mingw-%{pkgname}
Version:       4.0.10
Release:       2%{?dist}
Summary:       MinGW Windows %{pkgname} library

BuildArch:     noarch
License:       Zlib
URL:           https://github.com/zlib-ng/minizip-ng
Source0:       https://github.com/zlib-ng/minizip-ng/archive/%{version}/%{pkgname}-%{version}.tar.gz
# Add a library version
Patch0:        mingw-minizip_libver.patch

BuildRequires: make
BuildRequires: cmake

BuildRequires: mingw32-bzip2
BuildRequires: mingw32-filesystem
BuildRequires: mingw32-gcc-c++
BuildRequires: mingw32-openssl
BuildRequires: mingw32-xz
BuildRequires: mingw32-zlib
BuildRequires: mingw32-zstd

BuildRequires: mingw64-bzip2
BuildRequires: mingw64-filesystem
BuildRequires: mingw64-gcc-c++
BuildRequires: mingw64-openssl
BuildRequires: mingw64-xz
BuildRequires: mingw64-zlib
BuildRequires: mingw64-zstd


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
%autosetup -p1 -n %{pkgname}-ng-%{version}


%build
MINGW32_CMAKE_ARGS="-DINSTALL_INC_DIR=%{mingw32_includedir}/%{pkgname}" \
MINGW64_CMAKE_ARGS="-DINSTALL_INC_DIR=%{mingw64_includedir}/%{pkgname}" \
%mingw_cmake -DZSTD_FORCE_FETCH=OFF
%mingw_make_build


%install
%mingw_make_install


%files -n mingw32-%{pkgname}
%license LICENSE
%{mingw32_bindir}/lib%{pkgname}-1.dll
%{mingw32_libdir}/lib%{pkgname}.dll.a
%{mingw32_libdir}/cmake/%{pkgname}/
%{mingw32_libdir}/pkgconfig/%{pkgname}.pc
%{mingw32_includedir}/%{pkgname}/

%files -n mingw64-%{pkgname}
%license LICENSE
%{mingw64_bindir}/lib%{pkgname}-1.dll
%{mingw64_libdir}/lib%{pkgname}.dll.a
%{mingw64_libdir}/cmake/%{pkgname}/
%{mingw64_libdir}/pkgconfig/%{pkgname}.pc
%{mingw64_includedir}/%{pkgname}/


%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jun 09 2025 Sandro Mani <manisandro@gmail.com> - 4.0.10-1
- Update to 4.0.10

* Fri Apr 18 2025 Sandro Mani <manisandro@gmail.com> - 4.0.9-1
- Update to 4.0.9

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.7-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.7-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Nov 16 2022 Sandro Mani <manisandro@gmail.com> - 3.0.7-1
- Update to 3.0.7

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Mar 25 2022 Sandro Mani <manisandro@gmail.com> - 3.0.2-5
- Rebuild with mingw-gcc-12

* Thu Feb 17 2022 Sandro Mani <manisandro@gmail.com> - 3.0.2-4
- Rebuild (openssl)

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Jun 10 2021 Sandro Mani <manisandro@gmail.com> - 3.0.2-1
- Update to 3.0.2

* Fri Apr 16 2021 Sandro Mani <manisandro@gmail.com> - 3.0.1-1
- Update to 3.0.1

* Wed Feb 10 2021 Sandro Mani <manisandro@gmail.com> - 3.0.0-1
- Update to 3.0.0

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.10.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Nov 12 2020 Sandro Mani <manisandro@gmail.com> - 2.10.2-1
- Initial package
