%global snap_release 20190603
Summary: Root crontab files used to schedule the execution of programs
Name: crontabs
Version: 1.11
Release: 23%{?dist}
License: Public Domain and GPLv2
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL: https://github.com/cronie-crond/crontabs
Source0: https://github.com/cronie-crond/crontabs/releases/download/crontabs-%{snap_release}/%{name}-%{version}-%{snap_release}git.tar.gz
BuildArch: noarch
Requires: sed
Recommends: cronie

%description
This package is used by Fedora mainly for executing files by cron.

The crontabs package contains root crontab files and directories.
You will need to install cron daemon to run the jobs from the crontabs.
The cron daemon such as cronie or fcron checks the crontab files to
see when particular commands are scheduled to be executed.  If commands
are scheduled, it executes them.

Crontabs handles a basic system function, so it should be installed on
your system.

%prep
%setup -q

%build
#empty

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/etc/cron.{hourly,daily,weekly,monthly}
mkdir -p $RPM_BUILD_ROOT/usr/bin
mkdir -p $RPM_BUILD_ROOT/%{_mandir}/man4/

install -m644 ./crontab $RPM_BUILD_ROOT/etc/crontab
install -m755 ./run-parts $RPM_BUILD_ROOT/usr/bin/run-parts
install -m644 ./{crontabs,run-parts}.4 $RPM_BUILD_ROOT/%{_mandir}/man4/

mkdir -p $RPM_BUILD_ROOT/etc/sysconfig/
touch $RPM_BUILD_ROOT/etc/sysconfig/run-parts

