# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%{?mingw_package_header}

%global pkgname win-iconv

Name:          mingw-%{pkgname}
Version:       0.0.10
Release:       3%{?dist}
Summary:       Iconv implementation using Win32 API

BuildArch:     noarch
License:       LicenseRef-Fedora-Public-Domain
URL:           https://github.com/win-iconv/win-iconv
Source0:       https://github.com/win-iconv/win-iconv/archive/v%{version}/%{pkgname}-%{version}.tar.gz

BuildRequires: make
BuildRequires: cmake

BuildRequires: mingw32-filesystem
BuildRequires: mingw32-gcc-c++

BuildRequires: mingw64-filesystem
BuildRequires: mingw64-gcc-c++


%description
MinGW Windows Iconv library


%{?mingw_debug_package}


# Win32
%package -n mingw32-win-iconv
Summary:       MinGW Windows Iconv library

%description -n mingw32-win-iconv
MinGW Windows cross compiled Iconv library.

%package -n mingw32-win-iconv-static
Summary:       Static version of the MinGW Windows Iconv library
Requires:      mingw32-win-iconv = %{version}-%{release}

%description -n mingw32-win-iconv-static
Static version of the MinGW Windows Iconv library.

# Win64
%package -n mingw64-win-iconv
Summary:       MinGW Windows Iconv library

%description -n mingw64-win-iconv
MinGW Windows Iconv library

%package -n mingw64-win-iconv-static
Summary:       Static version of the MinGW Windows Iconv library
Requires:      mingw64-win-iconv = %{version}-%{release}

%description -n mingw64-win-iconv-static
Static version of the MinGW Windows Iconv library.


%prep
%autosetup -p1 -n %{pkgname}-%{version}
sed -i 's|\r||' readme.txt ChangeLog


%build
%mingw_cmake -DDISABLE_LOCALE_CHARSET=ON
%mingw_make_build


%install
%mingw_make_install

rm %{buildroot}/%{mingw32_bindir}/win_iconv.exe
rm %{buildroot}/%{mingw64_bindir}/win_iconv.exe

# Fix file conflict with mingw-libcharset
rm -f %{buildroot}%{mingw32_includedir}/localcharset.h
rm -f %{buildroot}%{mingw64_includedir}/localcharset.h


%files -n mingw32-win-iconv
%doc ChangeLog readme.txt
%{mingw32_bindir}/iconv.dll
%{mingw32_includedir}/iconv.h
%{mingw32_libdir}/libiconv.dll.a

%files -n mingw32-win-iconv-static
%{mingw32_libdir}/libiconv.a

%files -n mingw64-win-iconv
%doc ChangeLog readme.txt
%{mingw64_bindir}/iconv.dll
%{mingw64_includedir}/iconv.h
%{mingw64_libdir}/libiconv.dll.a

%files -n mingw64-win-iconv-static
%{mingw64_libdir}/libiconv.a


%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat May 31 2025 Sandro Mani <manisandro@gmail.com> - 0.0.10-2
- Pass DISABLE_LOCALE_CHARSET=ON

* Sat May 03 2025 Sandro Mani <manisandro@gmail.com> - 0.0.10-1
- Update to 0.0.10

* Mon Apr 28 2025 Sandro Mani <manisandro@gmail.com> - 0.0.9-2
- Fix file conflict with mingw-libcharset

* Mon Apr 21 2025 Sandro Mani <manisandro@gmail.com> - 0.0.9-1
- Update to 0.0.9

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.8-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.8-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.8-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.8-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.8-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.8-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Mar 25 2022 Sandro Mani <manisandro@gmail.com> - 0.0.8-8
- Rebuild with mingw-gcc-12

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.8-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.8-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.8-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Apr 17 2019 Sandro Mani <manisandro@gmail.com> - 0.0.8-1
- Update to 0.0.8
- Update upstream URLs

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.6-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.6-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.6-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.6-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.6-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Apr 11 2015 Erik van Pienbroek <epienbro@fedoraproject.org> - 0.0.6-3
- Stop using deprecated MinGW packaging macros

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 28 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 0.0.6-1
- Update to 0.0.6

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Sep 21 2012 Kalev Lember <kalevlember@gmail.com> - 0.0.4-1
- Update to 0.0.4
- Drop upstreamed dllname patch

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Mar 10 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 0.0-3-7
- Added win64 support

* Mon Feb 27 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 0.0.3-6
- Rebuild against the mingw-w64 toolchain

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jul 06 2011 Kalev Lember <kalevlember@gmail.com> - 0.0.3-4
- Rename the shared library to iconv.dll instead of hacking up the
  import library

* Wed Jul  6 2011 Erik van Pienbroek <epienbro@fedoraproject.org> - 0.0.3-3
- Make sure that the .dll.a import library refers to libiconv.dll
  instead of iconv.dll

* Sun Jul  3 2011 Erik van Pienbroek <epienbro@fedoraproject.org> - 0.0.3-2
- Add versioned BR for cmake >= 2.8.0

* Fri Jun  3 2011 Erik van Pienbroek <epienbro@fedoraproject.org> - 0.0.3-1
- Update to 0.0.3

* Thu Jun  2 2011 Erik van Pienbroek <epienbro@fedoraproject.org> - 0.0.2-3
- Moved the obsoletes/provides to the proper location
- Bumped the requirement for mingw32-filesystem to >= 68 because of RPM 4.9 support
- Dropped the %%defattr tags
- Dropped the %%{?dist} tag from the obsoletes/provides

* Thu Jun  2 2011 Erik van Pienbroek <epienbro@fedoraproject.org> - 0.0.2-2
- Use the name mingw-win-iconv for the srpm to ease the transition to
  the mingw-w64 based toolchain
- Use the RPM 4.9 dependency generator
- Dropped unnecessary tags

* Thu Feb 17 2011 Erik van Pienbroek <epienbro@fedoraproject.org> - 0.0.2-1
- Update to version 0.0.2
- Dropped upstreamed patch
- Dropped the win_iconv.exe binary
- Bumped the mingw32-iconv obsoletes

* Thu Sep 30 2010 Erik van Pienbroek <epienbro@fedoraproject.org> - 0.0.1-1
- Initial release
- Obsoletes/provides mingw32-iconv and mingw32-iconv-static

