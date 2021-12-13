Vendor:         Microsoft Corporation
Distribution:   Mariner
Name:           perl-Business-ISBN-Data
Version:        20191107
Release:        3%{?dist}
Summary:        The data pack for Business::ISBN
License:        Artistic 2.0
URL:            https://metacpan.org/release/Business-ISBN-Data
Source0:        https://cpan.metacpan.org/authors/id/B/BD/BDFOY/Business-ISBN-Data-%{version}.tar.gz#/perl-Business-ISBN-Data-%{version}.tar.gz
Patch0:         Business-ISBN-Data-20120719-shellbang.patch
BuildArch:      noarch
# Module Build
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.64
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(Test::Manifest) >= 1.21
# Module Runtime
BuildRequires:  perl(Carp)
BuildRequires:  perl(File::Basename)
BuildRequires:  perl(File::Spec::Functions)
BuildRequires:  perl(strict)
BuildRequires:  perl(vars)
BuildRequires:  perl(warnings)
# Test Suite
BuildRequires:  perl(Test::More) >= 0.95
BuildRequires:  perl(Test::Pod) >= 1.00
BuildRequires:  perl(Test::Pod::Coverage)
# Runtime
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

%description
This is a data pack for Business::ISBN.  You can update
the ISBN data without changing the version of Business::ISBN.
Most of the interesting stuff is in Business::ISBN.

%prep
%setup -q -n Business-ISBN-Data-%{version}

# Fix shellbang and script permissions for make_data.pl
%patch0
chmod -c +x make_data.pl

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%{make_build}

%install
%{make_install}
%{_fixperms} %{buildroot}

%check
make test

%files
%license LICENSE
%doc Changes README.pod examples/ t/
%{perl_vendorlib}/Business/
%{_mandir}/man3/Business::ISBN::Data.3*

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 20191107-3
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 20191107-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Dec 12 2019 Jitka Plesnikova <jplesnik@redhat.com> - 20191107-1
- 20191107 bump

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 20140910.003-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 20140910.003-11
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 20140910.003-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 20140910.003-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 20140910.003-8
- Perl 5.28 rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 20140910.003-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 20140910.003-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jun 05 2017 Jitka Plesnikova <jplesnik@redhat.com> - 20140910.003-5
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 20140910.003-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 20140910.003-3
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 20140910.003-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Dec 16 2015 Paul Howarth <paul@city-fan.org> - 20140910.003-1
- Update to 20140910.003
  - Hide the Business::ISBN namespace
- Drop now-redundant provides filter

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20140910.002-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jun 05 2015 Jitka Plesnikova <jplesnik@redhat.com> - 20140910.002-2
- Perl 5.22 rebuild

* Tue Sep 23 2014 Paul Howarth <paul@city-fan.org> - 20140910.002-1
- Update to 20140910.002
  - Look in the current directory for RangeMessage.xml if it's not in other
    locations; this can help with various Perl app packagers (also try
    ISBN_RANGE_MESSAGE env var)

* Fri Sep 19 2014 Paul Howarth <paul@city-fan.org> - 20140910.001-1
- Update to 20140910.001
  - Update to the latest data (2014-09-10)
- Use %%license
- Classify buildreqs by usage
- Drop redundant LWP::Simple requires filter

* Thu Aug 28 2014 Jitka Plesnikova <jplesnik@redhat.com> - 20120719.001-6
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20120719.001-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20120719.001-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Jul 21 2013 Petr Pisar <ppisar@redhat.com> - 20120719.001-3
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20120719.001-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 26 2012 Paul Howarth <paul@city-fan.org> - 20120719.001-1
- Update to 20120719.001:
  - Require Test::More ≥ 0.95 for subtest support
  - No code or feature changes
- Bump Test::Manifest version requirement to 1.21
- Bump Test::More version requirement to 0.95
- Drop redundant buildreq perl(Test::Prereq)

* Tue Jul 24 2012 Paul Howarth <paul@city-fan.org> - 20120719-1
- Update to 20120719:
  - Support using data from RangeMessage.xml, so you can use the latest data
    from ISBN without updating this module
- Fix shellbang and permissions of make_data.pl script to placate rpmlint
- Filter dependency on perl(LWP::Simple), required only by make_data.pl script,
  not in normal operation
- Don't need to remove empty directories from the buildroot
- BR: perl(Carp), perl(File::Spec::Functions) and perl(Test::Manifest) ≥ 1.14
- BR: at least version 1.00 of perl(Test::Pod)

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20081208-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 13 2012 Petr Pisar <ppisar@redhat.com> - 20081208-9
- Perl 5.16 rebuild

* Fri Jan 20 2012 Paul Howarth <paul@city-fan.org> - 20081208-8
- Clean up for modern rpmbuild:
  - Drop BuildRoot specification
  - Drop %%clean section
  - Don't bother cleaning buildroot in %%install section
  - Make %%files list more explicit
  - Use DESTDIR rather than PERL_INSTALL_ROOT
  - Use %%{_fixperms} macro rather than our own chmod incantation
  - Replace provides filter with version that works with rpm ≥ 4.9
- Include tests as %%doc since they're referred to by examples/README

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20081208-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jun 21 2011 Marcela Mašláňová <mmaslano@redhat.com> - 20081208-6
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20081208-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 15 2010 Marcela Maslanova <mmaslano@redhat.com> - 20081208-4
- Rebuild to fix problems with vendorarch/lib (#661697)

* Thu Apr 29 2010 Marcela Maslanova <mmaslano@redhat.com> - 20081208-3
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 20081208-2
- rebuild against perl 5.10.1

* Mon Oct  5 2009 Stepan Kasal <skasal@redhat.com> - 20081208-1
- new upstream version

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20081020-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20081020-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Nov 24 2008 Stepan Kasal <skasal@redhat.com> - 20081020-1
- new upstream version

* Thu Feb  7 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.15-4
- rebuild for new perl

* Thu Nov 15 2007 Robin Norwood <rnorwood@redhat.com> - 1.15-3
- Should not provide perl(Business::ISBN)

* Thu Oct 25 2007 Robin Norwood <rnorwood@redhat.com> - 1.15-2
- Fix BuildRequires

* Thu Oct 25 2007 Robin Norwood <rnorwood@redhat.com> - 1.15-1
- Initial build
