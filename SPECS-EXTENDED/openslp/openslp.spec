Vendor:         Microsoft Corporation
Distribution:   Azure Linux

Summary: Open implementation of Service Location Protocol V2
Name:    openslp
Version: 2.0.0
Release: 26%{?dist}

License: BSD
URL:     https://sourceforge.net/projects/openslp/
Source0: https://downloads.sf.net/openslp/openslp-%{version}.tar.gz

# Source2,3: simple man pages (slightly modified help2man output)
Source2: slpd.8.gz
Source3: slptool.1.gz
# Source3: service file
Source4: slpd.service

# Patch1: creates script from upstream init script that sets multicast
#     prior to the start of the service
Patch1:  openslp-2.0.0-multicast-set.patch
# Patch2: notify systemd of start-up completion
Patch2:  openslp-2.0.0-notify-systemd-of-start-up.patch
# Patch3: fixes posible null pointer dereference, bz#1337402, CVE-2016-4912
Patch3:  openslp-2.0.0-null-pointer-deref.patch
# Patch4: fixes FTBFS because of openssl-1.1
Patch4:  openslp-2.0.0-openssl-1.1-fix.patch
# Patch5: fixes possible overflow in SLPFoldWhiteSpace,
#   backported from upstream, CVE-2016-7567
Patch5:  CVE-2016-7567.patch
# Patch6: fixes heap memory corruption in slpd/slpd_process.c, which allows
#   denial of service or potentially code execution,
#   backported form upstream, CVE-2017-17833
Patch6:  CVE-2017-17833.patch
# Patch7: fixes a heap overwrite vulnerability
#   leading to remote code execution
Patch7:  CVE-2019-5544.patch

BuildRequires: automake libtool
BuildRequires: bison
BuildRequires: flex 
BuildRequires: openssl-devel
BuildRequires: systemd-units systemd-devel

%description
Service Location Protocol is an IETF standards track protocol that
provides a framework to allow networking applications to discover the
existence, location, and configuration of networked services in
enterprise networks.

OpenSLP is an open source implementation of the SLPv2 protocol as defined
by RFC 2608 and RFC 2614.

%package devel
Summary: OpenSLP headers and libraries
Requires: %{name}%{?_isa} = %{version}-%{release}
%description devel
OpenSLP header files and libraries.

%package server
Summary: OpenSLP server daemon
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: iproute
%description server
OpenSLP server daemon to dynamically register services.


%prep
%setup -q

%patch 1 -p1 -b .multicast-set
%patch 2 -p2 -b .systemd
%patch 3 -p1 -b .null-pointer-deref
%patch 4 -p1 -b .openssl-1.1-fix
%patch 5 -p1 -b .cve-2016-7567
%patch 6 -p1 -b .cve-2017-17833
%patch 7 -p1 -b .cve-2019-5544

# tarball goof (?), it wants to re-automake anyway, so let's do it right.
#libtoolize --force
#aclocal
#autoconf
#automake --add-missing
autoreconf -f -i

# remove CVS leftovers...
find . -name "CVS" | xargs rm -rf


%build

# for x86_64
export CFLAGS="-fPIC -fno-strict-aliasing -fPIE -DPIE $RPM_OPT_FLAGS"
# for slpd
export LDFLAGS="-pie -Wl,-z,now"

%configure \
  --prefix=%{_prefix} \
  --libdir=%{_libdir} \
  --sysconfdir=%{_sysconfdir} \
  --localstatedir=/var \
  --disable-dependency-tracking \
  --disable-static \
  --enable-slpv2-security \
  --disable-rpath \
  --enable-async-api

make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

mkdir -p ${RPM_BUILD_ROOT}/%{_sysconfdir}/slp.reg.d

# install script that sets multicast
mkdir -p ${RPM_BUILD_ROOT}/usr/lib/%{name}-server
install -m 0755 etc/slpd.all_init ${RPM_BUILD_ROOT}/usr/lib/%{name}-server/slp-multicast-set.sh

# install service file
mkdir -p ${RPM_BUILD_ROOT}/%{_unitdir}
install -p -m 644 %{SOURCE4} ${RPM_BUILD_ROOT}/%{_unitdir}/slpd.service

