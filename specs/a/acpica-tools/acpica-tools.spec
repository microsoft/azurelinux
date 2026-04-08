# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           acpica-tools
Version:        20240322
Release:        3%{?dist}
Summary:        ACPICA tools for the development and debug of ACPI tables

# Automatically converted from old format: GPLv2 - review is highly recommended.
License:        GPL-2.0-only
URL:            https://www.acpica.org/

ExcludeArch:	i686 armv7hl s390x

Source0:        https://acpica.org/sites/acpica/files/acpica-unix2-%{version}.tar.gz
Source1:        https://acpica.org/sites/acpica/files/acpitests-unix-%{version}.tar.gz
Source2:        README.Fedora
Source3:        iasl.1
Source4:        acpibin.1
Source5:        acpidump.1
Source6:        acpiexec.1
Source7:        acpihelp.1
Source9:        acpisrc.1
Source10:       acpixtract.1
Source11:       acpiexamples.1
Source12:       badcode.asl.result
Source13:       grammar.asl.result
Source14:       converterSample.asl.result
Source15:       run-misc-tests.sh
Source16:       COPYING

# other miscellaneous patches
Patch00:	unaligned.patch
Patch01:	template.patch
Patch02:        cve-2017-13693.patch
Patch03:        cve-2017-13694.patch
Patch04:        cve-2017-13695.patch
Patch05:        str-trunc-warn.patch
Patch06:	dbtest.patch
Patch07:	dangling-ptr.patch
Patch08:	uuid-len.patch
Patch09:	fix-version.patch
Patch10:	0001-Correct-DBG2-dump-of-OemData.patch
Patch11:	0002-Correct-dumping-of-SLIC-tables.patch
Patch12:	0003-PHAT-FW-health-table-can-be-zero-length.patch

BuildRequires:	make
BuildRequires:  bison patchutils flex gcc

# The previous iasl package contained only a very small subset of these tools
# and it produced only the iasl package listed below; further, the pmtools
# package -- which provides acpidump -- also provides a /usr/sbin/acpixtract
# that we don't really want to collide with
Provides:       acpixtract >= 20120913-7
Provides:       iasl = %{version}-%{release}
Obsoletes:      iasl < 20120913-8

# The pmtools package provides an obsolete and deprecated version of the
# acpidump command from lesswatts.org which has now been taken off-line.
# ACPICA, however, is providing a new version and we again do not want to
# conflict with the command name.
Provides:       acpidump >= 20100513-5
Provides:       pmtools = %{version}-%{release}
Obsoletes:      pmtools < 20100513-6

%description
The ACPI Component Architecture (ACPICA) project provides an OS-independent
reference implementation of the Advanced Configuration and Power Interface
Specification (ACPI).  ACPICA code contains those portions of ACPI meant to
be directly integrated into the host OS as a kernel-resident subsystem, and
a small set of tools to assist in developing and debugging ACPI tables.

This package contains only the user-space tools needed for ACPI table
development, not the kernel implementation of ACPI.  The following commands
are installed:
   -- iasl: compiles ASL (ACPI Source Language) into AML (ACPI Machine
      Language), suitable for inclusion as a DSDT in system firmware.
      It also can disassemble AML, for debugging purposes.
   -- acpibin: performs basic operations on binary AML files (e.g.,
      comparison, data extraction)
   -- acpidump: write out the current contents of ACPI tables
   -- acpiexec: simulate AML execution in order to debug method definitions
   -- acpihelp: display help messages describing ASL keywords and op-codes
   -- acpisrc: manipulate the ACPICA source tree and format source files
      for specific environments
   -- acpixtract: extract binary ACPI tables from acpidump output (see
      also the pmtools package)

This version of the tools is being released under GPLv2 license.

%prep
%setup -q -n acpica-unix2-%{version}
gzip -dc %{SOURCE1} | tar -x --strip-components=1 -f -

%autopatch -p1

cp -p %{SOURCE2} README.Fedora
cp -p %{SOURCE3} iasl.1
cp -p %{SOURCE4} acpibin.1
cp -p %{SOURCE5} acpidump.1
cp -p %{SOURCE6} acpiexec.1
cp -p %{SOURCE7} acpihelp.1
cp -p %{SOURCE9} acpisrc.1
cp -p %{SOURCE10} acpixtract.1
cp -p %{SOURCE11} acpiexamples.1
cp -p %{SOURCE12} badcode.asl.result
cp -p %{SOURCE13} grammar.asl.result
cp -p %{SOURCE14} converterSample.asl.result
cp -p %{SOURCE15} tests/run-misc-tests.sh
chmod a+x tests/run-misc-tests.sh
cp -p %{SOURCE16} COPYING

