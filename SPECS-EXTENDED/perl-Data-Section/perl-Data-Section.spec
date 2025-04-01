%if ! (0%{?rhel})
# Run extra test
%bcond_without perl_Data_Section_enables_extra_test
# Run optional test
%bcond_without perl_Data_Section_enables_optional_test
%else
%bcond_with perl_Data_Section_enables_extra_test
%bcond_with perl_Data_Section_enables_optional_test
%endif

Name:           perl-Data-Section
Version:        0.200008
Release:        1%{?dist}
Summary:        Read multiple hunks of data out of your DATA section
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://metacpan.org/release/Data-Section
Source0:        https://cpan.metacpan.org/authors/id/R/RJ/RJBS/Data-Section-%{version}.tar.gz
BuildArch:      noarch
# Build
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(ExtUtils::MakeMaker)
# Runtime
BuildRequires:  perl(Encode)
BuildRequires:  perl(MRO::Compat) >= 0.09
BuildRequires:  perl(strict)
BuildRequires:  perl(Sub::Exporter) >= 0.979
BuildRequires:  perl(warnings)
# Test Suite
BuildRequires:  perl(base)
BuildRequires:  perl(lib)
BuildRequires:  perl(Test::FailWarnings)
BuildRequires:  perl(Test::More) >= 0.96
BuildRequires:  perl(utf8)
%if %{with perl_Data_Section_enables_optional_test}
# Optional Tests
BuildRequires:  perl(CPAN::Meta) >= 2.120900
%endif
%if %{with perl_Data_Section_enables_extra_test}
# Extra Tests
BuildRequires:  perl(Test::Pod) >= 1.41
%endif

%description
Data::Section provides an easy way to access multiple named chunks of
line-oriented data in your module's DATA section. It was written to allow
modules to store their own templates, but probably has other uses.

%prep
%setup -q -n Data-Section-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -delete
%{_fixperms} -c $RPM_BUILD_ROOT

%check
make test
%if %{with perl_Data_Section_enables_extra_test}
make test TEST_FILES="$(echo $(find xt/ -name '*.t'))"
%endif

%files
%license LICENSE
%doc Changes README
%{perl_vendorlib}/Data/
%{_mandir}/man3/Data::Section.3*

%changelog
* Mon Feb 27 2025 Sumit Jena <v-sumitjena@microsoft.com> - 0.200008-1
- Update to version 0.200008
- License verified

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.200007-10
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.200007-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.200007-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.200007-7
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.200007-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.200007-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.200007-4
- Perl 5.28 rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.200007-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.200007-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Jul  7 2017 Paul Howarth <paul@city-fan.org> - 0.200007-1
- Update to 0.200007
  - Rename the test library "Parent.pm" to "Mother.pm" to avoid conflict with
    core "parent.pm" on case-insensitive systems
- Drop legacy Group: tag
- Simplify find command using -delete
- Classify buildreqs by usage

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.200006-9
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.200006-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.200006-7
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.200006-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.200006-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jun 05 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.200006-4
- Perl 5.22 rebuild

* Thu Aug 28 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.200006-3
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.200006-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Mar 10 2014 Paul Howarth <paul@city-fan.org> - 0.200006-1
- Update to 0.200006
  - Skip tests on Win32 pre-5.14 related to line endings; perl munges the data
    before we're able to get at it

* Wed Dec 11 2013 Paul Howarth <paul@city-fan.org> - 0.200005-1
- Update to 0.200005
  - Open DATA handles both :raw and :bytes to avoid content munging on Win32
  - This is not yet a perfect solution for Win32

* Mon Dec  2 2013 Paul Howarth <paul@city-fan.org> - 0.200004-1
- Update to 0.200004
  - Avoid confusion between \n, \x0d\x0a, and Win32

* Mon Nov  4 2013 Paul Howarth <paul@city-fan.org> - 0.200003-1
- Update to 0.200003
  [THIS MIGHT BREAK STUFF]
  - Add an "encoding" parameter to set encoding of data section contents; this
    defaults to UTF-8
- Drop support for old distributions as we now need Test::FailWarnings, which
  isn't available there

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.101622-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Jul 21 2013 Petr Pisar <ppisar@redhat.com> - 0.101622-2
- Perl 5.18 rebuild

* Thu Jun 20 2013 Paul Howarth <paul@city-fan.org> - 0.101622-1
- Update to 0.101622
  - Add a link to an Advent article about Data-Section
  - Update bugtracker, repo, etc.
- Run the release tests separately
- BR: perl(base), perl(File::Find), perl(File::Temp) and perl(lib) for the test
  suite
- Drop BR: perl(Pod::Coverage::TrustPod) and perl(Test::Pod::Coverage) as
  upstream has dropped their Pod coverage test
- Update patch for building with old Test::More versions

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.101621-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.101621-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 14 2012 Petr Pisar <ppisar@redhat.com> - 0.101621-3
- Perl 5.16 rebuild

* Wed Mar  7 2012 Paul Howarth <paul@city-fan.org> - 0.101621-2
- Add test suite patch to support building with Test::More < 0.88 so that we
  can build for EPEL-5, only applying the patch when necessary
- BR: at least version 0.09 of perl(MRO::Compat)
- BR: perl(Pod::Coverage::TrustPod), perl(Test::Pod) and
  perl(Test::Pod::Coverage) for full test coverage
- Run the release tests too
- Drop redundant explicit versioned dependency on perl(Sub::Exporter)
- Don't need to remove empty directories from buildroot
- Don't use macros for commands
- Use DESTDIR rather than PERL_INSTALL_ROOT
- Drop %%defattr, redundant since rpm 4.4
- Make %%files list more explicit

* Mon Jan 30 2012 Daniel P. Berrange <berrange@redhat.com> - 0.101621-1
- Update to 0.101621 release (rhbz #785362)

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.101620-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jun 29 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.101620-5
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.101620-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 16 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.101620-3
- 661697 rebuild for fixing problems with vendorach/lib

* Wed Jun 30 2010 Mark Chappell <tremble@fedoraproject.org> - 0.101620-2
- Add in missing BuildRequires MRO::Compat

* Wed Jun 30 2010 Mark Chappell <tremble@fedoraproject.org> - 0.101620-1
- Update for release 0.101620

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.093410-3
- Mass rebuild with perl-5.12.0

* Tue Jan 12 2010 Daniel P. Berrange <berrange@redhat.com> - 0.093410-2
- Fix source URL

* Thu Jan  7 2010 Daniel P. Berrange <berrange@redhat.com> - 0.093410-1
- Update to 0.093410 release

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.091820-3
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.091820-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul 22 2009 Daniel P. Berrange <berrange@redhat.com> - 0.091820-1
- Update to 0.091820 release

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.005-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Sep 06 2008 Daniel P. Berrange <berrange@redhat.com> 0.005-2
- Add Test::More BR

* Fri Sep 05 2008 Daniel P. Berrange <berrange@redhat.com> 0.005-1
- Specfile autogenerated by cpanspec 1.77.
