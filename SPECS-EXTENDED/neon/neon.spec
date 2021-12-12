Vendor:         Microsoft Corporation
Distribution:   Mariner
%bcond_without tests

Summary: An HTTP and WebDAV client library
Name: neon
Version: 0.31.2
Release: 2%{?dist}
License: LGPLv2+
URL: https://notroj.github.io/neon/
Source0: https://notroj.github.io/neon/neon-%{version}.tar.gz
Patch0: neon-0.27.0-multilib.patch
BuildRequires:  gcc-c++
BuildRequires: expat-devel, openssl-devel, zlib-devel, krb5-devel, libproxy-devel
BuildRequires: pkgconfig, pakchois-devel
Requires: ca-certificates
%if %{with tests}
# SSL tests require openssl binary, PKCS#11 testing need certutil
BuildRequires: /usr/bin/perl, /usr/bin/openssl, /usr/bin/certutil
%endif

%description
neon is an HTTP and WebDAV client library, with a C interface;
providing a high-level interface to HTTP and WebDAV methods along
with a low-level interface for HTTP request handling.  neon
supports persistent connections, proxy servers, basic, digest and
Kerberos authentication, and has complete SSL support.

%package devel
Summary: Development libraries and C header files for the neon library
Requires: neon = %{version}-%{release}, openssl-devel, zlib-devel, expat-devel
Requires: pkgconfig
# Documentation is GPLv2+
License: LGPLv2+ and GPLv2+

%description devel
The development library for the C language HTTP and WebDAV client library.

%prep
%setup -q
%patch0 -p1 -b .multilib

# prevent installation of HTML docs
sed -ibak '/^install-docs/s/install-html//' Makefile.in

%build
export CC="%{__cc} -pthread"
%configure --with-expat --enable-shared --disable-static \
        --enable-warnings \
        --with-ssl=openssl --enable-threadsafe-ssl=posix \
        --with-libproxy
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"

sed -ri "/^dependency_libs/{s,-l[^ ']*,,g}" \
      $RPM_BUILD_ROOT%{_libdir}/libneon.la

%find_lang %{name}

%if %{with tests}
%check
export TEST_QUIET=0
make %{?_smp_mflags} check
%endif

%ldconfig_scriptlets

