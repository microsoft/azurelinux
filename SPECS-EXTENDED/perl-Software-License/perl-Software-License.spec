# Run extra tests
%bcond_with perl_Software_License_enables_extra_test
%bcond_with perl_Software_License_enables_optional_test

Name:           perl-Software-License
Version:        0.104006
Release:        1%{?dist}
Summary:        Package that provides templated software licenses
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://metacpan.org/release/Software-License
Source0:        https://cpan.metacpan.org/authors/id/L/LE/LEONT/Software-License-%{version}.tar.gz
BuildArch:      noarch
# Module Build
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.78
# Module Runtime
BuildRequires:  perl(Carp)
BuildRequires:  perl(Data::Section)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(IO::Dir)
BuildRequires:  perl(Module::Load)
BuildRequires:  perl(parent)
BuildRequires:  perl(strict)
BuildRequires:  perl(Text::Template)
BuildRequires:  perl(utf8)
BuildRequires:  perl(warnings)
# Test Suite
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(Test::More) >= 0.88
BuildRequires:  perl(Try::Tiny)
%if %{with perl_Software_License_enables_optional_test}
# Optional Tests
BuildRequires:  perl(CPAN::Meta) >= 2.120900
BuildRequires:  perl(Software::License::CCpack)
%endif
%if %{with perl_Software_License_enables_extra_test}
# Extra Tests
BuildRequires:  perl(Encode)
BuildRequires:  perl(Test::Pod)
%endif
# Dependencies
# (none)

%description
Software-License contains templates for common open source software licenses.

%prep
%setup -q -n Software-License-%{version}

%build
/usr/bin/perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%{make_build}

%install
%{make_install}
%{_fixperms} -c %{buildroot}

%check
%{make_build} test
%if %{with perl_Software_License_enables_extra_test}
%{make_build} test TEST_FILES="$(echo $(find xt/ -name '*.t'))"
%endif

%files
%license LICENSE
%doc Changes README
%{perl_vendorlib}/Software/
%{_mandir}/man3/Software::License.3*
%{_mandir}/man3/Software::License::*.3*
%{_mandir}/man3/Software::LicenseUtils.3*

%changelog
* Mon Feb 27 2025 Sumit Jena <v-sumitjena@microsoft.com> - 0.104006-1
- Update to version 0.104006
- License verified

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.103014-7
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.103014-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.103014-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Jun 02 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.103014-4
- Perl 5.30 re-rebuild of bootstrapped packages

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.103014-3
- Perl 5.30 rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.103014-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Nov 28 2018 Paul Howarth <paul@city-fan.org> - 0.103014-1
- Update to 0.103014
  - Added SPDX license expression support
- This release by LEONT → update source URL

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.103013-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sun Jul 01 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.103013-4
- Perl 5.28 re-rebuild of bootstrapped packages

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.103013-3
- Perl 5.28 rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.103013-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Oct 30 2017 Paul Howarth <paul@city-fan.org> - 0.103013-1
- Update to 0.103013
  - guess_license_from_pod() now knows about Software::License::CC0_1_0
  - Enable "v" as a version word
  - Improve FreeBSD (2-Clause) phrases
  - Added EUPL v1.1 and v1.2
- This release by LEONT → update source URL
- Drop EL-5 support
  - Drop BuildRoot: and Group: tags
  - Drop explicit buildroot cleaning in %%install section
  - Drop explicit %%clean section
  - Drop workaround for building with Test::More < 0.88

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.103012-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jun 07 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.103012-6
- Perl 5.26 re-rebuild of bootstrapped packages

* Mon Jun 05 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.103012-5
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.103012-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed May 18 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.103012-3
- Perl 5.24 re-rebuild of bootstrapped packages

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.103012-2
- Perl 5.24 rebuild

* Sun Apr 24 2016 Paul Howarth <paul@city-fan.org> - 0.103012-1
- Update to 0.103012
  - Consider license names without parentheses when scanning text for license
  - When scanning text for license, put known substrings inside \b..\b
- Simplify find command using -delete
- Update patch for building with old Test::More versions

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.103011-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sun Jan 17 2016 Paul Howarth <paul@city-fan.org> - 0.103011-1
- Update to 0.103011
  - Do not load Sub::Install, since it isn't used!
  - Eliminate superfluous FULL STOP characters (".")
- Update patch for building with old Test::More versions
- Classify buildreqs by usage
- Use %%license where possible

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.103010-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.103010-4
- Perl 5.22 rebuild

