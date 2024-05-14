# Our /usr/bin/last is in the SysVInit package
%define with_last     0

Summary: Utilities for monitoring process activities
Name: psacct
Version: 6.6.4
Release: 8%{?dist}
License: GPLv3+
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL: https://www.gnu.org/software/acct/

Source: ftp://ftp.gnu.org/pub/gnu/acct/acct-%{version}.tar.gz
Source1: psacct.service
Source2: psacct-logrotate.in
Source3: accton-create

Patch1: psacct-6.6.2-unnumberedsubsubsec.patch
Patch2: psacct-6.6.1-SEGV-when-record-incomplete.patch
Patch3: psacct-6.6.4-lastcomm-manpage-pid-twice.patch

Conflicts: filesystem < 3
Requires: coreutils
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

BuildRequires: autoconf
BuildRequires: systemd
BuildRequires: gcc


%description
The psacct package contains several utilities for monitoring process
activities, including ac, lastcomm, accton and sa. The ac command
displays statistics about how long users have been logged on. The
lastcomm command displays information about previous executed
commands. The accton command turns process accounting on or off. The
sa command summarizes information about previously executed
commands.


%prep
%setup -q -n acct-%{version}

%patch 1 -p1 -b .subsubsec
%patch 2 -p1
%patch 3 -p1

# fixing 'gets' undeclared
sed -i 's|.*(gets,.*||g' lib/stdio.in.h

# workaround for broken autotools stuff
sed -i 's|@ACCT_FILE_LOC@|/var/account/pacct|g'      files.h.in
sed -i 's|@SAVACCT_FILE_LOC@|/var/account/savacct|g' files.h.in
sed -i 's|@USRACCT_FILE_LOC@|/var/account/usracct|g' files.h.in


%build
%configure --enable-linux-multiformat

make


%install
mkdir -p %{buildroot}{/sbin,%{_bindir},%{_mandir},%{_sbindir}}
make install prefix=%{buildroot}%{_prefix} \
        bindir=%{buildroot}%{_bindir} sbindir=%{buildroot}%{_sbindir} \
        infodir=%{buildroot}%{_datadir}/info mandir=%{buildroot}%{_mandir}
cp dump-acct.8 %{buildroot}%{_mandir}/man8/

# remove unwanted file
rm -f %{buildroot}%{_infodir}/dir

mkdir -p %{buildroot}/var/account
touch %{buildroot}/var/account/pacct && chmod 0600 %{buildroot}/var/account/pacct

# create logrotate config file
mkdir -p %{buildroot}/etc/logrotate.d
sed -e 's|%%{_bindir}|%{_bindir}|g' -e 's|%%{_sbindir}|%{_sbindir}|g' %{SOURCE2} > %{buildroot}/etc/logrotate.d/psacct

# install systemd unit file
mkdir -p %{buildroot}%{_unitdir}
install -m 644 %{SOURCE1} %{buildroot}%{_unitdir}

# install accton-create script
install -d -m 0755 %{buildroot}%{_libexecdir}/psacct
install -m 755 %{SOURCE3} %{buildroot}%{_libexecdir}/psacct/

%if ! %{with_last}
rm -f %{buildroot}%{_bindir}/last %{buildroot}%{_mandir}/man1/last.1*
%endif


%post
%systemd_post psacct.service
touch /var/account/pacct && chmod 0600 /var/account/pacct


%preun
%systemd_preun psacct.service

%postun
%systemd_postun_with_restart psacct.service


