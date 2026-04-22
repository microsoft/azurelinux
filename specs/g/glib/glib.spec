# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Summary:	A library of handy utility functions
Name:		glib
Epoch:		1
Version:	1.2.10
Release: 77%{?dist}
License:	LGPL-2.0-or-later
URL:		http://www.gtk.org/
Source0:	https://ftp.gnome.org/pub/gnome/sources/glib/1.2/glib-%{version}.tar.gz
BuildRequires:	coreutils
BuildRequires:	gcc
BuildRequires:	libtool
BuildRequires:	make

# We need newer versions of config.guess and config.sub to be able to
# handle exotic new architectures (at the time this software was released)
# such as x86_64
#
# http://git.savannah.gnu.org/gitweb/?p=config.git;a=blob_plain;f=config.guess;hb=HEAD
Source1:	config.guess
# http://git.savannah.gnu.org/gitweb/?p=config.git;a=blob_plain;f=config.sub;hb=HEAD
Source2:	config.sub

# Suppress warnings about varargs macros for -pedantic
Patch1: glib-1.2.10-isowarning.patch
Patch2: glib-1.2.10-gcc34.patch
Patch3: glib-1.2.10-underquoted.patch
Patch4: glib-1.2.10-no_undefined.patch
# http://bugzilla.redhat.com/222296
Patch5: glib-1.2.10-multilib.patch
# Fix unused direct shared library dependency on libgmodule for libgthread
Patch6: glib-1.2.10-unused-dep.patch
# Avoid having to run autotools at build time
Patch7: glib-1.2.10-autotools.patch
# Use format strings properly
Patch8: glib-1.2.10-format.patch
# Workaround for different inline semantics between GNU89 and C99
Patch9: glib-1.2.10-gcc5.patch
# gcc9: '__const__' is not an asm qualifier
Patch10: glib-1.2.10-gcc9.patch
# C99 compiler support
Patch11: glib-1.2.10-c99.patch

%description
GLib is a handy library of utility functions. This C library is
designed to solve some portability problems and provide other useful
functionality that most programs require.

%package devel
Summary: Libraries and header files for %{name} development 
Requires: %{name} = %{epoch}:%{version}-%{release}
Requires: pkgconfig

%description devel
%{summary}.

%prep
%setup -q 

%patch -P  1 -p1 -b .isowarning
%patch -P  2 -p1 -b .gcc34
%patch -P  3 -p1 -b .underquoted
%patch -P  4 -p1 -b .no_undefined
%patch -P  5 -p1 -b .multilib
%patch -P  6 -p1 -b .unused-dep
%patch -P  7 -p0 -b .autotools
%patch -P  8 -p0 -b .format
%patch -P  9 -p0 -b .gcc5
%patch -P 10 -p0 -b .gcc9
%patch -P 11 -p1 -b .c99

# The original config.{guess,sub} do not work on x86_64, aarch64 etc.
#
cp -p %{SOURCE1} %{SOURCE2} .
chmod -c +x config.{guess,sub}

%build
%if 0%{?set_build_flags:1}
%global build_type_safety_c 0
%set_build_flags
%endif

LIBTOOL=%{_bindir}/libtool \
%configure --disable-static

%make_build LIBTOOL=%{_bindir}/libtool

%install
%make_install \
	INSTALL="install -p" \
	LIBTOOL=%{_bindir}/libtool

# libgmodule-1.2.so.0* missing eXecute bit
chmod -c a+x %{buildroot}%{_libdir}/lib*.so*

## Unpackaged files
# info
rm -rf %{buildroot}%{_infodir}
# .la fies... die die die.
rm -rf %{buildroot}%{_libdir}/lib*.la
# despite use of --disable-static, delete static libs that get built anyway
rm -rf %{buildroot}%{_libdir}/lib*.a

%check
make check LIBTOOL=%{_bindir}/libtool

%if (0%{?rhel} && 0%{?rhel} <= 7) || (0%{?fedora} && 0%{?fedora} <= 27)
# ldconfig scriptlets replaced by RPM File Triggers from Fedora 28
%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig
%endif

%files
%license COPYING
%doc AUTHORS ChangeLog NEWS README
%{_libdir}/lib*.so.*

