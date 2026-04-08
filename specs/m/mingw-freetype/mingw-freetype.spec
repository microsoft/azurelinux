# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%{?mingw_package_header}

Name:           mingw-freetype
# NOTE See comment for Patch2 below
Version:        2.13.3
Release:        3%{?dist}
Summary:        Free and portable font rendering engine

License:        FTL OR GPL-2.0-or-later
URL:            http://www.freetype.org
Source0:        http://download.savannah.gnu.org/releases/freetype/freetype-%{version}.tar.xz

# Patches from native Fedora package:

# Enable subpixel rendering (ClearType)
Patch0:         freetype-2.3.0-enable-spr.patch
# Enable otvalid and gxvalid modules
Patch1:         freetype-2.2.1-enable-valid.patch
# Re-add symbol downstream for ABI compatibility only. Remove once soname has been bumped from -6.
Patch2:         freetype-2.10.0-internal-outline.patch

BuildArch:      noarch

BuildRequires:  gcc
BuildRequires:  make

BuildRequires:  mingw32-filesystem >= 95
BuildRequires:  mingw32-gcc
BuildRequires:  mingw32-binutils
BuildRequires:  mingw32-zlib
BuildRequires:  mingw32-bzip2
BuildRequires:  mingw32-libpng

BuildRequires:  mingw64-filesystem >= 95
BuildRequires:  mingw64-gcc
BuildRequires:  mingw64-binutils
BuildRequires:  mingw64-zlib
BuildRequires:  mingw64-bzip2
BuildRequires:  mingw64-libpng

%description
MinGW Windows Freetype library.

# Win32
%package -n mingw32-freetype
Summary:        Free and portable font rendering engine

%description -n mingw32-freetype
MinGW Windows Freetype library.

%package -n mingw32-freetype-static
Summary:        Static version of the MinGW Windows Freetype library
Requires:       mingw32-freetype = %{version}-%{release}

%description -n mingw32-freetype-static
Static version of the MinGW Windows Freetype library.

# Win64
%package -n mingw64-freetype
Summary:        Free and portable font rendering engine

%description -n mingw64-freetype
MinGW Windows Freetype library.

%package -n mingw64-freetype-static
Summary:        Static version of the MinGW Windows Freetype library
Requires:       mingw64-freetype = %{version}-%{release}

%description -n mingw64-freetype-static
Static version of the MinGW Windows Freetype library.


%{?mingw_debug_package}


%prep
%autosetup -p1 -n freetype-%{version}


%build
%mingw_configure \
           --enable-static \
           --enable-shared \
           --with-zlib=yes \
           --with-bzip2=yes \
           --with-png=yes \
           --enable-freetype-config \
           --with-harfbuzz=no

%mingw_make_build

# The ft2demos Makefile is hacky and doesn't understand
# cross-compilation.  This nearly works, but not quite, so
# disable. it.
#pushd ft2demos-%{version}
#make TOP_DIR=".." PLATFORM=win32
#popd


%install
%mingw_make_install

# Drop all .la files
find %{buildroot} -name "*.la" -delete

# Remove redundent man pages
rm -rf %{buildroot}%{mingw32_mandir} %{buildroot}%{mingw64_mandir}


%files -n mingw32-freetype
%license LICENSE.TXT
%{mingw32_bindir}/freetype-config
%{mingw32_bindir}/libfreetype-6.dll
%{mingw32_includedir}/freetype2
%{mingw32_libdir}/libfreetype.dll.a
%{mingw32_libdir}/pkgconfig/freetype2.pc
%{mingw32_datadir}/aclocal/freetype2.m4

%files -n mingw32-freetype-static
%{mingw32_libdir}/libfreetype.a

%files -n mingw64-freetype
%license LICENSE.TXT
%{mingw64_bindir}/freetype-config
%{mingw64_bindir}/libfreetype-6.dll
%{mingw64_includedir}/freetype2
%{mingw64_libdir}/libfreetype.dll.a
%{mingw64_libdir}/pkgconfig/freetype2.pc
%{mingw64_datadir}/aclocal/freetype2.m4

%files -n mingw64-freetype-static
%{mingw64_libdir}/libfreetype.a


%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.13.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.13.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Oct 10 2024 Sandro Mani <manisandro@gmail.com> - 2.13.3-1
- Update to 2.13.3

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.13.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.13.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.13.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jan 17 2024 Sandro Mani <manisandro@gmail.com> - 2.13.2-1
- Update to 2.13.2

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.13.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jun 28 2023 Sandro Mani <manisandro@gmail.com> - 2.13.1-1
- Update to 2.13.1

* Tue Feb 28 2023 Sandro Mani <manisandro@gmail.com> - 2.13.0-1
- Update to 2.13.0

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.12.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.12.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue May 03 2022 Sandro Mani <manisandro@gmail.com> - 2.12.1-1
- Update to 2.12.1

* Tue Apr 26 2022 Sandro Mani <manisandro@gmail.com> - 2.12.0-1
- Update to 2.12.0

* Fri Mar 25 2022 Sandro Mani <manisandro@gmail.com> - 2.11.1-3
- Rebuild with mingw-gcc-12

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.11.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Dec 15 2021 Sandro Mani <manisandro@gmail.com> - 2.11.1-1
- Update to 2.11.1

