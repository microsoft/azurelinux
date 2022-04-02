Summary:        Expect for Perl
Name:           perl-Expect
Version:        1.35
Release:        13%{?dist}
License:        GPL+ OR Artistic
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://metacpan.org/release/Expect
Source0:        https://cpan.metacpan.org/modules/by-module/Expect/Expect-%{version}.tar.gz#/perl-Expect-%{version}.tar.gz

BuildArch:      noarch

# Module Build
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  sed

# Module Runtime
BuildRequires:  perl(Carp)

# Test Suite
BuildRequires:  perl(Config)
BuildRequires:  perl(Errno)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.64
BuildRequires:  perl(Fcntl)
BuildRequires:  perl(File::Temp)
BuildRequires:  perl(IO::Handle)
BuildRequires:  perl(IO::Pty) >= 1.11
BuildRequires:  perl(IO::Tty) >= 1.11
BuildRequires:  perl(POSIX)
BuildRequires:  perl(Test::Builder)
BuildRequires:  perl(Test::More) >= 0.98
BuildRequires:  perl(strict)
BuildRequires:  perl(vars)
BuildRequires:  perl(warnings)

# Runtime
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

%description
This module provides Expect-like functionality to Perl. Expect is
a tool for automating interactive applications such as telnet, ftp,
passwd, fsck, rlogin, tip, etc.

%prep
%setup -q -n Expect-%{version}
sed -i 's|^#!/usr/local/bin/perl|#!/usr/bin/perl|' examples/kibitz/kibitz tutorial/[2-6].*
chmod -c a-x examples/ssh.pl examples/kibitz/kibitz tutorial/[2-6].*

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
%{_fixperms} -c %{buildroot}

%check
make test

%files
%license LICENSE
%doc Changes README.md examples/ tutorial/
%{perl_vendorlib}/Expect.pm
%{_mandir}/man3/Expect.3*

%changelog
* Fri Apr 01 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.35-13
- Cleaning-up spec. License verified.

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.35-12
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.35-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Aug 23 2019 Paul Howarth <paul@city-fan.org> - 1.35-10
- Use author-independent source URL

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.35-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.35-8
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.35-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.35-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.35-5
- Perl 5.28 rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.35-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.35-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.35-2
- Perl 5.26 rebuild

* Fri May 19 2017 Paul Howarth <paul@city-fan.org> - 1.35-1
- Update to 1.35
  - Official maintainer JACOBY (Dave Jacoby)
  - Added a MANIFEST so that "make dist" will work
  - Added AUTHOR key, listing all maintainers

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.33-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Jun 13 2016 Paul Howarth <paul@city-fan.org> - 1.33-1
- Update to 1.33
  - Remove dependency on Test::Exception
- This release by JACOBY → update source URL
- BR: perl-generators where available
- Package new LICENSE file

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.32-5
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.32-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.32-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jun 04 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.32-2
- Perl 5.22 rebuild

* Sun Oct 26 2014 Paul Howarth <paul@city-fan.org> - 1.32-1
- Update to 1.32
  - Skip bc tests (CPAN RT#98495)
- Classify buildreqs by usage

* Tue Sep 09 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.31-2
- Perl 5.20 mass

* Mon Sep  8 2014 Paul Howarth <paul@city-fan.org> - 1.31-1
- Update to 1.31
  - New co-maintainer (Gabor Szabo)
  - Merge .pod and .pm and move them to lib/
  - Move the test and the code to standard location /t in the distribution
  - Eliminate indirect calls in tests
  - Use Test::More instead of home-brew testing
  - Typos fixed in pod (CPAN RT#86852)
  - Changes file re-ordered and standardized
  - Refactored test script
  - Eliminate indirect calls in the code and in the docs
  - Use Perl::Tidy to unify layout
  - Added use warnings;
  - IO::Tty prerequisite version 1.03 → 1.11
  - More test diagnostics
  - Tests added for CPAN RT#62359
  - Skip the bc test on OS-es where it has been failing
  - Stop inheriting from Exporter
  - Eliminate $` and $' from the code (part of CPAN RT#61395); this fix might
    break some existing code in some extreme cases when the regex being matched
    has a lookbehind or a lookahead at the edges
  - Remove $& and $`, fixing the rest of CPAN RT#61395
  - Various code refactoring declaring loop variables, parameter passing,
    return undef, etc.
  - Croak if undef passed to _trim_length
  - Update documentation according to CPAN RT#60722
  - CPAN RT#47834: after a failed call to ->expect, the ->match and ->after
    will return undef and ->before will return the content of the accumulator;
    earlier they retained the values obtained during the last successful match
    (->before will return undef the first time but later, if we call
    ->clear_accum, it will start returning the empty string)
  - In the tests, add special treatment for $^O=midnightbsd and dragonfly, and
    for $^O=linux as well
  - Test t/11-calc.t also got some special treatment
- This release by SZABGAB → update source URL
- As we need Test::More ≳ 0.98, drop support for old distributions

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.21-18
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.21-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.21-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jul 18 2013 Petr Pisar <ppisar@redhat.com> - 1.21-15
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.21-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.21-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 12 2012 Petr Pisar <ppisar@redhat.com> - 1.21-12
- Perl 5.16 rebuild

* Mon Jan 23 2012 Paul Howarth <paul@city-fan.org> - 1.21-11
- Spec clean-up
  - Run the test suite in %%check now that it no longer breaks in mock
  - BR: perl(Carp), perl(Errno), perl(Exporter), perl(Fcntl), perl(IO::Handle)
    and perl(POSIX)
  - Make %%files list more explicit
  - Mark Expect.pod as %%doc
  - Use search.cpan.org source URL
  - Use DESTDIR rather than PERL_INSTALL_ROOT
  - Use %%{_fixperms} macro rather than our own chmod incantation
  - Don't use macros for commands
  - Use tabs

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.21-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Jun 23 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.21-9
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.21-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 16 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.21-7
- Rebuild to fix problems with vendorarch/lib (#661697)

* Sat May 01 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.21-6
- Mass rebuild with perl-5.12.0

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.21-5
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.21-4
- Rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.21-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.21-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Mar 05 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.21-1
- Update to 1.21

* Wed Mar 05 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.20-2
- Rebuild for new perl

* Mon Oct 15 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 1.20-1.1
- Correct license tag
- Add BR: perl(ExtUtils::MakeMaker)

* Fri Jul 21 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.20-1
- Update to 1.20

* Tue Jul 18 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.19-1
- Update to 1.19

* Tue Jul 11 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.18-1
- Update to 1.18

* Wed May 31 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.17-1
- Update to 1.17

* Tue May 16 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.16-2
- Description improved as suggested in #191622

* Mon May 08 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.16-1
- First build