%files devel
%{_bindir}/glib-config
%{_libdir}/lib*.so
%{_libdir}/glib/
%{_libdir}/pkgconfig/*
%{_includedir}/*
%{_mandir}/man1/*
%{_datadir}/aclocal/*

%changelog
* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.2.10-76
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.2.10-75
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.2.10-74
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.2.10-73
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.2.10-72
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Aug 16 2023 Florian Weimer <fweimer@redhat.com> - 1:1.2.10-71
- Set build_type_safety_c to 0 (#2167383)

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.2.10-70
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun  6 2023 Paul Howarth <paul@city-fan.org> - 1:1.2.10-69
- Avoid use of deprecated patch syntax
- Drop workaround for unavailable make_build macro on EL-6

* Mon Feb  6 2023 Paul Howarth <paul@city-fan.org> - 1:1.2.10-68
- Tweak C89 setting to work for older releases without %%set_build_flags, or
  with %%set_build_flags that does not set $CC (e.g. EL-7)
- Use %%license unconditionally
- Use SPDX-format license tag

* Mon Feb 06 2023 Florian Weimer <fweimer@redhat.com> - 1:1.2.10-67
- Build in C89 mode (#2167383)

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.2.10-66
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.2.10-65
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.2.10-64
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.2.10-63
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.2.10-62
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.2.10-61
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 22 2020 Paul Howarth <paul@city-fan.org> - 1:1.2.10-60
- The config.guess and config.sub scripts are no longer packaged with rpm 4.16
  onwards so we have to supply them ourselves
- Fix source URL to point to somewhere that still works
- Fix EL-6 compatibility (%%make_build only defined from EL-7, F-21 onwards)

* Wed Jul 22 2020 Tom Stellard <tstellar@redhat.com> - 1:1.2.10-59
- Use make macros
- https://fedoraproject.org/wiki/Changes/UseMakeBuildInstallMacro

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.2.10-58
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Sep  9 2019 Florian Weimer <fweimer@redhat.com> - 1:1.2.10-57
- Fix building in C99 mode

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.2.10-56
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb  1 2019 Paul Howarth <paul@city-fan.org> - 1:1.2.10-55
- Fix compilation error on ix86 with GCC 9

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.2.10-54
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.2.10-53
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb  7 2018 Paul Howarth <paul@city-fan.org> - 1:1.2.10-52
- ldconfig scriptlets replaced by RPM File Triggers from Fedora 28
- Drop legacy BuildRoot: and Group: tags
- Drop redundant explicit buildroot cleaning
- Specify all explicitly-used build requirements
- Preserve timestamps of unmodified upstream files that are shipped

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.2.10-51
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.2.10-50
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.2.10-49
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.2.10-48
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.2.10-47
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.2.10-46
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Mar 16 2015 Than Ngo <than@redhat.com> - 1:1.2.10-45
- Bump the release number of this package so that koji-shadow
  can rebuild it against new gcc on secondary arch. 

* Tue Feb 10 2015 Paul Howarth <paul@city-fan.org> - 1:1.2.10-44
- Work around different inline semantics between GNU89 and C99
- Drop %%defattr, redundant since rpm 4.4
- Use %%license where possible

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.2.10-43
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.2.10-42
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Nov 21 2013 Paul Howarth <paul@city-fan.org> - 1:1.2.10-41
- Use format strings properly

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.2.10-40
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri May 10 2013 Paul Howarth <paul@city-fan.org> - 1:1.2.10-39
- Avoid having to run autotools at build time (#961283)

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.2.10-38
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 27 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.2.10-37
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jan  5 2012 Paul Howarth <paul@city-fan.org> 1:1.2.10-36
- rebuilt for gcc 4.7

* Wed Oct 26 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> 1:1.2.10-35
- rebuilt for glibc bug#747377

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> 1:1.2.10-34
- rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> 1:1.2.10-33
- rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Apr 17 2009 Paul Howarth <paul@city-fan.org> 1:1.2.10-32
- remove redundant linkage of libgmodule to libgthread
- cosmetic spec changes

* Wed Feb 25 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> 1:1.2.10-31
- rebuild for pkgconfig deps

* Wed Oct  1 2008 Patrice Dumas <pertusus@free.fr> 1:1.2.10-30
- copy config.* from rpm directory, those shipped are too old. Should
  fix #462650.

* Mon Feb 11 2008 Rex Dieter <rdieter@fedoraproject.org> 1:1.2.10-29 
- respin (gcc43)

* Tue Aug 21 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 1:1.2.10-28
- respin (buildID)

* Sat Aug 11 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 1:1.2.10-27
- License: LGPLv2+

* Thu Jan 11 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 1:1.2.10-26
- revert libtool-related breakage 

* Thu Jan 11 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 1:1.2.10-25
- cleanup libtool hacks

* Thu Jan 11 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 1:1.2.10-24
- multilib patch (#222296)

* Tue Aug 29 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1:1.2.10-23
- fc6 respin

* Wed Aug 09 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1:1.2.10-22
- fc6 respin

* Thu May 04 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1:1.2.10-21
- fix undefined symbols in libgmodule,libgthread

* Wed Apr 12 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1:1.2.10-20
- cleanup %%description
- libgmodule-1.2.so.0* missing eXecute bit
- utf-8'ize specfile

* Thu Apr 06 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1:1.2.10-19
- cleanup for Extras
- -devel: Requires: pkgconfig

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1:1.2.10-18.2.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1:1.2.10-18.2.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Tue Jan  3 2006 Jesse Keating <jkeating@redhat.com> 1:1.2.10-18.2
- rebuilt again

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Mon Nov 21 2005 Matthias Clasen <mclasen@redhat.com> 1:1.2.10-18
- Make sure all libraries are stripped

* Mon Nov  7 2005 Matthias Clasen <mclasen@redhat.com> 1:1.2.10-17
- Remove .la files and static libs from the -devel package.

* Wed Mar  2 2005 Matthias Clasen <mclasen@redhat.com> 1:1.2.10-16
- Rebuild with gcc4

* Mon Aug  9 2004 Tim Waugh <twaugh@redhat.com> 1:1.2.10-15
- Fixed underquoted m4 definitions.

* Mon Jun 21 2004 Matthias Clasen <mclasen@redhat.com> 1:1.2.10-14
- Make it build with gcc 3.4

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Sun Jun  8 2003 Tim Powers <timp@redhat.com> 1:1.2.10-11.1
- build for RHEL

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Jun  3 2003 Jeff Johnson <jbj@redhat.com>
- add explicit epoch's where needed.

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Fri Nov 29 2002 Tim Powers <timp@redhat.com> 1:1.2.10-9
- remove unpackaged files from the buildroot

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Sat Jul 21 2001 Owen Taylor <otaylor@redhat.com>
- Add #pragma GCC system_header to supress warnings when in -pedantic
  mode. (41271)

* Tue Jul 10 2001 Trond Eivind Glomsrod <teg@redhat.com>
- s/Copyright/License/
- Make the devel subpackage depend on the main package

* Sun Jun 24 2001 Elliot Lee <sopwith@redhat.com>
- Bump release + rebuild.

* Sun Apr 22 2001  <jrb@redhat.com>
- Include pc files.

* Tue Apr 17 2001 Jonathan Blandford <jrb@redhat.com>
- Version 1.2.10

* Mon Mar 05 2001 Owen Taylor <otaylor@redhat.com>
- Version 1.2.9

* Wed Feb 28 2001 Owen Taylor <otaylor@redhat.com>
- Version 1.2.9pre3

* Tue Feb 27 2001 Owen Taylor <otaylor@redhat.com>
- Version 1.2.9pre2

* Tue Feb 13 2001 Owen Taylor <otaylor@redhat.com>
- Version 1.2.9pre1

* Sat Oct 28 2000 Owen Taylor <otaylor@redhat.com>
- Add patch to suppress warnings from GCC by using
  C99 standard varargs macros

* Fri Aug 11 2000 Jonathan Blandford <jrb@redhat.com>
- Up Epoch and release

* Thu Jul 13 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Mon Jun 19 2000 Preston Brown <pbrown@redhat.com>
- FHS paths

* Thu May 25 2000 Owen Taylor <otaylor@redhat.com>
- Version 1.2.8

* Mon May  1 2000 Matt Wilson <msw@redhat.com>
- version 1.2.7

* Fri Feb 04 2000 Owen Taylor <otaylor@redhat.com>
- Added fixes from stable branch of CVS

* Thu Oct 7  1999 Owen Taylor <otaylor@redhat.com>
- version 1.2.6

* Fri Sep 24 1999 Owen Taylor <otaylor@redhat.com>
- version 1.2.5

* Fri Sep 17 1999 Owen Taylor <otaylor@redhat.com>
- version 1.2.4

* Mon Jun 7 1999 Owen Taylor <otaylor@redhat.com>
- version 1.2.3

* Thu Mar 25 1999 Michael Fulbright <drmike@redhat.com>
- version 1.2.1

* Fri Feb 26 1999 Michael Fulbright <drmike@redhat.com>
- Version 1.2

* Thu Feb 25 1999 Michael Fulbright <drmike@redhat.com>
- version 1.2.0pre1

* Tue Feb 23 1999 Cristian Gafton <gafton@redhat.com>
- new description tags 

* Sun Feb 21 1999 Michael Fulbright <drmike@redhat.com>
- removed libtoolize from %%build

* Thu Feb 11 1999 Michael Fulbright <drmike@redhat.com>
- added libgthread to file list

* Fri Feb 05 1999 Michael Fulbright <drmike@redhat.com>
- version 1.1.15

* Wed Feb 03 1999 Michael Fulbright <drmike@redhat.com>
- version 1.1.14

* Mon Jan 18 1999 Michael Fulbright <drmike@redhat.com>
- version 1.1.13

* Wed Jan 06 1999 Michael Fulbright <drmike@redhat.com>
- version 1.1.12

* Wed Dec 16 1998 Michael Fulbright <drmike@redhat.com>
- updated in preparation for the GNOME freeze

* Mon Apr 13 1998 Marc Ewing <marc@redhat.com>
- Split out glib package
