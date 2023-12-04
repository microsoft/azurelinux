# some arches don't have valgrind so we need to disable its support on them
# Note: ppc64 and ppc64le currently have broken valgrind:
# https://bugzilla.redhat.com/show_bug.cgi?id=1470030
%ifarch %{ix86} x86_64 ppc s390x %{arm} aarch64 ppc64 ppc64le
%global with_valgrind 1
%endif

Summary:        Trace memory leaks
Name:           perl-Test-LeakTrace
Version:        0.17
Release:        1%{?dist}
License:        GPL+ OR Artistic
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://metacpan.org/release/Test-LeakTrace
Source0:        https://cpan.metacpan.org/modules/by-module/Test/Test-LeakTrace-%{version}.tar.gz#/perl-Test-LeakTrace-%{version}.tar.gz
Source1:        LICENSE.PTR

# Module Build
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  perl-devel
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  sed
BuildRequires:  perl(Class::Struct)
BuildRequires:  perl(Data::Dumper)

# Module Runtime
BuildRequires:  perl(Exporter) >= 5.57
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(FindBin)
BuildRequires:  perl(Module::CoreList)
BuildRequires:  perl(Module::Install::AuthorTests)
BuildRequires:  perl(Module::Install::Repository)
BuildRequires:  perl(Test::Builder::Module)
BuildRequires:  perl(Test::More) >= 0.62
BuildRequires:  perl(XSLoader)

# Test Suite
BuildRequires:  perl(autouse)
BuildRequires:  perl(constant)
BuildRequires:  perl(inc::Module::Install)
BuildRequires:  perl(strict)
BuildRequires:  perl(threads)
BuildRequires:  perl(warnings)

# Extra Tests
%if !%{defined perl_bootstrap}
BuildRequires:  perl(Test::Pod) >= 1.14
BuildRequires:  perl(Test::Pod::Coverage) >= 1.04
BuildRequires:  perl(Test::Spellunker)
BuildRequires:  perl(Test::Synopsis)
%if 0%{?with_valgrind}
BuildRequires:  perl(Test::Valgrind)
%endif
%endif

# Runtime
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

# Don't provide private perl libs
%{?perl_default_filter}

%description
Test::LeakTrace provides several functions that trace memory leaks. This module
scans arenas, the memory allocation system, so it can detect any leaked SVs in
given blocks.

Leaked SVs are SVs that are not released after the end of the scope they have
been created. These SVs include global variables and internal caches. For
example, if you call a method in a tracing block, perl might prepare a cache
for the method. Thus, to trace true leaks, no_leaks_ok() and leaks_cmp_ok()
executes a block more than once.

%prep
%setup -q -n Test-LeakTrace-%{version}

# Remove redundant exec bits
chmod -c -x lib/Test/LeakTrace/Script.pm t/lib/foo.pl

