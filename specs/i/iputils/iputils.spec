# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global _hardened_build 1

Summary: Network monitoring tools including ping
Name: iputils
Version: 20250605
Release: 1%{?dist}
# some parts are under the original BSD (ping.c)
# some are under GPLv2+ (tracepath.c)
License: BSD-4-Clause-UC AND GPL-2.0-or-later
URL: https://github.com/iputils/iputils

Source0: https://github.com/iputils/iputils/archive/%{version}/%{name}-%{version}.tar.gz
Source1: ifenslave.tar.gz
# Taken from ping.c on 2014-07-12
Source4: bsd.txt
Source5: https://www.gnu.org/licenses/old-licenses/gpl-2.0.txt

Patch100: iputils-ifenslave.patch
Patch101: iputils-ifenslave-CWE-170.patch

BuildRequires: gcc
BuildRequires: meson
BuildRequires: gettext
BuildRequires: glibc-kernheaders >= 2.4-8.19
BuildRequires: libidn2-devel
BuildRequires: libcap-devel
BuildRequires: libxslt docbook5-style-xsl
BuildRequires: systemd
BuildRequires: iproute
%{?systemd_ordering}
Provides: /bin/ping
Provides: /bin/ping6
Provides: /sbin/arping

%description
The iputils package contains basic utilities for monitoring a network,
including ping. The ping command sends a series of ICMP protocol
ECHO_REQUEST packets to a specified network host to discover whether
the target machine is alive and receiving network traffic.

%prep
%autosetup -a 1 -n %{name}-%{version} -p1
cp %{SOURCE4} %{SOURCE5} .

%build
%meson
%meson_build
gcc $RPM_OPT_FLAGS $CFLAGS $RPM_LD_FLAGS $LDFLAGS ifenslave.c -o ifenslave

%install
%meson_install
%find_lang %{name}

mkdir -p ${RPM_BUILD_ROOT}%{_sbindir}
ln -sf --relative ${RPM_BUILD_ROOT}%{_bindir}/ping ${RPM_BUILD_ROOT}%{_sbindir}/ping6
ln -sf --relative ${RPM_BUILD_ROOT}%{_bindir}/tracepath ${RPM_BUILD_ROOT}%{_sbindir}/tracepath6
%if "%{_sbindir}" != "%{_bindir}"
ln -sf --relative ${RPM_BUILD_ROOT}%{_bindir}/ping ${RPM_BUILD_ROOT}%{_sbindir}/
ln -sf --relative ${RPM_BUILD_ROOT}%{_bindir}/tracepath ${RPM_BUILD_ROOT}%{_sbindir}/
ln -sf --relative ${RPM_BUILD_ROOT}%{_bindir}/arping ${RPM_BUILD_ROOT}%{_sbindir}/
%endif

echo ".so man8/ping.8" > ${RPM_BUILD_ROOT}%{_mandir}/man8/ping6.8
echo ".so man8/tracepath.8" > ${RPM_BUILD_ROOT}%{_mandir}/man8/tracepath6.8
install -cp ifenslave ${RPM_BUILD_ROOT}%{_sbindir}/
install -cp ifenslave.8 ${RPM_BUILD_ROOT}%{_mandir}/man8/

%files -f %{name}.lang
%doc README.bonding
%license bsd.txt gpl-2.0.txt
%attr(0755,root,root) %caps(cap_net_raw=p) %{_bindir}/clockdiff
%attr(0755,root,root) %caps(cap_net_raw=p) %{_bindir}/arping
%attr(0755,root,root) %{_bindir}/ping
%{_sbindir}/ifenslave
%{_bindir}/tracepath
%{_sbindir}/ping6
%{_sbindir}/tracepath6
%if "%{_sbindir}" != "%{_bindir}"
%{_sbindir}/ping
%{_sbindir}/tracepath
%{_sbindir}/arping
%endif
%attr(644,root,root) %{_mandir}/man8/clockdiff.8*
%attr(644,root,root) %{_mandir}/man8/arping.8*
%attr(644,root,root) %{_mandir}/man8/ping.8*
%{_mandir}/man8/ping6.8*
%attr(644,root,root) %{_mandir}/man8/tracepath.8*
%{_mandir}/man8/tracepath6.8*
%attr(644,root,root) %{_mandir}/man8/ifenslave.8*