%files
%license COPYING
%doc README
%dir /var/account
%{_unitdir}/psacct.service
%attr(0600,root,root)   %ghost %config /var/account/pacct
%attr(0644,root,root)   %config(noreplace) /etc/logrotate.d/*
%{_sbindir}/accton
%{_sbindir}/sa
%{_sbindir}/dump-utmp
%{_sbindir}/dump-acct
%{_libexecdir}/psacct/accton-create
%{_bindir}/ac
%if %{with_last}
%{_bindir}/last
%endif
%{_bindir}/lastcomm
%{_mandir}/man1/ac.1*
%if %{with_last}
%{_mandir}/man1/last.1*
%endif
%{_mandir}/man1/lastcomm.1*
%{_mandir}/man8/sa.8*
%{_mandir}/man8/accton.8*
%{_mandir}/man8/dump-acct.8*
%{_mandir}/man8/dump-utmp.8*
%{_infodir}/accounting.info.*


%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 6.6.4-8
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 6.6.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 6.6.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Apr 24 2019 Björn Esser <besser82@fedoraproject.org> - 6.6.4-5
- Remove hardcoded gzip suffix from GNU info pages

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 6.6.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Oct 17 2018 Peter Robinson <pbrobinson@fedoraproject.org> 6.6.4-3
- Use %%license, drop legacy sys-v bits

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 6.6.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Jan Rybar <jrybar@redhat.com> - 6.6.4-1
- Rebase to acct-6.6.4
- lastcomm: Fixed "--pid" twice in manpage

* Fri Mar 02 2018 Jan Rybar <jrybar@redhat.com> - 6.6.3-4
- SPEC - changes in Requires and BuildRequires - systemd and gcc

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 6.6.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Dec 11 2017 Jan Rybar <jrybar@redhat.com> - 6.6.3-2
- lastcomm: added new --pid option to show process PID and PPID
- changelog update: 6.6.3-1 author change
- spec file update: added correct access mode to created /var/account/pacct

* Mon Dec 11 2017 Jan Rybar <jrybar@redhat.com> - 6.6.3-1
- New upstream release 6.6.3

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 6.6.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 6.6.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 6.6.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 6.6.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.6.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 6.6.2-2
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Fri Nov 28 2014 Jaromir Capik <jcapik@redhat.com> - 6.6.2-1
- Updating to 6.6.2

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.6.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.6.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Oct 10 2013 Jaromir Capik <jcapik@redhat.com> - 6.6.1-7
- Preventing SEGVs when an incomplete record appears (#1017715)

* Wed Aug 21 2013 Jaromir Capik <jcapik@redhat.com> - 6.6.1-6
- Unifying the default file paths (#985150)

* Wed Jul 31 2013 Jaromir Capik <jcapik@redhat.com> - 6.6.1-5
- Dropping psacct-6.3.2-man-pages.patch
- (Re)introducing modified dump-acct man page

* Wed Jul 31 2013 Jaromir Capik <jcapik@redhat.com> - 6.6.1-4
- RH man page scan (#948523)

* Mon Jun 17 2013 Jaromir Capik <jcapik@redhat.com> - 6.6.1-3
- Service fails to start if accounting file already exists (#974716)

* Thu Apr 11 2013 Jaromir Capik <jcapik@redhat.com> - 6.6.1-2
- Logfile creation in the systemd unit file (#918132)

* Tue Apr 09 2013 Jaromir Capik <jcapik@redhat.com> - 6.6.1-1
- Update to 6.6.1
- Fixing bogus dates in the changelog

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.5.5-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jan 16 2013 Jaromir Capik <jcapik@redhat.com> - 6.5.5-8
- #759321 - psacct logrotate script references init.d service
- #735300 - Enabling psacct causes daily cron spam

* Tue Aug 28 2012 Jaromir Capik <jcapik@redhat.com> - 6.5.5-7
- Migration to new systemd scriptlet macros
- Fixing the build (new glibc) - 'gets' undeclared

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.5.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jan 25 2012 Harald Hoyer <harald@redhat.com> 6.5.5-5
- install everything in /usr
  https://fedoraproject.org/wiki/Features/UsrMove

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.5.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jun 29 2011 Jaromir Capik <jcapik@redhat.com> - 6.5.5-3
- Migration to systemd unit file

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.5.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Nov 09 2010 Jan Görig <jgorig@redhat.com> - 6.5.5-1
- upgrade to new upstream release
- remove obsolete patches
- remove FHS_compliant condition
- remove obsolete conflicts with initscripts
- info installation fix
- modified man-pages patch
- spec fixes

* Mon Aug 16 2010 Ivana Hutarova Varekova <varekova@redhat.com> - 6.5.4-6
- fix two man-pages links

* Mon Jun 28 2010 Ivana Hutarova Varekova <varekova@redhat.com> - 6.5.4-5
- remove obsolete patches

* Fri Jun 18 2010 Ivana Hutarova Varekova <varekova@redhat.com> - 6.5.4-4
- Resolves: #575975
  Build psacct with --enable-linux-multiformat
- remove obsolete change
- fix sa problem with hzval variable

* Mon Apr 19 2010 Ivana Hutarova Varekova <varekova@redhat.com> - 6.5.4-3
- add force-reload action to init script

* Fri Mar  5 2010 Ivana Hutarova Varekova <varekova@redhat.com> - 6.5.4-2
- add the documentation
  fix init script

* Fri Feb 12 2010 Ivana Hutarova Varekova <varekova@redhat.com> - 6.5.4-1
- update to 6.5.4
- remove obsolete patches
- fix license tag

* Thu Jan 28 2010 Ivana Hutarova Varekova <varekova@redhat.com> - 6.5.1-5
- Fix the logrotate script and split its template to a separate file.
  (Michal Schmidt patch, thanks)

* Thu Jan 28 2010 Ivana Hutarova Varekova <varekova@redhat.com> - 6.5.1-4
- fix the logrotate change

* Wed Jan 27 2010 Ivana Hutarova Varekova <varekova@redhat.com> - 6.5.1-3
- Resolves: #523774
  process accounting enabled unconditionally from daily cron job

* Mon Jan  4 2010 Ivana Hutarova Varekova <varekova@redhat.com> - 6.5.1-2
- fix initscript (accton parameters changed)
- fix lastcomm setings (#550229 - confusion about accounting file
  location)

* Fri Dec 18 2009 Ivana Hutarova Varekova <varekova@redhat.com> - 6.5.1-1
- update to 6.5.1
  remove unnecessary patches, spec file changes

* Wed Dec  9 2009 Ivana Hutarova Varekova <varekova@redhat.com> - 6.2.3-57
- fix the initscript (service restart does not work)

* Wed Dec  2 2009 Ivana Hutarova Varekova <varekova@redhat.com> - 6.2.3-56
- add dump-utmp.8 and dump-acct.8 man-pages

* Wed Sep 16 2009 Ivana Varekova <varekova@redhat.com> - 6.2.3-55
- fix init script (#521195)

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.3.2-54
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.3.2-53
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Nov 13 2008 Ivana Varekova <varekova@redhat.com> - 6.3.2-52
- remove link to nonexisting page from sa man-page

* Tue Jun  3 2008 Ivana Varekova <varekova@redhat.com> - 6.3.2-51
- remove unwanted file

* Wed Feb 20 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 6.3.2-50
- Autorebuild for GCC 4.3

* Fri Jan 18 2008 Ivana Varekova <varekova@redhat.com> - 6.3.2-49
- rebuilt

* Tue Aug 28 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> - 6.3.2-48
- Rebuild for selinux ppc32 issue.

* Wed Jul 25 2007 Ivana Varekova <varekova@redhat.com> - 6.3.2-47
- fix status service

* Wed Jul 25 2007 Ivana Varekova <varekova@redhat.com> - 6.3.2-46
- Resolves: #247034
  fix init script

* Mon May 28 2007 Ivana Varekova <varekova@redhat.com> - 6.3.2-45
- fix the return value of "service psacct status" command

* Thu Apr  5 2007 Ivana Varekova <varekova@redhat.com> - 6.3.2-44
- small spec changes
- change buildroot
- remove makeinstall macro

* Tue Jan 23 2007 Ivana Varekova <varekova@redhat.com> - 6.3.2-43
- Resolves: 223728
  psacct logrotate file looks for non existant directory

* Tue Jan  2 2007 Ivana Varekova <varekova@redhat.com> - 6.3.2-42
- Resolves: 221069
  (fix lastcomm man page)
- spec file cleanup

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 6.3.2-41.1
- rebuild

* Mon Feb 27 2006 Peter Jones <pjones@redhat.com> - 6.3.2-41
- add touch to prereq

* Mon Feb 27 2006 Ivana Varekova <varekova@redhat.com> - 6.3.2-40
- add chkconfig to prereq - bug 182848

* Mon Feb 20 2006 Ivana Varekova <varekova@redhat.com> - 6.3.2-39
- add Large File Support

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 6.3.2-38.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 6.3.2-38.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Tue Jan  3 2006 Ivana Varekova <varekova@redhat.com> 6.3.2-38
- fix typo bug 176811

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Fri Mar  4 2005 Ivana Varekova <varekova@redhat.com> 6.3.2-37
- rebuilt

* Tue Feb 15 2005 Ivana Varekova <varekova@redhat.com> 6.3.2-36
- fix sa manpage - necessary becouse of bug #43294 and previous patch

* Tue Feb 15 2005 Ivana Varekova <varekova@redhat.com> 6.3.2-35
- fix #147782 logrotate script error

* Thu Feb  3 2005 Charles Bennett <ccb@redhat.com> 6.3.2-33.fc4
- rhbz 133077: logrotate fixed to continue accounting during rotate
- rhbz 141802: lastcomm was not handling all forms of --strict-match
- rhbz 141971: rpm -e no longer leaves /var/lock/subsys/psacct
- rhbz 43294: sa will never report any io because the kernel doesn't
   provide it.  Tweaked to ignore ac_io in acct.h
- integrate lastcomm hz patch from RH support

* Wed Sep  1 2004 root <ccb@redhat.com> - 6.3.2-31
- integrate JFenlason's hz patch, improve pts device reporting

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Thu Dec 26 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- make /etc/info-dir an optional file

* Wed Nov 13 2002 Mike A. Harris <mharris@redhat.com> 6.3.2-25
- Added with_last conditional to disable /usr/bin/last because ours is in
  the SysVInit package.  This fixes unpackaged files terminate build prob.

* Thu Aug 22 2002 Mike A. Harris <mharris@redhat.com> 6.3.2-24
- Fixed initscript reload/restart by creating start/stop functions and
  making everything use them (#72261)

* Tue Aug  6 2002 Mike A. Harris <mharris@redhat.com> 6.3.2-23
- Fixed chkconfig issue in rpm scripts (#61191)
- Excludearch ia64, not taking the time to debug/troubleshoot random
  buildsystem failure due to higher priorities.

* Mon Jul 08 2002 Elliot Lee <sopwith@redhat.com>
- Take the time to make sure things get through on all archs, by simply
  running it through the build system.

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed Mar 27 2002 Mike A. Harris <mharris@redhat.com> 6.3.2-19
- Made initscript touch/chmod accounting file if it is not present during
  startup, to ensure accounting works properly when enabled.

* Tue Mar 26 2002 Mike A. Harris <mharris@redhat.com> 6.3.2-18
- Fixed duh in initscript pointing to wrong accounting file (#61939)

* Sun Mar 17 2002 Mike A. Harris <mharris@redhat.com> 6.3.2-17
- Removed the files usracct and savacct, which are not used by psacct
  utilities at all, but by the sa program.  Our sa uses files in a different
  location, and so these files are unused and unnecessary.

* Sat Mar 16 2002 Mike A. Harris <mharris@redhat.com> 6.3.2-16
- Added chkconfig to post and preun scripts for bug (#61191)

* Tue Mar 12 2002 Mike A. Harris <mharris@redhat.com> 6.3.2-15
- Added new feature - psacct initscript now controls process accounting so
  that it is not just forced on if installed as was the previous behaviour
- Modified the initscripts package to not force psacct on anymore and made
  the new psacct-6.3.2-15 conflict with previous initscripts packages.
- Fixed logrotate config to set perms/owner of new log files, and closed
  bug (#54165)

* Thu Mar  7 2002 Mike A. Harris <mharris@redhat.com> 6.3.2-14
- Fixed 64bit bug in calls to ctime() in lastcomm and dump-utmp (#60712)

* Wed Mar  6 2002 Mike A. Harris <mharris@redhat.com> 6.3.2-13
- Removed Build_7x flag, added FHS_compliant flag, reworked specfile to use new
  flag, and fixed bug (#60716)

* Thu Feb 28 2002 Bill Nottingham <notting@redhat.com> 6.3.2-12
- rebuild in new environment for FHS correctness

* Thu Jan 31 2002 Mike A. Harris <mharris@redhat.com> 6.3.2-11
- Conditionalized acct-6.3.2-config.patch to only be applied for RHL 7.x
  builds, as it breaks FHS compliance by putting files in nonstandard
  locations.  Also fixed up other places in specfile for FHS 2.2.
- Added acct-6.3.2-I-HATE-GNU-AUTOCONK.patch because I hate GNU autoconk
  really really badly.

- Bumped to -11 to avoid buildsystem stupidness

* Thu Sep 06 2001 Mike A. Harris <mharris@redhat.com> 6.3.2-9
- Fixed bug (#53307) psacct is enabled by default, and the log files
  are huge, and will fill the disk up very quickly.  logrotate will
  now compress them daily.

* Sat Sep 01 2001 Florian La Roche <Florian.LaRoche@redhat.de> 6.3.2-8
- do not fail for ENOSYS to silently support kernels without
  process accounting

* Sun Aug 26 2001 Mike A. Harris <mharris@redhat.com> 6.3.2-7
- Change spec tag Copyright -> License
- change logrotate to rotate daily, and keep 1 month (31 days) of data

* Sun Jun 24 2001 Elliot Lee <sopwith@redhat.com>
- Bump release + rebuild.

* Fri Feb 02 2001 Helge Deller <hdeller@redhat.de>
- added logrotate file for /var/log/pacct (#24900)

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Mon Jun  5 2000 Nalin Dahyabhai <nalin@redhat.com>
- FHS fixes

* Sat May  6 2000 Bill Nottingham <notting@redhat.com>
- fix for new patch

* Thu Feb 03 2000 Nalin Dahyabhai <nalin@redhat.com>
- update to 6.3.2

* Mon Apr 05 1999 Preston Brown <pbrown@redhat.com>
- wrap post script with reference count.

* Tue Mar 23 1999 Preston Brown <pbrown@redhat.com>
- install-info sucks.  Still.

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com>
- auto rebuild in the new build environment (release 8)

* Thu Mar 18 1999 Bill Nottingham <notting@redhat.com>
- #define HAVE_LINUX_ACCT_H too, so it works. :)

* Sun Aug 16 1998 Jeff Johnson <jbj@redhat.com>
- accton needs to be accessible to /etc/rc.d/init.d/halt

* Fri May 08 1998 Erik Troan <ewt@redhat.com>
- install-info sucks

* Mon Apr 27 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Thu Oct 23 1997 Donnie Barnes <djb@redhat.com>
- updated from 6.2 to 6.3

* Mon Jul 21 1997 Erik Troan <ewt@redhat.com>
- built against glibc