# spurious executable permissions on text files in upstream
chmod a-x changes.txt
chmod a-x source/compiler/new_table.txt


%build
CWARNINGFLAGS="\
    -std=c99\
    -Wall\
    -Wbad-function-cast\
    -Wdeclaration-after-statement\
    -Werror\
    -Wformat=2\
    -Wmissing-declarations\
    -Wmissing-prototypes\
    -Wstrict-aliasing=0\
    -Wstrict-prototypes\
    -Wswitch-default\
    -Wpointer-arith\
    -Wundef\
    -Waddress\
    -Waggregate-return\
    -Winit-self\
    -Winline\
    -Wmissing-declarations\
    -Wmissing-field-initializers\
    -Wnested-externs\
    -Wold-style-definition\
    -Wno-format-nonliteral\
    -Wredundant-decls\
    -Wempty-body\
    -Woverride-init\
    -Wlogical-op\
    -Wmissing-parameter-type\
    -Wold-style-declaration\
    -Wtype-limits"

OPT_CFLAGS="%{optflags} $CWARNINGFLAGS"
OPT_LDFLAGS="%{__global_ldflags}"
export OPT_CFLAGS
export OPT_LDFLAGS

%{make_build}


%install
# Install the binaries
mkdir -p %{buildroot}%{_bindir}
install -pD generate/unix/bin*/* %{buildroot}%{_bindir}/

# Install the man pages
mkdir -p %{buildroot}%{_mandir}/man1
install -pDm 0644 *.1 %{buildroot}%{_mandir}/man1/

# Install the examples source code
mkdir -p %{buildroot}%{_docdir}/acpica-tools/examples
install -pDm 0644 source/tools/examples/* %{buildroot}%{_docdir}/acpica-tools/examples/

%check
cd tests

# ASL tests
./aslts.sh                         # relies on non-zero exit
[ $? -eq 0 ] || exit 1

# misc tests
./run-misc-tests.sh %{buildroot}%{_bindir} %{version}

%pre
if [ -e %{_bindir}/acpixtract-acpica ]
then
    alternatives --remove acpixtract %{_bindir}/acpixtract-acpica
fi
if [ -e %{_bindir}/acpidump-acpica ]
then
    alternatives --remove acpidump %{_bindir}/acpidump-acpica
fi

%postun
if [ -e %{_bindir}/acpixtract-acpica ]
then
    alternatives --remove acpixtract %{_bindir}/acpixtract-acpica
fi
if [ -e %{_bindir}/acpidump-acpica ]
then
    alternatives --remove acpidump %{_bindir}/acpidump-acpica
fi


%files
%doc changes.txt source/compiler/new_table.txt
%doc README.Fedora COPYING
%{_bindir}/*
%{_mandir}/*/*
%{_docdir}/*/*


%changelog
* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 20240322-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 20240322-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Aug 12 2024 Al Stone <ahs3@fedoraproject.org> - 20240322-1
- Update source tree to 20240322 version from upstream.  NB: this update
  is done in conjunction with removing s390x support due to the large
  number of patches that are now rendered obsolete.  Closes BZ#2138250.
- Note, too, that the upstream version of the tarball is missing two
  commits and has the wrong name; discussed this with upstream and
  included a patch with the two commits to correct this, and renamed
  the tarballs to try to maintain consistency. So, upstream is actually
  named version 20240321, but it should be 20240322 according to their
  own git tree (see tag G20240322 on github).
- Removed executable bit from all the upstream source files
- Remove big-endian support, aka s390x.  Closes BZ#2298855.
- Remove several 32-bit only patches that are also obsolete since they
  are for unsupported architectures (thanks to pbonzini and PR#5).
- Remove PIE patches since that is currently the default (again, thanks
  to pbonzini and PR#5)

* Mon Jul 29 2024 Miroslav Suchý <msuchy@redhat.com> - 20220331-10
- convert license to SPDX

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 20220331-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 20220331-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 20220331-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 20220331-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jan 18 2023 Fedora Release Engineering <releng@fedoraproject.org> - 20220331-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 20220331-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sun Apr 3 2022 Al Stone <ahs3@redhat.com> - 20220331-3
- Correct typo in ExcludeArch syntax

* Sun Apr 3 2022 Al Stone <ahs3@redhat.com> - 20220331-2
- Stop building 32-bit architecture (i686 and armv7hl); they have been
  deprecated in Fedora

* Sun Apr 3 2022 Al Stone <ahs3@redhat.com> - 20220331-1
- Update to 20220331 upstream source.  Bring all the patches up to date.
- Update the results of misc test cases.
- Add in big-endian patches for PRMT, RGRT and SVKL tables (thanks, Dean!)

* Mon Mar 28 2022 Al Stone <ahs3@redhat.com> - 20211217-2
- Stop building i686; it is the only Arch that stumbles across a problem
  in using varargs but since the Arch has been essentially deprecated,
  take this as an opportunity to finally drop support for it.

* Fri Mar 18 2022 Al Stone <ahs3@redhat.com> - 20211217-1
- Update to 20211217 upstream source.  Bring all the patches up to date.
- Rawhide use of GCC 12 introduces a new check for dangling pointers which
  causes non-portable code in utdebug.c stack functions to not compile; add
  a patch to disable -Wdangling-pointer=2 for the specific functions
- The AeRegionHandler() code in acpiexec call a UUID function with a buffer
  too small for the UUID output string; add a patch to correct this.

* Wed Jan 19 2022 Fedora Release Engineering <releng@fedoraproject.org> - 20210604-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Oct 4 2021 Al Stone <ahs3@redhat.com> - 20210730-1
- Update to 20210730 upstream source.  Bring all the patches up to date.

* Tue Jul 27 2021 Al Stone <ahs3@redhat.com> - 20210604-3
- Running 'iasl -T all' would segfault when dumping the PHAT template;
  fixed AcpiDmDumpPhat() by removing unnecessary assignments from patch
- Borrowed a patch from upstream to fix Unicode usage in WPBTs

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 20210604-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sun Jul 11 2021 Al Stone <ahs3@redhat.com> - 20210604-1
- Update to 20210604 source tree (please note that tarballs for versions
  between 20200925 and 20210604 have been uploaded for archival reasons
  but no packaged version of these has been commited to the Fedora project)
- Bring the big-endian patches up-to-date with what has been submitted
  upstream (not accepted currently).

* Mon Jan 25 2021 Fedora Release Engineering <releng@fedoraproject.org> - 20200925-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Oct 19 2020 Al Stone <ahs3@redhat.com> - 20200925-1
- Update to 20200925 source tree
- Completely revamp the old big-endian patches (maintainability was the goal).
  This results in a much larger patch set, but each patch is more clearly used
  for a specific purpose.
- The acpinames command has been deprecated upstream; acpiexec provides 
  replacement functionality.

* Fri Jul 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 20200430-3
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 20200430-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jun 8 2020 Al Stone <ahs3@redhat.com> - 202004306-1
- Update to 202004306 source tree, including patch refreshes

* Wed Apr 1 2020 Al Stone <ahs3@redhat.com> - 20200326-1
- Update to 20200326 source tree, including patch refreshes
- Removed a couple of patches that got included upstream

* Wed Feb 26 2020 Al Stone <ahs3@redhat.com> - 20200214-1
- Update to 20200214 source tree, including patch refreshes
- Add patch to fix up issues where strings and 4-byte quantities
  get interchanged; C strings want to be null terminated now, but
  AML does not so using strncpy is painful.
- Add patch for s390x specific issue (dbtest), where initializing a
  string on the stack behaves a little differently 
- "PCC" is a defined Register() type, but "PlatformCommChannel" was
  being used instead; put it back to "PCC" as it should be in pcc.patch
- Add another big-endian patch to compensate for changes to nsutils.c

* Mon Feb 24 2020 Al Stone <ahs3@redhat.com> - 20200110-1
- Update to 20200110 source tree, including patch refreshes

* Sun Feb 23 2020 Al Stone <ahs3@redhat.com> - 20191213-1
- Update to 20191213 source tree, including patch refeshes.
- badexit patch no longer needed, so removed
- GCC10 enforces -fno-common now, catching multiple places where linkage
  is not explicitly stated; added a patch to resolve the linker errors

* Sun Feb 23 2020 Al Stone <ahs3@redhat.com> - 20191018-2
- Upstream does not build from source -- this release not pushed into
  the archives and noted here just for record keeping

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 20190816-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Nov 23 2019 Al Stone <ahs3@redhat.com> - 20191018-1
- Update to 20191019 source tree, including patch refeshes.

* Tue Oct 29 2019 Al Stone <ahs3@redhat.com> - 20190816-1
- Update to 20190816 source tree, including patch refeshes.
- Add a patch to fix a non-zero exit from iasl -T ALL that actually succeeds
- Remove the "template" tests; they have been subsumed by aslts.sh as they
  should be

* Thu Oct 24 2019 Al Stone <ahs3@redhat.com> - 20190703-1
- Update to 20190703 source tree, including patch refeshes.

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 20190509-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun May 26 2019 Peter Robinson <pbrobinson@fedoraproject.org> 20190509-4
- Bump release for clean upgrade from F-29

* Mon May 13 2019 Al Stone <ahs3@redhat.com> - 20190509-2
- Added an arm7hl specific fix acenv.h; GCC9 on arm7hl can now deal
  with misalignments so the unaligned patch could be relaxed a bit
- the templates test was failing because of the backup left behind
  by the patch macro, so change the invocation of the macro.

* Sat May 11 2019 Al Stone <ahs3@redhat.com> - 20190509-1
- Update to 20190509 source tree, including patch refeshes.

* Fri May 10 2019 Al Stone <ahs3@redhat.com> - 20190405-1
- Update to 20190405 source tree, including patch refeshes.

* Fri May 10 2019 Al Stone <ahs3@redhat.com> - 20190329-1
- Update to 20190329 source tree, including patch refeshes.

* Fri May 10 2019 Al Stone <ahs3@redhat.com> - 20190215-1
- Update to 20190215 source tree, including patch refeshes.

* Fri May 10 2019 Al Stone <ahs3@redhat.com> - 20190108-1
- Update to 20190108 source tree, including patch refeshes.
- Replace use of strncpy() with memcpy() when moving ASCII bytes around;
  the tables use "strings" but they are seldom null terminated, causing
  GCC9 to complain.  Closes BZ#1674629.

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 20181213-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Dec 19 2018 Al Stone <ahs3@redhat.com> - 20181213-2
- Add a patch to allow zero DSDT addresses in the FADT when compiling

* Thu Dec 13 2018 Al Stone <ahs3@redhat.com> - 20181213-1
- Update to 20181213 source tree, including patch refeshes.
- Refresh patches; folded be-tpm2 into the larger big-endian patch after

* Thu Dec 13 2018 Al Stone <ahs3@redhat.com> - 20181031-1
- Update to 20181031 source tree, including patch refeshes. Closes BZ#1656229
- Refresh patches; folded be-tpm2 into the larger big-endian patch after
  cleaning it up a bit
- Merge in acpica-tools-tests PR

* Wed Oct 24 2018 Al Stone <ahs3@redhat.com> - 20181003-1
- Update to 20181003 source tree, including patch refeshes. Closes BZ#1634207
- Merge in dump-tables PR

* Mon Sep 17 2018 Al Stone <ahs3@redhat.com> - 20180810-1
- Update to 20180810 source tree, including patch refeshes. Closes BZ#1614986

* Wed Aug 8 2018 Al Stone <ahs3@redhat.com> - 20180629-3
- Add in man page for acpiexamples.  So that the man page makes some sense,
  also copy the source code used for acpiexamples to the doc directory for
  this package.  Closes BZ#1611145.
- Add in the converterSample.asl file from the misc tests.  Clean up the
  run-misc-tests.sh script, too, to make it more robust by simplifying
  the work done.

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 20180629-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sun Jul 8 2018 Al Stone <ahs3@redhat.com> - 20180629-1
- Update to 20180629 source tree, including patch refeshes. Closes BZ#1584923
- Includes upstream fix for #1592971 (iasl segfault).

* Thu Jun 21 2018 Al Stone <ahs3@redhat.com> - 20180531-1
- Update to 20180531 source tree, including patch refeshes. Closes BZ#1584923

* Tue May 22 2018 Al Stone <ahs3@redhat.com> - 20180508-2
- %%pre and %%post scriptlets fail -- stupid thinko where I inadvertently
  tested for alternatives not existing, vs existing 

* Tue May 15 2018 Al Stone <ahs3@redhat.com> - 20180508-1
- Update to 20180508 source tree, including patch refeshes. Closes BZ#1544048
- acpidump/acpixtract no longer have alternatives, so remove the scriptlets
  that maintain them and just install them directly; we do leave the pre-
  and post- scriptlets to remove the alternatives for now.  Closes BZ#1576970
- Typo: OPT_LDFLAGS, not OPT_LDLAGS in the build section.  Closes BZ#1560542

* Mon May 14 2018 Al Stone <ahs3@redhat.com> - 20180427-1
- Update to 20180427 source tree, including patch refeshes. Closes BZ#1544048

* Mon May 14 2018 Al Stone <ahs3@redhat.com> - 20180313-1
- Update to 20180313 source tree, including patch refeshes. Closes BZ#1544048

* Fri Mar 16 2018 Al Stone <ahs3@redhat.com> - 20180209-1
- Update to 20180209 source tree, including patch refeshes. Closes BZ#1544048
- CVE-2017-13693: operand cache leak in dsutils.c -- applied github patch to
  fix the leak.  Resolves BZ#1485346.
- CVE-2017-13694: acpi parse and parseext cache leaks in psobjects.c -- applied
  github patch to fix the leaks.  Resolves BZ#1485348.
- CVE-2017-13695: operand cache leak in nseval.c -- applied github patch to fix
  the leak.  Resolves BZ#1485349.
- Security fixes for the CVEs above applied.  Closes BZ#1485355.  NOTE: these
  patches fix acpica-tools ONLY; the kernel needs to be patch separately.
- Added gcc to BuildRequires
- It turns out the %%build section was incorrectly passing in OPT_CFLAGS; it
  made the wrong assumptions about what generate/unix/Makefile.config did with
  that value.  Added to the spec file what should happen so that a full and
  complete set of C flags get passed in, not just the small subset that was.
- Clean up compiler warnings for truncated strings
- Clean up compiler warnings for pointer casting on 32-bit architectures

* Fri Feb 09 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 20180105-3
- Escape macros in %%changelog

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 20180105-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Jan 8 2018 Al Stone <ahs3@redhat.com> - 20180105-1
- Update to 20180105 source tree, including patch refeshes. Closes BZ#1526651
- Cleaned up changelog. Closes BZ#1525938
- Pulled in a mips32/BE patch from Debian, for completeness sake

* Mon Jan 8 2018 Al Stone <ahs3@redhat.com> - 20171215-1
- Update to 20171215 source tree, including patch refeshes

* Mon Nov 20 2017 Al Stone <ahs3@redhat.com> - 20171110-1
- Update to 20171110 source tree, including patch refeshes
- Add patch for mips64el build, should it ever be needed; it also cleans
  up all 64-bit arches, so nice to have regardless
- Add new patch for a TPM2 big-endian issue.

* Fri Oct 6 2017 Al Stone <ahs3@redhat.com> - 20170929-1
- Update to 20170929 source tree, including patch refeshes
- Removed aslts-acpibin.patch to fix PATH problem in ASLTS; in upstream now

* Wed Sep 27 2017 Al Stone <ahs3@redhat.com> - 20170831-1
- Update to 20170831 source tree, including patch refeshes
- Add aslts-acpibin.patch to fix PATH problem in ASLTS that prevents
  some tests from being run

* Fri Aug 18 2017 Al Stone <ahs3@redhat.com> - 20170728-3
- Completed the big-endian fixes (I think)
- Fix ppc64le.patch that inadvertently broke s390x
- Minor patch refresh
- Re-enable full %%check for s390x

* Mon Aug 14 2017 Al Stone <ahs3@redhat.com> - 20170728-2
- Start some long delayed clean-up
- Temporarily disable one test section until all the big-endian issues
  can be resolved; it provides what may be a false negative result
- Consolidate the big-endian patches

* Fri Aug 11 2017 Al Stone <ahs3@redhat.com> - 20170728-1
- Update to 20170728 source tree, including patch refeshes

* Fri Aug 11 2017 Al Stone <ahs3@redhat.com> - 20170629-1
- Update to 20170629 source tree, including patch refeshes

* Fri Aug 11 2017 Al Stone <ahs3@redhat.com> - 20170531-1
- Update to 20170531 source tree, including patch refeshes

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 20170303-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 20170303-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri May 5 2017 Al Stone <ahs3@redhat.com> - 20170303-3
- Correct ppc64le.patch; it was not setting little-endian properly.

* Tue May 2 2017 Al Stone <ahs3@redhat.com> - 20170303-2
- Correct update-big-endian.patch; it introduced a bug due to logic being
  replaced in the wrong order.

* Fri Mar 31 2017 Al Stone <ahs3@redhat.com> - 20170303-1
- Update to latest upstream.  Closes BZ#1381017.
- Refresh patches.

* Fri Mar 31 2017 Al Stone <ahs3@redhat.com> - 20170224-1
- Update to latest upstream.  Closes BZ#1381017.
- Refresh patches.

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 20170119-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Jan 30 2017 Al Stone <ahs3@redhat.com> - 20170119-1
- Update to latest upstream.  Closes BZ#1381017.
- Refresh patches.
- Add patch to fix ASLTS.
- Add patch to fix ppc64le build.
- Add patch to fix arm7hl build.

* Mon Jan 9 2017 Al Stone <ahs3@redhat.com> - 20161222-1
- Update to latest upstream.  Closes BZ#1381017.
- Refresh patches.

* Mon Jan 9 2017 Al Stone <ahs3@redhat.com> - 20160930-3
- Restructure the repairs for big-endian support to simplify patching -- it is
  all combined into update-big-endian.patch now.  (NB: this version may still
  have issues on big-endian)

* Fri Dec 9 2016 Al Stone <ahs3@redhat.com> - 20160930-2
- Major repairs to compiler and disassembler code to make it endian-neutral
  again (added patches big-endian-part1 and big-endian-part2).

* Fri Oct 28 2016 Al Stone <ahs3@redhat.com> - 20160930-2
- Update to latest upstream.  Closes BZ#1381017.
- Refresh patches.
- Major repairs to disassembler code to make it endian-neutral again.

* Thu Sep 1 2016 Al Stone <ahs3@redhat.com> - 20160831-1
- Update to latest upstream.  Closes BZ#1372107.
- Refresh patches.
- Closes BZ#1365193 -- s390x FTBFS due to int/ptr size mismatch: made sure
  the tools built with 64-bit integers for s390x

* Tue Aug 2 2016 Al Stone <ahs3@redhat.com> - 20160729-1
- Update to latest upstream.  Closes BZ#1361737.
- Refresh patches.

* Thu Jun 9 2016 Al Stone <ahs3@redhat.com> - 20160527-1
- Update to latest upstream.  Closes BZ#1340573.
- Refresh patches.

* Tue Apr 26 2016 Al Stone <ahs3@redhat.com> - 20160422-1
- Update to latest upstream.  Closes BZ#1329774.
- Refresh patches.

* Sat Mar 19 2016 Al Stone <ahs3@redhat.com> - 20160318-1
- Update to latest upstream.  Closes BZ#1319359.
- Refresh patches.

* Mon Feb 22 2016 Al Stone <ahs3@redhat.com> - 20160212-1
- Update to latest upstream.  Closes BZ#1307192.
- Refresh patches.

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 20160108-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Jan 11 2016 Al Stone <ahs3@redhat.com> - 20160108-1
- Update to latest upstream.  Closes BZ#1297078.
- Refresh patches.

* Wed Jan 6 2016 Al Stone <ahs3@redhat.com> - 20151218-1
- Update to latest upstream.  Closes BZ#1292987.
- Refresh patches, and remove one no longer needed (acpinames).

* Tue Dec 15 2015 Al Stone <ahs3@redhat.com> - 20151124-1
- Update to latest upstream.  Closes BZ#1267772.
- Refresh patches.
- Add back in a patch to rename source/tools/acpinames/AcpiNames.h to remove
  the camel case; this is a leftover in the conversion to Un*x files, and
  crept back in with this version.

* Wed Oct 14 2015 Al Stone <ahs3@redhat.com> - 20150930-1
- Update to latest upstream.  Closes BZ#1267772.
- Refresh patches, and remove one no longer needed.

* Thu Sep 10 2015 Al Stone <ahs3@redhat.com> - 20150818-2
- Remove extraneous patch files for AAPITS.
- Correct an assumption that all names are stored in little-endian format.
  Fix is in asllookup-ppc64.patch.  Closes BZ#1251972.

* Wed Sep 9 2015 Al Stone <ahs3@redhat.com> - 20150818-1
- Update to latest upstream.  Closes BZ#1256134.
- Refresh patches
- This version deprecates aapits (ACPICA API Test Suite) for now; this is
  in accordance with upstream wishes, but in this maintainer's view, may
  not be the correct long term solution as there is no other API specific
  test suite.
- Add a patch to rename source/tools/acpinames/AcpiNames.h to remove the
  camel case; this is a leftover in the conversion to Un*x files.

* Tue Aug 4 2015 Al Stone <ahs3@redhat.com> - 20150717-1
- Update to latest upstream.  Closes BZ#1244449.
- Refresh patches
- Bodge back together the aapits makefile after source file relocations in
  the primary ACPICA component files
- Update the misc test results to incorporate iasl improvements

* Tue Jun 30 2015 Al Stone <ahs3@redhat.com> - 20150619-2
- Silly error: forgot to remove patches that are no longer needed

* Mon Jun 29 2015 Al Stone <ahs3@redhat.com> - 20150619-1
- Update to latest upstream.  Closes BZ#1232512.
- Refresh patches

* Tue Jun 16 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20150515-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 3 2015 Al Stone <ahs3@redhat.com> - 20150515-2
- Replace dev-mem patch with nodevmem; this is a much more robust version of
  the functionality needed, and set up properly for arm64 -- the patch makes
  it so that acpidump does not use /dev/mem at all on arm64 since it might
  not contain the right data.

* Mon Jun 1 2015 Al Stone <ahs3@redhat.com> - 20150515-1
- Update to latest upstream.  Closes BZ#122166
- Refresh patches
- Add patch from upstream for incorrect UUIDs for NFIT
- Add patch from Linaro to remove use of /dev/mem (use /sys instead)
- Add patch from upstream to correct ARM GIC entries in MADT
- Add patch to fix segfaults reported.  Closes BZ#1219341.

* Mon Apr 13 2015 Al Stone <ahs3@redhat.com> - 20150410-1
- Update to latest upstream.  Closes BZ#1190383
- Refresh patches

* Fri Apr 10 2015 Al Stone <ahs3@redhat.com> - 20150408-1
- Update to latest upstream.  Closes BZ#1190383
- Refresh patches

* Mon Mar 2 2015 Al Stone <ahs3@redhat.com> - 20150204-1
- Update to latest upstream.  Closes BZ#1190383
- Refresh patches

* Mon Nov 17 2014 Al Stone <ahs3@redhat.com> - 20141107-1
- Update to latest upstream.  Closes BZ#1147131.
- Refresh patches
- Patch to ensure ASLTS always reports when an error occurs, instead
  of glossing over it has been incorporated upstream, so remove patch.

* Wed Oct 1 2014 Al Stone <ahs3@redhat.com> - 20140926-1
- Update to latest upstream.  Closes BZ#1147131.
- Refresh patches
- Add patch to ensure ASLTS always reports when an error occurs, instead
  of glossing over it.
- Add use of %%__global_ldflags.  Closes BZ#1126134.

* Fri Aug 29 2014 Al Stone <ahs3@redhat.com> - 20140828-1
- Update to latest upstream.  Closes BZ#1135352.
- Refresh patches.

* Fri Aug 15 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20140724-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Mon Jul 28 2014 Al Stone <ahs3@redhat.com> - 20140724-1
- Update to latest upstream.  Closes BZ#1114275.
- This update adds support for the 5.1 version of the ACPI specification
- Refresh patches so everything applies properly.

* Fri Jun 6 2014 Dan Horák <dan[at]danny.cz> - 20140424-3
- refresh the big endian patch so it applies correctly, fixes build on big endians

* Thu May 22 2014 Al Stone <ahs3@redhat.com> - 20140424-2
- Add ppc64le as a 64-bit arch in run-misc-tests.sh.  Closes BZ#1098614.
- Re-enable big-endian support in iasl.

* Wed May 7 2014 Al Stone <ahs3@redhat.com> - 20140424-1
- Update to latest upstream.  Closes BZ#1091189.

* Fri Apr 4 2014 Al Stone <ahs3@redhat.com> - 20140325-1
- Update to latest upstream.  Closes BZ#1080791.
- Incorporated patch to fix broken symlinks.  Closes BZ#1074256.
- Add patch to fix missing .o files in aapits tests.

* Wed Feb 26 2014 Al Stone <ahs3@redhat.com> - 20140214-1
- Update to latest upstream.  Closes BZ#1053396.
- Remove temporary patch so that AAPITS will build and run.
- Add patch to print asllookup.c warning properly on big endian;
  Closes BZ#1069178.

* Tue Jan 21 2014 Al Stone <ahs3@redhat.com> - 20140114-1
- Update to latest upstream.  Closes BZ#1053396.
- Remove temporary patch to add Makefile missing from upstream tarball.
- Add temporary patch so that AAPITS will build and run.

* Tue Jan 7 2014 Al Stone <ahs3@redhat.com> - 20131218-1
- Update to latest upstream.  Closes BZ#1044951.
- Add temporary patch to add Makefile missing from upstream tarball.

* Mon Nov 25 2013 Al Stone <ahs3@redhat.com> - 20131115-1
- Update to latest upstream.  Closes BZ#1031255.
- Add a little code to workaround build problems that can occur (the tests
  will fail) when a build starts before midnight, but ends after midnight
- Remove patch to include Makefile.config that was missing from tarball.

* Wed Oct 09 2013 Al Stone <ahs3@redhat.com> - 20130927-1
- Update to latest upstream.  Closes BZ#1013090.
- Add temporary patch to include Makefile.config being missing from tarball.

* Fri Sep 13 2013 Michael Schwendt <mschwendt@fedoraproject.org> - 20130823-5
- correct iasl obs_ver

* Tue Sep 10 2013 Dean Nelson <dnelson@redhat.com> - 20130823-4
- Fix run-misc-tests.sh script to properly set the number of BITS to 64
  when run on a s390x system.

* Tue Sep 10 2013 Michael Schwendt <mschwendt@fedoraproject.org> - 20130823-3
- correct pmtools obs_ver

* Tue Aug 27 2013 Al Stone <ahs3@redhat.com> - 20130823-2
- Add in a copy of the GPLv2 text in order to comply with the requirement
  to always redistribute the terms of the license.

* Mon Aug 26 2013 Al Stone <ahs3@redhat.com> - 20130823-1
- Update to latest upstream source.

* Tue Aug 20 2013 Al Stone <ahs3@redhat.com> - 20130725-2
- Fix several rpmlint items (listed below)
- Add versions to explicit provides for acpixtract, acpidump
- Not all setup steps used -q
- Setup executable test script (run-misc-tests.sh) differently
- Removed unneeded commented out line with macros in it
- Removed mixed use of spaces and tabs (all spaces now)
- Corrected source URLs (upstream moved)

* Sun Aug 18 2013 Al Stone <ahs3@redhat.com> - 20130725-1
- Update to latest upstream source.

* Wed Jul 24 2013 Al Stone <ahs3@redhat.com> - 20130626-1
- Update to latest upstream source.
- Move acpidump to acpidump-acpica so it be an alternative properly
- Add basic man page for acpidump
- Enable use of AAPITS tests during the check step

* Sun Jun 02 2013 Al Stone <ahs3@redhat.com> - 20130517-2
- Correct an oversight: we provide an acpidump in conflict with the
  version in pmtools (which appears to be dead upstream) but had not
  made it an alternative before

* Tue May 28 2013 Al Stone <ahs3@redhat.com> - 20130517-1
- Update to latest upstream source.
- Remove acpica-tools-config.patch -- now in upstream
- Remove iasl-signed-char.patch -- now in upstream
- Updated debian-big_endian.patch
- Updated debian-unaligned.patch

* Mon May 13 2013 Al Stone <ahs3@redhat.com> - 20130328-1
- Update to latest upstream source.

* Wed Mar 20 2013 Al Stone <ahs3@redhat.com> - 20130214-2
- Incorporate use of optflags macro in the build.
- Remove extraneous rm -rf of buildroot.
- Remove extraneous use of defattr in the files section.
- Incorporate use of parallel make.
- Remove extraneous use of the clean section.
- Use simpler globbing in the files section.
- Use simpler globbing in the install section.
- Remove obsolete git notes from README.Fedora.
- Remove ExcludeArch restrictions.

* Mon Feb 18 2013 Al Stone <ahs3@redhat.com> - 20130214-1
- New upstream.
- Remove most of the config file patch; still need to remove -m{32,64}.
- Clarify the licensing; this source is dual-licensed and is being released
  under the GPLv2 as allowed by the original Intel license.
- Redo the misc tests so they compare results properly.

* Wed Feb 06 2013 Al Stone <ahs3@redhat.com> - 20130117-6
- Added a zero-fill to a date used in comparing testing results so that the
  comparison would be correct on days numbered < 10.

* Thu Jan 31 2013 Al Stone <ahs3@redhat.com> - 20130117-5
- Simplify versioning scheme and revert to the original scheme in use by
  iasl, which is use the latest official tarball date (2013017) as the
  version and 1%%{?dist} as the release, to be incremented for packaging
  and bug fixes as needed.

* Wed Jan 30 2013 Al Stone <ahs3@redhat.com> - 20130117-4
- Do a little reset: go back to using just the original upstream tarball
  instead of the latest git; the snapshot approach was more complicated
  than needed.
- Upstream tarballs split commands from test suites, so had to add the
  test suite back in as another Source: file.
- Change versioning scheme to include the APCI specification level (5.0),
  the latest official tarball date (2013017) and a revision level  (the
  .1 at the end) for packaging and bug fixes as needed.
- Changed the License field to reflect the source tarball change; the release
  tarball is dual-licensed, Intel ACPI or GPLv2.
- Updated patches to apply cleanly as needed.
- Corrected Obsoletes and Provides version numbers.

* Mon Jan 28 2013 Al Stone <ahs3@redhat.com> - 20130117-3
- Reconcile Fedora and Debian patches to be as alike as possible

* Mon Jan 28 2013 Al Stone <ahs3@redhat.com> - 20130117-2
- Verify ExcludeArch restrictions -- the architectures excluded can have
  no use for these tools.  Hardware support for ACPI is simply not
  implemented for them.
- Corrected versioning to note this source came from a git pull.
- Add License file as upstream has not yet provided one (and has not for
  many years).
- Insert properly versioned Provides and Obsoletes for iasl.
- Corrected files to use man.1* (vs man.1.gz) to allow flexibility in the
  compression being used.

* Wed Jan 23 2013 Al Stone <ahs3@redhat.com> - 20130117-1
- Clone from the current iasl package, with the intent of replacing it
- Update source to latest upstream
- NB: ACPICA documentation would normally be included in a source tarball.
  But, since it is not clearly redistributable, it is not included in the
  source RPM for this package.
- Build all ACPICA tools, not just iasl (and hence the package replacement)
- Add in brief man pages
- Set up acpixtract from this package as an alternative to the same command
  in the pmtools package
- Run the check step once built

