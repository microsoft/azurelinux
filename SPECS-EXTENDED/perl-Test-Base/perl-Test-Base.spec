Vendor:         Microsoft Corporation
Distribution:   Mariner
# Report a difference on string nonequivalnce
%bcond_without perl_Test_Base_enables_diff
# Run extra test
%bcond_without perl_Test_Base_enables_extra_test
# Enable getting documents by URLs
%bcond_without perl_Test_Base_enables_network

Name:           perl-Test-Base
Version:        0.89
Release:        8%{?dist}
Summary:        Data Driven Testing Framework
License:        GPL+ or Artistic
URL:            https://metacpan.org/release/Test-Base
Source0:        https://cpan.metacpan.org/authors/id/I/IN/INGY/Test-Base-%{version}.tar.gz#/perl-Test-Base-%{version}.tar.gz
BuildArch:      noarch
# Module Build
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.52
# Module Runtime
%if %{with perl_Test_Base_enables_diff}
BuildRequires:  perl(Algorithm::Diff) >= 1.15
%endif
BuildRequires:  perl(Carp)
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(File::Path)
BuildRequires:  perl(Filter::Util::Call)
%if %{with perl_Test_Base_enables_network}
# LWP::Simple not used at tests
%endif
BuildRequires:  perl(MIME::Base64)
BuildRequires:  perl(Scalar::Util) >= 1.07
BuildRequires:  perl(Spiffy) >= 0.40
BuildRequires:  perl(strict)
BuildRequires:  perl(Test::Deep)
BuildRequires:  perl(Test::More) >= 0.88
%if %{with perl_Test_Base_enables_diff}
BuildRequires:  perl(Text::Diff) >= 0.35
%endif
BuildRequires:  perl(warnings)
BuildRequires:  perl(YAML)
# Test Suite
BuildRequires:  perl(base)
BuildRequires:  perl(File::Find)
BuildRequires:  perl(lib)
BuildRequires:  perl(Test::Tester)
%if %{with perl_Test_Base_enables_extra_test}
# Release Tests
BuildRequires:  perl(Test::Pod) >= 1.41
%endif
# Dependencies
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
%if %{with perl_Test_Base_enables_diff}
Requires:       perl(Algorithm::Diff) >= 1.15
%endif
Requires:       perl(Data::Dumper)
Requires:       perl(File::Path)
Requires:       perl(Filter::Util::Call)
%if %{with perl_Test_Base_enables_network}
Requires:       perl(LWP::Simple)
%endif
Requires:       perl(MIME::Base64)
Requires:       perl(Scalar::Util) >= 1.07
Requires:       perl(Test::Deep)
Requires:       perl(Test::More) >= 0.88
%if %{with perl_Test_Base_enables_diff}
Requires:       perl(Text::Diff) >= 0.35
%endif
Requires:       perl(YAML)

%description
Testing is usually the ugly part of Perl module authoring. Perl gives you a
standard way to run tests with Test::Harness, and basic testing primitives
with Test::More. After that you are pretty much on your own to develop a
testing framework and philosophy. Test::More encourages you to make your
own framework by subclassing Test::Builder, but that is not trivial.

Test::Base gives you a way to write your own test framework base class that
*is* trivial.

%prep
%setup -q -n Test-Base-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
%{_fixperms} -c %{buildroot}

%check
make test %{?with_perl_Test_Base_enables_extra_test:RELEASE_TESTING=1}

%files
%license LICENSE
%doc Changes CONTRIBUTING README
%{perl_vendorlib}/Test/
%{_mandir}/man3/Test::Base.3*
%{_mandir}/man3/Test::Base::Filter.3*

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.89-8
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.89-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.89-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.89-5
- Perl 5.30 rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.89-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.89-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.89-2
- Perl 5.28 rebuild

