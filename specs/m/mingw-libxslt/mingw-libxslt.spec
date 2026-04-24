# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%{?mingw_package_header}

Name:           mingw-libxslt
Version:        1.1.43
Release: 6%{?dist}
Summary:        MinGW Windows Library providing the Gnome XSLT engine

License:        MIT
URL:            https://gitlab.gnome.org/GNOME/libxslt
Source0:        https://gitlab.gnome.org/GNOME/libxslt/-/archive/v%{version}/libxslt-v%{version}.tar.bz2
# Proposed fix for CVE-2025-7424
# https://gitlab.gnome.org/GNOME/libxslt/-/issues/139#note_2479564
Patch0:         gnome-libxslt-bug-139-apple-fix.patch
# Backport fix for CVE-2025-11731
Patch1:         https://gitlab.gnome.org/GNOME/libxslt/-/commit/fe508f201efb9ea37bfbe95413b8b28251497de3.patch
# Backport proposed fix for CVE-2025-10911
Patch2:         https://gitlab.gnome.org/GNOME/libxslt/-/merge_requests/77.patch

BuildArch:      noarch

BuildRequires:  automake autoconf libtool
BuildRequires:  make

BuildRequires:  mingw32-filesystem >= 95
BuildRequires:  mingw32-gcc
BuildRequires:  mingw32-binutils
BuildRequires:  mingw32-win-iconv
BuildRequires:  mingw32-libgcrypt
BuildRequires:  mingw32-libxml2 >= 2.7.2-3

BuildRequires:  mingw64-filesystem >= 95
BuildRequires:  mingw64-gcc
BuildRequires:  mingw64-binutils
BuildRequires:  mingw64-win-iconv
BuildRequires:  mingw64-libgcrypt
BuildRequires:  mingw64-libxml2 >= 2.7.2-3

BuildRequires:  pkgconfig

%description
This C library allows to transform XML files into other XML files
(or HTML, text, ...) using the standard XSLT stylesheet transformation
mechanism. To use it you need to have a version of libxml2 >= 2.6.27
installed. The xsltproc command is a command line interface to the XSLT engine


# Win32
%package -n mingw32-libxslt
Summary:        MinGW Windows Library providing the Gnome XSLT engine
Requires:       mingw32-libxml2 >= 2.7.2-3
Requires:       pkgconfig

%description -n mingw32-libxslt
This C library allows to transform XML files into other XML files
(or HTML, text, ...) using the standard XSLT stylesheet transformation
mechanism. To use it you need to have a version of libxml2 >= 2.6.27
installed. The xsltproc command is a command line interface to the XSLT engine

%package -n mingw32-libxslt-static
Summary:        Static version of the MinGW Windows LibXSLT library
Requires:       mingw32-libxslt = %{version}-%{release}

%description -n mingw32-libxslt-static
Static version of the MinGW Windows LibXSLT library.

# Win64
%package -n mingw64-libxslt
Summary:        MinGW Windows Library providing the Gnome XSLT engine
Requires:       mingw64-libxml2 >= 2.7.2-3
Requires:       pkgconfig

%description -n mingw64-libxslt
This C library allows to transform XML files into other XML files
(or HTML, text, ...) using the standard XSLT stylesheet transformation
mechanism. To use it you need to have a version of libxml2 >= 2.6.27
installed. The xsltproc command is a command line interface to the XSLT engine

%package -n mingw64-libxslt-static
Summary:        Static version of the MinGW Windows LibXSLT library
Requires:       mingw64-libxslt = %{version}-%{release}

%description -n mingw64-libxslt-static
Static version of the MinGW Windows LibXSLT library.


%{?mingw_debug_package}


%prep
%autosetup -n libxslt-v%{version} -p1
NOCONFIGURE=1 ./autogen.sh

%build
%mingw_configure --without-python --enable-shared --enable-static
%mingw_make_build


%install
%mingw_make_install

