Vendor:         Microsoft Corporation
Distribution:   Mariner
%define utempter_compat_ver 0.5.2

Summary: A privileged helper for utmp/wtmp updates
Name: libutempter
Version: 1.1.6
Release: 19%{?dist}
License: LGPLv2+
URL: https://github.com/altlinux/libutempter
# Sourece0: https://github.com/altlinux/libutempter/archive/refs/tags/1.1.6-alt2.tar.gz
Source0: https://github.com/altlinux/libutempter/archive/refs/tags/%{name}-%{version}.tar.bz2

BuildRequires: gcc

Requires(pre): shadow-utils

Provides: utempter = %{utempter_compat_ver}

%description
This library provides interface for terminal emulators such as
screen and xterm to record user sessions to utmp and wtmp files.

%package devel
Summary: Development environment for utempter
Requires: %{name} = %{version}-%{release}

%description devel
This package contains development files required to build
utempter-based software.

%prep
%setup -q

%build
make CFLAGS="$RPM_OPT_FLAGS" LDFLAGS="$RPM_LD_FLAGS" \
    libdir="%{_libdir}" libexecdir="%{_libexecdir}"

%install
make install DESTDIR="$RPM_BUILD_ROOT" libdir="%{_libdir}" libexecdir="%{_libexecdir}"