* Sat Jul 24 2021 Sandro Mani <manisandro@gmail.com> - 2.11.0-1
- Update to 2.11.0

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.10.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.10.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Oct 23 2020 Sandro Mani <manisandro@gmail.com> - 2.10.4-1
- Update to 2.10.4

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.10.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sat Jul 18 2020 Sandro Mani <manisandro@gmail.coM> - 2.10.2-1
- Update to 2.10.2

* Fri Feb 07 2020 Sandro Mani <manisandro@gmail.com> - 2.10.1-1
- Update to 2.10.1

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.10.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Aug 30 2019 Sandro Mani <manisandro@gmail.com> - 2.10.0-1
- Update to 2.10.0

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Nov 01 2018 Kalev Lember <klember@redhat.com> - 2.9.1-1
- Update to 2.9.1
- Sync patches with the native package
- Enable ClearType code thanks to Microsoft joining OIN

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sun Oct 15 2017 Kalev Lember <klember@redhat.com> - 2.8-1
- Update to 2.8
- Sync patches with the native package

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jun 20 2017 Kalev Lember <klember@redhat.com> - 2.7.1-1
- Update to 2.7.1

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun Oct 16 2016 Kalev Lember <klember@redhat.com> - 2.7-1
- Update to 2.7
- Sync patches with the native package

* Mon Sep 05 2016 Kalev Lember <klember@redhat.com> - 2.6.5-1
- Update to 2.6.5
- Don't set group tags

* Tue May 03 2016 Kalev Lember <klember@redhat.com> - 2.6.3-1
- Update to 2.6.3
- Sync patches with the native package

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sun Aug 23 2015 Kalev Lember <klember@redhat.com> - 2.6-1
- Update to 2.6
- Sync patches with the native package
- Use license macro for license files

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Dec 23 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.5.4-1
- Update to 2.5.4
- Fixes RHBZ #1172635

* Thu Jul 10 2014 Nicola Fontana <ntd@entidi.it> - 2.5.3-3
- Update subpixel rendering patch to 2.5.3 (RHBZ #1118276)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May 29 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.5.3-1
- Update to 2.5.3

* Sat Sep  7 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.5.0.1-1
- Update to 2.5.0.1
- Added BR: mingw32-libpng mingw64-libpng

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Jun 15 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.4.12-1
- Update to 2.4.12

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jan 16 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.4.11-1
- Update to 2.4.11
- Removed unused source tags

* Wed Oct 24 2012 Nicola Fontana <ntd@entidi.it> - 2.4.10-2
- Added static subpackage

* Sun Oct 07 2012 Kalev Lember <kalevlember@gmail.com> - 2.4.10-1
- Update to 2.4.10

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Jun 03 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.4.9-1
- Update to 2.4.9
- Added BR: mingw32-bzip2 mingw64-bzip2

* Sat Mar 10 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.4.8-5
- Added win64 support

* Fri Mar 09 2012 Kalev Lember <kalevlember@gmail.com> - 2.4.8-4
- Remove .la files

* Tue Mar 06 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.4.8-3
- Renamed the source package to mingw-freetype (RHBZ #800380)
- Use mingw macros without leading underscore

* Mon Feb 27 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.4.8-2
- Rebuild against the mingw-w64 toolchain

* Mon Jan 30 2012 Kalev Lember <kalevlember@gmail.com> - 2.4.8-1
- Update to 2.4.8

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Aug 07 2011 Kalev Lember <kalevlember@gmail.com> - 2.4.6-1
- Update to 2.4.6

* Sat Jul 30 2011 Kalev Lember <kalevlember@gmail.com> - 2.4.5-1
- Update to 2.4.5
- Synced patches with Fedora native freetype 2.4.5-2
- Spec cleanup
- Enable automatic mingw dep extraction
- Create -debuginfo subpackage

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jan 12 2010 Richard W.M. Jones <rjones@redhat.com> - 2.3.11-1
- New upstream version 2.3.11.
- Match patches from Fedora native version.
- Recheck package with rpmlint.

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Feb 20 2009 Richard W.M. Jones <rjones@redhat.com> - 2.3.8-2
- Rebuild for mingw32-gcc 4.4

* Fri Jan 16 2009 Richard W.M. Jones <rjones@redhat.com> - 2.3.8-1
- New upstream version 2.3.8.
- Use the patches from the Fedora native package.
- Disable patented code.
- Don't build the static library.
- Use _smp_mflags.
- BR mingw32-dlfcn (not required, but uses it if installed).
- Add license file to doc section.

* Tue Jan 13 2009 Richard W.M. Jones <rjones@redhat.com> - 2.3.7-6
- Requires pkgconfig.

* Wed Sep 24 2008 Richard W.M. Jones <rjones@redhat.com> - 2.3.7-5
- Rename mingw -> mingw32.

* Mon Sep 22 2008 Daniel P. Berrange <berrange@redhat.com> - 2.3.7-4
- Import patches from rawhide  & add docs

* Sun Sep 21 2008 Richard W.M. Jones <rjones@redhat.com> - 2.3.7-3
- Depends on filesystem >= 25.

* Wed Sep 10 2008 Richard W.M. Jones <rjones@redhat.com> - 2.3.7-2
- Fix source URL.
- Remove static libraries.

* Tue Sep  9 2008 Daniel P. Berrange <berrange@redhat.com> - 2.3.7-1
- Initial RPM release
