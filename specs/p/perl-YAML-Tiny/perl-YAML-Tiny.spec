# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Test using JSON::MaybeXS instead of JSON::PP
%if ! (0%{?rhel})
%{bcond_without perl_YAML_Tiny_enables_JSON_MaybeX_test}
%else
%{bcond_with perl_YAML_Tiny_enables_JSON_MaybeX_test}
%endif

Name:           perl-YAML-Tiny
Version:        1.76
Release: 4%{?dist}
Summary:        Read/Write YAML files with as little code as possible
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/YAML-Tiny
Source0:        https://www.cpan.org/modules/by-module/YAML/YAML-Tiny-%{version}.tar.gz
BuildArch:      noarch
# Module Build
BuildRequires:  coreutils
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
# Module Runtime
BuildRequires:  perl(B)
BuildRequires:  perl(Carp)
BuildRequires:  perl(Config)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(Fcntl)
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# Test Suite
BuildRequires:  perl(base)
BuildRequires:  perl(File::Basename)
BuildRequires:  perl(File::Find)
BuildRequires:  perl(File::Spec) >= 0.80
BuildRequires:  perl(File::Spec::Functions)
BuildRequires:  perl(File::Temp) >= 0.19
BuildRequires:  perl(Getopt::Long)
BuildRequires:  perl(IO::Dir)
BuildRequires:  perl(JSON::PP)
BuildRequires:  perl(lib)
BuildRequires:  perl(List::Util)
BuildRequires:  perl(open)
BuildRequires:  perl(Test::More) >= 0.88
BuildRequires:  perl(utf8)
BuildRequires:  perl(vars)
# Optional Tests
BuildRequires:  perl(CPAN::Meta) >= 2.120900
%if %{with perl_YAML_Tiny_enables_JSON_MaybeX_test}
BuildRequires:  perl(JSON::MaybeXS) >= 1.001000
%endif
# Dependencies
Requires:       perl(Carp)
Requires:       perl(Config)
Requires:       perl(Fcntl)

%description
YAML::Tiny is a Perl class for reading and writing YAML-style files,
written with as little code as possible, reducing load time and
memory overhead.

%prep
%setup -q -n YAML-Tiny-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%{make_build}

%install
%{make_install}
%{_fixperms} -c %{buildroot}

%check
make test

