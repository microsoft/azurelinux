%if ! (0%{?rhel})
%{bcond_without perl_IO_Socket_INET6_enables_optional_test}
%else
%{bcond_with perl_IO_Socket_INET6_enables_optional_test}
%endif

Name:           perl-IO-Socket-INET6
Version:        2.73
Release:        9%{?dist}
Summary:        Perl Object interface for AF_INET|AF_INET6 domain sockets
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/IO-Socket-INET6
Source0:        https://cpan.metacpan.org/modules/by-module/IO/IO-Socket-INET6-%{version}.tar.gz
# Fix bad code in test. Original code hides error, related to BZ#1207174
Patch0:         IO-Socket-INET6-2.72-fix_die_in_test.patch
# Fix random test error in binding to socket BZ#1207174
Patch1:         IO-Socket-INET6-2.72-bz1207174-fix_random_test_error.patch
BuildArch:      noarch
# Module Build
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(ExtUtils::MakeMaker)
# Module Runtime
BuildRequires:  perl(Carp)
BuildRequires:  perl(Errno)
BuildRequires:  perl(IO::Socket)
BuildRequires:  perl(Socket)
BuildRequires:  perl(Socket6) >= 0.12
BuildRequires:  perl(strict)
# Test Suite
BuildRequires:  perl(Config)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(utf8)
BuildRequires:  perl(vars)
BuildRequires:  perl(warnings)
%if %{with perl_IO_Socket_INET6_enables_optional_test}
# Optional Tests
BuildRequires:  perl(Test::Pod) >= 1.14
BuildRequires:  perl(Test::Pod::Coverage) >= 1.04
BuildRequires:  perl(Test::TrailingSpace)
%endif
# Runtime

%description
Perl Object interface for AF_INET|AF_INET6 domain sockets.

%prep
%setup -q -n IO-Socket-INET6-%{version}
%patch -P0 -p1
%patch -P1 -p1

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
%doc ChangeLog README
%{perl_vendorlib}/IO/
%{_mandir}/man3/IO::Socket::INET6.3*

%changelog
* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.73-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.73-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.73-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Apr 18 2023 Michal Josef Špaček <mspacek@redhat.com> - 2.73-6
- Update license to SPDX format

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.73-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.73-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue May 31 2022 Jitka Plesnikova <jplesnik@redhat.com> - 2.73-3
- Perl 5.36 rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.73-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Dec 10 2021 Paul Howarth <paul@city-fan.org> - 2.73-1
- Update to 2.73
  - Deprecate in favour of IO::Socket::IP

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.72-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 2.72-24
- Perl 5.34 rebuild

* Tue May 18 2021 Michal Josef Špaček <mspacek@redhat.com> - 2.72-23
- Patch for bad code in test
- Patch for random test fail (BZ#1207174)

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.72-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jan 11 2021 Paul Howarth <paul@city-fan.org> - 2.72-21
- Spec tidy-up
  - Use author-independent source URL
  - Specify all build dependencies
  - Simplify find command using -delete
  - Fix permissions verbosely

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.72-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 2.72-19
- Perl 5.32 rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.72-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.72-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 2.72-16
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.72-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.72-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 2.72-13
- Perl 5.28 rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.72-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.72-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jun 05 2017 Jitka Plesnikova <jplesnik@redhat.com> - 2.72-10
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.72-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon May 16 2016 Jitka Plesnikova <jplesnik@redhat.com> - 2.72-8
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.72-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.72-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 2.72-5
- Perl 5.22 rebuild

* Thu May 21 2015 Paul Howarth <paul@city-fan.org> - 2.72-4
- Classify buildreqs by usage
- Use %%license

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 2.72-3
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.72-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Jan 31 2014 Paul Howarth <paul@city-fan.org> - 2.72-1
- Update to 2.72
  - Add minimum version of perl to 5.8.x
  - Add LICENSE file

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.71-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Jul 20 2013 Petr Pisar <ppisar@redhat.com> - 2.71-2
- Perl 5.18 rebuild

* Sun Jun 23 2013 Paul Howarth <paul@city-fan.org> - 2.71-1
- Update to 2.71 (typo fixes - CPAN RT#73143, CPAN RT#86344)

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.69-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Nov 15 2012 Petr Šabata <contyk@redhat.com> - 2.69-4
- Modernize the spec a bit and add Carp to BRs

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.69-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 12 2012 Petr Pisar <ppisar@redhat.com> - 2.69-2
- Perl 5.16 rebuild

* Thu Jan 12 2012 Paul Howarth <paul@city-fan.org> - 2.69-1
- Update to 2.69:
  - Solved symbol clashes in t/io_multihomed6.t (CPAN RT#72769)
  - Fix the imports on t/io_multihomed6.t (CPAN RT#72769)
  - Update the link to the repository in Build.PL
- BR: perl(IO::Socket)
- BR: perl(Socket)
- Use %%{_fixperms} macro instead of our own chmod incantation

* Wed Jul 27 2011 Petr Sabata <contyk@redhat.com> - 2.67-1
- 2.67 bump

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 2.66-3
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.66-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jan 13 2011 Paul Howarth <paul@city-fan.org> - 2.66-1
- Update to 2.66
  - Fix inet_pton/inet_ntop import warnings (CPAN RT#55901)
  - Fix listening on :: or 0.0.0.0 (CPAN RT#54656)
  - Add test listen_port_only.t
  - Solved problems with multihomed and family order (CPAN RT#57676)
  - Fix select timeout issue in t/io_multihomed6.t
  - Fix t/io_multihomed6.t on systems with broken getaddrinfo() (CPAN RT#58198)
  - Made the "use Socket" call import constants selectively, and not rely on
    @EXPORT's whims

* Thu Jan 13 2011 Paul Howarth <paul@city-fan.org> - 2.57-4
- s/PERL_INSTALL_ROOT/DESTDIR/
- re-enable the test suite
- BR: perl(Test::More), perl(Test::Pod), perl(Test::Pod::Coverage)

* Mon Dec 20 2010 Marcela Maslanova <mmaslano@redhat.com> - 2.57-3
- Rebuild to fix problems with vendorarch/lib (#661697)

* Sun May 02 2010 Marcela Maslanova <mmaslano@redhat.com> - 2.57-2
- Mass rebuild with perl-5.12.0

* Wed Jan 27 2010 Stepan Kasal <skasal@redhat.com> - 2.57-1
- new upstream version

* Wed Jan 27 2010 Stepan Kasal <skasal@redhat.com> - 2.56-4
- fix the source url

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 2.56-3
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.56-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Apr 13 2009 Warren Togami <wtogami@redhat.com> - 2.56-1
- 2.56

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.54-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Mar 26 2008 Warren Togami <wtogami@redhat.com> - 2.54-1
- 2.54

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.51-5
- Rebuild for perl 5.10 (again)

* Thu Jan 31 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.51-4
- rebuild for new perl

* Fri Nov 16 2007 Parag Nemade <panemade@gmail.com> - 2.51-3
- Merge Review(#226263) Spec cleanup

* Tue Oct 16 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 2.51-2.1
- correct license tag
- add BR: perl(ExtUtils::MakeMaker)

* Thu Jul 06 2006 Warren Togami <wtogami@redhat.com> 2.51-2
- minor spec fixes (#197821)

* Thu Jul 06 2006 Warren Togami <wtogami@redhat.com> 2.51-1
- initial Fedora package
