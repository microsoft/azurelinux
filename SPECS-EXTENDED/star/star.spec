Vendor:         Microsoft Corporation
Distribution:   Azure Linux
%global ALTERNATIVES %{_sbindir}/alternatives

Summary:  An archiving tool with ACL support
Name: star
Version: 1.6
Release: 4%{?dist}
License: CDDL
URL: https://freecode.com/projects/star
Source: https://downloads.sourceforge.net/s-tar/%{name}-%{version}.tar.bz2


# Fix broken all.mk
Patch1: star-1.6-star-mk.patch

# # Prevent buffer overflow for filenames with length of 100 characters (#556664)
Patch2: star-1.5.2-bufferoverflow.patch

# # Fix some invalid manpage references (#624612)
Patch3: star-1.6-manpagereferences.patch

# Allow rmt to access all files.
# ~> downstream
# ~> #968980
Patch4: star-1.5.2-rmt-rh-access.patch

# Use ssh rather than rsh by default
# ~> downstream
# ~> related to #968980
Patch5: star-1.5.2-use-ssh-by-default.patch

BuildRequires: libattr-devel libacl-devel libtool libselinux-devel
BuildRequires: e2fsprogs-devel

%description
Star saves many files together into a single tape or disk archive,
and can restore individual files from the archive. Star supports ACL.

%package -n     spax
Summary:        Portable archive exchange
Requires(post):  %{ALTERNATIVES}
Requires(preun): %{ALTERNATIVES}


%description -n spax
The pax utility shall read and write archives, write lists of the members of
archive files and copy directory hierarchies as is defined in IEEE Std 1003.1.

%package -n     scpio
Summary:        Copy file archives in and out (LEGACY)

%description -n scpio
The scpio utility, depending on the options used: copies files to an archive
file, extracts files from an archive file, lists files from an archive file or
copies files from one directory tree to another.

%package -n     rmt
Summary: Provides certain programs with access to remote tape devices
# we need to be greater than the version from 'dump' package

%description -n rmt
The rmt utility provides remote access to tape devices for programs
like dump (a filesystem backup program), restore (a program for
restoring files from a backup), and tar (an archiving program).

# "desired" alternative constants
%global ALT_NAME                pax
%global ALT_LINK                %{_bindir}/pax
%global ALT_SL1_NAME            pax-man
%global ALT_SL1_LINK            %{_mandir}/man1/pax.1.gz

# "local" alternative constants
%global ALT_PATH                %{_bindir}/spax
%global ALT_SL1_PATH            %{_mandir}/man1/spax.1.gz

%prep
%autosetup -p1

# disable single "fat" binary
cp -a star/all.mk star/Makefile

star_recode()
{
    for i in $@; do
        iconv -f iso_8859-1 -t utf-8 $i > .tmp_file
        mv .tmp_file $i
    done
}

star_recode AN-1.5 AN-1.5.2 star/star.4

for PLAT in %{arm} %{power64} aarch64 %{mips} x86_64 s390 s390x sh3 sh4 sh4a sparcv9; do
    for AFILE in gcc cc; do
            [ ! -e RULES/${PLAT}-linux-${AFILE}.rul ] \
            && ln -s i586-linux-${AFILE}.rul RULES/${PLAT}-linux-${AFILE}.rul
    done
done

%build
# This is config/work-around for atypical build system.  Variables used are
# docummented makefiles.5.  GMAKE_NOWARN silences irritating warnings in
# GNU/Linux ecosystem.
%global make_flags GMAKE_NOWARN=true                                    \\\
    RUNPATH=                                                            \\\
    LDPATH=                                                             \\\
    PARCH=%{_target_cpu}                                                \\\
    K_ARCH=%{_target_cpu}                                               \\\
    INS_BASE=$RPM_BUILD_ROOT%{_prefix}                                  \\\
    INS_RBASE=$RPM_BUILD_ROOT                                           \\\
    INSTALL='sh $(SRCROOT)/conf/install-sh -c -m $(INSMODEINS)'         \\\
    COPTX="$RPM_OPT_FLAGS -DTRY_EXT2_FS"                                \\\
    LDOPTX="$RPM_LD_FLAGS"                                              \\\
    LINKMODE=dynamic                                                    \\\
    DEFCCOM=gcc

# Note: disable optimalisation by COPTX='-g3 -O0' LDOPTX='-g3 -O0'
make %make_flags

%install
make install -s %make_flags

ln -s star.1.gz ${RPM_BUILD_ROOT}%{_mandir}/man1/ustar.1
mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}
mkdir -p ${RPM_BUILD_ROOT}%{_pkgdocdir}
ln -s %{_sbindir}/rmt ${RPM_BUILD_ROOT}%{_sysconfdir}/rmt
install -p -m 644 COPYING star/README  CDDL.Schily.txt AN-* \
    ${RPM_BUILD_ROOT}%{_pkgdocdir}

