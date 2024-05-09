# Run author tests
%if ! (0%{?rhel})
%bcond_without perl_Perl_Critic_enables_extra_test
%else
%bcond_with perl_Perl_Critic_enables_extra_test
%endif

Name:		perl-Perl-Critic
Version:	1.138
Release:	3%{?dist}
Summary:	Critique Perl source code for best-practices
License:	GPL+ or Artistic
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:		https://metacpan.org/release/Perl-Critic
Source0:	https://cpan.metacpan.org/modules/by-module/Perl/Perl-Critic-%{version}.tar.gz
Patch0:		0001-Change-default-spell-check-tool-from-aspell-to-hunsp.patch
Patch3:		Perl-Critic-1.136-ppidump-shellbang.patch
BuildArch:	noarch

# Build process
BuildRequires:	coreutils
BuildRequires:	findutils
BuildRequires:	perl-generators
BuildRequires:	perl-interpreter
BuildRequires:	perl(lib)
BuildRequires:	perl(Module::Build) >= 0.42
BuildRequires:	perl(Task::Weaken)

# Module requirements
BuildRequires:	hunspell >= 1.2.12
BuildRequires:	hunspell-en
BuildRequires:	perl(B::Keywords) >= 1.05
BuildRequires:	perl(base)
BuildRequires:	perl(Carp)
BuildRequires:	perl(Config::Tiny) >= 2
BuildRequires:	perl(English)
BuildRequires:	perl(Exception::Class) >= 1.23
BuildRequires:	perl(Exporter) >= 5.58
BuildRequires:	perl(File::Find)
BuildRequires:	perl(File::Path)
BuildRequires:	perl(File::Spec)
BuildRequires:	perl(File::Spec::Unix)
BuildRequires:	perl(File::Temp)
BuildRequires:	perl(File::Which)
BuildRequires:	perl(Getopt::Long)
BuildRequires:	perl(IO::String)
BuildRequires:	perl(List::MoreUtils) >= 0.19
BuildRequires:	perl(List::Util)
BuildRequires:	perl(Module::Pluggable) >= 3.1
BuildRequires:	perl(Perl::Tidy)
BuildRequires:	perl(Pod::Parser)
BuildRequires:	perl(Pod::PlainText)
BuildRequires:	perl(Pod::Select)
BuildRequires:	perl(Pod::Spell) >= 1
BuildRequires:	perl(Pod::Usage)
BuildRequires:	perl(PPI) >= 1.265
BuildRequires:	perl(PPIx::QuoteLike)
BuildRequires:	perl(PPIx::Regexp) >= 0.010
BuildRequires:	perl(PPIx::Regexp::Util) >= 0.068
BuildRequires:	perl(PPIx::Utilities::Node)
BuildRequires:	perl(PPIx::Utilities::Statement) >= 1.001
BuildRequires:	perl(Readonly) >= 2
BuildRequires:	perl(Scalar::Util)
BuildRequires:	perl(strict)
BuildRequires:	perl(String::Format) >= 1.18
BuildRequires:	perl(Term::ANSIColor) >= 2.02
BuildRequires:	perl(Test::Builder) >= 0.92
BuildRequires:	perl(Text::ParseWords) >= 3
BuildRequires:	perl(version) >= 0.77
BuildRequires:	perl(warnings)

# Main test suite

BuildRequires:	perl(Fatal)
BuildRequires:	perl(File::Spec::Functions)
BuildRequires:	perl(Test::Deep)
BuildRequires:	perl(Test::Memory::Cycle)
BuildRequires:	perl(Test::More)

# We don't run the author tests when bootstrapping due to circular dependencies
# Test::Perl::Critic obviously pulls in Perl::Critic too
%if 0%{!?perl_bootstrap:1} && %{with perl_Perl_Critic_enables_extra_test}
BuildRequires:	perl(Devel::EnforceEncapsulation)
BuildRequires:	perl(Perl::Critic::Policy::Editor::RequireEmacsFileVariables)
BuildRequires:	perl(Perl::Critic::Policy::ErrorHandling::RequireUseOfExceptions)
BuildRequires:	perl(Perl::Critic::Policy::Miscellanea::RequireRcsKeywords)
BuildRequires:	perl(Test::Kwalitee) >= 1.15
BuildRequires:	perl(Test::Perl::Critic)
BuildRequires:	perl(Test::Pod) >= 1.00
BuildRequires:	perl(Test::Pod::Coverage) >= 1.04
BuildRequires:	perl(Test::Without::Module)
%endif