* Fri Aug 29 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.103010-3
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.103010-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Mar 30 2014 Paul Howarth <paul@city-fan.org> - 0.103010-1
- Update to 0.103010
  - Fix guess_license_from_pod's return on GPL licenses
- Update patch for building with old Test::More versions

* Fri Feb 21 2014 Paul Howarth <paul@city-fan.org> - 0.103009-1
- Update to 0.103009
  - Updated FSF mailing address in license text for GFDL version 1.2, GPL
    versions 1 and 2, and LGPL 2.1
- Update patch for building with old Test::More versions
- Don't try to run the extra tests with EL-5 or EL-6

* Sun Nov 17 2013 Paul Howarth <paul@city-fan.org> - 0.103008-1
- Update to 0.103008
  - Faster!
  - Add new_from_short_name to LicenseUtils for spdx.org-style short names
  - Avoid double trailing dots in expanded licenses
  - Fix some errors in (3-clause) BSD license text
  - The 2-clause BSD ("FreeBSD") license no longer incorrectly puts "FreeBSD"
    as the owner in the license full text
- Update patch for building with old Test::More versions

* Sun Oct 27 2013 Paul Howarth <paul@city-fan.org> - 0.103007-1
- Update to 0.103007
  - Fix regex to allow guessing from meta things like perl_5
  - Replace 'use base' with 'use parent'
- BR: perl(Try::Tiny) for the test suite
- Update patch for building with old Test::More versions

* Mon Oct 21 2013 Paul Howarth <paul@city-fan.org> - 0.103006-2
- Update patch for building with old Test::More versions
- Update core buildreqs for completeness

* Mon Oct 21 2013 Daniel P. Berrange <berrange@redhat.com> - 0.103006-1
* Update to 0.103006 release (rhbz #1021385)

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.103005-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul 22 2013 Petr Pisar <ppisar@redhat.com> - 0.103005-3
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.103005-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Dec  8 2012 Paul Howarth <paul@city-fan.org> - 0.103005-1
- Update to 0.103005
  - Add MPL 2.0
- BR: perl(File::Temp)
- Release tests moved to xt/
- Update patch for building with old Test::More versions

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.103004-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 14 2012 Petr Pisar <ppisar@redhat.com> - 0.103004-3
- Perl 5.16 rebuild

* Wed Mar  7 2012 Paul Howarth <paul@city-fan.org> - 0.103004-2
- Add test suite patch to support building with Test::More < 0.88 so that we
  can build for EPEL-5, only applying the patch when necessary
- Drop redundant versioned requirements of XXX >= 0.000
- Drop BR: perl ≥ 1:5.6.0; even EL-3 could have satisfied that
- BR: perl(base) and perl(Carp), which could be dual-lived
- BR: perl(Test::Pod) for full test coverage
- Run the release tests too
- Don't need to remove empty directories from buildroot
- Don't use macros for commands
- Use DESTDIR rather than PERL_INSTALL_ROOT
- Drop %%defattr, redundant since rpm 4.4
- Make %%files list more explicit

* Mon Jan 30 2012 Daniel P. Berrange <berrange@redhat.com> - 0.103004-1
- Update to 0.103004 release (rhbz #750790)

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.103002-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Sep 03 2011 Iain Arnell <iarnell@gmail.com> 0.103002-1
- update to latest upstream version

* Wed Jun 29 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.102341-4
- Perl mass rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.102341-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 22 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.102341-2
- 661697 rebuild for fixing problems with vendorach/lib

* Fri Dec 17 2010 Daniel P. Berrange <berrange@redhat.com> - 0.102341-1
- Update to 0.102341 release

* Wed Jun 02 2010 Iain Arnell <iarnell@gmail.com> 0.101410-1
- update to 0.101410 release

* Thu May 06 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.012-4
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.012-3
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.012-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul 22 2009 Daniel P. Berrange <berrange@redhat.com> - 0.012-1
- Update to 0.012 release

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.008-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Sep 20 2008 Daniel P. Berrange <berrange@redhat.com> 0.008-3
- Remove explicit requires that duplicate automatic perl deps

* Sat Sep 06 2008 Daniel P. Berrange <berrange@redhat.com> 0.008-2
- Fix description
- Add missing Test::More BR

* Fri Sep 05 2008 Daniel P. Berrange <berrange@redhat.com> 0.008-1
- Specfile autogenerated by cpanspec 1.77.
