# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%{?mingw_package_header}

Name:           mingw-libpng
Version:        1.6.55
Release: 2%{?dist}
Summary:        MinGW Windows Libpng library

License:        Zlib
URL:            http://www.libpng.org/pub/png/
Source0:        http://downloads.sourceforge.net/libpng/libpng-%{version}.tar.xz

BuildArch:      noarch

BuildRequires: make
BuildRequires:  mingw32-filesystem >= 95
BuildRequires:  mingw32-gcc
BuildRequires:  mingw32-binutils
BuildRequires:  mingw32-zlib

BuildRequires:  mingw64-filesystem >= 95
BuildRequires:  mingw64-gcc
BuildRequires:  mingw64-binutils
BuildRequires:  mingw64-zlib


%description
MinGW Windows Libpng library.


# Win32
%package -n mingw32-libpng
Summary:        MinGW Windows Libpng library
Requires:       pkgconfig

%description -n mingw32-libpng
MinGW Windows Libpng library.

%package -n mingw32-libpng-static
Summary:        Static version of MinGW Windows Libpng library
Requires:       mingw32-libpng = %{version}-%{release}

%description -n mingw32-libpng-static
MinGW Windows Libpng library.

This package contains static cross-compiled libraries.

# Win64
%package -n mingw64-libpng
Summary:        MinGW Windows Libpng library
Requires:       pkgconfig

%description -n mingw64-libpng
MinGW Windows Libpng library.

%package -n mingw64-libpng-static
Summary:        Static version of MinGW Windows Libpng library
Requires:       mingw64-libpng = %{version}-%{release}

%description -n mingw64-libpng-static
MinGW Windows Libpng library.

This package contains static cross-compiled libraries.


%{?mingw_debug_package}


%prep
%autosetup -p1 -n libpng-%{version}


%build
%mingw_configure
%mingw_make_build


%install
%mingw_make_install

# Drop all .la files
find %{buildroot} -name "*.la" -delete

# No need to distribute manpages which appear in the Fedora
# native packages already.
rm -rf %{buildroot}%{mingw32_mandir}
rm -rf %{buildroot}%{mingw64_mandir}


# Win32
%files -n mingw32-libpng
%license LICENSE
%doc ANNOUNCE CHANGES README TODO
%{mingw32_bindir}/libpng-config
%{mingw32_bindir}/libpng16-16.dll
%{mingw32_bindir}/libpng16-config
%{mingw32_bindir}/png-fix-itxt.exe
%{mingw32_bindir}/pngfix.exe
%{mingw32_includedir}/libpng16
%{mingw32_includedir}/png.h
%{mingw32_includedir}/pngconf.h
%{mingw32_includedir}/pnglibconf.h
%{mingw32_libdir}/libpng.dll.a
%{mingw32_libdir}/libpng16.dll.a
%{mingw32_libdir}/pkgconfig/libpng.pc
%{mingw32_libdir}/pkgconfig/libpng16.pc

%files -n mingw32-libpng-static
%{mingw32_libdir}/libpng.a
%{mingw32_libdir}/libpng16.a

# Win64
%files -n mingw64-libpng
%license LICENSE
%doc ANNOUNCE CHANGES README TODO
%{mingw64_bindir}/libpng-config
%{mingw64_bindir}/libpng16-16.dll
%{mingw64_bindir}/libpng16-config
%{mingw64_bindir}/png-fix-itxt.exe
%{mingw64_bindir}/pngfix.exe
%{mingw64_includedir}/libpng16
%{mingw64_includedir}/png.h
%{mingw64_includedir}/pngconf.h
%{mingw64_includedir}/pnglibconf.h
%{mingw64_libdir}/libpng.dll.a
%{mingw64_libdir}/libpng16.dll.a
%{mingw64_libdir}/pkgconfig/libpng.pc
%{mingw64_libdir}/pkgconfig/libpng16.pc

%files -n mingw64-libpng-static
%{mingw64_libdir}/libpng.a
%{mingw64_libdir}/libpng16.a


%changelog
* Thu Feb 12 2026 Sandro Mani <manisandro@gmail.com> - 1.6.55-1
- Update to 1.6.55

* Thu Jan 29 2026 Sandro Mani <manisandro@gmail.com> - 1.6.54-1
- Update to 1.6.54

* Fri Jan 16 2026 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.53-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Sat Dec 13 2025 Sandro Mani <manisandro@gmail.com> - 1.6.53-1
- Update to 1.6.53

* Sun Nov 30 2025 Sandro Mani <manisandro@gmail.com> - 1.6.51-1
- Update to 1.6.51

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.50-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jul 18 2025 Sandro Mani <manisandro@gmail.com> - 1.6.50-1
- Update to 1.6.50

* Tue Jun 17 2025 Sandro Mani <manisandro@gmail.com> - 1.6.49-1
- Update to 1.6.49

* Tue May 06 2025 Sandro Mani <manisandro@gmail.com> - 1.6.48-1
- Update to 1.6.48

* Thu Feb 20 2025 Sandro Mani <manisandro@gmail.com> - 1.6.47-1
- Update to 1.6.47

* Fri Feb 07 2025 Sandro Mani <manisandro@gmail.com> - 1.6.46-1
- Update to 1.6.46

* Mon Jan 20 2025 Sandro Mani <manisandro@gmail.com> - 1.6.44-3
- Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.44-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Sep 19 2024 Sandro Mani <manisandro@gmail.com> - 1.6.44-1
- Update to 1.6.44

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.40-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.40-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.40-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Sep 25 2023 Sandro Mani <manisandro@gmail.com> - 1.6.40-1
- Update to 1.6.40

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.37-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.37-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.37-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Mar 25 2022 Sandro Mani <manisandro@gmail.com> - 1.6.37-8
- Rebuild with mingw-gcc-12

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.37-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.37-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.37-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.37-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.37-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Oct 08 2019 Sandro Mani <manisandro@gmail.com> - 1.6.37-2
- Rebuild (Changes/Mingw32GccDwarf2)