%files
%{!?_licensedir:%global license %%doc}
%license COPYING
%config(noreplace) /etc/crontab
%attr(0644,root,root) %config(noreplace) /etc/sysconfig/run-parts
%{_bindir}/run-parts
%dir /etc/cron.hourly
%dir /etc/cron.daily
%dir /etc/cron.weekly
%dir /etc/cron.monthly
%{_mandir}/man4/*

%changelog
* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.11-23
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.11-22.20190603git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.11-21.20190603git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Jun  3 2019 Tomáš Mráz <tmraz@redhat.com> - 1.11-20.20190603git
- fix regression from the previous release (#1716114)

* Thu May 30 2019 Tomáš Mráz <tmraz@redhat.com> - 1.11-19.20190530git
- fix race condition in run-parts causing it to hang occasionally
- fix upstream URLs

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.11-18.20150630git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.11-17.20150630git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.11-16.20150630git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.11-15.20150630git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.11-14.20150630git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Nov 24 2016 Tomáš Mráz <tmraz@redhat.com> - 1.11-13.20150630git
- use Recommends to pull in cronie (#1269172)

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.11-12.20150630git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Aug 12 2015 Tomáš Mráz <tmraz@redhat.com> - 1.11-11.20150630git
- fix logging of PID in the finished line (#1236841)

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.11-10.20130830git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jul 11 2014 Tom Callaway <spot@fedoraproject.org> - 1.11-9.20130830git
- fix license handling

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.11-8.20130830git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Aug 30 2013 Marcela Mašláňová <mmaslano@redhat.com> 1.11-7.20121102git
- fix man page link 971583

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.11-6.20121102git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.11-5.20121102git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Nov  1 2012 Marcela Mašláňová <mmaslano@redhat.com> 1.11-5.20121102git
- update to the latest git snapshot with copying file and fixed man pages

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.11-4.20101115git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.11-3.20101115git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.11-2.20101115git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Nov 15 2010 Marcela Mašláňová <mmaslano@redhat.com> 1.11-1
- run-parts attempted to execute jobs that are not executable.

* Thu Nov 11 2010 Marcela Mašláňová <mmaslano@redhat.com> 1.11-1
- 652268 fix missing /

* Tue Nov  9 2010 Marcela Mašláňová <mmaslano@redhat.com> 1.11-1
- new git snapshot with --test and --list options

* Fri Oct 22 2010 Marcela Mašláňová <mmaslano@redhat.com> 1.11-1
- use sources from source fedorahosted

* Mon Oct 18 2010 Marcela Mašláňová <mmaslano@redhat.com> 1.10-34
- add --list option into run-parts

* Wed Mar 24 2010 Marcela Mašláňová <mmaslano@redhat.com> 1.10-33
- remove useless seting of home to "/"

* Mon Oct 12 2009 Marcela Mašláňová <mmaslano@redhat.com> 1.10-32
- rebuilt for review

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10-31
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jun 18 2009 Marcela Mašláňová <mmaslano@redhat.com> 1.10-30
- 491793 thanks Andrew Hecox for patch which allows set allow/deny jobs
- comment change "empty crontab"

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10-29
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Jan 27 2009 Marcela Mašláňová <mmaslano@redhat.com> 1.10-28
- 474219 requires on /etc/cron.d

* Mon Jan 26 2009 Marcela Mašláňová <mmaslano@redhat.com> 1.10-27
- Change requires back to cronie.

* Mon Jan 26 2009 Marcela Mašláňová <mmaslano@redhat.com> 1.10-26
- change /etc/crontab. All anacron jobs in cron.daily,weekly,...
 are check by anacron every hour. Anacron run them if they didn't
 run today. 

* Mon Dec  1 2008 Jan ONDREJ (SAL) <ondrejj(at)salstar.sk> 1.10-25
- Added /etc/cron.{hourly,daily,weekly,monthly} dirs again. bz#473353

* Mon Jun  9 2008 Marcela Maslanova <mmaslano@redhat.com> 1.10-23
- 450084 LANG=C is set up for running scripts

* Wed May 28 2008 Marcela Maslanova <mmaslano@redhat.com> 1.10-22
- remove scripts for delay, anacron now own most of the scripts. 
Crontabs owns only run-parts, /etc/crontab and crontabs sysconfig.

* Mon May 5 2008 Marcela Maslanova <mmaslano@redhat.com> 1.10-21
- 445079 delay script failed in case DELAY is zero

* Fri Apr 4 2008 Marcela Maslanova <mmaslano@redhat.com> 1.10-20
- 440410 log pid of process instead of logger's pid

* Mon Oct 22 2007 Marcela Maslanova <mmaslano@redhat.com> 1.10-19
- run-parts log also end of each job (patch from J. Kamens)
- Resolves: rhbz#303081

* Tue Sep 25 2007 Marcela Maslanova <mmaslano@redhat.com> 1.10-18
- cron.{hourly, daily,...} run ok
- rhbz#296741

* Thu Aug 30 2007 Marcela Maslanova <mmaslano@redhat.com> 1.10-17
- better solution of configuration script

* Mon Aug 27 2007 Marcela Maslanova <mmaslano@redhat.com> 1.10-16
- 254220 typo in script run-parts

* Tue Aug 21 2007 Marcela Maslanova <mmaslano@redhat.com> 1.10-15
- corrected license tag in spec
- add config file to crontab - delay of cron.{daily,...} could be
    switch off
- Resolves: rhbz#253536

* Tue Feb 27 2007 Marcela Maslanova <mmaslano@redhat.com> 1.10-14
- review again

* Thu Feb  8 2007 Marcela Maslanova <mmaslano@redhat.com> 1.10-13
- rhbz#225662 review

* Mon Jan 29 2007 Marcela Maslanova <mmaslano@redhat.com> 1.10-12
- link daily,weekly,monthly
- rhbz#224687

* Wed Jan 24 2007 Marcela Maslanova <mmaslano@redhat.com> 1.10-11
- crontabs should ignore Cfengine files, rebuilt
- Resolves: rhbz#223472

* Wed Oct 11 2006 Marcela Maslanova <mmaslano@redhat.com> 1.10-9
- patch (#110894) for delaying more emails in the moment

* Fri Jul 14 2006 Jesse Keating <jkeating@redhat.com> 0 1.10-8
- rebuilt

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Mon Sep 20 2004 Jason Vas Dias <jvdias@redhat.com>
- rebuilt under new CVS for dist-fc3

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb  7 2003 Bill Nottingham <notting@redhat.com>
- not-as-automated rebuild

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu Jul 19 2001 Preston Brown <pbrown@redhat.com>
- don't require tmpwatch

* Tue Feb 27 2001 Preston Brown <pbrown@redhat.com>
- noreplace crontab file; use tmppath

* Wed Jan 31 2001 Bill Nottingham <notting@redhat.com>
- don't process ,v files (#15968)

* Mon Aug  7 2000 Bill Nottingham <notting@redhat.com>
- put name of script in output of stuff run by run-parts (#12411)

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Tue Jun  6 2000 Bill Nottingham <notting@redhat.com>
- rebuild

* Fri Aug 27 1999 Jeff Johnson <jbj@redhat.com>
- don't run *~ or *, files (#4740).

* Thu Apr 15 1999 Bill Nottingham <notting@redhat.com>
- don't run .rpm{save,new,orig} files (bug #2190)

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 5)

* Mon Nov 30 1998 Bill Nottingham <notting@redhat.com>
- crontab: set HOME=/

* Sat Jun 27 1998 Jeff Johnson <jbj@redhat.com>
- run-parts: skip sub-directories (e.g. CVS) found instead of complaining

* Fri Apr 24 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Tue Apr 07 1998 Erik Troan <ewt@redhat.com>
- moved crontab jobs up a bit to make sure they aren't confused by
  switching to and fro daylight savings time
  
* Fri Oct 24 1997 Erik Troan <ewt@redhat.com>
- removed tmpwatch and at entries

* Thu Jul 31 1997 Erik Troan <ewt@redhat.com>
- made a noarch package