# install man page
mkdir -p ${RPM_BUILD_ROOT}/%{_mandir}/man8/
mkdir -p ${RPM_BUILD_ROOT}/%{_mandir}/man1/
cp %SOURCE2 ${RPM_BUILD_ROOT}/%{_mandir}/man8/
cp %SOURCE3 ${RPM_BUILD_ROOT}/%{_mandir}/man1/

# nuke unpackaged/unwanted files
rm -rf $RPM_BUILD_ROOT/usr/doc
rm -f  $RPM_BUILD_ROOT%{_libdir}/lib*.la



%ldconfig_scriptlets

%post server
%systemd_post slpd.service

%preun server
%systemd_preun slpd.service

%postun server
%systemd_postun_with_restart slpd.service


%files
%doc AUTHORS COPYING FAQ NEWS README THANKS
%config(noreplace) %{_sysconfdir}/slp.conf
%{_bindir}/slptool
%{_libdir}/libslp.so.1*
%{_mandir}/man1/*

%files server
%doc doc/doc/html/IntroductionToSLP
%doc doc/doc/html/UsersGuide
%doc doc/doc/html/faq*
%{_sbindir}/slpd
%config(noreplace) %{_sysconfdir}/slp.reg
%config(noreplace) %{_sysconfdir}/slp.spi
%{_unitdir}/slpd.service
%{_mandir}/man8/*
/usr/lib/%{name}-server/slp-multicast-set.sh

%files devel
%doc doc/doc/html/ProgrammersGuide
%doc doc/doc/rfc
%{_includedir}/slp.h
%{_libdir}/libslp.so


%changelog
* Wed Nov 23 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.0.0-26
- License verified.
- Re-named patch files to work with Mariner's vulnerability detection.

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.0.0-25
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.0-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Dec 09 2019 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.0.0-23
- Fix heap overwrite vulnerability, CVE-2019-5544
  Resolves: #1780754

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.0-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.0-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.0-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.0.0-19
- Remove dependency on initscripts
  Resolves: #1592378

* Wed May 09 2018 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.0.0-18
- Fix heap memory corruption, CVE-2017-17833
  Related: #1572166

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.0-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Oct 04 2017 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.0.0-16
- Replace route with appropriate command from iproute
  Related: #1496138

* Wed Oct 04 2017 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.0.0-15
- Removed dependency on net-tools
  Resolves: #1496138
- Removed init script, Group tag and macro from changelog in spec file
- Slightly modified openssl-1.1 fix to be able build the package
  with OpenSSL version lower than 1.1

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.0-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Mar 14 2017 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.0.0-12
- Fix possible overflow in SLPFoldWhiteSpace, CVE-2016-7567
  Resolves: #1379988

* Wed Feb 22 2017 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.0.0-11
- Fix FTBFS because of openssl-1.1
  Resolves: #1424028

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon May 23 2016 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.0.0-9
- Fix null pointer dereference, CVE-2016-4912
  Resolves: #1337402

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Mar 11 2015 Adam Jackson <ajax@redhat.com> 2.0.0-6
- Drop sysvinit script from F23+

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Mon Aug 04 2014 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.0.0-4
- Link to libsystemd.so instead of old libsystemd-daemon.so
  Resolves: #1125103

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Mar 17 2014 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.0.0-2
- Launch slpd as a 'notify' daemon with systemd, rather than forking
  (patch by Stephen Gallagher)

* Tue Oct 01 2013 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.0.0-1
- Update to openslp-2.0.0
- Fix bogus dates in %%changelog
- Add systemd support
- Add man pages for slptool and slpd
- Add CFLAGS and LDFLAGS for full relro
- Build with -fno-strict-aliasing

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.1-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jun 19 2013 Rex Dieter <rdieter@fedoraproject.org> 1.2.1-19
- -server: Requires: +net-tools (for netstat, #975868)

* Wed Jan 30 2013 Rex Dieter <rdieter@fedoraproject.org> 1.2.1-18
- update URL: tag (#905975)

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.1-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.1-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.1-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Sep 16 2009 Rex Dieter <rdieter@fedoraproject.org> - 1.2.1-14
- slpd crashes if slptool findsrvtypes is run, when message logging is on (#523609)

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 1.2.1-13
- rebuilt with new openssl

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Jan 17 2009 Tomas Mraz <tmraz@redhat.com> - 1.2.1-10
- rebuild with new openssl

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.2.1-9
- Autorebuild for GCC 4.3

* Tue Dec 04 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 1.2.1-8
- respin for openssl

* Tue Aug 21 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 1.2.1-7
- respin (buildID)

* Tue Aug 29 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.2.1-6
- fc6 respin

* Wed Aug 09 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.2.1-5
- fc6 respin

* Wed Mar 1 2006 Rex Dieter <rexdieter[AT]users.sf.net> 
- fc5: gcc/glibc respin

* Mon Dec 19 2005 Rex Dieter <rexdieter[AT]users.sf.net> 1.2.1-4
- make %%postun safer

* Wed Nov 16 2005 Rex Dieter <rexdieter[AT]users.sf.net> 1.2.1-3
- rebuild (for new openssl)
- make %%postun safer

* Fri Oct 21 2005 Rex Dieter <rexdieter[AT]users.sf.net> 1.2.1-2
- -fPIC (for x86_64)

* Fri Oct 21 2005 Rex Dieter <rexdieter[AT]users.sf.net> 1.2.1-1
- 1.2.1
- move most docs to -server
- --enable-slpv2-security
- --disable-dependency-tracking

* Sun May 22 2005 Jeremy Katz <katzj@redhat.com> - 1.2.0
- rebuild on all arches

* Thu Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Mon Jul 19 2004 Rex Dieter <rexdieter at sf.net> 0:1.2.0-0.fdr.4
- BR: flex

* Fri Jul 16 2004 Rex Dieter <rexdieter at sf.net> 0:1.2.0-0.fdr.3
- BR: bison

* Thu Jul 15 2004 Rex Dieter <rexdieter at sf.net> 0:1.2.0-0.fdr.2
- fix/add condrestart to init script

* Thu Jul 15 2004 Rex Dieter <rexdieter at sf.net> 0:1.2.0-0.fdr.1
- 1.2.0
- use -pie
- don't use Requires(post,postun)

* Fri Oct 24 2003 Rex Dieter <rexdieter af sf.net> 0:1.0.11-0.fdr.7
- fix for Fedora Core
- fix description (main package does *not* include daemon and header files).

* Fri May 30 2003 Rex Dieter <rexdieter at sf.net> 0:1.0.11-0.fdr.6
- -server: Requires(preun,postun): /sbin/service
- add a few more %%doc files to base pkg.
- initscript: add (real) 'reload' action.
- initscript: use $prog instead of hardcoded slpd.

* Fri May 16 2003 Rex Dieter <rexdieter at sf.net> 0:1.0.11-0.fdr.5
- -server: fix %%postun on uninstall

* Fri May 2 2003 Rex Dieter <rexdieter at sf.net> 0:1.0.11-0.fdr.4
- *really* do %%config(noreplace) slp.conf

* Thu May 1 2003 Rex Dieter <rexdieter at sf.net> 0:1.0.11-0.fdr.3
- capitalize Summary's.
- %%config(noreplace) slp.conf

* Thu May 1 2003 Rex Dieter <rexdieter at sf.net> 0:1.0.11-0.fdr.2
- docs: remove CVS files, include rfc, move ProgrammersGuide to -devel.
- improve sub-pkg descriptions.
- improve server %%preun,%%postun scripts: condrestart on upgrade,
  suppress output of server shutdown,restarts.

* Thu May 1 2003 Rex Dieter <rexdieter at sf.net> 0:1.0.11-0.fdr.1
- specfile cleanups for fedora packaging.

* Tue Apr 29 2003 Rex Dieter <rexdieter at sf.net> 0:1.0.11-0.fdr.0
- 1.0.11 release.
- fedorize things

* Mon Feb 03 2003 Rex Dieter <rexdieter at sf.net> 0:1.0.10-1.0
- sanitize specfile
- -devel,-server subpkgs.
