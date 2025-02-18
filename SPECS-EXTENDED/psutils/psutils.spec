# Unbundle gnulib
%bcond psutils_enables_unbundling_gnulib %{undefined rhel}

Name:       psutils
Version:    2.10
Release:    7%{?dist}
Summary:    PostScript utilities
# COPYING:          GPLv3 text
# epsffit.1:        GPLv3+
# epsffit.in.in:    GPLv3+
# extractres.in.in: psutils
# includeres.in.in: psutils
# psbook.1:         GPLv3+
# psbook.in.in:     GPLv3+
# psjoin.1:         GPLv3+
# psjoin.in.in:     GPLv3+
# psnup.in.in:      GPLv3+
# psresize.1:       GPLv3+
# psresize.in.in:   GPLv3+
# psselect.1:       GPLv3+
# psselect.in.in:   GPLv3+
# pstops.1:         GPLv3+
# pstops.in.in:     GPLv3+
# PSUtils.pm:       GPLv3+
# README:           GPLv3+
## In tests subpackage
# aclocal.m4:       FSFULLR
# build-aux/compile:        GPLv2+ with Autoconf exception
# build-aux/config.guess:   GPLv3+ with Autoconf exception
# build-aux/config.sub:     GPLv3+ with Autoconf exception
# build-aux/depcomp:        GPLv2+ with Autoconf exception
# build-aux/install-sh:     MIT
# build-aux/missing:        GPLv2+ with Autoconf exception
# build-aux/mdate-sh:       GPLv2+ with Autoconf exception
# build-aux/test-driver:    GPLv2+ with Autoconf exception
# build-aux/texinfo.tex:    GPLv3+ with TeX exception
# configure:                FSFULLR
# m4/00gnulib.m4:           FSFULLR
# m4/ax_check_gnu_make.m4:  FSFAP
# m4/gnulib-common.m4:      FSFULLR
# m4/gnulib-comp.m4:        GPLv3+ with Autoconf exception
# m4/relocatable-lib.m4:    FSFULLR
# Makefile.in:              FSFULLR
## Not in any binary package
# INSTALL:                  FSFAP
# old-scripts/fixwfwps:     See LICENSE
# pre-inst-env.in:          GPLv2+
License:    GPL-3.0-or-later
URL:        https://github.com/rrthomas/%{name}
Source:     %{url}/releases/download/v%{version}/%{name}-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  autoconf
BuildRequires:  automake >= 1.11
BuildRequires:  bash
# coreutils for chmod in Makefile.am
BuildRequires:  coreutils
# gcc is a default autoconf dependency and populates EXEEXT variable used in
# Makefile.am.
BuildRequires:  gcc
%if %{with psutils_enables_unbundling_gnulib}
BuildRequires:  gnulib-devel
%endif
BuildRequires:  grep
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  sed
# Run-time:
BuildRequires:  paper
BuildRequires:  perl-interpreter
BuildRequires:  perl(:VERSION) >= 5.14
BuildRequires:  perl(base)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(Fcntl)
BuildRequires:  perl(File::Basename)
BuildRequires:  perl(File::Copy)
BuildRequires:  perl(File::Spec::Functions)
BuildRequires:  perl(File::Temp)
BuildRequires:  perl(Getopt::Long)
BuildRequires:  perl(IPC::Run3)
BuildRequires:  perl(List::Util)
BuildRequires:  perl(POSIX)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# Tests:
BuildRequires:  diffutils
# Only for building
Provides:       bundled(gnulib)%(perl -ne 'if($. == 1 and /\A(\d+)-(\d+)-(\d+)/) {print qq{ = $1$2$3}}' %{_defaultdocdir}/gnulib/ChangeLog 2>/dev/null)
# psutils-perl was merged into psutils-2.03-1.fc34
Provides:       %{name}-perl = %{version}-%{release}
Obsoletes:      %{name}-perl < %{version}-%{release}
Requires:       paper

# Filter private modules
%global __requires_exclude %{?__requires_exclude:%{__requires_exclude}|}^perl\\(PSUtils\\)
%global __provides_exclude %{?__provides_exclude:%{__provides_exclude}|}^perl\\(PSUtils\\)

%description
Utilities for manipulating PostScript documents.
Page selection and rearrangement are supported, including arrangement into
signatures for booklet printing, and page merging for n-up printing.

%package tests
Summary:        Tests for %{name}
License:        GPLv3+ and FSFULLR and MIT and FSFAP
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       coreutils
Requires:       diffutils
Requires:       make

%description tests
Tests from %{name}. Execute them
with "%{_libexecdir}/%{name}/test".

