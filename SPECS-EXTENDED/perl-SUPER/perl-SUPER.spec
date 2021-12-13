Name:		perl-SUPER
Version:	1.20190531
Release:	5%{?dist}
Summary:	Sane superclass method dispatcher
License:	GPL+ or Artistic
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:		https://metacpan.org/release/SUPER
Source0:	https://cpan.metacpan.org/authors/id/C/CH/CHROMATIC/SUPER-%{version}.tar.gz#/perl-SUPER-%{version}.tar.gz
BuildArch:	noarch
# =============== Module Build =================
BuildRequires:	coreutils
BuildRequires:	findutils
BuildRequires:	make
BuildRequires:	perl-generators
BuildRequires:	perl-interpreter
BuildRequires:	perl(ExtUtils::MakeMaker)
# =============== Module Runtime ===============
BuildRequires:	perl(Carp)
BuildRequires:	perl(Scalar::Util) >= 1.20
BuildRequires:	perl(strict)
BuildRequires:	perl(Sub::Identify) >= 0.03
BuildRequires:	perl(warnings)
# =============== Test Suite ===================
BuildRequires:	perl(base)
BuildRequires:	perl(lib)
BuildRequires:	perl(Test::More) >= 0.88
# =============== Module Runtime ===============
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:	perl(Scalar::Util) >= 1.20
Requires:	perl(Sub::Identify) >= 0.03

%description
When subclassing a class, you occasionally want to dispatch control to the
superclass - at least conditionally and temporarily. This module provides
an easier, cleaner way for class methods to access their ancestor's
implementation.

%prep
%setup -q -n SUPER-%{version}

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
%if 0%{?_licensedir:1}
%license LICENSE
%else
%doc LICENSE
%endif
%doc Changes README
%{perl_vendorlib}/SUPER.pm
%{_mandir}/man3/SUPER.3*

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.20190531-5
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.20190531-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.20190531-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Jun 04 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.20190531-2
- Perl 5.30 re-rebuild updated packages

* Mon Jun  3 2019 Paul Howarth <paul@city-fan.org> - 1.20190531-1
- Update to 1.20190531
  - Allow main->SUPER::... to work when SUPER.pm is loaded (GH#1)

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.20141117-14
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.20141117-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.20141117-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.20141117-11
- Perl 5.28 rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.20141117-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.20141117-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.20141117-8
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.20141117-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Sep 27 2016 Paul Howarth <paul@city-fan.org> - 1.20141117-6
- Package LICENSE file
- Drop legacy spec file elements not needed for EL-6 onwards
- Simplify find command using -delete

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.20141117-5
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.20141117-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.20141117-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jun 05 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.20141117-2
- Perl 5.22 rebuild

* Mon Nov 17 2014 Paul Howarth <paul@city-fan.org> - 1.20141117-1
- Update to 1.20141117
  - Improved export mechanism
  - Removed useless Exporter tests
  - Improved docs (CPAN RT#79681)

* Mon Nov 17 2014 Paul Howarth <paul@city-fan.org> - 1.20141116-1
- Update to 1.20141116
  - Resolved Test::More changes (CPAN RT#97939)
- Switch to ExtUtils::MakeMaker flow

* Thu Aug 28 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.20120705-7
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.20120705-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.20120705-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jul 18 2013 Petr Pisar <ppisar@redhat.com> - 1.20120705-4
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.20120705-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.20120705-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jul  6 2012 Paul Howarth <paul@city-fan.org> - 1.20120705-1
- Update to 1.20120705
  - Resolved PAUSE packaging nit (CPAN RT#77110)
  - Converted to dzil
- Drop provides filter, not needed due to fix for CPAN RT#77110
- Classify buildreqs by what they are required for
- BR: perl(Test::Builder::Module) rather than perl(Test::Simple) ≥ 0.61
- BR: perl(base), perl(lib) and perl(Test::More)

* Tue Jun 12 2012 Petr Pisar <ppisar@redhat.com> - 1.17-8
- Perl 5.16 rebuild

* Tue Mar  6 2012 Paul Howarth <paul@city-fan.org> - 1.17-7
- Add provides filters that work with all supported distributions
- BR: perl(Carp) and perl(Exporter)
- Make %%files list more explicit
- Drop explicit requires of perl(Exporter) since it's auto-detected by rpm
  4.9 onwards, and is bundled with perl on all older distributions
- Don't need to remove empty directories from buildroot
- Don't use macros for commands
- %%defattr redundant since rpm 4.4
- Use tabs

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.17-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Jun 19 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.17-5
- Perl mass rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.17-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 22 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.17-3
- Rebuild to fix problems with vendorarch/lib (#661697)

* Thu May 06 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.17-2
- Mass rebuild with perl-5.12.0

* Sun Sep 27 2009 Chris Weyl <cweyl@alumni.drew.edu> - 1.17-1
- Update filtering
- Auto-update to 1.17 (by cpan-spec-update 0.01)
- Added a new br on perl(Scalar::Util) (version 1.20)
- Altered br on perl(Sub::Identify) (0 => 0.03)
- Altered br on perl(Test::Simple) (0 => 0.61)
- Added a new req on perl(Scalar::Util) (version 1.20)
- Added a new req on perl(Sub::Identify) (version 0.03)

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.16-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.16-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Mar 04 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.16-3
- Rebuild for new perl

* Wed Jan 02 2008 Ralf Corsépius <rc040203@freenet.de> - 1.16-2
- Adjust License-tag
- BR: perl(Test::Simple) (BZ 419631)

* Wed Apr 04 2007 Chris Weyl <cweyl@alumni.drew.edu> - 1.16-1
- Update to 1.16

* Tue Oct 03 2006 Chris Weyl <cweyl@alumni.drew.edu> - 1.15-1
- Update to 1.15
- Add explict requires on perl(Exporter); missed due to a use base construct

* Thu Sep 07 2006 Chris Weyl <cweyl@alumni.drew.edu> - 1.14-4
- Bump

* Thu Sep 07 2006 Chris Weyl <cweyl@alumni.drew.edu> - 1.14-3
- Update %%description and %%summary

* Thu Sep 07 2006 Chris Weyl <cweyl@alumni.drew.edu> - 1.14-2
- Filter errant perl(DB) provide

* Tue Sep 05 2006 Chris Weyl <cweyl@alumni.drew.edu> - 1.14-1
- Specfile autogenerated by cpanspec 1.69.1