# Optional/not automatically detected runtime dependencies
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:	hunspell >= 1.2.12
Requires:	perl(File::Which)
Requires:	perl(Module::Pluggable) >= 3.1
Requires:	perl(Pod::Parser)
Requires:	perl(PPI) >= 1.265
Requires:	perl(Term::ANSIColor) >= 2.02

%description
Perl::Critic is an extensible framework for creating and applying coding
standards to Perl source code. Essentially, it is a static source code
analysis engine. Perl::Critic is distributed with a number of
Perl::Critic::Policy modules that attempt to enforce various coding
guidelines. Most Policy modules are based on Damian Conway's book Perl
Best Practices. However, Perl::Critic is not limited to PBP and will
even support Policies that contradict Conway. You can enable, disable,
and customize those Polices through the Perl::Critic interface. You can
also create new Policy modules that suit your own tastes.

%package -n perl-Test-Perl-Critic-Policy
Summary:	A framework for testing your custom Policies
License:	GPL+ or Artistic
Requires:	perl(Test::Builder) >= 0.92

%description -n perl-Test-Perl-Critic-Policy
This module provides a framework for function-testing your custom
Perl::Critic::Policy modules. Policy testing usually involves feeding it a
string of Perl code and checking its behavior. In the old days, those strings
of Perl code were mixed directly in the test script. That sucked.

%prep
%setup -q -n Perl-Critic-%{version}

# Switch spell checker tool from aspell to hunspell
%patch 0 -p1

# Fix shellbang in ppidump tool
%patch 3

# Drop exec bits from samples/docs to avoid dependency bloat
find tools examples -type f -exec chmod -c -x {} ';'

%build
perl Build.PL --installdirs=vendor
./Build

%install
./Build install --destdir=%{buildroot} --create_packlist=0
%{_fixperms} -c %{buildroot}

%check
%if 0%{!?perl_bootstrap:1} && %{with perl_Perl_Critic_enables_extra_test}
LC_ALL=en_US ./Build authortest
%else
LC_ALL=en_US ./Build test
%endif

%files
%if 0%{?_licensedir:1}
%license LICENSE
%else
%doc LICENSE
%endif
%doc Changes CONTRIBUTING.md README TODO.pod examples/ extras/ tools/
%{_bindir}/perlcritic
%{perl_vendorlib}/Perl/
%{_mandir}/man1/perlcritic.1*
%{_mandir}/man3/Perl::Critic*.3*

%files -n perl-Test-Perl-Critic-Policy
%{perl_vendorlib}/Test/
%{_mandir}/man3/Test::Perl::Critic::Policy.3*

