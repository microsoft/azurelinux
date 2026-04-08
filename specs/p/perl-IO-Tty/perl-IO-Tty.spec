# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           perl-IO-Tty
Version:        1.20
Release:        8%{?dist}
Summary:        Perl interface to pseudo tty's
License:        (GPL-1.0-or-later OR Artistic-1.0-Perl) AND BSD-2-Clause
URL:            https://metacpan.org/release/IO-Tty
Source0:        https://cpan.metacpan.org/modules/by-module/IO/IO-Tty-%{version}.tar.gz
# Module Build
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  perl-devel
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(Config)
BuildRequires:  perl(Cwd)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
# Module Runtime
BuildRequires:  perl(Carp)
BuildRequires:  perl(DynaLoader)
BuildRequires:  perl(IO::File)
BuildRequires:  perl(IO::Handle)
BuildRequires:  perl(POSIX)
BuildRequires:  perl(strict)
BuildRequires:  perl(vars)
BuildRequires:  perl(warnings)
# Test Suite
BuildRequires:  perl(Test::More)
# Dependencies
# (none)

# Don't "provide" private Perl libs
%{?perl_default_filter}

%description
IO::Tty and IO::Pty provide an interface to pseudo tty's.

%prep
%setup -q -n IO-Tty-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor OPTIMIZE="%{optflags}" NO_PACKLIST=1 NO_PERLLOCAL=1
%{make_build}

%install
%{make_install}
find %{buildroot} -type f -name '*.bs' -empty -delete
%{_fixperms} -c %{buildroot}

%check
make test

