Name:           perl-File-Find-Rule-Perl
Version:        1.15
Release:        17%{?dist}
Summary:        Common rules for searching for Perl things
License:        GPL+ or Artistic
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://metacpan.org/release/File-Find-Rule-Perl
Source0:        https://cpan.metacpan.org/authors/id/E/ET/ETHER/File-Find-Rule-Perl-%{version}.tar.gz#/perl-File-Find-Rule-Perl-%{version}.tar.gz
# Filter out the files rpm generates in sourcedir.
Patch0:         File-Find-Rule-Perl-1.15-fedora.patch
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
BuildArch:      noarch
BuildRequires:  perl-generators
BuildRequires:  perl(constant)
BuildRequires:  perl(lib)
BuildRequires:  perl(Carp)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(File::Find::Rule) >= 0.20
BuildRequires:  perl(File::Spec) >= 0.82
BuildRequires:  perl(File::Spec::Functions)
BuildRequires:  perl(File::Spec::Unix)
BuildRequires:  perl(Params::Util) >= 0.38
BuildRequires:  perl(Parse::CPAN::Meta) >= 1.38
BuildRequires:  perl(Test::More) >= 0.47

%description
Common rules for searching for Perl things.

%prep
%setup -q -n File-Find-Rule-Perl-%{version}
%patch0 -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1
make %{?_smp_mflags}

%install
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
chmod -R u+w $RPM_BUILD_ROOT/*

%check
make test

%files
%doc Changes
%{perl_vendorlib}/File
%{_mandir}/man3/*

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.15-17
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.15-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.15-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.15-14
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.15-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.15-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.15-11
- Perl 5.28 rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.15-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.15-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.15-8
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.15-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.15-6
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.15-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sun Jan 31 2016 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.15-4
- Modernize spec.

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.15-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jun 04 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.15-2
- Perl 5.22 rebuild

* Wed Apr 15 2015 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.15-1
- Upstream update.
- Reflect Source0: having changed.
- Rework spec to reflect upstream changes.

* Sun Sep 07 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.13-8
- Perl 5.20 re-rebuild of bootstrapped packages

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.13-7
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.13-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Aug 14 2013 Jitka Plesnikova <jplesnik@redhat.com> - 1.13-5
- Perl 5.18 re-rebuild of bootstrapped packages

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.13-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Jul 21 2013 Petr Pisar <ppisar@redhat.com> - 1.13-3
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Nov 07 2012 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.13-1
- Revert parts of previous changes.
- Upstream update.

* Tue Oct 23 2012 Petr Šabata <contyk@redhat.com> - 1.12-6
- Specify all dependencies
- Modernize specfile
- Drop command macros
- Fix mixed whitespace

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 10 2012 Petr Pisar <ppisar@redhat.com> - 1.12-4
- Perl 5.16 re-rebuild of bootstrapped packages

* Tue Jun 12 2012 Petr Pisar <ppisar@redhat.com> - 1.12-3
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Nov 25 2011 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.12-1
- Upstream update.
- Update BRs.
- Spec file cleanup.

* Tue Jun 28 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.10-3
- rebuild with Perl 5.14.1
- add perl_bootstrap macro for test BR

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Nov 03 2010 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.10-1
- Upstream update.

* Sun May 09 2010 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.09-5
- Re-enable pmv-test.

* Sat May 01 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.09-4
- Mass rebuild with perl-5.12.0

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.09-3
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.09-2
- rebuild against perl 5.10.1

* Fri Aug 07 2009 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.09-1
- Upstream update.

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.08-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jul 20 2009 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.08-1
- Upstream update.

* Wed Jun 17 2009 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.06-1
- Upstream update.
- Build in subdir to work-around rpm disturbing testsuite.
- Rework BRs.

* Fri Feb 27 2009 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.04-4
- Adjust minimum perl version in META.yml (Add File-Find-Rule-Perl-1.04.diff).

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.04-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Jun 24 2008 Ralf Corsépius <rc040203@freenet.de> - 1.04-2
- Unconditionally BR: perl(Test::CPAN::Meta).

* Tue Jun 10 2008 Ralf Corsépius <rc040203@freenet.de> - 1.04-1
- Upstream update.

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.03-3
- Rebuild for perl 5.10 (again)

* Fri Jan 11 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.03-2
- rebuild for new perl

* Mon Nov 19 2007 Ralf Corsépius <rc040203@freenet.de> - 0.03-1
- Initial version.
