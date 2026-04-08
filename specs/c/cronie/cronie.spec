## START: Set by rpmautospec
## (rpmautospec version 0.8.4)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 13;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%bcond selinux 1
%bcond pam 1
%bcond audit 1
%bcond inotify 1

Summary:   Cron daemon for executing programs at set times
Name:      cronie
Version:   1.7.2
Release:   %autorelease
License:   GPL-2.0-or-later AND BSD-3-Clause AND BSD-2-Clause AND ISC AND LGPL-2.1-or-later
URL:       https://github.com/cronie-crond/cronie
Source0:   https://github.com/cronie-crond/cronie/releases/download/cronie-%{version}/cronie-%{version}.tar.gz

Patch:     0001-do-no-leak-file-descriptors.patch
# https://github.com/cronie-crond/cronie/issues/193
Patch:     make_error_func_prototype_complete.patch
# https://github.com/cronie-crond/cronie/pull/200
Patch:     fix_range_parsing.patch
# https://github.com/cronie-crond/cronie/pull/201
Patch:     move_parsing_code.patch
# https://github.com/cronie-crond/cronie/pull/206
Patch:     crontab-fix-backup-failure.patch

Requires:  dailyjobs

%if %{with selinux}
Requires:      libselinux >= 2.0.64
Buildrequires: libselinux-devel >= 2.0.64
%endif
%if %{with pam}
Requires:      pam >= 1.0.1
Buildrequires: pam-devel >= 1.0.1
%endif
%if %{with audit}
Buildrequires: audit-libs-devel >= 1.4.1
%endif

BuildRequires:    gcc
BuildRequires:    systemd
BuildRequires:    make
Obsoletes:        %{name}-sysvinit

Requires(post):   coreutils sed

%if 0%{?fedora} && 0%{?fedora} < 28 || 0%{?rhel} && 0%{?rhel} < 8
%{?systemd_requires}
%else
%{?systemd_ordering} # does not exist on Fedora27/RHEL7
%endif


%description
Cronie contains the standard UNIX daemon crond that runs specified programs at
scheduled times and related tools. It is a fork of the original vixie-cron and
has security and configuration enhancements like the ability to use pam and
SELinux.

%package anacron
Summary:   Utility for running regular jobs
Requires:  crontabs
Provides:  dailyjobs
Provides:  anacron = 2.4
Obsoletes: anacron <= 2.3
Requires(post): coreutils
Requires:  %{name} = %{version}-%{release}

%description anacron
Anacron is part of cronie that is used for running jobs with regular
periodicity which do not have exact time of day of execution.

The default settings of anacron execute the daily, weekly, and monthly
jobs, but anacron allows setting arbitrary periodicity of jobs.

Using anacron allows running the periodic jobs even if the system is often
powered off and it also allows randomizing the time of the job execution
for better utilization of resources shared among multiple systems.

%package noanacron
Summary:   Utility for running simple regular jobs in old cron style
Provides:  dailyjobs
Requires:  crontabs
Requires:  %{name} = %{version}-%{release}

%description noanacron
Old style of running {hourly,daily,weekly,monthly}.jobs without anacron. No
extra features.

%prep
%autosetup -p1

%build
%configure \
    %{?with_pam:--with-pam} \
    %{?with_selinux:--with-selinux} \
    %{?with_audit:--with-audit} \
    %{?with_inotify:--with-inotify} \
    --enable-anacron \
    --enable-pie \
    --enable-relro

%make_build V=2

%install
%make_install DESTMAN=$RPM_BUILD_ROOT%{_mandir}
mkdir -pm700 $RPM_BUILD_ROOT%{_localstatedir}/spool/cron
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/
mkdir -pm755 $RPM_BUILD_ROOT%{_sysconfdir}/cron.d/
%if ! %{with pam}
    rm -f $RPM_BUILD_ROOT%{_sysconfdir}/pam.d/crond
