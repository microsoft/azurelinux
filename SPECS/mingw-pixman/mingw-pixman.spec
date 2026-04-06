# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%{?mingw_package_header}

Name:           mingw-pixman
Version:        0.46.2
Release:        2%{?dist}
Summary:        MinGW Windows Pixman library

License:        MIT
URL:            http://cgit.freedesktop.org/pixman/

Source0:        http://cairographics.org/releases/pixman-%{version}.tar.gz
Source1:        make-pixman-snapshot.sh

BuildArch:      noarch

BuildRequires:  mingw32-filesystem >= 95
BuildRequires:  mingw32-gcc
BuildRequires:  mingw32-binutils
BuildRequires:  mingw32-libgomp

BuildRequires:  mingw64-filesystem >= 95
BuildRequires:  mingw64-gcc
BuildRequires:  mingw64-binutils
BuildRequires:  mingw64-libgomp

BuildRequires:  gcc
BuildRequires:  meson


%description
MinGW Windows Pixman library.


# Win32
%package -n mingw32-pixman
Summary:        MinGW Windows Pixman library

%description -n mingw32-pixman
MinGW Windows Pixman library.


%package -n mingw32-pixman-static
Summary:        Static version of the MinGW Windows Pixman library
Requires:       mingw32-pixman = %{version}-%{release}

%description -n mingw32-pixman-static
Static version of the MinGW Windows Pixman library.

# Win64
%package -n mingw64-pixman
Summary:        MinGW Windows Pixman library

%description -n mingw64-pixman
MinGW Windows Pixman library.

%package -n mingw64-pixman-static
Summary:        Static version of the cross compiled Pixman library
Requires:       mingw64-pixman = %{version}-%{release}

%description -n mingw64-pixman-static
Static version of the cross compiled Pixman library.


%{?mingw_debug_package}


%prep
%autosetup -p1 -n pixman-%{version}


%build
# Uses GTK for its testsuite, so disable this otherwise we have a chicken & egg problem on mingw
%mingw_meson --default-library=both -Dgtk=disabled
%mingw_ninja


%install
%mingw_ninja_install


# Win32
%files -n mingw32-pixman
%license COPYING
%{mingw32_bindir}/libpixman-1-0.dll
%{mingw32_includedir}/pixman-1
%{mingw32_libdir}/libpixman-1.dll.a
%{mingw32_libdir}/pkgconfig/pixman-1.pc

%files -n mingw32-pixman-static
%{mingw32_libdir}/libpixman-1.a

# Win64
%files -n mingw64-pixman
%license COPYING
%{mingw64_bindir}/libpixman-1-0.dll
%{mingw64_includedir}/pixman-1
%{mingw64_libdir}/libpixman-1.dll.a
%{mingw64_libdir}/pkgconfig/pixman-1.pc

%files -n mingw64-pixman-static
%{mingw64_libdir}/libpixman-1.a


%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.46.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jun 13 2025 Sandro Mani <manisandro@gmail.com> - 0.46.2-1
- Update to 0.46.2

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.44.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Dec 06 2024 Sandro Mani <manisandro@gmail.com> - 0.44.2-1
- Update to 0.44.2

* Sat Nov 09 2024 Sandro Mani <manisandro@gmail.com> - 0.44.0-1
- Update to 0.44.0

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.43.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Apr 08 2024 Sandro Mani <manisandro@gmail.com> - 0.43.4-1
- Update to 0.43.4

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.43.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.43.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jan 10 2024 Sandro Mani <manisandro@gmail.com> - 0.43.0-1
- Update to 0.43.0

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.42.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.42.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Nov 04 2022 Sandro Mani <manisandro@gmail.com> - 0.42.2-1
- Update to 0.42.2

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.40.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Mar 25 2022 Sandro Mani <manisandro@gmail.com> - 0.40.0-6
- Rebuild with mingw-gcc-12

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.40.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.40.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.40.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.40.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Apr 21 2020 Sandro Mani <manisandro@gmail.com> - 0.40.0-1
- Update to 0.40.0

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.38.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Oct 08 2019 Sandro Mani <manisandro@gmail.com> - 0.38.4-2
- Rebuild (Changes/Mingw32GccDwarf2)

* Mon Sep 16 2019 Sandro Mani <manisandro@gmail.com> - 0.38.4-1
- Update to 0.38.4

* Wed Aug 28 2019 Sandro Mani <manisandro@gmail.com> - 0.38.0-1
- Update to 0.38.0

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.34.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.34.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.34.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.34.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.34.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.34.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue May 03 2016 Kalev Lember <klember@redhat.com> - 0.34.0-1
- Update to 0.34.0

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.33.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sat Aug 22 2015 Kalev Lember <klember@redhat.com> - 0.33.2-1
- Update to 0.33.2
- Use license macro for COPYING files

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.32.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Oct 14 2014 Kalev Lember <kalevlember@gmail.com> - 0.32.6-1
- Update to 0.32.6

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.32.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Mar 29 2014 Kalev Lember <kalevlember@gmail.com> - 0.32.0-1
- Update to 0.32.0

