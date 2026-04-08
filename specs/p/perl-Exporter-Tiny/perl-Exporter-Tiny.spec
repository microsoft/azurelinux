# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:		perl-Exporter-Tiny
Version:	1.006002
Release:	9%{?dist}
Summary:	An exporter with the features of Sub::Exporter but only core dependencies
License:	GPL-1.0-or-later OR Artistic-1.0-Perl
URL:		https://exportertiny.github.io/
Source0:	https://cpan.metacpan.org/modules/by-module/Exporter/Exporter-Tiny-%{version}.tar.gz
BuildArch:	noarch
# Module Build
BuildRequires:	coreutils
BuildRequires:	make
BuildRequires:	perl-generators
BuildRequires:	perl-interpreter
# If we don't have at least 5.37.2 then we'll need Lexical::Var
BuildRequires:	perl(:VERSION) >= 5.37.2
BuildRequires:	perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:	sed
# Module Runtime
BuildRequires:	perl(Carp)
BuildRequires:	perl(strict)
BuildRequires:	perl(warnings)
# Test Suite
BuildRequires:	perl(Data::Dumper)
BuildRequires:	perl(lib)
BuildRequires:	perl(Test::More) >= 0.47
# Optional Tests
BuildRequires:	perl(Test::Fatal)
BuildRequires:	perl(Test::Warnings)
# Dependencies
Requires:	perl(Carp)

# Avoid doc-file dependency on perl(base)
%{?perl_default_filter}

%description
Exporter::Tiny supports many of Sub::Exporter's external-facing features
including renaming imported functions with the -as, -prefix and -suffix
options; explicit destinations with the into option; and alternative
installers with the installer option. But it's written in only about 40%%
as many lines of code and with zero non-core dependencies.

Its internal-facing interface is closer to Exporter.pm, with configuration
done through the @EXPORT, @EXPORT_OK and %%EXPORT_TAGS package variables.

Exporter::Tiny performs most of its internal duties (including resolution of
tag names to sub names, resolution of sub names to coderefs, and installation
of coderefs into the target package) as method calls, which means they can be
overridden to provide interesting behavior.

%prep
%setup -q -n Exporter-Tiny-%{version}

# Remove bundled modules Test::Fatal, Test::Requires, Test::Simple and Try::Tiny
rm -rv ./inc/
sed -i -e '/^inc\//d' MANIFEST

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%{make_build}

%install
%{make_install}
%{_fixperms} -c %{buildroot}

%check
make test

%files
%license COPYRIGHT LICENSE
%doc Changes CREDITS examples/ NEWS README TODO
%{perl_vendorlib}/Exporter/
%{_mandir}/man3/Exporter::Tiny.3*
%{_mandir}/man3/Exporter::Tiny::Manual::Etc.3*
%{_mandir}/man3/Exporter::Tiny::Manual::Exporting.3*
%{_mandir}/man3/Exporter::Tiny::Manual::Importing.3*
%{_mandir}/man3/Exporter::Tiny::Manual::QuickStart.3*
%{_mandir}/man3/Exporter::Shiny.3*

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.006002-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sun May 18 2025 Paul Howarth <paul@city-fan.org> - 1.006002-8
- Remove more legacy cruft
- Use %%{make_build} and %%{make_install}

* Sun May 18 2025 Yaakov Selkowitz <yselkowi@redhat.com> - 1.006002-7
- Remove obsolete dependency on Lexical::Var

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.006002-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.006002-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.006002-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.006002-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.006002-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sun Apr  2 2023 Paul Howarth <paul@city-fan.org> - 1.006002-1
- Update to 1.006002
  Documentation
  - Link to Exporter::Almighty in pod
  - Update copyright dates
  Packaging
  - Set homepage in metadata to https://exportertiny.github.io

* Sun Mar 26 2023 Paul Howarth <paul@city-fan.org> - 1.006001-1
- Update to 1.006001
  Documentation
  - Don't mention Alt::Lexical::Var::ButSupportModernPerl in manual
  Packaging
  - No longer dynamically recommend Alt::Lexical::Var::ButSupportModernPerl

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.006000-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Nov 21 2022 Paul Howarth <paul@city-fan.org> - 1.006000-1
- Update to 1.006000
  - Introduced lexical exporter support on Perl 5.11.2+ using the Lexical::Var
    module
  - Refactored the Perl 5.37.2+ lexical exporter support

* Sat Oct 15 2022 Paul Howarth <paul@city-fan.org> - 1.004004-1
- Update to 1.004004
  - Minor corrections to QuickStart page in the manual