%files
%doc ChangeLog README
%{perl_vendorarch}/auto/IO/
%{perl_vendorarch}/IO/
%{_mandir}/man3/IO::Pty.3*
%{_mandir}/man3/IO::Tty.3*
%{_mandir}/man3/IO::Tty::Constant.3*

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.20-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jul 07 2025 Jitka Plesnikova <jplesnik@redhat.com> - 1.20-7
- Perl 5.42 rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.20-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.20-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jun 10 2024 Jitka Plesnikova <jplesnik@redhat.com> - 1.20-4
- Perl 5.40 rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.20-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.20-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Dec 29 2023 Paul Howarth <paul@city-fan.org> - 1.20-1
- Update to 1.20 (rhbz#2256127)
  - Remove --no-undefined from compiler test, which is not compatible with all
    platforms (GH#37)
  - Skip t/pty_get_winsize.t tests on AIX (GH#32)
  - Fix patchlevel check for util.h (GH#27)

* Tue Nov 28 2023 Paul Howarth <paul@city-fan.org> - 1.18-1
- Update to 1.18 (rhbz#2251844)
  - Address Freebsd build issue: make function checks more robust within
    shared lib (GH#35)

* Tue Nov 28 2023 Florian Weimer <fweimer@redhat.com> - 1.17-5
- Backport upstream patch to fix C99 compatibility issue

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.17-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jul 11 2023 Jitka Plesnikova <jplesnik@redhat.com> - 1.17-3
- Perl 5.38 rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.17-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sun Nov 13 2022 Paul Howarth <paul@city-fan.org> - 1.17-1
- Update to 1.17 (rhbz#2142173)
  - Switch changelog entries to MetaCPAN-friendly format
  - Fix printf format conversion specifiers in croak to support size_t on all
    platforms (GH#29)
  - Tty.pm: pre-allocate buffer for ioctl but leave it length 0 (GH#11, GH#30)
  - Use $arg to match @ARGV in Makefile.PL (GH#28)
- Use SPDX-format license tag

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.16-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon May 30 2022 Jitka Plesnikova <jplesnik@redhat.com> - 1.16-6
- Perl 5.36 rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.16-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.16-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 1.16-3
- Perl 5.34 rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.16-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Jan 22 2021 Paul Howarth <paul@city-fan.org> - 1.16-1
- Update to 1.16
  - Switch to GitHub for issue tracker
  - Switch to testsuite CI workflow
  - Tidy

* Wed Nov  4 2020 Paul Howarth <paul@city-fan.org> - 1.15-1
- Update to 1.15
  - Skip winsize test on Solaris and QNX NTO (GH#22)
  - Make function tests more robust (GH#24)
  - Work around a header name collision on util.h; this is breaking on recent
    OSX (GH#26)

* Sat Aug 22 2020 Paul Howarth <paul@city-fan.org> - 1.14-5
- Fix FTBFS due to false detection of strlcpy() and _getpty()
  https://github.com/toddr/IO-Tty/pull/24
- Modernize spec using %%{make_build} and %%{make_install}

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.14-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jun 22 2020 Jitka Plesnikova <jplesnik@redhat.com> - 1.14-3
- Perl 5.32 rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sun Jan 19 2020 Paul Howarth <paul@city-fan.org> - 1.14-1
- Update to 1.14
  - Remove MAP_TARGET from Makefile.PL (CPAN RT#91590)
  - Fix for Solaris setuid when root running as other user (CPAN RT#88271)
  - Add strict/warnings to Tty.pm
  - Fix pod errors
  - Typo: s/dependend/dependent/
  - Prevent spurious warning from get_winsize()
  - Fix usage of setsid
  - Github actions testing; Windows is off of course
  - Make README.md
- Use author-independent source URL
- Fix permissions verbosely

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.12-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu May 30 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.12-15
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.12-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.12-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jun 27 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.12-12
- Perl 5.28 rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.12-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.12-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.12-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.12-8
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.12-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sat May 14 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.12-6
- Perl 5.24 rebuild

* Wed Apr 20 2016 Paul Howarth <paul@city-fan.org> - 1.12-5
- Fix FTBFS due to missing buildreq perl-devel
- Simplify find commands using -empty and -delete

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.12-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.12-2
- Perl 5.22 rebuild

* Mon Sep 22 2014 Paul Howarth <paul@city-fan.org> - 1.12-1
- Update to 1.12
  - Add support for PERL_MM_OPT
  - Fix typo in compiler detection error message (CPAN RT#75649)
  - Fix "redefinition of typedef" errors with v5.19.4 and above
- Classify buildreqs by usage

* Tue Sep 09 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.11-2
- Perl 5.20 mass

* Mon Sep  8 2014 Paul Howarth <paul@city-fan.org> - 1.11-1
- Update to 1.11
  - Add get_winsize and set_winsize
  - Explicitly drop support for Win32 (CPAN RT#77813)
- Make %%files list more explicit

* Tue Aug 26 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.10-15
- Perl 5.20 rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 1.10-11
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Nov 26 2012 Petr Šabata <contyk@redhat.com> - 1.10-9
- Buildrequire perl(Cwd), simplify filters

* Thu Nov 15 2012 Petr Šabata <contyk@redhat.com> - 1.10-8
- Fix the dependencies
- Re-enable the test suite
- Modernize the spec
- Correct the license tag

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 08 2012 Petr Pisar <ppisar@redhat.com> - 1.10-6
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.10-4
- Perl mass rebuild

* Thu Jun 09 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.10-3
- Perl 5.14 mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 28 2010 Steven Pritchard <steve@kspei.com> 1.10-1
- Update to 1.10.
- Use fixperms macro instead of our own chmod incantation.
- Update Source0 URL.
- BR Test::More.

* Mon Dec 20 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.08-6
- 661697 rebuild for fixing problems with vendorach/lib

* Sun May 02 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.08-5
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.08-4
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.08-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat May 16 2009 Chris Weyl <cweyl@alumni.drew.edu> - 1.08-2
- filter out private Perl .so provides

* Wed Feb 25 2009 Paul Howarth <paul@city-fan.org> - 1.08-1
- Update to 1.08 (add support for posix_openpt())
- Fix argument order for find with -depth

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.07-5
- Rebuild for perl 5.10 (again)

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.07-4
- Autorebuild for GCC 4.3

* Mon Jan 28 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.07-3
- rebuild for new perl

* Tue Oct 16 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 1.07-2.1
- correct license tag
- add BR: perl(ExtUtils::MakeMaker)

* Sun Sep 10 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.07-2
- Rebuild for FC6.

* Fri Jul 21 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.07-1
- Update to 1.07.

* Tue Jul 18 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.06-1
- Update to 1.06.

* Sat Jun 10 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.05-1
- Update to 1.05.

* Wed May 31 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.04-1
- Update to 1.04.

* Tue May  9 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.03-1
- Update to 1.03.
- Taking maintainership.

* Tue Feb 14 2006 Ville Skyttä <ville.skytta at iki.fi> - 1.02-5
- Rebuild.

* Tue Jan 17 2006 Ville Skyttä <ville.skytta at iki.fi> - 1.02-4
- Rebuild, cosmetic cleanups.

* Wed Apr  6 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 1.02-3
- rebuilt

* Sun Feb  1 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:1.02-0.fdr.2
- Reduce directory ownership bloat.

* Fri Nov 21 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:1.02-0.fdr.1
- First build.
