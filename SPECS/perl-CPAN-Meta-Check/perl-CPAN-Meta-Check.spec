Name:           perl-CPAN-Meta-Check
Summary:        Verify requirements in a CPAN::Meta object
Version:        0.018
Release:        1%{?dist}
License:        GPL+ OR Artistic
Group:          Development/Libraries
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://metacpan.org/release/CPAN-Meta-Check
Source0:        http://cpan.metacpan.org/authors/id/L/LE/LEONT/CPAN-Meta-Check-%{version}.tar.gz 
BuildArch:      noarch
# Build
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-generators
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
# Module
BuildRequires:  perl(base)
BuildRequires:  perl(CPAN::Meta::Prereqs) >= 2.132830
BuildRequires:  perl(CPAN::Meta::Requirements) >= 2.121
BuildRequires:  perl(Exporter)
BuildRequires:  perl(Module::Metadata) >= 1.000023
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# Test
%if %{with_check}
BuildRequires:  perl(CPAN::Meta) >= 2.120920
BuildRequires:  perl(Env)
BuildRequires:  perl(lib)
BuildRequires:  perl(Test::Deep)
BuildRequires:  perl(Test::More) >= 0.88
%endif

# Runtime
Requires:       perl

%description
This module verifies if requirements described in a CPAN::Meta object are
present.

%prep
%setup -q -n CPAN-Meta-Check-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}

%check
make test

%files
%license LICENSE
%doc Changes README
%{perl_vendorlib}/CPAN/
%{_mandir}/man3/CPAN::Meta::Check.3*

%changelog
* Mon Dec 18 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 0.018-1
- Auto-upgrade to 0.018 - Azure Linux 3.0 - package upgrades

* Wed Mar 02 2022 Muhammad Falak <mwani@microsoft.com> - 0.014-14
- Add an explicit BR on `perl(Test::Deep)` to enable ptest

* Wed Jan 19 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.014-13
- Adding BR on "perl-generators".

* Fri Jul 02 2021 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 0.014-12
- Initial CBL-Mariner import from Fedora 32 (license: MIT)
- License verified

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.014-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.014-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.014-9
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.014-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.014-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.014-6
- Perl 5.28 rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.014-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.014-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jun 05 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.014-3
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.014-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sat Nov 26 2016 Paul Howarth <paul@city-fan.org> - 0.014-1
- Update to 0.014
  - Undef versions are now passed through to CPAN::Meta::Requirements for the
    check, rather than failing with "Missing version" errors

* Thu Jul 21 2016 Paul Howarth <paul@city-fan.org> - 0.013-1
- Update to 0.013
  - Make tests more resilient against dev versions of dependencies
- BR: perl-generators
- Drop legacy Group: tag
- Take advantage of features in recent EU::MM to simplify flow

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.012-3
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.012-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jun 19 2015 Paul Howarth <paul@city-fan.org> - 0.012-1
- Update to 0.012
  - Drop dependency on Exporter 5.57

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.011-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.011-2
- Perl 5.22 rebuild

* Mon Mar 23 2015 Paul Howarth <paul@city-fan.org> - 0.011-1
- Update to 0.011
  - Declare the minimum version required for the "merged_requirements"
    interface
- Explicitly run the extra tests

* Mon Feb  2 2015 Paul Howarth <paul@city-fan.org> - 0.010-1
- Update to 0.010
  - Bump Module::Metadata prereq for $VERSION parsing (CPAN RT#101095)
  - Consistently require same version of CPAN::Meta::Requirements
- Use %%license

* Thu Aug 28 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.009-3
- Perl 5.20 rebuild

* Tue Jul  1 2014 Paul Howarth <paul@city-fan.org> - 0.009-2
- Always run the release tests (#1114859)

* Mon Jun 23 2014 Paul Howarth <paul@city-fan.org> - 0.009-1
- Update to 0.009
  - Various POD fixes

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.008-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Oct 17 2013 Paul Howarth <paul@city-fan.org> - 0.008-1
- Update to 0.008
  - Switch to using merged_requirements
  - Test Env instead of Carp for version overshoot (CPAN RT#89591)
  - Document $incdirs in the right function

* Wed Sep  4 2013 Paul Howarth <paul@city-fan.org> - 0.007-3
- Skip the release tests when bootstrapping

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.007-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 31 2013 Paul Howarth <paul@city-fan.org> - 0.007-1
- Update to 0.007
  - Swap conflicts test, as underscore versions broke it (CPAN RT#87438)

* Sat Jul 27 2013 Paul Howarth <paul@city-fan.org> - 0.006-1
- Update to 0.006
  - Fixed bad dereference during conflicts checking

* Tue Jul 23 2013 Petr Pisar <ppisar@redhat.com> - 0.005-3
- Perl 5.18 rebuild

* Wed May  1 2013 Paul Howarth <paul@city-fan.org> - 0.005-2
- Sanitize for Fedora submission

* Sat Apr 27 2013 Paul Howarth <paul@city-fan.org> - 0.005-1
- Initial RPM version
