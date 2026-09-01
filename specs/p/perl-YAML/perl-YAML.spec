# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Run test
%if ! (0%{?rhel})
%bcond_without perl_YAML_enables_test
%else
%bcond_with perl_YAML_enables_test
%endif
# Run extra test
%if ! (0%{?rhel})
%bcond_without perl_YAML_enables_extra_test
%else
%bcond_with perl_YAML_enables_extra_test
%endif

Name:           perl-YAML
Version:        1.31
Release:        6%{?dist}
Summary:        YAML Ain't Markup Language (tm)
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/YAML
# Tarball created from https://cpan.metacpan.org/modules/by-module/YAML/YAML-%%{version}.tar.gz
# using script YAML-free (see https://bugzilla.redhat.com/show_bug.cgi?id=1813197)
Source0:        YAML-free-%{version}.tar.gz
# Script to remove non-free content from upstream tarball
# Usage: YAML-free YAML-%%{version}.tar.gz
Source1:        YAML-free
BuildArch:      noarch
# Module Build
BuildRequires:  coreutils
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(ExtUtils::MakeMaker) > 6.75
# Module Runtime
BuildRequires:  perl(B)
BuildRequires:  perl(B::Deparse)
BuildRequires:  perl(Carp)
BuildRequires:  perl(constant)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(overload)
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# Test Suite
# Avoid circular build deps Test::YAML → Test::Base → YAML when bootstrapping
%if %{with perl_YAML_enables_test} && !%{defined perl_bootstrap}
BuildRequires:  perl(Config)
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(Encode)
BuildRequires:  perl(File::Find)
BuildRequires:  perl(IO::File)
BuildRequires:  perl(IO::Pipe)
BuildRequires:  perl(lib)
BuildRequires:  perl(Test::Deep)
BuildRequires:  perl(Test::More) >= 0.88
BuildRequires:  perl(Test::YAML) >= 1.05
BuildRequires:  perl(utf8)
%if %{with perl_YAML_enables_extra_test}
# Author Tests
BuildRequires:  perl(Test::Pod) >= 1.41
%endif
%endif
# Dependencies
Requires:       perl(B::Deparse)
Requires:       perl(Carp)

