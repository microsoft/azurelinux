# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:		perl-Perl-PrereqScanner-NotQuiteLite
Version:	0.9917
Release: 8%{?dist}
Summary:	A tool to scan your Perl code for its prerequisites
License:	GPL-1.0-or-later OR Artistic-1.0-Perl
URL:		https://metacpan.org/release/Perl-PrereqScanner-NotQuiteLite
Source0:	https://cpan.metacpan.org/modules/by-module/Perl/Perl-PrereqScanner-NotQuiteLite-%{version}.tar.gz
BuildArch:	noarch
# Module Build
BuildRequires:	coreutils
BuildRequires:	make
BuildRequires:	perl-generators
BuildRequires:	perl-interpreter
BuildRequires:	perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:	perl(ExtUtils::MakeMaker::CPANfile) >= 0.08
# Module Runtime
BuildRequires:	perl(Carp)
BuildRequires:	perl(constant)
BuildRequires:	perl(CPAN::Meta::Prereqs)
BuildRequires:	perl(CPAN::Meta::Requirements)
BuildRequires:	perl(Data::Dump)
BuildRequires:	perl(Exporter) >= 5.57
BuildRequires:	perl(File::Basename)
BuildRequires:	perl(File::Find)
BuildRequires:	perl(File::Glob)
BuildRequires:	perl(File::Spec)
BuildRequires:	perl(JSON::PP)
BuildRequires:	perl(Module::CoreList)
BuildRequires:	perl(Module::CPANfile) >= 1.1004
BuildRequires:	perl(Module::Find)
BuildRequires:	perl(parent)
BuildRequires:	perl(Parse::Distname)
BuildRequires:	perl(Regexp::Trie)
BuildRequires:	perl(strict)
BuildRequires:	perl(warnings)
# Script Runtime
BuildRequires:	perl(Getopt::Long)
BuildRequires:	perl(lib)
BuildRequires:	perl(Pod::Usage)
# Test Suite
BuildRequires:	perl(File::Path)
BuildRequires:	perl(File::Temp)
BuildRequires:	perl(FindBin)
BuildRequires:	perl(if)
BuildRequires:	perl(Test::More) >= 0.88
BuildRequires:	perl(Test::UseAllModules)
# Dependencies
Requires:	perl(Data::Dump)
Requires:	perl(JSON::PP)
Requires:	perl(Module::CoreList)
Requires:	perl(Module::Find)
Suggests:	perl(CPAN::Common::Index)

%description
Perl::PrereqScanner::NotQuiteLite is yet another prerequisites scanner. It
passes almost all the scanning tests for Perl::PrereqScanner and
Module::ExtractUse (i.e. except for a few dubious ones), and runs slightly
faster than PPI-based Perl::PrereqScanner. However, it doesn't run as fast as
Perl::PrereqScanner::Lite (which uses an XS lexer).

Perl::PrereqScanner::NotQuiteLite also recognizes eval. Prerequisites in eval
are not considered as requirements, but you can collect them as suggestions.

Conditional requirements or requirements loaded in a block are treated as
recommends. No-ed modules are stored separately (since 0.94). You may or may
not need to merge them into requires.

%prep
%setup -q -n Perl-PrereqScanner-NotQuiteLite-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PERLLOCAL=1 NO_PACKLIST=1
%make_build

%install
%make_install
%{_fixperms} -c %{buildroot}

%check
make test

