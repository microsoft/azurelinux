# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:    realmd
Version: 0.17.1
Release: 18%{?dist}
Summary: Kerberos realm enrollment service
License: LGPL-2.1-or-later
URL:     https://gitlab.freedesktop.org/realmd/realmd
Source0: https://gitlab.freedesktop.org/realmd/realmd/uploads/204d05bd487908ece2ce2705a01d2b26/realmd-%{version}.tar.gz

Patch0001: 0001-service-allow-multiple-names-and-_srv_-ad_server-opt.patch
Patch0002: 0002-service-fix-error-message-when-removing-host-from-AD.patch
Patch0003: 0003-doc-fix-reference-in-realmd.conf-man-page.patch
Patch0004: 0001-sssd-package-fix.patch
Patch0005: 0001-tools-fix-ccache-handling-for-leave-operation.patch
Patch0006: 0001-ipa-Propagate-hostname-error.patch
Patch0007: 0001-configure.ac-Install-dbus-policy-in-usr-share-not-et.patch
Patch0008: 0001-Systemd-security-settings.patch
Patch0009: 0002-Disable-NoNewPrivileges-in-Systemd-service.patch
Patch0010: 0003-service-use-dnshostname-with-net-ads-join.patch
Patch0011: 0004-systemd-set-CacheDirectory.patch
Patch0012: 0005-Various-fixes-for-issues-found-by-static-code-scanne.patch
Patch0013: 0006-krb5-add-realm_krb5_get_error_message.patch
Patch0014: 0001-Initial-implementation-of-a-renew-request.patch
Patch0015: 0002-renew-implement-support-for-adcli.patch
Patch0016: 0003-service-use-proper-macro-for-os-name-and-os-version.patch
Patch0017: 0004-renew-fix-issues-found-by-Coverity.patch

BuildRequires: make
BuildRequires: gcc
BuildRequires: automake
BuildRequires: autoconf
BuildRequires: intltool pkgconfig
BuildRequires: gettext-devel
BuildRequires: glib2-devel >= 2.32.0
BuildRequires: openldap-devel
BuildRequires: polkit-devel
BuildRequires: krb5-devel
BuildRequires: systemd-devel
BuildRequires: libxslt
BuildRequires: xmlto
BuildRequires: python3
BuildRequires: samba-common-tools

Requires: authselect
Requires: polkit
Conflicts: realmd-devel-docs < %{version}-%{release}

%description
realmd is a DBus system service which manages discovery and enrollment in realms
and domains like Active Directory or IPA. The control center uses realmd as the
back end to 'join' a domain simply and automatically configure things correctly.

%package devel-docs
Summary: Developer documentation files for %{name}
Conflicts: realmd < %{version}-%{release}

%description devel-docs
The %{name}-devel package contains developer documentation for developing
applications that use %{name}.

%define _hardened_build 1

%prep
%autosetup -p1

%build
autoreconf -fi
%configure --disable-silent-rules \
%if 0%{?rhel}
    --with-vendor-error-message='Please check\n    https://red.ht/support_rhel_ad \nto get help for common issues.' \
%endif
    %{nil}

%make_build

%check
make check

%install
%make_install

%find_lang realmd

%post
%systemd_post realmd.service

%preun
%systemd_preun realmd.service

%postun
%systemd_postun_with_restart realmd.service

%files -f realmd.lang
%doc AUTHORS COPYING NEWS README
%{_datadir}/dbus-1/system.d/org.freedesktop.realmd.conf
%{_sbindir}/realm
%dir %{_prefix}/lib/realmd
%{_libexecdir}/realmd
%{_prefix}/lib/realmd/realmd-defaults.conf
%{_prefix}/lib/realmd/realmd-distro.conf
%{_unitdir}/realmd.service
%{_datadir}/dbus-1/system-services/org.freedesktop.realmd.service
%{_datadir}/polkit-1/actions/org.freedesktop.realmd.policy
%{_mandir}/man8/realm.8.gz
%{_mandir}/man5/realmd.conf.5.gz
%{_localstatedir}/cache/realmd/

