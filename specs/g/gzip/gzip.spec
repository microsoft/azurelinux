# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Summary: GNU data compression program
Name: gzip
Version: 1.13
Release: 5%{?dist}
# info pages are under GFDL license
License: GPL-3.0-or-later AND GFDL-1.3-only
Source0: https://ftp.gnu.org/gnu/gzip/gzip-%{version}.tar.xz
Source1: https://www.gnu.org/licenses/fdl-1.3.txt

# downstream solution for coloured z*grep (#1034839)
Source100: colorzgrep.csh
Source101: colorzgrep.sh


# Fixed in upstream code.
# http://thread.gmane.org/gmane.comp.gnu.gzip.bugs/378
URL: https://www.gzip.org/
# Requires should not be added for gzip wrappers (eg. zdiff, zgrep,
# zless) of another tools, because gzip "extends" the tools by its
# wrappers much more than it "requires" them.
Requires: coreutils 
BuildRequires: texinfo, gcc, autoconf, automake, less
BuildRequires: make
Conflicts: filesystem < 3
Provides: /bin/gunzip
Provides: /bin/gzip
Provides: /bin/zcat
# Gzip contains bundled Gnulib
# exception https://fedorahosted.org/fpc/ticket/174
Provides: bundled(gnulib)

%description
The gzip package contains the popular GNU gzip data compression
program. Gzipped files have a .gz extension.

Gzip should be installed on your system, because it is a
very commonly used data compression program.

%prep
%setup -q
cp %{SOURCE1} .
autoreconf

%build
export DEFS="NO_ASM"
export CPPFLAGS="-DHAVE_LSTAT"
export CC="%{__cc}"
export CPP="%{__cpp}"
export CXX="%{__cxx}"
%ifarch s390x
export CFLAGS="$RPM_OPT_FLAGS -Dalignas=_Alignas -DDFLTCC_LEVEL_MASK=0x7e"
#use this in the next realease after gzip 1.13 export CFLAGS="$RPM_OPT_FLAGS -DDFLTCC_LEVEL_MASK=0x7e"
%configure --enable-dfltcc
%else
%configure
%endif
make
%check
make check
#make gzip.info

%install
%makeinstall

gzip -9nf ${RPM_BUILD_ROOT}%{_infodir}/gzip.info*

# we don't ship it, so let's remove it from ${RPM_BUILD_ROOT}
rm -f ${RPM_BUILD_ROOT}%{_infodir}/dir
# uncompress is a part of ncompress package
rm -f ${RPM_BUILD_ROOT}%{_bindir}/uncompress

# coloured z*grep (#1034839)
%global profiledir %{_sysconfdir}/profile.d
mkdir -p %{buildroot}%{profiledir}
install -p -m 644 %{SOURCE100} %{buildroot}%{profiledir}
install -p -m 644 %{SOURCE101} %{buildroot}%{profiledir}

