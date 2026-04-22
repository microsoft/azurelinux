# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%{?mingw_package_header}

Name:      mingw-gettext
Version:   0.25.1
Release: 2%{?dist}
Summary:   GNU libraries and utilities for producing multi-lingual messages

License:   GPL-2.0-or-later AND LGPL-2.0-or-later
URL:       http://www.gnu.org/software/gettext/
Source0:   https://ftp.gnu.org/pub/gnu/gettext/gettext-%{version}.tar.xz

BuildArch: noarch

BuildRequires: make
BuildRequires: mingw32-filesystem >= 95
BuildRequires: mingw32-gcc
BuildRequires: mingw32-gcc-c++
BuildRequires: mingw32-binutils
BuildRequires: mingw32-win-iconv
BuildRequires: mingw32-termcap

BuildRequires: mingw64-filesystem >= 95
BuildRequires: mingw64-gcc
BuildRequires: mingw64-gcc-c++
BuildRequires: mingw64-binutils
BuildRequires: mingw64-win-iconv
BuildRequires: mingw64-termcap

# Possible extra BRs.  These are used if available, but
# not required just for building.
#BuildRequires: mingw32-dlfcn
#BuildRequires: mingw32-libxml2
#BuildRequires: mingw32-expat
#BuildRequires: mingw32-glib2


%description
MinGW Windows Gettext library


# Win32
%package -n mingw32-gettext
Summary:         GNU libraries and utilities for producing multi-lingual messages

%description -n mingw32-gettext
MinGW Windows Gettext library

%package -n mingw32-gettext-static
Summary:        Static version of the MinGW Windows Gettext library
Requires:       mingw32-gettext = %{version}-%{release}

%description -n mingw32-gettext-static
Static version of the MinGW Windows Gettext library.

# Win64
%package -n mingw64-gettext
Summary:         GNU libraries and utilities for producing multi-lingual messages

%description -n mingw64-gettext
MinGW Windows Gettext library

%package -n mingw64-gettext-static
Summary:        Static version of the MinGW Windows Gettext library
Requires:       mingw64-gettext = %{version}-%{release}

%description -n mingw64-gettext-static
Static version of the MinGW Windows Gettext library.


%{?mingw_debug_package}


%prep
%autosetup -p1 -n gettext-%{version}

%build
%mingw_configure            \
    --disable-java          \
    --disable-native-java   \
    --disable-csharp        \
    --enable-static         \
    --enable-threads=win32  \
    --without-emacs         \
    --disable-openmp
%mingw_make_build


%install
%mingw_make_install

rm -f %{buildroot}%{mingw32_datadir}/locale/locale.alias
rm -f %{buildroot}%{mingw32_libdir}/charset.alias

rm -f %{buildroot}%{mingw64_datadir}/locale/locale.alias
rm -f %{buildroot}%{mingw64_libdir}/charset.alias

# Remove documentation - already available in base gettext-devel.
rm -rf %{buildroot}%{mingw32_mandir}
rm -rf %{buildroot}%{mingw32_docdir}
rm -rf %{buildroot}%{mingw32_infodir}

rm -rf %{buildroot}%{mingw64_mandir}
rm -rf %{buildroot}%{mingw64_docdir}
rm -rf %{buildroot}%{mingw64_infodir}

# Drop some useless tools
rm -rf %{buildroot}%{mingw32_libdir}/gettext
rm -rf %{buildroot}%{mingw64_libdir}/gettext

# Drop all .la files and .a files
find %{buildroot} -name "*.la" -delete
rm %{buildroot}%{mingw32_libdir}/libgettextlib.a
rm %{buildroot}%{mingw32_libdir}/libgettextsrc.a
rm %{buildroot}%{mingw64_libdir}/libgettextlib.a
rm %{buildroot}%{mingw64_libdir}/libgettextsrc.a

# Drop javaversion.class since it's a binary blob (RHBZ#2294881)
rm %{buildroot}%{mingw32_datadir}/gettext/javaversion.class
rm %{buildroot}%{mingw64_datadir}/gettext/javaversion.class

