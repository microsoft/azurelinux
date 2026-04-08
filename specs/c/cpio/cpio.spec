# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Summary: A GNU archiving program
Name: cpio
Version: 2.15
Release: 6%{?dist}
License: GPL-3.0-or-later
URL: https://www.gnu.org/software/cpio/
Source0: https://ftp.gnu.org/gnu/cpio/cpio-%{version}.tar.bz2

# help2man generated manual page distributed only in RHEL/Fedora
Source1: cpio.1

Source2: https://ftp.gnu.org/gnu/cpio/cpio-%{version}.tar.bz2.sig
# https://savannah.gnu.org/projects/cpio/ lists one maintainer, gray
# and their GPG key is https://savannah.gnu.org/people/viewgpg.php?user_id=311
Source3: gray-key.gpg

# We use SVR4 portable format as default.
Patch1: cpio-2.14-rh.patch

# fix warn_if_file_changed() and set exit code to 1 when cpio fails to store
# file > 4GB (#183224)
# http://lists.gnu.org/archive/html/bug-cpio/2006-11/msg00000.html
Patch2: cpio-2.14-exitCode.patch

# Support major/minor device numbers over 127 (bz#450109)
# http://lists.gnu.org/archive/html/bug-cpio/2008-07/msg00000.html
Patch3: cpio-2.14-dev_number.patch

# Define default remote shell as /usr/bin/ssh (#452904)
Patch4: cpio-2.9.90-defaultremoteshell.patch

# Fix segfault with nonexisting file with patternnames (#567022)
# http://savannah.gnu.org/bugs/index.php?28954
# We have slightly different solution than upstream.
Patch5: cpio-2.14-patternnamesigsegv.patch

# Fix bad file name splitting while creating ustar archive (#866467)
# (fix backported from tar's source)
Patch7: cpio-2.10-longnames-split.patch

# Cpio does Sum32 checksum, not CRC (downstream)
Patch8: cpio-2.11-crc-fips-nit.patch

Provides: bundled(gnulib)
Provides: bundled(paxutils)
Provides: /bin/cpio
BuildRequires: gcc
BuildRequires: texinfo, autoconf, automake, gettext, gettext-devel, rmt
BuildRequires: make
BuildRequires: gnupg2

%description
GNU cpio copies files into or out of a cpio or tar archive.  Archives
are files which contain a collection of other files plus information
about them, such as their file name, owner, timestamps, and access
permissions.  The archive can be another file on the disk, a magnetic
tape, or a pipe.  GNU cpio supports the following archive formats:  binary,
old ASCII, new ASCII, crc, HPUX binary, HPUX old ASCII, old tar and POSIX.1
tar.  By default, cpio creates binary format archives, so that they are
compatible with older cpio programs.  When it is extracting files from
archives, cpio automatically recognizes which kind of archive it is reading
and can read archives created on machines with a different byte-order.

Install cpio if you need a program to manage file archives.


%prep
%{gpgverify} --keyring='%{SOURCE3}' --signature='%{SOURCE2}' --data='%{SOURCE0}'
%autosetup -p1


%build
autoreconf -fi
# https://gcc.gnu.org/bugzilla/show_bug.cgi?id=118112
CFLAGS="$RPM_OPT_FLAGS -std=gnu17"
export CFLAGS="$RPM_OPT_FLAGS -D_GNU_SOURCE -D_FILE_OFFSET_BITS=64 -D_LARGEFILE64_SOURCE -pedantic -fno-strict-aliasing -Wall $CFLAGS"
%configure --with-rmt="%{_sysconfdir}/rmt"
%make_build
(cd po && make update-gmo)


%install
%make_install