%files devel-docs
%doc %{_datadir}/doc/realmd/
%doc ChangeLog

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.17.1-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Apr 24 2025 Sumit Bose <sbose@redhat.com> - 0.17.1-17
- Fix issues found by Coverity in renew code
  Resolves: jira#SSSD-8347

* Wed Apr 23 2025 Sumit Bose <sbose@redhat.com> - 0.17.1-16
- Add new renew option to renew the keytab
  Resolves: jira#SSSD-8347

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.17.1-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Nov 29 2024 Sumit Bose <sbose@redhat.com> - 0.17.1-14
- Various fixes for issues found by static code scanners
- Systemd security setting and CacheDirectory
- use 'dnshostname' with net ads join
- Install dbus policy in /usr/share, not /etc

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.17.1-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Mar 01 2024 Adam Williamson <awilliam@redhat.com> - 0.17.1-12
- Revert security hardening for now (it broke domain enrolment)

* Thu Feb 29 2024 Sumit Bose <sbose@redhat.com> - 0.17.1-11
- Update Systemd security settings as part of https://fedoraproject.org/wiki/Changes/SystemdSecurityHardening

* Mon Feb 26 2024 Sumit Bose <sbose@redhat.com> - 0.17.1-10
- Propagate FreeIPA hostname error
  Resolves: rhbz#2264944

* Fri Feb 09 2024 Sumit Bose <sbose@redhat.com> - 0.17.1-9
- fix ccache handling for leave operation
  Resolves: jira#SSSD-6420

* Mon Feb 05 2024 Sumit Bose <sbose@redhat.com> - 0.17.1-8
- improve sssd package handling due to removed sssd meta package
  Resolves: rhbz#2255725

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.17.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.17.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Dec 01 2023 Sumit Bose <sbose@redhat.com> - 0.17.1-5
- allow multiple names and _srv_ ad_server option
  Resolves: jira#SSSD-6077

* Wed Oct 18 2023 Sumit Bose <sbose@redhat.com> - 0.17.1-4
- migrated to SPDX license

* Wed Oct 18 2023 Tom Stellard <tstellar@redhat.com>
- Use make macros
- https://fedoraproject.org/wiki/Changes/UseMakeBuildInstallMacro

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.17.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.17.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Sep 29 2022 Sumit Bose <sbose@redhat.com> - 0.17.1-1
- Updated to upstream 0.17.1
  Resolves: rhbz#1628302

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.17.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Apr 25 2022 Andreas Schneider <asn@redhat.com> - 0.17.0-10
- resolves rhbz#2078447 - Fix detction for new samba commandline options

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.17.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Dec 15 2021 Sumit Bose <sbose@redhat.com> - 0.17.0-8
- Fix LDAP socket timeout, duplicate log messages and Samba CLI
  Resolves: rhbz#1817869, rhbz#2024248, rhbz#2028530

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.17.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue May 11 2021 Sumit Bose <sbose@redhat.com> - 0.17.0-6
- Add man page section, enable restart after update
  Resolves: rhbz#1926046

* Tue Apr 06 2021 Sumit Bose <sbose@redhat.com> - 0.17.0-5
- Add missing configure option
  Resolves: rhbz#1889386

* Tue Apr 06 2021 Sumit Bose <sbose@redhat.com> - 0.17.0-4
- Add vendor error message, autoconf-2.71 fixes, downstream gating
  Resolves: rhbz#1889386

* Wed Mar 03 2021 Sumit Bose <sbose@redhat.com> - 0.17.0-3
- Use authselect instead of authconfig
  Resolves: rhbz#1934124

* Sat Feb 20 2021 Sumit Bose <sbose@redhat.com> - 0.17.0-2
- Add Conflicts to avoid update/downgrade issues

* Fri Feb 19 2021 Sumit Bose <sbose@redhat.com> - 0.17.0-1
- Updated to upstream 0.17.0

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.16.3-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Nov 04 2020 Sumit Bose <sbose@redhat.com> - 0.16.3-27
- Sync with latest upstream patches

