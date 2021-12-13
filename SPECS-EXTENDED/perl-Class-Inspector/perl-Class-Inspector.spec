Name:		perl-Class-Inspector
Version:	1.36
Release:	3%{?dist}
Summary:	Get information about a class and its structure
License:	GPL+ or Artistic
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:		https://metacpan.org/release/Class-Inspector
Source0:	https://cpan.metacpan.org/authors/id/P/PL/PLICEASE/Class-Inspector-%{version}.tar.gz#/perl-Class-Inspector-%{version}.tar.gz

Requires:  perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
BuildArch: noarch

BuildRequires:	perl-generators
BuildRequires:	perl(Exporter)
BuildRequires:	perl(Test::More)
BuildRequires:	perl(ExtUtils::MakeMaker)
BuildRequires:	perl(File::Spec) >= 0.80
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)

%description
Class::Inspector allows you to get information about a loaded class.
Most or all of this information can be found in other ways, but they aren't
always very friendly, and usually involve a relatively high level of Perl
wizardry, or strange and unusual looking code. Class::Inspector attempts to
provide an easier, more friendly interface to this information.

%prep
%setup -q -n Class-Inspector-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1
make %{?_smp_mflags}

%install
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type d -depth -exec rmdir {} 2>/dev/null ';'
%{_fixperms} $RPM_BUILD_ROOT/*

%check
make test

%files
%doc Changes README
%license LICENSE
%{perl_vendorlib}/Class
%{_mandir}/man3/*

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.36-3
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.36-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jul 24 2019 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.36-1
- Update to 1.36.

* Thu May 30 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.34-2
- Perl 5.30 rebuild

* Fri Mar 29 2019 Tom Callaway <spot@fedoraproject.org> - 1.34-1
- update to 1.34

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.32-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.32-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jun 27 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.32-3
- Perl 5.28 rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.32-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Aug 14 2017 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.32-1
- Update to 1.32.

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.31-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.31-4
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.31-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Nov 29 2016 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.31-2
- Drop AUTOMATED_TESTING.
- Remove stray reference to %%perl_bootstrap.

* Tue Nov 29 2016 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.31-1
- Update to 1.31.

* Wed May 18 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.28-15
- Perl 5.24 re-rebuild of bootstrapped packages

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.28-14
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.28-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jan 26 2016 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.28-12
- Remove %%defattr.
- Add %%license.
- Modernise spec.

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.28-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 10 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.28-10
- Perl 5.22 re-rebuild of bootstrapped packages

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.28-9
- Perl 5.22 rebuild

* Sun Sep 07 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.28-8
- Perl 5.20 re-rebuild of bootstrapped packages

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.28-7
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.28-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Aug 14 2013 Jitka Plesnikova <jplesnik@redhat.com> - 1.28-5
- Perl 5.18 re-rebuild of bootstrapped packages

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.28-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 1.28-3
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.28-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Nov 06 2012 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.28-1
- Upstream update.

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.27-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 10 2012 Petr Pisar <ppisar@redhat.com> - 1.27-3
- Perl 5.16 re-rebuild of bootstrapped packages

* Wed Jun 06 2012 Petr Pisar <ppisar@redhat.com> - 1.27-2
- Perl 5.16 rebuild

* Fri Jan 27 2012 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.27-1
- Upstream update.
- Spec file modernization.
- Fix perl_bootstrap handling.

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.25-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jun 27 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.25-2
- rebuild with Perl 5.14.1

* Thu Feb 17 2011 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.25-1
- Upstream update.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.24-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 15 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.24-7
- 661697 rebuild for fixing problems with vendorach/lib

* Wed Jun 23 2010 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.24-6
- Re-enable pmv-test.

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.24-5
- Mass rebuild with perl-5.12.0

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 1.24-4
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.24-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jun 17 2009 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.24-2
- BR: perl(Test::MinimumVersion) >= 0.008

* Mon May 11 2009 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.24-1
- Upstream update.
- Remove Class-Inspector-1.23.diff.

* Fri Feb 27 2009 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.23-3
- Unconditionally BR: perl(Test::CPAN::Meta).
- Adjust minimum perl version in META.yml (Add Class-Inspector-1.23.diff).

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.23-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Jun 10 2008 Ralf Corsépius <rc040203@freenet.de> - 1.23-1
- Upstream update.

* Tue Mar 11 2008 Ralf Corsépius <rc040203@freenet.de> - 1.22-1
- Upstream update.

* Thu Feb 28 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.20-3
- Rebuild normally, second pass

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.20-2
- Rebuild for perl 5.10 (again), first pass

* Thu Feb 14 2008 Ralf Corsépius <rc040203@freenet.de> - 1.20-1
- Upstream update.

* Mon Jan 14 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.18-3
- rebuild normally, second pass

* Sun Jan 13 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.18-2.1
- rebuild for new perl, first pass, disable TMV, tests

* Sun Nov 25 2007 Ralf Corsépius <rc040203@freenet.de> - 1.18-2
- Add BR: perl(Test::MinimumVersion).

* Tue Nov 20 2007 Ralf Corsépius <rc040203@freenet.de> - 1.18-1
- Upstream update.

* Fri Aug 17 2007 Ralf Corsépius <rc040203@freenet.de> - 1.17-1
- Upstream update.

* Thu Apr 19 2007 Ralf Corsépius <rc040203@freenet.de> - 1.16-3
- Reflect perl package split.

* Tue Sep 05 2006 Ralf Corsépius <rc040203@freenet.de> - 1.16-2
- Mass rebuild.

* Sun May 21 2006 Ralf Corsépius <rc040203@freenet.de> - 1.16-1
- Upstream update.

* Mon May 08 2006 Ralf Corsépius <rc040203@freenet.de> - 1.15-1
- Upstream update.

* Wed Mar 01 2006 Ralf Corsépius <rc040203@freenet.de> - 1.13-2
- Rebuild for perl-5.8.8.

* Thu Sep 29 2005 Ralf Corsepius <rc040203@freenet.de> - 1.13-1
- Upstream update.

* Tue Sep 13 2005 Ralf Corsepius <rc040203@freenet.de>
- Fix another typo in %%summary.

* Tue Sep 13 2005 Ralf Corsepius <rc040203@freenet.de> - 1.12-2
- Fix typo in %%summary.
- Spec file cleanup.

* Tue Sep 13 2005 Ralf Corsepius <rc040203@freenet.de> - 1.12-1
- FE submission.
