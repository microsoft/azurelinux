Summary:        Spell checker
Name:           aspell
Version:        0.60.8.1
Release:        1%{?dist}
# LGPLv2+ .. common/gettext.h
# LGPLv2  .. modules/speller/default/phonet.hpp,
#            modules/speller/default/phonet.cpp,
#            modules/speller/default/affix.cpp
# GPLv2+  .. ltmain.sh, misc/po-filter.c
# BSD     .. myspell/munch.c
License:        LGPLv2+ AND LGPLv2 AND GPLv2+ AND BSD
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            http://aspell.net/
Source:         ftp://ftp.gnu.org/gnu/aspell/aspell-%{version}.tar.gz
Patch0:         aspell-0.60.7-fileconflict.patch
Patch1:         aspell-0.60.7-pspell_conf.patch
BuildRequires:  chrpath
BuildRequires:  gcc-c++
BuildRequires:  gettext
BuildRequires:  ncurses-devel
BuildRequires:  perl-interpreter
BuildRequires:  pkg-config

%description
GNU Aspell is a spell checker designed to eventually replace Ispell. It can
either be used as a library or as an independent spell checker. Its main
feature is that it does a much better job of coming up with possible
suggestions than just about any other spell checker out there for the
English language, including Ispell and Microsoft Word. It also has many
other technical enhancements over Ispell such as using shared memory for
dictionaries and intelligently handling personal dictionaries when more
than one Aspell process is open at once.

%package devel
Summary:        Libraries and header files for Aspell development
Requires:       %{name} = %{version}-%{release}
Requires:       pkg-config

%description devel
The aspell-devel package includes libraries
and header files needed for Aspell development.

%prep
%setup -q
%patch0 -p1 -b .fc
%patch1 -p1 -b .mlib
iconv -f iso-8859-2 -t utf-8 < manual/aspell.info > manual/aspell.info.aux
mv manual/aspell.info.aux manual/aspell.info

%build
%configure --disable-rpath
sed -i -e 's! -shared ! -Wl,--as-needed\0!g' libtool
make %{?_smp_mflags}
cp scripts/aspell-import examples/aspell-import
chmod 644 examples/aspell-import
cp manual/aspell-import.1 examples/aspell-import.1

%install
%make_install

mkdir -p %{buildroot}%{_libdir}/aspell-0.60

mv %{buildroot}%{_libdir}/aspell-0.60/ispell %{buildroot}%{_bindir}
mv %{buildroot}%{_libdir}/aspell-0.60/spell %{buildroot}%{_bindir}

chrpath --delete %{buildroot}%{_libdir}/aspell-0.60//nroff-filter.so
chrpath --delete %{buildroot}%{_libdir}/aspell-0.60//sgml-filter.so
chrpath --delete %{buildroot}%{_libdir}/aspell-0.60//context-filter.so
chrpath --delete %{buildroot}%{_libdir}/aspell-0.60//email-filter.so
chrpath --delete %{buildroot}%{_libdir}/aspell-0.60//tex-filter.so
chrpath --delete %{buildroot}%{_libdir}/aspell-0.60//texinfo-filter.so
chrpath --delete %{buildroot}%{_libdir}/aspell-0.60//markdown-filter.so
chrpath --delete %{buildroot}%{_bindir}/aspell
chrpath --delete %{buildroot}%{_libdir}/libpspell.so.*