# XXX Nuke unpackaged files.
( cd ${RPM_BUILD_ROOT}
  rm -f .%{_bindir}/mt
  rm -f .%{_bindir}/smt
  rm -f .%{_bindir}/tartest
  rm -f .%{_bindir}/tar
  rm -f .%{_bindir}/gnutar
  rm -f .%{_bindir}/star_fat
  rm -f .%{_bindir}/star_sym
  rm -f .%{_bindir}/suntar
  rm -f .%{_sysconfdir}/default/star
  rm -rf .%{_prefix}%{_sysconfdir}
  rm -rf .%{_prefix}/include
  rm -rf .%{_prefix}/lib # hard-wired intently
  rm -rf .%{_mandir}/man3
  rm -rf .%{_mandir}/man5/{makefiles,makerules}.5*
  rm -rf .%{_mandir}/man1/{tartest,gnutar,smt,mt,suntar,match}.1*
  rm -rf .%{_docdir}/star/testscripts
  rm -rf .%{_docdir}/star/TODO
  rm -rf .%{_docdir}/rmt
)

%global general_docs \
%dir %{_pkgdocdir} \
%doc %{_pkgdocdir}/COPYING \
%doc %{_pkgdocdir}/CDDL.Schily.txt \

%post -n spax
%{ALTERNATIVES} \
    --install   %{ALT_LINK}     %{ALT_NAME}     %{ALT_PATH}     66 \
    --slave     %{ALT_SL1_LINK} %{ALT_SL1_NAME} %{ALT_SL1_PATH}

%preun -n spax
if [ $1 -eq 0 ]; then
    # only on pure uninstall (not upgrade)
    %{ALTERNATIVES} --remove %{ALT_NAME} %{ALT_PATH}
fi

%files
%doc %{_pkgdocdir}
%{_bindir}/star
%{_bindir}/ustar
%{_mandir}/man1/star.1*
%{_mandir}/man1/star_sym.1*
%{_mandir}/man1/ustar.1*
%{_mandir}/man5/star.5*

%files -n scpio
%general_docs
%doc %{_mandir}/man1/scpio.1*
%{_bindir}/scpio

%files -n spax
%general_docs
%doc %{_mandir}/man1/spax.1*
%{_bindir}/spax
%ghost %verify(not md5 size mode mtime) %{ALT_LINK}
%ghost %verify(not md5 size mode mtime) %{ALT_SL1_LINK}

%files -n rmt
%general_docs
%{_sbindir}/rmt
%{_mandir}/man1/rmt.1*
%config %{_sysconfdir}/default/rmt
# This symlink is used by cpio, star, spax, scpio, .. thus it is needed.  Even
# if the cpio may be configured to use /sbin/rmt rather than /etc/rmt, star (and
# thus spax, ..) has the lookup path hardcoded to '/etc/rmt' (it means that even
# non rpm based systems will try to look for /etc/rmt).  And - the conclusion is
# - it does not make sense to fight against /etc/rmt symlink ATM (year 2013).
%{_sysconfdir}/rmt

%changelog
* Fri Oct 29 2021 Muhammad Falak <mwani@microsft.com> - 1.6-4
- Remove epoch