%files
%license LICENSE
%doc Changes CONTRIBUTING README
%{perl_vendorlib}/YAML/
%{_mandir}/man3/YAML::Tiny.3*

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.76-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.76-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Dec 16 2024 Paul Howarth <paul@city-fan.org> - 1.76-1
- Update to 1.76 (rhbz#2332646)
  - Revert change from GH#60: "yes", "y", etc. are not actually booleans (GH#66)

* Mon Dec 16 2024 Paul Howarth <paul@city-fan.org> - 1.75-1
- Update to 1.75 (rhbz#2332503)
  - Fixed regression in %%QUOTE (GH#60)
  - Fix version comparison logic for forward compatibility (GH#63)
- Switch source URL from cpan.metacpan.org to www.cpan.org
- Use %%{make_build} and %%{make_install}

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.74-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.74-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.74-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.74-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Mar 23 2023 Paul Howarth <paul@city-fan.org> - 1.74-1
- Update to 1.74 (rhbz#2181091)
  - A few documentation tweaks
- Use SPDX-format license tag

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.73-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.73-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue May 31 2022 Jitka Plesnikova <jplesnik@redhat.com> - 1.73-15
- Perl 5.36 rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.73-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.73-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 1.73-12
- Perl 5.34 rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.73-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.73-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 1.73-9
- Perl 5.32 rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.73-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.73-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.73-6
- Perl 5.30 rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.73-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Nov 16 2018 Paul Howarth <paul@city-fan.org> - 1.73-4
- Drop legacy Group: tag
- Drop redundant test requirements

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.73-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.73-2
- Perl 5.28 rebuild

* Thu Feb 22 2018 Paul Howarth <paul@city-fan.org> - 1.73-1
- Update to 1.73
  - Perform correct stripping of leading white space in literal/folded text
    blocks (GH#44, CPAN RT#56045)
  - Fix compatibility with Test::Builder 0.94 in test shim

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.70-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.70-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jun 05 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.70-3
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.70-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun Jan 22 2017 Paul Howarth <paul@city-fan.org> - 1.70-1
- Update to 1.70
  - Some errors writing to a file were incorrectly reported
- Simplify find command using -delete

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.69-3
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.69-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sun Jul 26 2015 Paul Howarth <paul@city-fan.org> - 1.69-1
- Update to 1.69
  - Tests no longer print to stderr unnecessarily; this makes core perl builds
    (where this distribution is included as CPAN-Meta-YAML) a little quieter
  - The Test::More dependency has been reduced to 0.88 by emulating 'subtest'
    for those tests that need it

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.67-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.67-2
- Perl 5.22 rebuild

* Tue May 12 2015 Paul Howarth <paul@city-fan.org> - 1.67-1
- Update to 1.67
  - Instead of erroring on duplicate keys found in a hash (introduced in
    version 1.63), now we only warn; this fixes an issue in Strawberry Perl
    (via CPAN::Meta::YAML) when parsing a configuration file
  - Updated File::Temp test prereq to 0.19 for 'newdir'

* Tue Mar 17 2015 Paul Howarth <paul@city-fan.org> - 1.66-1
- Update to 1.66
  - Removed bundled Test::TempDir::Tiny to rely on File::Temp for temporary
    directories during testing
- Revert to ExtUtils::MakeMaker flow

* Sat Mar 14 2015 Paul Howarth <paul@city-fan.org> - 1.65-1
- Update to 1.65
  - Artifacts left behind from testing are now cleaned up (GH#34)

* Wed Oct  8 2014 Paul Howarth <paul@city-fan.org> 1.64-1
- Update to 1.64
  - Remove silencing of any errors encountered while loading Scalar::Util
    (GH#33)
  - Now using JSON::MaybeXS in tests instead of JSON.pm
- Use %%license

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> 1.63-2
- Perl 5.20 rebuild

* Thu Jun 12 2014 Paul Howarth <paul@city-fan.org> 1.63-1
- Update to 1.63
  - Incorrect error messages fixed, when $@ is clobbered when Carp wasn't
    loaded (GH#30, GH#31)
  - Now checking for, and erroring on, duplicate keys found in a hash (GH#32)

* Sat Jun  7 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> 1.62-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Mar 16 2014 Paul Howarth <paul@city-fan.org> 1.62-1
- Update to 1.62
  - Fix handling of trailing colon in key name (CPAN RT#92916)

* Tue Feb 25 2014 Paul Howarth <paul@city-fan.org> 1.61-1
- Update to 1.61
  - Fixed a test for VMS (CPAN RT#93297)

* Fri Feb 14 2014 Paul Howarth <paul@city-fan.org> 1.60-1
- Update to 1.60
  - Numeric values are now quoted whenever they've been used as a string,
    which fixes inconsistent behaviour seen with numeric values, due to
    differences between the XS and pure-perl variants of Data::Dumper
    (GitHub Issue #24)
  - Numeric hash keys are now always quoted

* Wed Feb  5 2014 Paul Howarth <paul@city-fan.org> 1.58-1
- Update to 1.58
  - 1.57 omitted a change entry for the following change:
  Incompatible change:
  - Previously, YAML::Tiny was sloppy about file encodings; it is now strict
  - The 'read' method and 'LoadFile' function expect UTF-8 encoded files
  - The 'write' method and 'DumpFile' function produce UTF-8 encoded files
  - The 'read_string' and 'write_string' methods and the 'Load' and 'Dump'
    functions expect or generate (decoded) character data

* Fri Jan 31 2014 Paul Howarth <paul@city-fan.org> 1.57-1
- Update to 1.57
  Incompatible change:
  - Previously, some errors would throw exceptions and some would return the
    error condition in $YAML::Tiny::errstr, but now all errors throw
    exceptions; use of $errstr and the errstr method are deprecated
  Fixed:
  - Fixed write method to encode YAML file with UTF-8
  - Improved SYNOPSIS and documentation of new
  Testing:
  - Tests have been cleaned up and reorganized
  - Test coverage has been significantly improved
- Package docs CONTRIBUTING and README.md
- Update dependencies as needed

* Wed Sep 25 2013 Paul Howarth <paul@city-fan.org> 1.56-1
- Update to 1.56
  - read_string documentation error fixed (CPAN RT#74409)
  - Re-release with fixed compile test
- Go back to Module::Build::Tiny flow

* Thu Sep 19 2013 Paul Howarth <paul@city-fan.org> 1.55-1
- Update to 1.55
  - Revert to ExtUtils::MakeMaker flow
- Update buildreqs as needed

* Thu Aug 22 2013 Paul Howarth <paul@city-fan.org> 1.54-1
- Update to 1.54
  - Convert to Dist::Zilla
  - Updated format to conform to CPAN::Changes::Spec
- Upstream shipping README again
- Switch to Module::Build::Tiny flow
- Classify buildreqs by usage

* Wed Aug 21 2013 Paul Howarth <paul@city-fan.org> 1.53-1
- Update to 1.53
  - Updated repository metadata to reflect move to github
- This release by ETHER -> update source URL
- Upstream no longer shipping README
- Don't need to remove empty directories from the buildroot
- Make %%files list more explicit

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.51-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Jul 20 2013 Petr Pisar <ppisar@redhat.com> - 1.51-7
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.51-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Aug 21 2012 Jitka Plesnikova <jplesnik@redhat.com> - 1.51-5
- Add perl(Carp) to requires.

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.51-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 20 2012 Petr Pisar <ppisar@redhat.com> - 1.51-3
- Perl 5.16 rebuild

* Mon Jun 04 2012 Petr Pisar <ppisar@redhat.com> - 1.51-2
- The POD tests do not run by default

* Wed Mar 14 2012 Petr Šabata <contyk@redhat.com> - 1.51-1
- 1.51 bump
- Remove command macros

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.50-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Jul 21 2011 Petr Sabata <contyk@redhat.com> - 1.50-4
- Perl mass rebuild

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 1.50-3
- Perl mass rebuild

* Thu Jul 14 2011 Iain Arnell <iarnell@gmail.com> 1.50-2
- drop Test::MinimumVersion BR to avoid circular build deps

* Mon Jun 27 2011 Petr Sabata <contyk@redhat.com> - 1.50-1
- 1.50 bump
- Cleaning the spec file (I assume pre-EPEL6 compatibility is no longer
  essential here)
- Adding Exporter and Scalar::Util (optional but preferred) to BR/Rs

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.46-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Dec 18 2010 Steven Pritchard <steve@kspei.com> 1.46-1
- Update to 1.46.

* Tue Dec 07 2010 Steven Pritchard <steve@kspei.com> 1.44-1
- Update to 1.44.

* Fri May 07 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.40-3
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.40-2
- rebuild against perl 5.10.1

* Sun Sep 27 2009 Chris Weyl <cweyl@alumni.drew.edu> 1.40-1
- auto-update to 1.40 (by cpan-spec-update 0.01)

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.39-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat May 23 2009 Chris Weyl <cweyl@alumni.drew.edu> 1.39-1
- auto-update to 1.39 (by cpan-spec-update 0.01)
- added a new br on perl(File::Spec) (version 0.80)

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.36-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Jan 17 2009 Steven Pritchard <steve@kspei.com> 1.36-1
- Update to 1.36.
- BR Test::More.

* Fri May 16 2008 Steven Pritchard <steve@kspei.com> 1.32-1
- Update to 1.32.

* Fri Feb  8 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.25-2
- rebuild for new perl

* Mon Jan 28 2008 Steven Pritchard <steve@kspei.com> 1.25-1
- Update to 1.25.

* Tue Dec 11 2007 Steven Pritchard <steve@kspei.com> 1.21-1
- Update to 1.21.
- Update License tag.
- BR Test::MinimumVersion.

* Thu Aug 23 2007 Steven Pritchard <steve@kspei.com> 1.14-1
- Update to 1.14.

* Fri Jul 13 2007 Steven Pritchard <steve@kspei.com> 1.13-1
- Update to 1.13.

* Fri Jun 08 2007 Steven Pritchard <steve@kspei.com> 1.12-1
- Update to 1.12.

* Mon May 28 2007 Steven Pritchard <steve@kspei.com> 1.09-1
- Update to 1.09.

* Sat May 19 2007 Steven Pritchard <steve@kspei.com> 1.08-1
- Update to 1.08.
- Update description.

* Tue Mar 13 2007 Steven Pritchard <steve@kspei.com> 1.04-1
- Specfile autogenerated by cpanspec 1.70.
- Drop redundant perl build dependency.
- BR YAML, YAML::Syck, and Test::Pod for better test coverage.