%files
%license LICENSE
%doc Changes README
%{_bindir}/scan-perl-prereqs-nqlite
%{perl_vendorlib}/Perl/
%{_mandir}/man1/scan-perl-prereqs-nqlite.1*
%{_mandir}/man3/Perl::PrereqScanner::NotQuiteLite.3*
%{_mandir}/man3/Perl::PrereqScanner::NotQuiteLite::App.3*
%{_mandir}/man3/Perl::PrereqScanner::NotQuiteLite::Context.3*
%{_mandir}/man3/Perl::PrereqScanner::NotQuiteLite::Parser::Aliased.3*
%{_mandir}/man3/Perl::PrereqScanner::NotQuiteLite::Parser::AnyMoose.3*
%{_mandir}/man3/Perl::PrereqScanner::NotQuiteLite::Parser::Autouse.3*
%{_mandir}/man3/Perl::PrereqScanner::NotQuiteLite::Parser::Catalyst.3*
%{_mandir}/man3/Perl::PrereqScanner::NotQuiteLite::Parser::ClassAccessor.3*
%{_mandir}/man3/Perl::PrereqScanner::NotQuiteLite::Parser::ClassAutouse.3*
%{_mandir}/man3/Perl::PrereqScanner::NotQuiteLite::Parser::ClassLoad.3*
%{_mandir}/man3/Perl::PrereqScanner::NotQuiteLite::Parser::Core.3*
%{_mandir}/man3/Perl::PrereqScanner::NotQuiteLite::Parser::Inline.3*
%{_mandir}/man3/Perl::PrereqScanner::NotQuiteLite::Parser::KeywordDeclare.3*
%{_mandir}/man3/Perl::PrereqScanner::NotQuiteLite::Parser::Later.3*
%{_mandir}/man3/Perl::PrereqScanner::NotQuiteLite::Parser::Mixin.3*
%{_mandir}/man3/Perl::PrereqScanner::NotQuiteLite::Parser::ModuleRuntime.3*
%{_mandir}/man3/Perl::PrereqScanner::NotQuiteLite::Parser::MojoBase.3*
%{_mandir}/man3/Perl::PrereqScanner::NotQuiteLite::Parser::Moose.3*
%{_mandir}/man3/Perl::PrereqScanner::NotQuiteLite::Parser::MooseXDeclare.3*
%{_mandir}/man3/Perl::PrereqScanner::NotQuiteLite::Parser::ObjectPad.3*
%{_mandir}/man3/Perl::PrereqScanner::NotQuiteLite::Parser::Only.3*
%{_mandir}/man3/Perl::PrereqScanner::NotQuiteLite::Parser::POE.3*
%{_mandir}/man3/Perl::PrereqScanner::NotQuiteLite::Parser::PackageVariant.3*
%{_mandir}/man3/Perl::PrereqScanner::NotQuiteLite::Parser::Plack.3*
%{_mandir}/man3/Perl::PrereqScanner::NotQuiteLite::Parser::Prefork.3*
%{_mandir}/man3/Perl::PrereqScanner::NotQuiteLite::Parser::Superclass.3*
%{_mandir}/man3/Perl::PrereqScanner::NotQuiteLite::Parser::Syntax.3*
%{_mandir}/man3/Perl::PrereqScanner::NotQuiteLite::Parser::SyntaxCollector.3*
%{_mandir}/man3/Perl::PrereqScanner::NotQuiteLite::Parser::TestClassMost.3*
%{_mandir}/man3/Perl::PrereqScanner::NotQuiteLite::Parser::TestMore.3*
%{_mandir}/man3/Perl::PrereqScanner::NotQuiteLite::Parser::TestRequires.3*
%{_mandir}/man3/Perl::PrereqScanner::NotQuiteLite::Parser::UniversalVersion.3*
%{_mandir}/man3/Perl::PrereqScanner::NotQuiteLite::Parser::Unless.3*
%{_mandir}/man3/Perl::PrereqScanner::NotQuiteLite::Tokens.3*
%{_mandir}/man3/Perl::PrereqScanner::NotQuiteLite::Util.3*
%{_mandir}/man3/Perl::PrereqScanner::NotQuiteLite::Util::CPANfile.3*
%{_mandir}/man3/Perl::PrereqScanner::NotQuiteLite::Util::Prereqs.3*

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.9917-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.9917-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.9917-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.9917-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.9917-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.9917-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Apr 28 2023 Paul Howarth <paul@city-fan.org> - 0.9917-1
- Update to 0.9917
  - Update Object::Pad support (:isa/:does)
