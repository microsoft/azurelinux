Vendor:         Microsoft Corporation
Distribution:   Mariner
Name:           perl-UNIVERSAL-can
Version:        1.20140328
Release:        17%{?dist}
Summary:        Hack around people calling UNIVERSAL::can() as a function
License:        GPL+ or Artistic
URL:            https://metacpan.org/release/UNIVERSAL-can
Source0:        https://cpan.metacpan.org/modules/by-module/UNIVERSAL/UNIVERSAL-can-%{version}.tar.gz#/perl-UNIVERSAL-can-%{version}.tar.gz
BuildArch:      noarch
# Build:
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.30
# Module:
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(strict)
BuildRequires:  perl(vars)
BuildRequires:  perl(warnings)
BuildRequires:  perl(warnings::register)
# Test Suite:
BuildRequires:  perl(lib)
BuildRequires:  perl(overload)
BuildRequires:  perl(Test::More)
# Dependencies:
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

%description
The UNIVERSAL class provides a few default methods so that all objects
can use them. Object orientation allows programmers to override these
methods in subclasses to provide more specific and appropriate behavior.

Some authors call methods in the UNIVERSAL class on potential invocants
as functions, bypassing any possible overriding. This is wrong and you
should not do it. Unfortunately, not everyone heeds this warning and
their bad code can break your good code.

%prep
%setup -q -n UNIVERSAL-can-%{version}

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
%doc Changes README
%{perl_vendorlib}/UNIVERSAL/
%{_mandir}/man3/UNIVERSAL::can.3*

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.20140328-17
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.20140328-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sun Oct 13 2019 Paul Howarth <paul@city-fan.org> - 1.20140328-15
- Spec tidy-up
  - Use author-independent source URL
  - Classify buildreqs by usage
  - Simplify find command using -delete
  - Don't need to remove empty directories from the buildroot
  - Fix permissions verbosely
  - Package LICENSE file
  - Make %%files list more explicit

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.20140328-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.20140328-13
- Perl 5.30 rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.20140328-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.20140328-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.20140328-10
- Perl 5.28 rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.20140328-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.20140328-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.20140328-7
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.20140328-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.20140328-5
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.20140328-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.20140328-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jun 05 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.20140328-2
- Perl 5.22 rebuild

* Fri Mar 27 2015 Tom Callaway <spot@fedoraproject.org> - 1.20140328-1
- update to 1.20140328

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.20120726-6
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.20120726-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.20120726-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Jul 20 2013 Petr Pisar <ppisar@redhat.com> - 1.20120726-3
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.20120726-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Jan 20 2013 Tom Callaway <spot@fedoraproject.org> 1.20120726-1
- update to 1.20120726

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.15-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 12 2012 Petr Pisar <ppisar@redhat.com> - 1.15-8
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.15-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.15-6
- Perl mass rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.15-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 23 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.15-4
- 661697 rebuild for fixing problems with vendorach/lib

* Fri May 07 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.15-3
- Mass rebuild with perl-5.12.0

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 1.15-2
- rebuild against perl 5.10.1

* Wed Oct  7 2009 Marcela Mašláňová <mmaslano@redhat.com> - 1.15-1
- update to new upstream release

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Mar  5 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.12-2
- rebuild for new perl

* Wed Apr  5 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.12-1
- Update to 1.12.

* Fri Feb 10 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.11-1
- Update to 1.11.
- No longer build requires perl(Test::Exception).

* Thu Feb  9 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.03-2
- Missing build requirement: perl(Test::Exception).

* Wed Feb  8 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.03-1
- Update to 1.03.

* Tue Dec 27 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.01-1
- First build.