%files -f %{name}.lang
%doc AUTHORS BUGS TODO src/COPYING.LIB NEWS README* THANKS
%{_libdir}/*.so.*

%files devel
%{_bindir}/*
%{_includedir}/*
%{_libdir}/pkgconfig/neon.pc
%{_mandir}/man1/*
%{_mandir}/man3/*
%{_libdir}/*.*a
%{_libdir}/*.so

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.31.2-2
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jun 24 2020 Joe Orton <jorton@redhat.com> - 0.31.2-1
- update to 0.31.2

* Fri Apr 17 2020 Joe Orton <jorton@redhat.com> - 0.31.1-1
- update to 0.31.1

* Tue Mar 24 2020 Joe Orton <jorton@redhat.com> - 0.31.0-1
- update to 0.31.0

* Mon Feb 10 2020 Joe Orton <jorton@redhat.com> - 0.30.2-14
- fix FTBFS (#1799679)

* Mon Feb 03 2020 Kalev Lember <klember@redhat.com> - 0.30.2-13
- Avoid using bindir macro in buildrequires

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.30.2-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.30.2-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Apr  5 2019 Joe Orton <jorton@redhat.com> - 0.30.2-10
- updates for OpenSSL 1.1 (#1675444)

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.30.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.30.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Joe Orton <jorton@redhat.com> - 0.30.2-7
- fix gcc warnings in test suite build

* Thu Jun 28 2018 Joe Orton <jorton@redhat.com> - 0.30.2-6
- fix implicit writev declaration (Mattias Ellert, #1572180)
- add build conditional for tests
- use ldconfig_scriptlets macro

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.30.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.30.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.30.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.30.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Sep 30 2016 Joe Orton <jorton@redhat.com> - 0.30.2-1
- update to 0.30.2

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.30.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.30.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Sep 23 2014 Joe Orton <jorton@redhat.com> - 0.30.1-2
- switch to OpenSSL

* Tue Sep 23 2014 Joe Orton <jorton@redhat.com> - 0.30.1-1
- update to 0.30.1

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.30.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.30.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Jul 31 2013 Joe Orton <jorton@redhat.com> - 0.30.0-2
- prevent installation of HTML docs

* Wed Jul 31 2013 Joe Orton <jorton@redhat.com> - 0.30.0-1
- update to 0.30.0 (#983563, #926212)

* Mon Mar 18 2013 Joe Orton <jorton@redhat.com> - 0.29.6-6
- fix strict-aliasing warning (upstream r1896)

* Mon Feb 25 2013 Tomáš Mráz <tmraz@redhat.com> - 0.29.6-5
- fix build with gnutls3 - patch by Bartosz Brachaczek

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.29.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.29.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.29.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue May  3 2011 Joe Orton <jorton@redhat.com> - 0.29.6-1
- update to 0.29.6
- correct -devel License; drop old Conflicts

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.29.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Oct 14 2010 Joe Orton <jorton@redhat.com> - 0.29.5-1
- update to 0.29.5

* Fri Oct  1 2010 Joe Orton <jorton@redhat.com> - 0.29.4-1
- update to 0.29.4

* Thu Mar 25 2010 Joe Orton <jorton@redhat.com> - 0.29.3-1
- update to 0.29.3

* Fri Jan  8 2010 Joe Orton <jorton@redhat.com> - 0.29.2-1
- update to 0.29.2

* Tue Dec 15 2009 Joe Orton <jorton@redhat.com> - 0.29.1-1
- update to 0.29.1

* Sun Sep 13 2009 Joe Orton <jorton@redhat.com> 0.29.0-3
- enable libproxy support

* Sun Sep 13 2009 Joe Orton <jorton@redhat.com> 0.29.0-1
- update to 0.29.0

* Wed Aug 19 2009 Joe Orton <jorton@redhat.com> 0.28.6-1
- update to 0.28.6

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.28.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jul  9 2009 Joe Orton <jorton@redhat.com> 0.28.5-1
- update to 0.28.5

* Fri Mar  6 2009 Joe Orton <jorton@redhat.com> 0.28.4-1
- update to 0.28.4

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.28.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Jan 19 2009 Joe Orton <jorton@redhat.com> 0.28.3-3
- use install-p in "make install" (Robert Scheck, #226189)

* Thu Aug 28 2008 Joe Orton <jorton@redhat.com> 0.28.3-2
- update to 0.28.3

* Wed Jun 25 2008 Joe Orton <jorton@redhat.com> 0.28.2-4
- rebuild for new GnuTLS

* Mon Jun  2 2008 Joe Orton <jorton@redhat.com> 0.28.2-3
- require ca-certificates package

* Thu Apr  3 2008 Joe Orton <jorton@redhat.com> 0.28.2-2
- update to 0.28.2

* Wed Apr  2 2008 Joe Orton <jorton@redhat.com> 0.28.1-3
- use the OpenSSL CA bundle

* Mon Mar 10 2008 Joe Orton <jorton@redhat.com> 0.28.1-2
- update to 0.28.1

* Tue Feb 26 2008 Joe Orton <jorton@redhat.com> 0.28.0-3
- rebuild against pakchois

* Wed Dec  5 2007 Joe Orton <jorton@redhat.com> 0.27.2-4
- trim dependency_libs in .la file

* Tue Dec  4 2007 Joe Orton <jorton@redhat.com> 0.27.2-3
- rebuild against GnuTLS
- drop static library

* Tue Sep 25 2007 Joe Orton <jorton@redhat.com> 0.27.2-2
- update to 0.27.2

* Thu Sep 20 2007 Joe Orton <jorton@redhat.com> 0.27.0-3
- fix Negotiate response verification

* Thu Aug 30 2007 Joe Orton <jorton@redhat.com> 0.27.0-2
- enable OpenSSL thread-safety hooks

* Wed Aug 22 2007 Joe Orton <jorton@redhat.com> 0.27.0-1
- update to 0.27.0 (#243638)

* Mon Aug 20 2007 Joe Orton <jorton@redhat.com> 0.25.5-7
- fix License

* Mon Feb  5 2007 Joe Orton <jorton@redhat.com> 0.25.5-6
- remove trailing dot in -devel Summary
- use standard BuildRoot
- change Group to System Environment/Libraries
- drop Prefix

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 0.25.5-5.1
- rebuild

* Thu Jun  1 2006 Joe Orton <jorton@redhat.com> 0.25.5-5
- have -devel require pkgconfig (#193355)

* Wed May 24 2006 Joe Orton <jorton@redhat.com> 0.25.5-4
- add multilib fixes for neon-config (#192734)

* Wed May 17 2006 Joe Orton <jorton@redhat.com> 0.25.5-3
- rebuild

* Mon Feb 27 2006 Joe Orton <jorton@redhat.com> 0.25.5-2
- don't trim exported libraries (#182997)

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 0.25.5-1.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 0.25.5-1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Tue Jan 31 2006 Joe Orton <jorton@redhat.com> 0.25.5-1
- update to 0.25.5

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Wed Dec  7 2005 Joe Orton <jorton@redhat.com> 0.24.7-10
- strip unnecessary exports from .la file/neon-config

* Tue Nov  8 2005 Tomas Mraz <tmraz@redhat.com> 0.24.7-9
- rebuilt with new openssl

* Fri Sep 23 2005 Joe Orton <jorton@redhat.com> 0.24.7-8
- restore static libs for rpm

* Mon Sep 19 2005 Joe Orton <jorton@redhat.com> 0.24.7-7
- drop static libs, doc/html from devel docdir

* Wed Mar  2 2005 Joe Orton <jorton@redhat.com> 0.24.7-6
- rebuild

* Thu Feb 10 2005 Joe Orton <jorton@redhat.com> 0.24.7-5
- don't define min() in ne_utils.h (Caolan McNamara, #147228)

* Tue Oct 12 2004 Joe Orton <jorton@redhat.com> 0.24.7-4
- update to GSSAPI code from trunk

* Fri Jul 23 2004 Joe Orton <jorton@redhat.com> 0.24.7-3
- rebuild

* Tue Jul 20 2004 Joe Orton <jorton@redhat.com> 0.24.7-2.1
- rebuild

* Tue Jul  6 2004 Joe Orton <jorton@redhat.com> 0.24.7-2
- devel requires neon of same release, expat-devel (#127330)

* Mon Jul  5 2004 Joe Orton <jorton@redhat.com> 0.24.7-1
- update to 0.24.7

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed May 19 2004 Joe Orton <jorton@redhat.com> 0.24.6-1
- update to 0.24.6

* Wed Apr 14 2004 Joe Orton <jorton@redhat.com> 0.24.5-2
- rebuild

* Wed Apr 14 2004 Joe Orton <jorton@redhat.com> 0.24.5-1
- update to 0.24.5 for CVE CAN-2004-0179 fix

* Thu Mar 25 2004 Joe Orton <jorton@redhat.com> 0.24.4-4
- implement the Negotate auth scheme, and only over SSL

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Feb 25 2004 Joe Orton <jorton@redhat.com> 0.24.4-3
- use BuildRequires not BuildPrereq, drop autoconf, libtool;
  -devel requires {openssl,zlib}-devel (#116744)

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com> 0.24.4-2
- rebuilt

* Mon Feb  9 2004 Joe Orton <jorton@redhat.com> 0.24.4-1
- update to 0.24.4

* Thu Oct  9 2003 Joe Orton <jorton@redhat.com> 0.24.3-1
- update to 0.24.3

* Wed Sep 24 2003 Joe Orton <jorton@redhat.com> 0.24.2-1
- update to 0.24.2

* Tue Jul 22 2003 Nalin Dahyabhai <nalin@redhat.com> 0.23.9-7
- rebuild

* Tue Jun 24 2003 Joe Orton <jorton@redhat.com> 0.23.9-6
- never print libdir in --libs output

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Jun  3 2003 Joe Orton <jorton@redhat.com> 0.23.9-4
- don't regenerate docs; limit conflict with subversion

* Wed May 28 2003 Jeff Johnson <jbj@redhat.com> 0.23.9-3
- build.

* Sat May 24 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- add ldconfig to post/postun

* Tue May 20 2003 Jeff Johnson <jbj@redhat.com> 0.23.9-2
- force expat, include neon-config, for subversion build.
- do "make check" (but ignore failure for now)

* Mon May 19 2003 Jeff Johnson <jbj@redhat.com> 0.23.9-1
- upgrade to 0.23.9.
- avoid xmlto breakage generating man pages for now.

* Mon Nov 11 2002 Jeff Johnson <jbj@redhat.com> 0.23.5-2
- avoid subversion-devel until libxml2 vs. expat is resolved.

* Sat Nov  9 2002 Jeff Johnson <jbj@redhat.com> 0.23.5-1
- Create.
