# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%bcond_without selinux
# Don't run check on 32-bit arches, seems to be issues with some tests
%ifarch %{ix86} %{arm}
%bcond_with check
%else
%bcond_without check
%endif

Summary: GNU file archiving program
Name: tar
Epoch: 2
Version: 1.35
Release: 6%{?dist}
License: GPL-3.0-or-later
URL: https://www.gnu.org/software/tar/

Source0: https://ftp.gnu.org/gnu/tar/tar-%{version}.tar.xz
Source1: https://ftp.gnu.org/gnu/tar/tar-%{version}.tar.xz.sig

# Note that all patches are documented in patch files (git format-patch format)
Patch1:  tar-1.28-loneZeroWarning.patch
Patch2:  tar-1.28-vfatTruncate.patch
Patch3:  tar-1.29-wildcards.patch
Patch4:  tar-1.28-atime-rofs.patch
Patch9:  tar-1.28-document-exclude-mistakes.patch
Patch10: tar-1.33-fix-capabilities-test.patch
Patch11: tar-1.35-add-forgotten-tests-from-upstream.patch
Patch12: tar-1.35-revert-fix-savannah-bug-633567.patch

BuildRequires: autoconf
BuildRequires: automake
BuildRequires: gcc
BuildRequires: gettext
BuildRequires: libacl-devel
BuildRequires: make
BuildRequires: texinfo

%if %{with check}
# cover needs of tar's testsuite
BuildRequires: attr acl policycoreutils
%endif

%if %{with selinux}
BuildRequires: libselinux-devel
%endif
Provides: bundled(gnulib)
Provides: bundled(paxutils)
Provides: /bin/tar
Provides: /bin/gtar

%description
The GNU tar program saves many files together in one archive and can
restore individual files (or all of the files) from that archive. Tar
can also be used to add supplemental files to an archive and to update
or list files in the archive. Tar includes multivolume support,
automatic archive compression/decompression, the ability to perform
remote archives, and the ability to perform incremental and full
backups.

If you want to use tar for remote backups, you also need to install
the rmt package on the remote box.


%prep
%autosetup -p1
autoreconf -v

# Keep only entries related to the latest release.
mv ChangeLog{,~}
awk 'stop = false; /^2014-07-27/ { stop = true; exit }; { print }' \
    < ChangeLog~ > ChangeLog


%build
%configure \
    %{!?with_selinux:--without-selinux} \
    --with-lzma="xz --format=lzma" \
    DEFAULT_RMT_DIR=%{_sysconfdir} \
    RSH=/usr/bin/ssh

%make_build


%install
%make_install

ln -s tar $RPM_BUILD_ROOT%{_bindir}/gtar
rm -f $RPM_BUILD_ROOT/%{_infodir}/dir
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1
ln -s tar.1.gz $RPM_BUILD_ROOT%{_mandir}/man1/gtar.1

# XXX Nuke unpackaged files.
rm -f $RPM_BUILD_ROOT%{_sysconfdir}/rmt
rm -f $RPM_BUILD_ROOT%{_mandir}/man8/rmt.8*

%find_lang %name


%check
%if %{with check}
rm -f $RPM_BUILD_ROOT/test/testsuite
# make check TESTSUITEFLAGS='-k \!dirrem01,\!dirrem02' || (
make check || (
    # get the error log
    set +x
    find -name testsuite.log | while read line; do
        echo "=== $line ==="
        cat "$line"
        echo
    done
    false
)
%endif


%files -f %{name}.lang
%license COPYING
%doc AUTHORS README THANKS NEWS ChangeLog
%{_bindir}/tar
%{_bindir}/gtar
%{_mandir}/man1/tar.1*
%{_mandir}/man1/gtar.1*
%{_infodir}/tar.info*


%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2:1.35-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2:1.35-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2:1.35-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2:1.35-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Aug 15 2023 Pavel Raiskup <praiskup@redhat.com> - 1.35-2
- fix duplicated entries bug with --delete, rhbz#2230127

* Tue Jul 25 2023 Lukas Javorsky <ljavorsk@redhat.com> - 2:1.35-1
- Rebase to version 1.35

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2:1.34-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Mar 01 2023 Lukas Javorsky <ljavorsk@redhat.com> - 2:1.34-8
- Resolve CVE-2022-48303