%prep
%setup -q
%if %{with psutils_enables_unbundling_gnulib}
gnulib-tool --import --no-changelog relocatable-perl
%endif
autoreconf -fi

%build
%configure --disable-relocatable
%{make_build}
 
%install
%{make_install}
# Install tests
mkdir -p %{buildroot}%{_libexecdir}/%{name}
cp -a aclocal.m4 build-aux config.status configure configure.ac m4 Makefile* tests %{buildroot}%{_libexecdir}/%{name}
printf '#!/bin/sh\nexec "$@"\n' > %{buildroot}%{_libexecdir}/%{name}/pre-inst-env
chmod +x %{buildroot}%{_libexecdir}/%{name}/pre-inst-env
cat > %{buildroot}%{_libexecdir}/%{name}/test << 'EOF'
#!/bin/bash
set -e
# Makefile writes into CWD
DIR=$(mktemp -d)
cp -a %{_libexecdir}/%{name}/* "$DIR"
pushd "$DIR"
unset PSUTILS_UNINSTALLED
make -j "$(getconf _NPROCESSORS_ONLN)" check-TESTS
popd
rm -r "$DIR"
EOF
chmod +x %{buildroot}%{_libexecdir}/%{name}/test

%check
unset PSUTILS_UNINSTALLED
make check %{?_smp_mflags}

%files
%license COPYING
# ChangeLog is not helpful
# old-scripts excluded intentionally
%doc README
%{_bindir}/epsffit
%{_bindir}/extractres
%{_bindir}/includeres
%{_bindir}/psbook
%{_bindir}/psjoin
%{_bindir}/psnup
%{_bindir}/psresize
%{_bindir}/psselect
%{_bindir}/pstops
%{_datadir}/%{name}
%{_mandir}/man1/epsffit.1*
%{_mandir}/man1/extractres.1*
%{_mandir}/man1/includeres.1*
%{_mandir}/man1/psbook.1*
%{_mandir}/man1/psjoin.1*
%{_mandir}/man1/psnup.1*
%{_mandir}/man1/psresize.1*
%{_mandir}/man1/psselect.1*
%{_mandir}/man1/pstops.1*
%{_mandir}/man1/psutils.1*

%files tests
%{_libexecdir}/%{name}

%changelog
* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.10-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jul 03 2024 Ondřej Pohořelský <opohorel@redhat.com> - 2.10-6
- Don't copy configure~ into psutils-tests package

* Wed May 15 2024 Yaakov Selkowitz <yselkowi@redhat.com> - 2.10-5
- Use bundled gnulib on RHEL

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.10-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Feb 28 2023 Ondřej Pohořelský <opohorel@redhat.com> - 2.10-1
- 2.10 bump
- resolves: rhbz#2173614

* Fri Jan 20 2023 Ondřej Pohořelský <opohorel@redhat.com> - 2.09-1
- 2.09 bump
- resolves: rhbz#2035916

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.07-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.07-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.07-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Oct 26 2021 Ondřej Pohořelský <opohorel@redhat.com> - 2.07-1
- 2.07 bump
- Resolves: rhbz#2012555

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.06-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jun 01 2021 Ondřej Pohořelský <opohorel@redhat.com> - 2.06-1
- 2.06 bump

* Tue Apr 06 2021 Petr Pisar <ppisar@redhat.com> - 2.05-1
- 2.05 bump
- Package tests

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.04-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Nov 18 2020 Petr Pisar <ppisar@redhat.com> - 2.04-1
- 2.04 bump

* Fri Oct 02 2020 Petr Pisar <ppisar@redhat.com> - 2.03-1
- 2.03 bump

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.23-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.23-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.23-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.23-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.23-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.23-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.23-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.23-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.23-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.23-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.23-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri May 29 2015 Jiri Popelka <jpopelka@redhat.com> - 1.23-7
- Correctly parse paper sizes returned by paperconf (#1208985)

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.23-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.23-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Apr 23 2014 Jiri Popelka <jpopelka@redhat.com> - 1.23-4
- move psjoin to perl subpackage (#226324#c16)

* Thu Apr 10 2014 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.23-3
- Use /usr/bin/perl instead of /usr/bin/env perl.
- Add BR: perl(*).
- Use wildcards instead of hardcoded *.gz for man-pages.

* Tue Mar 04 2014 Jiri Popelka <jpopelka@redhat.com> - 1.23-2
- use paperconf instead of paper binary (#1072371)

* Wed Jan 22 2014 Jiri Popelka <jpopelka@redhat.com> - 1.23-1
- 1.23

* Tue Oct 22 2013 Jiri Popelka <jpopelka@redhat.com> - 1.21-1
- new upstream
- version 1.21

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.17-43
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Mar 26 2013 Jiri Popelka <jpopelka@redhat.com> - 1.17-42
- few usage/man page fixes

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.17-41
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Nov 29 2012 Jiri Popelka <jpopelka@redhat.com> - 1.17-40
- fix dist tag and URL
- put psutils-copyright.patch among sources as it's used only in
  psutils-remove-copyrighted-files
- no need to define BuildRoot and clean it in %%clean and %%install anymore
- %%defattr no longer needed in %%files

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.17-39
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.17-38
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.17-37
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jul 08 2010 Tomas Smetana <tsmetana@redhat.com> 1.17-36
- add the LICENSE file to the perl subpackage

* Thu Apr 22 2010 Daniel Novotny <dnovotny@redhat.com> 1.17-35
- renamed "clean" tarball to psutils-p17-clean.tar.gz 
  (merge review: #226324)

* Tue Jan 26 2010 Daniel Novotny <dnovotny@redhat.com> 1.17-34
- remove Apple copyrighted files (merge review: #226324)
- fixed URLs to upstream

* Mon Aug 10 2009 Ville Skyttä <ville.skytta@iki.fi> - 1.17-33
- Convert specfile to UTF-8.

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.17-32
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul 22 2009 Adam Jackson <ajax@redhat.com> 1.17-31
- Split perl scripts to a subpackage.

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.17-30
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Aug 29 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.17-29
- fix license tag

* Wed Feb 13 2008 Tomas Smetana <tsmetana@redhat.com> - 1.17-28
- rebuild (gcc-4.3)

* Tue Sep 18 2007 Martin Bacovsky <mbacovsk@redhat.com> - 1.17-27
- fixed Source url pointing to non-existing site

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.17-26.1
- rebuild

* Mon Jun 12 2006 Jitka Kudrnacova <jkudrnac@redhat.com> - 1.17-26
- new implementation of psmerge by Peter Williams

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.17-25.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.17-25.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Wed Mar 16 2005 Tim Waugh <twaugh@redhat.com> 1.17-25
- Rebuild for new GCC.

* Mon Jan 10 2005 Tim Waugh <twaugh@redhat.com> 1.17-24
- Manpage correction for psresize (bug #144582).

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Jun 17 2003 Tim Waugh <twaugh@redhat.com> 1.17-21
- Rebuilt.

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Wed Dec 11 2002 Tim Powers <timp@redhat.com> 1.17-18
- rebuild on all arches

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu Jun 20 2002 Than Ngo <than@redhat.com> 1.17-16
- Don't forcibly strip binaries

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu Jul 19 2001 Than Ngo <than@redhat.com> 1.17-13
- add patch from enrico.scholz@informatik.tu-chemnitz.de

* Fri Jul 13 2001 Than Ngo <than@redhat.com> 1.17-12
- media size as letter (Bug #48831)
- Copyright->License
- don't hardcode manpath

* Sun Jun 24 2001 Elliot Lee <sopwith@redhat.com>
- Bump release + rebuild.

* Fri Dec  8 2000 Tim Powers <timp@redhat.com>
- built for dist-7.1

* Mon Jul 24 2000 Prospector <prospector@redhat.com>
- rebuilt

* Mon Jul 10 2000 Tim Powers <timp@redhat.com>
- rebuilt

* Mon Jul 03 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Fri May 26 2000 Tim Powers <timp@redhat.com>
- man pages in /usr/share/man (FHS compliant location)
- grabbed spec from contrib
- initial build for Powertools

* Wed May 12 1999 Peter Soos <sp@osb.hu>
- Corrected the file and directory attributes to rebuild the package
  under RedHat Linux 6.0

* Fri Dec 25 1998 Peter Soos <sp@osb.hu>
- Corrected the file and directory attributes

* Tue Jun 23 1998 Peter Soos <sp@osb.hu>
- Using %%attr for ability to rebuild the package as an ordinary user.

* Wed Jun 04 1997 Timo Karjalainen <timok@iki.fi>
- Reverted back to un-gzipped man-pages (Redhat style)
- Added patch to compile everything cleanly
- Some minor changes to specfile

* Thu Mar 27 1997 Tomasz Kłoczko <kloczek@rudy.mif.pg.gda.pl>
  - new version:
    Patchlevel 17 had some minor bugfixes and improvements
    - Trailer information now put before %%EOF comments if no %%Trailer
    - psselect can now add blank pages.
    - Piped input works in Linux
    - spec file rewrited for using Buildroot,
    - man pages gziped.
