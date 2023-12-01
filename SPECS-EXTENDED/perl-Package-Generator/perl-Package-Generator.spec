# We need to patch the test suite if we have an old version of Test::More
%global old_test_more %(perl -MTest::More -e 'print (($Test::More::VERSION < 0.88) ? 1 : 0);' 2>/dev/null || echo 0)
# Run extra test
%if ! (0%{?rhel})
%bcond_without perl_Package_Generator_enables_extra_test
%else
%bcond_with perl_Package_Generator_enables_extra_test
%endif

Name:		perl-Package-Generator
Version:	1.106
Release:	18%{?dist}
Summary:	Generate new packages quickly and easily
License:	GPL+ or Artistic
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:		https://metacpan.org/release/Package-Generator
Source0:	https://cpan.metacpan.org/authors/id/R/RJ/RJBS/Package-Generator-%{version}.tar.gz#/perl-Package-Generator-%{version}.tar.gz
Patch1:		Package-Generator-1.106-old-Test-More.patch
BuildArch:	noarch
# Module Build
BuildRequires:	perl-generators
BuildRequires:	perl(ExtUtils::MakeMaker) >= 6.30
# Module
BuildRequires:	perl(Carp)
BuildRequires:	perl(Scalar::Util)
# Test Suite
BuildRequires:	perl(Params::Util) >= 0.11
BuildRequires:	perl(Test::More) >= 0.47
%if %{with perl_Package_Generator_enables_extra_test}
# Extra Tests
BuildRequires:	perl(Test::Pod)
%endif
# Runtime
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

%description
This module lets you quickly and easily construct new packages. It gives
them unused names and sets up their package data, if provided.

%prep
%setup -q -n Package-Generator-%{version}

# We need to patch the test suite if we have an old version of Test::More
%if %{old_test_more}
%patch1
%endif

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
%if %{with perl_Package_Generator_enables_extra_test}
make test TEST_FILES="$(echo $(find xt/ -name '*.t'))"
%endif

%files
%doc Changes LICENSE README
%{perl_vendorlib}/Package/
%{_mandir}/man3/Package::Generator.3pm*
%{_mandir}/man3/Package::Reaper.3pm*

%changelog
* Wed Apr 28 2021 Olivia Crain <oliviacrain@microsoft.com> - 1.106-18
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Remove colons from patchnames

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.106-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.106-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.106-15
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.106-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.106-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.106-12
- Perl 5.28 rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.106-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.106-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.106-9
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.106-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.106-7
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.106-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.106-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jun 05 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.106-4
- Perl 5.22 rebuild

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.106-3
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.106-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Dec 29 2013 Paul Howarth <paul@city-fan.org> - 1.106-1
- Update to 1.106
  - Update github links
  - Typo fix
- Update patch for building with Test::More < 0.88

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.105-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jul 18 2013 Petr Pisar <ppisar@redhat.com> - 1.105-2
- Perl 5.18 rebuild

* Mon Jul  8 2013 Paul Howarth <paul@city-fan.org> - 1.105-1
- Update to 1.105
  - Repackage, update bug tracker
  - Drop pod tests
- Add patch to support building with Test::More < 0.88
- Classify buildreqs by usage
- Explicitly run the extra tests

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.103-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Aug 24 2012 Paul Howarth <paul@city-fan.org> - 0.103-14
- Drop EPEL-4 support
- Drop %%defattr, redundant since rpm 4.4
- Don't need to remove empty directories from the buildroot
- BR: perl(File::Spec)

* Tue Aug 14 2012 Petr Pisar <ppisar@redhat.com> - 0.103-13
- Specify all dependencies
- Package LICENSE

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.103-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 10 2012 Petr Pisar <ppisar@redhat.com> - 0.103-11
- Perl 5.16 re-rebuild of bootstrapped packages

* Tue Jun 12 2012 Petr Pisar <ppisar@redhat.com> - 0.103-10
- Perl 5.16 rebuild

* Tue Feb  7 2012 Paul Howarth <paul@city-fan.org> - 0.103-9
- Don't BR: perl(Test::Perl::Critic) if we're bootstrapping

* Wed Feb  1 2012 Paul Howarth <paul@city-fan.org> - 0.103-8
- Run Perl::Critic test in %%check too
- BR: perl(Test::Perl::Critic)
- BR: perl(Carp) and perl(Symbol), which might be dual-lived
- Use DESTDIR rather than PERL_INSTALL_ROOT
- Drop version requirement for perl(ExtUtils::MakeMaker); older versions work
  without problems, e.g. version 6.17 on EL-4
- Make %%files list more explicit
- Don't use macros for commands
- Use tabs

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.103-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.103-6
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.103-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 21 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.103-4
- Rebuild to fix problems with vendorarch/lib (#661697)

* Tue May 04 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.103-3
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.103-2
- Rebuild against perl 5.10.1

* Tue Aug 11 2009 Chris Weyl <cweyl@alumni.drew.edu> - 0.103-1
- Auto-update to 0.103 (by cpan-spec-update 0.01)
- Added a new br on perl(ExtUtils::MakeMaker) (version 6.42)

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.102-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.102-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.102-2
- Rebuild for perl 5.10 (again)

* Thu Jan 24 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.102-1
- Rebuild for new perl
- Update to 0.102
- Fix license tag

* Wed Sep 06 2006 Chris Weyl <cweyl@alumni.drew.edu> - 0.100-2
- Bump

* Tue Sep 05 2006 Chris Weyl <cweyl@alumni.drew.edu> - 0.100-1
- Specfile autogenerated by cpanspec 1.69.1
