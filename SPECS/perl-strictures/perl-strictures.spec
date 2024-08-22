# Run optional tests
%if ! (0%{?rhel})
%{bcond_without perl_strictures_enables_optional_test}
%else
%{bcond_with perl_strictures_enables_optional_test}
%endif

Name:           perl-strictures
Version:        2.000006
Release:        9%{?dist}
Summary:        Turn on strict and make most warnings fatal
License:        GPL+ or Artistic
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://metacpan.org/release/strictures
Source0:        https://cpan.metacpan.org/authors/id/H/HA/HAARG/strictures-%{version}.tar.gz#/perl-strictures-%{version}.tar.gz
BuildArch:      noarch
# Module Build
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(Text::ParseWords)
# Dependencies of bundled ExtUtils::HasCompiler
BuildRequires:  perl(base)
BuildRequires:  perl(Config)
BuildRequires:  perl(DynaLoader)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(File::Basename)
BuildRequires:  perl(File::Spec::Functions)
BuildRequires:  perl(File::Temp)
# Module Runtime
BuildRequires:  perl(Carp)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# Test Suite
BuildRequires:  perl(Cwd)
BuildRequires:  perl(File::Path)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(Test::More) >= 0.88
%if %{with perl_strictures_enables_optional_test}
# Optional Tests
BuildRequires:  perl(indirect)
BuildRequires:  perl(multidimensional)
BuildRequires:  perl(bareword::filehandles)
%endif
# Runtime
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:       perl(Carp)

%description
This package turns on strict and makes most warnings fatal.

%prep
%setup -q -n strictures-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%{make_build}

%install
%{make_install}
%{_fixperms} -c %{buildroot}

%check
make test

%files
%license LICENSE
%doc Changes README
%{perl_vendorlib}/strictures.pm
%{perl_vendorlib}/strictures/
%{_mandir}/man3/strictures.3*
%{_mandir}/man3/strictures::extra.3*

%changelog
* Thu Aug 22 2024 Neha Agarwal <nehaagrwal@microsoft.com> - 2.000006-9
- Promote package to Core repository.

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.000006-8
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.000006-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.000006-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 2.000006-5
- Perl 5.30 rebuild

* Mon Mar 11 2019 Jitka Plesnikova <jplesnik@redhat.com> - 2.000006-4
- 2.000006 bump

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.000005-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.000005-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 2.000005-2
- Perl 5.28 rebuild

* Mon Apr 23 2018 Jitka Plesnikova <jplesnik@redhat.com> - 2.000005-1
- Update to 2.000005

* Fri Apr 20 2018 Paul Howarth <paul@city-fan.org> - 2.000004-1
- Update to 2.000004
  - Update bundled ExtUtils::HasCompiler to 0.021
  - Update internal list of warnings (no behavior change)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.000003-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.000003-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 2.000003-4
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.000003-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 2.000003-2
- Perl 5.24 rebuild

* Tue Apr 19 2016 Paul Howarth <paul@city-fan.org> - 2.000003-1
- Update to 2.000003
  - Update bundled ExtUtils::HasCompiler to 0.013 to fix potential false
    negative (CPAN RT#113637)
  - List optional XS dependencies as suggests rather than recommends
    (CPAN RT#107393)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.000002-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Nov  5 2015 Paul Howarth <paul@city-fan.org> - 2.000002-1
- Update to 2.000002
  - Use ExtUtils::HasCompiler to detect compiler rather than ExtUtils::CBuilder
  - More comprehensive testing

* Mon Jun 29 2015 Paul Howarth <paul@city-fan.org> - 2.000001-1
- Update to 2.000001
  - Update for perl 5.22 warning categories
  - Avoid using goto &UNIVERSAL::VERSION on perl 5.8, since it segfaults some
    builds
  - Also detect development directories based on .bzr directory
  - Various test clean-ups
- Update %%summary and %%description to reflect that not all warnings are made
  fatal by this module

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.000000-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 2.000000-2
- Perl 5.22 rebuild

* Thu Feb 26 2015 Paul Howarth <paul@city-fan.org> - 2.000000-1
- Update to 2.000000
  - INCOMPATIBLE CHANGE:
    - strictures 2 fatalizes only a subset of warnings; some warning categories
      are not safe to catch, or just inappropriate to have fatal
    - Existing code looking like 'use strictures 1;' will continue to get the
      old behavior of fatalizing all errors; the new behavior will take effect
      when no version or version 2 is specified

* Sat Jan 31 2015 Paul Howarth <paul@city-fan.org> - 1.005006-1
- Update to 1.005006
  - Fix extra checks triggering on paths starting with t, xt, lib, or blib
    rather than only triggering on those directories
  - Avoid stat checks for VCS directories until we are in an appropriately
    named file
  - Various clean-ups in test files

* Fri Oct  3 2014 Paul Howarth <paul@city-fan.org> - 1.005005-1
- Update to 1.005005
  - Detect mercurial when checking for development trees
  - Avoid using constant.pm to save a bit of memory on older perls
  - Update to v2 metadata
  - Fix skip on old perl on test script
  - Extra prereqs will be listed as hard prerequisites if a compiler is
    available
  - Added support for PUREPERL_ONLY (CPAN RT#91407)
  - Fixed using strictures->VERSION to query the version (CPAN RT#92965)
  - Make sure meta files list extra modules as recommendations, not requirements
  - Include minimum perl version in metadata
- This release by HAARG → update source URL
- Make %%files list more explicit

* Fri Aug 29 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.004004-6
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.004004-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Aug 07 2013 Petr Pisar <ppisar@redhat.com> - 1.004004-4
- Perl 5.18 rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.004004-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.004004-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Dec 07 2012 Iain Arnell <iarnell@gmail.com> 1.004004-1
- update to latest upstream version

* Sun Sep 09 2012 Iain Arnell <iarnell@gmail.com> 1.004002-1
- update to latest upstream version

* Sat Jul 21 2012 Iain Arnell <iarnell@gmail.com> 1.004001-1
- update to latest upstream version

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.003001-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jun 23 2012 Petr Pisar <ppisar@redhat.com> - 1.003001-3
- Perl 5.16 rebuild

* Sat May 19 2012 Iain Arnell <iarnell@gmail.com> 1.003001-2
- buildrequire multidimensional and bareword::filehandes for additional testing

* Mon Apr 09 2012 Iain Arnell <iarnell@gmail.com> 1.003001-1
- update to latest upstream version

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.002002-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Oct 02 2011 Iain Arnell <iarnell@gmail.com> 1.002002-2
- better description

* Sun Oct 02 2011 Iain Arnell <iarnell@gmail.com> 1.002002-1
- Specfile autogenerated by cpanspec 1.79.
