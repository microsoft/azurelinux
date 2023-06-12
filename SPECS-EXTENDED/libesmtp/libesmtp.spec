Vendor:         Microsoft Corporation
Distribution:   Mariner
%define plugindir %{_libdir}/esmtp-plugins

Summary:        SMTP client library
Name:           libesmtp
Version:        1.0.6
Release:        21%{?dist}
License:        LGPLv2+
#Source0:        https://github.com/libesmtp/libESMTP/archive/refs/tags/v1.0.6.tar.gz
Source:         https://github.com/libesmtp/libESMTP/archive/refs/tags/%{name}-%{version}.tar.bz2
URL:            https://github.com/libesmtp
BuildRequires:  gcc
BuildRequires:  openssl-devel pkgconfig autoconf automake libtool
Patch0: libesmtp-1.0.6-openssl-1.1.patch
Patch1: CVE-2019-19977-avoid-stach-overrwrite-6.patch

%description
LibESMTP is a library to manage posting (or submission of) electronic
mail using SMTP to a preconfigured Mail Transport Agent (MTA) such as
Exim. It may be used as part of a Mail User Agent (MUA) or another
program that must be able to post electronic mail but where mail
functionality is not the program's primary purpose.

%package devel
Summary: Headers and development libraries for libESMTP
# example file is under the GPLv2+
License: LGPLv2+ and GPLv2+
Requires: %{name} = %{version}-%{release}, openssl-devel

%description devel
LibESMTP is a library to manage posting (or submission of) electronic
mail using SMTP to a preconfigured Mail Transport Agent (MTA) such as
Exim.

The libesmtp-devel package contains headers and development libraries
necessary for building programs against libesmtp.

%prep 
%autosetup -p1

autoreconf -fi

# Keep rpmlint happy about libesmtp-debuginfo...
chmod a-x htable.c

%build

if pkg-config openssl ; then
  export CFLAGS="$CFLAGS $RPM_OPT_FLAGS `pkg-config --cflags openssl`"
  export LDFLAGS="$LDFLAGS `pkg-config --libs-only-L openssl`"
fi
%configure --with-auth-plugin-dir=%{plugindir} --enable-pthreads \
  --enable-require-all-recipients --enable-debug \
  --enable-etrn --disable-isoc --disable-more-warnings --disable-static
make %{?_smp_mflags}
cat << "EOF" > libesmtp.pc
prefix=%{_prefix}
exec_prefix=%{_prefix}
libdir=%{_libdir}
includedir=%{_includedir}

Name: libESMTP
Version: %{version}
Description: SMTP client library.
Requires: openssl
Libs: -pthread -L${libdir} -lesmtp
Cflags:
EOF

