Vendor:         Microsoft Corporation
Distribution:   Mariner
Name:		perl-Devel-EnforceEncapsulation
Version:	0.51
Release:	18%{?dist}
Summary:	Find access violations to blessed objects
License:	GPL+ or Artistic
URL:		https://metacpan.org/release/Devel-EnforceEncapsulation
Source0:	https://cpan.metacpan.org/authors/id/C/CD/CDOLAN/Devel-EnforceEncapsulation-%{version}.tar.gz#/perl-Devel-EnforceEncapsulation-%{version}.tar.gz
BuildArch:	noarch
BuildRequires:	perl-generators
BuildRequires:	perl(Carp)
BuildRequires:	perl(English)
BuildRequires:	perl(ExtUtils::MakeMaker)
BuildRequires:	perl(Test::More)
BuildRequires:	perl(Test::Pod)
BuildRequires:	perl(Test::Pod::Coverage)
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

%description
Encapsulation is the practice of creating subroutines to access the properties
of a class instead of accessing those properties directly. The advantage of
good encapsulation is that the author is permitted to change the internal
implementation of a class without breaking its usage.

Object-oriented programming in Perl is most commonly implemented via blessed
hashes. This practice makes it easy for users of a class to violate
encapsulation by simply accessing the hash values directly. Although less
common, the same applies to classes implemented via blessed arrays, scalars,
filehandles, etc.

This module is a hack to block those direct accesses. If you try to access a
hash value of an object from its own class, or a superclass or subclass, all
goes well. If you try to access a hash value from any other package, an
exception is thrown. The same applies to the scalar value of a blessed scalar,
entry in a blessed array, etc.

To be clear: this class is NOT intended for strict enforcement of
encapsulation. If you want bullet-proof encapsulation, use inside-out objects
or the like. Instead, this module is intended to be a development or debugging
aid in catching places where direct access is used against classes implemented
as blessed hashes.

To repeat: the encapsulation enforced here is a hack and is easily
circumvented. Please use this module for good (finding bugs), not evil (making
life harder for downstream developers).

%prep
%setup -q -n Devel-EnforceEncapsulation-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} \;
%{_fixperms} %{buildroot}

%check
make test AUTHOR_TEST=1 AUTHOR_TEST_CDOLAN=1

%files
%doc CHANGES LICENSE README
%{perl_vendorlib}/Devel/
%{_mandir}/man3/Devel::EnforceEncapsulation.3pm*

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.51-18
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.51-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.51-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.51-15
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.51-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.51-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.51-12
- Perl 5.28 rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.51-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.51-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.51-9
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.51-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.51-7
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.51-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.51-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jun 05 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.51-4
- Perl 5.22 rebuild

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.51-3
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.51-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Mar 28 2014 Paul Howarth <paul@city-fan.org> - 0.51-1
- Update to 0.51
  - Fix for change in overload behavior in Perl 5.17 onwards (CPAN RT#77486)
- This release by CDOLAN -> update source URL

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.50-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Jul 20 2013 Petr Pisar <ppisar@redhat.com> - 0.50-10
- Perl 5.18 rebuild

* Wed Jul 17 2013 Paul Howarth <paul@city-fan.org> - 0.50-9
- Fix for change in overload behavior in Perl 5.17 onwards (CPAN RT#77486)
- Don't need to remove empty directories from the buildroot
- Drop %%defattr, redundant since rpm 4.4

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.50-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.50-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 12 2012 Petr Pisar <ppisar@redhat.com> - 0.50-6
- Perl 5.16 rebuild

* Wed Jan 11 2012 Paul Howarth <paul@city-fan.org> - 0.50-5
- BR: perl(Carp) and perl(English)

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.50-4
- Perl mass rebuild

* Mon Apr 11 2011 Paul Howarth <paul@city-fan.org> - 0.50-3
- Clean up for modern rpmbuild

* Mon Apr 11 2011 Paul Howarth <paul@city-fan.org> - 0.50-2
- Nobody else likes macros for commands

* Fri Mar 18 2011 Paul Howarth <paul@city-fan.org> - 0.50-1
- Initial RPM version