# Filter private provides:
# perl(yaml_mapping) perl(yaml_scalar) perl(yaml_sequence)
%global __provides_exclude ^perl\\(yaml_

%description
If you need to use YAML with Perl, it is likely that you will have a look at
this module (YAML.pm) first. There are several YAML modules in Perl and they
all support the simple Load() and Dump() API. Since this one has the obvious
name "YAML", it may seem obvious to pick this one.

The author of this module humbly asks you to choose another. YAML.pm was the
very first YAML implementation in the world, released in 2001. It was
originally made as a prototype, over 2 years before the YAML 1.0 spec was
published. Although it may work for your needs, it has numerous bugs and is
barely maintained.

Please consider using these first:
 * YAML::PP - Pure Perl, full featured, well maintained
 * YAML::PP::LibYAML - A libyaml Perl binding like YAML::XS but with the
   YAML::PP API

%prep
%setup -q -n YAML-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%{make_build}

%install
%{make_install}
%{_fixperms} -c %{buildroot}

%check
# Avoid circular build deps Test::YAML → Test::Base → YAML when bootstrapping
%if %{with perl_YAML_enables_test} && !%{defined perl_bootstrap}
make test AUTHOR_TESTING=%{with perl_YAML_enables_extra_test}
%endif

%files
%license LICENSE
%doc Changes CONTRIBUTING README
%dir %{perl_vendorlib}/YAML/
%dir %{perl_vendorlib}/YAML/Dumper/
%dir %{perl_vendorlib}/YAML/Loader/
%doc %{perl_vendorlib}/YAML.pod
%doc %{perl_vendorlib}/YAML/Any.pod
%doc %{perl_vendorlib}/YAML/Dumper.pod
%doc %{perl_vendorlib}/YAML/Dumper/Base.pod
%doc %{perl_vendorlib}/YAML/Error.pod
%doc %{perl_vendorlib}/YAML/Loader.pod
%doc %{perl_vendorlib}/YAML/Loader/Base.pod
%doc %{perl_vendorlib}/YAML/Marshall.pod
%doc %{perl_vendorlib}/YAML/Node.pod
%doc %{perl_vendorlib}/YAML/Tag.pod
%doc %{perl_vendorlib}/YAML/Types.pod
%{perl_vendorlib}/YAML.pm
%{perl_vendorlib}/YAML/Any.pm
%{perl_vendorlib}/YAML/Dumper.pm
%{perl_vendorlib}/YAML/Dumper/Base.pm
%{perl_vendorlib}/YAML/Error.pm
%{perl_vendorlib}/YAML/Loader.pm
%{perl_vendorlib}/YAML/Loader/Base.pm
%{perl_vendorlib}/YAML/Marshall.pm
%{perl_vendorlib}/YAML/Mo.pm
%{perl_vendorlib}/YAML/Node.pm
%{perl_vendorlib}/YAML/Tag.pm
%{perl_vendorlib}/YAML/Types.pm
%{_mandir}/man3/YAML.3*
%{_mandir}/man3/YAML::Any.3*
%{_mandir}/man3/YAML::Dumper.3*
%{_mandir}/man3/YAML::Dumper::Base.3*
%{_mandir}/man3/YAML::Error.3*
%{_mandir}/man3/YAML::Loader.3*
%{_mandir}/man3/YAML::Loader::Base.3*
%{_mandir}/man3/YAML::Marshall.3*
%{_mandir}/man3/YAML::Node.3*
%{_mandir}/man3/YAML::Tag.3*
%{_mandir}/man3/YAML::Types.3*

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.31-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.31-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.31-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.31-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.31-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Dec 28 2023 Paul Howarth <paul@city-fan.org> - 1.31-1
- Update to 1.31 (rhbz#2255994)
  - Update docs to recommend YAML::PP
- Package description updated as per upstream documentation

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.30-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Mar 02 2023 Michal Josef Špaček <mspacek@redhat.com> - 1.30-15
- Update license to SPDX format

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.30-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.30-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jun 03 2022 Jitka Plesnikova <jplesnik@redhat.com> - 1.30-12
- Perl 5.36 re-rebuild of bootstrapped packages

* Mon May 30 2022 Jitka Plesnikova <jplesnik@redhat.com> - 1.30-11
- Perl 5.36 rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.30-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.30-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon May 24 2021 Jitka Plesnikova <jplesnik@redhat.com> - 1.30-8
- Perl 5.34 re-rebuild of bootstrapped packages

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 1.30-7
- Perl 5.34 rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.30-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.30-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jun 26 2020 Jitka Plesnikova <jplesnik@redhat.com> - 1.30-4
- Perl 5.32 re-rebuild of bootstrapped packages

* Mon Jun 22 2020 Jitka Plesnikova <jplesnik@redhat.com> - 1.30-3
- Perl 5.32 rebuild

* Fri Mar 13 2020 Paul Howarth <paul@city-fan.org> - 1.30-2
- Remove non-free test file t/load-slides.t (#1813197, GH#219)

* Tue Jan 28 2020 Paul Howarth <paul@city-fan.org> - 1.30-1
- Update to 1.30
  - Breaking Change: Set $YAML::LoadBlessed default to false to make it more
    secure

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.29-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Jun 02 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.29-3
- Perl 5.30 re-rebuild of bootstrapped packages

* Thu May 30 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.29-2
- Perl 5.30 rebuild

* Sat May 11 2019 Paul Howarth <paul@city-fan.org> - 1.29-1
- Update to 1.29
  - Fix regex for alias to match the one for anchors (GH#214)

* Sun Apr 28 2019 Paul Howarth <paul@city-fan.org> - 1.28-1
- Update to 1.28
  - Security fix: only enable loading globs when $LoadCode is set (GH#213)
- Modernize spec using %%{make_build} and %%{make_install}

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.27-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Nov  3 2018 Paul Howarth <paul@city-fan.org> - 1.27-1
- Update to 1.27
  - Remove a warning about uninitialized value for perl ≤ 5.10

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.26-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sat Jun 30 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.26-3
- Perl 5.28 re-rebuild of bootstrapped packages

* Wed Jun 27 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.26-2
- Perl 5.28 rebuild

* Sun May 20 2018 Paul Howarth <paul@city-fan.org> - 1.26-1
- Update to 1.26
  - Fix bug introduced in 1.25 - loading of quoted string with colon as
    sequence element (GH#208)
  - Support zero indented block sequences (GH#207)

* Sat May 12 2018 Paul Howarth <paul@city-fan.org> - 1.25-1
- Update to 1.25
  - Support trailing comments (GH#189, GH#190, GH#191)
  - Remove unused code (GH#192)
  - Use Test::Deep to actually test correctly for class names (GH#193)
  - Fix loading of mapping key that starts with '= ' (GH#194)
  - Fix loading strings with multiple spaces (GH#172)
  - Allow more characters in anchor name (GH#196)
  - Add $YAML::LoadBlessed for disabling loading objects (GH#197)
  - Disable test with long string under certain conditions (GH#201)
  - Quote scalar if it equals '=' (GH#202)
  - Multiple regexp roundtrip does not grow (GH#203)
  - Add support for compact nested block sequences (GH#204)
  - Support reverse order of block scalar indicators (GH#205)
  - Support nested mappings in sequences (GH#206)
  - Fix parsing of quoted strings (GH#188)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.24-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Oct 31 2017 Paul Howarth <paul@city-fan.org> - 1.24-1
- Update to 1.24
  - Fix $LoadCode (GH#180, GH#181, GH#182)
- This release by TINITA → update source URL
- Drop redundant Group: tag

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.23-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jun 07 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.23-3
- Perl 5.26 re-rebuild of bootstrapped packages

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.23-2
- Perl 5.26 rebuild

* Mon Feb 20 2017 Paul Howarth <paul@city-fan.org> - 1.23-1
- Update to 1.23
  - Fix $YAML::Numify (empty values were converted to 0)

* Wed Feb 15 2017 Paul Howarth <paul@city-fan.org> - 1.22-1
- Update to 1.22
  - Add $YAML::Numify

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.21-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sat Dec 24 2016 Paul Howarth <paul@city-fan.org> - 1.21-1
- Update to 1.21
  - Declare variables with our() to avoid warnings (GH#109, GH#171)
  - Empty mapping value at the end resolves to null (was becoming empty string)
    (GH#131, GH#170)
  - Output key in warning when duplicate key was found (GH#119, GH#169)
  - Allow reading and writing to IO::Handle (GH#157, GH#168)

* Sat Dec  3 2016 Paul Howarth <paul@city-fan.org> - 1.20-1
- Update to 1.20
 - Allow quoted map keys in arrays (GH#146)
 - B::Deparse is loaded at runtime now
 - New feature $YAML::Preserve (GH#9)
- This release by INGY → update source URL

* Sat Nov 19 2016 Paul Howarth <paul@city-fan.org> - 1.19-1
- Update to 1.19
  - Add pod link to YAML::Shell (GH#164)
  - Fix infinite loop for aliases without a name (GH#151)
  - Improve error messages (GH#142, GH#162)
  - Trailing spaces after inline seq/map work now (GH#163)
  - Add test case for trailing comments (GH#154)

* Sat Jul  9 2016 Paul Howarth <paul@city-fan.org> - 1.18-1
- Update to 1.18
  - List Test::More as a prereq (GH#161)

* Wed Jul  6 2016 Paul Howarth <paul@city-fan.org> - 1.17-1
- Update to 1.17
  - Use Mo 0.40
- This release by TINITA → update source URL

* Sun Jul  3 2016 Paul Howarth <paul@city-fan.org> - 1.16-1
- Update to 1.16
  - Drop inconsistent $VERSION from YAML::Mo (GH#158)
- BR: perl-generators

* Wed May 18 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.15-7
- Perl 5.24 re-rebuild of bootstrapped packages

* Sat May 14 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.15-6
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.15-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.15-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 10 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.15-3
- Perl 5.22 re-rebuild of bootstrapped packages

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.15-2
- Perl 5.22 rebuild

* Mon Apr 20 2015 Paul Howarth <paul@city-fan.org> - 1.15-1
- Update to 1.15
  - Don't require newlines at end of YAML (GH#149)

* Mon Jan 26 2015 Paul Howarth <paul@city-fan.org> - 1.14-1
- Update to 1.14
  - Add support for QuoteNumericStrings global setting (PR/145)

* Sun Oct 12 2014 Paul Howarth <paul@city-fan.org> - 1.13-1
- Update to 1.13
  - Disable some warnings in YAML::Any (PR/140)

* Wed Sep 24 2014 Paul Howarth <paul@city-fan.org> - 1.12-1
- Update to 1.12
  - Fix parsing of unquoted strings (CPAN RT#97870)
- Classify buildreqs by usage

* Sun Sep 07 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.11-3
- Perl 5.20 re-rebuild of bootstrapped packages

* Wed Sep 03 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.11-2
- Perl 5.20 rebuild

* Tue Sep  2 2014 Paul Howarth <paul@city-fan.org> - 1.11-1
- Update to 1.11
  - Apply PR/139:
    -  Remove die() that can't be called (regex always matches)

* Fri Aug 29 2014 Paul Howarth <paul@city-fan.org> - 1.10-1
- Update to 1.10
  - Apply PR/138:
    - Report an error message mentioning indentation when choking on non-space
      indentation
    - die() should be called as a method of $self

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.09-2
- Perl 5.20 rebuild

* Tue Aug 26 2014 Paul Howarth <paul@city-fan.org> - 1.09-1
- Update to 1.09
  - Add t/000-compile-modules.t
  - Eliminate File::Basename from test/
  - Eliminate spurious trailing whitespace
  - Meta 0.0.2
  - Change testdir to t
  - Add doc examples for YAML::Any (PR/8)
  - Dep on Test::YAML 1.05
  - Replace tabs with spaces

* Tue Aug 12 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.01-2
- Disable tests when bootstrapping

* Fri Aug  8 2014 Paul Howarth <paul@city-fan.org> - 1.01-1
- Update to 1.01
  - Depend on patched Test::YAML

* Fri Aug  8 2014 Paul Howarth <paul@city-fan.org> - 1.00-1
- Update to 1.00
  - Switch to external Test::Base
  - Fix bad encoding in Pod
- Test::YAML is now unbundled
- Take advantage of new features in recent EU::MM to simplify spec

* Thu Jul 31 2014 Paul Howarth <paul@city-fan.org> - 0.98-1
- Update to 0.98
  - Fix indexing of YAML::Any
  - Change IRC to irc.perl.org#yaml
- Use %%license
- Drop workaround for #1115971

* Thu Jul 17 2014 Paul Howarth <paul@city-fan.org> - 0.97-1
- Update to 0.97
  - Move remaining docs to Swim
- Upstream reinstated all those pod files and manpages again

* Mon Jul 14 2014 Paul Howarth <paul@city-fan.org> - 0.96-1
- Update to 0.96
  - Fix Metadata and add Contributing file
  - Change Kwim to Swim
- Upstream dropped all those pod files and manpages again

* Thu Jul 03 2014 Petr Pisar <ppisar@redhat.com> - 0.95-2
- Inject VERSION into each module (bug #1115971)

* Mon Jun 23 2014 Paul Howarth <paul@city-fan.org> - 0.95-1
- Update to 0.95
  - Fix dumping blessed globs

* Sun Jun 15 2014 Paul Howarth <paul@city-fan.org> - 0.94-1
- Update to 0.94
  - Switch to Zilla::Dist
  - Add badges to doc
  - Fix regression introduced with earlier fix for complex regular
    subexpression recursion limit (GH#18)
  - Fix reference to non-existent sub Carp::Croak (GH#19)
- Enumerate all files so we can mark POD files as %%doc
- Bump Test::More version requirement to 0.88 due to use of done_testing

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.92-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Jun 03 2014 Petr Pisar <ppisar@redhat.com> - 0.92-2
- Do not run release tests on bootstrap (bug #1104137)

* Thu May 29 2014 Paul Howarth <paul@city-fan.org> 0.92-1
- Update to 0.92
  - Metadata fixes (https://github.com/ingydotnet/yaml-pm/pull/23)

* Wed May 28 2014 Paul Howarth <paul@city-fan.org> - 0.91-1
- Update to 0.91
  - Force escaping of single '-'
    (https://github.com/ingydotnet/yaml-pm/pull/22)

* Fri Feb 28 2014 Paul Howarth <paul@city-fan.org> - 0.90-2
- Avoid circular build deps via Module::Build when bootstrapping

* Tue Feb 11 2014 Paul Howarth <paul@city-fan.org> - 0.90-1
- Update to 0.90
  - Revert Mo from 0.38 to 0.31 following a report of it breaking cpan client

* Mon Feb 10 2014 Paul Howarth <paul@city-fan.org> - 0.89-1
- Update to 0.89
  - Synopsis in YAML::Dumper didn't work as expected (CPAN RT#19838)
  - Address complex regular subexpression recursion limit (CPAN RT#90593)
  - Use latest Test::Builder (CPAN RT#90847)
  - Fixed tests to work under parallel testing
  - Switched to dzil release process
- This release by INGY -> update source URL
- Make %%files list more explicit
- Specify all dependencies

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.84-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul 15 2013 Petr Pisar <ppisar@redhat.com> - 0.84-6
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.84-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Aug 28 2012 Jitka Plesnikova <jplesnik@redhat.com> - 0.84-4
- Specify all dependencies

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.84-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 17 2012 Paul Howarth <paul@city-fan.org> - 0.84-2
- Haven't needed to fix documentation character encoding since 0.79
- Drop Test::Base build dependency again to avoid a BR loop (#215637)
- Filter private provides perl(yaml_mapping), perl(yaml_scalar) and
  perl(yaml_sequence)
- Don't need to remove empty directories from the buildroot
- This release by MSTROUT -> update source URL

* Mon Jul 16 2012 Petr Šabata <contyk@redhat.com> - 0.84-1
- 0.84 bump
- Drop command macros
- Drop previously added patch (included in 0.82)

* Fri Jun 22 2012 Jitka Plesnikova <jplesnik@redhat.com> 0.81-4
- Apply patch to for YAML::Any RT#74226

* Wed Jun 06 2012 Petr Pisar <ppisar@redhat.com> - 0.81-3
- Perl 5.16 rebuild

* Mon Apr 23 2012 Paul Howarth <paul@city-fan.org> - 0.81-2
- R: perl(Carp) and perl(Data::Dumper)
- BR: perl(Carp), perl(constant) and perl(Exporter)
- Release tests no longer shipped, so drop buildreqs for them and don't bother
  setting AUTOMATED_TESTING; run tests even when bootstrapping

* Mon Apr 23 2012 Marcela Mašláňová <mmaslano@redhat.com> - 0.81-1
- Update to 0.81
- Add BR Data::Dumper

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.73-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jun 21 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.73-2
- Perl mass rebuild
- add perl_bootstrap macro

* Sat May 14 2011 Iain Arnell <iarnell@gmail.com> 0.73-1
- update to latest upstream version
- clean up spec for modern rpmbuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.72-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 08 2010 Steven Pritchard <steve@kspei.com> 0.72-1
- Update to 0.72.

* Wed Aug 18 2010 Paul Howarth <paul@city-fan.org> - 0.71-1
- Update to 0.71 (use UTF-8 encoding in LoadFile/DumpFile: CPAN RT#25434)
- Enable AUTOMATED_TESTING
- BR: perl(Test::CPAN::Meta), perl(Test::MinimumVersion), perl(Test::Pod)
- This release by ADAMK -> update source URL
- Re-code docs as UTF-8

* Thu Apr 29 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.70-5
- Mass rebuild with perl-5.12.0

* Thu Feb 25 2010 Marcela Mašláňová <mmaslano@redhat.com> - 0.70-4
- add license

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.70-3
- rebuild against perl 5.10.1

* Wed Oct  7 2009 Marcela Mašláňová <mmaslano@redhat.com> - 0.70-2
- rebuild for push

* Tue Oct 6  2009 Marcela Mašláňová <mmaslano@redhat.com> - 0.70-1
- new upstream version

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.68-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.68-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Dec 10 2008 Steven Pritchard <steve@kspei.com> 0.68-1
- Update to 0.68.
- COMPATIBILITY went away.
- ysh moved to YAML::Shell.

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.66-3
- Rebuild for perl 5.10 (again)

* Fri Jan 11 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.66-2
- rebuild for new perl

* Tue Oct 16 2007 Steven Pritchard <steve@kspei.com> 0.66-1
- Update to 0.66.
- Update License tag.

* Wed Jun 27 2007 Steven Pritchard <steve@kspei.com> 0.65-1
- Update to 0.65.

* Tue Mar 13 2007 Steven Pritchard <steve@kspei.com> 0.62-3
- Use fixperms macro instead of our own chmod incantation.
- Drop Test::Base build dependency to avoid a BR loop (#215637).
- BR ExtUtils::MakeMaker.

* Sat Sep 16 2006 Steven Pritchard <steve@kspei.com> 0.62-2
- Fix find option order.

* Fri Jul 07 2006 Steven Pritchard <steve@kspei.com> 0.62-1
- Update to 0.62.
- Removed Test::YAML (bug #197539).

* Mon Jul 03 2006 Steven Pritchard <steve@kspei.com> 0.61-1
- Update to 0.61.

* Sat May 20 2006 Steven Pritchard <steve@kspei.com> 0.58-3
- Rebuild.

* Tue May 09 2006 Steven Pritchard <steve@kspei.com> 0.58-2
- Drop testmore patch.
- Catch Test::YAML module and man page in file list.

* Thu May 04 2006 Steven Pritchard <steve@kspei.com> 0.58-1
- Update to 0.58.
- Small spec cleanups.

* Thu Apr 14 2005 Ville Skyttä <ville.skytta at iki.fi> - 0.39-2
- 0.39.

* Wed Apr  6 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Sat May 15 2004 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0:0.35-0.fdr.5
- Avoid creation of the perllocal.pod file (make pure_install).

* Sun Apr 25 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.35-0.fdr.4
- Require perl(:MODULE_COMPAT_*).
- Cosmetic tweaks (bug 1383).

* Sun Mar 14 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.35-0.fdr.3
- Reduce directory ownership bloat.

* Tue Nov 18 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:0.35-0.fdr.2
- Use INSTALLARCHLIB workaround in %%install.

* Wed Sep  3 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:0.35-0.fdr.1
- First build.
