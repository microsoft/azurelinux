%global racoonconfdir %{_sysconfdir}/racoon

Name:         ipsec-tools
Version:      0.8.2
Release:      18%{?dist}
Summary:      Tools for configuring and using IPSEC
Group:        Applications/Networking
Vendor:       Microsoft Corporation
Distribution: Mariner
License:      BSD
URL:          http://ipsec-tools.sourceforge.net/

Source:       ftp://ftp.netbsd.org/pub/NetBSD/misc/ipsec-tools/0.8/ipsec-tools-%{version}.tar.bz2
Source1:      racoon.conf
Source2:      psk.txt
Source3:      p1_up_down
Source4:      racoon.service
Source5:      racoon.pam
Source6:      ifup-ipsec
Source7:      ifdown-ipsec

# Ignore acquires that are sent by kernel for SAs that are already being
# negotiated (#234491)
Patch3: ipsec-tools-0.8.0-acquires.patch
# Support for labeled IPSec on loopback
Patch4: ipsec-tools-0.8.0-loopback.patch
# Create racoon as PIE
Patch11: ipsec-tools-0.7.1-pie.patch
# Fix leak in certification handling
Patch14: ipsec-tools-0.7.2-moreleaks.patch
# Do not install development files
Patch16: ipsec-tools-0.8.0-nodevel.patch
# Use krb5 gssapi mechanism
Patch18: ipsec-tools-0.7.3-gssapi-mech.patch
# Drop -R from linker
Patch19: ipsec-tools-0.7.3-build.patch
# Silence strict aliasing warnings
Patch20: ipsec-tools-0.8.0-aliasing.patch
# CVE-2015-4047
Patch21: ipsec-tools-0.8.2-CVE-2015-4047.patch
# Calling_station-Id attribute for xauth RADIUS requests
Patch22: ipsec-tools-0.8.2-952413.patch
Patch30: openssl_1_1.patch

BuildRequires:    audit-libs >= 1.3.1
BuildRequires:    audit-devel >= 1.3.1
BuildRequires:    automake
BuildRequires:    bison
BuildRequires:    libcap-ng-devel
BuildRequires:    readline-devel
BuildRequires:    glibc-devel
BuildRequires:    e2fsprogs-devel
BuildRequires:    openssl-devel
BuildRequires:    flex
BuildRequires:    flex-devel
BuildRequires:    krb5-devel
BuildRequires:    libtool
BuildRequires:    libselinux-devel
BuildRequires:    openldap
BuildRequires:    pam-devel
BuildRequires:    systemd

Requires:         pam
Requires:         initscripts
Requires:         chkconfig
Requires(post):   systemd
Requires(preun):  systemd
Requires(postun): systemd


%description
This package contains tools necessary for establishing
keys for IPSEC connections including the rekeying during
the connection lifetime.

The main tools of this package are:

- setkey, a program to directly manipulate policies and SAs in the kernel
- racoon, an IKEv1 keying daemon

%package devel
Summary:       Devel package for ipsec-tools
Group:         Development/Libraries

%description devel
This package contains static libraries and header files need for development.

%prep
%setup -q
%patch3 -p1 -b .acquires
%patch4 -p1 -b .loopback

%patch11 -p1 -b .pie
%patch14 -p1 -b .moreleaks
# %patch16 -p1 -b .nodevel
%patch18 -p1 -b .gssapi-mech
%patch19 -p1 -b .build
%patch20 -p1 -b .aliasing
%patch21 -p1 -b .cve_2015_4047
%patch22 -p1 -b .station_id
%patch30 -p1

%build
./bootstrap
# Needed because some bad sizeof()'s
sed -i 's|-Werror||g' configure
# Needed to avoid error on gethostbyname, enable full relro
LDFLAGS="$LDFLAGS -Wl,--as-needed"
# Enable full relro hardening
export LDFLAGS="$LDFLAGS -fPIC -pie -Wl,-z,relro -Wl,-z,now"
%configure \
 --with-kernel-headers=/usr/include \
 --sysconfdir=%{racoonconfdir} \
 --disable-shared \
 --without-readline \
 --enable-adminport \
 --enable-hybrid \
 --enable-frag \
 --enable-dpd \
 --enable-gssapi \
 --enable-natt \
 --enable-security-context \
 --enable-audit \
 --with-libpam \
 --with-libldap \