%mingw_find_lang %{name} --all-name


# Win32
%files -n mingw32-gettext -f mingw32-%{name}.lang
%license COPYING
%{mingw32_bindir}/autopoint
%{mingw32_bindir}/envsubst.exe
%{mingw32_bindir}/gettext.exe
%{mingw32_bindir}/gettext.sh
%{mingw32_bindir}/gettextize
%{mingw32_bindir}/libasprintf-0.dll
%{mingw32_bindir}/libgettextlib-0-25-1.dll
%{mingw32_bindir}/libgettextpo-0.dll
%{mingw32_bindir}/libgettextsrc-0-25-1.dll
%{mingw32_bindir}/libintl-8.dll
%{mingw32_bindir}/libtextstyle-0.dll
%{mingw32_bindir}/msg*.exe
%{mingw32_bindir}/ngettext.exe
%{mingw32_bindir}/recode-sr-latin.exe
%{mingw32_bindir}/xgettext.exe
%{mingw32_includedir}/autosprintf.h
%{mingw32_includedir}/gettext-po.h
%{mingw32_includedir}/libintl.h
%{mingw32_includedir}/textstyle.h
%{mingw32_includedir}/textstyle/stdbool.h
%{mingw32_includedir}/textstyle/version.h
%{mingw32_includedir}/textstyle/woe32dll.h
%{mingw32_libdir}/libasprintf.dll.a
%{mingw32_libdir}/libgettextlib.dll.a
%{mingw32_libdir}/libgettextpo.dll.a
%{mingw32_libdir}/libgettextsrc.dll.a
%{mingw32_libdir}/libintl.dll.a
%{mingw32_libdir}/libtextstyle.dll.a
%dir %{mingw32_libexecdir}/gettext/
%{mingw32_libexecdir}/gettext/cldr-plurals.exe
%{mingw32_libexecdir}/gettext/hostname.exe
%{mingw32_libexecdir}/gettext/project-id
%{mingw32_libexecdir}/gettext/urlget.exe
%{mingw32_libexecdir}/gettext/user-email
%{mingw32_datadir}/gettext/
%{mingw32_datadir}/gettext-%{version}/
%{mingw32_datadir}/aclocal/nls.m4

%files -n mingw32-gettext-static
%{mingw32_libdir}/libasprintf.a
%{mingw32_libdir}/libgettextpo.a
%{mingw32_libdir}/libintl.a
%{mingw32_libdir}/libtextstyle.a

# Win64
%files -n mingw64-gettext -f mingw64-%{name}.lang
%license COPYING
%{mingw64_bindir}/autopoint
%{mingw64_bindir}/envsubst.exe
%{mingw64_bindir}/gettext.exe
%{mingw64_bindir}/gettext.sh
%{mingw64_bindir}/gettextize
%{mingw64_bindir}/libasprintf-0.dll
%{mingw64_bindir}/libgettextlib-0-25-1.dll
%{mingw64_bindir}/libgettextpo-0.dll
%{mingw64_bindir}/libgettextsrc-0-25-1.dll
%{mingw64_bindir}/libintl-8.dll
%{mingw64_bindir}/libtextstyle-0.dll
%{mingw64_bindir}/msg*.exe
%{mingw64_bindir}/ngettext.exe
%{mingw64_bindir}/recode-sr-latin.exe
%{mingw64_bindir}/xgettext.exe
%{mingw64_includedir}/autosprintf.h
%{mingw64_includedir}/gettext-po.h
%{mingw64_includedir}/libintl.h
%{mingw64_includedir}/textstyle.h
%{mingw64_includedir}/textstyle/stdbool.h
%{mingw64_includedir}/textstyle/version.h
%{mingw64_includedir}/textstyle/woe32dll.h
%{mingw64_libdir}/libasprintf.dll.a
%{mingw64_libdir}/libgettextlib.dll.a
%{mingw64_libdir}/libgettextpo.dll.a
%{mingw64_libdir}/libgettextsrc.dll.a
%{mingw64_libdir}/libintl.dll.a
%{mingw64_libdir}/libtextstyle.dll.a
%dir %{mingw64_libexecdir}/gettext/
%{mingw64_libexecdir}/gettext/cldr-plurals.exe
%{mingw64_libexecdir}/gettext/hostname.exe
%{mingw64_libexecdir}/gettext/project-id
%{mingw64_libexecdir}/gettext/urlget.exe
%{mingw64_libexecdir}/gettext/user-email
%{mingw64_datadir}/gettext/
%{mingw64_datadir}/gettext-%{version}/
%{mingw64_datadir}/aclocal/nls.m4