* Wed Aug 12 2020 Sumit Bose <sbose@redhat.com> - 0.16.3-25
- Sync with latest upstream patches

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.16.3-25
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.16.3-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Mar 18 2020 Sumit Bose <sbose@redhat.com> - 0.16.3-23
- Sync with latest upstream patches and fix package URL
  Resolves: rhbz#1800897

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.16.3-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Aug 02 2019 Sumit Bose <sbose@redhat.com> - 0.16.3-21
- Remove gtester support, use autosetup
  Resolves: rhbz#1736578

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.16.3-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Feb 21 2019 Sumit Bose <sbose@redhat.com> - 0.16.3-19
- fix test depending on order
  Resolves: rhbz#1675879

* Wed Feb 20 2019 Adam Williamson <awilliam@redhat.com> - 0.16.3-18
- Backport fix from upstream to always install latest packages via PK

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.16.3-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Sep 27 2018 Sumit Bose <sbose@redhat.com> - 0.16.3-16
- Do not call authselect for IPA domains
  Resolves: rhbz#1620097

* Tue Aug 21 2018 Sumit Bose <sbose@redhat.com> - 0.16.3-15
- Change IPA defaults and improve realm discovery
  Resolves: rhbz#1575538
  Resolves: rhbz#1145777

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.16.3-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jul 04 2018 Sumit Bose <sbose@redhat.com> - 0.16.3-13
- Drop python2 build dependency
- Add polkit runtime dependency
  Resolves: rhbz#1577178
- Fix documentation reference in systemd unit file
  Resolves: rhbz#1596323
- Use current Samba config options
  Resolves: rhbz#1482926

* Sun Mar 18 2018 René Genz <liebundartig@freenet.de> - 0.16.3-12
- use correct authselect syntax for *-disable-logins to fix rhbz#1558245
- Iryna Shcherbina <ishcherb@redhat.com>
  Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Thu Mar 01 2018 Sumit Bose <sbose@redhat.com> - 0.16.3-11
- Require authselect instead of authconfig, related: rhbz#1537246

