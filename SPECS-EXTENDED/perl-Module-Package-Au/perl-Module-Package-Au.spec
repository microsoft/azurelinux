Name:		perl-Module-Package-Au
Version:	2
Release:	18%{?dist}
Summary:	Reusable Module::Install bits
License:	CC0
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:		https://metacpan.org/release/Module-Package-Au
Source0:	https://cpan.metacpan.org/authors/id/A/AU/AUDREYT/Module-Package-Au-%{version}.tar.gz#/%{name}-%{version}.tar.gz
Patch0:		perl-Module-Package-Au-no-bundle.patch
BuildArch:	noarch
BuildRequires:	perl-generators
BuildRequires:	perl(FindBin)
BuildRequires:	perl(File::Remove)
BuildRequires:	perl(Module::CoreList)
BuildRequires:	perl(ExtUtils::MakeMaker)
BuildRequires:	perl(Module::Install::AuthorTests)
BuildRequires:	perl(Module::Install::GithubMeta)
BuildRequires:	perl(Module::Install::ReadmeFromPod)
BuildRequires:	perl(Module::Install::ReadmeMarkdownFromPod)
BuildRequires:	perl(Module::Install::Repository)
BuildRequires:	perl(Module::Package) >= 0.24
BuildRequires:	perl(Pod::Markdown)
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

# Don't "provide" private Perl libs
%{?perl_default_filter}

%description
This module defines a set of standard configurations for Makefile.PL
files based on Module::Package.

%prep
%autosetup -n Module-Package-Au-%{version} -p1
rm -rf inc/*

# Work around goofy perl versioning mistakes of the past
sed -i 's|1.110730|1.301|g' lib/Module/Package/Au.pm
sed -i 's|1.110730|1.301|g' META.yml

%build
perl Makefile.PL INSTALLDIRS=vendor
%make_build

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -type f -name '*.bs' -empty -exec rm -f {} ';'
%{_fixperms} %{buildroot}

%check
make test

%files
%license README
%doc Changes
%{perl_vendorlib}/Module/Package/
%{_mandir}/man3/Module::Package::Au.3pm*

%changelog
* Tue Mar 07 2023 Muhammad Falak <mwani@microsoft.com> - 2-18
- License verified

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2-17
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 2-14
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jun 29 2018 Jitka Plesnikova <jplesnik@redhat.com> - 2-11
- Perl 5.28 rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jun 05 2017 Jitka Plesnikova <jplesnik@redhat.com> - 2-8
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon May 16 2016 Jitka Plesnikova <jplesnik@redhat.com> - 2-6
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 2-3
- Perl 5.22 rebuild

* Fri Aug 29 2014 Jitka Plesnikova <jplesnik@redhat.com> - 2-2
- Perl 5.20 rebuild

* Tue Jul  8 2014 Tom Callaway <spot@fedoraproject.org> - 2-1
- update to 2

* Tue Dec 11 2012 Tom Callaway <spot@fedoraproject.org> - 0.01-1
- initial package
