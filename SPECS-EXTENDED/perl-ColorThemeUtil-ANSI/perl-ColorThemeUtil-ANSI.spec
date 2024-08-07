%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}perl\\(Exporter\\)\\s*$
%global __requires_exclude %{?__requires_exclude}|perl\\(Color::ANSI::Util\\)\\s*$

Summary:        Utility routines related to color themes and ANSI code
Name:           perl-ColorThemeUtil-ANSI
Version:        0.002
Release:        4%{?dist}
License:        GPL+ OR Artistic
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://metacpan.org/release/ColorThemeUtil-ANSI/
Source0:        https://cpan.metacpan.org/authors/id/P/PE/PERLANCAR/ColorThemeUtil-ANSI-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  coreutils
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(:VERSION) >= 5.10.1
# Run-time
BuildRequires:  perl(Color::ANSI::Util) >= 0.164
BuildRequires:  perl(Exporter) >= 5.57
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)

%if 0%{?with_check}
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(IO::Handle)
BuildRequires:  perl(IPC::Open3)
BuildRequires:  perl(Test::More) >= 0.98
BuildRequires:  perl(blib)
%endif

Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:       perl(Color::ANSI::Util) >= 0.161
Requires:       perl(Exporter) >= 5.57

%description
This module provides utility routines related to color themes and ANSI
code.

%prep
%setup -q -n ColorThemeUtil-ANSI-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
%make_install
%{_fixperms} %{buildroot}/*

%check
unset AUTHOR_TESTING
make test

%files
%license LICENSE
%doc Changes README
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Wed Jan 26 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.002-4
- Initial CBL-Mariner import from Fedora 36 (license: MIT).
- License verified.

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.002-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 0.002-2
- Perl 5.34 rebuild

* Tue Feb 09 2021 Jitka Plesnikova <jplesnik@redhat.com> - 0.002-1
- 0.002 bump

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.001-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.001-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 14 2020 Jitka Plesnikova <jplesnik@redhat.com> 0.001-1
- Specfile autogenerated by cpanspec 1.78.