%endif
install -m 644 crond.sysconfig $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/crond
touch $RPM_BUILD_ROOT%{_sysconfdir}/cron.deny
install -m 644 contrib/anacrontab $RPM_BUILD_ROOT%{_sysconfdir}/anacrontab
install -c -m755 contrib/0hourly $RPM_BUILD_ROOT%{_sysconfdir}/cron.d/0hourly
mkdir -pm 755 $RPM_BUILD_ROOT%{_sysconfdir}/cron.hourly
install -c -m755 contrib/0anacron $RPM_BUILD_ROOT%{_sysconfdir}/cron.hourly/0anacron
mkdir -p $RPM_BUILD_ROOT/var/spool/anacron
touch $RPM_BUILD_ROOT/var/spool/anacron/cron.daily
touch $RPM_BUILD_ROOT/var/spool/anacron/cron.weekly
touch $RPM_BUILD_ROOT/var/spool/anacron/cron.monthly

# noanacron package
install -m 644 contrib/dailyjobs $RPM_BUILD_ROOT/%{_sysconfdir}/cron.d/dailyjobs

# install systemd initscript
install -m 644 -D contrib/cronie.systemd $RPM_BUILD_ROOT/usr/lib/systemd/system/crond.service

%post
# run after an installation
%systemd_post crond.service

%post anacron
[ -e /var/spool/anacron/cron.daily ] || install -m 0600 -D /dev/null /var/spool/anacron/cron.daily 2>/dev/null || :
[ -e /var/spool/anacron/cron.weekly ] || install -m 0600 -D /dev/null /var/spool/anacron/cron.weekly 2>/dev/null || :
[ -e /var/spool/anacron/cron.monthly ] || install -m 0600 -D /dev/null /var/spool/anacron/cron.monthly 2>/dev/null || :

%preun
# run before a package is removed
%systemd_preun crond.service

%postun
# run after a package is removed
%systemd_postun_with_restart crond.service

%triggerun -- cronie-anacron < 1.4.1
# empty /etc/crontab in case there are only old regular jobs
cp -a /etc/crontab /etc/crontab.rpmsave
sed -e '/^01 \* \* \* \* root run-parts \/etc\/cron\.hourly/d'\
  -e '/^02 4 \* \* \* root run-parts \/etc\/cron\.daily/d'\
  -e '/^22 4 \* \* 0 root run-parts \/etc\/cron\.weekly/d'\
  -e '/^42 4 1 \* \* root run-parts \/etc\/cron\.monthly/d' /etc/crontab.rpmsave > /etc/crontab
exit 0

%triggerun -- cronie < 1.4.7-2
# Save the current service runlevel info
# User must manually run systemd-sysv-convert --apply crond
# to migrate them to systemd targets
/usr/bin/systemd-sysv-convert --save crond

# The package is allowed to autostart:
/bin/systemctl enable crond.service >/dev/null 2>&1

/bin/chkconfig --del crond >/dev/null 2>&1 || :
/bin/systemctl try-restart crond.service >/dev/null 2>&1 || :
/bin/systemctl daemon-reload >/dev/null 2>&1 || :

%triggerin -- pam, glibc, libselinux
# changes in pam, glibc or libselinux can make crond crash
# when it calls pam
/bin/systemctl try-restart crond.service >/dev/null 2>&1 || :

%files
%doc AUTHORS README ChangeLog
%{!?_licensedir:%global license %%doc}
%license COPYING
%attr(755,root,root) %{_bindir}/crond
%attr(4755,root,root) %{_bindir}/crontab
%attr(755,root,root) %{_bindir}/cronnext
%{_mandir}/man8/crond.*
%{_mandir}/man8/cron.*
%{_mandir}/man5/crontab.*
%{_mandir}/man1/crontab.*
%{_mandir}/man1/cronnext.*
%dir %{_localstatedir}/spool/cron
%dir %{_sysconfdir}/cron.d
%if %{with pam}
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/pam.d/crond
%endif
%config(noreplace) %{_sysconfdir}/sysconfig/crond
%config(noreplace,missingok) %{_sysconfdir}/cron.deny
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/cron.d/0hourly
%attr(0644,root,root) /usr/lib/systemd/system/crond.service

%files anacron
%{_bindir}/anacron
%attr(0755,root,root) %{_sysconfdir}/cron.hourly/0anacron
%config(noreplace) %{_sysconfdir}/anacrontab
%dir /var/spool/anacron
%ghost %attr(0600,root,root) %verify(not md5 size mtime) /var/spool/anacron/cron.daily
%ghost %attr(0600,root,root) %verify(not md5 size mtime) /var/spool/anacron/cron.weekly
%ghost %attr(0600,root,root) %verify(not md5 size mtime) /var/spool/anacron/cron.monthly
%{_mandir}/man5/anacrontab.*
%{_mandir}/man8/anacron.*