* Wed Sep 01 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.6-3
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Using "LINKMODE=dynamic" to fix build issues.

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Sep 23 2019 Pavel Raiskup <praiskup@redhat.com> - 1.6-1
- new upstream release
- drop WITH_SELINUX knob and selinux patches, there's built-in support now
- drop several patches which were incorporated upstream, except for
  changewarnSegv patch (did not apply, and not needed nowadays)

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.3-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.3-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Nov 28 2018 Pavel Raiskup <praiskup@redhat.com> - 1.5.3-15
- fix covscan issues which have upstream fix (rhbz#1602700)
- reorder patches so we can easily apply %%_rawbuild macro

* Wed Aug 01 2018 Vaclav Danek <vdanek@redhat.com> - 1.5.3-14
- Fix segfault on restore default acl (rhbz#1567836)

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.3-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Apr 09 2018 Rafael Santos <rdossant@redhat.com> - 1.5.3-12
- Use standard Fedora linker flags (bug #1548670)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.3-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.3-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Aug 12 2016 Michal Toman <mtoman@fedoraproject.org> - 1.5.3-7
- Build properly on MIPS

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Dec 17 2014 Pavel Raiskup <praiskup@redhat.com> - 1.5.3-4
- fix segfault for pax -X (#1175009)

* Tue Sep 16 2014 Peter Robinson <pbrobinson@fedoraproject.org> 1.5.3-3
- Re-enable profiling on aarch64

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Jun 27 2014 Pavel Raiskup <praiskup@redhat.com> - 1.5.3-1
- rebase to 1.5.3

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.2-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Jan 17 2014 Pavel Raiskup <praiskup@redhat.com> - 1.5.2-10
- enable build for ppc64le (#1054401)

* Mon Jan 13 2014 Peter Robinson <pbrobinson@fedoraproject.org> 1.5.2-9
- Temporarily disable profiling on aarch64

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jun 20 2013 Pavel Raiskup <praiskup@redhat.com> - 1.5.2-7
- we should provide /etc/rmt symlink for a while (related to #968980)
- use the ssh as the default remote access method

* Thu May 30 2013 Pavel Raiskup <praiskup@redhat.com> - 1.5.2-6
- subpackage also 'rmt' (#968980)

* Fri May 24 2013 Pavel Raiskup <praiskup@redhat.com> - 1.5.2-5
- add missing ghost files (#960007)
- fix the upgrade path, sorry for the noise (#959917, #960007)

* Mon May 06 2013 Pavel Raiskup <praiskup@redhat.com> - 1.5.2-2
- package spax and scpio separately (#959917)
- fedora-review fixes, unapplied patch
- make the spax to be pax alternative (#960007)

* Wed Apr 10 2013 Pavel Raiskup <praiskup@redhat.com> - 1.5.2-1
- rebase to most up2date upstream tarball, remove patches already upstream, fix
  code movements in patches (#928758)
- fix man-page-day objections (private #948866)
- fix the build for aarch64 (#926571)

* Thu Mar 21 2013 Pavel Raiskup <praiskup@redhat.com> - 1.5.1-12
- package also the 'scpio' utility (#771926)

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Oct 18 2012 Pavel Raiskup <praiskup@redhat.com> - 1.5.1-10
- do not crash during extracting if extended attributes are not set on all
  archived files (#861848)
- note in man page that H=crc format uses Sum32 algorithm (FIPS refuses CRC)

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jan 04 2011 Ondrej Vasik <ovasik@redhat.com> 1.5.1-6
- fix segfault with multivol option due to signedness(#666015)

* Wed Sep 29 2010 jkeating - 1.5.1-5
- Rebuilt for gcc bug 634757

* Tue Sep 14 2010 Ondrej Vasik <ovasik@redhat.com> 1.5.1-4
- fix another instance of buffer overflow for files with
  long names(#632384)

* Tue Aug 17 2010 Ondrej Vasik <ovasik@redhat.com> 1.5.1-3
- Fix some invalid manpage references (#624612)
- ship star.4 manpage with star format description

* Wed Feb 03 2010 Ondrej Vasik <ovasik@redhat.com> 1.5.1-2
- fix buffer overflow for files with names of length
  100 chars(#556664)

* Wed Jan 13 2010 Ondrej Vasik <ovasik@redhat.com> 1.5.1-1
- new upstream release 1.5.1

* Thu Aug 27 2009 Ondrej Vasik <ovasik@redhat.com> 1.5-8
- provide symlinked manpage for ustar

* Thu Aug 27 2009 Ondrej Vasik <ovasik@redhat.com> 1.5-7
- Merge review (#226434) changes: convert AN-1.5 to utf-8,
  spec file cosmetic/policy changes, ship README.linux in doc

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun May 10 2009 Ville Skyttä <ville.skytta at iki.fi> - 1.5-5
- Build with $RPM_OPT_FLAGS.
- Convert specfile to UTF-8.

* Wed Apr 08 2009 Ondrej Vasik <ovasik@redhat.com> 1.5-4
- fix build failure due to symbols conflicting
  with stdio(#494213)

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Jan 28 2009 Ondrej Vasik <ovasik@redhat.com> 1.5-2
- remove names.c requirements from non-fat Makefiles,
  do not ship names.c (#255261 for details)

* Tue Jan 27 2009 Ondrej Vasik <ovasik@redhat.com> 1.5-1
- use final instead of beta
- ship missing names.c separately
- enable optimalization again

* Wed Dec 03 2008 Ondrej Vasik <ovasik@redhat.com> 1.5a89-1
- update to latest upstream release

* Fri Jun 06 2008 Dennis Gilmore <dennis@ausil.us> 1.5a84-6
- add sparcv9 support

* Mon May 12 2008 Peter Vrabec <pvrabec@redhat.com> 1.5a84-5
- add super-H(sh3,4) architecture support (#442883)

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.5a84-4
- Autorebuild for GCC 4.3

* Fri Aug 31 2007 Dan Kopecek <dkopecek@redhat.com> 1.5a84-3
- added -O0 to COPTX (CFLAGS) (see #255261)

* Mon Aug 27 2007 Peter Vrabec <pvrabec@redhat.com> 1.5a84-2
- fix segfault of data-change-warn option (#255261),
  patch from dkopecek@redhat.com

* Fri Aug 24 2007 Peter Vrabec <pvrabec@redhat.com> 1.5a84-1
- new upstream release with CVE-2007-4134 fix

* Sun Jun 24 2007 Peter Vrabec <pvrabec@redhat.com> 1.5a76-3
- build star on ARM platforms (#245465)

* Mon Jan 29 2007 Peter Vrabec <pvrabec@redhat.com> 1.5a76-2
- fix buildreq. and rebuild

* Thu Jan 18 2007 Jan Cholasta <grubber.x@gmail.com> 1.5a76-1
- upgrade

* Tue Aug 08 2006 Peter Vrabec <pvrabec@redhat.com> 1.5a75-1
- upgrade

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.5a74-3.1
- rebuild

* Tue Jun 13 2006 Peter Vrabec <pvrabec@redhat.com> 1.5a74-3
- use autoconf provided by star

* Fri Jun 02 2006 Peter Vrabec <pvrabec@redhat.com> 1.5a74-2
- update tarball

* Mon Apr 24 2006 Peter Vrabec <pvrabec@redhat.com> 1.5a74-1
- upgrade

* Wed Mar 22 2006 Peter Vrabec <pvrabec@redhat.com> 1.5a73-1
- upgrade

* Wed Mar 01 2006 Peter Vrabec <pvrabec@redhat.com> 1.5a72-1
- upgrade

* Wed Feb 22 2006 Peter Vrabec <pvrabec@redhat.com> 1.5a71-1
- upgrade

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Tue Nov 08 2005 Peter Vrabec <pvrabec@redhat.com> 1.5a69-1
- upgrade

* Mon Oct 10 2005 Peter Vrabec <pvrabec@redhat.com> 1.5a68-1
- upgrade

* Thu Sep 22 2005 Peter Vrabec <pvrabec@redhat.com> 1.5a67-1
- upgrade

* Fri Aug 26 2005 Peter Vrabec <pvrabec@redhat.com> 1.5a65-1
- upgrade 1.5a65-1 made by Horst H. von Brand <vonbrand@inf.utfsm.cl>
- Source URL changed, no homepage now
- License changed from GPL to CDDL 1.0
- Define MAKEPROG=gmake like the Gmake.linux script does
- Disable fat binary as per star/Makefile, update star-1.5-selinux.patch for
  the various *.mk files used in that case
- Axe /usr/share/man/man1/match.1*, /usr/etc/default/rmt too
- Explicit listing in %%files, allow for compressed or plain manpages

* Fri Aug 26 2005 Peter Vrabec <pvrabec@redhat.com>
- do not remove star_fat

* Fri Aug 12 2005 Peter Vrabec <pvrabec@redhat.com>
- upgrade  1.5a64-1

* Thu Aug 04 2005 Karsten Hopp <karsten@redhat.de> 1.5a54-3
- remove /usr/bin/tar symlink

* Fri Mar 18 2005 Peter Vrabec <pvrabec@redhat.com>
- rebuilt

* Mon Nov 22 2004 Peter Vrabec <pvrabec@redhat.com>
- upgrade 1.5a54-1 & rebuild

* Mon Oct 25 2004 Peter Vrabec <pvrabec@redhat.com>
- fix dependencie (#123770)

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Jan 26 2004 Dan Walsh <dwalsh@redhat.com> 1.5a25-4
- Fix call to is_selinux_enabled

* Mon Jan 19 2004 Jeff Johnson <jbj@jbj.org> 1.5.a25-3
- fix: (!(x & 1)) rather than (!x & 1) patch.

* Wed Sep 24 2003 Dan Walsh <dwalsh@redhat.com> 1.5a25-2
- turn selinux off

* Tue Sep 16 2003 Dan Walsh <dwalsh@redhat.com> 1.5a25-1.sel
- turn selinux on

* Fri Sep 5 2003 Dan Walsh <dwalsh@redhat.com> 1.5a18-5
- turn selinux off

* Mon Aug 25 2003 Dan Walsh <dwalsh@redhat.com> 1.5a18-3
- Add SELinux modification to handle setting security context before creation.

* Thu Aug 21 2003 Dan Walsh <dwalsh@redhat.com> 1.5a18-2
- Fix free_xattr bug

* Wed Jul 16 2003 Dan Walsh <dwalsh@redhat.com> 1.5a18-1
- Add SELinux support

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Tue Nov 12 2002 Elliot Lee <sopwith@redhat.com> 1.5a08-3
- Build when uname -m != _target_platform
- Use _smp_mflags
- Build on x86_64

* Mon Nov 11 2002 Jeff Johnson <jbj@redhat.com> 1.5a08-2
- update to 1.5a08.
- build from cvs.

* Wed Jun 26 2002 Trond Eivind Glomsrød <teg@redhat.com> 1.5a04
- Initial build. Alpha version - it's needed for ACLs.
