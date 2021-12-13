Vendor:         Microsoft Corporation
Distribution:   Mariner
# Perform optional tests
%bcond_without perl_Convert_ASN1_enables_optional_test

Summary:        ASN.1 encode/decode library
Name:           perl-Convert-ASN1
Version:        0.27
Release:        21%{?dist}
License:        GPL+ or Artistic
URL:            https://metacpan.org/release/Convert-ASN1
Source0:        https://cpan.metacpan.org/authors/id/G/GB/GBARR/Convert-ASN1-%{version}.tar.gz#/perl-Convert-ASN1-%{version}.tar.gz
# Correct shebangs in the tests
Patch0:         Convert-ASN1-0.27-Correct-shebangs-in-tests.patch
# Allow running tests from a read-only location,
# <https://github.com/gbarr/perl-Convert-ASN1/pull/40>
Patch1:         Convert-ASN1-0.27-Use-temporary-output-files-for-tests.patch
# Fix unsafe decoding in indef case,
# <https://github.com/gbarr/perl-Convert-ASN1/pull/15>
Patch2:         Convert-ASN1-0.27-CVE-2013-7488.patch
BuildArch:      noarch
BuildRequires:  coreutils
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# Run-time:
BuildRequires:  perl(:VERSION) >= 5.4
BuildRequires:  perl(Carp)
BuildRequires:  perl(constant)
BuildRequires:  perl(Encode)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(POSIX)
BuildRequires:  perl(Socket)
BuildRequires:  perl(Time::Local)
BuildRequires:  perl(utf8)
BuildRequires:  perl(vars)
# Optional run-time:
BuildRequires:  perl(bytes)
# Tests:
BuildRequires:  perl(File::Temp)
BuildRequires:  perl(IO::Socket)
BuildRequires:  perl(Math::BigInt) >= 1.997
%if %{with perl_Convert_ASN1_enables_optional_test}
# Optional tests:
BuildRequires:  perl(Data::Dumper)
%endif
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Suggests:       perl(bytes)
Requires:       perl(Carp)
Requires:       perl(Encode)
Requires:       perl(POSIX)
Requires:       perl(Time::Local)
Requires:       perl(utf8)

# Remove under-specified dependencies
%global __requires_exclude %{?__requires_exclude:%{__requires_exclude}|}^perl\\(Math::BigInt\\)$

%description
Convert::ASN1 encodes and decodes ASN.1 data structures using BER/DER rules.

%package tests
Summary:        Tests for %{name}
Requires:       %{name} = %{version}-%{release}
Requires:       perl-Test-Harness
Requires:       perl(Math::BigInt) >= 1.997
%if %{with perl_Convert_ASN1_enables_optional_test}
# Optional tests:
Requires:       perl(Data::Dumper)
%endif

%description tests
Tests from %{name}-%{version}. Execute them
with "%{_libexecdir}/%{name}/test".

%prep
%setup -q -n Convert-ASN1-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
chmod +x t/*.t

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%{make_build}

%install
%{make_install}
mkdir -p %{buildroot}/%{_libexecdir}/%{name}
cp -a t %{buildroot}/%{_libexecdir}/%{name}
cat > %{buildroot}/%{_libexecdir}/%{name}/test << 'EOF'
#!/bin/sh
cd %{_libexecdir}/%{name} && exec prove -I . -j "$(getconf _NPROCESSORS_ONLN)"
EOF
chmod +x %{buildroot}/%{_libexecdir}/%{name}/test
%{_fixperms} %{buildroot}/*

%check
unset YYDEBUG
make test

%files
%license LICENSE
%doc ChangeLog OldChanges README.md examples/
%{perl_vendorlib}/Convert/
%{_mandir}/man3/*.3pm*

%files tests
%{_libexecdir}/%{name}

%changelog
* Mon Nov 01 2021 Muhammad Falak <mwani@microsft.com> - 0.27-21
- Remove epoch

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.27-20
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Mon Nov 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 0.27-19
- Fix unsafe decoding in indef case (CVE-2013-7488)

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.27-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Oct 30 2019 Petr Pisar <ppisar@redhat.com> - 0.27-17
- Quote a substituted number of processors in the test script

* Wed Aug 28 2019 Petr Pisar <ppisar@redhat.com> - 0.27-16
- Modernize spec file
- Package upstream tests

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.27-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu May 30 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.27-14
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.27-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.27-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jun 27 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.27-11
- Perl 5.28 rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.27-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.27-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.27-8
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.27-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.27-6
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.27-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.27-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.27-3
- Perl 5.22 rebuild

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.27-2
- Perl 5.20 rebuild

* Mon Jun 30 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.27-1
- 0.27 bump

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.26-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.26-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jul 18 2013 Petr Pisar <ppisar@redhat.com> - 0.26-5
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.26-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.26-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 11 2012 Petr Pisar <ppisar@redhat.com> - 0.26-2
- Perl 5.16 rebuild

* Mon Jun 11 2012 Petr Pisar <ppisar@redhat.com> - 0.26-1
- 0.26 bump

* Mon May 07 2012 Petr Šabata <contyk@redhat.com> - 0.23-1
- 0.23 bump
- Modernize spec

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.22-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.22-6
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.22-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 15 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.22-4
- 661697 rebuild for fixing problems with vendorach/lib

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.22-3
- Mass rebuild with perl-5.12.0

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 0.22-2
- rebuild against perl 5.10.1

* Mon Jul 27 2009 Marcela Mašláňová <mmaslano@redhat.com> - 0.22-1
- update to 0.22

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.21-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.21-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Feb  8 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.21-3
- rebuild for new perl

* Mon Oct 15 2007 Tom "spot" Callaway <tcallawa@redhat.com> 0.21-2.1
- add BR: perl(ExtUtils::MakeMaker)

* Fri Aug 24 2007 Robin Norwood <rnorwood@redhat.com> - 0.21-2
- Fix license tag.

* Sat Feb  3 2007 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.21-1
- Update to 0.21.
- Corrected several changelog entries.
- Removed an explicit perl(Convert::ASN1) provides.

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 0.20-1.1
- rebuild

* Thu Mar 09 2006 Jason Vas Dias <jvdias@redhat.com> - 0.20-1
- upgrade to upstream version 0.20

* Fri Feb 03 2006 Jason Vas Dias <jvdias@redhat.com> - 0.19-1.2
- rebuild for new perl-5.8.8

* Fri Dec 16 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt for new gcc

* Wed Apr 20 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.19-1
- Update to 0.19. (#155458)
- Bring up to date with current Fedora.Extras perl spec template.

* Wed Sep 22 2004 Chip Turner <cturner@redhat.com> 0.18-3
- rebuild

* Wed Mar 10 2004 Chip Turner <cturner@redhat.com> - 0.18-1
- Specfile autogenerated.
