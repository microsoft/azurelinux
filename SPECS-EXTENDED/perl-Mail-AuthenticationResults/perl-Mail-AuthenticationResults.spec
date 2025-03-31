Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Name:           perl-Mail-AuthenticationResults
Version:        2.20231031
Release:        1%{?dist}
Summary:        Object Oriented Authentication-Results Headers
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/Mail-AuthenticationResults/
Source0:        https://cpan.metacpan.org/modules/by-module/Mail/Mail-AuthenticationResults-%{version}.tar.gz
BuildArch:      noarch

BuildRequires: make
BuildRequires:  perl >= 0:5.008
BuildRequires:  perl-generators
BuildRequires:  perl(base)
BuildRequires:  perl(Carp)
BuildRequires:  perl(Clone)
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(JSON)
BuildRequires:  perl(lib)
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(strict)
BuildRequires:  perl(Test::Exception)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(warnings)


%description
Object Oriented Authentication-Results email headers.


%prep
%setup -q -n Mail-AuthenticationResults-%{version}


%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
%make_install
%{_fixperms} $RPM_BUILD_ROOT/*


%check
%make_build test


%files
%license LICENSE
%doc Changes dist.ini README README.md
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Mon Feb 27 2025 Sumit Jena <v-sumitjena@microsoft.com> - 2.20231031-1
- Update to version 2.20231031
- License verified

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.20200108-3
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.20200108-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jan 09 2020 Xavier Bachelot <xavier@bachelot.org> 1.20200108-1
- Update to 1.20200108 (RHBZ#1789387).

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.20180923-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.20180923-3
- Perl 5.30 rebuild

* Mon Apr 15 2019 Xavier Bachelot <xavier@bachelot.org> 1.20180923-2
- Review fixes.

* Thu Apr 11 2019 Xavier Bachelot <xavier@bachelot.org> 1.20180923-1
- Initial package.
