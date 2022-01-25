Name:           perl-Module-CPANfile
Version:        1.1004
Release:        9%{?dist}
Summary:        Parse cpanfile
License:        GPL+ OR Artistic
Group:          Development/Libraries
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://metacpan.org/release/Module-CPANfile
Source0:        https://cpan.metacpan.org/authors/id/M/MI/MIYAGAWA/Module-CPANfile-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-generators
BuildRequires:  perl(base)
BuildRequires:  perl(Carp)
BuildRequires:  perl(Cwd)
BuildRequires:  perl(CPAN::Meta) >= 2.12091
BuildRequires:  perl(CPAN::Meta::Feature) >= 2.12091
BuildRequires:  perl(CPAN::Meta::Prereqs) >= 2.12091
BuildRequires:  perl(CPAN::Meta::Requirements)
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(parent)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# tests
BuildRequires:  perl(Exporter)
BuildRequires:  perl-File-pushd
BuildRequires:  perl(lib)
BuildRequires:  perl(POSIX)
BuildRequires:  perl(Test::More) >= 0.88

Requires:       perl(CPAN::Meta) >= 2.12091
Requires:       perl(CPAN::Meta::Prereqs) >= 2.12091
Requires:       perl(CPAN::Meta::Feature) >= 2.12091
Requires:       perl(Data::Dumper)
Requires:       perl(Pod::Usage)
Requires:       perl

%?perl_default_filter
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}perl\\(CPAN::Meta\\)$

%description
Module::CPANfile is a tool to handle cpanfile format to load application
specific dependencies, not just for CPAN distributions.

%prep
%setup -q -n Module-CPANfile-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1
make %{?_smp_mflags}

%install
make pure_install DESTDIR=$RPM_BUILD_ROOT
%{_fixperms} $RPM_BUILD_ROOT/*

%check
make test

%files
%license LICENSE
%doc Changes README
%{_bindir}/mymeta-cpanfile
%{_bindir}/cpanfile-dump
%{perl_vendorlib}/*
%{_mandir}/man1/mymeta-cpanfile*
%{_mandir}/man1/cpanfile-dump*
%{_mandir}/man3/*

%changelog
* Wed Jan 19 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.1004-9
- Adding 'BuildRequires: perl-generators'.

* Fri Jul 02 2021 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 1.1004-8
- Initial CBL-Mariner import from Fedora 32 (license: MIT)
- License verified

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1004-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1004-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.1004-5
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1004-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1004-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.1004-2
- Perl 5.28 rebuild

* Fri Apr 27 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.1004-1
- 1.1004 bump

* Mon Apr 23 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.1003-1
- 1.1003 bump

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1002-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1002-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.1002-4
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1002-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.1002-2
- Perl 5.24 rebuild

* Mon Feb 15 2016 Petr Pisar <ppisar@redhat.com> - 1.1002-1
- 1.1002 bump

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.1001-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Sep 07 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.1001-1
- 1.1001 bump

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1000-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.1000-2
- Perl 5.22 rebuild

* Fri Sep 19 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.1000-1
- 1.1000 bump

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.0001-5
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0001-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Aug 30 2013 Marcela Mašláňová <mmaslano@redhat.com> 1.0001-3
- fix all problems found in review rhbz#929254

* Tue Aug 27 2013 Marcela Mašláňová <mmaslano@redhat.com> 1.0001-2
- fix all problems found in review rhbz#929254

* Tue Aug 27 2013 Marcela Mašláňová <mmaslano@redhat.com> 1.0001-1
- Specfile autogenerated by cpanspec 1.78.