* Fri Sep 30 2022 Paul Howarth <paul@city-fan.org> - 1.004003-1
- Update to 1.004003
  Bug Fixes
  - If exporting non-CODE items that happen to have the same name as exported
    CODE items, their export was quietly being blocked; these exports should
    now work (GH#9)
  - Using ! with a tag now works; it was previously documented as working but
    not implemented (GH#8)

* Tue Sep 20 2022 Paul Howarth <paul@city-fan.org> - 1.004002-1
- Update to 1.004002
  - Fix for t/15nonhashvalue.t on old versions of Test::More that don't support
    'done_testing'

* Sat Sep 10 2022 Paul Howarth <paul@city-fan.org> - 1.004001-1
- Update to 1.004001
  - Fix handling of non-hashref references in import list

* Mon Aug 29 2022 Paul Howarth <paul@city-fan.org> - 1.004000-1
- Update to 1.004000
  - Provide an experimental '-lexical' export option on Perl 5.37.2+
  - Quote $1 when passing it as a parameter to a function (GH#7)
- Use SPDX-format license tag
- Use %%license unconditionally
- Package new NEWS file

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.002002-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue May 31 2022 Jitka Plesnikova <jplesnik@redhat.com> - 1.002002-8
- Perl 5.36 rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.002002-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.002002-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 1.002002-5
- Perl 5.34 rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.002002-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.002002-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 1.002002-2
- Perl 5.32 rebuild

* Fri Apr 24 2020 Paul Howarth <paul@city-fan.org> - 1.002002-1
- Update to 1.002002
  - Fix bug in handling regexps in import lists; Exporter::Tiny allowed regexps
    like /foo/i but not /foo/; having trailing flags is now optional! (GH#6)
  - Tests would fail if 'PERL5OPT=-Mfeature=:5.18' environment variable was set;
    this is because bareword '-default' was being interpreted as the Perl
    'default' keyword (GH#5)
- Unbundle newly-bundled test modules

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.002001-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.002001-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.002001-3
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.002001-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Jul 18 2018 Paul Howarth <paul@city-fan.org> - 1.002001-1
- Update to 1.002001
  - Added support for generating and exporting non-code symbols such as $Foo,
    @Bar, and %%Baz
  - Improved test coverage, up from 88.78%% on coveralls.io to 96.74%%

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.000000-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.000000-5
- Perl 5.28 rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.000000-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.000000-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jun 05 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.000000-2
- Perl 5.26 rebuild

* Mon May 22 2017 Paul Howarth <paul@city-fan.org> - 1.000000-1
- Update to 1.000000
  - Repackage as 1.000000
- All shipped files are now GPL+ or Artistic
- Drop EL-5 support
  - Drop BuildRoot: and Group: tags
  - Drop explicit buildroot cleaning in %%install section
  - Drop explicit %%clean section

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.044-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Jan 30 2017 Paul Howarth <paul@city-fan.org> - 0.044-1
- Update to 0.044
  - Support { -as => CODE } to programmatically rename functions
  - Restructure documentation
- Simplify find command using -delete

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.042-6
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.042-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.042-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.042-3
- Perl 5.22 rebuild

* Fri Mar  6 2015 Paul Howarth <paul@city-fan.org> - 0.042-2
- Correct license tagging (#1199491)

* Thu Oct  9 2014 Paul Howarth <paul@city-fan.org> - 0.042-1
- Update to 0.042
  - Add an 'unimport' feature
  - Option validation needs to happen after expanding tags
  - Housekeeping on %%TRACKED

* Wed Sep 17 2014 Paul Howarth <paul@city-fan.org> - 0.040-1
- Update to 0.040
  - Document warning and error messages produced by Exporter::Tiny
  - Exporter::Tiny would previously cause B.pm to be loaded into memory any
    time it exported anything: it no longer does
  - No longer die when redefining locally defined subs
  - Warn when redefining any subs
- Use %%license where possible

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.038-3
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.038-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Apr  4 2014 Paul Howarth <paul@city-fan.org> - 0.038-1
- Update to 0.038
  - Added: Support Exporter.pm's import negation syntax qw( !foo )
  - Added: Support Exporter.pm's regexp import syntax qw( /foo/ )
  - Fix minor error in documentation of generators
  - Improved handling of hashrefs of options passed to tags, and hashrefs of
    options found within %%EXPORT_TAGS arrayrefs
  - Only attempt to merge hashes if we're sure they're both really hashes!

* Mon Mar 17 2014 Paul Howarth <paul@city-fan.org> - 0.036-2
- Sanitize for Fedora submission

* Thu Mar 13 2014 Paul Howarth <paul@city-fan.org> - 0.036-1
- Initial RPM version
