# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           perl-Socket6
Version:        0.29
Release: 27%{?dist}
Summary:        IPv6 related part of the C socket.h defines and structure manipulators
License:        BSD-3-Clause
URL:            https://metacpan.org/release/Socket6
Source0:        https://cpan.metacpan.org/modules/by-module/Socket6/Socket6-%{version}.tar.gz
Patch0:         Socket6-0.29-remove_support_of_gethostname2.patch
# Build:
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  perl-devel
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(Config)
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
# Module:
BuildRequires:  perl(base)
BuildRequires:  perl(Carp)
BuildRequires:  perl(DynaLoader)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(strict)
BuildRequires:  perl(vars)
# Tests:
BuildRequires:  perl(Socket)
BuildRequires:  perl(Test)
# Run-time:

# Filter the Perl extension module
%{?perl_default_filter}

%description
This module supports getaddrinfo() and getnameinfo() to intend to enable
protocol independent programming. If your environment supports IPv6, IPv6
related defines such as AF_INET6 are included.

%prep
%setup -q -n Socket6-%{version}
%patch -P0 -p1

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1 OPTIMIZE="%{optflags}"
%{make_build}

%install
%{make_install}
find %{buildroot} -type f -name '*.bs' -empty -delete
%{_fixperms} -c %{buildroot}

%check
make test

%files
%doc ChangeLog README gailookup.pl
%{perl_vendorarch}/Socket6.pm
%{perl_vendorarch}/auto/Socket6/
%{_mandir}/man3/Socket6.3*

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.29-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jul 07 2025 Jitka Plesnikova <jplesnik@redhat.com> - 0.29-25
- Perl 5.42 rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.29-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.29-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jun 10 2024 Jitka Plesnikova <jplesnik@redhat.com> - 0.29-22
- Perl 5.40 rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.29-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.29-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.29-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jul 11 2023 Jitka Plesnikova <jplesnik@redhat.com> - 0.29-18
- Perl 5.38 rebuild

* Thu Mar 23 2023 Michal Josef Špaček <mspacek@redhat.com> - 0.29-17
- Update license to SPDX format

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.29-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.29-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon May 30 2022 Jitka Plesnikova <jplesnik@redhat.com> - 0.29-14
- Perl 5.36 rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.29-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.29-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jul 07 2021 Michal Josef Spacek - 0.29-11
- Remove support of gethostbyname2

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 0.29-10
- Perl 5.34 rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.29-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.29-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jun 22 2020 Jitka Plesnikova <jplesnik@redhat.com> - 0.29-7
- Perl 5.32 rebuild

* Thu Feb 06 2020 Tom Stellard <tstellar@redhat.com> - 0.29-6
- Spec file cleanups: Use make_build and make_install macros, use NO_PACKLIST=1
  - https://docs.fedoraproject.org/en-US/packaging-guidelines/#_parallel_make
  - https://fedoraproject.org/wiki/Perl/Tips#ExtUtils::MakeMaker

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.29-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.29-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu May 30 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.29-3
- Perl 5.30 rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.29-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Oct  1 2018 Paul Howarth <paul@city-fan.org> - 0.29-1
- Update to 0.29
  - Socket6.xs: Update the tests for handling the correct headers on NetBSD
    and DragonFly BSD

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.28-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jun 27 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.28-7
- Perl 5.28 rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.28-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.28-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.28-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.28-3
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.28-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Jul 11 2016 Paul Howarth <paul@city-fan.org> - 0.28-1
- Update to 0.28
  - aclocal.m4 (IPv6_CHECK_INET_NTOP): inet_ntop(3) may return an
    IPv4-compatible IPv6 address (CPAN RT#113950)
- BR: perl-generators

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.27-2
- Perl 5.24 rebuild

* Wed Mar 23 2016 Paul Howarth <paul@city-fan.org> - 0.27-1
- Update to 0.27
  - t/use.t: We still support an environment where AF_INET6 is not defined

* Fri Mar 18 2016 Paul Howarth <paul@city-fan.org> - 0.26-1
- Update to 0.26
  - gailookup.pl.in: Add -P option to ease specification of port number
  - gailookup.pl.in: Add awareness of AI_ALL and AI_V4MAPPED
  - gailookup.pl.in: Add -r option to do reverse lookup
  - System inet_ntop broken in darwin (CPAN RT#113005)
  - Makefile.PL: Make Socket6 buildable on Android (CPAN RT#98181)
- Simplify find commands using -delete
- Explicitly BR: perl-devel, needed for EXTERN.h

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.25-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.25-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.25-6
- Perl 5.22 rebuild

* Thu May 21 2015 Paul Howarth <paul@city-fan.org> - 0.25-5
- Drop workaround for CPAN RT#66811, fixed upstream
- Tidy spec

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.25-4
- Perl 5.20 rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.25-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.25-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Feb 25 2014 Petr Šabata <contyk@redhat.com> - 0.25-1
- 0.25 bump
- Modernize the spec somewhat

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.23-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jul 18 2013 Petr Pisar <ppisar@redhat.com> - 0.23-14
- Perl 5.18 rebuild

* Fri Apr 19 2013 Petr Pisar <ppisar@redhat.com> - 0.23-13
- Produce manual pages (CPAN RT #66811)

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.23-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Aug 17 2012 Petr Pisar <ppisar@redhat.com> - 0.23-11
- Specify all dependencies

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.23-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 11 2012 Petr Pisar <ppisar@redhat.com> - 0.23-9
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.23-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.23-7
- Perl mass rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.23-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 22 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.23-5
- Rebuild to fix problems with vendorarch/lib (#661697)

* Thu May 06 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.23-4
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.23-3
- Rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.23-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Apr 13 2009 Warren Togami <wtogami@redhat.com> - 0.23-1
- 0.23

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Apr 22 2008 Robert Scheck <robert@fedoraproject.org> - 0.20-1
- Upgrade to 0.20 (#443497)

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.19-7
- Rebuild for perl 5.10 (again)

* Wed Feb 20 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.19-6
- Autorebuild for GCC 4.3

* Thu Jan 31 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.19-5
- rebuild for new perl

* Tue Oct 16 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 0.19-4.1
- add BR: perl(ExtUtils::MakeMaker)

* Tue Aug 21 2007 Warren Togami <wtogami@redhat.com> - 0.19-4
- rebuild

* Wed Jul 12 2006 Warren Togami <wtogami@redhat.com> - 0.19-3
- import into FC6

* Thu May 18 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.19-2
- License: BSD (http://www.opensource.org/licenses/bsd-license.php).

* Sat May 13 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.19-1
- First build.