%changelog
* Wed Aug 06 2025 Kevin Fenzi <kevin@scrye.com> - 20250605-1
- Update to 20250605 to fix regression with ping -c1 (fixes rhbz#2384212 )

* Fri Jul 25 2025 Jan Macku <jamacku@redhat.com> - 20250602-3
- remove build dependency on openssl-devel removed in s20200821

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 20250602-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sun Jul 13 2025 Kevin Fenzi <kevin@scrye.com> - 20250602-1
- Update to 20250602. Fixes rhbz#2369782

* Sat May 17 2025 Kevin Fenzi <kevin@scrye.com> - 20240905-4
- Add upstream patch for CVE-2025-47268.

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 20240905-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sun Jan 12 2025 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 20240905-2
- Rebuilt for the bin-sbin merge (2nd attempt)

* Sat Sep 07 2024 Kevin Fenzi <kevin@scrye.com> - 20240905-1
- Update to 20240905. Fixes rhbz#2310191

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 20240117-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Jul 09 2024 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 20240117-5
- Rebuilt for the bin-sbin merge

* Sun Feb 11 2024 Kevin Fenzi <kevin@scrye.com> - 20240117-4
- Fix sources. Fixes rhbz#2263028

* Mon Jan 29 2024 Fedora Release Engineering <releng@fedoraproject.org> - 20240117-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 20240117-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Kevin Fenzi <kevin@scrye.com> - 20240117-1
- Update to 20240117. Fixes rhbz#2258910

* Sat Jan 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 20231222-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Dec 27 2023 Kevin Fenzi <kevin@scrye.com> - 20231222-1
- Update to 20231222. Fixes rhbz#2255687
- Fix PatchN warnings

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 20221126-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Apr 12 2023 Lukáš Zaoral <lzaoral@redhat.com> - 20221126-3
- migrate to SPDX license format

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 20221126-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sun Nov 27 2022 Kevin Fenzi <kevin@scrye.com> - 20221126-1
- Update to 20221126. Fixes rhbz#2148690

* Fri Nov 25 2022 Jan Macku <jamacku@redhat.com> - 20211215-4
- Build iputils and ifenslave with correct flags provided by Fedora

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 20211215-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 20211215-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Dec 16 2021 Kevin Fenzi <kevin@scrye.com> - 20211215-1
- Update to 20211215. Fixes rhbz#2033161

* Sun Jul 25 2021 Kevin Fenzi <kevin@scrye.com> - 20210722-1
- Update to 20210722. Fixes rhbz#1985117

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 20210202-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Mar 23 2021 Jan Macku <jamacku@redhat.com> - 20210202-3
- ifenslave: fix CWE-170 (related to rhbz#1938746)

* Tue Mar 02 2021 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 20210202-2
- Rebuilt for updated systemd-rpm-macros
  See https://pagure.io/fesco/issue/2583.

* Tue Feb 02 2021 Kevin Fenzi <kevin@scrye.com> - 20210202-1
- Update to 20210202. Fixes rhbz#1923917

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 20200821-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sat Oct 31 2020 Kevin Fenzi <kevin@scrye.com> - 20200821-1
- Update to 20200821 release. Fixes bug #1871310

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 20190515-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon May 18 2020 Jan Synáček <jsynacek@redhat.com> - 20190515-7
- arping exits with error when should not (#1836607)

* Mon Mar  2 2020 Jan Synáček <jsynacek@redhat.com> - 20190515-6
- Make ping unprivileged (#1699497)

* Mon Feb  3 2020 Jan Synáček <jsynacek@redhat.com> - 20190515-5
- Symlink arping to /usr/sbin/arping to maintain backward compatibility (#1797525)

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 20190515-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 20190515-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed May 22 2019 Jan Synáček <jsynacek@redhat.com> - 20190515-2
- Mark localization files correctly (#1712514)

* Wed May 22 2019 Jan Synáček <jsynacek@redhat.com> - 20190515-1
- Update to s20190515 (#1710647)

* Thu Mar 28 2019 Jan Synáček <jsynacek@redhat.com> - 20190324-1
- Update to s20190324 (#1692136)

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 20180629-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Jan 23 2019 Bogdan Dobrelya <bdobreli@redhat.com> - 20180629-3
- Use systemd_ordering macro

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 20180629-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jul  3 2018 Jan Synáček <jsynacek@redhat.com> - 20180629-1
- update to s20180629 (#1596893)

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 20161105-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Nov 24 2017 Jan Synáček <jsynacek@redhat.com> - 20161105-8
- switch to libidn2 (#1449149)

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 20161105-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Sun Jul 30 2017 Florian Weimer <fweimer@redhat.com> - 20161105-6
- Rebuild with binutils fix for ppc64le (#1475636)

* Thu Jul 27 2017 Jan Synáček <jsynacek@redhat.com> - 20161105-5
- ping does not work in dkr images (#1350019)

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 20161105-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri May 12 2017 Karsten Hopp <karsten@redhat.com> - 20161105-3
- don't build docs for module builds to limit dependencies

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 20161105-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Nov  8 2016 Jan Synáček <jsynacek@redhat.com> - 20161105-1
- Update to s20161105 (#1392759)

* Thu Oct 13 2016 Tomáš Mráz <tmraz@redhat.com> -  20160308-4
- rebuild with OpenSSL 1.1.0

* Wed Jun 22 2016 Jan Synáček <jsynacek@redhat.com> - 20160308-3
- Fix: Failed to bind to device (#1348934)

* Wed Mar  9 2016 Jan Synáček <jsynacek@redhat.com> - 20160308-2
- Don't build against libnettle

* Wed Mar  9 2016 Jan Synáček <jsynacek@redhat.com> - 20160308-1
- Update to s20160308 (#1315975)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 20150815-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Nov 19 2015 Jan Synáček <jsynacek@redhat.com> - 20150815-2
- Fix: Always use POSIX locale when parsing -i (#1283277)

* Thu Sep 24 2015 Jan Synáček <jsynacek@redhat.com> - 20150815-1
- Update to s20150815 (#617934)

* Sun Aug 23 2015 Peter Robinson <pbrobinson@fedoraproject.org> 20140519-6
- Don't depend on chkconfig, uses systemctl now

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20140519-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20140519-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jul 12 2014 Tom Callaway <spot@fedoraproject.org> - 2040519-3
- fix license handling

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20140519-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue May 20 2014 Jan Synáček <jsynacek@redhat.com> - 20140519-1
- Update to iputils-s20140519 (#1096617)

* Fri Apr 11 2014 Jan Synáček <jsynacek@redhat.com> - 20121221-10
- Fix arping hang if SIGALRM is blocked (#1085971)

* Wed Mar 26 2014 Jan Synáček <jsynacek@redhat.com> - 20121221-9
- Fix message flood when EPERM is encountered in ping (#1061867)

* Mon Feb  3 2014 Jan Synáček <jsynacek@redhat.com> - 20121221-8
- reference documentation in the service files
- remove redundant sysconfig-related stuff
- remove sysvinit script

* Tue Jan 21 2014 Jan Synáček <jsynacek@redhat.com> - 20121221-7
- Build with pie/full RELRO (#1055742)

* Sun Jan 19 2014 Ville Skyttä <ville.skytta@iki.fi> - 20121221-6
- Don't order services after syslog.target.

* Thu Oct 31 2013 Jan Synáček <jsynacek@redhat.com> - 20121221-5
- Harden the package even more (full RELRO)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20121221-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul 15 2013 Jan Synáček <jsynacek@redhat.com> - 20121221-3
- Harden the package

* Fri Feb 01 2013 Jan Synáček <jsynacek@redhat.com> - 20121221-2
- Always use posix locale when reading -i (#905840)
- Set correct ninfod capabilities

* Mon Jan 07 2013 Jan Synáček <jsynacek@redhat.com> - 20121221-1
- Update to iputils-s20121207 (#890397) and remove unnecessary patches

* Fri Dec 07 2012 Jan Synáček <jsynacek@redhat.com> - 20121207-1
- Update to iputils-s20121207 (#884983) - fixes a ping segfault introduced
  by the previous update
- Update ninfod-minor patch
- Renumber patches
- Fix -F switch (flowlabel patch)

* Thu Dec 06 2012 Jan Synáček <jsynacek@redhat.com> - 20121205-1
- Update to iputils-s20121205 (#884436) and remove unnecessary patches

* Thu Dec 06 2012 Jan Synáček <jsynacek@redhat.com> - 20121125-3
- Package ninfod (#877530)
- Update systemd requirements

* Mon Nov 26 2012 Jan Synáček <jsynacek@redhat.com> - 20121125-2
- Comment patches and cleanup
- Update ifaddrs patch
- Call usage() before limiting capabilities
- Correct ifaddrs patch
- Drop corr_type patch (gcc 4.4 build hack)
- Fix missing end tags in sgml documentation

* Mon Nov 26 2012 Jan Synáček <jsynacek@redhat.com> - 20121125-1
- Update to iputils-s20121125 (#879952)

* Mon Nov 26 2012 Jan Synáček <jsynacek@redhat.com> - 20121121-2
- Re-fix arping's default device search logic (#879807)

* Thu Nov 22 2012 Jan Synáček <jsynacek@redhat.com> - 20121121-1
- Update to iputils-s20121121, drop unnecessary patches
- Add capabilities to clockdiff and arping
- Renumber patches
- Fix arping's default device search logic

* Mon Nov 19 2012 Jan Synáček <jsynacek@redhat.com> - 20121112-2
- Update License field

* Tue Nov 13 2012 Jan Synáček <jsynacek@redhat.com> - 20121112-1
- Update to iputils-s20121112 (#875767)
  + drop unnecessary patches
  + update patches
  + wrap SO_BINDTODEVICE with the correct capability
  + fix incorrect free (hits when -lidn is used)

* Thu Nov 08 2012 Jan Synáček <jsynacek@redhat.com> - 20121106-2
- Update ifenslave tarball (#859182)

* Tue Nov 06 2012 Jan Synáček <jsynacek@redhat.com> - 20121106-1
- Update to iputils-s20121106 (#873571) and update patches

* Mon Oct 15 2012 Jan Synáček <jsynacek@redhat.com> - 20121011-1
- Update to iputils-s20121011
  + drop unnecessary patches
  + update patches
  + improve spec

* Wed Aug 22 2012 Jan Synáček <jsynacek@redhat.com> - 20101006-18
- Improve spec for fedora
- Add systemd-rpm macros (#850167)

* Mon Jul 23 2012 Jan Synáček <jsynacek@redhat.com> 20101006-17
- Minor update: capabilities patch

* Fri Jul 20 2012 Jan Synáček <jsynacek@redhat.com> 20101006-16
- Make fedora-review friendly

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20101006-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 25 2012 Jan Synáček <jsynacek@redhat.com> 20101006-15
- Ping fixes:
  + enable marking packets when the correct capabilities are set (#802197)
  + integer overflow (#834661)
  + Fallback to numeric addresses while exiting (#834661)

* Wed Jan 25 2012 Harald Hoyer <harald@redhat.com> 20101006-14
- install everything in /usr
  https://fedoraproject.org/wiki/Features/UsrMove

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20101006-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Nov 24 2011 Jiri Skala <jskala@redhat.com> - 20101006-12
- fixes #756439 - ping Record Route report incorrect (same route)

* Thu Nov 10 2011 Jiri Skala <jskala@redhat.com> - 20101006-11
- fixes #752397 - arping uses eth0 as default interface

* Mon Aug 01 2011 Jiri Skala <jskala@redhat.com> - 20101006-10
- rebuild for libcap

* Mon Jun 27 2011 Jiri Skala <jskala@redhat.com> - 20101006-9
- fixes #697532 - The SysV initscript should be packaged into subpackage

* Tue Mar 29 2011 Jiri Skala <jskala@redhat.com> - 20101006-8
- fixes #663734 - ping/ping6 man page fixes
- fixes #673831 - tracepath/tracepath6 manpage fixes

* Wed Feb 09 2011 Jiri Skala <jskala@redhat.com> - 20101006-7
- fixes build errors due to unused variables

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20101006-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jan 19 2011 Jiri Skala <jskala@redhat.com> - 20101006-5
- fixes #670380 - added /etc/sysconfig/rdisc, modified initscript
- initscript moved to git

* Wed Dec 15 2010 Jiri Skala <jskala@redhat.com> - 20101006-4
- fixes #662720 - Providing native systemd file
- freeing memory when capabilities are dropped

* Mon Nov 08 2010 Jiri Skala <jskala@redhat.com> - 20101006-3
- applied patch dropping capabilities of Ludwig Nussel
- fixes building ping, pinpg6 with -pie option
- moves most CFLAGS options from spec to Makefile

* Wed Oct 27 2010 Jiri Skala <jskala@redhat.com> - 20101006-2
- fixes #646444 - Replace SETUID in spec file with the correct file capabilities

* Mon Oct 11 2010 Jiri Skala <jskala@redhat.com> - 20101006-1
- update to latest upstream

* Tue Jul 13 2010 Jiri Skala <jskala@redhat.com> - 20100418-3
- applied patch preventing ping against dos attack

* Wed May 19 2010 Jiri Skala <jskala@redhat.com> - 20100418-2
- fixes #593641 - update bonding files (updated ifenslave tarball)

* Tue Apr 20 2010 Jiri Skala <jskala@redhat.com> - 20100418-1
- update to latest upstream
- enables flowlabel feature (-F option)

* Fri Mar 05 2010 Jiri Skala <jskala@redhat.com> - 20071127-10
- fixes #557308 - arping ignores the deadline option

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20071127-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Jiri Skala <jskala@redhat.com> - 20071127-8
- remake type conversions to gcc4.4 requirements

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20071127-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Sep 26 2008 Jiri Skala <jskala@redhat.com> - 20071127-6
- #455713 not accepted - suid is back

* Fri Aug 15 2008 Jiri Skala <jskala@redhat.com> - 20071127-5
- removed a dependency on libsysfs library in arping

* Wed Aug 06 2008 Jiri Skala <jskala@redhat.com> - 20071127-4
- Resolves: #455713 remove suid from ping
- corrected typing error in man

* Tue Jun 03 2008 Martin Nagy <mnagy@redhat.com> - 20071127-3
- major patch cleanup so it will be easier to get patches upstream
- fix for #68212, previous fix actually didn't work for ping6
- renewed the ia64 align patches
- update README.bonding
- clear up the code from warnings
- spec file cleanup

* Tue Mar 25 2008 Martin Nagy <mnagy@redhat.com> - 20071127-2
- fix inconsistent behaviour of ping (#360881)

* Mon Feb 25 2008 Martin Nagy <mnagy@redhat.com> - 20071127-1
- update to new upstream version

* Mon Feb 18 2008 Martin Nagy <mnagy@redhat.com> - 20070202-9
- rebuild

* Mon Feb 18 2008 Martin Nagy <mnagy@redhat.com> - 20070202-8
- correctly fix the -w option and return code of arping (#387881)

* Fri Feb 01 2008 Martin Nagy <mnagy@redhat.com> - 20070202-7
- fix -Q option of ping6 (#213544)

* Mon Jan 14 2008 Martin Nagy <mnagy@redhat.com> - 20070202-6
- fix absolute symlinks and character encoding for RELNOTES (#225909)
- preserve file timestamps (#225909)
- use %%{?_smp_mflags} (#225909)
- fix service rdisc stop removing of lock file

* Fri Sep 14 2007 Martin Bacovsky <mbacovsk@redhat.com> - 20070202-5
- rebuild

* Fri Aug  3 2007 Martin Bacovsky <mbacovsk@redhat.com> - 20070202-4
- resolves: #236725: ping does not work for subsecond intervals for ordinary user
- resolves: #243197: RFE: Please sync ifenslave with current kernel
- resolves: #246954: Initscript Review
- resolves: #251124: can't build rdisc - OPEN_MAX undeclared

* Fri Apr  6 2007 Martin Bacovsky <mbacovsk@redhat.com> - 20070202-3
- resolves: #235374: Update of iputils starts rdisc, breaking connectivity 

* Tue Mar 27 2007 Martin Bacovsky <mbacovsk@redhat.com> - 20070202-2
- Resolves: #234060: [PATCH] IDN (umlaut domains) support for ping and ping6
  patch provided by Robert Scheck <redhat@linuxnetz.de>

* Thu Mar 15 2007 Martin Bacovsky <mbacovsk@redhat.com> - 20070202-1
- upgarde to new upstream iputils-s20070202
- Resolves: #229995
- Resolves: #225909 - Merge Review: iputils
- patches revision

* Thu Feb 22 2007 Martin Bacovsky <mbacovsk@redhat.com>- 20020927-42
- Resolves: #218706 - now defines the destination address along RFC3484
- Resolves: #229630 - ifenslave(8) man page added
- Resolves: #213716 - arping doesn't work on InfiniBand ipoib interfaces
 
* Wed Sep 13 2006 Radek Vokal <rvokal@redhat.com> - 20020927-41
- new ifenslave/bonding documentation

* Mon Aug 21 2006 Martin Bacovsky <mbacovsk@redhat.com> - 20020927-40 
- tracepath doesn't continue past destination host (#174032) 
  previous patch replaced by new one provided by <mildew@gmail.com>
  option -c added

* Mon Jul 17 2006 Radek Vokal <rvokal@redhat.com> - 20020927-39
- rebuilt

* Mon Jul 10 2006 Radek Vokal <rvokal@redhat.com> - 20020927-38
- tracepath doesn't continue past destination host (#174032) <mildew@gmail.com>

* Wed Mar 29 2006 Radek Vokál <rvokal@redhat.com> - 20020927-37
- fix ifenslave, shows interface addresses
- add RPM_OPT_FLAGS to ifenslave
 
* Sun Mar 12 2006 Radek Vokál <rvokal@redhat.com> - 20020927-36
- fix ifenslave man page (#185223)

* Fri Feb 24 2006 Radek Vokál <rvokal@redhat.com> - 20020927-35
- add PreReq: chkconfig (#182799,#182798)

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 20020927-34.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 20020927-34.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Mon Feb 06 2006 Radek Vokál <rvokal@redhat.com> 20020927-34
- ping clean-up, added new ICMP warning messages

* Wed Jan 25 2006 Radek Vokál <rvokal@redhat.com> 20020927-33
- gcc patch, warnings cleaned-up

* Tue Dec 13 2005 Radek Vokal <rvokal@redhat.com> 20020927-32
- fix HOPLIMIT option for setsockopt() (#175471)

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Mon Dec 05 2005 Radek Vokal <rvokal@redhat.com> 20020927-31
- ifenslave.8 from debian.org
- separate ifenslave to its own tarball

* Tue Nov 08 2005 Radek Vokal <rvokal@redhat.com> 20020927-30
- don't ship traceroute6, now part of traceroute package

* Wed Oct 05 2005 Radek Vokal <rvokal@redhat.com> 20020927-29
- add ping6 and tracepath6 manpages, fix attributes. 

* Fri Sep 30 2005 Radek Vokal <rvokal@redhat.com> 20020927-28
- memset structure before using it (#168166)

* Mon Sep 26 2005 Radek Vokal <rvokal@redhat.com> 20020927-27
- fixed ping -f, flooding works again (#134859,#169141)

* Thu Sep 08 2005 Radek Vokal <rvokal@redhat.com> 20020927-26
- tracepath6 and tracepath fix, use getaddrinfo instead of gethostbyname(2) 
  (#100778,#167735)

* Fri Aug 12 2005 Radek Vokal <rvokal@redhat.com> 20020927-25
- fixed arping timeout (#165715)

* Mon Jul 18 2005 Radek Vokal <rvokal@redhat.com> 20020927-24
- fixed arping buffer overflow (#163383)

* Fri May 27 2005 Radek Vokal <rvokal@redhat.com> 20020927-23
- fixed un-initialized "device" (#158914)

* Thu Apr 07 2005 Radek Vokal <rvokal@redhat.com> 20020927-22
- don't start rdisc as default (#154075)

* Tue Apr 05 2005 Radek Vokal <rvokal@redhat.com> 20020927-21
- rdisc init script added (#151614)

* Fri Mar 04 2005 Radek Vokal <rvokal@redhat.com> 20020927-20
- arping fix for infiniband (#150156)

* Tue Dec 07 2004 Radek Vokal <rvokal@redhat.com> 20020927-19
- return values fixed - patch from suse.de

* Mon Oct 18 2004 Radek Vokal <rvokal@redhat.com>
- ifenslave.c and README.bonding updated from kernel-2.6.8-1.521 (#136059)

* Mon Oct 11 2004 Radek Vokal <rvokal@redhat.com>
- spec file updated, source fixed (#135193)

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed May 12 2004 Phil Knirsch <pknirsch@redhat.com> 20020927-15
- Updated rh patch to enable PIE build of binaries.

* Thu Apr 22 2004 Phil Knirsch <pknirsch@redhat.com> 20020927-14
- Fixed bug with wrong return code check of inet_pton() in traceroute6 (#100684)

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Oct 02 2003 Phil Knirsch <pknirsch@redhat.com> 20020927-12
- Fixed unaligned access problem on ia64 (#101417)

* Wed Sep 10 2003 Phil Knirsch <pknirsch@redhat.com> 20020927-11
- Don't use own headers, use glibc and kernheaders.

* Thu Sep 04 2003 Bill Nottingham <notting@redhat.com> 20020927-10
- fix build with new glibc-kernheaders

* Wed Sep 03 2003 Phil Knirsch <pknirsch@redhat.com> 20020927-9.1
- rebuilt

* Wed Sep 03 2003 Phil Knirsch <pknirsch@redhat.com> 20020927-9
- Start icmp_seq from 0 instead of 1 (Conform with debian and Solaris #100609).

* Thu Jul 31 2003 Phil Knirsch <pknirsch@redhat.com> 20020927-8
- One more update to ifenslave.c

* Mon Jun 16 2003 Phil Knirsch <pknirsch@redhat.com> 20020927-7
- Updated ifenslave.c and README.bonding to latest version.

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu May 15 2003 Phil Knirsch <pknirsch@redhat.com> 20020927-5
- Bumped release and rebuilt

* Thu May 15 2003 Phil Knirsch <pknirsch@redhat.com> 20020927-4
- Fixed DNS lookup problems (#68212).
- Added warning if binding problem failed on subinterface (#81640).

* Tue May 13 2003 Phil Knirsch <pknirsch@redhat.com> 20020927-3
- Removed bonding tarball and replaced it with ifenslave.c and README
- FHS compliance for all tools, now to be found in /bin with compat symlinks to
  old places.

* Wed Jan 22 2003 Tim Powers <timp@redhat.com> 20020927-2
- rebuilt

* Fri Nov 29 2002 Phil Knirsch <pknirsch@redhat.com> 20020927-1
- Updated to latest upstream version.

* Fri Jun 21 2002 Tim Powers <timp@redhat.com> 20020124-8
- automated rebuild

* Tue Jun 18 2002 Phil Knirsch <pknirsch@redhat.com> 20020124-7
- Added new BuildPreReqs for docbook-utils and perl-SGMLSpm (#66661)
- Fixed ipv6 error printing problem (#66659).

* Sun May 26 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Tue May 21 2002 Phil Knirsch <pknirsch@redhat.com>
- Added a patch to activate the rdisc server (#64270).
- Display the countermeasures warning only in verbose (#55236)

* Thu Apr 18 2002 Bill Nottingham <notting@redhat.com>
- quit trying to build HTML versions of the man pages

* Thu Mar 14 2002 Phil Knirsch <pknirsch@redhat.com>
- Added fix by Tom "spot" Callaway to fix buffer overflow problems in stats.

* Wed Feb 27 2002 Phil Knirsch <pknirsch@redhat.com>
- Update to iputils-ss020124.

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Mon Aug 27 2001 Philipp Knirsch <pknirsch@redhat.de> 20001110-6
- Fixed buffer overflow problem in traceroute6.c (#51135)

* Mon Jul 02 2001 Philipp Knirsch <pknirsch@redhat.de>
- Made ping6 and traceroute6 setuid (safe as they drop it VERY early) (#46769)

* Thu Jun 28 2001 Philipp Knirsch <pknirsch@redhat.de>
- Fixed ping statistics overflow bug (#43801)

* Tue Jun 26 2001 Philipp Knirsch <pknirsch@redhat.de>
- Fixed a bunch of compiler warnings (#37131)
- Fixed wrong exit code for no packets and deadline (#40323)
- Moved arping to /sbin from /usr/sbin due to ifup call (#45785). Symlink from
  /usr/sbin/ provided for backwards compatibility.

* Mon Apr 30 2001 Preston Brown <pbrown@redhat.com>
- install in.rdisc.8c as rdisc.8

* Tue Jan 16 2001 Jeff Johnson <jbj@redhat.com>
- update to ss001110
- doco fixes (#23844).

* Sun Oct  8 2000 Jeff Johnson <jbj@redhat.com>
- update to ss001007.

* Tue Aug  8 2000 Tim Waugh <twaugh@redhat.com>
- fix spelling mistake (#15714).

* Tue Aug  8 2000 Tim Waugh <twaugh@redhat.com>
- turn on -U on machines without TSC (#15223).

* Tue Aug  1 2000 Jeff Johnson <jbj@redhat.com>
- better doco patch (#15050).

* Tue Jul 25 2000 Jakub Jelinek <jakub@redhat.com>
- fix include-glibc/ to work with new glibc 2.2 resolver headers

* Thu Jul 13 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Sun Jun 18 2000 Jeff Johnson <jbj@redhat.com>
- FHS packaging.
- update to ss000418.
- perform reverse DNS lookup only once for same input.

* Sun Mar  5 2000 Jeff Johnson <jbj@redhat.com>
- include README.ifenslave doco.
- "ping -i N" was broke for N >= 3 (#9929).
- update to ss000121:
-- clockdiff: preserve raw socket errno.
-- ping: change error exit code to 1 (used to be 92,93, ...)
-- ping,ping6: if -w specified, transmit until -c limit is reached.
-- ping,ping6: exit code non-zero if some packets not received within deadline.

* Tue Feb 22 2000 Jeff Johnson <jbj@redhat.com>
- man page corrections (#9690).

* Wed Feb  9 2000 Jeff Johnson <jbj@jbj.org>
- add ifenslave.

* Thu Feb  3 2000 Elliot Lee <sopwith@redhat.com>
- List /usr/sbin/rdisc in %%files list.

* Thu Jan 27 2000 Jeff Johnson <jbj@redhat.com>
- add remaining binaries.
- casts to remove compilation warnings.
- terminate if -w deadline is reached exactly (#8724).

* Fri Dec 24 1999 Jeff Johnson <jbj@redhat.com>
- create (only ping for now, traceroute et al soon).
