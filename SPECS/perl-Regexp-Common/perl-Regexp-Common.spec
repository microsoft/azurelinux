# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:		perl-Regexp-Common
Version:	2024080801
Release:	3%{?dist}
Summary:	Regexp::Common Perl module
# Old Artistic 1.0 is also valid, but we won't list it here since it is non-free.
# Also, it would throw off the automated license check and flag this package.
License:	Artistic-2.0 OR MIT OR BSD-3-Clause
URL:		https://metacpan.org/release/Regexp-Common
Source0:	https://cpan.metacpan.org/authors/id/A/AB/ABIGAIL/Regexp-Common-%{version}.tar.gz

BuildArch: noarch

BuildRequires:  %{__perl}
BuildRequires:  %{__make}

BuildRequires:	perl-generators
BuildRequires:	perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Carp)
BuildRequires:  perl(Config)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(overload)
BuildRequires:  perl(re)
BuildRequires:  perl(strict)
BuildRequires:  perl(vars)
BuildRequires:  perl(warnings)

# for improved tests
BuildRequires:	perl(Test::More)
BuildRequires:	perl(Test::Regexp)


%description
Regexp::Common - Provide commonly requested regular expressions

%prep
%setup -q -n Regexp-Common-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%{make_build}

%install
%{make_install}
chmod -R u+w $RPM_BUILD_ROOT/*

%check
%{__make} test

%files
%doc TODO README
%{perl_vendorlib}/Regexp
%{_mandir}/man3/*

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2024080801-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2024080801-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Aug 15 2024 Ralf Corsépius <corsepiu@fedoraproject.org> - 2024080801-1
- Upstream update to 2024080801.

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2017060201-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2017060201-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2017060201-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2017060201-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2017060201-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Nov 30 2022 Ralf Corsépius <corsepiu@fedoraproject.org> - 2017060201-20
- Modernize spec.
- Convert license to SPDX.

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2017060201-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue May 31 2022 Jitka Plesnikova <jplesnik@redhat.com> - 2017060201-18
- Perl 5.36 rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2017060201-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2017060201-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 2017060201-15
- Perl 5.34 rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2017060201-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2017060201-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 2017060201-12
- Perl 5.32 rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2017060201-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2017060201-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 2017060201-9
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2017060201-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2017060201-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 2017060201-6
- Perl 5.28 rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 2017060201-5
- Perl 5.28 rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2017060201-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2017060201-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jun 07 2017 Jitka Plesnikova <jplesnik@redhat.com> - 2017060201-2
- Perl 5.26 re-rebuild of bootstrapped packages

* Wed Jun 07 2017 Ralf Corsépius <corsepiu@fedoraproject.org> - 2017060201-1
- Upstream update to 2017060201.

* Mon Jun 05 2017 Jitka Plesnikova <jplesnik@redhat.com> - 2017040401-2
- Perl 5.26 rebuild

* Thu Apr 06 2017 Ralf Corsépius <corsepiu@fedoraproject.org> - 2017040401-1
- Upstream update to 2017040401.
- BR: %%{__perl}, %%{__make}.

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2016060801-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Jun 13 2016 Ralf Corsépius <corsepiu@fedoraproject.org> - 2016060801-1
- Upstream update to 2016060801.

* Tue Jun 07 2016 Ralf Corsépius <corsepiu@fedoraproject.org> - 2016060201-2
- Reflect upstream having removed author-tests.

* Tue Jun 07 2016 Ralf Corsépius <corsepiu@fedoraproject.org> - 2016060201-1
- Upstream update to 2016060201.

* Thu Jun 02 2016 Ralf Corsépius <corsepiu@fedoraproject.org> - 2016060101-1
- Upstream update to 2016060101.
- Add conditional author_tests.

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 2016020301-2
- Perl 5.24 rebuild

* Sun Feb 14 2016 Ralf Corsépius <corsepiu@fedoraproject.org> - 2016020301-1
- Upstream update.
- Add BR: perl(Test::Regexp).

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2016010801-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sat Jan 30 2016 Ralf Corsépius <corsepiu@fedoraproject.org> - 2016010801-2
- Modernize spec.

* Thu Jan 14 2016 Ralf Corsépius <corsepiu@fedoraproject.org> - 2016010801-1
- Upstream update.
- Expand BR:s.
- Modernize spec.

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2013031301-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jun 05 2015 Jitka Plesnikova <jplesnik@redhat.com> - 2013031301-7
- Perl 5.22 rebuild

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 2013031301-6
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2013031301-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2013031301-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Jul 20 2013 Petr Pisar <ppisar@redhat.com> - 2013031301-3
- Perl 5.18 rebuild

* Sun Mar 24 2013 Ralf Corsépius <corsepiu@fedoraproject.org> - 2013031301-2
- Add BR: perl(Carp).

* Thu Mar 21 2013 Ralf Corsépius <corsepiu@fedoraproject.org> - 2013031301-1
- Upstream update.

* Mon Mar 11 2013 Ralf Corsépius <corsepiu@fedoraproject.org> - 2013030901-1
- Upstream update.
- Fix bogus changelog dates.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2011121001-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2011121001-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 12 2012 Petr Pisar <ppisar@redhat.com> - 2011121001-3
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2011121001-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Dec 15 2011 Ralf Corsépius <corsepiu@fedoraproject.org> - 2011121001-1
- Upstream update.

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 2011041701-2
- Perl mass rebuild

* Sun Apr 17 2011 Ralf Corsépius <corsepiu@fedoraproject.org> - 2011041701-1
- Upstream update.
- Spec modernization.

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2010010201-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 21 2010 Marcela Maslanova <mmaslano@redhat.com> - 2010010201-3
- 661697 rebuild for fixing problems with vendorach/lib

* Thu May 06 2010 Marcela Maslanova <mmaslano@redhat.com> - 2010010201-2
- Mass rebuild with perl-5.12.0

* Mon Mar 08 2010 Ralf Corsépius <corsepiu@fedoraproject.org> - 2010010201-1
- Upstream update.

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 2.122-4
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.122-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.122-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu May 29 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.122-1
- update to 2.122
- license change

* Wed Mar  5 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.120-7
- rebuild for new perl

* Wed Aug 29 2007 Ralf Corsépius <rc040203@freenet.de> - 2.120-6
- BR: perl(ExtUtils::MakeMaker).

* Tue Sep 05 2006 Ralf Corsépius <rc040203@freenet.de> - 2.120-5
- Mass rebuild.

* Sat Feb 25 2006 Ralf Corsépius <rc040203@freenet.de> - 2.120-4
- Rebuild for FC5/perl-5.8.8.

* Sat Aug 20 2005 Ralf Corsepius <ralf@links2linux.de> - 2.120-3
- Further spec cleanup.

* Sat Aug 20 2005 Ralf Corsepius <ralf@links2linux.de> - 2.120-2
- Spec cleanup.

* Thu Aug 11 2005 Ralf Corsepius <ralf@links2linux.de> - 2.120-1
- FE submission.
