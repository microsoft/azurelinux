# Run extra tests
%bcond_without perl_DateTime_Format_Mail_enables_extra_test

Name:           perl-DateTime-Format-Mail
Version:        0.403
Release:        13%{?dist}
Summary:        Convert between DateTime and RFC2822/822 formats
License:        GPL+ or Artistic        
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://metacpan.org/release/DateTime-Format-Mail            
Source0:        https://cpan.metacpan.org/authors/id/B/BO/BOOK/DateTime-Format-Mail-%{version}.tar.gz#/perl-DateTime-Format-Mail-%{version}.tar.gz
BuildArch:      noarch
# Build
BuildRequires:  coreutils
BuildRequires:  make
BuildRequires:  perl-interpreter
BuildRequires:  perl-generators
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# Runtime
BuildRequires:  perl(Carp)
BuildRequires:  perl(DateTime) >= 1.04
BuildRequires:  perl(Params::Validate)
BuildRequires:  perl(vars)
# Tests only
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(Test::More) >= 0.88
%if %{with perl_DateTime_Format_Mail_enables_extra_test}
# Author tests
BuildRequires:  perl(Pod::Coverage::TrustPod)
BuildRequires:  perl(Test::Pod) >= 1.41
BuildRequires:  perl(Test::Pod::Coverage) >= 1.08
# Release tests
BuildRequires:  perl(Test::CPAN::Meta)
%endif
# Dependencies
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

%description
RFCs 2822 and 822 specify date formats to be used by email. This module parses
and emits such dates.

RFC2822 (April 2001) introduces a slightly different format of date than that
used by RFC822 (August 1982). The main correction is that the preferred format
is more limited, and thus easier to parse programmatically.

Despite the ease of generating and parsing perfectly valid RFC822 and RFC2822
people still get it wrong. This module aims to correct that.

%prep
%setup -q -n DateTime-Format-Mail-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
%{_fixperms} %{buildroot}

%check
make test %{?with_perl_DateTime_Format_Mail_enables_extra_test:\
    AUTHOR_TESTING=1 RELEASE_TESTING=1}

%files
%license LICENSE
%doc CREDITS Changes README
%{perl_vendorlib}/DateTime/
%{_mandir}/man3/DateTime::Format::Mail.3*

%changelog
* Mon Nov 01 2021 Muhammad Falak <mwani@microsft.com> - 0.403-13
- Remove epoch

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1:0.403-12
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.403-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.403-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1:0.403-9
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.403-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.403-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jun 29 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1:0.403-6
- Perl 5.28 rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.403-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.403-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jun 06 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1:0.403-3
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.403-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jun 28 2016 Paul Howarth <paul@city-fan.org> - 1:0.403-1
- Update to 0.403
  - Use DateTime->set_locale instead of ->set to set the locale; using ->set
    may actually change the local time unintentionally (GH#2)
- Run the author and release tests too
- Make %%files list more explicit
- Update build dependencies and drop redundant requires filter

* Mon May 16 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1:0.402.0-3
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.402.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jul 23 2015 Petr Šabata <contyk@redhat.com> - 1:0.402.0-1
- 0.402 bump

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.401.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1:0.401.0-2
- Perl 5.22 rebuild

* Fri Dec 05 2014 Petr Pisar <ppisar@redhat.com> - 1:0.401.0-1
- 0.401 bump

* Fri Aug 29 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.3001-21
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3001-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3001-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 31 2013 Petr Pisar <ppisar@redhat.com> - 0.3001-18
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3001-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Dec 29 2012 Iain Arnell <iarnell@gmail.com> 0.3001-16
- gzip the sample dates file in documentation (rhbz#890441)
- update spec for modern rpmbuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3001-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 20 2012 Petr Pisar <ppisar@redhat.com> - 0.3001-14
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3001-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jul 20 2011 Iain Arnell <iarnell@gmail.com> - 0.3001-12
- update filtering macros for rpm 4.9

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 0.3001-11
- Perl mass rebuild

* Mon Feb 14 2011 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.3001-10
- Switch to using perl-filters/Abandon filter-requires.sh 
  (Work around mass rebuild breakdown).

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3001-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 16 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.3001-8
- 661697 rebuild for fixing problems with vendorach/lib

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.3001-7
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.3001-6
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3001-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3001-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.3001-3
- Rebuild for perl 5.10 (again)

* Fri Jan 25 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.3001-2
- no more notes/ directory

* Thu Jan 24 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.3001-1
- 0.3001
- fix license tag
- rebuild against new perl

* Thu Aug 31 2006 Chris Weyl <cweyl@alumni.drew.edu> 0.30-4
- bump for mass rebuild

* Sun Aug 06 2006 Chris Weyl <cweyl@alumni.drew.edu> 0.30-3
- bump for build and release

* Sun Aug 06 2006 Chris Weyl <cweyl@alumni.drew.edu> 0.30-2
- add missing br: perl(File::Find::Rule)
- additional files from the test suite added to %%doc

* Fri Aug 04 2006 Chris Weyl <cweyl@alumni.drew.edu> 0.30-1
- Initial spec file for F-E
