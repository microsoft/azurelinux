Name:           perl-Return-MultiLevel
Version:        0.08
Release:        1%{?dist}
Summary:        Return across multiple call levels
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://metacpan.org/release/Return-MultiLevel
Source0:        https://cpan.metacpan.org/authors/id/P/PL/PLICEASE/Return-MultiLevel-%{version}.tar.gz
BuildArch:      noarch
# Build
BuildRequires:  coreutils
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
# Module
BuildRequires:  perl(Carp)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(parent)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# Test Suite
BuildRequires:  perl(Config)
BuildRequires:  perl(Test::Fatal)
BuildRequires:  perl(Test::More)
# Dependencies
# (none)
# Optional Functionality
BuildRequires:  perl(Scope::Upper) >= 0.29
Requires:       perl(Scope::Upper) >= 0.29

%description
This module provides a way to return immediately from a deeply nested call
stack. This is similar to exceptions, but exceptions don't stop automatically
at a target frame (and they can be caught by intermediate stack frames using
eval). In other words, this is more like setjmp(3)/longjmp(3) than die.

%prep
%autosetup -n Return-MultiLevel-%{version}

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
%doc Changes README
%{perl_vendorlib}/Return/
%{_mandir}/man3/Return::MultiLevel.3*

%changelog
* Fri Dec 26 2025 Aditya Singh <v-aditysing@microsoft.com> - 0.08-1
- Upgrade to version 0.08
- License verified.

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.05-10
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Mon Feb 17 2020 Paul Howarth <paul@city-fan.org> - 0.05-9
- Spec tidy-up
  - BR:/R: perl(Scope::Upper) for improved functionality
  - Classify buildreqs by usage
  - Use %%{make_build} and %%{make_install}
  - Fix permissions verbosely

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.05-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.05-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.05-6
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.05-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.05-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.05-3
- Perl 5.28 rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.05-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Sep 14 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.05-1
- 0.05 bump

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.04-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jun 05 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.04-7
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.04-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.04-5
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.04-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.04-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.04-2
- Perl 5.22 rebuild

* Fri Oct 03 2014 David Dick <ddick@cpan.org> - 0.04-1
- Initial release