# Remove doc and man which duplicate stuff already in Fedora native package.
rm -r %{buildroot}%{mingw32_datadir}/gtk-doc
rm -r %{buildroot}%{mingw32_docdir}
rm -r %{buildroot}%{mingw32_mandir}
rm -r %{buildroot}%{mingw64_datadir}/gtk-doc
rm -r %{buildroot}%{mingw64_docdir}
rm -r %{buildroot}%{mingw64_mandir}

# Drop all .la files
find %{buildroot} -name "*.la" -delete


# Win32
%files -n mingw32-libxslt
%license Copyright
%{mingw32_bindir}/xslt-config
%{mingw32_bindir}/xsltproc.exe
%{mingw32_includedir}/libexslt
%{mingw32_includedir}/libxslt
%{mingw32_bindir}/libexslt-0.dll
%{mingw32_libdir}/libexslt.dll.a
%{mingw32_bindir}/libxslt-1.dll
%{mingw32_libdir}/libxslt.dll.a
%{mingw32_libdir}/pkgconfig/libexslt.pc
%{mingw32_libdir}/pkgconfig/libxslt.pc
%{mingw32_libdir}/cmake/libxslt/
%{mingw32_libdir}/xsltConf.sh

%files -n mingw32-libxslt-static
%{mingw32_libdir}/libexslt.a
%{mingw32_libdir}/libxslt.a

# Win64
%files -n mingw64-libxslt
%license Copyright
%{mingw64_bindir}/xslt-config
%{mingw64_bindir}/xsltproc.exe
%{mingw64_includedir}/libexslt
%{mingw64_includedir}/libxslt
%{mingw64_bindir}/libexslt-0.dll
%{mingw64_libdir}/libexslt.dll.a
%{mingw64_bindir}/libxslt-1.dll
%{mingw64_libdir}/libxslt.dll.a
%{mingw64_libdir}/pkgconfig/libexslt.pc
%{mingw64_libdir}/pkgconfig/libxslt.pc
%{mingw64_libdir}/cmake/libxslt/
%{mingw64_libdir}/xsltConf.sh

%files -n mingw64-libxslt-static
%{mingw64_libdir}/libexslt.a
%{mingw64_libdir}/libxslt.a


%changelog
* Fri Jan 16 2026 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.43-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Tue Jan 13 2026 Sandro Mani <manisandro@gmail.com> - 1.1.43-4
- Backport fix for CVE-2025-11731 and proposed fix for CVE-2025-10911

* Sun Jul 27 2025 Sandro Mani <manisandro@gmail.com> - 1.1.43-3
- Apply proposed fix for CVE-2025-7424

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.43-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Mar 17 2025 Sandro Mani <manisandro@gmail.com> - 1.1.43-1
- Update to 1.1.43

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.42-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.42-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Jul 06 2024 Sandro Mani <manisandro@gmail.com> - 1.1.42-1
- Update to 1.1.42

* Fri Jun 21 2024 Sandro Mani <manisandro@gmail.com> - 1.1.41-1
- Update to 1.1.41

* Sat Jun 15 2024 Sandro Mani <manisandro@gmail.com> - 1.1.40-1
- Update to 1.1.40

* Sat Jun 15 2024 Sandro Mani <manisandro@gmail.com> - 1.1.38-1
- Update to 1.1.38

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.39-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.39-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Nov 21 2023 Sandro Mani <manisandro@gmail.com> - 1.1.39-1
- Update to 1.1.39

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.38-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon May 08 2023 Sandro Mani <manisandro@gmail.com> - 1.1.38-1
- Update to 1.1.38

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.37-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Aug 30 2022 Sandro Mani <manisandro@gmail.com> - 1.1.37-1
- Update to 1.1.37

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.35-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Mar 25 2022 Sandro Mani <manisandro@gmail.com> - 1.1.35-3
- Rebuild with mingw-gcc-12

