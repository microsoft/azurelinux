# Run optional tests
%if ! (0%{?rhel})
%bcond_without perl_Devel_Hide_enables_optional_test
%else
%bcond_with perl_Devel_Hide_enables_optional_test
%endif

Name:           perl-Devel-Hide
Version:        0.0013
Release:        2%{?dist}
Summary:        Forces the unavailability of specified Perl modules (for testing)
License:        GPL+ or Artistic
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://metacpan.org/release/Devel-Hide
Source0:        https://cpan.metacpan.org/modules/by-module/Devel/Devel-Hide-%{version}.tar.gz#/perl-Devel-Hide-%{version}.tar.gz
BuildArch:      noarch
# Module Build
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(ExtUtils::MakeMaker)
# Module Runtime
BuildRequires:  perl(lib)
# Module::CoreList is used from a private subroutine that is never called
BuildRequires:  perl(strict)
BuildRequires:  perl(vars)
BuildRequires:  perl(warnings)
# Test Suite
BuildRequires:  perl(Test::More)
%if %{with perl_Devel_Hide_enables_optional_test}
# Optional Tests
BuildRequires:  perl(Test::Pod) >= 1.18
BuildRequires:  perl(Test::Pod::Coverage) >= 1.04
%endif
# Dependencies
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

%description
Given a list of Perl modules/filenames, this module makes require and use
statements fail (regardless of whether the specified files/modules are
installed or not).

%prep
%setup -q -n Devel-Hide-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
%{_fixperms} -c %{buildroot}

%check
make test

%files
%doc Changes README
%{perl_vendorlib}/Devel/
%{_mandir}/man3/Devel::Hide.3*

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.0013-2
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Mon Feb 17 2020 Paul Howarth <paul@city-fan.org> - 0.0013-1
- Update to 0.0013
  - Cope with changes to how the hints hash works in perl 5.31.7

* Sun Feb 16 2020 Paul Howarth <paul@city-fan.org> - 0.0012-1
- Update to 0.0012
  - Add -lexically argument to import() to support hiding modules just during
    the current scope

* Thu Feb 13 2020 Paul Howarth <paul@city-fan.org> - 0.0011-1
- Update to 0.0011
  - @INC hook should die directly (CPAN RT#120220)
  - Match core error more closely (CPAN RT#120221)
  - Add -quiet option to suppress some notices

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.0010-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.0010-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.0010-5
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.0010-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.0010-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.0010-2
- Perl 5.28 rebuild

* Mon Jun 18 2018 Paul Howarth <paul@city-fan.org> - 0.0010-1
- Update to 0.0010
  - Makefile.PL: better prereqs declaration
  - Documentation typo fix
- Switch upstream from search.cpan.org to metacpan.org
- Drop legacy Group: tag
- Use plain 'perl' instead of '%%{__perl}' macro
- Use DESTDIR rather than PERL_INSTALL_ROOT
- Make %%files list more explicit

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.0009-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Dec 06 2017 Petr Pisar <ppisar@redhat.com> - 0.0009-13
- Specify all dependencies

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.0009-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.0009-11
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.0009-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.0009-9
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.0009-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0009-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jun 05 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.0009-6
- Perl 5.22 rebuild

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.0009-5
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0009-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0009-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Jul 20 2013 Petr Pisar <ppisar@redhat.com> - 0.0009-2
- Perl 5.18 rebuild

* Sun Feb 03 2013 Iain Arnell <iarnell@gmail.com> 0.0009-1
- update to latest upstream
- remove rt74225.patch as it's fixed in latest release
- clean up spec for modern rpmbuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0008-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul 09 2012 Petr Pisar <ppisar@redhat.com> - 0.0008-12
- Perl 5.16 rebuild

* Thu Jun 28 2012 Iain Arnell <iarnell@gmail.com> 0.0008-11
- patch to avoid warnings for 'defined(@array)' - rt#74225

* Tue Jun 12 2012 Petr Pisar <ppisar@redhat.com> - 0.0008-10
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0008-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.0008-8
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0008-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 16 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.0008-6
- 661697 rebuild for fixing problems with vendorach/lib

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.0008-5
- Mass rebuild with perl-5.12.0

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.0008-4
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.0008-3
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0008-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat Apr 04 2009 Iain Arnell 0.0008-1
- Specfile autogenerated by cpanspec 1.78.