* Fri Apr 20 2018 Paul Howarth <paul@city-fan.org> - 0.89-1
- Update to 0.89
  - Require Test::More ≥ 0.88 (GH#19)
  - Support the use of plain 'use Test::Base' without any tests (GH#21)
- Classify buildreqs by usage
- Drop legacy Group: tag
- Simplify find command using -delete

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.88-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.88-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jun 05 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.88-8
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.88-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon May 16 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.88-6
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.88-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.88-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.88-3
- Perl 5.22 rebuild

* Thu Aug 28 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.88-2
- Perl 5.20 rebuild

* Tue Aug 26 2014 Paul Howarth <paul@city-fan.org> - 0.88-1
- Update to 0.88
  - Add t/000-require-modules.t
  - Eliminate File::Basename from test/
  - Eliminate spurious trailing whitespace
  - Meta 0.0.2
  - Fix Meta error (s/zild/=zild/)
  - Unbundle Module::Install::TestBase
  - Fix failing t/diff_is.t (Issue/15)
  - Replace tabs with spaces

* Sat Aug  9 2014 Paul Howarth <paul@city-fan.org> - 0.79-1
- Update to 0.79
  - Change Provider test to use string eval, keeping it out of the eyes of
    Perl::Prereqs
  - Fix swim errors
  - Dep on EU::MM 6.52

* Thu Aug  7 2014 Paul Howarth <paul@city-fan.org> - 0.76-1
- Update to 0.76
  - Switch to Zilla-Dist
  - Add Algorithm::Diff and Text::Diff to test.requires
  - Fix copyright years
  - Remove (c) from Copyright
  - Switch docs to Swim
  - Add badges to docs
  - PR/11 and fixes
  - Add $VERSION back into Test::Base
  - Applied PR/4 from schwern++
  - Dep on new Spiffy-0.40 to get rid of warnings on blead 5.21.x
  - Use PR/14 which makes old and new Test::Builders work
  - Fix bad encoding in Pod
- Use %%license

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.62-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Feb 11 2014 Paul Howarth <paul@city-fan.org> - 0.62-1
- Update to 0.62
  - Fix bad skip counts in tests

* Mon Feb 10 2014 Paul Howarth <paul@city-fan.org> - 0.61-1
- Update to 0.61
  - Switch to dzil
- Package upstream's LICENSE file
- Make %%files list more explicit
- Run the pod test too
- Update dependencies
- Extend %%description a little

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.60-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Jul 20 2013 Petr Pisar <ppisar@redhat.com> - 0.60-8
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.60-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Nov 08 2012 Jitka Plesnikova <jplesnik@redhat.com> - 0.60-6
- Update dependencies
- Use DESTDIR rather than PERL_INSTALL_ROOT
- Don't use macros for commands
- Don't need to remove empty directories from the buildroot

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.60-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 13 2012 Petr Pisar <ppisar@redhat.com> - 0.60-4
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.60-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jun 29 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.60-2
- Perl mass rebuild

* Sat May 14 2011 Iain Arnell <iarnell@gmail.com> 0.60-1
- update to latest upstream version
- clean up spec for modern rpmbuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.59-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 22 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.59-2
- Rebuild to fix problems with vendorarch/lib (#661697)

* Mon Dec 13 2010 Steven Pritchard <steve@kspei.com> 0.59-1
- Update to 0.59.

* Thu May 06 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.58-4
- Mass rebuild with perl-5.12.0

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 0.58-3
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.58-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun May 17 2009 Steven Pritchard <steve@kspei.com> 0.58-1
- Update to 0.58.
- BR Test::Deep and Test::Tester.

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.55-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Dec 10 2008 Steven Pritchard <steve@kspei.com> 0.55-1
- Update to 0.55.
- Explicitly BR Test::More >= 0.62.
- BR YAML.

* Thu Mar 06 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.54-3
- Rebuild for new perl

* Sat Jul 07 2007 Steven Pritchard <steve@kspei.com> 0.54-2
- BR Test::More.

* Mon Jul 02 2007 Steven Pritchard <steve@kspei.com> 0.54-1
- Update to 0.54.

* Wed Apr 18 2007 Steven Pritchard <steve@kspei.com> 0.53-2
- BR ExtUtils::MakeMaker.

* Sat Dec 09 2006 Steven Pritchard <steve@kspei.com> 0.53-1
- Update to 0.53.
- Use fixperms macro instead of our own chmod incantation.

* Sat Sep 16 2006 Steven Pritchard <steve@kspei.com> 0.52-2
- Fix find option order.

* Sat Jul 01 2006 Steven Pritchard <steve@kspei.com> 0.52-1
- Update to 0.52.

* Mon May 08 2006 Steven Pritchard <steve@kspei.com> 0.50-2
- Add explicit dependencies for Text::Diff and LWP::Simple.

* Thu May 04 2006 Steven Pritchard <steve@kspei.com> 0.50-1
- Specfile autogenerated by cpanspec 1.65.
- Remove explicit BR: perl and Requires: perl(Spiffy).
