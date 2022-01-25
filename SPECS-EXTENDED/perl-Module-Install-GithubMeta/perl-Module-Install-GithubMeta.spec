Name:       perl-Module-Install-GithubMeta 
Version:    0.30
Release:    17%{?dist}
# lib/Module/Install/GithubMeta.pm -> GPL+ or Artistic
License:    GPL+ or Artistic 
Vendor:         Microsoft Corporation
Distribution:   Mariner
Summary:    A Module::Install extension to include GitHub meta information in META.yml 
Source:     https://cpan.metacpan.org/authors/id/B/BI/BINGOS/Module-Install-GithubMeta-%{version}.tar.gz 
Url:        https://metacpan.org/release/Module-Install-GithubMeta
Requires:   perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
BuildArch:  noarch

BuildRequires: perl-generators
BuildRequires: perl(base)
BuildRequires: perl(Capture::Tiny) >= 0.05
BuildRequires: perl(Config)
BuildRequires: perl(Cwd)
BuildRequires: perl(ExtUtils::MakeMaker) >= 6.42
BuildRequires: perl(ExtUtils::Manifest)
BuildRequires: perl(Fcntl)
BuildRequires: perl(File::Path)
BuildRequires: perl(File::Find)
BuildRequires: perl(File::Spec)
BuildRequires: perl(FindBin)
BuildRequires: perl(Module::Build)
BuildRequires: perl(Module::Install) >= 0.85
BuildRequires: perl(strict)
BuildRequires: perl(Test::More) >= 0.47
BuildRequires: perl(Test::Pod)
BuildRequires: perl(vars)
BuildRequires: perl(warnings)

Requires:      perl(Module::Install) >= 0.85

%{?perl_default_filter}

%description
Module::Install::GithubMeta is a Module::Install extension
to include GitHub (http://github.com) meta information in
'META.yml'.  It automatically detects if the distribution 
directory is under 'git' version control and whether the 
'origin' is a GitHub repository; if so, it will set the
'repository' and 'homepage' meta in 'META.yml' to the 
appropriate URLs for GitHub.


%prep
%setup -q -n Module-Install-GithubMeta-%{version}

cat README | iconv -f `file --mime-encoding --brief README` -t UTF-8 > x
mv x README

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
%{_fixperms} %{buildroot}/*

%check
make test

%files
%license LICENSE
%doc README
%{perl_vendorlib}/*
%{_mandir}/man3/*.3*

%changelog
* Thu Jan 13 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.30-17
- License verified.

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.30-16
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.30-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.30-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.30-13
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.30-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.30-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.30-10
- Perl 5.28 rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.30-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.30-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jun 05 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.30-7
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.30-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.30-5
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.30-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.30-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.30-2
- Perl 5.22 rebuild

* Mon Mar 23 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.30-1
- 0.30 bump

* Thu Aug 28 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.28-3
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.28-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon May 26 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.28-1
- 0.28 bump

* Tue Sep 10 2013 Jitka Plesnikova <jplesnik@redhat.com> - 0.26-1
- 0.26 bump

* Mon Aug 26 2013 Jitka Plesnikova <jplesnik@redhat.com> - 0.24-1
- 0.24 bump

* Fri Aug 02 2013 Petr Pisar <ppisar@redhat.com> - 0.22-3
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.22-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jan  2 2013 Jitka Plesnikova <jplesnik@redhat.com> - 0.22-1
- 0.22 bump

* Mon Oct 22 2012 Jitka Plesnikova <jplesnik@redhat.com> - 0.18-1
- 0.18 bump
- Specify all dependencies.

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.16-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 22 2012 Petr Pisar <ppisar@redhat.com> - 0.16-2
- Perl 5.16 rebuild

* Fri Jan 27 2012 Marcela Mašláňová <mmaslano@redhat.com> - 0.16-1
- update to 0.16

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Oct 16 2011 Iain Arnell <iarnell@gmail.com> 0.14-1
- update to latest upstream version
- clean up spec for modern rpmbuild
- use DESTDIR, not PERL_INSTALL_ROOT

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 0.10-6
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Dec 20 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.10-4
- 661697 rebuild for fixing problems with vendorach/lib

* Mon May 03 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.10-3
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.10-2
- rebuild against perl 5.10.1

* Fri Sep 11 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.10-1
- submission

* Fri Sep 11 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.10-0
- initial RPM packaging
- generated with cpan2dist (CPANPLUS::Dist::RPM version 0.0.8)

