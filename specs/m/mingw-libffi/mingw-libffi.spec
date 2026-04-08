# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%{?mingw_package_header}

Name:		mingw-libffi
Version:	3.5.1
Release:	2%{?dist}
Summary:	A portable foreign function interface library for MinGW

License:	MIT
URL:		http://sourceware.org/libffi
Source0:        https://github.com/libffi/libffi/releases/download/v%{version}/libffi-%{version}.tar.gz

BuildArch:	noarch

BuildRequires:  make

BuildRequires:	mingw32-filesystem >= 95
BuildRequires:	mingw32-binutils
BuildRequires:	mingw32-gcc

BuildRequires:	mingw64-filesystem >= 95
BuildRequires:	mingw64-binutils
BuildRequires:	mingw64-gcc


%description
Foreign function interface library for MinGW.


# Win32
%package -n mingw32-libffi
Summary:	A portable foreign function interface library for MinGW

%description -n mingw32-libffi
Foreign function interface library for MinGW.

# Win32 static
%package -n mingw32-libffi-static
Summary:       A portable foreign function interface static library for MinGW

%description -n mingw32-libffi-static
Foreign function interface static library for MinGW.


# Win64
%package -n mingw64-libffi
Summary:	A portable foreign function interface library for MinGW

%description -n mingw64-libffi
Foreign function interface library for MinGW.

# Win64 static
%package -n mingw64-libffi-static
Summary:       A portable foreign function interface static library for MinGW

%description -n mingw64-libffi-static
Foreign function interface static library for MinGW.


%{?mingw_debug_package}


%prep
%autosetup -p1 -n libffi-%{version}

%build
%mingw_configure --enable-shared
%mingw_make


%install
%mingw_make_install

rm -rf %{buildroot}%{mingw32_infodir}
rm -rf %{buildroot}%{mingw64_infodir}
rm -rf %{buildroot}%{mingw32_mandir}
rm -rf %{buildroot}%{mingw64_mandir}

# Drop all .la files
find %{buildroot} -name "*.la" -delete


%files -n mingw32-libffi
%license LICENSE
%{mingw32_bindir}/libffi-8.dll
%{mingw32_includedir}/ffi.h
%{mingw32_includedir}/ffitarget.h
%{mingw32_libdir}/libffi.dll.a
%{mingw32_libdir}/pkgconfig/libffi.pc

%files -n mingw32-libffi-static
%{mingw32_libdir}/libffi.a

%files -n mingw64-libffi
%license LICENSE
%{mingw64_bindir}/libffi-8.dll
%{mingw64_includedir}/ffi.h
%{mingw64_includedir}/ffitarget.h
%{mingw64_libdir}/libffi.dll.a
%{mingw64_libdir}/pkgconfig/libffi.pc

%files -n mingw64-libffi-static
%{mingw64_libdir}/libffi.a


%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sun Jun 15 2025 Sandro Mani <manisandro@gmail.com> - 3.5.1-1
- Update to 3.5.1

* Tue May 13 2025 Sandro Mani <manisandro@gmail.com> - 3.4.8-1
- Update to 3.4.8

* Wed Mar 05 2025 Sandro Mani <manisandro@gmail.com> - 3.4.7-1
- Update to 3.4.7

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Mar 22 2024 Sandro Mani <manisandro@gmail.com> - 3.4.6-1
- Update to 3.4.6

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Nov 12 2022 Sandro Mani <manisandro@gmail.com> - 3.4.4-1
- Update to 3.4.4

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Mar 25 2022 Sandro Mani <manisandro@gmail.com> - 3.4.2-3
- Rebuild with mingw-gcc-12

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 30 2021 Sandro Mani <manisandro@gmail.com> - 3.4.2-1
- Update to 3.4.2

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Feb 12 2020 Sandro Mani <manisandro@gmail.com> - 3.1-9
- Drop libffi-3.1-fix-include-path.patch, it just breaks the pkgconfig file

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Aug 14 2019 Fabiano Fidêncio <fidencio@redhat.com> - 3.1-7
- Add the same patches from its native counter part, rhbz#1740764

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jun 20 2017 Kalev Lember <klember@redhat.com> - 3.1-1
- Update to 3.1
- Use license macro

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.13-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.13-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.13-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.13-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.13-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Jun 15 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 3.0.13-3
- Rebuild to resolve InterlockedCompareExchange regression in mingw32 libraries

* Fri May 31 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 3.0.13-2
- Rebuild against latest mingw-filesystem

* Sun May  5 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 3.0.13-1
- Update to 3.0.13

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.11-0.5.rc2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.11-0.4.rc2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri May 11 2012 Eric Smith <eric@brouhaha.com> - 3.0.11-0.3.rc2
- Added static subpackages

* Sat Mar 10 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 3.0.11-0.2.rc2
- Added win64 support

* Thu Mar 08 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 3.0.11-0.1.rc2
- Update to 3.0.11-rc2
- Removed .la file

* Tue Mar 06 2012 Kalev Lember <kalevlember@gmail.com> - 3.0.9-5
- Renamed the source package to mingw-libffi (#800427)
- Spec clean up

* Mon Feb 27 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 3.0.9-4
- Rebuild against the mingw-w64 toolchain

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Oct 9 2010 Paolo Bonzini <pbonzini@redhat.com> - 3.0.9-1
- Created.