rm -f %{buildroot}%{_libdir}/libaspell.la
rm -f %{buildroot}%{_libdir}/libpspell.la
rm -f %{buildroot}%{_libdir}/aspell-0.60/*-filter.la
rm -f %{buildroot}%{_bindir}/aspell-import
rm -f %{buildroot}%{_mandir}/man1/aspell-import.1
rm -f %{buildroot}%{_infodir}/dir

%find_lang %{name}

%files -f %{name}.lang
%license COPYING
%doc README TODO examples/aspell-import examples/aspell-import.1
%dir %{_libdir}/aspell-0.60
%{_bindir}/a*
%{_bindir}/ispell
%{_bindir}/pr*
%{_bindir}/run-with-aspell
%{_bindir}/spell
%{_bindir}/word-list-compress
%{_libdir}/lib*.so.*
%{_libdir}/aspell-0.60/*
%{_infodir}/aspell.*
%{_mandir}/man1/aspell.1.*
%{_mandir}/man1/run-with-aspell.1*
%{_mandir}/man1/word-list-compress.1*
%{_mandir}/man1/prezip-bin.1.*

%files devel
%dir %{_includedir}/pspell
%{_bindir}/pspell-config
%{_includedir}/aspell.h
%{_includedir}/pspell/pspell.h
%{_libdir}/lib*spell.so
%{_libdir}/pkgconfig/*
%{_infodir}/aspell-dev.*
%{_mandir}/man1/pspell-config.1*

%changelog
* Mon Jan 22 2024 Sean Dougherty <sdougherty@microsoft.com> - 0.60.8.1-1
- Upgrade to 0.60.8.1 for Mariner 3.0

* Wed Sep 20 2023 Jon Slobodzian <joslobo@microsoft.com> - 0.60.8-8
- Recompile with stack-protection fixed gcc version (CVE-2023-4039)

* Fri Oct 14 2022 Henry Li <lihl@microsoft.com> - 0.60.8-7
- Rename aspell-0.60.8-objstack.patch to CVE-2019-25051.patch to make the CVE
  scanner tool recognize the fix patch

* Fri Oct 07 2022 Osama Esmail <osamaesmail@microsoft.com> - 0.60.8-6
- Moved from SPECS-EXTENDED to SPECS
- Added patch for CVE-2019-25051
- License verified

* Mon Nov 01 2021 Muhammad Falak <mwani@microsft.com> - 0.60.8-5
- Remove epoch

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 12:0.60.8-4
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 12:0.60.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Oct 22 2019 Nikola Forró <nforro@redhat.com> - 12:0.60.8-2
- remove RPATH from markdown-filter.so

* Fri Oct 18 2019 Nikola Forró <nforro@redhat.com> - 12:0.60.8-1
- resolves: #1761152
  update to 0.60.8

* Mon Aug 19 2019 Nikola Forró <nforro@redhat.com> - 12:0.60.7-1
- resolves: #1742373
  update to 0.60.7

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 12:0.60.6.1-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 12:0.60.6.1-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 12:0.60.6.1-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Nikola Forró <nforro@redhat.com> - 12:0.60.6.1-23
- remove ldconfig from scriptlets

* Tue Jun 19 2018 Nikola Forró <nforro@redhat.com> - 12:0.60.6.1-22
- remove install-info from scriptlets

* Wed Apr 04 2018 Nikola Forró <nforro@redhat.com> - 12:0.60.6.1-21
- resolves: #1562364
  do not call back() on an empty vector

* Tue Feb 20 2018 Nikola Forró <nforro@redhat.com> - 12:0.60.6.1-20
- add missing gcc-c++ build dependency

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 12:0.60.6.1-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 12:0.60.6.1-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 12:0.60.6.1-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Feb 23 2017 Nikola Forró <nforro@redhat.com> - 12:0.60.6.1-16
- resolves: #1423239
  fix building with GCC 7

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 12:0.60.6.1-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Dec 06 2016 Nikola Forró <nforro@redhat.com> - 12:0.60.6.1-14
- resolves: #1401713
  add perl to BuildRequires

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 12:0.60.6.1-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 12:0.60.6.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 12:0.60.6.1-11
- Rebuilt for GCC 5 C++11 ABI change

* Fri Aug 15 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 12:0.60.6.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 12:0.60.6.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 12:0.60.6.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Mar 25 2013 Peter Schiffer <pschiffe@redhat.com> - 12:0.60.6.1-7
- resolves: #925034
  add support for aarch64

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 12:0.60.6.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Aug 27 2012 Peter Schiffer <pschiffe@redhat.com> - 12:0.60.6.1-5
- done some minor .spec file cleanup

* Thu Jul 19 2012 Peter Schiffer <pschiffe@redhat.com> - 12:0.60.6.1-4
- resolves: #813261
  fixed crash when trying to run "aspell dump personal"

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 12:0.60.6.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 12:0.60.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Aug 16 2011 Peter Schiffer <pschiffe@redhat.com> - 12:0.60.6.1-1
- resolves: #718946
  update to 0.60.6.1

* Mon May  2 2011 Ivana Hutarova Varekova <varekova@redhat.com> - 12.0.60.6-15
- fix minor problems in spec file

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 12:0.60.6-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Aug 17 2010 Ivana Hutarova Varekova <varekova@redhat.com> - 12.0.60.6-13
- remove obsolete links from man-pages

* Tue Mar  2 2010 Ivana Hutarova Varekova <varekova@redhat.com> - 12.0.60.6-12
- fix -devel scriptlets

* Tue Dec 15 2009 Ivana Hutarova Varekova <varekova@redhat.com> - 12:0.60.6-11
- remove obsolete patch

* Fri Dec  4 2009 Ivana Hutarova Varekova <varekova@redhat.com> - 12:0.60.6-10
- fix rpath problem (chrpath)

* Tue Dec  1 2009 Ivana Hutarova Varekova <varekova@redhat.com> - 12:0.60.6-9
- add --disable-rpath to configure part
  remove remanent obsolete tags
  fix license field

* Fri Nov 27 2009 Ivana Hutarova Varekova <varekova@redhat.com> - 12:0.60.6-8
- change summary name
  remove outdated Obsoletes, Conflicts and Provides flag
  fix requirement to install-info (pre -> post)
  move aspell-import to documentation part
  remove exit 0 from scriptlets

* Mon Aug 10 2009 Ivana Varekova <varekova@redhat.com> - 12:0.60.6-7
- fix installation with --excludedocs option (#515911)

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 12:0.60.6-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 12:0.60.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Feb 12 2009 Ivana Varekova <varekova@redhat.com> - 12:0.60.6-4
- remove aspell-en require

* Mon Sep  1 2008 Ivana Varekova <varekova@redhat.com> - 12:0.60.6-3
- fix patch format

* Thu May 29 2008 Ivana Varekova <varekova@redhat.com> - 12:0.60.6-2
- Resolves: #447428
  aspell sigserv on checking file with 0 length

* Wed May  7 2008 Ivana Varekova <varekova@redhat.com> - 12:0.60.6-1
- update to 0.60.6

* Wed Feb 20 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 12:0.60.5-5
- Autorebuild for GCC 4.3

* Tue Jan 22 2008 Ivana Varekova <varekova@redhat.com> - 12:0.60.5-4
- add gcc43 patch

* Thu Feb  8 2007 Ivana Varekova <varekova@redhat.com> - 12:0.60.5-3
- incorporate package review feedback

* Mon Jan 22 2007 Ivana Varekova <varekova@redhat.com> - 12:0.60.5-2
- Resolves: 223676
  fix non-failsafe install-info problem

* Tue Jan  2 2007 Ivana Varekova <varekova@redhat.com> - 12:0.60.5-1
- update to 0.60.4
- cleanup spec file

* Wed Nov  8 2006 Ivana Varekova <varekova@redhat.com> - 12:0.60.4-1
- update to 0.60.4

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 12:0.60.3-7.1
- rebuild

* Tue May 23 2006 Ivana Varekova <varekova@redhat.com> - 12:0.60.3-7
- fix multilib problem (used pkgconfig)

* Wed Mar 22 2006 Ivana Varekova <varekova@redhat.com> - 12:0.60.3-6
- remove .la files (bug 184184)

* Thu Mar  2 2006 Ivana Varekova <varekova@redhat.com> - 12:0.60.3-5
- update aspell man page (bug 183205)

* Tue Feb 21 2006 Ivana Varekova <varekova@redhat.com> - 12:0.60.3-4
- fix multilib file conflict

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 12:0.60.3-3.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 12:0.60.3-3.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Mon Dec 19 2005 Ivana Varekova <varekova@redhat.com> 12:0.60.3-3
- fix for gcc 4.1

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Fri Jul 15 2005 Ivana Varekova <varekova@redhat.com> 12:0.60.3-2
- fix install-info problem 

* Wed Jul 13 2005 Ivana Varekova <varekova@redhat.com> 12:0.60.3-1
- update to 0.60.3 - (bug 141968) thanks to Dawid Gajownik 
- add BuildRequires: ncurses-devel, gettext 
- add config script patch (thanks tmraz@redhat.com)

* Mon Mar  7 2005 Ivana Varekova <varekova@redhat.com> 12:0.50.5-6
- rebuilt

* Thu Jan 13 2005 Adrian Havill <havill@redhat.com> 12:0.50.5-5
- added aspell-pt_BR to the obsoletes

* Fri Nov 12 2004 Warren Togami <wtogami@redhat.com> 12:0.50.5-4
- rebuild

* Wed Oct 06 2004 Than Ngo <than@redhat.com> 12:0.50.5-3.fc3
- add obsolete aspell-config

* Mon Aug 23 2004 Adrian Havill <havill@redhat.com> 12:0.50.5-2.fc3
- fix doc dir (#128140) (don't flag aspell doc stuff with the doc macro
  flag due to rpm badness)

* Mon Jun 21 2004 Warren Togami <wtogami@redhat.com> 12:0.50.5-1
- update to 0.50.5

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Jan 29 2004 Adrian Havill <havill@redhat.com> 12:0.50.50.3-18
- make rpm own some unclaimed dirs (#112984, #113778)
- explicitly claim kbd anbd dat files in /usr/share/aspell
- a little spec file files cleanup-- macro subs, dir prefix
- make /usr/lib/aspell; don't make the dictionary packages do it

* Mon Nov 17 2003 Thomas Woerner <twoerner@redhat.com> 12:0.50.3-17
- fixed build: added make to %%build to avoid rpath for build directory

* Tue Oct 07 2003 Adrian Havill <havill@redhat.com> 12:0.50.3-16
- moved spell compat script from /usr/share/aspell to /usr/bin (#105921)

* Tue Jul 01 2003 Adrian Havill <havill@redhat.com> 11:0.50.3-15
- moved ispell compat script from /usr/share/aspell to /usr/bin (#90907)

* Tue Jun 24 2003 Adrian Havill <havill@redhat.com> 10:0.50.3-14
- removed emacs/xemacs el files which are already provided

* Wed Jun 18 2003 Adrian Havill <havill@redhat.com> 9:0.50.3-13
- provide pspell-devel in addition to obsoleting it

* Tue Jun 10 2003 Adrian Havill <havill@redhat.com> 8:0.50.3-12
- obsolete old dicts designed for previous aspell

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri May 30 2003 Joe Orton <jorton@redhat.com> 7:0.50.3-10
- rebuild again to fix libpspell deps

* Fri May 30 2003 Joe Orton <jorton@redhat.com> 7:0.50.3-9
- remove ExcludeArch

* Thu May 22 2003 Jeremy Katz <katzj@redhat.com> 7:0.50.3-8
- fix build with gcc 3.3

* Wed May 21 2003 Adrian Havill <havill@redhat.com> 0.50.3-7
- require aspell-en for upgrades

* Sun May 11 2003 Jeremy Katz <katzj@redhat.com> 6:0.50.3-6
- -devel should obsolete pspell-devel

* Tue May  6 2003 Joe Orton <jorton@redhat.com> 0.50.3-5
- include libpspell.so in devel package

* Thu May  1 2003 Adrian Havill <havill@redhat.com> 0.50.3-4
- removed .la files

* Wed Apr 16 2003 Adrian Havill <havill@redhat.com> 0.50.3-3
- Changed the header for provides, obsoletes, epoch
- fixed config prefix in dirs.h

* Wed Apr 16 2003 Adrian Havill <havill@redhat.com> 0.50.3-1
- upgrade to 0.50.3

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Fri Nov  8 2002 Tim Powers <timp@redhat.com>
- fix broken pspell epoch dep
- create $RPM_BUILD_ROOT/usr/bin by hand
- remove /usr/doc
- fix hardcoding of /usr/lib so that we can build on x86_64

* Tue Aug 13 2002 Nalin Dahyabhai <nalin@redhat.com> 0.33.7.1-16
- require pspell and pspell-devel using the proper epoch

* Sat Aug 10 2002 Elliot Lee <sopwith@redhat.com>
- rebuilt with gcc-3.2 (we hope)

* Mon Jul 22 2002 Tim Powers <timp@redhat.com> 0.33.7.1-14
- rebuild using gcc-3.2-0.1

* Fri Jun 21 2002 Tim Powers <timp@redhat.com> 0.33.7.1-13
- automated rebuild

* Thu Jun 13 2002 Trond Eivind Glomsrød <teg@redhat.com> 0.33.7.1-12
- Rebuild to make it work again... #66708

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Mon May 13 2002 Trond Eivind Glomsrød <teg@redhat.com> 0.33.7.1-10
- Rebuild

* Thu Feb 21 2002 Trond Eivind Glomsrød <teg@redhat.com> 0.33.7.1-9
- Disable evil patch

* Mon Jan 28 2002 Trond Eivind Glomsrød <teg@redhat.com> 0.33.7.1-8
- Build on more archs (doh)

* Tue Jan 22 2002 Trond Eivind Glomsrød <teg@redhat.com> 0.33.7.1-7
- Make it compile with new compiler (evil workaround)

* Wed Jan 16 2002 Trond Eivind Glomsrød <teg@redhat.com> 0.33.7.1-5
- Rebuild
- Unexclude alpha

* Fri Dec 14 2001 Trond Eivind Glomsrød <teg@redhat.com> 0.33.7.1-3
- Rebuild
- Don't build on alpha

* Mon Oct 29 2001 Bernhard Rosenkraenzer <bero@redhat.com> 0.33.7.1-2
- "make it work with gcc 3.1" ;)

* Tue Sep 18 2001 Trond Eivind Glomsrød <teg@redhat.com> 0.33.7.1-1
- 0.33.7.1, which is a "make it work with gcc 3" release

* Wed Sep 12 2001 Tim Powers <timp@redhat.com>
- rebuild with new gcc and binutils

* Thu Aug  9 2001 Trond Eivind Glomsrød <teg@redhat.com> 0.33.7-1
- 0.33.7 bugfix release. Requested by the author, it fixes
  coredumps in sug-mode and when not using typo-analyses.
  It also contains code cleanups so it compiles with -ansi
- should fix coredump on IA64 (#49746)

* Wed Jul 11 2001 Trond Eivind Glomsrød <teg@redhat.com>
- Add the .la files in the main package - used for dynamic loading

* Sun Jun  3 2001 Trond Eivind Glomsrød <teg@redhat.com>
- 0.33.6.3, which includes the fix made yesterday

* Sat Jun  2 2001 Trond Eivind Glomsrød <teg@redhat.com>
- Make it search for directories in the correct location

* Wed May 30 2001 Trond Eivind Glomsrød <teg@redhat.com>
- No more workarounds at the specfile level

* Tue May 29 2001 Trond Eivind Glomsrød <teg@redhat.com>
- Use custom ltmain.sh to work around buggy bundled libtool

* Sun May 20 2001 Trond Eivind Glomsrød <teg@redhat.com>
- 0.33.6
- use standard %%configure macro - it works now.

* Fri May 11 2001 Bernhard Rosenkraenzer <bero@redhat.com> 0.33.5-2
- Rebuild with new libltdl

* Mon Apr 23 2001 Trond Eivind Glomsrød <teg@redhat.com>
- 0.33.5

* Thu Nov 30 2000 Trond Eivind Glomsrød <teg@redhat.com>
- use new emacs init scheme for Emacs and XEmacs

* Wed Nov 22 2000 Trond Eivind Glomsrød <teg@redhat.com>
-  .32.6

* Sat Aug 19 2000 Trond Eivind Glomsrød <teg@redhat.com>
- .32.5 bugfix release (also contains improved documentation),
  obsolete old patch
- the compatibility scripts are now part of the package itself
- clean up build procedure
- remove manual.aux file from docs (#16424)

* Sun Aug 06 2000 Trond Eivind Glomsrød <teg@redhat.com>
- .32.1 bugfix release, obsolete old patch
- rename to 0.32.1
- add patch from author to change his email address
- add spell and ispell compatibility scripts

* Fri Aug 04 2000 Trond Eivind Glomsrød <teg@redhat.com>
- rebuild

* Tue Aug 01 2000 Trond Eivind Glomsrød <teg@redhat.com>
- remember to obsolete ispell
- build the Canadian and British dictionaries here now,
  as part of the main package. Same package names and 
  descriptions.

* Mon Jul 24 2000 Trond Eivind Glomsrød <teg@redhat.com>
- .32
- remove old patches, add a patch since namespace isn't 
  polluted as much anymore (as opposed to older toolchain)

* Wed Jul 19 2000 Trond Eivind Glomsrød <teg@redhat.com>
- rebuild

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Tue Jul  4 2000 Jakub Jelinek <jakub@redhat.com>
- Rebuild with new C++

* Fri Jun 30 2000 Trond Eivind Glomsrød <teg@redhat.com>
- use RPM_OPT_FLAGS, not just -O0
- dont include .la-files

* Fri Jun 23 2000 Trond Eivind Glomsrød <teg@redhat.com>
- excludearch ia64

* Fri Jun 23 2000 Trond Eivind Glomsrød <teg@redhat.com>
- patch to work around compiler bug(?) wrt. inline functions
- use CFLAGS and CXXFLAGS
- set them to -O0 to work around YACB
- copy libtool files for IA64 support

* Sun Jun 18 2000 Trond Eivind Glomsrød <teg@redhat.com>
- update to .31.1. My patch was upstreamed and is no longer needed.
- new patch added so DESTDIR works properly

* Fri Jun 16 2000 Trond Eivind Glomsrød <teg@redhat.com>
- (this entry includes some old ones...)
- update to .31
- added patch to make it compile with a pickier compiler
- include /usr/share/pspell

* Mon May 1 2000 Tim Powers <timp@redhat.com>
- updated to .30.1
- used build fixes from Ryan Weaver's 0.30.1-1 package on sourceforge
- updated URL, download/ftp location
- removed redundant define's at top of spec file

* Thu Jul 8 1999 Tim Powers <timp@redhat.com>
- built for Powertools 6.1
- removed serial macro definitions from spec file to make versioning
  consistant with the other packages we ship.
- changed build root path
- general spec file cleanups

* Tue Mar  2 1999 Ryan Weaver <ryanw@infohwy.com>
  [aspell-.27.2-2]
- Changes from .27.1 to .27.2 (Mar 1, 1999)
- Fixed a major bug that caused aspell to dump core when used
  without any arguments
- Fixed another major bug that caused aspell to do nothing when used
  in interactive mode.
- Added an option to exit in Aspell's interactive mode.
- Removed some old documentation files from the distribution.
- Minor changes on to the section on using Aspell with egcs.
- Minor changes to remove -Wall warnings.
