%global cpan_version 0.111
Name:           perl-Data-Munge
Version:        0.111
Release:        1%{?dist}
Summary:        Utility functions for working with perl data structures and code references
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://metacpan.org/release/Data-Munge
Source0:        https://cpan.metacpan.org/modules/by-module/Data/Data-Munge-%{version}.tar.gz#/perl-Data-Munge-%{version}.tar.gz
BuildArch:      noarch
# build requirements
BuildRequires:  coreutils
BuildRequires:  make
BuildRequires:  perl-interpreter
BuildRequires:  perl-generators
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(File::Find)
BuildRequires:  perl(File::Spec)
# Run-time:
# Scalar::Util not used since perl 5.016
BuildRequires:  perl(Exporter)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# Tests:
BuildRequires:  perl(Test2::V0)
BuildRequires:  perl(Test::Pod)

%description
This module defines a few generally useful utility functions that process
perl data structures and code references.

%prep
%setup -q -n Data-Munge-%{cpan_version}

%build
/usr/bin/perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%{make_build}

%install
%{make_install}
%{_fixperms} $RPM_BUILD_ROOT/*

%check
%{make_build} test

%files
%doc Changes README
%{perl_vendorlib}/Data*
%{_mandir}/man3/Data*

%changelog
* Mon Mar 17 2025 Sumit Jena <v-sumitjena@microsoft.com> - 0.111-1
- Update to version 0.111
- License verified

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.097-11
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.097-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.097-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.097-8
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.097-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.097-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.097-5
- Perl 5.28 rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.097-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.097-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jun 05 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.097-2
- Perl 5.26 rebuild

* Tue Mar 21 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.097-1
- 0.097 bump

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.096-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.096-2
- Perl 5.24 rebuild

* Thu Mar 31 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.096-1
- 0.096 bump

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.095-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 25 2015 Petr Pisar <ppisar@redhat.com> - 0.095-1
- 0.095 bump

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.093-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.093-2
- Perl 5.22 rebuild

* Sat Jan 17 2015 David Dick <ddick@cpan.org> - 0.093-1
- Fix typo in synopsis

* Sat Nov 22 2014 David Dick <ddick@cpan.org> - 0.091-1
- Work around regex bug in perls < 5.18 that causes spurious test failures.

* Fri Oct 03 2014 David Dick <ddick@cpan.org> - 0.08-1
- Initial release
