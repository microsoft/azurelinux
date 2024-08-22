# Run optional test
%if ! (0%{?rhel})
%bcond_without perl_Sub_Install_enables_optional_test
%else
%bcond_with perl_Sub_Install_enables_optional_test
%endif

Name:           perl-Sub-Install
Version:        0.928
Release:        24%{?dist}
Summary:        Install subroutines into packages easily
License:        GPL+ or Artistic
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://metacpan.org/release/Sub-Install
Source0:        https://cpan.metacpan.org/authors/id/R/RJ/RJBS/Sub-Install-%{version}.tar.gz#/perl-Sub-Install-%{version}.tar.gz
BuildArch:      noarch
# ================= Module Build ============================
BuildRequires:  perl-interpreter
BuildRequires:  perl-generators
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.30
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# ================= Run-time ================================
BuildRequires:  perl(B)
BuildRequires:  perl(Carp)
BuildRequires:  perl(Scalar::Util)
# ================= Test Suite ==============================
BuildRequires:  perl(Test::More) >= 0.88
%if %{with perl_Sub_Install_enables_optional_test} && !%{defined perl_bootstrap}
# ================= Optional Tests ==========================
# Test::Output -> Sub::Exporter -> Sub::Install
BuildRequires:  perl(Test::Output)
%endif
# ================= Run-time ================================
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:       perl(B)

%description
This module makes it easy to install subroutines into packages without the
unsightly mess of no strict or typeglobs lying about where just anyone
can see them.

%prep
%setup -q -n Sub-Install-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} \;
%{_fixperms} %{buildroot}

%check
make test

%files
%doc Changes LICENSE README
%{perl_vendorlib}/Sub/
%{_mandir}/man3/Sub::Install.3pm*

%changelog
* Thu Aug 22 2024 Neha Agarwal <nehaagrwal@microsoft.com> - 0.928-24
- Promote package to Core repository.

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.928-23
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.928-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.928-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Jun 02 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.928-20
- Perl 5.30 re-rebuild of bootstrapped packages

* Thu May 30 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.928-19
- Perl 5.30 rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.928-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.928-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sat Jun 30 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.928-16
- Perl 5.28 re-rebuild of bootstrapped packages

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.928-15
- Perl 5.28 rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.928-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.928-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jun 07 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.928-12
- Perl 5.26 re-rebuild of bootstrapped packages

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.928-11
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.928-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed May 18 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.928-9
- Perl 5.24 re-rebuild of bootstrapped packages

* Sat May 14 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.928-8
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.928-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.928-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 10 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.928-5
- Perl 5.22 re-rebuild of bootstrapped packages

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.928-4
- Perl 5.22 rebuild

* Sun Sep 07 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.928-3
- Perl 5.20 re-rebuild of bootstrapped packages

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.928-2
- Perl 5.20 rebuild

* Fri Jun 27 2014 Paul Howarth <paul@city-fan.org> - 0.928-1
- Update to 0.928
  - Cope with subroutines with spaces in their names when catching warnings
  - Don't assume that the source sub isn't blessed in tests (!)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.927-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Nov 20 2013 Jitka Plesnikova <jplesnik@redhat.com> - 0.927-2
- Update BRs

* Wed Nov 13 2013 Robin Lee <cheeselee@fedoraproject.org> - 0.927-1
- Update to 0.927

* Wed Aug 14 2013 Jitka Plesnikova <jplesnik@redhat.com> - 0.926-10
- Perl 5.18 re-rebuild of bootstrapped packages

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.926-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Jul 20 2013 Petr Pisar <ppisar@redhat.com> - 0.926-8
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.926-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Aug 23 2012 Paul Howarth <paul@city-fan.org> - 0.926-6
- Be more selective about what to exclude when bootstrapping
- Don't use macros for commands
- Drop %%defattr, redundant since rpm 4.4
- Don't need to remove empty directories from the buildroot
- Make %%files list more explicit
- Fix typo in %%description

* Mon Aug 20 2012 Petr Pisar <ppisar@redhat.com> - 0.926-5
- Specify all dependencies

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.926-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 10 2012 Petr Pisar <ppisar@redhat.com> - 0.926-3
- Perl 5.16 re-rebuild of bootstrapped packages

* Sun Jun 10 2012 Petr Pisar <ppisar@redhat.com> - 0.926-2
- Perl 5.16 rebuild

* Mon Mar 12 2012 Robin Lee <cheeselee@fedoraproject.org> - 0.926-1
- Update to 0.926

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.925-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jun 28 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.925-9
- Perl mass rebuild
- add perl_bootstrap macro
- add missing BR ExtUtils::MakeMaker

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.925-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 22 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.925-7
- 661697 rebuild for fixing problems with vendorach/lib

* Thu May 06 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.925-6
- Mass rebuild with perl-5.12.0

* Thu Feb 25 2010 Marcela Mašláňová <mmaslano@redhat.com> - 0.925-5
- add license

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.925-4
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.925-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.925-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Feb 03 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.925-1
- update to 0.925

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.924-3
- Rebuild for perl 5.10 (again)

* Thu Jan 24 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.924-2
- rebuild for new perl
- fix license tag

* Wed Nov 22 2006 Chris Weyl <cweyl@alumni.drew.edu> 0.924-1
- update to 0.924
- add perl(Test::Perl::Critic) to BR's

* Wed Sep 06 2006 Chris Weyl <cweyl@alumni.drew.edu> 0.922-2
- bump

* Sat Sep 02 2006 Chris Weyl <cweyl@alumni.drew.edu> 0.922-1
- Specfile autogenerated by cpanspec 1.69.1.