* Wed Aug 28 2019 Sandro Mani <manisandro@gmail.com> - 1.6.37-1
- Update to 1.6.37

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.29-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.29-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.29-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.29-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.29-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jun 20 2017 Kalev Lember <klember@redhat.com> - 1.6.29-1
- Update to 1.6.29

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.27-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Dec 30 2016 Kalev Lember <klember@redhat.com> - 1.6.27-1
- Update to 1.6.27

* Tue Oct 25 2016 Kalev Lember <klember@redhat.com> - 1.6.26-1
- Update to 1.6.26
- Don't set group tags

* Sun Oct 16 2016 Kalev Lember <klember@redhat.com> - 1.6.25-1
- Update to 1.6.25

* Mon Aug 08 2016 Kalev Lember <klember@redhat.com> - 1.6.24-1
- Update to 1.6.24

* Wed Jun 15 2016 Kalev Lember <klember@redhat.com> - 1.6.23-1
- Update to 1.6.23

* Sat Feb  6 2016 Erik van Pienbroek <epienbro@fedoraproject.org> - 1.6.21-1
- Update to 1.6.21
- Fixes various CVE's (RHBZ #1281760, #1281756)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.19-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Nov 19 2015 Kalev Lember <klember@redhat.com> - 1.6.19-1
- Update to 1.6.19

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Mar 29 2014 Kalev Lember <kalevlember@gmail.com> - 1.6.10-1
- Update to 1.6.10

* Wed Nov 20 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 1.6.7-1
- Update to 1.6.7

* Sat Sep  7 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 1.6.3-1
- Update to 1.6.3

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Jul 13 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 1.6.2-1
- Update to 1.6.2

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Oct 07 2012 Kalev Lember <kalevlember@gmail.com> - 1.5.13-1
- Update to 1.5.13 (CVE-2011-3464)

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Mar 10 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 1.5.7-4
- Added win64 support

* Tue Mar 06 2012 Kalev Lember <kalevlember@gmail.com> - 1.5.7-3
- Renamed the source package to mingw-libpng (#800430)
- Use mingw macros without leading underscore

* Mon Feb 27 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 1.5.7-2
- Rebuild against the mingw-w64 toolchain

* Tue Jan 31 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 1.5.7-1
- Update to 1.5.7
- Dropped .la files

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Dec 24 2011 Ivan Romanov <drizt@land.ru> - 1.4.8-2
- New static subpackage

* Fri Jul 22 2011 Kalev Lember <kalevlember@gmail.com> - 1.4.8-1
- Update to 1.4.8 (CVE-2011-2690, CVE-2011-2692)
- Generate debuginfo subpackage
- Removed static libs from the main package
- Spec cleanup

* Wed Jun 29 2011 Richard W.M. Jones <rjones@redhat.com> - 1.4.3-3
- Include fix for CVE-2011-2501 (RHBZ#717510, RHBZ#717511).

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jul  4 2010 Erik van Pienbroek <epienbro@fedoraproject.org> - 1.4.3-1
- Update to 1.4.3
- Fixes CVE-2010-1205 (BZ #608238)
- Fixes CVE-2010-2249 (BZ #608644)
- Use %%global instead of %%define
- Fixed %%defattr tag
- Dropped unneeded patches

* Fri Nov 20 2009 Erik van Pienbroek <epienbro@fedoraproject.org> - 1.2.40-2
- In the previous build no symbols were exported in the resulting DLL making this
  package unusable. This should be fixed for now (but may need more research)

* Thu Nov  5 2009 Richard W.M. Jones <rjones@redhat.com> - 1.2.40-1
- New upstream version 1.2.40.

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.37-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jun  9 2009 Richard W.M. Jones <rjones@redhat.com> - 1.2.37-1
- New upstream version 1.2.37 to fix SECURITY bug RHBZ#504782.

* Wed Feb 25 2009 Richard W.M. Jones <rjones@redhat.com> - 1.2.35-1
- Update to libpng 1.2.35, to fix CVE-2009-0040 (Tom Lane).

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.34-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Feb 20 2009 Richard W.M. Jones <rjones@redhat.com> - 1.2.34-3
- Rebuild for mingw32-gcc 4.4

* Tue Jan 13 2009 Richard W.M. Jones <rjones@redhat.com> - 1.2.34-2
- Depend on mingw32-filesystem >= 40 so we can still build in F-10.

* Tue Jan 13 2009 Richard W.M. Jones <rjones@redhat.com> - 1.2.34-1
- Rebase to 1.2.34 and patches from Fedora.
- Requires pkgconfig.
- Add documentation.

* Wed Sep 24 2008 Richard W.M. Jones <rjones@redhat.com> - 1.2.31-5
- Rename mingw -> mingw32.

* Mon Sep 22 2008 Daniel P. Berrange <berrange@redhat.com> - 1.2.31-4
- Add patches from rawhide RPM

* Sun Sep 21 2008 Richard W.M. Jones <rjones@redhat.com> - 1.2.31-3
- Don't duplicate Fedora native manpages.

* Wed Sep 10 2008 Richard W.M. Jones <rjones@redhat.com> - 1.2.31-2
- Remove static library.

* Tue Sep  9 2008 Daniel P. Berrange <berrange@redhat.com> - 1.2.31-1
- Initial RPM release
