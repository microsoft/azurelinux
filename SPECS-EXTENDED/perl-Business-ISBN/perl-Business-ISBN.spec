Vendor:         Microsoft Corporation
Distribution:   Mariner
Name:           perl-Business-ISBN
%global cpan_version 3.005
Version:        %(echo '%{cpan_version}' | tr '_' '.'})
Release:        3%{?dist}
Summary:        Perl module to work with International Standard Book Numbers

License:        Artistic 2.0
URL:            https://metacpan.org/release/Business-ISBN
Source0:        https://cpan.metacpan.org/authors/id/B/BD/BDFOY/Business-ISBN-%{cpan_version}.tar.gz#/perl-Business-ISBN-%{cpan_version}.tar.gz
BuildArch:      noarch
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl-interpreter
BuildRequires:  perl-generators
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(File::Spec::Functions)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# Test::Manifest 1.21 is optional
# Run-time:
BuildRequires:  perl(base)
BuildRequires:  perl(Business::ISBN::Data) >= 20191107
BuildRequires:  perl(Carp)
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(subs)
BuildRequires:  perl(vars)
# Optinonal run-time
BuildRequires:  perl(GD::Barcode::EAN13)
# Tests:
BuildRequires:  perl(Test::More) >= 0.95
# Optional tests:
BuildRequires:  perl(Test::Pod) >= 1.00
BuildRequires:  perl(Test::Pod::Coverage)
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:       perl(GD::Barcode::EAN13)

%description
This modules handles International Standard Book Numbers, including
ISBN-10 and ISBN-13.

%prep
%setup -q -n Business-ISBN-%{cpan_version}

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%{make_build}

%install
%{make_install}
%{_fixperms} -c $RPM_BUILD_ROOT/*

%check
make test

%files
%license LICENSE
%doc Changes README.pod
%{perl_vendorlib}/*
%{_mandir}/man3/*.3*

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.005-3
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.005-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Dec 12 2019 Jitka Plesnikova <jplesnik@redhat.com> - 3.005-1
- 3.005 bump

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.004-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 3.004-8
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.004-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.004-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 3.004-5
- Perl 5.28 rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.004-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.004-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jun 05 2017 Jitka Plesnikova <jplesnik@redhat.com> - 3.004-2
- Perl 5.26 rebuild

* Tue Apr 25 2017 Jitka Plesnikova <jplesnik@redhat.com> - 3.004-1
- 3.004 bump

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.003-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Sep 29 2016 Jitka Plesnikova <jplesnik@redhat.com> - 3.003-1
- 3.003 bump

* Wed Aug 10 2016 Jitka Plesnikova <jplesnik@redhat.com> - 3.002-1
- 3.002 bump

* Thu Jun 09 2016 Jitka Plesnikova <jplesnik@redhat.com> - 2.011-1
- 2.011 bump

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 2.010-3
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.010-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Dec 15 2015 Jitka Plesnikova <jplesnik@redhat.com> - 2.010-1
- 2.010 bump

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.09-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 10 2015 Jitka Plesnikova <jplesnik@redhat.com> - 2.09-6
- Perl 5.22 re-rebuild of bootstrapped packages

* Fri Jun 05 2015 Jitka Plesnikova <jplesnik@redhat.com> - 2.09-5
- Perl 5.22 rebuild

* Tue Sep 23 2014 Jitka Plesnikova <jplesnik@redhat.com> - 2.09-1
- 2.09 bump

* Sun Sep 07 2014 Jitka Plesnikova <jplesnik@redhat.com> - 2.07-4
- Perl 5.20 re-rebuild of bootstrapped packages

* Thu Aug 28 2014 Jitka Plesnikova <jplesnik@redhat.com> - 2.07-3
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.07-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Jan 06 2014 Jitka Plesnikova <jplesnik@redhat.com> - 2.07-1
- 2.07 bump

* Wed Aug 14 2013 Jitka Plesnikova <jplesnik@redhat.com> - 2.06-4
- Perl 5.18 re-rebuild of bootstrapped packages

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.06-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Jul 21 2013 Petr Pisar <ppisar@redhat.com> - 2.06-2
- Perl 5.18 rebuild

* Mon Jun 03 2013 Petr Pisar <ppisar@redhat.com> - 2.06-1
- 2.06 bump

* Wed Feb 27 2013 Paul Howarth <paul@city-fan.org> - 2.05.03-3
- Don't BR: perl(LWP::Simple) for optional tests when bootstrapping; this is a
  cleaner fix than nobbling perl-URI's runtime dependencies

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.05.03-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Oct 09 2012 Jitka Plesnikova <jplesnik@redhat.com> - 2.05.03-1
- 2.05_03 bump. Fix failing tests (RT#78671, RT#75686)

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.05-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 15 2012 Petr Pisar <ppisar@redhat.com> - 2.05-8
- Perl 5.16 rebuild
- Specify all dependencies

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.05-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 2.05-6
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.05-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 15 2010 Marcela Maslanova <mmaslano@redhat.com> - 2.05-4
- 661697 rebuild for fixing problems with vendorach/lib

* Thu Apr 29 2010 Marcela Maslanova <mmaslano@redhat.com> - 2.05-3
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 2.05-2
- rebuild against perl 5.10.1

* Mon Oct  5 2009 Stepan Kasal <skasal@redhat.com> - 2.05-1
- new upstream version

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.04_01-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.04_01-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Nov 24 2008 Stepan Kasal <skasal@redhat.com> - 2.04_01-1
- new upstream version
- drop integrated patch

* Thu Feb  7 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.03-4
- rebuild for new perl

* Fri Oct 26 2007 Robin Norwood <rnorwood@redhat.com> - 2.03-3
- Apply patch to fix barcode test

* Thu Oct 25 2007 Robin Norwood <rnorwood@redhat.com> - 2.03-2
- Fix buildrequires and doc list

* Thu Oct 25 2007 Robin Norwood <rnorwood@redhat.com> - 2.03-1
- Initial build
