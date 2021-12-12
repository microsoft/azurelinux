Vendor:         Microsoft Corporation
Distribution:   Mariner
Summary: A text-based modem control and terminal emulation program
Name: minicom
Version: 2.7.1
Release: 14%{?dist}
URL: https://salsa.debian.org/minicom-team/minicom
# Some files are built from Public Domain files in addition to GPLv2+ files
# (/usr/bin/minicom). Some LGPLv2+ files *may* be used in building of certain
# files (minicom, ascii-xfr, runscript). They are probably not actually used,
# but I wasn't able to exclude them from the build process completely yet.
# The rest is simply GPLv2+.
License: GPLv2+ and LGPLv2+ and Public Domain
#ExcludeArch: s390 s390x

Source0: https://alioth.debian.org/frs/download.php/file/4215/%{name}-%{version}.tar.gz

# Upstream patch:
Patch1: 0001-Add-a-missing-va_end-call.patch
# Upstream patch:
Patch2: 0002-Make-sure-strings-copied-by-strncpy-are-null-termina.patch
# Upstream patch:
Patch3: 0003-Fix-file-descriptor-leaks.patch
# Upstream patch:
Patch4: 0004-Fix-a-directory-handle-leak.patch
# Upstream patch:
Patch5: 0005-Fix-a-read-past-end-of-buffer.patch
# Upstream patch:
Patch6: 0006-Fix-a-warning-about-an-unused-variable.patch
# Upstream patch:
Patch7: 0007-loadconv-Add-missing-fclose.patch
# Upstream patch:
Patch8: 0001-Drop-superfluous-global-variable-definitions.patch
# Upstream patch:
Patch9: 0002-Drop-superfluous-global-variable-definitions.patch
# Upstream patch:
Patch10: 0003-Drop-superfluous-global-variable-definitions.patch

BuildRequires: lockdev-devel ncurses-devel autoconf automake gettext-devel
BuildRequires: gcc
# For %%autosetup -S git:
BuildRequires: git
Requires: lockdev lrzsz


%description
Minicom is a simple text-based modem control and terminal emulation
program somewhat similar to MSDOS Telix. Minicom includes a dialing
directory, full ANSI and VT100 emulation, an (external) scripting
language, and other features.


%prep
%autosetup -S git

cp -pr doc doc_
rm -f doc_/Makefile*


%build
#./autogen.sh
autoreconf --verbose --force --install

# Remove unused files to make sure we've got the License tag right.
# It seems this needs to be done after autoreconf, otherwise it will fail.
rm -f lib/snprintf.c

%configure
%make_build


%install
%make_install
mkdir -p %{buildroot}%{_sysconfdir}

%find_lang %{name}


