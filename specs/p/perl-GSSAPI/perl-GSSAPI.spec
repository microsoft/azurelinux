# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

#
# Rebuild option:
#
#   --with testsuite         - run the test suite
#

Name:           perl-GSSAPI
Version:        0.28
Release: 51%{?dist}
Summary:        Perl extension providing access to the GSSAPIv2 library
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/GSSAPI
Source0:        https://cpan.metacpan.org/authors/id/A/AG/AGROLMS/GSSAPI-%{version}.tar.gz
# Fix a crash in gss_release_oid() when destructing out_mech (rhbz #1994263, CPAN RT#121873)
Patch0:         GSSAPI-0.28-Fix-a-crash-in-gss_release_oid-when-destructing-out_.patch
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  gcc
BuildRequires:  krb5-devel
BuildRequires:  make
BuildRequires:  perl-devel
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(Config)
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(Getopt::Long)
BuildRequires:  perl(strict)
BuildRequires:  which
# Run-time
%{?_with_testsuite:BuildRequires: perl(Carp)}
%{?_with_testsuite:BuildRequires: perl(constant)}
%{?_with_testsuite:BuildRequires: perl(Exporter)}
%{?_with_testsuite:BuildRequires: perl(overload)}
%{?_with_testsuite:BuildRequires: perl(warnings)}
%{?_with_testsuite:BuildRequires: perl(XSLoader)}
# Tests
%{?_with_testsuite:BuildRequires: perl(ExtUtils::testlib)}
%{?_with_testsuite:BuildRequires: perl(Test::More)}
# Optional tests
%{?_with_testsuite:BuildRequires: perl(Test::Pod) >= 1.00}

%description
This module gives access to the routines of the GSSAPI library, as
described in rfc2743 and rfc2744 and implemented by the Kerberos-1.2
distribution from MIT.

%prep
%setup -q -n GSSAPI-%{version}
%patch -P0 -p1
chmod -c a-x examples/*.pl

%build
perl Makefile.PL INSTALLDIRS=vendor OPTIMIZE="%{optflags}" NO_PACKLIST=1 NO_PERLLOCAL=1
%{make_build}

%install
%{make_install}
find %{buildroot} -type f -name '*.bs' -empty -delete
%{_fixperms} %{buildroot}/*

%check
# fails a couple of tests if network not available
%{?_with_testsuite:make test}

%files
%doc Changes README examples/
%{perl_vendorarch}/auto/*
%{perl_vendorarch}/GSSAPI*
%{_mandir}/man3/*

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.28-50
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jul 07 2025 Jitka Plesnikova <jplesnik@redhat.com> - 0.28-49
- Perl 5.42 rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.28-48
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.28-47
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jun 10 2024 Jitka Plesnikova <jplesnik@redhat.com> - 0.28-46
- Perl 5.40 rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.28-45
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.28-44
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.28-43
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jul 11 2023 Jitka Plesnikova <jplesnik@redhat.com> - 0.28-42
- Perl 5.38 rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.28-41
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.28-40
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon May 30 2022 Jitka Plesnikova <jplesnik@redhat.com> - 0.28-39
- Perl 5.36 rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.28-38
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Aug 19 2021 Jitka Plesnikova <jplesnik@redhat.com> - 0.28-25
- Fix a crash in gss_release_oid() when destructing out_mech

* Mon Aug 16 2021 Jitka Plesnikova <jplesnik@redhat.com> - 0.28-36
- Fix comparison of OID structure

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.28-35
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 0.28-34
- Perl 5.34 rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.28-33
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.28-32
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jun 22 2020 Jitka Plesnikova <jplesnik@redhat.com> - 0.28-31
- Perl 5.32 rebuild

* Tue Feb 04 2020 Tom Stellard <tstellar@redhat.com> - 0.28-30
- Spec file cleanups: Use make_build and make_install macros
- https://docs.fedoraproject.org/en-US/packaging-guidelines/#_parallel_make
- https://fedoraproject.org/wiki/Perl/Tips#ExtUtils::MakeMake

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.28-29
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.28-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu May 30 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.28-27
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.28-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.28-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jun 27 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.28-24
- Perl 5.28 rebuild

* Mon Feb 19 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.28-23
- Add build-require gcc

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.28-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.28-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.28-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.28-19
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.28-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.28-17
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.28-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.28-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.28-14
- Perl 5.22 rebuild

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.28-13
- Perl 5.20 rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.28-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.28-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.28-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 0.28-9
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.28-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Nov 06 2012 Petr Šabata <contyk@redhat.com> - 0.28-7
- Modernize the spec a bit and fix the deps

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.28-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 11 2012 Petr Pisar <ppisar@redhat.com> - 0.28-5
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.28-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Jun 19 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.28-3
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.28-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Dec 27 2010 Steven Pritchard <steve@kspei.com> 0.28-1
- Update to 0.28.

* Fri Dec 17 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.26-7
- 661697 rebuild for fixing problems with vendorach/lib

* Thu Jun  3 2010 Petr Pisar <ppisar@redhat.com> - 0.26-6
- Do not source /etc/profile.d/krb5-devel.sh as krb5-devel-1.8.1-6 does not
  provide it and places executables into standard PATH.

* Sun May 02 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.26-5
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.26-4
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.26-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.26-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu May 15 2008 Steven Pritchard <steve@kspei.com> 0.26-1
- Update to 0.26.
- Cleanup a little to more closely match cpanspec output.
- BR ExtUtils::MakeMaker.

* Mon Mar  3 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.24-6
- rebuild for new perl (again)

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.24-5
- Autorebuild for GCC 4.3

* Thu Feb 07 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.24-4
- rebuild for new perl

* Thu Jan 03 2008 Steven Pritchard <steve@kspei.com> 0.24-3
- Use sysconfdir macro instead of hard-coding /etc.

* Sat Dec 08 2007 Steven Pritchard <steve@kspei.com> 0.24-2
- Update License tag.
- Use fixperms macro instead of our own chmod incantation.
- Source in /etc/profile.d/krb5-devel.sh to get our path right.

* Thu Feb 22 2007 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.24-1
- Update to 0.24.

* Sun Sep 10 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.23-2
- Rebuild for FC6.

* Thu Aug  3 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.23-1
- Update to 0.23.

* Mon May 29 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.22-1
- Update to 0.22.

* Thu Apr  6 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.21-1
- Update to 0.21.

* Fri Mar 31 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.20-1
- First build.