- Use SPDX-format license tag

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.9916-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.9916-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue May 31 2022 Jitka Plesnikova <jplesnik@redhat.com> - 0.9916-2
- Perl 5.36 rebuild

* Fri Apr  8 2022 Paul Howarth <paul@city-fan.org> - 0.9916-1
- Update to 0.9916
  - Ignore core modules with undef version correctly
  - Drop URI::cpan dependency and use Parse::Distname to parse cpan URI

* Fri Apr  1 2022 Paul Howarth <paul@city-fan.org> - 0.9915-1
- Update to 0.9915
  - Add 'optional' option

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.9914-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Sep 13 2021 Paul Howarth <paul@city-fan.org> - 0.9914-1
- Update to 0.9914
  - Support Object::Pad
- Use %%license unconditionally

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.9913-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 0.9913-3
- Perl 5.34 rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.9913-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sun Sep  6 2020 Paul Howarth <paul@city-fan.org> - 0.9913-1
- Update to 0.9913
  - Fix not to dedupe core modules needlessly
  - Use a main module to represent modules that belong to the same distribution
  - Dedupe build requires as well
  - Add URI::cpan to cpanfile

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.9911-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 0.9911-2
- Perl 5.32 rebuild

* Sun May 10 2020 Paul Howarth <paul@city-fan.org> - 0.9911-1
- Update to 0.9911
  - Changed ::App->run to return processed cpanfile object if 'cpanfile' option
    is set
  - Changed ::App->run not to print unless 'print' option is set
  - Remove cached cpanmeta if prereqs are replaced

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.9909-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Nov 30 2019 Paul Howarth <paul@city-fan.org> - 0.9909-1
- Update to 0.9909
  - Allowed full package names for Plack Middleware

* Mon Aug 26 2019 Paul Howarth <paul@city-fan.org> - 0.9908-1
- Update to 0.9908
  - Fixed Win32 path separator issues

* Thu Aug 22 2019 Paul Howarth <paul@city-fan.org> - 0.9907-1
- Update to 0.9907
  - Changed scan_also and features options to accept glob expressions
  - Added "verbose" option to show what's going on

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.9906-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Jul  8 2019 Paul Howarth <paul@city-fan.org> - 0.9906-1
- Update to 0.9906
  - Fixed PackageVariant parser not to die when it finds something other than
    importing

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.9905-2
- Perl 5.30 rebuild

* Fri May 10 2019 Paul Howarth <paul@city-fan.org> - 0.9905-1
- Update to 0.9905
  - Changed scan-perl-prereqs-nqlite to use only :bundled parsers by default
  - Added perl_minimum_version option
  - Added feature pragma arg parser
  - Added indented heredoc and <<$fh>> support
  - Fixed eval shortcut handling
  - Fixed parsers to treat several keywords as ops
  - Fixed various small parser issues (//, regexp after return, heredoc
    terminator, package version/block, when modifier etc.)
  - Renamed internal flags

* Thu Feb  7 2019 Paul Howarth <paul@city-fan.org> - 0.9904-1
- Update to 0.9904
  - Made sure to exclude local/core/private modules from feature prereqs
  - Added scan_also/parser/private options

* Wed Feb  6 2019 Paul Howarth <paul@city-fan.org> - 0.9903-2
- Address issues raised in package review (#1672313)
  - Switch upstream URL from search.cpan.org to metacpan.org
  - BR: perl(if) for test suite
- Modernize spec using %%make_build and %%make_install

* Mon Feb  4 2019 Paul Howarth <paul@city-fan.org> - 0.9903-1
- Update to 0.9903
  - Added an option to dedupe modules that belong to the same distribution
    with the help of CPAN::Common::Index

* Sun Feb  3 2019 Paul Howarth <paul@city-fan.org> - 0.9902-1
- Initial RPM version
