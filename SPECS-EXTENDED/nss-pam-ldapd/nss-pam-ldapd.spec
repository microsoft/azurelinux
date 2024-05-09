Vendor:         Microsoft Corporation
Distribution:   Azure Linux
%global nssdir /%{_lib}
%global pamdir /%{_lib}/security

%define _hardened_build 1

Name:           nss-pam-ldapd
Version:        0.9.10
Release:        5%{?dist}
Summary:        An nsswitch module which uses directory servers
License:        LGPLv2+
URL:            https://arthurdejong.org/nss-pam-ldapd/
Source0:        https://arthurdejong.org/nss-pam-ldapd/nss-pam-ldapd-%{version}.tar.gz
Source1:        https://arthurdejong.org/nss-pam-ldapd/nss-pam-ldapd-%{version}.tar.gz.sig
Source3:        nslcd.tmpfiles
Source4:        nslcd.service

# Pylint tests fail w/o certain imports and are not needed for nslcd anyway,
# plus, we don't ship the python utilities
Patch0001:      0001-Disable-pylint-tests.patch
Patch0002:      0002-Watch-for-uint32_t-overflows.patch

BuildRequires:  gcc
BuildRequires:  openldap-devel, krb5-devel
BuildRequires:  autoconf, automake
BuildRequires:  pam-devel
BuildRequires:  systemd-units
%{?systemd_requires}

# Pull in nscd, which is recommended.
Recommends:     nscd

Obsoletes:      nss-ldapd < 0.7
Provides:       nss-ldapd = %{version}-%{release}

# Obsolete PADL's nss_ldap
Provides:       nss_ldap = 265-12
Obsoletes:      nss_ldap < 265-11

# Obsolete PADL's pam_ldap
Provides:       pam_ldap = 185-15
Obsoletes:      pam_ldap < 185-15

%description
The nss-pam-ldapd daemon, nslcd, uses a directory server to look up name
service information (users, groups, etc.) on behalf of a lightweight
nsswitch module.

%prep
%autosetup -p1
autoreconf -f -i

%build
%configure --libdir=%{nssdir} \
           --disable-utils \
           --with-pam-seclib-dir=%{pamdir}
%make_build

%check
make check

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/{%{_libdir},%{_unitdir}}
install -p -m644 %{SOURCE4} $RPM_BUILD_ROOT/%{_unitdir}/

ln -s libnss_ldap.so.2 $RPM_BUILD_ROOT/%{nssdir}/libnss_ldap.so

sed -i -e 's,^uid.*,uid nslcd,g' -e 's,^gid.*,gid ldap,g' \
$RPM_BUILD_ROOT/%{_sysconfdir}/nslcd.conf
touch -r nslcd.conf $RPM_BUILD_ROOT/%{_sysconfdir}/nslcd.conf
mkdir -p -m 0755 $RPM_BUILD_ROOT/var/run/nslcd
mkdir -p -m 0755 $RPM_BUILD_ROOT/%{_tmpfilesdir}
install -p -m 0644 %{SOURCE3} $RPM_BUILD_ROOT/%{_tmpfilesdir}/%{name}.conf

%files
%doc AUTHORS ChangeLog COPYING HACKING NEWS README TODO
%{_sbindir}/*
%{nssdir}/*.so*
%{pamdir}/pam_ldap.so
%{_mandir}/*/*
%attr(0600,root,root) %config(noreplace) %verify(not md5 size mtime) /etc/nslcd.conf
%attr(0644,root,root) %config(noreplace) %{_tmpfilesdir}/%{name}.conf
%{_unitdir}/nslcd.service
%attr(0775,nslcd,root) /var/run/nslcd

%pre
getent group  ldap  > /dev/null || \
/usr/sbin/groupadd -r -g 55 ldap
getent passwd nslcd > /dev/null || \
/usr/sbin/useradd -r -g ldap -c 'LDAP Client User' \
    -u 65 -d / -s /sbin/nologin nslcd 2> /dev/null || :

%post
# The usual stuff.
/sbin/ldconfig
%systemd_post nslcd.service

%preun
%systemd_preun nslcd.service

%postun
/sbin/ldconfig
%systemd_postun_with_restart nslcd.service

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.9.10-5
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.10-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Sep  3 2018 Jakub Hrozek <jhrozek@redhat.com> - 0.9.10-1
- New upstream release 0.9.10

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed May 30 2018 Jakub Hrozek <jhrozek@redhat.com> - 0.9.9-3
- Also change the pemissions on tmpfiles
- Related: rhbz#1583211 - nslcd, the local LDAP daemon, fails to start
                          with SELinux enabled