rm -f $RPM_BUILD_ROOT%{_libexecdir}/rmt
rm -f $RPM_BUILD_ROOT%{_infodir}/dir
rm -f $RPM_BUILD_ROOT%{_mandir}/man1/*.1*
install -c -p -m 0644 %{SOURCE1} ${RPM_BUILD_ROOT}%{_mandir}/man1

%find_lang %{name}

%check
rm -f ${RPM_BUILD_ROOT}/test/testsuite
make check || {
    echo "### TESTSUITE.LOG ###"
    cat tests/testsuite.log
    exit 1
}


%files -f %{name}.lang
%doc AUTHORS ChangeLog NEWS README THANKS TODO
%license COPYING
%{_bindir}/*
%{_mandir}/man*/*
%{_infodir}/*.info*

%changelog
* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.15-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jun 06 2025 Lukáš Zaoral <lzaoral@redhat.com> - 2.15-5
- exit with 1 when storing excessively large files in bin format
  - fixes a regression introduced after the rebase to 2.13

* Fri Jan 24 2025 Than Ngo <than@redhat.com> - 2.15-4
- Fixed rhbz#2340003 - cpio: FTBFS in Fedora rawhide/f42

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.15-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jan 24 2024 Lukas Javorsky <ljavorsk@redhat.com> - 2.15-1
- Rebase to version 2.15

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.14-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.14-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Nov 15 2023 Florian Weimer <fweimer@redhat.com> - 2.14-5
- Backport upstream patch for C99 compatibility issue

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.14-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sun Jul 16 2023 Stewart Smith <trawets@amazon.com> - 2.14-3
- gpg verify source tarball

* Mon May 29 2023 Lukas Javorsky <ljavorsk@redhat.com> - 2.14-2
- Release bump

* Tue May 16 2023 Lukas Javorsky <ljavorsk@redhat.com> - 2.14-1
- Rebase to version 2.14
- Resolves #1188590 CVE-2015-1197

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.13-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.13-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jan 19 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.13-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.13-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Feb 18 2021 Ondrej Dubaj <odubaj@redhat.com> - 2.13-10
- Properly drop priviledges for remote command

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.13-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.13-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 13 2020 Tom Stellard <tstellar@redhat.com> - 2.13-7
- Use make macros
- https://fedoraproject.org/wiki/Changes/UseMakeBuildInstallMacro

* Mon Jun 15 2020 Ondrej Dubaj <odubaj@redhat.com> - 2.13-6
- Extract: retain times for symlinks (#1486364)

* Tue Apr 07 2020 Ondrej Dubaj <odubaj@redhat.com> - 2.13-5.1
- Release bump due to testing of gating

* Wed Feb 05 2020 Petr Kubat <pkubat@redhat.com> - 2.13-4
- Revert fix for CVE-2015-1197 as it causes shutdown issues (#1797163)

* Thu Jan 30 2020 Than Ngo <than@redhat.com> - 2.13-3
- Fix multiple definition of program_name

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Nov 06 2019 Pavel Raiskup <praiskup@redhat.com> - 2.13-1
- new upstream release, per release notes
  https://lists.gnu.org/archive/html/bug-cpio/2019-11/msg00000.html

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.12-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Feb 19 2019 Pavel Raiskup <praiskup@redhat.com> - 2.12-11
- admit that we bundle paxutils project

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.12-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.12-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Apr 11 2018 Pavel Raiskup <praiskup@redhat.com> - 2.12-8
- spring spec cleanup

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.12-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.12-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.12-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.12-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.12-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Sep 14 2015 Pavel Raiskup <praiskup@redhat.com> - 2.12-2
- (re)generate manual page for new options

* Mon Sep 14 2015 Pavel Raiskup <praiskup@redhat.com> - 2.12-1
- rebase, per release notes
  http://lists.gnu.org/archive/html/bug-cpio/2015-09/msg00004.html

* Mon Jul 06 2015 Ondrej Vasik <ovasik@redhat.com> - 2.11-36
- in 2015, file name in CVE-2014-9112 shows in a bit different timestamp
  format (fix FTBFS, #1239416)

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.11-35
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 2.11-34
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Wed Dec 03 2014 Pavel Raiskup <praiskup@redhat.com> - 2.11-33
- the stored archive in testsuite has little endian headers, expect also
  'reversed byte-order' warning on big-endian

* Wed Dec 03 2014 Pavel Raiskup <praiskup@redhat.com> - 2.11-32
- adjust the testsuite fix for CVE-2014-9112 (#1167573)
- put the testsuite.log to standard output if make check fails

* Tue Dec 02 2014 Pavel Raiskup <praiskup@redhat.com> - 2.11-31
- fix for CVE-2014-9112 (#1167573)

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.11-30
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Jul 11 2014 Tom Callaway <spot@fedoraproject.org> - 2.11-29
- fix license handling

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.11-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat May 24 2014 Pavel Raiskup <praiskup@redhat.com> - 2.11-27
- better fix for bad read() error checking (#996150)

* Mon Apr 07 2014 Pavel Raiskup <praiskup@redhat.com> - 2.11-26
- fix manual page to warn users about inode truncation (#952313)
- fix for RU translation (#1075510)

* Tue Nov 12 2013 Pavel Raiskup <praiskup@redhat.com> - 2.11-25
- fix build for ppc64le (#1029540)

* Mon Sep 30 2013 Pavel Raiskup <praiskup@redhat.com> - 2.11-24
- properly trim "crc" checksum to 32 bits (#1001965)
- remove unneeded patch for config.gues/config.sub (#951442)
- allow treat read() errors (#996150)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.11-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Mar 27 2013 Pavel Raiskup <praiskup@redhat.com> - 2.11-20
- fix another bogus date in changelog
- update config.guess/config.sub for aarm64 build (#925189)
- run autoreconf instead of autoheader

* Fri Mar 15 2013 Pavel Raiskup <praiskup@redhat.com> - 2.11-19
- revert the fix for memory leak (at least for now) #921725

* Tue Mar 12 2013 Pavel Raiskup <praiskup@redhat.com> - 2.11-18
- explicitly provide /bin/cpio for packages that are dependant on this file

* Mon Mar 11 2013 Pavel Raiskup <praiskup@redhat.com> - 2.11-17
- fix small memory leak in copyin.c (#919454)
- remove %%defattr and install 'cpio' to real %%{_bindir}
- CovScan: add %%{?_rawbuild}

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.11-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Nov 05 2012 Pavel Raiskup <praiskup@redhat.com> - 2.11-15
- disable the temporary O_SYNC fix (glibc is fixed - #872366)

* Fri Nov 02 2012 Pavel Raiskup <praiskup@redhat.com> - 2.11-14
- fix bad changelog entries
- allow to build in Fedora Rawhide (temporarily because of #872336) (the value
  is guessed from from /usr/include/asm-generic/fcntl.h)

* Mon Oct 22 2012 Pavel Raiskup <praiskup@redhat.com> 2.11-13
- move RH-only manual page cpio.1 from look-aside cache into dist-git repository

* Thu Oct 18 2012 Pavel Raiskup <praiskup@redhat.com> 2.11-12
- fix for bad file name splitting while creating ustar archive (#866467)

* Wed Aug 29 2012 Ondrej Vasik <ovasik@redhat.com> 2.11-11
- add missing options to manpage (#852765)

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.11-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 04 2012 Ondrej Vasik <ovasik@redhat.com> 2.11-9
- fix build failure in rawhide build system (gets undefined)

* Wed May 30 2012 Ondrej Vasik <ovasik@redhat.com> 2.11-8
- drop unnecessary patches: cpio-2.9-dir_perm.patch and
  cpio-2.9-sys_umask.patch - reported by M.Castellini

* Tue May 15 2012 Ondrej Vasik <ovasik@redhat.com> 2.11-7
- add virtual provides for bundled(gnulib) copylib (#821749)

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.11-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Oct 14 2011 Ondrej Vasik <ovasik@redhat.com> 2.11-5
- update manpage to reflect new option, polish the style (#746209)

* Mon Mar 07 2011 Ondrej Vasik <ovasik@redhat.com> 2.11-4
- fix several typos and manpage syntax(Ville Skyttä, #682470)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon May 31 2010 Ondrej Vasik <ovasik@redhat.com> 2.11-2
- built with fno-strict-aliasing(#596153)

* Thu Mar 11 2010 Ondrej Vasik <ovasik@redhat.com> 2.11-1
- new upstream release 2.11
- removed applied patches, run test suite

* Wed Mar 10 2010 Ondrej Vasik <ovasik@redhat.com> 2.10-6
- CVE-2010-0624 fix heap-based buffer overflow by expanding
  a specially-crafted archive(#572150)
- comment patches

* Thu Feb 25 2010 Ondrej Vasik <ovasik@redhat.com> 2.10-5
- remove redundant setLocale patch
- fix segfault with nonexisting file with patternnames
  (#567022)

* Wed Jan 06 2010 Ondrej Vasik <ovasik@redhat.com> 2.10-4
- do not fail with new POSIX 2008 utimens() glibc call
  (#552320)

* Thu Aug 06 2009 Ondrej Vasik <ovasik@redhat.com> 2.10-3
- do process install-info only without --excludedocs(#515924)

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jun 22 2009 Ondrej Vasik <ovasik@redhat.com> 2.10-1
- new upstream release 2.10

* Mon Mar  9 2009 Ondrej Vasik <ovasik@redhat.com> 2.9.90-5
- define default remote shell as /usr/bin/ssh(#452904)
- use /etc/rmt as default rmt command

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.9.90-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 11 2009 Ondrej Vasik <ovasik@redhat.com> 2.9.90-3
- make -d honor system umask(#484997)

* Fri Jul 18 2008 Kamil Dudka <kdudka@redhat.com> 2.9.90-2
- Support major/minor device numbers over 127 (bz#450109)

* Tue Jun 03 2008 Ondrej Vasik <ovasik@redhat.com> 2.9.90-1
- new upstream alpha version 2.9.90 + removed applied patches

* Mon Mar 03 2008 Radek Brich <rbrich@redhat.com> 2.9-7
- fix -dir_perm patch to restore permissions correctly even
  in passthrough mode -- revert affected code to cpio 2.8 state
  (bz#430835)

* Thu Feb 14 2008 Radek Brich <rbrich@redhat.com> 2.9-6
- when extracting archive created with 'find -depth',
  restore the permissions of directories properly (bz#430835)
- fix for GCC 4.3

* Thu Nov 01 2007 Radek Brich <rbrich@redhat.com> 2.9-5
- upstream patch for CVE-2007-4476 (stack crashing in safer_name_suffix)

* Tue Sep 04 2007 Radek Brich <rbrich@redhat.com> 2.9-4
- Updated license tag

* Wed Aug 29 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> - 2.9-3
- Rebuild for selinux ppc32 issue.

* Thu Jul 19 2007 Radek Brich <rbrich@redhat.com> 2.9-1.1
- fix spec, rebuild

* Thu Jul 19 2007 Radek Brich <rbrich@redhat.com> 2.9-1
- update to 2.9, GPLv3

* Tue Feb 20 2007 Peter Vrabec <pvrabec@redhat.com> 2.6-27
- fix typo in changelog

* Thu Feb 08 2007 Ruben Kerkhof <ruben@rubenkerkhof.com> 2.6-26
- Preserve timestamps when installing files

* Thu Feb 08 2007 Peter Vrabec <pvrabec@redhat.com> 2.6-25
- set cpio bindir properly

* Wed Feb 07 2007 Peter Vrabec <pvrabec@redhat.com> 2.6-24
- fix spec file to meet Fedora standards (#225656) 

* Mon Jan 22 2007 Peter Vrabec <pvrabec@redhat.com> 2.6-23
- fix non-failsafe install-info use in scriptlets (#223682)

* Sun Dec 10 2006 Peter Vrabec <pvrabec@redhat.com> 2.6-22
- fix rpmlint issue in spec file

* Tue Dec 05 2006 Peter Vrabec <pvrabec@redhat.com> 2.6-21
- fix setlocale (#200478)

* Sat Nov 25 2006 Peter Vrabec <pvrabec@redhat.com> 2.6-20
- cpio man page provided by RedHat

* Tue Jul 18 2006 Peter Vrabec <pvrabec@redhat.com> 2.6-19
- fix cpio --help output (#197597)

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 2.6-18.1
- rebuild

* Sat Jun 10 2006 Peter Vrabec <pvrabec@redhat.com> 2.6-18
- autoconf was added to BuildRequires, because autoheader is 
  used in prep phase (#194737)

* Tue Mar 28 2006 Peter Vrabec <pvrabec@redhat.com> 2.6-17
- rebuild

* Sat Mar 25 2006 Peter Vrabec <pvrabec@redhat.com> 2.6-15
- fix (#186339) on ppc and s390

* Thu Mar 23 2006 Peter Vrabec <pvrabec@redhat.com> 2.6-14
- init struct  file_hdr (#186339)

* Wed Mar 15 2006 Peter Vrabec <pvrabec@redhat.com> 2.6-13
- merge toAsciiError.patch with writeOutHeaderBufferOverflow.patch
- merge largeFileGrew.patch with lfs.patch
- fix large file support, cpio is able to store files<8GB 
  in 'old ascii' format (-H odc option)
- adjust warnings.patch

* Tue Mar 14 2006 Peter Vrabec <pvrabec@redhat.com> 2.6-12
- fix warn_if_file_changed() and set exit code to #1 when 
  cpio fails to store file > 4GB (#183224)

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 2.6-11.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 2.6-11.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Wed Nov 23 2005 Peter Vrabec <pvrabec@redhat.com> 2.6-11
- fix previous patch(writeOutHeaderBufferOverflow)

* Wed Nov 23 2005 Peter Vrabec <pvrabec@redhat.com> 2.6-10
- write_out_header rewritten to fix buffer overflow(#172669)

* Mon Oct 31 2005 Peter Vrabec <pvrabec@redhat.com> 2.6-9
- fix checksum error on 64-bit machines (#171649)

* Fri Jul 01 2005 Peter Vrabec <pvrabec@redhat.com> 2.6-8
- fix large file support, archive >4GiB, archive members <4GiB (#160056)
- fix race condition holes, use mode 0700 for dir creation

* Tue May 17 2005 Peter Vrabec <pvrabec@redhat.com> 2.6-7
- fix #156314 (CAN-2005-1229) cpio directory traversal issue
- fix some gcc warnings

* Mon Apr 25 2005 Peter Vrabec <pvrabec@redhat.com> 2.6-6
- fix race condition (#155749)
- use find_lang macro

* Thu Mar 17 2005 Peter Vrabec <pvrabec@redhat.com>
- rebuild 2.6-5

* Mon Jan 24 2005 Peter Vrabec <pvrabec@redhat.com>
- insecure file creation (#145721)

* Mon Jan 17 2005 Peter Vrabec <pvrabec@redhat.com>
- fix symlinks pack (#145225)

* Fri Jan 14 2005 Peter Vrabec <pvrabec@redhat.com>
- new fixed version of lfs patch (#144688)

* Thu Jan 13 2005 Peter Vrabec <pvrabec@redhat.com>
- upgrade to cpio-2.6

* Tue Nov 09 2004 Peter Vrabec <pvrabec@redhat.com>
- fixed "cpio -oH ustar (or tar) saves bad mtime date after Jan 10 2004" (#114580)

* Mon Nov 01 2004 Peter Vrabec <pvrabec@redhat.com>
- support large files > 2GB (#105617)

* Thu Oct 21 2004 Peter Vrabec <pvrabec@redhat.com>
- fix dependencies in spec

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Sep 23 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- do not link against -lnsl

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 14 2003 Jeff Johnson <jbj@redhat.com> 2.5-3
- setlocale for i18n compliance (#79136).

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Mon Nov 18 2002 Jeff Johnson <jbj@redhat.com> 2.5-1
- update 2.5, restack and consolidate patches.
- don't apply (but include for now) freebsd and #56346 patches.
- add url (#54598).

* Thu Nov  7 2002 Jeff Johnson <jbj@redhat.com> 2.4.2-30
- rebuild from CVS.

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu Nov 22 2001 Bernhard Rosenkraenzer <bero@redhat.com> 2.4.2-25
- Fix up extraction of multiply linked files when the first link is
  excluded (Bug #56346)

* Mon Oct  1 2001 Bernhard Rosenkraenzer <bero@redhat.com> 2.4.2-24
- Merge and adapt patches from FreeBSD, this should fix FIFO handling

* Tue Jun 26 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- Add and adapt Debian patch (pl36), fixes #45285 and a couple of other issues

* Sun Jun 24 2001 Elliot Lee <sopwith@redhat.com>
- Bump release + rebuild.

* Tue Aug  8 2000 Jeff Johnson <jbj@redhat.com>
- update man page with decription of -c behavior (#10581).

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Thu Jun 29 2000 Preston Brown <pbrown@redhat.com>
- patch from HJ Lu for better error codes upon exit

* Mon Jun  5 2000 Jeff Johnson <jbj@redhat.com>
- FHS packaging.

* Wed Feb  9 2000 Jeff Johnson <jbj@redhat.com>
- missing defattr.

* Mon Feb  7 2000 Bill Nottingham <notting@redhat.com>
- handle compressed manpages

* Fri Dec 17 1999 Jeff Johnson <jbj@redhat.com>
- revert the stdout patch (#3358), restoring original GNU cpio behavior
  (#6376, #7538), the patch was dumb.

* Tue Aug 31 1999 Jeff Johnson <jbj@redhat.com>
- fix infinite loop unpacking empty files with hard links (#4208).
- stdout should contain progress information (#3358).

* Sun Mar 21 1999 Crstian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 12)

* Sat Dec  5 1998 Jeff Johnson <jbj@redhat.com>
- longlong dev wrong with "-o -H odc" headers (formerly "-oc").

* Thu Dec 03 1998 Cristian Gafton <gafton@redhat.com>
- patch to compile on glibc 2.1, where strdup is a macro

* Tue Jul 14 1998 Jeff Johnson <jbj@redhat.com>
- Fiddle bindir/libexecdir to get RH install correct.
- Don't include /sbin/rmt -- use the rmt from dump package.
- Don't include /bin/mt -- use the mt from mt-st package.
- Add prereq's

* Tue Jun 30 1998 Jeff Johnson <jbj@redhat.com>
- fix '-c' to duplicate svr4 behavior (problem #438)
- install support programs & info pages

* Mon Apr 27 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Fri Oct 17 1997 Donnie Barnes <djb@redhat.com>
- added BuildRoot
- removed "(used by RPM)" comment in Summary

* Thu Jun 19 1997 Erik Troan <ewt@redhat.com>
- built against glibc
- no longer statically linked as RPM doesn't use cpio for unpacking packages