* Tue Mar 08 2022 Sandro Mani <manisandro@gmail.com> - 1.1.35-2
- Rebuild to fix missing entry point error

* Fri Feb 18 2022 Sandro Mani <manisandro@gmail.com> - 1.1.35-1
- Update to 1.1.35

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.34-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.34-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.34-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.34-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Mar 10 2020 Sandro Mani <manisandro@gmail.com> - 1.1.34-1
- Update to 1.1.34

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.33-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.33-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Jun 10 2019 David King <amigadave@amigadave.com> - 1.1.33-1
- Update to 1.1.33
- Fix CVE-2019-11068 (#1709699)

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.28-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.28-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.28-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.28-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.28-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.28-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.28-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.28-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.28-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.28-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Nov 21 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 1.1.28-1
- Update to 1.1.28

* Sat Oct 13 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 1.1.27-2
- Fix a regression in default namespace handling (GNOME BZ #684564)

* Sat Sep 22 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 1.1.27-1
- Update to 1.1.27

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.26-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Mar 18 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 1.1.26-9
- Added win64 support (contributed by Mikkel Kruse Johnsen)

* Fri Mar 09 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 1.1.26-8
- Dropped .la files

* Wed Mar 07 2012 Kalev Lember <kalevlember@gmail.com> - 1.1.26-7
- Renamed the source package to mingw-libxslt (#800931)
- Modernize the spec file
- Use mingw macros without leading underscore

* Tue Feb 28 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 1.1.26-6
- Rebuild against the mingw-w64 toolchain
- Fix compatibility with mingw-w64

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.26-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jul 06 2011 Kalev Lember <kalevlember@gmail.com> - 1.1.26-4
- Rebuilt against win-iconv

* Fri Apr 22 2011 Kalev Lember <kalev@smartlink.ee> - 1.1.26-3
- Rebuilt for pseudo-reloc version mismatch (#698827)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.26-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Sep 24 2009 Erik van Pienbroek <epienbro@fedoraproject.org. - 1.1.26-1
- Update to 1.1.26

* Mon Sep 21 2009 Erik van Pienbroek <epienbro@fedoraproject.org> - 1.1.25-2
- Fix a locking bug in 1.1.25 (patch from native libxslt package)

* Thu Sep 17 2009 Erik van Pienbroek <epienbro@fedoraproject.org> - 1.1.25-1
- Update to 1.1.25
- Dropped upstreamed CVE patch
- Dropped upstreamed mingw32 patches
- Added a patch to never use pthreads even if it's available
- Automatically generate debuginfo subpackages

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.24-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jun 11 2009 Erik van Pienbroek <epienbro@fedoraproject.org> - 1.1.24-8
- Resolve FTBFS

* Fri May 22 2009 Erik van Pienbroek <epienbro@fedoraproject.org> - 1.1.24-7
- Use %%global instead of %%define
- Dropped the reference to the multilib patch as it isn't used for MinGW
- Fixed dangling-relative-symlink rpmlint warning

* Sat May  9 2009 Erik van Pienbroek <epienbro@fedoraproject.org> - 1.1.24-6
- Added some more comments in the .spec file
- Added -static subpackage
- Dropped the 'gzip ChangeLog' line as the ChangeLog isn't bundled anyway
- Fixed %%defattr line

* Fri Feb 20 2009 Richard W.M. Jones <rjones@redhat.com> - 1.1.24-5
- Rebuild for mingw32-gcc 4.4

* Fri Feb  6 2009 Richard W.M. Jones <rjones@redhat.com> - 1.1.24-4
- Include license file.

* Fri Jan 23 2009 Richard W.M. Jones <rjones@redhat.com> - 1.1.24-3
- Use _smp_mflags.
- Rebuild libtool.
- +BRs dlfcn and iconv.

* Sat Oct 25 2008 Richard W.M. Jones <rjones@redhat.com> - 1.1.24-2
- Initial RPM release.