* Wed May 30 2018 Jakub Hrozek <jhrozek@redhat.com> - 0.9.9-2
- Apply a patch by Lukas Slebodnik to allow root to write to the
  /var/run/nslcd directory
- Resolves: rhbz#1583211 - nslcd, the local LDAP daemon, fails to start
                           with SELinux enabled

* Sun Apr  1 2018 Jakub Hrozek <jhrozek@redhat.com> - 0.9.9-1
- Upgrade to the latest upstream
  - Disable the python utilities
  - Don't bother with failing pylint test as we don't ship the python
    utilities
- Drop unused validname and exitcode patches, port strtoid overflow
  patch

* Sat Mar 31 2018 Jakub Hrozek <jhrozek@redhat.com> - 0.8.14-12
- Get rid of all conditions that are always true for both EPEL-7 and Fedora
  as it's quite unlikely we'd use this specfile on EPEL-6
- Remove the sysvinit script and all the scriptlets around it
- Unconditionally use systemd scriptlet macros and systemd_requires
- Unconditionally build the PAM module as the PADL module is long dead
- Remove the auto-migration of settings from nss_ldap as it's been
  long gone from Fedora
- Don't check /etc/sysconfig/authconfig as authconfig is on its way
  out from Fedora
- Use only spaces, not tabs, to stop my editor from looking like a
  Christmas tree
- Remove the obsolete Group stanza
- Make nscd Recommended, not Required

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.14-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.14-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.14-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Feb  8 2017 Jakub Hrozek <jhrozek@redhat.com> 0.8.14-8
- Apply a patch from Stanislav Moravec to fix nslcd return code

* Tue Mar 29 2016 Nalin Dahyabhai <nalin@redhat.com> 0.8.14-7
- move the packaged tmpfiles.d file from /etc/tmpfiles.d to %%{_tmpfilesdir},
  per heads-up from Ville Skyttä on devel@

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.14-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.14-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.14-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.14-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 07 2014 Nalin Dahyabhai <nalin@redhat.com> 0.8.14-2
- where we check for USELDAP=yes in /etc/sysconfig/authconfig as an indication
  of nss_ldap being in use, to decide whether to enable the nslcd service or
  not, also check for USELDAPAUTH=yes, which indicates pam_ldap is being used

* Sat Oct 05 2013 Jakub Hrozek <jhrozek@redhat.com>  0.8.14-1
- New upstream release 0.8.14
- Remove upstreamed patches

* Sat Oct 05 2013 Jakub Hrozek <jhrozek@redhat.com>  0.8.13-4
- Backport fixes for #1003011

* Sat Oct 05 2013 Jakub Hrozek <jhrozek@redhat.com>  0.8.13-3
- Build with _hardened_build macro

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon May  6 2013 Nalin Dahyabhai <nalin@redhat.com> 0.8.13-1
- update to 0.8.13
- correct a syntax error in the fix that was added for #832706