# --with-libradius requires an unknown radius library
# and complains about our -liconv being broken.
make

%install
mkdir -p $RPM_BUILD_ROOT/sbin
mkdir -p $RPM_BUILD_ROOT%{racoonconfdir}
make install DESTDIR=$RPM_BUILD_ROOT

install -m 600 %{SOURCE1} \
  $RPM_BUILD_ROOT%{racoonconfdir}/racoon.conf
install -m 600 %{SOURCE2} \
  $RPM_BUILD_ROOT%{racoonconfdir}/psk.txt

mv $RPM_BUILD_ROOT%{_sbindir}/setkey $RPM_BUILD_ROOT/sbin

mkdir -m 0700 -p $RPM_BUILD_ROOT%{racoonconfdir}/certs
mkdir -m 0700 -p $RPM_BUILD_ROOT%{racoonconfdir}/scripts
install -m 700 %{SOURCE3} \
  $RPM_BUILD_ROOT%{racoonconfdir}/scripts/p1_up_down
install -D -m644 %{SOURCE4} $RPM_BUILD_ROOT%{_unitdir}/racoon.service
install -D -m644 %{SOURCE5} $RPM_BUILD_ROOT%{_sysconfdir}/pam.d/racoon

mkdir -m 0755 -p $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/network-scripts
install -p -m755 %{SOURCE6} %{SOURCE7} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/network-scripts


%post
/sbin/ldconfig
%systemd_post racoon.service

%preun
%systemd_preun racoon.service

%postun
/sbin/ldconfig
%systemd_postun_with_restart racoon.service

