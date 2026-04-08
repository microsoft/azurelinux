# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Perform optional tests
%bcond_without perl_Text_Template_enables_optional_test

Name:           perl-Text-Template
Version:        1.61
Release:        8%{?dist}
Summary:        Expand template text with embedded Perl
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/Text-Template
Source0:        https://cpan.metacpan.org/authors/id/M/MS/MSCHOUT/Text-Template-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# Run-time:
BuildRequires:  perl(base)
BuildRequires:  perl(Carp)
BuildRequires:  perl(Exporter)
# Tests:
BuildRequires:  perl(Config)
BuildRequires:  perl(Encode)
BuildRequires:  perl(File::Temp)
BuildRequires:  perl(lib)
BuildRequires:  perl(Test::More) >= 0.94
BuildRequires:  perl(utf8)
BuildRequires:  perl(vars)
%if %{with perl_Text_Template_enables_optional_test}
# Optional tests:
BuildRequires:  perl(Safe)
# Not in Fedora
# BuildRequires:  perl(Test::More::UTF8)
BuildRequires:  perl(Test::Warnings)
%endif
Requires:       perl(Carp)

%description
This is a library for generating form letters, building HTML pages, or
filling in templates generally.  A 'template' is a piece of text that
has little Perl programs embedded in it here and there.  When you
'fill in' a template, you evaluate the little programs and replace
them with their values.

%prep
%setup -q -n Text-Template-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -delete
%{_fixperms} $RPM_BUILD_ROOT/*

%check
unset AUTHOR_TESTING
make test

%files
%license LICENSE
%doc README
%{perl_vendorlib}/Text/
%{_mandir}/man3/*.3pm*

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.61-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.61-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.61-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.61-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.61-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.61-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.61-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Oct 17 2022 Jitka Plesnikova <jplesnik@redhat.com> - 1.61-1
- 1.61 bump

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.60-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue May 31 2022 Jitka Plesnikova <jplesnik@redhat.com> - 1.60-3
- Perl 5.36 rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.60-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Sep 16 2021 Tom Callaway <spot@fedoraproject.org> - 1.60-1
- update to 1.60

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.59-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 1.59-4
- Perl 5.34 rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.59-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.59-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 15 2020 Tom Callaway <spot@fedoraproject.org> - 1.59-1
- update to 1.59

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 1.58-3
- Perl 5.32 rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.58-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Oct 16 2019 Tom Callaway <spot@fedoraproject.org> - 1.58-1
- update to 1.58

* Tue Sep 10 2019 Tom Callaway <spot@fedoraproject.org> - 1.57-1
- update to 1.57

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.56-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Jul  9 2019 Tom Callaway <spot@fedoraproject.org> - 1.56-1
- update to 1.56

* Thu Jun 06 2019 Petr Pisar <ppisar@redhat.com> - 1.55-3
- Enable tests

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.55-2
- Perl 5.30 rebuild

* Tue Feb 26 2019 Tom Callaway <spot@fedoraproject.org> - 1.55-1
- update to 1.55

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.54-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jan 14 2019 Tom Callaway <spot@fedoraproject.org> - 1.54-1
- update to 1.54

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.53-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.53-2
- Perl 5.28 rebuild

* Sat May  5 2018 Tom Callaway <spot@fedoraproject.org> - 1.53-1
- update to 1.53

* Sun Mar 25 2018 Tom Callaway <spot@fedoraproject.org> - 1.52-1
- update to 1.52

* Mon Mar  5 2018 Tom Callaway <spot@fedoraproject.org> - 1.51-1
- update to 1.51

* Thu Mar 01 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.50-1
- 1.50 bump

* Wed Feb 14 2018 Tom Callaway <spot@fedoraproject.org> - 1.47-5
- fix license tag

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.47-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.47-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.47-2
- Perl 5.26 rebuild

* Tue Feb 28 2017 Tom Callaway <spot@fedoraproject.org> - 1.47-1
- update to 1.47

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.46-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sat May 14 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.46-5
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.46-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.46-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.46-2
- Perl 5.22 rebuild

* Fri Mar 27 2015 Tom Callawau <spot@fedoraproject.org> - 1.46-1
- update to 1.46

* Fri Mar 06 2015 Petr Pisar <ppisar@redhat.com> - 1.45-18
- Correct license declaration to ((GPL+ or Artistic) and (GPLv2+ or Artistic))
  (bug #1198991)

* Thu Jan 15 2015 Petr Pisar <ppisar@redhat.com> - 1.45-17
- Specify all dependencies

* Tue Aug 26 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.45-16
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.45-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.45-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jul 18 2013 Petr Pisar <ppisar@redhat.com> - 1.45-13
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.45-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.45-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 11 2012 Petr Pisar <ppisar@redhat.com> - 1.45-10
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.45-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.45-8
- Perl mass rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.45-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 23 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.45-6
- 661697 rebuild for fixing problems with vendorach/lib

* Fri May 07 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.45-5
- Mass rebuild with perl-5.12.0

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 1.45-4
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.45-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.45-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Apr 23 2008 Ralf Corsépius <rc040203@freenet.de> - 1.45-1
- Upstream update.
- Abandon perl-Text-Template-perl510-fixtest09.patch.

* Thu Feb  7 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.44-6
- fix test 09 for perl5.10

* Tue Feb  5 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.44-5
- rebuild for new perl

* Wed Oct 17 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 1.44-4.1
- correct license tag
- add BR: perl(ExtUtils::MakeMaker)

* Thu Sep  7 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.44-4
- Rebuild for FC6.

* Thu Feb 16 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.44-3
- Rebuild for FC5 (perl 5.8.8).

* Thu Aug 25 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.44-2
- Removed the explicit perl build requirement.

* Wed Aug 10 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.44-1
- Update to Fedora Extras template.

* Sat Dec 18 2004 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0:1.44-0.fdr.1
- First build.