cat << "EOF" > libesmtp-config
#! /bin/sh
exec pkg-config "$@" libesmtp
EOF

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install INSTALL='install -p'
rm $RPM_BUILD_ROOT/%{_libdir}/*.la
rm $RPM_BUILD_ROOT/%{_libdir}/esmtp-plugins/*.la
install -p -m644 -D libesmtp.pc $RPM_BUILD_ROOT%{_libdir}/pkgconfig/libesmtp.pc


%ldconfig_scriptlets

%files
%doc AUTHORS COPYING.LIB NEWS Notes README
%{_libdir}/libesmtp.so.*
%{plugindir}

%files devel
%doc examples COPYING
%{_bindir}/libesmtp-config
%{_prefix}/include/*
%{_libdir}/libesmtp.so
%{_libdir}/pkgconfig/libesmtp.pc

%changelog
* Tue Jun 6 2023 Dan Streetman <ddstreet@ieee.org> - 1.0.6-21
- Fix buffer overflow for CVE-2019-19977
- Change from %setup to %autosetup
- License verified

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.0.6-20
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.6-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.6-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.6-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 21 2018 Pawel Salek <salek@kth.se> - 1.0.6-16
- apply the ssl patch from https://bugzilla.redhat.com/show_bug.cgi?id=1483350

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.6-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.6-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.6-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.6-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.6-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.6-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.6-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.6-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.6-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.6-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Dec  3 2010 Pawel Salek <pawsa@theochem.kth.se> - 1.0.6-1
- update to upstream 1.0.6

* Sat Jun 12 2010 Pawel Salek <pawsa@theochem.kth.se> - 1.0.4-14

- fix bug 599428: use 'version' macro instead of '_version'.
- Use SSL patch by Ludwig Nussel of SUSE (bugzilla att id 399130).

* Tue Mar  9 2010 Pawel Salek <pawsa@theochem.kth.se> - 1.0.4-13
- fix CVE-2009-2408 (#571817).

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 1.0.4-12
- rebuilt with new openssl

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.4-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.4-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Jan 17 2009 Tomas Mraz <tmraz@redhat.com> - 1.0.4-9
- rebuild with new openssl

* Sat Nov  1 2008 Manuel "lonely wolf" Wolfshant <wolfy@fedoraproject.org> - 1.0.4-8
- do not package libtool files from the plugin directory

* Fri Apr  4 2008 Pawel Salek <pawsa@theochem.kth.se> - 1.0.4-7
- attempt at multilib support (#342011).

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.0.4-6
- Autorebuild for GCC 4.3

* Wed Dec 05 2007 Release Engineering <rel-eng at fedoraproject dot org> - 1.0.4-5
 - Rebuild for deps

* Sun Nov 18 2007 Patrice Dumas <pertusus@free.fr> - 1.0.4-4
- use --disable-static

* Thu Nov 15 2007 Pawel Salek <pawsa@theochem.kth.se> - 1.0.4-3
- drop static libs as suggested in bug 377731.

* Mon Sep 11 2006 Pawel Salek <pawsa@theochem.kth.se> - 1.0.4-2
- rebuild for FC6.

* Fri Mar 24 2006 Pawel Salek <pawsa@theochem.kth.se> - 1.0.4-1
- Update to 1.0.4 - redo build and ssl patches.

* Wed Mar  1 2006 Pawel Salek <pawsa@theochem.kth.se> - 1.0.3r1-8
- Rebuild for Fedora Extras 5

* Sun Dec  4 2005 Pawel Salek <pawsa@theochem.kth.se> - 1.0.3r1-7
- Fix bug 173332 completely, including licence issues.

* Thu Nov 17 2005 Pawel Salek <pawsa@theochem.kth.se> - 1.0.3r1-6
- fix #173332.

* Tue Nov 15 2005 Dan Williams <dcbw@redhat.com> - 1.0.3r1-5
- rebuild against newer crypto libs

* Wed Oct 19 2005 Pawel Salek <pawsa@theochem.kth.se> - 1.0.3r1-4
- fix crashes on certificates with subjectAltName extension. Fix #166844.

* Sun Jun 12 2005 Pawel Salek <pawsa@theochem.kth.se> - 1.0.3r1-3
- Add libesmtp-build.patch - fix building under FC4.

* Thu Sep 30 2004 Miloslav Trmac <mitr@redhat.com> - 1.0.3r1-2
- Include libesmtp-config in libesmtp-devel (#125426, patch by Robert Scheck)

* Tue Jul 13 2004 John Dennis <jdennis@redhat.com> 1.0.3r1-1
- bring up to latest upstream release

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Jan 29 2004 Bill Nottingham <notting@redhat.com> 1.0.2-1
- upgrade to 1.0.2 (#113894)

* Fri Oct  3 2003 Bill Nottingham <notting@redhat.com> 1.0.1-1
- update to 1.0.1, rebuild to fix some broken 64-bit libs

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Tue Jan  7 2003 Nalin Dahyabhai <nalin@redhat.com> 0.8.12-4
- include compilation flags for openssl as defined for pkg-config
- don't blow up on compile because key schedules aren't arrays

* Tue Nov  5 2002 Bill Nottingham <notting@redhat.com> 0.8.12-3
- build on various platforms

* Tue Jul 23 2002 Bill Nottingham <notting@redhat.com> 0.8.12-2
- fix broken lib (no pthread dependency)
