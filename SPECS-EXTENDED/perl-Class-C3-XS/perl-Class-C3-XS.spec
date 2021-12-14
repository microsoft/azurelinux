Name:		perl-Class-C3-XS
Version:	0.14
Release:	13%{?dist}
Summary:	XS speedups for Class::C3
License:	GPL+ or Artistic
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:		https://metacpan.org/release/Class-C3-XS
Source0:	https://cpan.metacpan.org/authors/id/E/ET/ETHER/Class-C3-XS-%{version}.tar.gz#/perl-Class-C3-XS-%{version}.tar.gz
# Module Build
BuildRequires:	coreutils
BuildRequires:	findutils
BuildRequires:	gcc
BuildRequires:	make
BuildRequires:	perl-interpreter

BuildRequires:	perl-devel

BuildRequires:	perl-generators
BuildRequires:	perl(ExtUtils::MakeMaker)
# Module Runtime
BuildRequires:	perl(strict)
BuildRequires:	perl(warnings)
BuildRequires:	perl(XSLoader)
# Test Suite
BuildRequires:	perl(base)
BuildRequires:	perl(File::Spec)
BuildRequires:	perl(Module::Metadata)
BuildRequires:	perl(Test::More)
# Optional Tests
BuildRequires:	perl(CPAN::Meta) >= 2.120900
BuildRequires:	perl(Sub::Name)
# Dependencies
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

# Avoid provides from private shared objects
%{?perl_default_filter}

%description
This contains XS performance enhancers for Class::C3 version 0.16 and
higher. The main Class::C3 package will use this package automatically if
it can find it. Do not use this package directly, use Class::C3 instead.

%prep
%setup -q -n Class-C3-XS-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name '*.bs' -empty -delete
%{_fixperms} %{buildroot}

%check
make test

%files
%if 0%{?_licensedir:1}
%license LICENCE
%else
%doc LICENCE
%endif
%doc Changes CONTRIBUTING README
%{perl_vendorarch}/auto/Class/
%{perl_vendorarch}/Class/
%{_mandir}/man3/Class::C3::XS.3*

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.14-13
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.14-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.14-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.14-10
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.14-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.14-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.14-7
- Perl 5.28 rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.14-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.14-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.14-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.14-3
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun Aug  7 2016 Paul Howarth <paul@city-fan.org> - 0.14-1
- Update to 0.14
  - Fix naming of test packages, now that . is no longer in @INC while base.pm
    is running (CPAN RT#116566, Perl RT#128769)
- This release by ETHER → update source URL
- Package new upstream LICENCE file

* Thu Aug  4 2016 Paul Howarth <paul@city-fan.org> - 0.13-22
- Avoid relying on . being in @INC (CPAN RT#116566)
- BR: perl-generators
- Simplify find commands using -empty and -delete

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.13-21
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.13-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jan 28 2016 Paul Howarth <paul@city-fan.org> - 0.13-19
- Spec clean-up
  - Classify buildreqs by usage
  - Don't ship the tests
  - Drop provides/requires filters as they're no longer needed
  - Drop %%defattr, redundant since rpm 4.4
  - Don't need to remove empty directories from the buildroot

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jun 05 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.13-17
- Perl 5.22 rebuild

* Thu Aug 28 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.13-16
- Perl 5.20 rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jul 18 2013 Petr Pisar <ppisar@redhat.com> - 0.13-12
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 11 2012 Petr Pisar <ppisar@redhat.com> - 0.13-9
- Perl 5.16 rebuild

* Wed Jan 18 2012 Paul Howarth <paul@city-fan.org> - 0.13-8
- BR: perl(Sub::Name) for testing
- Make %%files list more explicit
- Filter unwanted requires and provides
- Use DESTDIR rather than PERL_INSTALL_ROOT
- Use tabs

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.13-6
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 15 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.13-4
- Rebuild to fix problems with vendorarch/lib (#661697)

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.13-3
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.13-2
- Rebuild against perl 5.10.1

* Sat Sep 26 2009 Chris Weyl <cweyl@alumni.drew.edu> - 0.13-1
- Update filtering
- Auto-update to 0.13 (by cpan-spec-update 0.01)
- Altered br on perl(ExtUtils::MakeMaker) (0 => 6.42)

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Apr 02 2009 Chris Weyl <cweyl@alumni.drew.edu> - 0.11-1
- Update to 0.11

* Sat Feb 28 2009 Chris Weyl <cweyl@alumni.drew.edu> - 0.08-6
- Stripping bad provides of private Perl extension libs

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.08-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Mar  4 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.08-4
- Rebuild for new perl

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.08-3
- Autorebuild for GCC 4.3

* Tue Aug 21 2007 Chris Weyl <cweyl@alumni.drew.edu> - 0.08-2
- Bump

* Thu Aug 09 2007 Chris Weyl <cweyl@alumni.drew.edu> - 0.08-1
- Update to 0.08

* Thu May 31 2007 Chris Weyl <cweyl@alumni.drew.edu> - 0.06-1
- Update to 0.06

* Sun May 13 2007 Chris Weyl <cweyl@alumni.drew.edu> - 0.04-1
- Update to 0.04

* Wed May 09 2007 Chris Weyl <cweyl@alumni.drew.edu> - 0.03-2
- Bump

* Wed May 09 2007 Chris Weyl <cweyl@alumni.drew.edu> - 0.03-1
- Update to 0.03

* Fri May 04 2007 Chris Weyl <cweyl@alumni.drew.edu> - 0.02-1
- Specfile autogenerated by cpanspec 1.71
