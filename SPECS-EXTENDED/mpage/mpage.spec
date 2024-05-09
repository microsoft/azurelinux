Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Summary: A tool for printing multiple pages of text on each printed page
Name: mpage
Version: 2.5.7
Release: 10%{?dist}
License: GPLv2+
Url: https://www.mesa.nl/pub/mpage/
Source: ftp://ftp.mesa.nl/pub/mpage/mpage-%{version}.tgz
Patch0: mpage25-config.patch
BuildRequires: gcc

%description
The mpage utility takes plain text files or PostScript(TM) documents
as input, reduces the size of the text, and prints the files on a
PostScript printer with several pages on each sheet of paper. Mpage is
very useful for viewing large printouts without using up lots of
paper. Mpage supports many different layout options for the printed
pages.

%prep
%setup -q
%patch 0 -p1 -b .config

%build
make BINDIR=%{_bindir} LIBDIR=%{_datadir} MANDIR=%{_mandir}/man1

iconv -f iso-8859-2 -t utf-8 CHANGES > CHANGES.tmp && \
touch -r CHANGES CHANGES.tmp && mv CHANGES.tmp CHANGES

%install
mkdir -p $RPM_BUILD_ROOT{%{_bindir},%{_datadir}/mpage,%{_mandir}/man1}

make PREFIX=$RPM_BUILD_ROOT/%{_prefix} BINDIR=$RPM_BUILD_ROOT/%{_bindir} \
	LIBDIR=$RPM_BUILD_ROOT/%{_datadir} \
	MANDIR=$RPM_BUILD_ROOT/%{_mandir}/man1 \
	install

%files
%license COPYING
%doc CHANGES Copyright README NEWS TODO FAQ
%{_bindir}/mpage
%{_mandir}/man1/mpage.*
%{_datadir}/mpage

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.5.7-10
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.7-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.7-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.7-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.7-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Mar 07 2018 Michal Hlavinka <mhlavink@redhat.com> - 2.5.7-5
- add gcc buildrequire

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Jun 29 2017 Tom Callaway <spot@fedoraproject.org> - 2.5.7-1
- update to 2.5.7 (upstream relicenses code clearly under GPLv2+)

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.6-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.6-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.6-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.6-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.6-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.6-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.6-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.6-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.6-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.6-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.6-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Mar 27 2009 Michal Hlavinka <mhlavink@redhat.com> - 2.5.6-7
- fix doc in file section

* Fri Mar 27 2009 Michal Hlavinka <mhlavink@redhat.com> - 2.5.6-6
- preserve time stamps

* Fri Mar 27 2009 Michal Hlavinka <mhlavink@redhat.com> - 2.5.6-5
- clean-up for merge review

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Aug 11 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.5.6-3
- fix license tag

* Wed Feb 13 2008 Tomas Smetana <tsmetana@redhat.com> - 2.5.6-2
- rebuild (gcc-4.3)

* Tue Jan 15 2008 Tomas Smetana <tsmetana@redhat.com> - 2.5.6-1
- new upstream version

* Thu Aug 23 2007 Martin Bacovsky <mbacovsk@redhat.com> - 2.5.5-1
- upgrade to new upstream version 2.5.5

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 2.5.4-7.1
- rebuild

* Fri May 12 2006 Jitka Kudrnacova <jkudrnac@redhat.com> - 2.5.4-7
- Applied patch for font-restriction to avoid problems with gs (bug #191459)

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 2.5.4-6.1
- bump again for double-long bug on ppc(64)

* Wed Feb 08 2006 Jitka Kudrnacova <jkudrnac@redhat.com> 2.5.4-6
- Fixed page scaling (bug #173276) and modified the manpage
  (the bug was mentioned in the manpage)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 2.5.4-5.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Wed Mar  2 2005 Tim Waugh <twaugh@redhat.com> 2.5.4-5
- Rebuild for new GCC.

* Thu Feb 17 2005 Tim Waugh <twaugh@redhat.com> 2.5.4-4
- Fixed build with GCC 4.

* Wed Feb  9 2005 Tim Waugh <twaugh@redhat.com> 2.5.4-3
- Rebuilt.

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Jun  1 2004 Tim Waugh <twaugh@redhat.com> 2.5.4-1
- 2.5.4.

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Jun 23 2003 Tim Waugh <twaugh@redhat.com> 2.5.3-6
- Fix header output (bug #97764).
- Fix UTF-8 patch (bug #97763).
- Fix license tag (bug #97763).

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu May  8 2003 Tim Waugh <twaugh@redhat.com> 2.5.3-4
- Handle UTF-8 CJK (bug #90436).

* Wed Jan 22 2003 Tim Powers <timp@redhat.com> 2.5.3-3
- rebuilt

* Wed Nov  6 2002 Tim Waugh <twaugh@redhat.com> 2.5.3-2
- Fix segfault on malformed arguments (bug #77417).
- Removed unused patches.

* Sun Oct 20 2002 Tim Waugh <twaugh@redhat.com> 2.5.3-1
- 2.5.3 (bug #74401, bug #70826).

* Tue Jul 16 2002 Tim Waugh <twaugh@redhat.com> 2.5.2-4
- Fix segfault when MPAGE is set (bug #68701).

* Fri Jun 21 2002 Tim Powers <timp@redhat.com> 2.5.2-3
- automated rebuild

* Fri Jun 14 2002 Tim Waugh <twaugh@redhat.com> 2.5.2-2
- s/Copyright:/License:/.
- Don't explicitly strip binaries (bug #62564).
- Fix -H option (bug #57105).

* Wed Apr 24 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- update to 2.5.2

* Sat Apr 13 2002 Tim Powers <timp@redhat.com>
- bump release and rebuild

* Thu Nov  8 2001 Bill Nottingham <notting@redhat.com>
- don't segfault if run in a nonexistant locale (#55900)

* Sun Jun 24 2001 Elliot Lee <sopwith@redhat.com>
- Bump release + rebuild.

* Wed Apr 11 2001 Bill Nottingham <notting@redhat.com>
- only output japanese if we're running in japanese (#34882)

* Wed Jan 10 2001 Bill Nottingham <notting@redhat.com>
- actually *apply the patch*

* Mon Jan  8 2001 Bill Nottingham <notting@redhat.com>
- add patch to use mkstemp

* Mon Dec 18 2000 Bill Nottingham <notting@redhat.com>
- don't change the default papersize

* Mon Dec 18 2000 Yukihiro Nakai <ynakai@redhat.com>
- Add a Japanese patch.

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Sat Jun 10 2000 Bill Nottingham <notting@redhat.com>
- Hm. 2.5.1pre hasn't been touched in two years. I guess that's 'stable'.
- add a bugfix patch from debian.

* Thu Feb  3 2000 Bill Nottingham <notting@redhat.com>
- handle compressed man pages

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 7)

* Tue Jan 24 1999 Michael Maher <mike@redhat.com>
- changed group

* Thu Dec 17 1998 Michael Maher <mike@redhat.com>
- 6.0 build stuff.

* Sun Aug 16 1998 Jeff Johnson <jbj@redhat.com>
- build root

* Mon Apr 27 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Wed Oct 15 1997 Michael Fulbright <msf@redhat.com>
- (Re)applied patch to correctly print dvips output.

* Mon Jul 21 1997 Erik Troan <ewt@redhat.com>
- built against glibc
