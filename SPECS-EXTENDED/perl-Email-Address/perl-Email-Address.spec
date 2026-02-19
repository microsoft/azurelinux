Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Name:           perl-Email-Address
Version:        1.913
Release:        1%{?dist}
Summary:        RFC 2822 Address Parsing and Creation (DEPRECATED)
License:        GPL+ or Artistic
URL:            https://metacpan.org/release/Email-Address
Source0:        https://cpan.metacpan.org/modules/by-module/Email/Email-Address-%{version}.tar.gz#/perl-Email-Address-%{version}.tar.gz
BuildArch:      noarch
# Build
BuildRequires:  coreutils
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
# Module
BuildRequires:  perl(overload)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# Test Suite
BuildRequires:  perl(Encode)
BuildRequires:  perl(Encode::MIME::Header)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(Test::More) >= 0.88
BuildRequires:  perl(Time::HiRes)
# Dependencies
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

%description
This class implements a regex-based RFC 2822 parser that locates email
addresses in strings and returns a list of Email::Address objects found.
Alternatively you may construct objects manually. The goal of this software
is to be correct, and very very fast.

%prep
%setup -q -n Email-Address-%{version}
perl -pi -e 's|^#!/usr/local/bin/perl\b|#!%{__perl}|' bench/ea-vs-ma.pl


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
%doc Changes README bench/
%{perl_vendorlib}/Email/
%{_mandir}/man3/Email::Address.3*


%changelog
* Wed Dec 18 2024 Kevin Lockwood <v-klockwood@microsoft.com> - 1.913-1
- Update to 1.913
- License verified.

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.912-7
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.912-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Oct 16 2019 Paul Howarth <paul@city-fan.org> - 1.912-5
- Spec tidy-up
  - Use author-independent source URL
  - Classify buildreqs by usage
  - Use %%{make_build} and %%{make_install}
  - Fix permissions verbosely
  - Make %%files list more explicit

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.912-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.912-3
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.912-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Jan  2 2019 Tom Callaway <spot@fedoraproject.org> - 1.912-1
- update to 1.912
- fixes CVE-2015-7686 and CVE-2018-12558

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.909-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.909-2
- Perl 5.28 rebuild

* Fri Apr 13 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.909-1
- 1.909 bump

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.908-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.908-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.908-5
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.908-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.908-3
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.908-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Sep 24 2015 Tom Callaway <spot@fedoraproject.org> - 1.908-1
- update to 1.908

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.907-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jun 05 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.907-2
- Perl 5.22 rebuild

* Mon Feb  9 2015 Tom Callaway <spot@fedoraproject.org> - 1.907-1
- update to 1.907

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.905-2
- Perl 5.20 rebuild

* Fri Jun 20 2014 Tom Callaway <spot@fedoraproject.org> - 1.905-1
- update to 1.905

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.903-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Apr 22 2014 Tom Callaway <spot@fedoraproject.org> - 1.903-1
- update to 1.903

* Thu Feb 13 2014 Tom Callaway <spot@fedoraproject.org> - 1.901-1
- update to 1.901

* Fri Aug 16 2013 Tom Callaway <spot@fedoraproject.org> - 1.900-1
- update to 1.900

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.898-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Jul 20 2013 Petr Pisar <ppisar@redhat.com> - 1.898-3
- Perl 5.18 rebuild

* Wed Jun 26 2013 Jitka Plesnikova <jplesnik@redhat.com> - 1.898-2
- Specify all dependencies
- Drop %%defattr, remove %%clean section
- Don't need to remove empty directories from the buildroot
- Use DESTDIR rather than PERL_INSTALL_ROOT

* Fri Feb  8 2013 Tom Callaway <spot@fedoraproject.org> - 1.898-1
- update to 1.898

* Wed Dec 19 2012 Tom Callaway <spot@fedoraproject.org> - 1.897-1
- update to 1.897

* Tue Sep 18 2012 Marcela Mašláňová <mmaslano@redhat.com> 1.896-1
- update to 1.896

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.889-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 12 2012 Petr Pisar <ppisar@redhat.com> - 1.889-11
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.889-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.889-9
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.889-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 16 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.889-7
- 661697 rebuild for fixing problems with vendorach/lib

* Sat May 01 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.889-6
- Mass rebuild with perl-5.12.0

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.889-5
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.889-4
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.889-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.889-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Feb 12 2009 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.889-1
- Upstream update.

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.888-3
- Rebuild for perl 5.10 (again)

* Sun Jan 20 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.888-2
- rebuild for new perl

* Sat Jun 23 2007 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.888-1
- Update to 1.888.

* Thu Apr  5 2007 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.887-1
- Update to 1.887.

* Sun Mar 18 2007 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.886-1
- Update to 1.886.

* Tue Dec 12 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.884-1
- Update to 1.884.

* Sat Nov 25 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.883-1
- Update to 1.883.

* Wed Nov 22 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.882-1
- Update to 1.882.

* Sat Nov 11 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.880-1
- Update to 1.880.

* Fri Oct 13 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.871-1
- Update to 1.871.

* Sat Aug 12 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.870-1
- Update to 1.870.

* Sat Jul 22 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.86-1
- Update to 1.86.

* Tue Jul 11 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.85-1
- Update to 1.85.

* Thu Sep 08 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.80-1
- First build.