%files noanacron
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/cron.d/dailyjobs

%changelog
## START: Generated by rpmautospec
* Mon Apr 06 2026 azldev <> - 1.7.2-13
- Latest state for cronie

* Wed Aug 06 2025 Ondřej Pohořelský <opohorel@redhat.com> - 1.7.2-12
- Fix backup failure when ~/.cache directory is missing

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.2-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jul 07 2025 Ondřej Pohořelský <opohorel@redhat.com> - 1.7.2-10
- tests: migrate from STI to TMT

* Tue May 13 2025 Ondřej Pohořelský <opohorel@redhat.com> - 1.7.2-9
- Move parsing code before separator check

* Wed Apr 23 2025 Ondřej Pohořelský <opohorel@redhat.com> - 1.7.2-8
- Install crond.service into /usr/lib

* Mon Apr 07 2025 Ondřej Pohořelský <opohorel@redhat.com> - 1.7.2-7
- Fix range parsing

* Mon Jan 27 2025 Ondřej Pohořelský <opohorel@redhat.com> - 1.7.2-6
- Remove sbin mentions from spec file

* Mon Jan 27 2025 Ondřej Pohořelský <opohorel@redhat.com> - 1.7.2-5
- Resolve build failure with GCC15

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Dec 09 2024 Ondřej Pohořelský <opohorel@redhat.com> - 1.7.2-3
- Create anacron timestamp files with correct permissions

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jul 01 2024 Jan Staněk <jstanek@redhat.com> - 1.7.2-1
- Update to version 1.7.2 (rhbz#2294896)
- Polish bconds to use newer macros
- Patch leaks found by SAST scan

* Mon Feb 26 2024 Ondřej Pohořelský <opohorel@redhat.com> - 1.7.1-1
- Update to 1.7.1

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Jan 02 2024 Ondřej Pohořelský <opohorel@redhat.com> - 1.7.0-2
- Adds -n option: wait on finnishing grandchild process

* Tue Oct 17 2023 Ondřej Pohořelský <opohorel@redhat.com> - 1.7.0-1
- update to 1.7.0

* Fri Oct 06 2023 Ondřej Pohořelský <opohorel@redhat.com> - 1.6.1-9
- Add -n option for crontab entries

* Fri Oct 06 2023 Ondřej Pohořelský <opohorel@redhat.com> - 1.6.1-8
- Fixes indentation for one BuildRequire

* Mon Sep 11 2023 Jan Staněk <jstanek@redhat.com> - 1.6.1-6
- Migrated to SPDX license

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue Jun 28 2022 Jan Staněk <jstanek@redhat.com> - 1.6.1-2
- Set 'missingok' for /etc/cron.deny to not recreate it on update

* Mon May 02 2022 Ondřej Pohořelský <opohorel@redhat.com> - 1.6.1-1
- New upstream release 1.6.1

* Tue Mar 22 2022 Ondřej Pohořelský <opohorel@redhat.com> - 1.6.0-1
- New upstream release 1.6.0

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Apr 30 2021 Jan Staněk <jstanek@redhat.com> - 1.5.7-2
- Address issues found by static scanners

* Mon Mar 29 2021 Tomáš Mráz <tmraz@fedoraproject.org> - 1.5.7-1
- new upstream release 1.5.7 with bug fixes and enhancements

* Wed Mar 17 2021 Tomáš Mráz <tmraz@fedoraproject.org> - 1.5.6-1
- new upstream release 1.5.6 with bug fixes and enhancements

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 13 2020 Tom Stellard <tstellar@redhat.com> - 1.5.5-3
- Use make macros
- https://fedoraproject.org/wiki/Changes/UseMakeBuildInstallMacro

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 31 2019 Tomáš Mráz <tmraz@redhat.com> - 1.5.5-1
- new upstream release 1.5.5 with multiple bug fixes and improvements

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Mar 18 2019 Tomáš Mráz <tmraz@redhat.com> - 1.5.4-1
- new upstream release 1.5.4 with regression fix

* Fri Mar 15 2019 Tomáš Mráz <tmraz@redhat.com> - 1.5.3-1
- new upstream release 1.5.3 fixing CVE-2019-9704 and CVE-2019-9705

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Nov 30 2018 Tomáš Mráz <tmraz@redhat.com> - 1.5.2-4
- Do not hard-require systemd as crond is used in containers without
  systemd (#1654659)

* Wed Oct 31 2018 Tomáš Mráz <tmraz@redhat.com> - 1.5.2-3
- use role from the current context for system crontabs (#1639381)

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu May  3 2018 Tomáš Mráz <tmraz@redhat.com> - 1.5.2-1
- new upstream release 1.5.2

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu May  4 2017 Tomáš Mráz <tmraz@redhat.com> - 1.5.1-6
- fix Y2038 problems in cron and anacron (#1445136)

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jan  3 2017 Tomáš Mráz <tmraz@redhat.com> - 1.5.1-4
- make failure of creation of the ghost files in /var non-fatal

* Mon Sep  5 2016 Tomáš Mráz <tmraz@redhat.com> - 1.5.1-3
- on some machines the power supply is named ADP0

* Tue Aug 23 2016 Tomáš Mráz <tmraz@redhat.com> - 1.5.1-2
- query power status directly from kernel

* Thu Jun 23 2016 Tomáš Mráz <tmraz@redhat.com> - 1.5.1-1
- new upstream release

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Jul 13 2015 Tomáš Mráz <tmraz@redhat.com> - 1.5.0-3
- the temp file name used by crontab needs to be ignored by crond

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu May 28 2015 Tomáš Mráz <tmraz@redhat.com> - 1.5.0-1
- new upstream release

* Tue Apr 21 2015 Tomáš Mráz <tmraz@redhat.com> - 1.4.12-6
- mark the 0hourly and dailyjobs crontabs as config
- do not add already existing orphan on reload

* Tue Feb  3 2015 Tomáš Mráz <tmraz@redhat.com> - 1.4.12-5
- correct the permissions of the anacron timestamp files

* Fri Jan  2 2015 Tomáš Mráz <tmraz@redhat.com> - 1.4.12-4
- check for NULL pamh on two more places (#1176215)

* Tue Dec  2 2014 Tomáš Mráz <tmraz@redhat.com> - 1.4.12-3
- call PAM only for non-root user or non-system crontabs (#956157)
- bypass the PAM check in crontab for root (#1169175)

* Tue Nov  4 2014 Tomáš Mráz <tmraz@redhat.com> - 1.4.12-2
- refresh user entries when jobs are run

* Wed Sep 17 2014 Marcela Mašláňová <mmaslano@redhat.com> - 1.4.12-1
- new release 1.4.12
- remove gpl2 license, because it's part of upstream COPYING now

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.11-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Jul 11 2014 Tom Callaway <spot@fedoraproject.org> - 1.4.11-8
- fix license handling

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.11-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Apr 30 2014 Marcela Mašláňová <mmaslano@redhat.com> - 1.4.11-6
- unwanted fd could make trouble to SElinux 1075106

* Thu Jan 16 2014 Ville Skyttä <ville.skytta@iki.fi> - 1.4.11-5
- Drop INSTALL from docs, fix rpmlint tabs vs spaces warning.

* Wed Sep 25 2013 Marcela Mašláňová <mmaslano@redhat.com> - 1.4.11-4
- some jobs are not executed because not all environment variables are set 995590
- cronie's systemd script use "KillMode=process" 919290

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul 22 2013 Marcela Mašláňová <mmaslano@redhat.com> - 1.4.11-2
- scriptlets are not created correctly if systemd is not in BR 986698
- remove sub-package sysvinit, which is not needed anymore
- update license, anacron is under GPLv2+

* Thu Jul 18 2013 Marcela Mašláňová <mmaslano@redhat.com> - 1.4.11-1
- new release 1.4.11 (contains previous bug fixes from 1.4.10-5)

* Tue Jun 11 2013 Tomáš Mráz <tmraz@redhat.com> - 1.4.10-5
- add support for RANDOM_DELAY - delaying job startups
- pass some environment variables to processes (LANG, etc.) (#969761)
- do not use putenv() with string literals (#971516)

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.10-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jan  2 2013 Marcela Mašláňová <mmaslano@redhat.com> - 1.4.10-3
- change configuration files to 644
- change 6755 to 4755 for crontab binary

* Tue Nov 27 2012 Marcela Mašláňová <mmaslano@redhat.com> - 1.4.10-1
- New release 1.4.10

* Thu Nov 22 2012 Marcela Mašláňová <mmaslano@redhat.com> - 1.4.9-1
- New release 1.4.9

* Wed Sep 05 2012 Václav Pavlín <vpavlin@redhat.com> - 1.4.8-13
- Scriptlets replaced with new systemd macros (#850070)

* Fri Jul 27 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.8-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.8-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Oct 26 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.8-10
- Rebuilt for glibc bug#747377

* Tue Oct 25 2011 Tomáš Mráz <tmraz@redhat.com> - 1.4.8-9
- make crond run a little bit later in the boot process (#747759)

* Mon Oct 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.4.8-8
- change triggerun to fix 735802 during upgrade

* Wed Jul 27 2011 Karsten Hopp <karsten@redhat.com> 1.4.8-7
- rebuild again, ppc still had the broken rpm in the buildroots

* Thu Jul 21 2011 Rex Dieter <rdieter@fedoraproject.org> 1.4.8-6
- rebuild (broken rpm in buildroot)

* Thu Jul 21 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.4.8-5
- fix permission of init.d/crond

* Thu Jun 30 2011 Tomáš Mráz <tmraz@redhat.com> - 1.4.8-4
- drop the without systemd build condition
- add the chkconfig readding trigger to the sysvinit subpackage

* Wed Jun 29 2011 Tomáš Mráz <tmraz@redhat.com> - 1.4.8-3
- start crond after auditd

* Wed Jun 29 2011 Tomáš Mráz <tmraz@redhat.com> - 1.4.8-2
- fix inotify support to not leak fds (#717505)

* Tue Jun 28 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.4.8-1
- update to 1.4.8
- create sub-package sysvinit for initscript

* Mon May  9 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.4.7-3
- missing requirement on systemd-sysv for scriptlets

* Thu May 05 2011 Tomáš Mráz <tmraz@redhat.com> - 1.4.7-2
- use only systemd units with systemd
- add trigger for restart on glibc, libselinux or pam upgrades (#699189)

* Tue Mar 15 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.4.7-1
- new release 1.4.7

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.6-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jan 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.4.6-8
- enable crond even with systemctl

* Thu Dec 16 2010 Marcela Mašláňová <mmaslano@redhat.com> - 1.4.6-7
- 663193 rewritten selinux support

* Wed Dec 15 2010 Marcela Mašláňová <mmaslano@redhat.com> - 1.4.6-6
- apply selinux patch from dwalsh

* Fri Dec 10 2010 Tomas Mraz <tmraz@redhat.com> - 1.4.6-5
- do not lock jobs that fall out of allowed range - 661966

* Thu Dec 02 2010 Marcela Mašláňová <mmaslano@redhat.com> - 1.4.6-4
- fix post (thanks plautrba for review)

* Tue Nov 30 2010 Marcela Mašláňová <mmaslano@redhat.com> - 1.4.6-3
- systemd init script 617320

* Tue Nov 30 2010 Marcela Mašláňová <mmaslano@redhat.com> - 1.4.6-2
- fix typos in man pages

* Fri Oct 22 2010 Marcela Mašláňová <mmaslano@redhat.com> - 1.4.6-1
- update to 1.4.6

* Fri Aug 13 2010 Marcela Mašláňová <mmaslano@redhat.com> - 1.4.5-4
- 623908 fix fd leak in anacron, which caused denail of prelink
  and others

* Mon Aug  9 2010 Marcela Mašláňová <mmaslano@redhat.com> - 1.4.5-2
- remove sendmail from requirements. If it's not installed, it will
 log into (r)syslog.

* Mon Aug  2 2010 Marcela Mašláňová <mmaslano@redhat.com> - 1.4.5-1
- update to new release

* Fri Feb 19 2010 Marcela Mašláňová <mmaslano@redhat.com> - 1.4.4-1
- update to new release

* Mon Feb 15 2010 Marcela Mašláňová <mmaslano@redhat.com> - 1.4.3-3
- 564894 FTBFS DSOLinking

* Thu Nov  5 2009 Marcela Mašláňová <mmaslano@redhat.com> - 1.4.3-2
- 533189 pam needs add a line and selinux needs defined one function

* Fri Oct 30 2009 Marcela Mašláňová <mmaslano@redhat.com> - 1.4.3-1
- 531963 and 532482 creating noanacron package

* Mon Oct 19 2009 Marcela Mašláňová <mmaslano@redhat.com> - 1.4.2-2
- 529632 service crond stop returns appropriate value

* Mon Oct 12 2009 Marcela Mašláňová <mmaslano@redhat.com> - 1.4.2-1
- new release

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 1.4.1-3
- rebuilt with new audit

* Fri Aug 14 2009 Tomas Mraz <tmraz@redhat.com> - 1.4.1-2
- create the anacron timestamps in correct post script

* Fri Aug 14 2009 Marcela Mašláňová <mmaslano@redhat.com> - 1.4.1-1
- update to 1.4.1
- create and own /var/spool/anacron/cron.{daily,weekly,monthly} to
 remove false warning about non existent files
- Resolves: 517398

* Wed Aug  5 2009 Tomas Mraz <tmraz@redhat.com> - 1.4-4
- 515762 move anacron provides and obsoletes to the anacron subpackage

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jul 20 2009 Marcela Mašláňová <mmaslano@redhat.com> - 1.4-2
- merge cronie and anacron in new release of cronie
- obsolete/provide anacron in spec

* Thu Jun 18 2009 Marcela Mašláňová <mmaslano@redhat.com> - 1.3-2
- 506560 check return value of access

* Mon Apr 27 2009 Marcela Mašláňová <mmaslano@redhat.com> - 1.3-1
- new release

* Fri Apr 24 2009 Marcela Mašláňová <mmaslano@redhat.com> - 1.2-8
- 496973 close file descriptors after exec

* Mon Mar  9 2009 Tomas Mraz <tmraz@redhat.com> - 1.2-7
- rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Dec 23 2008 Marcela Mašláňová <mmaslano@redhat.com> - 1.2-5
- 477100 NO_FOLLOW was removed, reload after change in symlinked
  crontab is needed, man updated.

* Fri Oct 24 2008 Marcela Mašláňová <mmaslano@redhat.com> - 1.2-4
- update init script

* Thu Sep 25 2008 Marcela Maslanova <mmaslano@redhat.com> - 1.2-3
- add sendmail file into requirement, cause it's needed some MTA

* Thu Sep 18 2008 Marcela Maslanova <mmaslano@redhat.com> - 1.2-2
- 462252  /etc/sysconfig/crond does not need to be executable

* Thu Jun 26 2008 Marcela Maslanova <mmaslano@redhat.com> - 1.2-1
- update to 1.2

* Tue Jun 17 2008 Tomas Mraz <tmraz@redhat.com> - 1.1-3
- fix setting keycreate context
- unify logging a bit
- cleanup some warnings and fix a typo in TZ code
- 450993 improve and fix inotify support

* Wed Jun  4 2008 Marcela Maslanova <mmaslano@redhat.com> - 1.1-2
- 49864 upgrade/update problem. Syntax error in spec.

* Wed May 28 2008 Marcela Maslanova <mmaslano@redhat.com> - 1.1-1
- release 1.1

* Tue May 20 2008 Marcela Maslanova <mmaslano@redhat.com> - 1.0-6
- 446360 check for lock didn't call chkconfig

* Tue Feb 12 2008 Marcela Maslanova <mmaslano@redhat.com> - 1.0-5
- upgrade from less than cronie-1.0-4 didn't add chkconfig

* Wed Feb  6 2008 Marcela Maslanova <mmaslano@redhat.com> - 1.0-4
- 431366 after reboot wasn't cron in chkconfig

* Tue Feb  5 2008 Marcela Maslanova <mmaslano@redhat.com> - 1.0-3
- 431366 trigger part => after update from vixie-cron on cronie will
  be daemon running.

* Wed Jan 30 2008 Marcela Maslanova <mmaslano@redhat.com> - 1.0-2
- change the provides on higher version than obsoletes

* Tue Jan  8 2008 Marcela Maslanova <mmaslano@redhat.com> - 1.0-1
- packaging cronie
- thank's for help with packaging to my reviewers

## END: Generated by rpmautospec