%files -f %{name}.lang
%doc ChangeLog AUTHORS NEWS TODO doc_/*
%license COPYING
# DO NOT MAKE minicom SUID/SGID anything.
%{_bindir}/minicom
%{_bindir}/runscript
%{_bindir}/xminicom
%{_bindir}/ascii-xfr
%{_mandir}/man1/*


%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.7.1-14
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Mon Feb 10 2020 Ondřej Lysoněk <olysonek@redhat.com> - 2.7.1-13
- Fix build with gcc 10
- Resolves: rhbz#1799652

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Aug 13 2018 Ondřej Lysoněk <olysonek@redhat.com> - 2.7.1-9
- Fix issues found by Coverity Scan
- Resolves: rhbz#1602618

* Mon Jul 23 2018 Ondřej Lysoněk <olysonek@redhat.com> - 2.7.1-8
- Corrected the License tag

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Feb 19 2018 Ondřej Lysoněk <olysonek@redhat.com> - 2.7.1-6
- Add gcc to BuildRequires

* Tue Feb 13 2018 Vasiliy N. Glazov <vascom2@gmail.com> - 2.7.1-5
- Cleanup spec

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Jul 15 2017 Filipe Rosset <rosset.filipe@gmail.com> - 2.7.1-1
- Rebuilt to new upstream version 2.7.1 fixes rhbz#1443071 and rhbz#1443129

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.7-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.7-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 2.7-4
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Jan 06 2014 Jaromir Capik <jcapik@redhat.com> - 2.7-1
- Update to 2.7
- Fixing bogus dates in the changelog

* Wed Aug 07 2013 Jaromir Capik <jcapik@redhat.com> - 2.6.2-4
- Fixing the license tag

* Wed Jul 31 2013 Jaromir Capik <jcapik@redhat.com> - 2.6.2-3
- RH man page scan (#948521)

* Thu Feb 07 2013 Jaromir Capik <jcapik@redhat.com> - 2.6.2-2
- Disabling lockfile warnings when the device disappears (ttyUSB hot unplug)

* Thu Feb 07 2013 Jaromir Capik <jcapik@redhat.com> - 2.6.2-1
- Update to 2.6.2

* Wed Jan 23 2013 Jaromir Capik <jcapik@redhat.com> - 2.6.1-2
- Disable lock path config when built with lockdev (#754235)

* Tue Jan 22 2013 Jaromir Capik <jcapik@redhat.com> - 2.6.1-1
- Update to 2.6.1

* Thu Nov 22 2012 Jaromir Capik <jcapik@redhat.com> 2.5-11
- Fixing the license tag

* Wed Nov 21 2012 Jaromir Capik <jcapik@redhat.com> 2.5-10
- Removing de-ANSI-fication (obsolete - support removed from autotools)

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Oct 24 2011 Jaromir Capik <jcapik@redhat.com> 2.5-7
- applying modified lockdev patch made by Jiri Popelka (#747936)
- minor spec file changes according to the latest guidelines

* Wed Apr 6 2011 Jan Görig <jgorig@redhat.com> 2.5-6
- reverted last change (#681898)

* Wed Mar 9 2011 Jan Görig <jgorig@redhat.com> 2.5-5
- dropped rh patch because /var/lock/lockdev is now world writeable

* Thu Feb 24 2011 Jan Görig <jgorig@redhat.com> 2.5-4
- fixed crashing on device reconnecting (#678812)

* Wed Feb 09 2011 Jan Görig <jgorig@redhat.com> 2.5-3
- fixed crashing on non-readable directory (#675400)
- fixed typos in minicom and runscript manpages (#675453,#675456)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jan 31 2011 Jan Görig <jgorig@redhat.com> 2.5-1
- update to new upstream version
- remove patches merged by upstream
- update rh patch to support unix socket (#592355)

* Fri Jan 14 2011 Jan Görig <jgorig@redhat.com> 2.4-2
- fixed typos in ascii-xfr manpage (#669098)
- fixed empty lines handling in configuration file (#669406)

* Tue Mar 9 2010 Jan Görig <jgorig@redhat.com> 2.4-1
- update to 2.4
- /etc/minicom.users removed by upstream
- add minicom-2.4-config.patch
- remove minicom-2.3-getline.patch - fixed in upstream
- remove minicom-2.3-drop-privs.patch - permissions handling removed by upstream
- remove minicom-2.3-ncurses.patch - deprecated
- modify minicom-2.4-rh.patch - wrong doinit checking (#519637)

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jul 16 2009 Miroslav Lichvar <mlichvar@redhat.com> 2.3-5
- rename getline to avoid conflict with glibc (#511715)
- remove makefiles from docs
- drop wchar patch

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Aug 29 2008 Miroslav Lichvar <mlichvar@redhat.com> 2.3-3
- rediff patches with fuzz

* Thu Mar 13 2008 Lubomir Kundrak <lkundrak@redhat.com> 2.3-2
- Add ChangeLog to %%doc

* Sun Feb 24 2008 Lubomir Kundrak <lkundrak@redhat.com> 2.3-1
- 2.3

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2.2-6
- Autorebuild for GCC 4.3

* Sun Sep 23 2007 Lubomir Kundrak <lkundrak@redhat.com> 2.2-5
- Fix capture file handling (#302081)

* Wed Aug 22 2007 Miroslav Lichvar <mlichvar@redhat.com> 2.2-4
- update license tag

* Wed Jul 25 2007 Miroslav Lichvar <mlichvar@redhat.com> 2.2-3
- check for errors on tty device (#248701)

* Tue Jul 10 2007 Miroslav Lichvar <mlichvar@redhat.com> 2.2-2
- improve signal handling a bit (#246465)

* Fri Mar 09 2007 Miroslav Lichvar <mlichvar@redhat.com> 2.2-1
- update to 2.2
- handle filenames with spaces (#98655)
- add requires for lrzsz
- spec cleanup

* Tue Jul 18 2006 Martin Stransky <stransky@redhat.com> 2.1-3
- removed unnecessary debug output (#199707)

* Tue Jul 18 2006 Martin Stransky <stransky@redhat.com> 2.1-2
- added ncurses-devel to BuildPrereq

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 2.1-1.2.2
- rebuild

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 2.1-1.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 2.1-1.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Thu Jul 14 2005 Martin Stransky <stransky@redhat.com> 2.1-1
- New upstream version

* Mon Mar  7 2005 Martin Stransky <stransky@redhat.com>
- gcc4 patch

* Wed Oct 20 2004 Adrian Havill <havill@redhat.com> 2.00.0-20
- correct an off-by-one error array-store error (#110770)

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Sep 12 2003 Adrian Havill <havill@redhat.com> 2.00.0-17.1
- bump n-v-r for RHEL

* Fri Sep 12 2003 Adrian Havill <havill@redhat.com> 2.00.0-17
- fix error handling for the case when you attempt to "goto" a dir
  that doesn't exist. (#103902)
- updated URL in spec file

* Thu Aug 21 2003 Adrian Havill <havill@redhat.com> 2.00.0-16.1
- bump n-v-r for RHEL

* Thu Aug 21 2003 Adrian Havill <havill@redhat.com> 2.00.0-16
- don't overwrite buffer when ins chars (#98733)

* Wed Aug 20 2003 Adrian Havill <havill@redhat.com> 2.00.0-15.1
- bump n-v-r for RHEL

* Wed Aug 20 2003 Adrian Havill <havill@redhat.com> 2.00.0-15
- initialize savetrans, check vttrans to prevent segfaults with
  certain ESC sequences (#84129)

* Fri Aug 01 2003 Adrian Havill <havill@redhat.com> 2.00.0-14
- removed static buffers that limit multi-file zmodem functionality (#98654)
- removed assertions from above patch, massage out conflicts with rh patch

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Sat Jan 18 2003 Mike A. Harris <mharris@redhat.com> 2.00.0-11
- Update spec file URL to new homepage (#71894)

* Mon Dec  2 2002 Tim Powers <timp@redhat.com> 2.00.0-10
- add PreReq coreutils so that we get the ordering right in the
  install

* Wed Nov 13 2002 Mike A. Harris <mharris@redhat.com> 2.00.0-9
- Added find_lang macro andlang files to package, also avoiding 
  _unpackaged_files_terminate_build
- Added with_desktop_menu_entry macro to disable minicom.desktop by default

* Tue Oct  8 2002 Mike A. Harris <mharris@redhat.com> 2.00.0-8
- All-arch rebuild
- Make /etc/minicom.users config(noreplace)

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Sun May 26 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Tue May 21 2002 Mike A. Harris <mharris@redhat.com> 2.00.0-4
- Rebuilt in new build environment

* Tue Feb 26 2002 Mike A. Harris <mharris@redhat.com> 2.00.0-3
- Rebuilt in new build environment

* Wed Jan 09 2002 Tim Powers <timp@redhat.com> 2.00.0-2
- automated rebuild

* Wed Nov 21 2001 Mike A. Harris <mharris@redhat.com> 2.00.0-1
- Updated to version 2.00.0-0, which now uses GNU autoconf for everything,
  to ease portability and internationalization issues.  Hold on for the
  ride, as there's bound to be some bumps on the way.  ;o)  On the up side,
  the packaging is likely to be MUCH more maintainable in the future, which
  is very nice to see.
- Disabled most patches as they are either included now, not needed, or
  it has yet to be determined.

* Fri Oct 12 2001 Trond Eivind Glomsrød <teg@redhat.com> 1.83.1-17
- Delete bad entries in ko.po, fix charset in ja.po

* Tue Aug 28 2001 Jeff Johnson <jbj@redhat.com>
- map specific errno's into status for return from helper.

* Tue Aug 14 2001 Jeff Johnson <jbj@redhat.com>
- rebuild against unzigged lockdev-1.0.0-11 (#51577).
- add BuildPrereq: on lockdev-devel, not /usr/include/baudboy.h.

* Sun Aug 12 2001 Mike A. Harris <mharris@redhat.com> 1.83.1-14
- Added Requires: lockdev (#51576)
- s/Copyright/License/

* Sat Jul 28 2001 Jeff Johnson <jbj@redhat.com>
- use baudboy for serial port locking.

* Mon Jul 23 2001 Mike A. Harris <mharris@redhat.com> 1.83.1-12
- Added minicom-1.83.1-disable-message.patch to disable warning message and
  delay when running minicom as root since root-only is the only supported
  method of running minicom now due to security issues.
  
* Sat Jul 21 2001 Tim Powers <timp@redhat.com> 1.83.1-11
- no minicom applnk entry. Is cluttering up the menus

* Tue Jun 19 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- add ExcludeArch: s390 s390x
- allow to build with newer gettext versions

* Thu May  3 2001 Mike A. Harris <mharris@redhat.com> 1.83.1-8
- Changed minicom to disable SGID/SUID operation completely as it was
  never designed to be secure, and likely never will be. (#35613)
- Updated the format string patch I made to fix more format string abuses.
- Added Czeck cs_CZ locale translations.

* Thu Apr 12 2001 Mike A. Harris <mharris@redhat.com>
- Fixed format string vuln in usage of do_log()  (bug #35613)
- Fixed misc other format string abuse with werror().
- Changed main tarball to bzip2 compression
- Corrected Buildroot to use _tmppath

* Tue Mar 27 2001 Crutcher Dunnavant <crutcher@redhat.com>
- patch to drop mask for config file

* Fri Feb 23 2001 Jakub Jelinek <jakub@redhat.com>
- fix build under glibc 2.2.2

* Thu Aug 24 2000 Bill Nottingham <notting@redhat.com>
- drop privs on opening of capture file

* Fri Aug  4 2000 Bill Nottingham <notting@redhat.com>
- add translation to desktop entry

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Sat Jun 10 2000 Bill Nottingham <notting@redhat.com>
- update to 1.83.1

* Wed Apr  5 2000 Bill Nottingham <notting@redhat.com>
- rebuild against current ncurses/readline

* Tue Mar  7 2000 Jeff Johnson <jbj@redhat.com>
- rebuild for sparc baud rates > 38400.

* Mon Feb 07 2000 Preston Brown <pbrown@redhat.com>
- wmconfig -> desktop

* Wed Feb 02 2000 Cristian Gafton <gafton@redhat.com>
- fix description

* Fri Dec 17 1999 Bill Nottingham <notting@redhat.com>
- update to 1.83.0

* Fri Jul 30 1999 Bill Nottingham <notting@redhat.com>
- update to 1.82.1
- s/sunsite/metalab

* Wed May 19 1999 Jeff Johnson <jbj@redhat.com>
- restore setgid uucp to permit minicom to lock in /var/lock (#2922).

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 5)

* Sun Jan 24 1999 Michael Maher <mike@redhat.com>
- fixed bug, changed groups.

* Thu Oct 01 1998 Cristian Gafton <gafton@redhat.com>
- updated to 1.82 to include i18n fixes

* Wed Sep 02 1998 Michael Maher <mike@redhat.com>
- Built package for 5.2.

* Sun May 10 1998 Cristian Gafton <gafton@redhat.com>
- security fixes (alan cox, but he forgot about the changelog)

* Thu May 07 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Thu May 07 1998 Cristian Gafton <gafton@redhat.com>
- BuildRoot; updated .make patch to cope with the buildroot
- fixed the spec file

* Wed May 06 1998 Michael Maher <mike@redhat.com>
- update of package (1.81)

* Wed Oct 29 1997 Otto Hammersmith <otto@redhat.com>
- added wmconfig entries

* Tue Oct 21 1997 Otto Hammersmith <otto@redhat.com>
- fixed source url

* Thu Jul 10 1997 Erik Troan <ewt@redhat.com>
- built against glibc
