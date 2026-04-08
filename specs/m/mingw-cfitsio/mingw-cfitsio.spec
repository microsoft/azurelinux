# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%{?mingw_package_header}

%global pkgname cfitsio

Name:          mingw-%{pkgname}
# NOTE: sync SOVER in cfitsio_build.patch with the one in configure.in
Version:       4.6.2
Release:       3%{?dist}
Summary:       MinGW Windows CFITSIO library

License:       CFITSIO
BuildArch:     noarch
URL:           http://heasarc.gsfc.nasa.gov/fitsio/
Source0:       http://heasarc.gsfc.nasa.gov/FTP/software/fitsio/c/%{pkgname}-%{version}.tar.gz
# Install headers to include/cfitsio
Patch0:        cfitsio_cmake.patch

BuildRequires: make
BuildRequires: cmake

BuildRequires: mingw32-filesystem
BuildRequires: mingw32-curl
BuildRequires: mingw32-gcc-c++
BuildRequires: mingw32-zlib

BuildRequires: mingw64-filesystem
BuildRequires: mingw64-curl
BuildRequires: mingw64-gcc-c++
BuildRequires: mingw64-zlib


%description
MinGW Windows CFITSIO library.


%package -n mingw32-%{pkgname}
Summary:       MinGW Windows CFITSIO library

%description -n mingw32-%{pkgname}
MinGW Windows CFITSIO library.


%package -n mingw32-%{pkgname}-tools
Summary:       MinGW Windows CFITSIO library

%description -n mingw32-%{pkgname}-tools
MinGW Windows CFITSIO library.


%package -n mingw64-%{pkgname}
Summary:       MinGW Windows CFITSIO library

%description -n mingw64-%{pkgname}
MinGW Windows CFITSIO library.


%package -n mingw64-%{pkgname}-tools
Summary:       MinGW Windows CFITSIO library

%description -n mingw64-%{pkgname}-tools
MinGW Windows CFITSIO library.


%{?mingw_debug_package}


%prep
%autosetup -p1 -n %{pkgname}-%{version}


%build
%mingw_cmake -DUTILS=ON -DCMAKE_DLL_NAME_WITH_SOVERSION=ON -DTESTS=OFF
%mingw_make_build


%install
%mingw_make_install


%files -n mingw32-%{pkgname}
%license licenses/License.txt
%{mingw32_bindir}/libcfitsio-10.dll
%{mingw32_libdir}/libcfitsio.dll.a
%{mingw32_libdir}/pkgconfig/cfitsio.pc
%{mingw32_libdir}/cmake/%{pkgname}/
%{mingw32_includedir}/cfitsio/

%files -n mingw32-%{pkgname}-tools
%{mingw32_bindir}/fitscopy.exe
%{mingw32_bindir}/fitsverify.exe
%{mingw32_bindir}/fpack.exe
%{mingw32_bindir}/funpack.exe
%{mingw32_bindir}/imcopy.exe
%{mingw32_bindir}/speed.exe

%files -n mingw64-%{pkgname}
%license licenses/License.txt
%{mingw64_bindir}/libcfitsio-10.dll
%{mingw64_libdir}/libcfitsio.dll.a
%{mingw64_libdir}/pkgconfig/cfitsio.pc
%{mingw64_libdir}/cmake/%{pkgname}/
%{mingw64_includedir}/cfitsio/

%files -n mingw64-%{pkgname}-tools
%{mingw64_bindir}/fitscopy.exe
%{mingw64_bindir}/fitsverify.exe
%{mingw64_bindir}/fpack.exe
%{mingw64_bindir}/funpack.exe
%{mingw64_bindir}/imcopy.exe
%{mingw64_bindir}/speed.exe

%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4.6.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jul 17 2025 Sandro Mani <manisandro@gmail.com> - 4.6.2-2
- Increase minimum cmake version

* Fri Mar 28 2025 Sandro Mani <manisandro@gmail.com> - 4.6.2-1
- Update to 4.6.2

* Fri Mar 21 2025 Sandro Mani <manisandro@gmail.com> - 4.6.0-1
- Update to 4.6.0

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4.5.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Sep 26 2024 Sandro Mani <manisandro@gmail.com> - 4.5.0-2
- Pass -DCMAKE_DLL_NAME_WITH_SOVERSION=ON

* Tue Aug 27 2024 Sandro Mani <manisandro@gmail.com> - 4.5.0-1
- Update to 4.5.0

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Mar 07 2024 Sandro Mani <manisandro@gmail.com> - 4.4.0-1
- Update to 4.4.0

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Nov 28 2023 Sandro Mani <manisandro@gmail.com> - 4.3.1-1
- Update to 4.3.1

* Tue Aug 29 2023 Sandro Mani <manisandro@gmail.com> - 4.3.0-1
- Update to 4.3.0

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Dec 30 2022 Sandro Mani <manisandro@gmail.com> - 4.2.0-1
- Update to 4.2.0

* Tue Aug 30 2022 Sandro Mani <manisandro@gmail.com> - 4.1.0-1
- Update to 4.1.0

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Mar 25 2022 Sandro Mani <manisandro@gmail.com> - 4.0.0-4
- Rebuild with mingw-gcc-12

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Dec 07 2021 Sandro Mani <manisandro@gmail.com> - 4.0.0-2
- Fix pkg-config file

* Sun Dec 05 2021 Sandro Mani <manisandro@gmail.com> - 4.0.0-1
- Update to 4.0.0

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.490-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Feb 01 2021 Sandro Mani <manisandro@gmail.com> - 3.490-1
- Update to 3.490

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.470-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.470-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.470-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Oct 08 2019 Sandro Mani <manisandro@gmail.com> - 3.470-3
- Rebuild (Changes/Mingw32GccDwarf2)

* Mon Sep 16 2019 Sandro Mani <manisandro@gmail.com> - 3.470-2
- Fix broken pkgconfig file

* Fri Aug 02 2019 Sandro Mani <manisandro@gmail.com> - 3.470-1
- Update to 3.470

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.450-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.450-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.450-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon May 28 2018 Sandro Mani <manisandro@gmail.com> - 3.450-1
- Updateto 3.450

* Mon Mar 12 2018 Sandro Mani <manisandro@gmail.com> - 3.430-1
- Update to 3.430

* Fri Feb 23 2018 Sandro Mani <manisandro@gmail.com> - 3.420-1
- Update to 3.420

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.410-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Apr 20 2017 Sandro Mani <manisandro@gmail.com> - 3.410-1
- Update to 3.410

* Thu Apr 23 2015 Sandro Mani <manisandro@gmail.com> - 3.370-1
- Initial package