* Wed Sep 04 2013 Kalev Lember <kalevlember@gmail.com> - 0.30.0-4
- Disable SSE2 (fdo#68300)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.30.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Jun 15 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 0.30.0-2
- Rebuild to resolve InterlockedCompareExchange regression in mingw32 libraries

* Tue May 14 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 0.30.0-1
- Update to 0.30.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.28.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Nov 22 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 0.28.0-1
- Update to 0.28.0

* Wed Nov 21 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 0.26.2-1
- Update to 0.26.2

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.24.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Mar 10 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 0.24.4-3
- Added win64 support
- Dropped unneeded BR: mingw32-dlfcn

* Tue Mar 06 2012 Kalev Lember <kalevlember@gmail.com> - 0.24.4-2
- Renamed the source package to mingw-pixman (#800445)
- Use mingw macros without leading underscore

* Tue Feb 28 2012 Kalev Lember <kalevlember@gmail.com> - 0.24.4-1
- Update to 0.24.4
- Remove .la files

* Mon Feb 27 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 0.24.2-2
- Rebuild against the mingw-w64 toolchain

* Wed Feb 01 2012 Kalev Lember <kalevlember@gmail.com> - 0.24.2-1
- Update to 0.24.2

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.22.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Jul 16 2011 Kalev Lember <kalevlember@gmail.com> - 0.22.2-1
- Update to 0.22.2
- Use automatic mingw dep extraction
- Cleaned up the spec file for modern rpmbuild

* Sun May 08 2011 Kalev Lember <kalev@smartlink.ee> - 0.22.0-1
- Update to 0.22.0

* Mon Apr 25 2011 Kalev Lember <kalev@smartlink.ee> - 0.20.2-1
- Update to 0.20.2

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.19.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Sep 24 2010 Erik van Pienbroek <epienbro@fedoraproject.org> - 0.19.4-1
- Update to 0.19.4
- Fixed Source URL
- Fixed a small rpmlint warning

* Tue Sep  7 2010 Erik van Pienbroek <epienbro@fedoraproject.org> - 0.19.2-1
- Update to 0.19.2

* Mon Jul 12 2010 Erik van Pienbroek <epienbro@fedoraproject.org> - 0.18.2-1
- Update to 0.18.2 (RHBZ #613665)

* Tue Sep 29 2009 Erik van Pienbroek <epienbro@fedoraproject.org> - 0.16.2-1
- Update to 0.16.2

* Fri Sep 18 2009 Erik van Pienbroek <epienbro@fedoraproject.org> - 0.16.0-2
- Rebuild because of broken mingw32-gcc/mingw32-binutils

* Sat Aug 29 2009 Erik van Pienbroek <epienbro@fedoraproject.org> - 0.16.0-1
- Update to 0.16.0

* Thu Aug 13 2009 Erik van Pienbroek <epienbro@fedoraproject.org> - 0.15.20-1
- Update to version 0.15.20
- Updated SOURCE0 and URL
- Automatically generate debuginfo subpackage
- Don't build the 'blitters-test' testcase as it requires the memalign function
  which we don't have on MinGW

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.15.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jun 10 2009 Erik van Pienbroek <epienbro@fedoraproject.org> - 0.15.10-1
- Update to 0.15.10
- Use %%global instead of %%define
- Dropped pixman-0.13.2-license.patch as freedesktop bug #19582 is resolved

* Fri Apr  3 2009 Erik van Pienbroek <epienbro@fedoraproject.org> - 0.13.2-5
- Fixed %%defattr line
- Added -static subpackage

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Feb 20 2009 Richard W.M. Jones <rjones@redhat.com> - 0.13.2-3
- Rebuild for mingw32-gcc 4.4

* Thu Jan 15 2009 Richard W.M. Jones <rjones@redhat.com> - 0.13.2-2
- Include LICENSE file (freedesktop bug 19582).

* Tue Jan 13 2009 Richard W.M. Jones <rjones@redhat.com> - 0.13.2-1
- Resynch with Fedora package (0.13.2).
- Disable static library for speed.
- Use _smp_mflags.
- Requires pkgconfig.
- Depends on dlfcn.

* Wed Sep 24 2008 Richard W.M. Jones <rjones@redhat.com> - 0.12.0-2
- Rename mingw -> mingw32.

* Mon Sep 22 2008 Daniel P. Berrange <berrange@redhat.com> - 0.12.0-1
- Update to 0.12.0 release

* Wed Sep 10 2008 Richard W.M. Jones <rjones@redhat.com> - 0.11.10-2
- Remove static library.

* Tue Sep  9 2008 Daniel P. Berrange <berrange@redhat.com> - 0.11.10-1
- Initial RPM release