rm -f $RPM_BUILD_ROOT%{_libdir}/*.a

%pre
{
    %{_sbindir}/groupadd -g 22 -r -f utmp || :
    %{_sbindir}/groupadd -g 35 -r -f utempter || :
}

%ldconfig_scriptlets

%files
%license COPYING
%doc README
%{_libdir}/libutempter.so.0
%{_libdir}/libutempter.so.1.*
%dir %attr(755,root,utempter) %{_libexecdir}/utempter
%attr(2711,root,utmp) %{_libexecdir}/utempter/utempter

%files devel
%{_includedir}/utempter.h
%{_libdir}/libutempter.so
%{_mandir}/man3/*

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.1.6-19
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.6-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.6-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.6-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.6-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Feb 26 2018 Miroslav Lichvar <mlichvar@redhat.com> - 1.1.6-14
- build with hardening LDFLAGS (#1548717)
- remove obsolete macro and comments
- add gcc to build requirements

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.6-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Feb 03 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.1.6-12
- Switch to %%ldconfig_scriptlets

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.6-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.6-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.6-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.6-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.6-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.6-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Jul 18 2014 Tom Callaway <spot@fedoraproject.org> - 1.1.6-5
- fix license handling

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jan 24 2013 Miroslav Lichvar <mlichvar@redhat.com> - 1.1.6-2
- compile with PIE and RELRO flags (#853176)

* Thu Oct 11 2012 Miroslav Lichvar <mlichvar@redhat.com> - 1.1.6-1
- update to 1.1.6
- fix license tag
- remove unnecessary macros

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.1.5-2
- Autorebuild for GCC 4.3

* Wed Nov 07 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.1.5-1
- version upgrade
- fix #246063

* Tue Aug 21 2007 Adam Jackson <ajax@redhat.com> - 1.1.4-4
- Rebuild for build id

* Thu Jul 27 2006 Mike A. Harris <mharris@redhat.com> 1.1.4-3.fc6
- Create 'utempter' group with official allocated GID==35 (from setup package).

* Tue Jul 25 2006 Mike A. Harris <mharris@redhat.com> 1.1.4-2.fc6
- Removed usage of rpm macros inside the spec changelog (#200051)
- Removed non-UTF-8 chars from changelog.

* Mon Jul 24 2006 Mike A. Harris <mharris@redhat.com> 1.1.4-1.fc6
- Initial build of Dimitry's libutempter replacement for Fedora Core.
- Reworked the upstream spec file for Fedora packaging compliance.
- Removed static lib subpackage as we dont ship those.

* Fri Dec 09 2005 Dmitry V. Levin <ldv@altlinux.org> 1.1.4-alt1
- Enabled almost all diagnostics supported by gcc and fixed all
  issues found by gcc-3.4.4-alt3.
- Added FreeBSD support, based on patches from Gentoo/FreeBSD.
- Makefile:
  + Fixed few portability issues reported by Gentoo developers.
- libutempter: Linked with -Wl,-z,defs.
- utempter:
  + Fixed struct utmp initialization on 64-bit architectures
    with 32-bit backwards compatibility enabled (like x86_64).
  + Linked with -Wl,-z,now, i.e., marked it to tell the dynamic
    linker to resolve all symbols when the program is started.
    Suggested by Gentoo developers.

* Thu Aug 18 2005 Dmitry V. Levin <ldv@altlinux.org> 1.1.3-alt1
- Restricted list of global symbols exported by the library.
- Updated FSF postal address.

* Sun Sep 05 2004 Dmitry V. Levin <ldv@altlinux.org> 1.1.2-alt1
- Added multilib support.

* Fri Feb 14 2003 Dmitry V. Levin <ldv@altlinux.org> 1.1.1-alt1
- iface.c: don't block SIGCHLD; redefine signal handler instead.

* Mon Dec 23 2002 Dmitry V. Levin <ldv@altlinux.org> 1.1.0-alt1
- Changed soname back to libutempter.so.0, introduced versioning.

* Tue Sep 24 2002 Dmitry V. Levin <ldv@altlinux.org> 1.0.7-alt1
- If helper execution fails, try saved group ID.

* Tue May 21 2002 Dmitry V. Levin <ldv@altlinux.org> 1.0.6-alt1
- New function: utempter_set_helper.

* Mon Dec 10 2001 Dmitry V. Levin <ldv@alt-linux.org> 1.0.5-alt1
- iface.c: block SIGCHLD instead of redefine signal handler.

* Wed Nov 21 2001 Dmitry V. Levin <ldv@alt-linux.org> 1.0.4-alt1
- utempter.h: do not use "__attribute ((unused))".

* Tue Nov 13 2001 Dmitry V. Levin <ldv@alt-linux.org> 1.0.3-alt1
- Added compatibility declarations to ease upgrade of old applications.
- Added small README file.
- Corrected provides.

* Thu Nov 08 2001 Dmitry V. Levin <ldv@alt-linux.org> 1.0.2-alt1
- Added compatibility library to ease upgrade of old applications.

* Mon Nov 05 2001 Dmitry V. Levin <ldv@alt-linux.org> 1.0.1-alt1
- Indented code a bit (Solar request).

* Mon Oct 15 2001 Dmitry V. Levin <ldv@alt-linux.org> 1.0.0-alt1
- Rewritten the code completely.
- Renamed to libutempter.
- Corrected the package description.
- FHSificated (yes, there are no more {_sbindir}/utempter).
- Libificated.

* Fri Oct 12 2001 Dmitry V. Levin <ldv@altlinux.ru> 0.5.2-alt4
- {_libdir}/utempter sounds better so use it as helper directory.

* Thu Oct 11 2001 Dmitry V. Levin <ldv@altlinux.ru> 0.5.2-alt3
- Specfile cleanup.
- Owl-compatible changes:
  + added utempter group;
  + utempter binary moved to {_libdir}/utempter.d,
    owned by group utempter with 710 permissions.

* Thu Jun 28 2001 Sergie Pugachev <fd_rag@altlinux.ru> 0.5.2-alt1
- new version

* Tue Dec 05 2000 AEN <aen@logic.ru>
- build for RE

* Tue Jul 25 2000 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.5.1-4mdk
- BM

* Fri May 19 2000 Pixel <pixel@mandrakesoft.com> 0.5.1-3mdk
- add -devel
- add soname
- spec helper cleanup

* Sat Apr 08 2000 Christopher Molnar <molnarc@mandrakesoft.com> 0.5.1-2mdk
- changed group

* Tue Oct 26 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- 0.5.1
- fix utmp as group 22.
- strip utempter.
- defattr to root.

* Thu Jun 10 1999 Bernhard Rosenkraenzer <bero@mandrakesoft.com>
- Mandrake adaptions

* Fri Jun  4 1999 Jeff Johnson <jbj@redhat.com>
- ignore SIGCHLD while processing utmp.