* Thu Feb 02 2023 Arjun Shankar <arjun@redhat.com> - 2:1.34-7
- Port configure script to C99

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2:1.34-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Nov 03 2022 Peter Robinson <pbrobinson@fedoraproject.org> - 2:1.34-5
- Disable check on 32 bit arches as tests have issues

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2:1.34-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2:1.34-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2:1.34-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sat Feb 13 2021 Ondrej Dubaj <odubaj@redhat.com> - 1.34-1
- Rebase to version 1.34

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2:1.33-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jan 25 2021 Ondrej Dubaj <odubaj@redhat.com> - 1.33-2
- Fixed memory leak in read_header() in list.c (#1917631)

* Thu Jan 07 2021 Pavel Raiskup <praiskup@redhat.com> - 1.33-1
- new upstream release (see the packaged NEWS file)

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2:1.32-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 13 2020 Ondrej Dubaj <odubaj@redhat.com> - 2:1.32-5
- Bugfix of --sparse option in --diff mode

* Wed Feb 05 2020 Than Ngo <than@redhat.com> - 2:1.32-4
- Skip the test if genfile is unable to create

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2:1.32-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2:1.32-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Feb 25 2019 Pavel Raiskup <praiskup@redhat.com> - 1.32-1
- the latest upstream release, per release notes
  http://lists.gnu.org/archive/html/info-gnu/2019-02/msg00010.html
- admit that we bundle paxutils project

* Mon Feb 04 2019 Pavel Raiskup <praiskup@redhat.com> - 1.31-4
- fix racy compress: gzip test

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2:1.31-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jan 17 2019 Pavel Raiskup <praiskup@redhat.com> - 1.31-2
- backport fix for dirrem tests, and reenable them again

* Thu Jan 10 2019 Pavel Raiskup <praiskup@redhat.com> - 1.31-1
- the latest upstream release, per release notes
  http://lists.gnu.org/archive/html/info-gnu/2019-01/msg00001.html

* Tue Aug 07 2018 Pavel Raiskup <praiskup@redhat.com> - 1.30-6
- use %%bcond_* for selinux, use %%make_* macros

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2:1.30-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed May 23 2018 Pavel Raiskup <praiskup@redhat.com> - 1.30-4
- drop BuildRequires: rsh, we anyways use ./configure RSH=%%_bindir/ssh

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2:1.30-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Jan 06 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2:1.30-2
- Return Epoch back

* Thu Jan 04 2018 Pavel Raiskup <praiskup@redhat.com> - 1.30-1
- testsuite fixes per upstream reports

* Mon Dec 18 2017 Pavel Raiskup <praiskup@redhat.com> - 1.30-1
- rebase to latest upstream release, per release notes
  http://lists.gnu.org/archive/html/info-gnu/2017-12/msg00011.html

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2:1.29-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2:1.29-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed May 24 2017 Tomas Repik <trepik@redhat.com> - 2:1.29-5
- fix --add-file option (rhbz#1436030)

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2:1.29-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Nov 28 2016 Pavel Raiskup <praiskup@redhat.com> - 1.29-3
- revert back some docs
- fix --create to use --xattrs-include/exclude (rhbz#1341787)
- don't hang with '-x --skip-old-files --xattrs' (rhbz#1399036)

* Mon Nov  7 2016 Peter Robinson <pbrobinson@fedoraproject.org> 1.29-2
- Drop large docs, minor specs cleanups

* Tue May 17 2016 Pavel Raiskup <praiskup@redhat.com> - 1.29-1
- new upstream release 1.29 (rhbz#1336607)

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2:1.28-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jun 26 2015 Pavel Raiskup <praiskup@redhat.com> - 1.28-6
- fix --files-from and -T cooperation (rhbz#1230762)
- avoid two testsuite false alarms related to --files-from option

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:1.28-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 2:1.28-4
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:1.28-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Wed Aug  6 2014 Tom Callaway <spot@fedoraproject.org> - 2:1.28-2
- fix license handling

* Mon Jul 28 2014 Pavel Raiskup <praiskup@redhat.com> - 1.28-1
- rebase to new upstream tarball, per release notes:
  https://savannah.gnu.org/forum/forum.php?forum_id=8037

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:1.27.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon May 12 2014 Pavel Raiskup <praiskup@redhat.com> - 1.27.1-4
- enable parallel build

* Tue Apr 01 2014 Pavel Raiskup <praiskup@redhat.com> - 1.27.1-3
- document --exclude mistakes (#903666)
- fix default ACLs propagation (#1082603)
- infinite loop(s) in sparse-file handling (#1082608)
- fix listing (and --verify) for big sparse files (#916995)
- fix eternal loop in -T option (#1083066)
- don't read/write archive from/to terminal (#1083075)

* Fri Nov 29 2013 Pavel Raiskup <praiskup@redhat.com> - 1.27.1-2
- sync manual page contents with help2man output

* Mon Nov 18 2013 Pavel Raiskup <praiskup@redhat.com> - 1.27.1-1
- minor version update to 1.27.1

* Tue Oct 29 2013 Pavel Raiskup <praiskup@redhat.com> - 1.27-2
- sparse file detection based on fstat() fix (#1024095)

* Wed Oct 09 2013 Ondrej Vasik <ovasik@redhat.com> - 1.27-1
- new upstream release 1.27 (#1016288)

* Mon Sep 09 2013 Pavel Raiskup <praiskup@redhat.com> - 1.26-28
- add documenation for xattrs-like options (#996753)
- the --xattrs-include implies --xattrs now (#965969)

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:1.26-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jun 20 2013 Pavel Raiskup <praiskup@redhat.com> - 1.26-26
- the /etc/rmt seems to be the best place where to look for rmt binary (see the
  commit message in Fedora's cpio.git for more info)

* Tue Jun 04 2013 Pavel Raiskup <praiskup@redhat.com> - 2:1.26-25
- fix "symlink eating" bug (already fixed in upstream git)

* Thu May 30 2013 Pavel Raiskup <praiskup@redhat.com> - 2:1.26-24
- use /usr/bin/ssh as the default remote shell binary (#969015)
- do not verbose-print xattrs when --no-xattrs option is used
- do not override the config.{guess,sub} twice, this is already done by the
  redhat-rpm-config package (#951442)

* Tue May 28 2013 Pavel Raiskup <praiskup@redhat.com> - 2:1.26-23
- again search for 'rmt' binary in %%{_sbindir} on target host

* Tue Mar 26 2013 Pavel Raiskup <praiskup@redhat.com> - 2:1.26-22
- enable build for arm64 (#926610)
- fix the NAME part in manual page (copied from texinfo)
- silence gcc warnings (lint fixes without risk from upstream) for RPMDiff

* Tue Mar 19 2013 Pavel Raiskup <praiskup@redhat.com> - 2:1.26-21
- allow extracting single volume from multi-volume archive (#919897)
- usrmove: /bin/tar ~> /usr/bin/tar, selinux handling edit
- add possibility to pass arguments to commands called from tar (#819187)

* Fri Mar 01 2013 Pavel Raiskup <praiskup@redhat.com> - 2:1.26-19
- fix creating sparse pax archives containing files of effective
  size >8GB (#516309)
- silence rpmlint (fix bad dates in changelog based on git log dates)

* Wed Feb 20 2013 Pavel Raiskup <praiskup@redhat.com> - 2:1.26-18
- fix problems with big uids/gids and pax format (> 2^21) (#913406)

* Mon Feb 18 2013 Pavel Raiskup <praiskup@redhat.com> - 2:1.26-17
- add possibility to 'rpmbuild' without %%check phase
- make the autoreconf phase verbose
- re-create older patches (avoid offset warnings during patching)
- remove patches which we don't need now (xattrs - will be updated, sigpipe -
  test should work now, partial revert of *at() conversion was done because of
  incompatible xattr patch)
- add upstream up2date xattr patch

* Fri Feb 01 2013 Pavel Raiskup <praiskup@redhat.com> - 2:1.26-16
- make the info documentation more visible in manpage (#903666)
- sync tar.1 manpage with actual --help output (e.g. added --skip-old-files)
- add the last_help2man_run file to git repo to allow more easily find changes
  in --help in future
- make the DEFAULTS section to be more visible in man page
- verbose 'make check' only when some fail happened (append to koji build.log)

* Thu Nov 29 2012 Ondrej Vasik <ovasik@redhat.com> - 2:1.26-15
- add missing --full-time option to manpage

* Thu Oct 18 2012 Pavel Raiskup <praiskup@redhat.com> - 2:1.26-14
- fix bad behaviour of --keep-old-files and add --skip-old-files option
  (#799252)

* Wed Oct 10 2012 Pavel Raiskup <praiskup@redhat.com> 2:1.26-13
- fix badly written macro for building --without-selinux
- allow to build tar in difference CoverityScan by forcing the '.gets' patch to
  be applied even in the run without patches

* Fri Oct 05 2012 Pavel Raiskup <praiskup@redhat.com> 2:1.26-12
- repair the xattr-gnulib-prepare patch to allow build tar without SELinux
  support
- fedora-review compliance -> remove trailing white-spaces, remove macro from
  comment, remove BR of gawk;coreutils;gzip that should be covered automatically
  by minimum build environment, do not `rm -rf' buildroot at the beginning of
  install phase (needed only in EPEL), remove BuildRoot definition, remove
  defattr macro, s/define/global/
- do not use ${VAR} syntax for bash variables, use just $VAR

* Wed Aug 22 2012 Pavel Raiskup <praiskup@redhat.com> 2:1.26-11
- fix manpage to reflect #850291 related commit

* Tue Aug 21 2012 Pavel Raiskup <praiskup@redhat.com> 2:1.26-10
- prepare Gnulib for new xattrs (#850291)
- new version of RH xattrs patch (#850291)
- enable verbose mode in testsuite to allow better debugging on error

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:1.26-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jul 12 2012 Pavel Raiskup <praiskup@redhat.com> 2:1.26-8
- force the fchown() be called before xattrs_set() (#771927)

* Sat Jun 16 2012 Ondrej Vasik <ovasik@redhat.com> 2:1.26-7
- store&restore security.capability extended attributes category
  (#771927)
- fix build failure with undefined gets

* Tue May 15 2012 Ondrej Vasik <ovasik@redhat.com> 2:1.26-6
- add virtual provides for bundled(gnulib) copylib (#821790)

* Thu Apr 05 2012 Pavel Raiskup <praiskup@redhat.com> 2:1.26-5
- fix for bad cooperation of the '-C' (change directory) and '-u' (update
  package) options (#688567)

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:1.26-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Oct  2 2011 Ville Skyttä <ville.skytta@iki.fi> - 2:1.26-3
- Man page heading formatting fixes.

* Mon Sep 26 2011 Kamil Dudka <kdudka@redhat.com> 2:1.26-2
- restore basic functionality of --acl, --selinux, and --xattr (#717684)

* Sat Mar 12 2011 Ondrej Vasik <ovasik@redhat.com> 2:1.26-1
- new upstream release 1.26
* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:1.25-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jan 20 2011 Ondrej Vasik <ovasik@redhat.com> 2:1.25-5
- drop unnecessary hard dependency on info package(#671157)

* Mon Jan 03 2011 Ondrej Vasik <ovasik@redhat.com> 2:1.25-4
- mention that some compression options might not work if
  the external program is not available(#666755)

* Wed Dec 08 2010 Kamil Dudka <kdudka@redhat.com> 2:1.25-3
- correctly store long sparse file names in PAX archives (#656834)

* Tue Nov 23 2010 Ondrej Vasik <ovasik@redhat.com> 2:1.25-2
- fix issue with --one-file-system and --listed-incremental
  (#654718)

* Mon Nov 08 2010 Ondrej Vasik <ovasik@redhat.com> 2:1.25-1
- new upstream release 1.25

* Mon Oct 25 2010 Ondrej Vasik <ovasik@redhat.com> 2:1.24-1
- new upstream release 1.24, use .xz archive

* Wed Sep 29 2010 jkeating - 2:1.23-8
- Rebuilt for gcc bug 634757

* Fri Sep 24 2010 Kamil Dudka <kdudka@redhat.com> 2:1.23-7
- match non-stripped file names (#637085)

* Mon Sep 20 2010 Kamil Dudka <kdudka@redhat.com> 2:1.23-6
- fix exclusion of long file names with --xattrs (#634866)
- do not crash with --listed-incremental (#635318)

* Mon Aug 16 2010 Ondrej Vasik <ovasik@redhat.com> 2:1.23-5
- add support for security.NTACL xattrs (#621215)

* Tue Jun 01 2010 Ondrej Vasik <ovasik@redhat.com> 2:1.23-4
- recognize old-archive/portability options(#594044)

* Wed Apr 07 2010 Ondrej Vasik <ovasik@redhat.com> 2:1.23-3
- allow storing of extended attributes for fifo and block
  or character devices files(#573147)

* Mon Mar 15 2010 Ondrej Vasik <ovasik@redhat.com> 2:1.23-2
- update help2maned manpage

* Fri Mar 12 2010 Ondrej Vasik <ovasik@redhat.com> 2:1.23-1
- new upstream release 1.23, remove applied patches

* Wed Mar 10 2010 Ondrej Vasik <ovasik@redhat.com> 2:1.22-17
- CVE-2010-0624 tar, cpio: Heap-based buffer overflow
  by expanding a specially-crafted archive (#572149)
- realloc within check_exclusion_tags() caused invalid write
  (#570591)
- not closing file descriptors for excluded files/dirs with
  exlude-tag... options could cause descriptor exhaustion
  (#570591)

* Sat Feb 20 2010 Kamil Dudka <kdudka@redhat.com> 2:1.22-16
- support for "lustre.*" extended attributes (#561855)

* Thu Feb 04 2010 Ondrej Vasik <ovasik@redhat.com> 2:1.22-15
- fix segfault with corrupted metadata in code_ns_fraction
  (#531441)

* Wed Feb 03 2010 Kamil Dudka <kdudka@redhat.com> 2:1.22-14
- allow also build with SELinux support

* Mon Feb 01 2010 Ondrej Vasik <ovasik@redhat.com> 2:1.22-13
- allow build without SELinux support(#556679)

* Tue Jan 05 2010 Ondrej Vasik <ovasik@redhat.com> 2:1.22-12
- do not fail with POSIX 2008 glibc futimens() (#552320)
- temporarily disable fix for #531441, causing stack smashing
  with newer glibc(#551206)

* Tue Dec 08 2009 Ondrej Vasik <ovasik@redhat.com> 2:1.22-11
- fix segfault with corrupted metadata in code_ns_fraction
  (#531441)
- commented patches and sources

* Fri Nov 27 2009 Ondrej Vasik <ovasik@redhat.com> 2:1.22-10
- store xattrs for symlinks (#525992) - by Kamil Dudka
- update tar(1) manpage (#539787)
- fix memory leak in xheader (#518079)

* Wed Nov 18 2009 Kamil Dudka <kdudka@redhat.com> 2:1.22-9
- store SELinux context for symlinks (#525992)

* Thu Aug 27 2009 Ondrej Vasik <ovasik@redhat.com> 2:1.22-8
- provide symlink manpage for gtar

* Thu Aug 06 2009 Ondrej Vasik <ovasik@redhat.com> 2:1.22-7
- do process install-info only without --excludedocs(#515923)

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:1.22-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jul 16 2009 Ondrej Vasik <ovasik@redhat.com> 2:1.22-5
- Fix restoring of directory default acls(#511145)
- Do not patch generated autotools files

* Thu Jun 25 2009 Ondrej Vasik <ovasik@redhat.com> 2:1.22-4
- Report record size only if the archive refers to a device
  (#487760)
- Do not sigabrt with new gcc/glibc because of writing to
  struct members of gnutar header at once via strcpy

* Fri May 15 2009 Ondrej Vasik <ovasik@redhat.com> 2:1.22-3
- ignore errors from setting utime() for source file
  on read-only filesystem (#500742)

* Fri Mar 06 2009 Kamil Dudka <kdudka@redhat.com> 2:1.22-2
- improve tar-1.14-loneZeroWarning.patch (#487315)

* Mon Mar 02 2009 Ondrej Vasik <ovasik@redhat.com> 2:1.22-1
- New upstream release 1.22, removed applied patch

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:1.21-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Jan 05 2009 Ondrej Vasik <ovasik@redhat.com> 2:1.21-1
- New upstream release 1.21, removed applied patches
- add support for -I option, fix testsuite failure

* Thu Dec 11 2008 Ondrej Vasik <ovasik@redhat.com> 2:1.20-6
- add BuildRequires for rsh (#475950)

* Fri Nov 21 2008 Ondrej Vasik <ovasik@redhat.com> 2:1.20-5
- fix off-by-one errors in xattrs patch (#472355)

* Mon Nov 10 2008 Kamil Dudka <kdudka@redhat.com> 2:1.20-4
- fixed bug #465803: labels with --multi-volume (upstream patch)

* Fri Oct 10 2008 Ondrej Vasik <ovasik@redhat.com> 2:1.20-3
- Fixed wrong documentation for xattrs options (#466517)
- fixed bug with null file terminator and change dirs
  (upstream)

* Fri Aug 29 2008 Ondrej Vasik <ovasik@redhat.com> 2:1.20-2
- patch fuzz clean up

* Mon May 26 2008 Ondrej Vasik <ovasik@redhat.com> 2:1.20-1
- new upstream release 1.20 (lzma support, few new options
  and bugfixes)
- heavily modified xattrs patches(as tar-1.20 now uses automake
  1.10.1)

* Tue Feb 12 2008 Radek Brich <rbrich@redhat.com> 2:1.19-3
- do not print getfilecon/setfilecon warnings when SELinux is disabled
  or SELinux data are not available (bz#431879)
- fix for GCC 4.3

* Mon Jan 21 2008 Radek Brich <rbrich@redhat.com> 2:1.19-2
- fix errors in man page
  * fix definition of --occurrence (bz#416661, patch by Jonathan Wakely)
  * update meaning of -l: it has changed from --one-filesystem
    to --check-links (bz#426717)
- update license tag, tar 1.19 is GPLv3+

* Mon Dec 17 2007 Radek Brich <rbrich@redhat.com> 2:1.19-1
- upgrade to 1.19
- updated xattrs patch, removed 3 upstream patches

* Wed Dec 12 2007 Radek Brich <rbrich@redhat.com> 2:1.17-5
- fix (non)detection of xattrs
- move configure stuff from -xattrs patch to -xattrs-conf,
  so the original patch could be easily read
- fix -xattrs patch to work with zero length files and show
  warnings when xattrs not available (fixes by James Antill)
- possible corruption (#408621) - add warning to man page
  for now, may be actually fixed later, depending on upstream

* Tue Oct 23 2007 Radek Brich <rbrich@redhat.com> 2:1.17-4
- upstream patch for CVE-2007-4476
  (tar stack crashing in safer_name_suffix)

* Tue Aug 28 2007 Radek Brich <rbrich@redhat.com> 2:1.17-3
- gawk build dependency

* Tue Aug 28 2007 Radek Brich <rbrich@redhat.com> 2:1.17-2
- updated license tag
- fixed CVE-2007-4131 tar directory traversal vulnerability (#251921)

* Thu Jun 28 2007 Radek Brich <rbrich@redhat.com> 2:1.17-1
- new upstream version
- patch for wildcards (#206841), restoring old behavior
- patch for testsuite
- update -xattrs patch
- drop 13 obsolete patches

* Tue Feb 06 2007 Peter Vrabec <pvrabec@redhat.com> 2:1.15.1-26
- fix spec file to meet Fedora standards (#226478)

* Mon Jan 22 2007 Peter Vrabec <pvrabec@redhat.com> 2:1.15.1-25
- fix non-failsafe install-info use in scriptlets (#223718)

* Wed Jan 03 2007 Peter Vrabec <pvrabec@redhat.com> 2:1.15.1-24
- supply tar man page (#219375)

* Tue Dec 12 2006 Florian La Roche <laroche@redhat.com> 2:1.15.1-23
- fix CVE-2006-6097 GNU tar directory traversal (#216937)

* Sun Dec 10 2006 Peter Vrabec <pvrabec@redhat.com> 2:1.15.1-22
- fix some rpmlint spec file issues

* Wed Oct 25 2006 Peter Vrabec <pvrabec@redhat.com> 2:1.15.1-21
- build with dist-tag

* Mon Oct 09 2006 Peter Vrabec <pvrabec@redhat.com> 2:1.15.1-20
- another fix of tar-1.15.1-xattrs.patch from James Antill

* Wed Oct 04 2006 Peter Vrabec <pvrabec@redhat.com> 2:1.15.1-19
- another fix of tar-1.15.1-xattrs.patch from James Antill

* Sun Oct 01 2006 Peter Vrabec <pvrabec@redhat.com> 2:1.15.1-18
- fix tar-1.15.1-xattrs.patch (#208701)

* Tue Sep 19 2006 Peter Vrabec <pvrabec@redhat.com> 2:1.15.1-17
- start new epoch, downgrade to solid stable 1.15.1-16 (#206979),
- all patches are backported

* Tue Sep 19 2006 Peter Vrabec <pvrabec@redhat.com> 1.15.91-2
- apply patches, which were forgotten during upgrade

* Wed Sep 13 2006 Peter Vrabec <pvrabec@redhat.com> 1.15.91-1
- upgrade, which also fix incremental backup (#206121)

* Fri Sep 08 2006 Peter Vrabec <pvrabec@redhat.com> 1.15.90-7
- fix tar-debuginfo package (#205615)

* Thu Aug 10 2006 Peter Vrabec <pvrabec@redhat.com> 1.15.90-6
- add xattr support (#200925), patch from james.antill@redhat.com

* Mon Jul 24 2006 Peter Vrabec <pvrabec@redhat.com> 1.15.90-5
- fix incompatibilities in appending files to the end
  of an archive (#199515)

* Tue Jul 18 2006 Peter Vrabec <pvrabec@redhat.com> 1.15.90-4
- fix problem with unpacking archives in a directory for which
  one has write permission but does not own (such as /tmp) (#149686)

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.15.90-3.1
- rebuild

* Thu Jun 29 2006 Peter Vrabec <pvrabec@redhat.com> 1.15.90-3
- fix typo in tar.1 man page

* Tue Apr 25 2006 Peter Vrabec <pvrabec@redhat.com> 1.15.90-2
- exclude listed02.at from testsuite again, because it
  still fails on s390

* Tue Apr 25 2006 Peter Vrabec <pvrabec@redhat.com> 1.15.90-1
- upgrade

* Mon Apr 24 2006 Peter Vrabec <pvrabec@redhat.com> 1.15.1-16
- fix problem when options at the end of command line were
  not recognized (#188707)

* Thu Apr 13 2006 Peter Vrabec <pvrabec@redhat.com> 1.15.1-15
- fix segmentation faul introduced with hugeSparse.patch

* Wed Mar 22 2006 Peter Vrabec <pvrabec@redhat.com> 1.15.1-14
- fix problems with extracting large sparse archive members (#185460)

* Fri Feb 17 2006 Peter Vrabec <pvrabec@redhat.com> 1.15.1-13
- fix heap overlfow bug CVE-2006-0300 (#181773)

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.15.1-12.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.15.1-12.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Mon Feb 06 2006 Peter Vrabec <pvrabec@redhat.com> 1.15.1-12
- fix extracting sparse files to a filesystem like vfat,
  when ftruncate may fail to grow the size of a file.(#179507)

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Fri Nov 04 2005 Peter Vrabec <pvrabec@redhat.com> 1.15.1-11
- correctly pad archive members that shrunk during archiving (#172373)

* Tue Sep 06 2005 Peter Vrabec <pvrabec@redhat.com> 1.15.1-10
- provide man page (#163709, #54243, #56041)

* Mon Aug 15 2005 Peter Vrabec <pvrabec@redhat.com> 1.15.1-9
- silence newer option (#164902)

* Wed Jul 27 2005 Peter Vrabec <pvrabec@redhat.com> 1.15.1-8
- A file is dumpable if it is sparse and both --sparse
  and --totals are specified (#154882)

* Tue Jul 26 2005 Peter Vrabec <pvrabec@redhat.com> 1.15.1-7
- exclude listed02.at from testsuite

* Fri Jul 22 2005 Peter Vrabec <pvrabec@redhat.com> 1.15.1-6
- remove tar-1.14-err.patch, not needed (158743)

* Fri Apr 15 2005 Peter Vrabec <pvrabec@redhat.com> 1.15.1-5
- extract sparse files even if the output fd is not seekable.(#154882)
- (sparse_scan_file): Bugfix. offset had incorrect type.

* Mon Mar 14 2005 Peter Vrabec <pvrabec@redhat.com>
- gcc4 fix (#150993) 1.15.1-4

* Mon Jan 31 2005 Peter Vrabec <pvrabec@redhat.com>
- rebuild 1.15.1-3

* Mon Jan 17 2005 Peter Vrabec <pvrabec@redhat.com>
- fix tests/testsuite

* Fri Jan 07 2005 Peter Vrabec <pvrabec@redhat.com>
- upgrade to 1.15.1

* Mon Oct 11 2004 Peter Vrabec <pvrabec@redhat.com>
- patch to stop issuing lone zero block warnings
- rebuilt

* Mon Oct 11 2004 Peter Vrabec <pvrabec@redhat.com>
- URL added to spec file
- spec file clean up

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Jun  7 2004 Jeff Johnson <jbj@jbj.org> 1.14-1
- upgrade to 1.14.

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Jun 17 2003 Jeff Johnson <jbj@redhat.com> 1.13.25-13
- rebuilt because of crt breakage on ppc64.
- dump automake15 requirement.

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Fri Nov 29 2002 Tim Powers <timp@redhat.com> 1.13.25-10
- fix broken buildrquires on autoconf253

* Thu Nov  7 2002 Jeff Johnson <jbj@redhat.com> 1.13.25-9
- rebuild from CVS.

* Fri Aug 23 2002 Phil Knirsch <pknirsch@redhat.com> 1.13.25-8
- Included security patch from errata release.

* Mon Jul  1 2002 Bernhard Rosenkraenzer <bero@redhat.com> 1.13.25-7
- Fix argv NULL termination (#64869)

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Tue Apr  9 2002 Bernhard Rosenkraenzer <bero@redhat.com> 1.13.25-4
- Fix build with autoconf253 (LIBOBJ change; autoconf252 worked)

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Tue Oct 23 2001 Bernhard Rosenkraenzer <bero@redhat.com> 1.13.25-2
- Don't include hardlinks to sockets in a tar file (#54827)

* Thu Sep 27 2001 Bernhard Rosenkraenzer <bero@redhat.com> 1.13.25-1
- 1.13.25

* Tue Sep 18 2001 Bernhard Rosenkraenzer <bero@redhat.com> 1.13.22-1
- Update to 1.13.22, adapt patches

* Mon Aug 27 2001 Bernhard Rosenkraenzer <bero@redhat.com> 1.13.19-6
- Fix #52084

* Thu May 17 2001 Bernhard Rosenkraenzer <bero@redhat.com> 1.13.19-5
- Fix build with current autoconf (stricter checking on AC_DEFINE)
- Fix segfault when tarring directories without having read permissions
  (#40802)

* Tue Mar  6 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- Don't depend on librt.

* Fri Feb 23 2001 Trond Eivind Glomsröd <teg@redhat.com>
- langify

* Thu Feb 22 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- Fix up the man page (#28915)

* Wed Feb 21 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- 1.3.19, nukes -I and fixes up -N
- Add -I back in as an alias to -j with a nice loud warning

* Mon Oct 30 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- 1.3.18
- Update man page to reflect changes

* Thu Oct  5 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Fix the "ignore failed read" option (Bug #8330)

* Mon Sep 25 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- fix hang on tar tvzf - <something.tar.gz, introduced by
  exit code fix (Bug #15448), Patch from Tim Waugh <twaugh@redhat.com>

* Fri Aug 18 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- really fix exit code (Bug #15448)

* Mon Aug  7 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- fix exit code (Bug #15448), patch from Tim Waugh <twaugh@redhat.com>

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Mon Jun 19 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- FHSify

* Fri Apr 28 2000 Bill Nottingham <notting@redhat.com>
- fix for ia64

* Wed Feb  9 2000 Bernhard Rosenkränzer <bero@redhat.com>
- Fix the exclude bug (#9201)

* Wed Feb 02 2000 Cristian Gafton <gafton@redhat.com>
- man pages are compressed
- fix description
- fix fnmatch build problems

* Sun Jan  9 2000 Bernhard Rosenkränzer <bero@redhat.com>
- 1.13.17
- remove dotbug patch (fixed in base)
- update download URL

* Fri Jan  7 2000 Bernhard Rosenkränzer <bero@redhat.com>
- Fix a severe bug (tar xf any_package_containing_. would delete the
  current directory)

* Wed Jan  5 2000 Bernhard Rosenkränzer <bero@redhat.com>
- 1.3.16
- unset LINGUAS before running configure

* Tue Nov  9 1999 Bernhard Rosenkränzer <bero@redhat.com>
- 1.13.14
- Update man page to know about -I / --bzip
- Remove dependancy on rmt - tar can be used for anything local
  without it.

* Fri Aug 27 1999 Preston Brown <pbrown@redhat.com>
- upgrade to 1.13.11.

* Wed Aug 18 1999 Jeff Johnson <jbj@redhat.com>
- update to 1.13.9.

* Thu Aug 12 1999 Jeff Johnson <jbj@redhat.com>
- update to 1.13.6.
- support -y --bzip2 options for bzip2 compression (#2415).

* Fri Jul 23 1999 Jeff Johnson <jbj@redhat.com>
- update to 1.13.5.

* Tue Jul 13 1999 Bill Nottingham <notting@redhat.com>
- update to 1.13

* Sat Jun 26 1999 Jeff Johnson <jbj@redhat.com>
- update to 1.12.64014.
- pipe patch corrected for remote tars now merged in.

* Sun Jun 20 1999 Jeff Johnson <jbj@redhat.com>
- update to tar-1.12.64013.
- subtract (and reopen #2415) bzip2 support using -y.
- move gtar to /bin.

* Tue Jun 15 1999 Jeff Johnson <jbj@redhat.com>
- upgrade to tar-1.12.64011 to
-   add bzip2 support (#2415)
-   fix filename bug (#3479)

* Mon Mar 29 1999 Jeff Johnson <jbj@redhat.com>
- fix suspended tar with compression over pipe produces error (#390).

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com>
- auto rebuild in the new build environment (release 8)

* Mon Mar 08 1999 Michael Maher <mike@redhat.com>
- added patch for bad name cache.
- FIXES BUG 320

* Wed Feb 24 1999 Preston Brown <pbrown@redhat.com>
- Injected new description and group.

* Fri Dec 18 1998 Preston Brown <pbrown@redhat.com>
- bumped spec number for initial rh 6.0 build

* Tue Aug  4 1998 Jeff Johnson <jbj@redhat.com>
- add /usr/bin/gtar symlink (change #421)

* Tue Jul 14 1998 Jeff Johnson <jbj@redhat.com>
- Fiddle bindir/libexecdir to get RH install correct.
- Don't include /sbin/rmt -- use the rmt from dump.
- Turn on nls.

* Mon Apr 27 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Thu Oct 16 1997 Donnie Barnes <djb@redhat.com>
- updated from 1.11.8 to 1.12
- various spec file cleanups
- /sbin/install-info support

* Thu Jun 19 1997 Erik Troan <ewt@redhat.com>
- built against glibc

* Thu May 29 1997 Michael Fulbright <msf@redhat.com>
- Fixed to include rmt