# Fix up shellbangs in doc scripts
sed -i -e 's|^#!perl|#!/usr/bin/perl|' benchmark/*.pl example/*.{pl,t} {t,xt}/*.t

# Avoid bundled Module::Install and use the system version instead
rm -rf inc/
sed -i -e '/^inc\//d' MANIFEST

# Don't try to run the valgrind test whilst bootstrapping
%if %{defined perl_bootstrap} || ! 0%{?with_valgrind}
rm xt/05_valgrind.t
sed -i -e '/^xt\/05_valgrind\.t/d' MANIFEST
%endif

%build
perl Makefile.PL INSTALLDIRS=vendor OPTIMIZE="%{optflags}"
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name '*.bs' -empty -delete
%{_fixperms} -c %{buildroot}

cp %{SOURCE1} .

%check
make test

%files
%license LICENSE.PTR
%doc Changes README benchmark/ example/ %{?perl_default_filter:t/ xt/}
%{perl_vendorarch}/auto/Test/
%{perl_vendorarch}/Test/
%{_mandir}/man3/Test::LeakTrace.3*
%{_mandir}/man3/Test::LeakTrace::JA.3*
%{_mandir}/man3/Test::LeakTrace::Script.3*

%changelog
* Fri Oct 27 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 0.17-1
- Auto-upgrade to 0.17 - Azure Linux 3.0 - package upgrades

* Tue May 31 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.16-18
- Linted spec.

* Thu Jan 13 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.16-17
- License verified.

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.16-16
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.16-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.16-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Jun 02 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.16-13
- Perl 5.30 re-rebuild of bootstrapped packages

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.16-12
- Perl 5.30 rebuild

* Tue Apr  2 2019 Paul Howarth <paul@city-fan.org> - 0.16-11
- Re-enable valgrind on ppc64 and ppc64le (see #1470030)

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.16-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.16-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sun Jul 01 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.16-8
- Perl 5.28 re-rebuild of bootstrapped packages

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.16-7
- Perl 5.28 rebuild

* Thu Mar 15 2018 Paul Howarth <paul@city-fan.org> - 0.16-6
- Rebuild due to missing the boat for F-28 (#1556107)

* Tue Feb 20 2018 Paul Howarth <paul@city-fan.org> - 0.16-5
- Disable valgrind test on ppc64 and ppc64le until valgrind is working again
  (#1470030)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.16-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.16-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.16-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 18 2017 Paul Howarth <paul@city-fan.org> - 0.16-1
- Update to 0.16
  - Fix build and test issues with perl5.26 due to removal of . from @INC
    (CPAN RT#120420, GH#3)
- This release by LEEJO → update source URL
- Simplify find commands using -empty and -delete
- Drop EL-5 support
  - Drop BuildRoot: and Group: tags
  - Drop explicit buildroot cleaning in %%install section
  - Drop explicit %%clean section
  - BR: perl-devel unconditionally

* Wed Jun 07 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.15-12
- Perl 5.26 re-rebuild of bootstrapped packages

* Mon Jun 05 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.15-11
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.15-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed May 18 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.15-9
- Perl 5.24 re-rebuild of bootstrapped packages

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.15-8
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.15-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.15-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 10 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.15-5
- Perl 5.22 re-rebuild of bootstrapped packages

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.15-4
- Perl 5.22 rebuild

* Thu Jan 15 2015 Dan Horák <dan[at]danny.cz> - 0.15-3
- remove the valgrind test also when valgrind is missing

* Wed Nov 19 2014 Paul Howarth <paul@city-fan.org> - 0.15-2
- Re-enable pod spelling test

* Fri Nov 14 2014 Paul Howarth <paul@city-fan.org> - 0.15-1
- Update to 0.15
  - Fix test failure on Windows
    (https://github.com/gfx/p5-Test-LeakTrace/pull/1)
- Temporarily disable pod spelling test until a more up to date version of
  Spellunker is available

* Fri Sep 19 2014 Paul Howarth <paul@city-fan.org> - 0.14-13
- ppc64le and aarch64 have valgrind
- Drop obsoletes/provides for old -tests sub-package
- Avoid bundled Module::Install and use system version instead
- Classify buildreqs by usage

* Sun Sep 07 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.14-12
- Perl 5.20 re-rebuild of bootstrapped packages

* Fri Aug 29 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.14-11
- Perl 5.20 rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.14-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.14-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Mar 25 2014 Petr Pisar <ppisar@redhat.com> - 0.14-8
- Break build-cycle: perl-Test-LeakTrace → perl-Test-Spelling → perl-Pod-Spell
  → perl-File-SharedDir-ProjectDistDir → perl-Path-Tiny → perl-Unicode-UTF8
  → perl-Test-LeakTrace

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.14-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jul 25 2013 Petr Pisar <ppisar@redhat.com> - 0.14-6
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.14-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jul 18 2012 Dan Horák <dan[at]danny.cz> - 0.14-4
- valgrind is available only on selected arches and perl(Test::Valgrind) is noarch

* Mon Jun 18 2012 Petr Pisar <ppisar@redhat.com> - 0.14-3
- Perl 5.16 rebuild

* Thu May  3 2012 Paul Howarth <paul@city-fan.org> - 0.14-2
- BR: perl(Test::Valgrind) for additional test coverage

* Mon Mar 12 2012 Paul Howarth <paul@city-fan.org> - 0.14-1
- Update to 0.14
  - Fix Test::Valgrind failures
- Drop tests subpackage; move tests to main package documentation as long as
  we have %%{perl_default_filter} to avoid the resulting doc-file dependencies
- Run the release tests too, except for xt/05_valgrind.t since we don't have
  Test::Valgrind yet
- BR: perl(Test::Pod), perl(Test::Pod::Coverage), perl(Test::Spelling),
  aspell-en/hunspell-en and perl(Test::Synopsis) for the release tests
- Drop version requirement of perl(ExtUtils::MakeMaker) to 6.30, which works
  fine in EPEL-5
- Tidy %%description
- Make %%files list more explicit
- Package benchmark/ and example/ as documentation
- Drop explicit versioned requires of perl(Exporter) ≥ 5.57, satisfied by all
  supported distributions
- Don't need to remove empty directories from buildroot
- Don't use macros for commands
- Drop %%defattr, redundant since rpm 4.4
- Use tabs

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jun 15 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.13-3
- Perl mass rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Nov 17 2010 Paul Howarth <paul@city-fan.org> - 0.13-1
- Update to 0.13
  - Use ">= 0", instead of "== 0" for no_leaks_ok()
  - Add count_sv() to count all the SVs in a perl interpreter
  - Fix tests broken for some perls in 0.12

* Wed Nov 17 2010 Paul Howarth <paul@city-fan.org> - 0.11-1
- Update to 0.11 (#654301)
  - Fix false-positive related to XS code (CPAN RT #58133)

* Thu May 06 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.10-2
- Mass rebuild with perl-5.12.0

* Sun Apr 04 2010 Chris Weyl <cweyl@alumni.drew.edu> - 0.10-1
- Specfile by Fedora::App::MaintainerTools 0.006