%changelog
* Sun Jul 25 2021 Jon Slobodzian <joslobo@microsoft.com> - 1.138-3
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Removed dependency on glibc-langpack-en.

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.138-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Jan 25 2020 Paul Howarth <paul@city-fan.org> - 1.138-1
- Update to 1.138
  - RequireCheckingReturnValueOfEval didn't count returning the result of an
    eval as checking it - now it does; however, it's only if you "return eval
    { ... }" - it still doesn't handle the case of "return ( eval {} )"
    (GH#324)
  - ProhibitPunctuationVars would get confused and think that the expression
    qr/SOME$/ was using the $/ special variable (GH#843)

* Thu Nov 28 2019 Paul Howarth <paul@city-fan.org> - 1.136-1
- Update to 1.136
  New Features
  - The ProhibitNoWarnings policy now handles warnings in the experimental::
    group (GH#892)
  Documentation
  - Prevented some example code from showing up in 'perldoc' (GH#799)
- Fix shellbang in ppidump tool

* Thu Sep  5 2019 Paul Howarth <paul@city-fan.org> - 1.134-5
- Do not run extra tests on RHEL

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.134-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Jun 02 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.134-3
- Perl 5.30 re-rebuild of bootstrapped packages

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.134-2
- Perl 5.30 rebuild

* Thu May 23 2019 Paul Howarth <paul@city-fan.org> - 1.134-1
- Update to 1.134
  New Features
  - Added new policy BuiltinFunctions::ProhibitShiftRef (GH#837)
  - Support indented heredocs (GH#861)
  - In Subroutines::ProhibitManyArgs, you can now omit the object variable
    (C<$self> or C<$class>) from the argument count (GH#815)
  Policy Changes
  - The policy Documentation::RequirePodLinksIncludeText is obsolete and has
    been removed (GH#494)
  Dependencies
  - Removed use of File::HomeDir
  - Upgrade to PPI 1.265 (GH#860)
  - Fix failed tests caused by new PPI (GH#858)
  Internals
  - Updated the Appveyor config (GH#851)

* Mon Apr 29 2019 Paul Howarth <paul@city-fan.org> - 1.132-8
- Add workaround for PPI ≥ 1.262

* Fri Apr 26 2019 Paul Howarth <paul@city-fan.org> - 1.132-7
- Add workaround for PPI ≥ 1.250
  https://github.com/Perl-Critic/Perl-Critic/issues/858

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.132-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Nov  6 2018 Paul Howarth <paul@city-fan.org> - 1.132-5
- Explicitly BR: glibc-langpack-en

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.132-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sun Jul 01 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.132-3
- Perl 5.28 re-rebuild of bootstrapped packages

* Fri Jun 29 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.132-2
- Perl 5.28 rebuild

* Fri Jun  1 2018 Paul Howarth <paul@city-fan.org> - 1.132-1
- Update to 1.132
  New Features
  - In the ProhibitLeadingZeros policy, added an exception for mkfifo (GH#786)
  - Add colour support for Windows platforms (GH#700)
  - Perl::Critic now assumes that .psgi files are Perl, too (GH#805)
  - Variables::ProhibitUnusedVariables no longer gives a false positive for
    variables used in interpolation (GH#801)
  - Added the ability to specify a regex to tell what unused private
    subroutines are OK in Subroutines::ProhibitUnusedPrivateSubroutines; this
    is handy for Moose classes where there could be many false positives on
    _build_xxxx() subroutines (GH#811, GH#812)
  Dependencies
  - Perl::Critic now no longer relies on the deprecated Email::Address
    (GH #816)
  Bug Fixes
  - Recode Perl::Critic::Utils::all_perl_files() to use File::Find instead of
    opendir/readdir; this solves endless directory traversals if the
    directories contain circular symbolic references
  - Added missing requirement for Fatal.pm
  Documentation
  - Added CONTRIBUTING.md
- Switch upstream from search.cpan.org to metacpan.org
- Switch spell checker from aspell to hunspell

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.130-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.130-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Jul 21 2017 Paul Howarth <paul@city-fan.org> - 1.130-1
- Update to 1.130
  New Features
  - Policies that ensure that system calls are checked, such as
    RequireCheckedSystemCalls, now have an "autodie_modules" setting that
    allows you to tell the policy about other modules that export autodie
    (GH#699, GH#747)

* Sun Jun 11 2017 Paul Howarth <paul@city-fan.org> - 1.128-1
- Update to 1.128
  Bug Fixes
  - PPI misparsing a module caused an incorrect "Must end with a recognizable
    true value"; this is fixed by upgrading to PPI 1.224 (GH#696, GH#607)
  - A test would fail under the upcoming Perl 5.26 that omits the current
    directory from @INC
  - Fixed an invalid test in the RequireBarewordsIncludes test (GH#751)
  - If an element contained blank lines then the source "%%r" displayed for a
    violation was wrong (GH#702, GH#734)
  Dependencies
  - Perl::Critic now requires PPI 1.224; PPI is the underlying Perl parser on
    which Perl::Critic is built, and 1.224 introduces many parsing fixes such
    as:
    - Fixes for dot-in-@INC
    - Parse left side of => as bareword even if it looks like a keyword or op
    - $::x now works
    - Higher accuracy when deciding whether certain characters are operators or
      variable type casts (*&%% etc.)
    - Subroutine attributes parsed correctly
  Performance Enhancements
  - Sped up BuiltinFunctions::ProhibitUselessTopic ~7%% (GH#656)
  Documentation
  - Fixed incorrect explanation of capture variables in
    ProhibitCaptureWithoutTest
  - Fixed incorrect links
  - Fixed incorrect example for returning a sorted list
  - Fixed invalid POD (GH#735)
  - Updated docs on ProhibitYadaOperator (GH#662)
  - Removed all the references to the old mailing list and code repository at
    tigris.org (GH#757)
- This release by PETDANCE → update source URL

* Wed Jun 07 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.126-8
- Perl 5.26 re-rebuild of bootstrapped packages

* Tue Jun 06 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.126-7
- Perl 5.26 rebuild

* Wed May 24 2017 Paul Howarth <paul@city-fan.org> - 1.126-6
- Fix t/07_perlcritic.t for @INC without '.' (GH#738)
- Drop legacy Group: tags

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.126-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed May 18 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.126-4
- Perl 5.24 re-rebuild of bootstrapped packages

* Mon May 16 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.126-3
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.126-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Aug 11 2015 Paul Howarth <paul@city-fan.org> - 1.126-1
- Update to 1.126
  - Added a policy: ControlStructures::ProhibitYadaOperator - Never use ... in
    production code
  - Fixed problems arising from having -b in your .perltidyrc file
  - Removed extra newline from policy names returned by P::C::Config->policies
  - 'fc' and 'say' are now covered by ProhibitUselessTopic
  - Add more strict/warnings importer modules
  - Path::Tiny is now recommended over File::Slurp
  - Micro-optimize by calling ->content() directly instead of going through the
    overloads
  - Square brackets are now allowed around your '## no critic' policy list

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.125-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 10 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.125-3
- Perl 5.22 re-rebuild of bootstrapped packages

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.125-2
- Perl 5.22 rebuild

* Tue Mar  3 2015 Paul Howarth <paul@city-fan.org> - 1.125-1
- Update to 1.125
  - Corrected dependency on List::Util::any() to List::MoreUtils::any()
  - Revised and updated documentation
- Drop upstreamed patch for GH #626

* Sat Feb 28 2015 Paul Howarth <paul@city-fan.org> - 1.124-1
- Update to 1.124
  - The ProhibitUnusedPrivateSubroutines policy can now ignore files that use
    particular modules with the 'skip_when_using' option, which allows, for
    example, skipping the policy for roles
  - The RequireUseStrict and RequireUseWarnings policies now regard Moose, Moo,
    Mouse, Dancer, Mojolicious, and several other modules as equivalent to the
    strict and warnings pragma
  - The RequireChecked* family of policies has been fixed to accommodate
    version numbers when use-ing the autodie pragma (GH #612)
- Add patch to avoid the need for List::Util ≥ 1.33 (GH #626)

* Wed Nov 12 2014 Paul Howarth <paul@city-fan.org> - 1.123-1
- Update to 1.123
  - Now requires PPI-1.220 which has numerous bug fixes; this may eliminate
    the need for some "## no critic" markers you inserted to work around those
    bugs - the "ProhibitUselessNoCritic" policy should help you find them
  - Fixed a typo in the Variables::ProhibitPerl4PackageNames message

* Sun Sep 07 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.122-3
- Perl 5.20 re-rebuild of bootstrapped packages

* Fri Aug 29 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.122-2
- Perl 5.20 rebuild

* Mon Aug 25 2014 Paul Howarth <paul@city-fan.org> - 1.122-1
- Update to 1.122
  - Now requires PPI-1.218, which has numerous enahncements and bug fixes
  - Also now requires Readonly-2.00, which obviates the need for Readonly::XS
    to get fast constants
  - File::HomeDir, File::Which, and Term::ANSIColor are all required now
    instead of being optional or recommended; this simplifies our test code
    and ensures consistent optimal behavior for all users
  - Added two new policies: BuiltinFunctions::ProhibitUselessTopic and
    RegularExpressions::ProhibitUselessTopic
  - Updated the perlcritic.el script to use modern Emacs hooks (GH #556)
  - Removed all the internal RCS keyword boilerplate blocks that were never
    getting expanded
- Use %%license where possible
- Drop upstreamed patches

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.121-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May  2 2014 Paul Howarth <paul@city-fan.org> - 1.121-3
- Add upstream fix for Build.PL to work with current toolchain, and reinstate
  use of "Build authortest"

* Wed Apr 30 2014 Paul Howarth <paul@city-fan.org> - 1.121-2
- xt/author/82_optional_modules.t shouldn't be trying to use Readonly::XS (#1092921)
- Run the author tests using "Build test" rather than "Build authortest" because the
  latter ends up deleting META.yml and that causes the kwalitee test to fail

* Mon Nov  4 2013 Paul Howarth <paul@city-fan.org> - 1.121-1
- Update to 1.121
  - Added new themes based on CERT guidelines
  - The source code repository for Perl-Critic has been moved to GitHub at
    https://github.com/Perl-Critc/Perl-Critic; all tickets from the RT queue
    have also been moved there - please use GitHub for submitting any new bugs
    or corresponding about existing ones
  - The change log was reformatted to comply with CPAN::Changes::Spec
- BR: perl(Perl::Critic::Policy::Miscellanea::RequireRcsKeywords) for the
  extra tests
- Bump perl(Test::Kwalitee) version requirement to 1.15

* Sat Oct 26 2013 Paul Howarth <paul@city-fan.org> - 1.120-1
- Update to 1.120
  - Fix precedence error in Perl::Critic::Utils (CPAN RT#88866)

* Thu Sep 26 2013 Paul Howarth <paul@city-fan.org> - 1.119-1
- Update to 1.119
  - Tests were failing with Config::Tiny 2.17 or later, due to a change in the
    error messages produced by that module (CPAN RT#88679, CPAN RT#88889,
    https://github.com/Perl-Critic/Perl-Critic/pull/16)
  - BuiltinFunctions::ProhibitVoidGrep and ::ProhibitVoidMap: grep and map
    called as functions are now allowed in slice operations (CPAN RT#79289)
  - Subroutines::RequireArgUnpacking: most tests of the size of @_ are now
    allowed (CPAN RT#79138)
  - Modernized our usage of Exporter (CPAN RT#75300)
- Drop redundant patch for CPAN RT#87875

* Wed Aug 14 2013 Jitka Plesnikova <jplesnik@redhat.com> - 1.118-7
- Perl 5.18 re-rebuild of bootstrapped packages
- Remove MailingList from Build.PL to fix author test failure (CPAN RT#87875)

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.118-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 30 2013 Petr Pisar <ppisar@redhat.com> - 1.118-5
- Perl 5.18 rebuild

* Thu Jun 20 2013 Paul Howarth <paul@city-fan.org> - 1.118-4
- BR: perl(Fatal) for the test suite

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.118-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.118-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jul 11 2012 Paul Howarth <paul@city-fan.org> - 1.118-1
- update to 1.118
  Policy Changes:
  - CodeLayout::RequireTidyCode: revise to work with incompatible changes in
    Perl::Tidy 20120619 (CPAN RT#77977)
  - TestingAndDebugging::ProhibitNoWarnings: correct the parse of the
    'no warnings' statement, so that 'no warnings "qw"' is recognized as
    suppressing just 'qw' warnings (CPAN RT#74647)
  - Miscellanea::RequireRcsKeywords has been moved to the Perl-Critic-More
    distribution (CPAN RT#69546)
  Other Changes:
  - make all unescaped literal "{" characters in regexps into character
    classes; these are deprecated, and became noisy with Perl 5.17.0
    (CPAN RT#77510)
- drop now-redundant patch for Perl::Tidy compatibility
- BR: perl(lib) for the build process
- BR: perl(base), perl(PPIx::Utilities::Node) and perl(Test::Builder) ≥ 0.92
  for the module (Test::Builder required by Test::Perl::Critic::Policy)
- BR: perl(Exporter) ≥ 5.58; with older versions we get:
  ":color_severity" is not exported by the Perl::Critic::Utils::Constants module
- BR: perl(File::Spec::Functions) for the test suite
- drop buildreqs for perl(charnames), perl(File::Basename), perl(File::Find),
  perl(overload), perl(strict) and perl(warnings) - not dual lived

* Tue Jul 10 2012 Petr Pisar <ppisar@redhat.com> - 1.117-9
- Perl 5.16 re-rebuild of bootstrapped packages

* Tue Jul 10 2012 Paul Howarth <paul@city-fan.org> - 1.117-8
- fix breakage with Perl::Tidy ≥ 20120619 (CPAN RT#77977)

* Tue Jul 10 2012 Petr Pisar <ppisar@redhat.com> - 1.117-7
- Perl 5.16 re-rebuild of bootstrapped packages

* Wed Jun 20 2012 Petr Pisar <ppisar@redhat.com> - 1.117-6
- Perl 5.16 rebuild

* Thu Jun  7 2012 Marcela Mašláňová <mmaslano@redhat.com> - 1.117-5
- conditionalize aspell

* Tue Apr 24 2012 Petr Pisar <ppisar@redhat.com> - 1.117-4
- do not use Test::Kwalitee on RHEL ≥ 7

* Tue Feb 28 2012 Paul Howarth <paul@city-fan.org> - 1.117-3
- spec clean-up
  - separate build requirements and runtime requirements
  - drop redundant %%{?perl_default_filter}
  - fix permissions verbosely
  - use tabs

* Thu Jan 12 2012 Paul Howarth <paul@city-fan.org> - 1.117-2
- drop %%defattr, no longer needed

* Thu Dec 22 2011 Paul Howarth <paul@city-fan.org> - 1.117-1
- update to 1.117
  New Policies:
  - Variables::ProhibitAugmentedAssignmentInDeclaration reports constructs like
    'my $x += 1'
  Policy Changes:
  - BuiltinFunctions::ProhibitLvalueSubstr: add explicit 'use version'
    (CPAN RT#68498)
  - CodeLayout::ProhibitHardTabs: add 'pbp' to the default_themes list
    (CPAN RT#71093)
  - ControlStructures::ProhibitMutatingListFunctions now understands that
    tr///r (introduced in 5.13.7) does not change its operand
  - ControlStructures::ProhibitMutatingListFunctions now understands that
    '//=', '<<=', and '>>=' are assignment operators (CPAN RT#70901)
  - ErrorHandling::RequireCheckingReturnValueOfEval now allows things
    like grep { eval $_ } (CPAN RT#69489)
  - Modules::RequireExplicitPackage now has configuraion option
    allow_import_of, to allow the import of specified modules before the
    package statement (CPAN RT#72660)
  - RegularExpressions::ProhibitEnumeratedClasses no longer thinks
    that [A-Za-z_] matches \w. RT #69322.
  - RegularExpressions::ProhibitUnusedCaptures now skips the first block of
    an 'if' or 'elsif' if the regular expression is bound to its operand with
    the '!~' operator (CPAN RT#69867)
  - RegularExpressions::ProhibitUnusedCaptures now looks into lists and blocks
    in the replacement portion of the regular expression if /e is asserted
    (CPAN RT#72086)
  - RegularExpressions::RequireDotMatchAnything,
    RegularExpressions::RequireExtendedFormatting and
    RegularExpressions::RequireLineBoundaryMatching now honor defaults set with
    'use re "/modifiers"' (CPAN RT#72151)
  - Subroutines::ProhibitManyArgs now recognizes '+' as a prototype character
  - Variables::ProhibitPunctuationVars now recognizes bracketed variables
    embedded in interpolated strings (e.g. "${$}"); for the purpose of the
    'allow' configuration, these are considered equivalent to the unbracketed
    form (CPAN RT#72910)
  Other Changes:
  - corrected POD in Perl::Critic::PPI::Utils (CPAN RT#68898)
  - Perl::Critic::Violation source() method now returns the line containing
    the violation (not the first line) when the statement containing the
    violation spans multiple lines
- this release by THALJEF -> update source URL
- drop stopwords patch, now included upstream

* Fri Jul 22 2011 Paul Howarth <paul@city-fan.org> - 1.116-6
- reinstate author tests: META.yml creation issue fixed in perl-5.14.1-182

* Fri Jul 22 2011 Petr Sabata <contyk@redhat.com> - 1.116-5
- completely disable author tests to avoid Kwalitee META complaints

* Thu Jul 21 2011 Petr Sabata <contyk@redhat.com> - 1.116-4
- Perl mass rebuild

* Wed Jul 20 2011 Petr Sabata <contyk@redhat.com> - 1.116-3
- Perl mass rebuild

* Wed Jun 29 2011 Paul Howarth <paul@city-fan.org> - 1.116-2
- move BR: perl(Test::Perl::Critic) to author test section where it belongs
- run the author tests if we're not bootstrapping

* Mon May 16 2011 Paul Howarth <paul@city-fan.org> - 1.116-1
- update to 1.116
  - BuiltInFunctions::ProhibitLvalueSubstr does not report violations if the
    document contains an explicit 'use n.nnn;' where the version is before
    5.005 (CPAN RT#59112)
  - Documentation::RequirePodSections no longer blows up on code having POD but
    no =head1 (CPAN RT#67231)
  - RegularExpressions::ProhibitUnusedCapture should more reliably find things
    like s/(a)/${1}2/ (CPAN RT#67273)
  - ValuesAndExpressions::ProhibitMagicNumbers and Module::RequireVersionVar
    now treat versions passed as the second argument of a 'package' statement
    the same as versions declared as 'our $VERSION ...' (CPAN RT#67159)
  - Variables::RequireLexicalLoopIterators does not report violations if the
    document contains an explicit 'use n.nnn;' where the version is before
    5.004 (CPAN RT#67760)

* Fri Apr  1 2011 Paul Howarth <paul@city-fan.org> - 1.115-1
- update to 1.115
  - fatal error in RegularExpressions::ProhibitUnusedCapture here document
    check (CPAN RT#67116)
  - internal POD error in Documentation::RequirePodLinksIncludeText
    (CPAN RT#67012)

* Tue Mar 29 2011 Paul Howarth <paul@city-fan.org> 1.114-1
- update to 1.114
  - Documentation::RequirePodLinksIncludeText now handles nested POD formatting
    (CPAN RT#65569)
  - clarified relation of severity numbers to names in Perl::Critic POD
    (CPAN RT#66017)
  - removed caveats from Variables::RequireLocalizedPunctuationVars, no longer
    necessary with PPI 1.208 (CPAN RT#65514)
  - have InputOutput::RequireBriefOpen attempt to expand scope as necessary to
    deal with the case where the open() and the corresponding close() are not
    in the same scope (CPAN RT#64437)
  - RegularExpressions::ProhibitUnusedCapture now looks inside double-quotish
    things (CPAN RT#38942)
  - RegularExpressions::ProhibitUnusedCapture now takes logical alternation
    into account, so that (e.g.)
	if ( /(a)/ || /(b)/ ) {
		say $1;
	}
    is not a violation (CPAN RT#38942)
  - ValuesAndExpressions::ProhibitCommaSeparatedStatements now recognizes
    'return { foo => 1, bar => 2 }' as containing a hash constructor, not a
    block; this was fixed by PPI 1.215 (CPAN RT#61301)
  - ValuesAndExpressions::ProhibitCommaSeparatedStatements now recognizes
    'bless { foo => 1, bar => 2 }' as containing a hash constructor, not a
    block; this was fixed by PPI 1.215 (CPAN RT#64132)
- bump PPI version requirement to 1.215
- BR/R: perl(Pod::Parser)
- BR/R: optional modules perl(Readonly::XS), perl(Term::ANSIColor) >= 2.02
- BR: perl(Pod::Spell) >= 1
- BR: perl(Text::ParseWords) >= 3
- add runtime deps for optional modules perl(File::HomeDir), perl(File::Which)
- drop redundant (for modern rpm) BuildRoot tag and buildroot cleaning
- split Test::Perl::Critic::Policy off into its own package
- add dependency on aspell for Perl::Critic::Policy::Documentation::PodSpelling
- add version 1.889 requirement for perl(Email::Address)
- add version 0.19 requirement for perl(List::MoreUtils)
- add version 0.010 requirement for perl(PPIx::Regexp)
- add version 1.001 requirement for perl(PPIx::Utilities::Statement)
- add version 0.77 requirement for perl(version)
- drop unused buildreq perl(Test::Spelling)
- drop bogus buildreqs perl(lib) and perl(base)
- add option for building with author tests enabled (--with authortests)
- add patch with words not in Fedora dictionaries for spell check tests
- split buildreqs into separate sections for build process, the module, the
  main test suite and the author tests

* Mon Mar  7 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.113-1
- update to 1.113

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.111-2
- rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jan  3 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.111-1
- update

* Tue Dec 21 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.108-2
- rebuild to fix problems with vendorarch/lib (#661697)

* Fri Aug  6 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.108-1
- update

* Tue May 04 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.105-4
- mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.105-3
- rebuild against perl 5.10.1

* Wed Nov 25 2009 Stepan Kasal <skasal@redhat.com> - 1.105-2
- use the new filtering macros (verified that the resulting provides
  and requires are the same)
- add version to perl(PPI) require (#541020)

* Wed Oct  7 2009 Stepan Kasal <skasal@redhat.com> - 1.105-1
- new upstream version
- update build requires

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.098-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun May 17 2009 Chris Weyl <cweyl@alumni.drew.edu> 1.098-1
- "neaten" filtering
- auto-update to 1.098 (by cpan-spec-update 0.01)
- added a new br on perl(strict) (version 0)
- added a new br on perl(Scalar::Util) (version 0)
- added a new br on perl(File::Temp) (version 0)
- added a new br on perl(Pod::Usage) (version 0)
- added a new br on perl(File::Find) (version 0)
- added a new br on perl(PPI::Token::Whitespace) (version 1.203)
- added a new br on perl(charnames) (version 0)
- added a new br on perl(PPI::Document::File) (version 1.203)
- added a new br on perl(File::Spec::Unix) (version 0)
- added a new br on perl(List::Util) (version 0)
- added a new br on perl(lib) (version 0)
- added a new br on perl(Getopt::Long) (version 0)
- added a new br on perl(Exporter) (version 0)
- added a new br on perl(Test::More) (version 0)
- added a new br on perl(overload) (version 0)
- added a new br on perl(base) (version 0)
- added a new br on perl(version) (version 0)
- added a new br on perl(Carp) (version 0)
- added a new br on perl(warnings) (version 0)
- added a new br on perl(PPI::Document) (version 1.203)
- added a new br on perl(File::Basename) (version 0)
- added a new br on perl(PPI::Token::Quote::Single) (version 1.203)
- added a new br on perl(File::Spec) (version 0)
- added a new br on perl(File::Path) (version 0)
- added a new br on perl(Pod::PlainText) (version 0)
- added a new br on perl(Pod::Select) (version 0)
- added a new br on perl(PPI::Node) (version 1.203)
- added a new br on perl(English) (version 0)

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.092-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Sep 08 2008 Chris Weyl <cweyl@alumni.drew.edu> 1.092-1
- update to 1.092

* Sun Mar 09 2008 Chris Weyl <cweyl@alumni.drew.edu> 1.082-1
- update to 1.082
- resolve BZ#431577
- add t/ examples/ extras/ tools/, and filter

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.080-3
- Rebuild for perl 5.10 (again)

* Mon Jan 14 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.080-2
- add missing BR: perl-Exception-Class

* Mon Jan 14 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.080-1
- bump to 1.080

* Mon Jan 14 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.053-2
- rebuild for new perl

* Sat Jun 16 2007 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.053-1
- Update to 1.053.

* Tue Mar 20 2007 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.05-1
- Update to 1.05.

* Thu Feb 15 2007 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.03-1
- Update to 1.03.

* Fri Jan 26 2007 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.01-2
- Bumping release (forgot to commit sources and .cvsignore changes).

* Fri Jan 26 2007 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.01-1
- Update to 1.01.
- New build requirement: perl(Test::Memory::Cycle).

* Thu Jan 25 2007 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.23-2
- perl(Set::Scalar) is no longer required.

* Wed Jan 24 2007 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.23-1
- Update to 0.23.
- New requirement: perl(B::Keywords).
- Author tests coverage improved.

* Sun Dec 17 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.22-2
- Enabled author tests.
- BR perl(HomeDir).

* Sun Dec 17 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.22-1
- Update to 0.22.

* Sat Nov 11 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.21-1
- Update to 0.21.
- New BR: perl(Set::Scalar).

* Sat Sep 16 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.2-1
- First build.