%files -n mingw64-gettext-static
%{mingw64_libdir}/libasprintf.a
%{mingw64_libdir}/libgettextpo.a
%{mingw64_libdir}/libintl.a
%{mingw64_libdir}/libtextstyle.a


%changelog
* Sun Jul 27 2025 Sandro Mani <manisandro@gmail.com> - 0.25.1-1
- Update to 0.25.1

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.25-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri May 16 2025 Sandro Mani <manisandro@gmail.com> - 0.25-1
- Update to 0.25

* Tue Mar 11 2025 Sandro Mani <manisandro@gmail.com> - 0.24-1
- Update to 0.24

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.23.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Jan 15 2025 Sandro Mani <manisandro@gmail.com> - 0.23.1-1
- Update to 0.23.1

* Wed Dec 18 2024 Sandro Mani <manisandro@gmail.com> - 0.23-1
- Update to 0.23

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.22.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jul 01 2024 Richard W.M. Jones <rjones@redhat.com> - 0.22.5-2
- Drop javaversion.class files (RHBZ#2294881)

* Mon Mar 04 2024 Sandro Mani <manisandro@gmail.com> - 0.22.5-1
- Update to 0.22.5

* Thu Feb 15 2024 Sandro Mani <manisandro@gmail.com> - 0.22.4-1
- Update to 0.22.4

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.22-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.22-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.22-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jun 28 2023 Sandro Mani <manisandro@gmail.com> - 0.22-1
- Update to 0.22

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.21.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Oct 20 2022 Sandro Mani <manisandro@gmail.com> - 0.21.1-1
- Update to 0.21.1

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.21-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Mar 25 2022 Sandro Mani <manisandro@gmail.com> - 0.21-5
- Rebuild with mingw-gcc-12

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.21-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.21-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.21-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Aug 03 2020 Sandro Mani <manisandro@gmail.com> - 0.21.0-1
- Update to 0.21.0

* Tue Jul 28 2020 Sandro Mani <manisandro@gmail.com> - 0.20.2-3
- Add gettext-printf_collision.patch

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.20.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Apr 16 2020 Sandro Mani <manisandro@gmail.com> - 0.20.2-1
- Update to 0.20.2

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.20.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Oct 08 2019 Sandro Mani <manisandro@gmail.com> - 0.20.1-2
- Rebuild (Changes/Mingw32GccDwarf2)

* Tue Aug 13 2019 Fabiano Fidêncio <fidencio@redhat.com> - 0.20.1-1
- Update the sources accordingly to its native counter part, rhbz#1740721

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.19.7-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.19.7-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.19.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.19.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.19.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.19.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue May 03 2016 Kalev Lember <klember@redhat.com> - 0.19.7-1
- Update to 0.19.7

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.19.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.19.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jan  1 2015 Erik van Pienbroek <epienbro@fedoraproject.org> - 0.19.4-1
- Update to 0.19.4

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.18.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Mar 29 2014 Kalev Lember <kalevlember@gmail.com> - 0.18.3.2-1
- Update to 0.18.3.2

* Sat Sep  7 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 0.18.3.1-1
- Update to 0.18.3.1

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.18.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Jul 13 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 0.18.3-1
- Update to 0.18.3
- Dropped upstreamed patch

* Sat Jun 15 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 0.18.2.1-3
- Fix FTBFS due to invalid use of cdecl

* Sat Jun 15 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 0.18.2.1-2
- Rebuild to resolve InterlockedCompareExchange regression in mingw32 libraries

* Sat May  4 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 0.18.2.1-1
- Update to 0.18.2.1

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.18.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jan  4 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 0.18.2-1
- Update to 0.18.2
- Removed all hacks as they're not needed any more

* Thu Dec  6 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 0.18.1.1-11
- Fix the build on RHEL6 (too old libtool)
- Minor cleanup

* Sun Jul 22 2012 Kalev Lember <kalevlember@gmail.com> - 0.18.1.1-10
- Fix message catalog split to subpackages (#842166)

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.18.1.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Mar 10 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 0.18.1.1-8
- Added win64 support

* Thu Mar 08 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 0.18.1.1-7
- Dropped .la files

* Tue Mar 06 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 0.18.1.1-6
- Renamed the source package to mingw-gettext (RHBZ #800387)
- Use mingw macros without leading underscore

* Mon Feb 27 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 0.18.1.1-5
- Rebuild against the mingw-w64 toolchain
- Added a patch to fix compatibility with mingw-w64

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.18.1.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jul  6 2011 Erik van Pienbroek <epienbro@fedoraproject.org> - 0.18.1.1-3
- Rebuild again to fix incomplete dependencies

* Wed Jul  6 2011 Erik van Pienbroek <epienbro@fedoraproject.org> - 0.18.1.1-2
- Rebuild against win-iconv

* Mon May 23 2011 Kalev Lember <kalev@smartlink.ee> - 0.18.1.1-1
- Update to 0.18.1.1
- Spec cleanup
- Split debug symbols in -debuginfo subpackage

* Mon May 23 2011 Kalev Lember <kalev@smartlink.ee> - 0.17-16
- Removed html documentation and info pages

* Wed Apr 27 2011 Erik van Pienbroek <epienbro@fedoraproject.org> - 0.17.15
- Dropped the proxy-libintl pieces as the upstream gtk+ win32 maintainers
  also decided to drop it and it's causing more harm than good

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.17-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Oct 16 2010 Erik van Pienbroek <epienbro@fedoraproject.org> - 0.17-13
- Replaced the libintl import library with a small wrapper library in order
  to let other binaries have a soft-dependency on libintl-8.dll as proposed
  on the fedora-mingw mailing list

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.17-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Apr  3 2009 Erik van Pienbroek <epienbro@fedoraproject.org> - 0.17-11
- Added -static subpackage

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.17-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Feb 20 2009 Richard W.M. Jones <rjones@redhat.com> - 0.17-9
- Rebuild for mingw32-gcc 4.4

* Fri Jan 23 2009 Richard W.M. Jones <rjones@redhat.com> - 0.17-8
- Use find_lang macro.

* Fri Jan 16 2009 Richard W.M. Jones <rjones@redhat.com> - 0.17-7
- Remove the manpages - already available in base Fedora gettext-devel.
- Use _smp_mflags for build.
- Added list of potential BRs.
- Added license file to doc section.

* Fri Oct 31 2008 Richard W.M. Jones <rjones@redhat.com> - 0.17-6
- Add fix for undefined Gnulib symbols (Farkas Levente).
- Rebuild against mingw32-termcap / libtermcap.

* Wed Sep 24 2008 Richard W.M. Jones <rjones@redhat.com> - 0.17-5
- Rename mingw -> mingw32.

* Thu Sep 11 2008 Daniel P. Berrange <berrange@redhat.com> - 0.17-4
- Disable emacs lisp file install

* Thu Sep 11 2008 Richard W.M. Jones <rjones@redhat.com> - 0.17-3
- Remove static libraries.

* Thu Sep  4 2008 Richard W.M. Jones <rjones@redhat.com> - 0.17-2
- Use RPM macros from mingw-filesystem.

* Tue Sep  2 2008 Daniel P. Berrange <berrange@redhat.com> - 0.17-1
- Initial RPM release, largely based on earlier work from several sources.