%files
%doc src/racoon/samples/racoon.conf src/racoon/samples/psk.txt
%doc src/racoon/doc/FAQ
%doc NEWS README
%{_sbindir}/*
%{_mandir}/man*/*
%{_unitdir}/racoon.service
%dir %{racoonconfdir}
%{racoonconfdir}/scripts/*
%dir %{racoonconfdir}/certs
%dir %{racoonconfdir}/scripts
%dir %{_localstatedir}/racoon
%config(noreplace) %{racoonconfdir}/psk.txt
%config(noreplace) %{racoonconfdir}/racoon.conf
%config(noreplace) %{_sysconfdir}/pam.d/racoon
%dir %{_includedir}/libipsec
%{_includedir}/libipsec/*.h
%dir %{_includedir}/racoon
%{_includedir}/racoon/*.h
%{_libdir}/*
/sbin/*
%{_sysconfdir}/sysconfig/network-scripts/ifup-ipsec
%{_sysconfdir}/sysconfig/network-scripts/ifdown-ipsec


%changelog
* Fri Sep 17 2021 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 0.8.2-18
- Initial CBL-Mariner import from Fedora 32 (license: MIT)
- License verified

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.2-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.2-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.2-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jan 14 2019 Björn Esser <besser82@fedoraproject.org> - 0.8.2-14
- Rebuilt for libcrypt.so.2 (#1666033)

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.2-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.2-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Jan 20 2018 Björn Esser <besser82@fedoraproject.org> - 0.8.2-11
- Rebuilt for switch to libxcrypt

* Thu Jan 11 2018 Peter Robinson <pbrobinson@fedoraproject.org> 0.8.2-10
- Spec cleanup and modernise, build with compat-openssl10 (fix FTBFS)

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jan 24 2017 Paul Wouters <pwouters@redhat.com> - 0.8.2-6
- Resolves: rhbz#1416122 ipsec-tools component racoon.service triggers complaints from systemd

* Thu Apr 28 2016 Paul Wouters <pwouters@redhat.com> - 0.8.2-5
- Resolves: rhbz#1251691 ifup-ipsec causes invalid ICMP redirects
  (Patch by Kaarle Ritvanen <kaarle.ritvanen@datakunkku.fi>)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Dec 17 2015 Paul Wouters <pwouters@redhat.com> - 0.8.2-2
- Resolves: rhbz#1292522 Add remoteid/ph1id configuration feature

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue May 26 2015 Paul Wouters <pwouters@redhat.com> - 0.8.2-1
- Upgraded to 0.8.2
- Resolves rhbz#1223420 CVE-2015-4047 NULL pointer dereference in racoon/gssapi.c
- Resolves rhbz#1154906 fix port 4500 vs 500 isakmp initiator issue
- Resolves rhbz#952413 Support for Calling-Station-Id attribute for xauth RADIUS requests

* Fri Jan 09 2015 Paul Wouters <pwouters@redhat.com> - 0.8.1-6
- Resolves: rhbz#1029503 missing depdendency on psmisc (fixup systemd scripts)

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Nov 14 2013 Paul Wouters <pwouters@redhat.com> - 0.8.1-3
- Enable ldap support (rhbz#895965)
- Update systemd macros (rhbz#850016)
- Enable full relro hardening

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 27 2013 Tomáš Mráz <tmraz@redhat.com> - 0.8.1-1
- new upstream release
- enabled ldap support (#895965)
- macroized systemd script calls (#850165)

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jan 26 2012 Tomas Mraz <tmraz@redhat.com> - 0.8.0-4
- prefer the main IKE exchange mode (#475337)
- allow specification of additional parameters for the ifup-ipsec (#784859)
- convert the init script to systemd unit (#662714)

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jun 17 2011 Tomas Mraz <tmraz@redhat.com> - 0.8.0-2
- take over ifup-ipsec, ifdown-ipsec from initscripts

* Mon Mar 21 2011 Tomas Mraz <tmraz@redhat.com> - 0.8.0-1
- update to a new upstream version

* Thu Feb 10 2011 Tomas Mraz <tmraz@redhat.com> - 0.7.3-8
- fix build - drop -R from compiler invocation

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec  7 2010 Tomas Mraz <tmraz@redhat.com> - 0.7.3-6
- fix FTBFS, add flex-static to buildrequires (#660865)

* Wed Apr 14 2010 Tomas Mraz <tmraz@redhat.com> - 0.7.3-5
- fix the initscript (#500571, #521647)

* Fri Sep 25 2009 Tomas Mraz <tmraz@redhat.com> - 0.7.3-4
- properly check for errors on gssapi_get_token_to_send()
- use proper mechanism when canonicalizing gss names
- use password-auth common PAM configuration instead of system-auth

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 0.7.3-3
- rebuilt with new openssl

* Wed Aug 19 2009 Tomas Mraz <tmraz@redhat.com> - 0.7.3-2
- enable xauth over PAM (#470793)
- add TMPDIR setting to the p1_up_down script

* Tue Aug 18 2009 Tomas Mraz <tmraz@redhat.com> - 0.7.3-1
- update to a new upstream version
- fix service stop in preun (#515880)

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul 15 2009 Tomas Mraz <tmraz@redhat.com> - 0.7.2-2
- fix FTBFS (#511556)
- fix some memory leaks and compilation warnings found by review

* Thu Apr 23 2009 Tomas Mraz <tmraz@redhat.com> - 0.7.2-1
- Update to a new upstream version

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Jan 15 2009 Tomas Mraz <tmraz@redhat.com> - 0.7.1-7
- rebuild with new openssl

* Mon Nov 10 2008 Tomas Mraz <tmraz@redhat.com> - 0.7.1-6
- fix patch porting error in the dpd-fixes patch (#470575)

* Fri Oct 17 2008 Tomas Mraz <tmraz@redhat.com> - 0.7.1-5
- fix CVE-2008-3652 (memory leak DoS)
- compile racoon as PIE
- another fix for teardown of the IPSEC SAs on DPD in some circumstances

* Sun Aug 10 2008 Tomas Mraz <tmraz@redhat.com> - 0.7.1-4
- Even better fix for IPSEC SA purging avoiding code duplication
  (original idea by Darrel Goeddel)

* Fri Aug  8 2008 Tomas Mraz <tmraz@redhat.com> - 0.7.1-3
- Fix IPSEC SA purge with NAT_T enabled

* Wed Jul 30 2008 Tomas Mraz <tmraz@redhat.com> - 0.7.1-2
- Different approach to allow racoon to add loopback SAs for
  labeled IPSec (without ISAKMP)

* Tue Jul 29 2008 Tomas Mraz <tmraz@redhat.com> - 0.7.1-1
- Update to a new upstream version

* Thu Feb 28 2008 Steve Conklin <sconklin@redhat.com> - 0.7-13
- Resolves bz#273261 remote-access client connection to Cisco ASA

* Mon Feb 25 2008 Steve Conklin <sconklin@redhat.com> - 0.7-12
- And again

* Mon Feb 25 2008 Steve Conklin <sconklin@redhat.com> - 0.7-11
- Messed that up, bumping

* Mon Feb 25 2008 Steve Conklin <sconklin@redhat.com> - 0.7-10
- Added upstream patch to fix ipv6 cookie alen

* Thu Feb 14 2008 Steve Conklin <sconklin@redhat.com> - 0.7-9
- rebuild for gcc4.3

* Wed Dec 19 2007 Steve Conklin <sconklin@redhat.com> - 0.7-8
- sourced krb5-devel.sh to set path

* Tue Dec 18 2007 Steve Conklin <sconklin@redhatcom> - 0.7-7
- bumped for retag

* Tue Dec 18 2007 Steve Conklin <sconklin@redhat.com> - 0.7-6
- Added a patch for context size change
- Resolves #413331 racoon dies with buffer overflow in MCS/MLS loopback

* Fri Dec  7 2007 Steve Conklin <sconklin@redhat.com> - 0.7-5
- Bump for retagging

* Fri Dec  7 2007 Steve Conklin <sconklin@redhat.com> - 0.7-4
- Rebuild for dependencies

* Thu Sep 20 2007 Steve Conklin <sconklin@redhat.com> - 0.7-3
- Applied the following patches from Gabriel Somlo
- Patches for connecting to Cisco ASA in remote-access (road-warrior) mode
- Added phase1_up_down mode config script
- Including our own .h files (ipsec, pfkeyv2, xfrm, udp) no longer necessary
- Added init script for racoon daemon

* Tue Aug 28 2007 Steve Conklin <sconklin@redhat.com> - 0.7-2
- Fixed the loopback patch

* Tue Aug 28 2007 Steve Conklin <sconklin@redhat.com> - 0.7-1
- Rebase to upstream 0.7

* Mon Apr 23 2007 Steve Grubb <sgrubb@redhat.com> - 0.6.5-8
- Upstream fix for Racoon DOS, informational delete must be encrypted
- Resolves: rhbz#235388 - CVE-2007-1841 ipsec-tools racoon DoS

* Fri Apr 20 2007 Steve Grubb <sgrubb@redhat.com> - 0.6.5-7
- Resolves: #218386 labeled ipsec does not work over loopback

* Mon Apr 16 2007 Steve Grubb <sgrubb@redhat.com> - 0.6.5-6.6
- Related: #232508 add auditing to racoon

* Sat Apr 14 2007 Steve Grubb <sgrubb@redhat.com> - 0.6.6-6%{?dist}
- Resolves: #235680 racoon socket descriptor exhaustion

* Fri Apr 13 2007 Steve Grubb <sgrubb@redhat.com> - 0.6.6-4%{?dist}
- Resolves: #236121 increase buffer for context
- Resolves: #234491 kernel sends ACQUIRES that racoon is not catching
- Resolves: #218386 labeled ipsec does not work over loopback

* Tue Mar 20 2007 Harald Hoyer <harald@redhat.com> - 0.6.6-3%{?dist}
- fix for setting the security context into a 
  proposal (32<->64bit) (rhbz#232508)

* Wed Jan 17 2007 Harald Hoyer <harald@redhat.com> - 0.6.6-1
- version 0.6.6

* Sun Oct 01 2006 Jesse Keating <jkeating@redhat.com> - 0.6.5-6
- rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Mon Sep 25 2006 Harald Hoyer <harald@redhat.com> - 0.6.5-5
- added patch for selinux integration (bug #207159)

* Fri Aug  4 2006 Harald Hoyer <harald@redhat.com> - 0.6.5-4
- backport of important 0.6.6 fixes:
  - sets NAT-T ports to 0 if no NAT encapsulation
  - fixed memory leak

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 0.6.5-3.1
- rebuild

* Wed Jun 21 2006 Harald Hoyer <harald@redhat.com> - 0.6.5-3
- more build requirements

* Tue Apr 18 2006 Dan Walsh <dwalsh@redhat.com> - 0.6.5-2
- Fix patch to build MLS Stuff correctly

* Tue Apr 18 2006 Dan Walsh <dwalsh@redhat.com> - 0.6.5-1
- Update to latest upstream version
- Add MLS Patch to allow use of labeled networks
- Patch provided by Joy Latten <latten@austin.ibm.com>

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 0.6.4-1.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Harald Hoyer <harald@redhat.com> 0.6.4-1
- version 0.6.4

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 0.6.3-1.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Mon Dec 05 2005 Harald Hoyer <harald@redhat.com> 0.6.3-1
- version 0.6.3, which contains fixes for various DoS problems

* Wed Nov  9 2005 Tomas Mraz <tmraz@redhat.com> 0.6.1-2
- rebuilt against new openssl

* Wed Oct 12 2005 Harald Hoyer <harald@redhat.com> 0.6.1-1
- version 0.6.1

* Mon Mar 28 2005 Bill Nottingham <notting@redhat.com> 0.5-4
- fix 64-bit issue in setph1attr() (<aviro@redhat.com>)

* Mon Mar 14 2005 Bill Nottingham <notting@redhat.com> 0.5-3
- add patch for DoS (CAN-2005-0398, #145532)

* Sat Mar  5 2005 Uwe Beck <ubeck@c3pdm.com> 0.5-2
- now racoon use /etc/racoon/racoon.conf as default
- add the /var/racoon directory for racoon.sock

* Wed Feb 23 2005 Bill Nottingham <notting@redhat.com> 0.5-1
- update to 0.5

* Thu Nov  4 2004 Bill Nottingham <notting@redhat.com> 0.3.3-2
- don't use new 0.3.3 handling of stdin in setkey; it breaks the
  format (#138105)

* Mon Sep 27 2004 Bill Nottingham <notting@redhat.com> 0.3.3-1
- update to 0.3.3 (#122211)

* Sun Aug 08 2004 Alan Cox <alan@redhat.com> 0.2.5-6
- fix buildreqs (Steve Grubb)

* Mon Jun 28 2004 Nalin Dahyabhai <nalin@redhat.com> 0.2.5-5
- rebuild

* Fri Jun 25 2004 Nalin Dahyabhai <nalin@redhat.com> 0.2.5-4
- backport certificate validation fixes from 0.3.3 (#126568)

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Apr 14 2004 Bill Nottingham <notting@redhat.com> - 0.2.5-2
- add patch for potential remote DoS (CAN-2004-0403)

* Tue Apr  6 2004 Bill Nottingham <notting@redhat.com>
- update to 0.2.5

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Feb 23 2004 Bill Nottingham <notting@redhat.com>
- update to 0.2.4, fix racoon install location (#116374, <kajtzu@fi.basen.net>)

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Dec  8 2003 Bill Nottingham <notting@redhat.com> 0.2.2-8
- rebuild

* Fri Aug 29 2003 Bill Nottingham <notting@redhat.com> 0.2.2-7
- add fix for #103238

* Tue Aug  5 2003 Bill Nottingham <notting@redhat.com> 0.2.2-6
- update kernel interface bits, rebuild against them

* Tue Jul 29 2003 Bill Nottingham <notting@redhat.com> 0.2.2-5
- rebuild

* Wed Jul  2 2003 Bill Notitngham <notting@redhat.com> 0.2.2-4
- ship a much more pared-down racoon.conf and psk.txt

* Thu Jun  5 2003 Bill Notitngham <notting@redhat.com> 0.2.2-3
- update pfkey header for current kernels

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri May  2 2003 Bill Nottingham <notting@redhat.com> 0.2.2-1
- update to 0.2.2

* Fri Mar  7 2003 Bill Nottingham <notting@redhat.com>
- initial build
