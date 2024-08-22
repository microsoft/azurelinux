Name:           perl-Sub-Quote
Version:        2.006006
Release:        4%{?dist}
Summary:        Efficient generation of subroutines via string eval
License:        GPL+ or Artistic
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://metacpan.org/release/Sub-Quote
Source0:        https://cpan.metacpan.org/authors/id/H/HA/HAARG/Sub-Quote-%{version}.tar.gz#/perl-Sub-Quote-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(:VERSION) >= 5.6.0
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# Run-time
BuildRequires:  perl(B)
BuildRequires:  perl(Carp)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(Scalar::Util)
# Tests
BuildRequires:  perl(Config)
BuildRequires:  perl(constant)
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(lib)
BuildRequires:  perl(List::Util)
BuildRequires:  perl(overload)
BuildRequires:  perl(POSIX)
BuildRequires:  perl(Test::Builder)
BuildRequires:  perl(Test::Fatal) >= 0.003
BuildRequires:  perl(Test::More) >= 0.94
BuildRequires:  perl(threads)
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Conflicts:      perl-Moo < 2.003000

%description
This package provides performant ways to generate subroutines from strings.

%prep
%setup -q -n Sub-Quote-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%{make_build}

%install
%{make_install}
%{_fixperms} $RPM_BUILD_ROOT/*

%check
make test

%files
%license LICENSE
%doc Changes README
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Thu Aug 22 2024 Neha Agarwal <nehaagrwal@microsoft.com> - 2.006006-4
- Promote package to Core repository.

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.006006-3
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.006006-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Oct 02 2019 Jitka Plesnikova <jplesnik@redhat.com> - 2.006006-1
- 2.006006 bump

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.006003-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 2.006003-2
- Perl 5.30 rebuild

* Mon Mar 11 2019 Jitka Plesnikova <jplesnik@redhat.com> - 2.006003-1
- 2.006003 bump

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.005001-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.005001-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 2.005001-2
- Perl 5.28 rebuild

* Fri Apr 20 2018 Jitka Plesnikova <jplesnik@redhat.com> - 2.005001-1
- 2.005001 bump

* Wed Feb 07 2018 Jitka Plesnikova <jplesnik@redhat.com> - 2.005000-1
- 2.005000 bump

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.004000-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jun 12 2017 Jitka Plesnikova <jplesnik@redhat.com> - 2.004000-1
- 2.004000 bump

* Mon Jun 05 2017 Jitka Plesnikova <jplesnik@redhat.com> - 2.003001-3
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.003001-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 12 2016 Jitka Plesnikova <jplesnik@redhat.com> - 2.003001-1
- Initial release