%files
%doc NEWS README AUTHORS ChangeLog THANKS TODO
%license COPYING fdl-1.3.txt
%{_bindir}/*
%{_mandir}/*/*
%{_infodir}/gzip.info*
%{profiledir}/*

%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.13-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.13-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Feb 01 2024 Jakub Martisko <jamartis@redhat.com> - 1.13-1
- Rebase to gzip 1.13
- There's a bug on s390x: https://lists.gnu.org/archive/html/bug-gzip/2023-10/msg00000.html
- Revert the s390x build options in the next release
Resolves: rhbz#2232890

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.12-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jan 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.12-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Aug 02 2023 Jakub Martisko <jamartis@redhat.com> - 1.12-6
- Enbale the s390x optimizations
Resolves: rhbz#2175699

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.12-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Apr 13 2023 Lukáš Zaoral <lzaoral@redhat.com> - 1.12-4
- migrate to SPDX license format

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.12-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Apr 11 2022 Jakub Martisko <jamartis@redhat.com> - 1.12-1
- Rebase to gzip 1.12
Resolves: rhbz#2073133
Resolves: CVE-2022-1271

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Oct 21 2021 Jakub Martisko <jamartis@redhat.com> - 1.11-1
- Rebase to gzip 1.11
- Run the tests in the check section instead of the build section
Resolve: rhbz#2001025

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.10-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.10-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Aug 09 2019 Jakub Martisko <jamartis@redhat.com> - 1.10-1
- Rebase to 1.10

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.9-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Mar 26 2019 Jakub Martisko <jamartis@redhat.com> - 1.9-9
- Fix wrong skip size in gzexe
- Add new test dealing with the ^^ (needs autoreconf)
- Enable make check (needs less)
  Related: 1690825

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.9-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jul 26 2018 Jakub Martisko <jamartis@redhat.com> - 1.9-7
- Fix FTBFS bug (gnulib problems)
- more details: https://lists.gnu.org/r/bug-gnulib/2018-03/msg00000.html
  Resolves 1604303

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.9-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Mar 01 2018 Jakub Martisko <jamartis@redhat.com> - 1.9-5
- Fix previous commit (gcc was added to requires instead of buildrequires)

* Thu Mar 01 2018 Jakub Martisko <jamartis@redhat.com> - 1.9-4
- Add gcc to buildrequires

* Fri Feb 09 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.9-3
- Escape macros in %%changelog

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jan 10 2018 Jakub Martisko <jamartis@redhat.com> - 1.9-1
- rebase to v1.9

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Jul 01 2016 Petr Stodulka <pstodulk@redhat.com> - 1.8-1
- rebase to v1.8
- gzip -l no longer falsely reports a write error when writing to a pipe

* Tue Apr 05 2016 Petr Stodulka <pstodulk@redhat.com> - 1.7-1
- rebase to new upstream version 1.7
- dropped all patches (almost all issues are fixed in new upstream version,
  sometimes in different way)
  - only patch gzip-1.3.12-openbsd-owl-tmp.patch is untested - code is changed
    significantly and patch is undocumented from archaic time, so I drop it too
  Resolves: #1321560

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.6-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jul 09 2015 Petr Stodulka <pstodulk@redhat.com> - 1.6-9
- fix zless for archive with empty file (#1238298)

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 1.6-7
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Tue Aug 26 2014 Petr Stodulka <pstodulk@redhat.com> - 1.6-7
- correct changelog

* Tue Aug 26 2014 Petr Stodulka <pstodulk@redhat.com> - 1.6-6
- changed spec file - build section
  obey compiler macros %%__cc, %%__cpp, %%__cxx (#667144)
- zgrep inherits color setup from grep (#1034839)

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jul 12 2014 Tom Callaway <spot@fedoraproject.org> - 1.6-4
- fix license handling

* Fri Jun 06 2014 Petr Stodulka <pstodulk@redhat.com> - 1.6-3
- Added description of rsyncable into the manpage (#988713)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jun 11 2013 Michal Luscon <mluscon@redhat.com> - 1.6-1
- New upstream version
- Removed addsuffix.patch

* Thu Mar 14 2013 Michal Luscon <mluscon@redhat.com> - 1.5-5
- Adjust gzip-1.3.5-zforce patch

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Nov 13 2012 Daniel Drake <dsd@laptop.org> - 1.5-3
- Fix "gzip --rsyncable" functionality by removing a spurious blank line from
  the patch.

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 21 2012 Michal Luscon <mluscon@redhat.com>
- Added bundled(glib) 

* Tue Jun 19 2012 Michal Luscon <mluscon@redhat.com> 1.5-1
- New upstream version
- Removed gzip-1.3.9-stderr.patch
- Removed gzip-1.3.10-zgreppipe.patch
- Removed gzip-1.3.13-noemptysuffix.patch

* Wed Jan 25 2012 Harald Hoyer <harald@redhat.com> 1.4-6
- add filesystem guard

* Wed Jan 25 2012 Harald Hoyer <harald@redhat.com> 1.4-5
- install everything in /usr
  https://fedoraproject.org/wiki/Features/UsrMove

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Sep  6 2010 Karel Klic <kklic@redhat.com> - 1.4-2
- Removed the dependency on less (rhbz#629580)
- Removed the BuildRoot tag
- Removed the %%clean section

* Tue Mar 16 2010 Karel Klic <kklic@redhat.com> - 1.4-1
- New upstream release
- Use XZ upstream source archive
- Removed cve-2010-0001 patch as it's fixed in this release
- Removed zdiff patch as it's fixed in this release

* Mon Feb 22 2010 Karel Klic <kklic@redhat.com> - 1.3.13-3
- Added a patch to disallow -S '' parameter (noemptysuffix)

* Fri Jan 22 2010 Karel Klic <kklic@redhat.com> - 1.3.13-2
- Fixed CVE-2010-0001 (rhbz#554418)

* Tue Dec  1 2009 Karel Klic <kklic@redhat.com> - 1.3.13-1
- New upstream version
- Updated license from GPLv2 to GPLv3+
- Removed gzip-1.3.12-futimens.patch, as it is fixed in the new version
- Updated rsync patch to the new upstream version
- Updated cve-2006-4337 patch to use gzip_error instead of error

* Fri Oct  9 2009 Ivana Varekova <varekova@redhat.com> - 1.3.12-12
- change the source tag

* Tue Aug 11 2009 Ivana Varekova <varekova redhat com> - 1.3.12-11
- fix installation with --excludedocs option (#515975)

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.12-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Mar 13 2009 Ivana Varekova <varekova@redhat.com> - 1.3.12-9
- fix #484213 - zdiff shows no output

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.12-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Sep  1 2008 Ivana Varekova <varekova@redhat.com> - 1.3.12-7
- update patches

* Wed Feb 20 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.3.12-6
- Autorebuild for GCC 4.3

* Fri Jan 18 2008 Ivana Varekova <varekova@redhat.com> - 1.3.12-5
- rebuild

* Tue Aug 28 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> - 1.3.12-4
- Rebuild for selinux ppc32 issue.

* Fri Jun 15 2007 Ivana Varekova <varekova@redhat.com> - 1.3.12-3
- remove useless patches (fixed in upstream version)

* Mon Jun 11 2007 Ivana Varekova <varekova@redhat.com> - 1.3.12-2
- remove useless patches

* Mon Jun  4 2007 Ivana Varekova <varekova@redhat.com> - 1.3.12-1
- update to 1.3.12

* Mon Mar  5 2007 Ivana Varekova <varekova@redhat.com> - 1.3.11-1
- update to 1.3.11
  remove uncompress

* Tue Feb  6 2007 Ivana Varekova <varekova@redhat.com> - 1.3.10-1
- Resolves: 225878
  update to 1.3.10
  change BuildRoot

* Mon Jan 22 2007 Ivana Varekova <varekova@redhat.com> - 1.3.9-2
- Resolves: 223702
  fix non-failsafe install-info problem

* Mon Jan 15 2007 Ivana Varekova <varekova@redhat.com> - 1.3.9-1
- rebuild to 1.3.9
- spec cleanup

* Wed Nov 22 2006 Ivana Varekova <varekova@redhat.com> - 1.3.5-11
- fix too strict uncompress function

* Mon Oct 23 2006 Ivana Varekova <varekova@redhat.com> - 1.3.5-10
- fix package description (#208924)

* Sun Oct 01 2006 Jesse Keating <jkeating@redhat.com> - 1.3.5-9
- rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Wed Sep 20 2006 Ivana Varekova <varekova@redhat.com> 1.3.5-8
- fix bug 204676 (patches by Tavis Ormandy)
  - cve-2006-4334 - null dereference problem
  - cve-2006-4335 - buffer overflow problem
  - cve-2006-4336 - buffer underflow problem
  - cve-2006-4338 - infinite loop problem
  - cve-2006-4337 - buffer overflow problem

* Fri Jul 14 2006 Karsten Hopp <karsten@redhat.de> 1.3.5-7
- buildrequire texinfo, otherwise gzip.info will be empty

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.3.5-6.2.2
- rebuild

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.3.5-6.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.3.5-6.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Mon May 02 2005 Ivana Varekova <varekova@redhat.com> 1.3.5-6
- rebuilt

* Fri Apr 29 2005 Ivana Varekova <varekova@redhat.com> 1.3.5-5
- fix bug 156269 - CAN-2005-1228 directory traversal bug
 (using the patch from Ulf Harnhammar)

* Tue Apr 26 2005 Ivana Varekova <varekova@redhat.com> 1.3.5-4
- fix bug 155746 - CAN-2005-0988 Race condition in gzip (patch9)

* Wed Mar 23 2005 Tomas Mraz <tmraz@redhat.com> 1.3.5-3
- don't use the asm code again as it's slower than the gcc compiled one
- convert the .spec to UTF-8

* Tue Mar 22 2005 Tomas Mraz <tmraz@redhat.com> 1.3.5-2
- upstream 1.3.5
- dropped long ago obsolete dirinfo patch
- escape file names in zgrep (#123012)
- make stack in match.S nonexecutable

* Fri Mar 04 2005 Jiri Ryska <jryska@redhat.com>
- rebuilt

* Mon Dec 13 2004 Ivana Varekova <varekova@redhat.com>
- fix patch - remove brackets

* Mon Dec 13 2004 Ivana Varekova <varekova@redhat.com>
- fix bug #106551 problem with zmore which requires the suffix .gz in file name

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Oct 28 2003 Jeff Johnson <jbj@redhat.com> 1.3.3-11
- rebuilt.

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Jan 31 2003 Jeff Johnson <jbj@redhat.com> 1.3.3-9
- enlarge window buffer to avoid accessing beyond end-of-buffer (#78413,#83095).
- re-enable rsync ready patch.

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Fri Nov 22 2002 Jeff Johnson <jbj@redhat.com> 1.3.3-7
- workaround mis-compilation with gcc-3.2-4 on alpha for now (#78413).

* Mon Nov 18 2002 Tim Powers <timp@redhat.com>
- rebuild on all arches
- remove file from buildroot we aren't shipping

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Fri Jun 21 2002 Trond Eivind Glomsrød <teg@redhat.com> 1.3.3-4
- Fix the reading of unitialized memory problem (#66913)

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu Apr 25 2002 Trond Eivind Glomsrød <teg@redhat.com> 1.3.3-2
- Rebuild

* Wed Mar 13 2002 Trond Eivind Glomsrød <teg@redhat.com> 1.3.3-1
- 1.3.3

* Sun Mar 10 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- add rsyncable patch #58888

* Thu Feb 21 2002 Trond Eivind Glomsrød <teg@redhat.com> 1.3.2-3
- Rebuild

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Mon Nov 19 2001 Bernhard Rosenkraenzer <bero@redhat.com> 1.3.2-1
- 1.3.2: no need for autoconf 2.5x hacks anymore

* Sat Nov 17 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- update to 1.3.1:
- disable patch2

* Fri Oct 26 2001 Trond Eivind Glomsrød <teg@redhat.com> 1.3.0-16
- replace tempfile patches with improved ones solar@openwall.com
- Add less to the dependency chain - zless needs it

* Thu Aug 23 2001 Trond Eivind Glomsrød <teg@redhat.com> 1.3.0-15
- Fix typo in comment in zgrep (#52465) 
- Copyright -> License

* Tue Jun  5 2001 Trond Eivind Glomsrød <teg@redhat.com>
- Patch various uses of $$ in the bundled scripts

* Mon Jun  4 2001 Trond Eivind Glomsrød <teg@redhat.com>
- Fix the SIGPIPE patch to avoid blank lines (#43319)

* Thu Feb 08 2001 Philipp Knirsch <pknirsch@redhat.de>
- Fixed buzilla bug #26680. Wrong skip value after mktemp patch and forced
  overwrite for output file during decompression.

* Tue Jan 30 2001 Trond Eivind Glomsrød <teg@redhat.com>
- trap SIGPIPE in zgrep, so "zgrep | less" gets a happy ending
  (#24104)

* Sun Dec 10 2000 Trond Eivind Glomsrød <teg@redhat.com>
- add HAVE_LSTAT define, to avoid it doing weird things to symlinks
  instead of ignoring them as the docs say it should (#22045)

* Fri Dec 01 2000 Trond Eivind Glomsrød <teg@redhat.com>
- rebuild

* Thu Nov 09 2000 Trond Eivind Glomsrød <teg@redhat.com>
- patch all scripts so usage error messages are written to 
  stderr (#20597)

* Mon Oct 30 2000 Trond Eivind Glomsrød <teg@redhat.com>
- disable assembly, as it is faster without it (bug #19910)

* Thu Jul 13 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Tue Jun 27 2000 Trond Eivind Glomsrød <teg@redhat.com>
- rebuild

* Wed Jun 07 2000 Trond Eivind Glomsrød <teg@redhat.com>
- Use %%{_mandir}, %%{_infodir},  %%configure, %%makeinstall
  and %%{_tmppath}

* Fri May 12 2000 Trond Eivind Glomsrød <teg@redhat.com>
- Add root as default owner of the files, permits building 
  as non-root user

* Wed May 10 2000 Trond Eivind Glomsrød <teg@redhat.com>
- Build system handles stripping
- Don't do thing the system does, like creating directories
- use --bindir /bin
- Added URL
- skip unnecesarry sed step
- Include THANKS, AUTHORS, ChangeLog, TODO

* Mon Mar 20 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- 1.3
- handle RPM_OPT_FLAGS

* Tue Feb 15 2000 Cristian Gafton <gafton@redhat.com>
- handle compressed man pages even better

* Tue Feb 08 2000 Cristian Gafton <gafton@redhat.com>
- adopt patch from Paul Eggert to fix detection of the improper tables in
  inflate.c(huft_build)
- the latest released version 1.2.4a, which provides documentation updates
  only. But it lets us use small revision numbers again
- add an dirinfo entry for gzip.info so we can get rid of the ugly --entry
  args to install-info

* Mon Feb  7 2000 Bill Nottingham <notting@redhat.com>
- handle compressed manpages

* Thu Feb 03 2000 Elliot Lee <sopwith@redhat.com>
- Fix bug #7970

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 14)

* Thu Dec 17 1998 Cristian Gafton <gafton@redhat.com>
- built against gliibc 2.1

* Thu May 07 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Thu Apr 09 1998 Cristian Gafton <gafton@redhat.com>
- added /usr/bin/gzip and /usr/bin/gunzip symlinks as some programs are too
  brain dead to figure out they should be at least trying to use $PATH
- added BuildRoot

* Wed Jan 28 1998 Erik Troan <ewt@redhat.com>
- fix /tmp races

* Sun Sep 14 1997 Erik Troan <ewt@redhat.com>
- uses install-info
- applied patch for gzexe

* Mon Jun 02 1997 Erik Troan <ewt@redhat.com>
- built against glibc

* Tue Apr 22 1997 Marc Ewing <marc@redhat.com>
- (Entry added for Marc by Erik) fixed gzexe to use /bin/gzip