* Tue Feb 20 2018 Sumit Bose <sbose@redhat.com> - 0.16.3-10
- added BuildRequires gcc
- Use authselect instead of authconfig, related: rhbz#1537246

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.16.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Sep 05 2017 Petr Pisar <ppisar@redhat.com> - 0.16.3-8
- Update all m4 macros to prevent from mismatching between Automake versions

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.16.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.16.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Apr 25 2017 Sumit Bose <sbose@redhat.com> - 0.16.3-5
- Resolves: rhbz#1445017

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.16.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Jan 19 2017 Merlin Mathesius <mmathesi@redhat.com> - 0.16.3-3
- Add BuildRequires: python to fix FTBFS (BZ#1415000).

* Tue Dec 13 2016 Sumit Bose <sbose@redhat.com> - 0.16.3-2
- Resolves: rhbz#1401605

* Wed Nov 30 2016 Sumit Bose <sbose@redhat.com> - 0.16.3-1
- Updated to upstream 0.16.3 plus patches from git master

* Fri Jun 03 2016 Sumit Bose <sbose@redhat.com> - 0.16.2-5
- properly apply patch for rhbz#1330766
- Resolves: rhbz#1330766

* Wed May 18 2016 Sumit Bose <sbose@redhat.com> - 0.16.2-4
- Resolves: rhbz#1330766

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.16.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Sep 11 2015 Stef Walter <stefw@redhat.com> - 0.16.2-2
- Fixed --computer-ou regression
- Show message when installing packages

* Fri Jul 31 2015 Stef Walter <stefw@redhat.com> - 0.16.2-1
- Updated to upstream 0.16.2
- Install to $prefix/lib instead of $libdir
- Resolves: rhbz#1246741

* Tue Jul 14 2015 Stef Walter <stefw@redhat.com> - 0.16.1-1
- Updated to upstream 0.16.1
- Resolves: rhbz#1231128

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.16.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Apr 14 2015 Stef Walter <stefw@redhat.com> - 0.16.0-1
- Updated to upstream 0.16.0
- Resolves: rhbz#1205753
- Resolves: rhbz#1142190
- Resolves: rhbz#1061091
- Resolves: rhbz#1205752

* Thu Apr 09 2015 Stephen Gallagher <sgallagh@redhat.com> - 0.15.2-2
- Resolves: rhbz#1210483

* Mon Oct 06 2014 Stef Walter <stefw@redhat.com> - 0.15.2-1
- Update to upstream 0.15.2

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.15.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.15.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat May 31 2014 Peter Robinson <pbrobinson@fedoraproject.org> 0.15.1-2
- Move ChangeLog to devel-docs. NEWS is probably riveting enough for users

* Fri May 23 2014 Stef Walter <stefw@redhat.com> - 0.15.1-1
- Update to upstream 0.15.1
- Remove the packagekit patch that's now integrated upstream

* Thu Jan 30 2014 Richard Hughes <rhughes@redhat.com> - 0.15.0-2
- Rebuild for libpackagekit-glib soname bump

* Tue Jan 07 2014 Stef Walter <stefw@redhat.com> - 0.15.0-1
- Update to upstream 0.15.0 release, fixing various bugs

* Mon Sep 09 2013 Stef Walter <stefw@redhat.com> - 0.14.6-1
- Update to upstream 0.14.6 point release
- Set 'kerberos method = system keytab' in smb.conf properly
- Limit Netbios name to 15 chars when joining AD domain

* Thu Aug 15 2013 Stef Walter <stefw@redhat.com> - 0.14.5-1
- Update to upstream 0.14.5 point release
- Fix regression conflicting --unattended and -U as in --user args
- Pass discovered server address to adcli tool

* Wed Aug 07 2013 Stef Walter <stefw@redhot.com> - 0.14.4-1
- Update to upstream 0.14.4 point release
- Fix up the [sssd] section in sssd.conf if it's screwed up
- Add an --unattended argument to realm command line client
- Clearer 'realm permit' manual page example

* Wed Aug 07 2013 Stef Walter <stefw@redhot.com> - 0.14.3-1
- Update to upstream 0.14.3 point release
- Populate LoginFormats correctly [#961442]
- Documentation clarifications
- Set sssd.conf default_shell per domain
- Notify in terminal output when installing packages
- If joined via adcli, delete computer with adcli too [#961244]
- If input is not a tty, read from stdin without getpass() [#983153]
- Configure pam_winbind.conf appropriately [#983153]
- Refer to FreeIPA as IPA
- Support use of kerberos ccache to join when winbind

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.14.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul 15 2013 Stef Walter <stefw@redhat.com> - 0.14.2-4
- Build with verbose automake output

* Tue Jun 11 2013 Stef Walter <stefw@redhat.com> - 0.14.2-3
- Run test suite when building the package
- Fix rpmlint errors

* Thu Jun 06 2013 Stef Walter <stefw@redhat.com> - 0.14.2-2
- Install oddjobd and oddjob-mkhomedir when joining domains [#969441]

* Mon May 27 2013 Stef Walter <stefw@redhat.com> - 0.14.2-1
- Update to upstream 0.14.2 version
- Discover FreeIPA 3.0 with AD trust correctly [#966148]
- Only allow joining one realm by default [#966650]
- Enable the oddjobd service after joining a domain [#964971]
- Remove sssd.conf allow lists when permitting all [#965760]
- Add dependency on authconfig [#964675]
- Remove glib-networking dependency now that we no longer use SSL.

* Mon May 13 2013 Stef Walter <stefw@redhat.com> - 0.14.1-1
- Update to upstream 0.14.1 version
- Fix crasher/regression using passwords with joins [#961435]
- Make second Ctrl-C just quit realm tool [#961325]
- Fix critical warning when leaving IPA realm [#961320]
- Don't print out journalctl command in obvious situations [#961230]
- Document the --all option to 'realm discover' [#961279]
- No need to require sssd-tools package [#961254]
- Enable services even in install mode [#960887]
- Use the AD domain name in sssd.conf directly [#960270]
- Fix critical warning when service Release() method [#961385]

* Mon May 06 2013 Stef Walter <stefw@redhat.com> - 0.14.0-1
- Work around broken krb5 with empty passwords [#960001]
- Add manual page for realmd.conf [#959357]
- Update to upstream 0.14.0 version

* Thu May 02 2013 Stef Walter <stefw@redhat.com> - 0.13.91-1
- Fix regression when using one time password [#958667]
- Support for permitting logins by group [#887675]

* Mon Apr 29 2013 Stef Walter <stefw@redhat.com> - 0.13.90-1
- Add option to disable package-kit installs [#953852]
- Add option to use unqualified names [#953825]
- Better discovery of domains [#953153]
- Concept of managing parts of the system [#914892]
- Fix problems with cache directory [#913457]
- Clearly explain when realm cannot be joined [#878018]
- Many other upstream enhancements and fixes

* Wed Apr 17 2013 Stef Walter <stefw@redhat.com> - 0.13.3-2
- Add missing glib-networking dependency, currently used
  for FreeIPA discovery [#953151]

* Wed Apr 17 2013 Stef Walter <stefw@redhat.com> - 0.13.3-1
- Update for upstream 0.13.3 version
- Add dependency on systemd for installing service file

* Tue Apr 16 2013 Stef Walter <stefw@redhat.com> - 0.13.2-2
- Fix problem with sssd not starting after joining

* Mon Feb 18 2013 Stef Walter <stefw@redhat.com> - 0.13.2-1
- Update to upstream 0.13.2 version

* Mon Feb 18 2013 Stef Walter <stefw@redhat.com> - 0.13.1-1
- Update to upstream 0.13.1 version for bug fixes

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Nov 12 2012 Stef Walter <stefw@redhat.com> - 0.12-1
- Update to upstream 0.12 version for bug fixes

* Tue Oct 30 2012 Stef Walter <stefw@redhat.com> - 0.11-1
- Update to upstream 0.11 version

* Sat Oct 20 2012 Stef Walter <stefw@redhat.com> - 0.10-1
- Update to upstream 0.10 version

* Wed Oct 17 2012 Stef Walter <stefw@redhat.com> - 0.9-1
- Update to upstream 0.9 version

* Wed Sep 19 2012 Stef Walter <stefw@redhat.com> - 0.8-2
- Add openldap-devel build requirement

* Wed Sep 19 2012 Stef Walter <stefw@redhat.com> - 0.8-1
- Update to upstream 0.8 version
- Add support for translations

* Mon Aug 20 2012 Stef Walter <stefw@redhat.com> - 0.7-2
- Build requires gtk-doc

* Mon Aug 20 2012 Stef Walter <stefw@redhat.com> - 0.7-1
- Update to upstream 0.7 version
- Remove files no longer present in upstream version
- Put documentation in its own realmd-devel-docs subpackage
- Update upstream URLs

* Mon Aug 6 2012 Stef Walter <stefw@redhat.com> - 0.6-1
- Update to upstream 0.6 version

* Tue Jul 17 2012 Stef Walter <stefw@redhat.com> - 0.5-2
- Remove missing SssdIpa.service file from the files list.
  This file will return upstream in 0.6

* Tue Jul 17 2012 Stef Walter <stefw@redhat.com> - 0.5-1
- Update to upstream 0.5 version

* Tue Jun 19 2012 Stef Walter <stefw@redhat.com> - 0.4-1
- Update to upstream 0.4 version
- Cleanup various rpmlint warnings

* Tue Jun 19 2012 Stef Walter <stefw@redhat.com> - 0.3-2
- Add doc files
- Own directories
- Remove obsolete parts of spec file
- Remove explicit dependencies
- Updated License line to LGPLv2+

* Tue Jun 19 2012 Stef Walter <stefw@redhat.com> - 0.3
- Build fixes

* Mon Jun 18 2012 Stef Walter <stefw@redhat.com> - 0.2
- Initial RPM
