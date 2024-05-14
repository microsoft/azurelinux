Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Name:           perl-Mail-AuthenticationResults
Version:        1.20200108
Release:        3%{?dist}
Summary:        Object Oriented Authentication-Results Headers
License:        GPL+ or Artistic
URL:            https://search.cpan.org/dist/Mail-AuthenticationResults/
Source0:        https://www.cpan.org/modules/by-module/Mail/Mail-AuthenticationResults-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  perl >= 0:5.008
BuildRequires:  perl-generators
BuildRequires:  perl(base)
BuildRequires:  perl(Carp)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(JSON)
BuildRequires:  perl(lib)
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(strict)
BuildRequires:  perl(Test::Exception)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(warnings)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))


%description
Object Oriented Authentication-Results email headers.


%prep
%setup -q -n Mail-AuthenticationResults-%{version}


%build
perl Makefile.PL INSTALLDIRS=vendor
%make_build


%install
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null \;

%{_fixperms} $RPM_BUILD_ROOT/*


%check
make test


%files
%license LICENSE
%doc Changes dist.ini README README.md
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
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
