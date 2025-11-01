Name:           perl-Pod-Coverage-TrustPod
Version:        0.100006
Release:        1%{?dist}
Summary:        Allow a module's pod to contain Pod::Coverage hints
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://metacpan.org/release/Pod-Coverage-TrustPod
Source0:        https://cpan.metacpan.org/modules/by-module/Pod/Pod-Coverage-TrustPod-%{version}.tar.gz
BuildArch:      noarch
# Build:
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(:VERSION) >= 5.12
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.78
# Run-time:
BuildRequires:  perl(base)
BuildRequires:  perl(Pod::Coverage::CountParents)
BuildRequires:  perl(Pod::Eventual::Simple)
BuildRequires:  perl(Pod::Find)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# Tests:
BuildRequires:  perl(Carp::Heavy)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(lib)
BuildRequires:  perl(Test::More) >= 0.88
# Explicit dependencies:

%description
This is a Pod::Coverage subclass (actually, a subclass of
Pod::Coverage::CountParents) that allows the POD itself to declare certain
symbol names trusted.

%prep
%setup -q -n Pod-Coverage-TrustPod-%{version}

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
%{perl_vendorlib}/Pod/
%{_mandir}/man3/Pod::Coverage::TrustPod.3*

%changelog
* Mon Feb 27 2025 Sumit Jena <v-sumitjena@microsoft.com> - 0.100006-1
- Update to version 0.100006
- License verified

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.100005-9
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.100005-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Aug 24 2019 Paul Howarth <paul@city-fan.org> - 0.100005-7
- Use author-independent source URL

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.100005-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.100005-5
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.100005-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.100005-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.100005-2
- Perl 5.28 rebuild

* Mon Mar 12 2018 Paul Howarth <paul@city-fan.org> - 0.100005-1
- Update to 0.100005
  - Remove an accidentally-introduced // operator

* Mon Mar  5 2018 Paul Howarth <paul@city-fan.org> - 0.100004-1
- Update to 0.100004
  - Report more usefully when a regex can't be compiled
- Simplify find command using -delete

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.100003-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.100003-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jun 05 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.100003-7
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.100003-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.100003-5
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.100003-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.100003-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jun 05 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.100003-2
- Perl 5.22 rebuild

* Thu Nov 13 2014 Paul Howarth <paul@city-fan.org> - 0.100003-1
- Update to 0.100003
  - The string *EVERYTHING* is now a pattern meaning "trust everything"
  - Only anchor the regex from Pod; trustme regex are again non-anchored
- Use %%license
- Make %%files list more explicit

* Thu Aug 28 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.100002-9
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.100002-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.100002-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul 22 2013 Petr Pisar <ppisar@redhat.com> - 0.100002-6
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.100002-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Oct 25 2012 Petr Pisar <ppisar@redhat.com> - 0.100002-4
- Correct dependencies

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.100002-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 14 2012 Petr Pisar <ppisar@redhat.com> - 0.100002-2
- Perl 5.16 rebuild

* Sun Apr 22 2012 Iain Arnell <iarnell@gmail.com> 0.100002-1
- update to latest upstream version
- clean up spec for modern rpmbuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.100001-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jul 26 2011 Iain Arnell <iarnell@gmail.com> 0.100001-1
- update to latest upstream

* Thu Jul 21 2011 Petr Sabata <contyk@redhat.com> - 0.100000-3
- Perl mass rebuild

* Thu Jul 21 2011 Petr Sabata <contyk@redhat.com> - 0.100000-2
- Perl mass rebuild

* Sat Apr 09 2011 Iain Arnell <iarnell@gmail.com> 0.100000-1
- update to latest upstream version

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.092832-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Nov 19 2010 Iain Arnell <iarnell@gmail.com> 0.092832-1
- update to latest upstream version

* Tue May 04 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.092830-4
- Mass rebuild with perl-5.12.0

* Tue Feb 16 2010 Iain Arnell <iarnell@gmail.com> 0.092830-3
- use perl_default_filter
- use DESTDIR, not PERL_INSTALL_ROOT

* Wed Feb 03 2010 Iain Arnell <iarnell@gmail.com> 0.092830-2
- requires perl(Pod::Coverage::CountParents)

* Thu Jan 14 2010 Iain Arnell 0.092830-1
- Specfile autogenerated by cpanspec 1.78.
