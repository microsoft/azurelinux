%global __requires_exclude %{?__requires_exclude:%{__requires_exclude}|}^perl\\((MIME::QuotedPrint|Scalar::Util)\\)$
# Perform optional tests
%bcond_with perl_Bytes_Random_Secure_enables_optional_test

Summary:        Perl extension to generate cryptographically-secure random bytes
Name:           perl-Bytes-Random-Secure
Version:        0.29
Release:        21%{?dist}
License:        GPL+ OR Artistic
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://metacpan.org/release/Bytes-Random-Secure
Source0:        https://cpan.metacpan.org/modules/by-module/Bytes/Bytes-Random-Secure-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(:VERSION) >= 5.6

# Run-time:
BuildRequires:  perl(Carp)
BuildRequires:  perl(Crypt::Random::Seed)

# Tests:
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(English)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(List::Util)
BuildRequires:  perl(MIME::Base64)
BuildRequires:  perl(MIME::QuotedPrint) >= 3.03
BuildRequires:  perl(Math::Random::ISAAC)
BuildRequires:  perl(Scalar::Util) >= 1.21
BuildRequires:  perl(Test::More) >= 0.98
BuildRequires:  perl(Time::HiRes)
BuildRequires:  perl(constant)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)

%if !%{with perl_Bytes_Random_Secure_enables_optional_test}
BuildRequires:  coreutils
%endif
%if %{with perl_Bytes_Random_Secure_enables_optional_test}
# Optional tests:
# Pod::Coverage not used
BuildRequires:  perl(Statistics::Basic)
# Test::CheckManifest not used
# Test::CPAN::Changes not used
# Test::CPAN::Meta::JSON not used
# Test::CPAN::Meta::YAML not used
# Test::Kwalitee not used
# Test::Perl::Critic not used
# Test::Pod not used
# Test::Pod::Coverage
BuildRequires:  perl(Test::Warn)
%endif

Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:       perl(MIME::QuotedPrint) >= 3.03
Requires:       perl(Scalar::Util) >= 1.21

%description
Bytes::Random::Secure provides two interfaces for obtaining crypto-quality
random bytes. The simple interface is built around plain functions. For
greater control over the random number generator's seeding, there is an
object-oriented interface that provides much more flexibility.

%prep
%setup -q -n Bytes-Random-Secure-%{version}
%if !%{with perl_Bytes_Random_Secure_enables_optional_test}
rm t/21-bytes_random_tests.t
perl -i -ne 'print $_ unless m{^t/21-bytes_random_tests.t}' MANIFEST
%endif

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
%make_install
%{_fixperms} %{buildroot}/*

%check
unset RELEASE_TESTING
make test

%files
%license README
%doc Changes README examples
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Tue May 31 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.29-21
- Initial CBL-Mariner import from Fedora 34 (license: MIT).
- License verified.

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.29-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.29-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 0.29-18
- Perl 5.34 rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.29-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.29-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 0.29-15
- Perl 5.32 rebuild

* Tue Mar 10 2020 Petr Pisar <ppisar@redhat.com> - 0.29-14
- Modernize a spec file

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.29-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.29-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.29-11
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.29-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.29-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jun 29 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.29-8
- Perl 5.28 rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.29-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.29-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jun 05 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.29-5
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.29-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.29-3
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.29-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Oct 26 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.29-1
- 0.29 bump

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.28-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.28-2
- Perl 5.22 rebuild

* Sun Jan 18 2015 David Dick <ddick@cpan.org> - 0.28-1
- Initial release
