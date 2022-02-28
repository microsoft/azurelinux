Vendor:         Microsoft Corporation
Distribution:   Mariner
Name:           perl-Spiffy
Version:        0.46
Release:        17%{?dist}
Summary:        Framework for doing object oriented (OO) programming in Perl
License:        GPL+ or Artistic
URL:            https://metacpan.org/release/Spiffy
Source0:        https://cpan.metacpan.org/authors/id/I/IN/INGY/Spiffy-%{version}.tar.gz#/perl-Spiffy-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  perl-interpreter
BuildRequires:  perl-generators
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.30
# Run-time:
BuildRequires:  perl(Carp)
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(Filter::Util::Call)
BuildRequires:  perl(overload)
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
BuildRequires:  perl(YAML)
# Tests:
BuildRequires:  perl(base)
BuildRequires:  perl(Cwd)
BuildRequires:  perl(lib)
BuildRequires:  perl(Test::More)
# Release Tests:
BuildRequires:  perl(Test::Pod) >= 1.41
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:       perl(Data::Dumper)
Requires:       perl(Filter::Util::Call)
Requires:       perl(overload)
Requires:       perl(Scalar::Util)
Requires:       perl(warnings)
Requires:       perl(YAML)

# Filter bogus provide of perl(DB)
%global __provides_exclude %{?__provides_exclude:%__provides_exclude|}^perl\\(DB\\)

%description
"Spiffy" is a framework and methodology for doing object oriented (OO)
programming in Perl. Spiffy combines the best parts of Exporter.pm, base.pm,
mixin.pm and SUPER.pm into one magic foundation class. It attempts to fix all
the nits and warts of traditional Perl OO, in a clean, straightforward and
(perhaps someday) standard way.

%prep
%setup -q -n Spiffy-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;
%{_fixperms} $RPM_BUILD_ROOT/*

%check
make test RELEASE_TESTING=1

# Support use of %%license on old distributions
%{!?_licensedir:%global license %%doc}

%files
%license LICENSE
%doc Changes CONTRIBUTING README
%{perl_vendorlib}/Spiffy.pm
%doc %{perl_vendorlib}/Spiffy.pod
%{perl_vendorlib}/Spiffy/
%{_mandir}/man3/Spiffy.3pm*

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.46-17
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.46-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.46-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.46-14
- Perl 5.30 rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.46-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.46-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.46-11
- Perl 5.28 rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.46-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.46-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.46-8
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.46-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.46-6
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.46-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.46-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jun 05 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.46-3
- Perl 5.22 rebuild

* Tue Sep 09 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.46-2
- Perl 5.20 rebuild

* Tue Sep  9 2014 Paul Howarth <paul@city-fan.org> - 0.46-1
- Update to 0.46
  - Meta 0.0.2
  - Eliminate spurious trailing whitespace
  - Eliminate File::Basename from test/
  - Add t/000-compile-modules.t

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.42-2
- Perl 5.20 rebuild

* Sat Aug  9 2014 Paul Howarth <paul@city-fan.org> - 0.42-1
- Update to 0.42
  - Only support back to 5.8.1

* Thu Aug  7 2014 Paul Howarth <paul@city-fan.org> - 0.41-1
- Update to 0.41
  - Remove (c) from Copyright
  - Add badges to docs
  - Fix a bug that was causing lots of warnings in Test::Base on perl 5.21
  - Fix bad encoding in Pod

* Thu Jul 31 2014 Paul Howarth <paul@city-fan.org> - 0.37-1
- Update to 0.37
  - Update IRC in Meta

* Mon Jul 28 2014 Paul Howarth <paul@city-fan.org> - 0.36-1
- Update to 0.36
  - Fix email in Meta

* Tue Jul 22 2014 Paul Howarth <paul@city-fan.org> - 0.35-1
- Update to 0.35
  - Fix Meta and add Contributing
- Use %%license where possible

* Wed Jun 18 2014 Paul Howarth <paul@city-fan.org> - 0.32-1
- Update to 0.32
  - Release with Zilla::Dist
- Declare Spiffy.pod as %%doc

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.31-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.31-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 0.31-4
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.31-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Oct 29 2012 Petr Pisar <ppisar@redhat.com> - 0.31-2
- Package license

* Mon Oct 29 2012 Petr Pisar <ppisar@redhat.com> - 0.31-1
- 0.31 bump
- Modernize spec file

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.30-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 11 2012 Petr Pisar <ppisar@redhat.com> - 0.30-19
- Perl 5.16 rebuild
- Specify all dependencies

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.30-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.30-17
- Perl mass rebuild

* Tue Apr 19 2011 Paul Howarth <paul@city-fan.org> - 0.30-16
- Make the provides filter work with rpm 4.9 too

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.30-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 22 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.30-14
- Rebuild to fix problems with vendorarch/lib (#661697)

* Thu May 06 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.30-13
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.30-12
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.30-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.30-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Feb 02 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.30-9
- rebuild for new perl

* Wed Jan 02 2008 Ralf Corsépius <rc040203@freenet.de> 0.30-8
- Adjust License-tag.
- BR: perl(Test::More) (BZ 419631).

* Wed Apr 18 2007 Steven Pritchard <steve@kspei.com> 0.30-7
- Use fixperms macro instead of our own chmod incantation.
- BR ExtUtils::MakeMaker.

* Mon Sep 04 2006 Steven Pritchard <steve@kspei.com> 0.30-6
- Rework spec to look more like current cpanspec output.

* Tue Feb 28 2006 Steven Pritchard <steve@kspei.com> 0.30-5
- Improve filter.

* Mon Feb 27 2006 Steven Pritchard <steve@kspei.com> 0.30-4
- Drop dummy mixin.pm.

* Mon Feb 27 2006 Steven Pritchard <steve@kspei.com> 0.30-3
- Filter out Provides: perl(DB).

* Mon Feb 27 2006 Steven Pritchard <steve@kspei.com> 0.30-2
- Drop explicit Provides: mixin.
- Add dummy mixin.pm.
- Improve Summary.
- Fix Source0.

* Sat Feb 25 2006 Steven Pritchard <steve@kspei.com> 0.30-1
- Update to 0.30.
- Drop explicit perl BR.

* Wed Dec 28 2005 Steven Pritchard <steve@kspei.com> 0.24-1
- Specfile autogenerated.