* Tue Apr 30 2013 Nalin Dahyabhai <nalin@redhat.com> 0.8.12-4
- in %%post, attempt to rewrite any instances of "map group uniqueMember ..."
  to be "map group member ..." in nslcd.conf, as the attribute name changed
  in 0.8.4 (via freeipa ticket #3589)

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.12-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jan 18 2013 Nalin Dahyabhai <nalin@redhat.com> 0.8.12-2
- drop local patch to make the client flush some more read buffers

* Fri Jan 18 2013 Nalin Dahyabhai <nalin@redhat.com> 0.8.12-1
- update to 0.8.12 (#846793)
- make building pam_ldap conditional on the targeted release
- add "After=named.service dirsrv.target slapd.service" to nslcd.service,
  to make sure that nslcd is started after them if they're to be started
  on the local system (#832706)
- alter the versioned Obsoletes: on pam_ldap to include the F18 package
- use %%{_unitdir} when deciding where to put systemd configuration, based
  on patch from Václav Pavlín (#850232)
- use new systemd macros for scriptlet hooks, when available, based on
  patch from Václav Pavlín (#850232)

* Sun Sep 09 2012 Jakub Hrozek <jhrozek@redhat.com> 0.7.17-1
- new upstream release 0.7.17

* Sun Aug 05 2012 Jakub Hrozek <jhrozek@redhat.com> - 0.7.16-5
- Obsolete PADL's nss_ldap

* Sat Aug 04 2012 Jakub Hrozek <jhrozek@redhat.com> - 0.7.16-4
- Build the PAM module, obsoletes PADL's pam-ldap (#856006)

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.16-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon May 14 2012 Jakub Hrozek <jhrozek@redhat.com> 0.7.16-2
- backport upstream revision r1659 related to broken pipe when
  requesting a large group
- use grep -E instead of egrep to avoid rpmlint warnings

* Sat Apr 28 2012 Jakub Hrozek <jhrozek@redhat.com> 0.7.16-1
- new upstream release 0.7.16

* Thu Mar 15 2012 Jakub Hrozek <jhrozek@redhat.com> 0.7.15-2
- Do not print "Broken Pipe" error message when requesting a large group

* Fri Mar 9 2012 Jakub Hrozek <jhrozek@redhat.com> 0.7.15-1
- new upstream release 0.7.15

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.14-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Dec 16 2011 Jakub Hrozek <jhrozek@redhat.com> 0.7.14-2
- Do not overflow large UID/GID values on 32bit architectures

* Mon Nov 28 2011 Nalin Dahyabhai <nalin@redhat.com>
- use the same conditional test for deciding when to create the .so symlink as
  we do later on for deciding when to include it in the package (#757004)

* Fri Sep 23 2011 Jakub Hrozek <jhrozek@redhat.com> 0.7.14-1
- new upstream release 0.7.14
- obsoletes nss-pam-ldapd-0.7.x-buffers.patch

* Wed Aug 24 2011 Nalin Dahyabhai <nalin@redhat.com> 0.7.13-8
- include backported enhancement to take URIs in the form "dns:DOMAIN" in
  addition to the already-implemented "dns" (#730309)

* Thu Jul 14 2011 Nalin Dahyabhai <nalin@redhat.com> 0.7.13-7
- switch to only munging the contents of /etc/nslcd.conf on the very first
  install (#706454)
- make sure that we have enough space to parse any valid GID value when
  parsing a user's primary GID (#716822)
- backport support for the "validnames" option from SVN and use it to allow
  parentheses characters by modifying the default setting (#690870), then
  modify the default again to also allow shorter and shorter names to pass
  muster (#706860)

* Wed Jul 13 2011 Nalin Dahyabhai <nalin@redhat.com> 0.7.13-6
- convert to systemd-native startup (#716997)

* Mon Jun 13 2011 Nalin Dahyabhai <nalin@redhat.com> 0.7.13-5
- change the file path Requires: we have for pam_ldap into a package name
  Requires: (#601931)

* Wed Mar 30 2011 Nalin Dahyabhai <nalin@redhat.com> 0.7.13-4
- tag nslcd.conf with %%verify(not md5 size mtime), since we always tweak
  it in %%post (#692225)

* Tue Mar  1 2011 Nalin Dahyabhai <nalin@redhat.com> 0.7.13-3
- add a tmpfiles configuration to ensure that /var/run/nslcd is created when
  /var/run is completely empty at boot (#656643)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Dec 13 2010 Nalin Dahyabhai <nalin@redhat.com> 0.7.13-1
- update to 0.7.13

* Fri Oct 29 2010 Nalin Dahyabhai <nalin@redhat.com> 0.7.12-1
- update to 0.7.12

* Fri Oct 15 2010 Nalin Dahyabhai <nalin@redhat.com> 0.7.11-1
- update to 0.7.11

* Wed Sep 29 2010 jkeating - 0.7.10-2
- Rebuilt for gcc bug 634757

* Fri Sep 24 2010 Nalin Dahyabhai <nalin@redhat.com> 0.7.10-1
- update to 0.7.10

* Thu Sep 23 2010 Nalin Dahyabhai <nalin@redhat.com> 0.7.9-2
- when creating /var/run/nslcd in the buildroot, specify that 0755 is a
  permissions value and not another directory name (#636880)

* Mon Aug 30 2010 Nalin Dahyabhai <nalin@redhat.com> 0.7.9-1
- update to 0.7.9

* Wed Aug 18 2010 Nalin Dahyabhai <nalin@redhat.com> 0.7.8-1
- update to 0.7.8

* Wed Jul  7 2010 Nalin Dahyabhai <nalin@redhat.com> 0.7.7-1
- update to 0.7.7

* Mon Jun 28 2010 Nalin Dahyabhai <nalin@redhat.com> 0.7.6-3
- don't accidentally set multiple 'gid' settings in nslcd.conf, and try to
  clean up after older versions of this package that did (#608314)

* Thu May 27 2010 Nalin Dahyabhai <nalin@redhat.com> 0.7.6-2
- make inclusion of the .so symlink conditional on being on a sufficiently-
  new Fedora where pam_ldap isn't part of the nss_ldap package, so having
  this package conflict with nss_ldap doesn't require that pam_ldap be
  removed (#596691)

* Thu May 27 2010 Nalin Dahyabhai <nalin@redhat.com> 0.7.6-1
- update to 0.7.6

* Mon May 17 2010 Nalin Dahyabhai <nalin@redhat.com> 0.7.5-3
- switch to the upstream patch for #592411

* Fri May 14 2010 Nalin Dahyabhai <nalin@redhat.com> 0.7.5-2
- don't return an uninitialized buffer as the value for an optional attribute
  that isn't present in the directory server entry (#592411)

* Fri May 14 2010 Nalin Dahyabhai <nalin@redhat.com> 0.7.5-1
- update to 0.7.5

* Fri May 14 2010 Nalin Dahyabhai <nalin@redhat.com> 0.7.4-1
- update to 0.7.4
- stop trying to migrate retry timeout parameters from old ldap.conf files
- add an explicit requires: on nscd to make sure it's at least available on
  systems that are using nss-pam-ldapd; otherwise it's usually optional

* Tue Mar 23 2010 Nalin Dahyabhai <nalin@redhat.com> 0.7.3-1
- update to 0.7.3

* Thu Feb 25 2010 Nalin Dahyabhai <nalin@redhat.com> 0.7.2-2
- bump release for post-review commit

* Thu Feb 25 2010 Nalin Dahyabhai <nalin@redhat.com> 0.7.2-1
- add comments about why we have a .so link at all, and not a -devel subpackage

* Wed Jan 13 2010 Nalin Dahyabhai <nalin@redhat.com>
- obsolete/provides nss-ldapd
- import configuration from nss-ldapd.conf, too

* Tue Jan 12 2010 Nalin Dahyabhai <nalin@redhat.com>
- rename to nss-pam-ldapd
- also check for import settings in /etc/nss_ldap.conf and /etc/pam_ldap.conf

* Thu Sep 24 2009 Nalin Dahyabhai <nalin@redhat.com> 0.6.11-2
- rebuild

* Wed Sep 16 2009 Nalin Dahyabhai <nalin@redhat.com> 
- apply Mitchell Berger's patch to clean up the init script, use %%{_initddir},
  and correct the %%post so that it only thinks about turning on nslcd when
  we're first being installed (#522947)
- tell status() where the pidfile is when the init script is called for that

* Tue Sep  8 2009 Nalin Dahyabhai <nalin@redhat.com>
- fix typo in a comment, capitalize the full name for "LDAP Client User" (more
  from #516049)

* Wed Sep  2 2009 Nalin Dahyabhai <nalin@redhat.com> 0.6.11-1
- update to 0.6.11

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.10-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jun 18 2009 Nalin Dahyabhai <nalin@redhat.com> 0.6.10-3
- update URL: and Source:

* Mon Jun 15 2009 Nalin Dahyabhai <nalin@redhat.com> 0.6.10-2
- add and own /var/run/nslcd
- convert hosts to uri during migration

* Thu Jun 11 2009 Nalin Dahyabhai <nalin@redhat.com> 0.6.10-1
- update to 0.6.10

* Fri Apr 17 2009 Nalin Dahyabhai <nalin@redhat.com> 0.6.8-1
- bump release number to 1 (part of #491767)
- fix which group we check for during %%pre (part of #491767)

* Tue Mar 24 2009 Nalin Dahyabhai <nalin@redhat.com>
- require chkconfig by package rather than path (Jussi Lehtola, part of #491767)

* Mon Mar 23 2009 Nalin Dahyabhai <nalin@redhat.com> 0.6.8-0.1
- update to 0.6.8

* Mon Mar 23 2009 Nalin Dahyabhai <nalin@redhat.com> 0.6.7-0.1
- start using a dedicated user

* Wed Mar 18 2009 Nalin Dahyabhai <nalin@redhat.com> 0.6.7-0.0
- initial package (#445965)
