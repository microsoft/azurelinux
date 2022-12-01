Vendor:         Microsoft Corporation
Distribution:   Mariner
Name:           perl-Net-DNS-Resolver-Programmable
Version:        0.009
Release:        9%{?dist}
Summary:        Programmable DNS resolver class for offline emulation of DNS
License:        GPLv2+ or Artistic
URL:            https://metacpan.org/release/Net-DNS-Resolver-Programmable
Source0:        https://cpan.metacpan.org/authors/id/B/BI/BIGPRESH/Net-DNS-Resolver-Programmable-%{version}.tar.gz#/perl-Net-DNS-Resolver-Programmable-%{version}.tar.gz
BuildArch:      noarch
# Module Build
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl%{?fedora:-interpreter}
BuildRequires:  perl(ExtUtils::MakeMaker)
# Module Runtime
BuildRequires:  perl(base)
BuildRequires:  perl(constant)
BuildRequires:  perl(Net::DNS) >= 0.69
BuildRequires:  perl(Net::DNS::Packet)
BuildRequires:  perl(Net::DNS::Resolver)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# Test Suite
BuildRequires:  perl(Test::More)
# Dependencies
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

%description
Net::DNS::Resolver::Programmable is a Net::DNS::Resolver descendant class
that allows a virtual DNS to be emulated instead of querying the real DNS.
A set of static DNS records may be supplied, or arbitrary code may be
specified as a means for retrieving DNS records, or even generating them
on the fly.

%prep
%setup -q -n Net-DNS-Resolver-Programmable-%{version}

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
%doc CHANGES README TODO
%{perl_vendorlib}/Net/
%{_mandir}/man3/Net::DNS::Resolver::Programmable.3*

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.009-9
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.009-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.009-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.009-6
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.009-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.009-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jun 29 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.009-3
- Perl 5.28 rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.009-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 10 2017 Paul Howarth <paul@city-fan.org> - 0.009-1
- Update to 0.009
  - BIGPRESH taking over maintainership of this seemingly orphaned but very
    useful distribution
  - Avoid deprecated make_query_packet() call (CPAN RT#109266)
  - Remove debian/ subdir (CPAN RT#108522)
  - Regenerate README via pod2readme
  - Fix version number in older changelog entry
  - Remove use of deprecated qv()
  - Import rcode list from Net::DNS (CPAN RT#96390)
  - Don't demand 5.10, work on perl ≥ 5.6
  - No taint mode flag in t/01-basic.t
  - Avoid problems with our $VERSION = '...' on one line
  - Fix handling pre-prepared ::Packet objects passed to send()
  - Additional tests
  - Add Scalar::Util to dependencies
  - Cleaner way to handle both arrays of strings and Net::DNS::Packet objects
    (CPAN RT#122542)
  - Extend tests to cover non-mocked queries too
- This release by BIGPRESH → update source URL
- Switch to ExtUtils::MakeMaker flow
- BR: perl-interpreter rather than perl on Fedora
- Drop legacy Group: tag
- Use %%license
- Make %%files list more explicit

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.003-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.003-26
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.003-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.003-24
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.003-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.003-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jun 05 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.003-21
- Perl 5.22 rebuild

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.003-20
- Perl 5.20 rebuild

* Thu Jul 24 2014 Petr Pisar <ppisar@redhat.com> - 0.003-19
- Do not use private Net::DNS API removed in Net-DNS-0.75 (bug #1099382)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.003-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.003-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 0.003-16
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.003-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Oct 23 2012 Petr Pisar <ppisar@redhat.com> - 0.003-14
- Change license to "GPLv2+ or Artistic" and remove unneeded dependencies

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.003-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 13 2012 Petr Pisar <ppisar@redhat.com> - 0.003-12
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.003-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 0.003-10
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.003-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 21 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.003-8
- 661697 rebuild for fixing problems with vendorach/lib

* Tue May 04 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.003-7
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.003-6
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.003-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.003-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Mar  5 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.003-3
- rebuild for new perl

* Wed Jul 11 2007 Steven Pritchard <steve@kspei.com> 0.003-2
- Rebuild.

* Tue Jul 10 2007 Steven Pritchard <steve@kspei.com> 0.003-1
- Specfile autogenerated by cpanspec 1.72.
- Add "v" to files and path names.
- Drop explicit redundant dependencies.
