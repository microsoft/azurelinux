# PPI::XSAccessor is experimental
%bcond_without XSAccessor

Name:           perl-PPI
Version:        1.279
Release:        1%{?dist}
Summary:        Parse, Analyze and Manipulate Perl
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://metacpan.org/release/PPI
Source0:        https://cpan.metacpan.org/modules/by-module/PPI/PPI-%{version}.tar.gz
BuildArch:      noarch
# =============== Module Build ======================
BuildRequires:  coreutils
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(ExtUtils::MakeMaker) > 6.75
BuildRequires:  perl(Task::Weaken)
BuildRequires:  perl(warnings)
BuildRequires:  sed
# =============== Module Runtime ====================
BuildRequires:  perl(Carp)
BuildRequires:  perl(Clone) >= 0.30
BuildRequires:  perl(constant)
BuildRequires:  perl(Digest::MD5) >= 2.35
BuildRequires:  perl(Exporter)
BuildRequires:  perl(File::Path)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(if)
BuildRequires:  perl(List::Util) >= 1.33
BuildRequires:  perl(overload)
BuildRequires:  perl(Params::Util) >= 1.00
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(Storable) >= 2.17
BuildRequires:  perl(strict)
# =============== Test Suite ========================
BuildRequires:  perl(B)
BuildRequires:  perl(Class::Inspector) >= 1.22
BuildRequires:  perl(CPAN::Meta) >= 2.120900
BuildRequires:  perl(Encode)
BuildRequires:  perl(File::Copy)
BuildRequires:  perl(File::Spec::Functions)
BuildRequires:  perl(File::Temp)
BuildRequires:  perl(lib)
BuildRequires:  perl(parent)
BuildRequires:  perl(Test::More) >= 0.96
BuildRequires:  perl(Test::NoWarnings)
BuildRequires:  perl(Test::Object) >= 0.07
BuildRequires:  perl(Test::SubCalls) >= 1.07
BuildRequires:  perl(Test::Warnings)
BuildRequires:  perl(Time::HiRes)
BuildRequires:  perl(utf8)
# =============== Dependencies ======================
# Run-require Task::Weaken, see Changes for more details.
Requires:       perl(Task::Weaken)

# Filter out redundant unversioned provides
%global __provides_exclude ^perl\\(PPI::.+\\)$

%description
Parse, analyze and manipulate Perl (without perl).

%prep
%setup -q -n PPI-%{version}

# Fix bogus exec permissions
chmod -c -x Changes LICENSE README

%if %{without XSAccessor}
rm lib/PPI/XSAccessor.pm
sed -i '/^lib\/PPI\/XSAccessor\.pm$/d' MANIFEST
%endif

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
%doc Changes README
%{perl_vendorlib}/PPI/
%{perl_vendorlib}/PPI.pm
%{_mandir}/man3/PPI*.3*

%changelog
* Mon Feb 27 2025 Sumit Jena <v-sumitjena@microsoft.com> - 1.279-1
- Update to version 1.279
- License verified

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.270-4
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.270-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.270-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Jul 10 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.270-1
- Update to 1.270
  - Attempt to handle new blead binary/hexadecimal parsing behavior in tests

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.269-2
- Perl 5.30 rebuild

* Sun May 19 2019 Paul Howarth <paul@city-fan.org> - 1.269-1
- Update to 1.269
  - Many small documentation improvements

* Thu May 16 2019 Paul Howarth <paul@city-fan.org> - 1.268-1
- Update to 1.268
  - Make PPI::Test::Run more OS-agnostic
  - Fix a broken link in the pod

* Thu May 16 2019 Paul Howarth <paul@city-fan.org> - 1.266-1
- Update to 1.266
  - Prevent heredoc terminator detection triggering regex errors
  - Small clean-ups
- Work around test failures caused by DOS line endings in test data files
  (https://github.com/adamkennedy/PPI/issues/243)

* Wed May 15 2019 Paul Howarth <paul@city-fan.org> - 1.265-1
- Update to 1.265
  - Simplified a code construct

* Mon Apr 29 2019 Paul Howarth <paul@city-fan.org> - 1.264-1
- Update to 1.264
  - Keep vstring processing from swallowing underscores

* Sun Apr 28 2019 Paul Howarth <paul@city-fan.org> - 1.262-1
- Update to 1.262
  - Add support for the double diamond (<<>>) input operator
  - Adjust position of a todo marker to not catch a passing test
  - Recognize `for (;<$foo>;) {}` as containing a readline operator
  - Remove accidentally included use of Test::InDistDir
  - Allow all PPI::Document instances to have a filename attribute
  - Allow underscores in vstrings
  - Convert newlines in some raw test files from win32 to unix

* Fri Apr 26 2019 Paul Howarth <paul@city-fan.org> - 1.250-1
- Update to 1.250
  - Support postfix dereference
  - Add support for lexical subroutines from perl-5.26
  - Support key-value and index-value slices in PPI::Token::Symbol symbol
    method
  - Support indented here-docs
  - Parse list-embedded curlies as hash constructors
  - Keep exponents of 2 or more zeroes from trapping PPI in an endless loop
  - Remove dependencies on vars, base and List::MoreUtils
  - Remove dependency on File::Remove
  - Reduce globals and cross-package variables
  - Move to Dist::Zilla
  - Add some tests including a TODO test for misparse bug on '(1)-1'
  - Allow tests to run without pre-determined module versions
  - Make xt/api.t skip/run properly
  - Fix some typos and formatting in Changes
  - Add travis-perl helper to be run before install
  - Update versions of Perl Travis tests on
- Modernize spec using %%{make_build} and %%{make_install}
- Don't try to run the release tests in the package build

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.236-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.236-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sun Jul 01 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.236-5
- Perl 5.28 re-rebuild of bootstrapped packages

* Fri Jun 29 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.236-4
- Perl 5.28 rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.236-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.236-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Jun 22 2017 Paul Howarth <paul@city-fan.org> - 1.236-1
- Update to 1.236
  - Prevent Node->child from proceeding without a valid argument
  - Make test pragma warning code enable -w to match warnings policy

* Wed Jun 21 2017 Paul Howarth <paul@city-fan.org> - 1.234-1
- Update to 1.234
  - Prevent sub names like v10 from being version strings (GH#65)
  - Add Changes entries forgotten in 1.230
  - Remove temporary fix introduced in 1.226
  - Prevent possible regex on undefined scalar in
    __current_token_is_forced_word

* Wed Jun 21 2017 Paul Howarth <paul@city-fan.org> - 1.228-1
- Update to 1.228
  - Fix test reliance on '.' in @INC
  - Temporary fix to keep an untested combination from blocking Perl::Critic
  - Keep PPI::Dumper from breaking Perl::Critic under cperl 5.27
- Fix upstream's temporary fix (GH#206, GH#212)

* Wed Jun 07 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.224-3
- Perl 5.26 re-rebuild of bootstrapped packages

* Mon Jun 05 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.224-2
- Perl 5.26 rebuild

* Tue May 16 2017 Paul Howarth <paul@city-fan.org> - 1.224-1
- Update to 1.224
  - Unit tests for many parts, both passing and TODO
  - Many documentation fixes
  - Add ->version method to PPI::Statement::Package
  - Remove unused PPI::Document->new timeout feature
  - Do not expect '.' in @INC
  - Many parsing fixes
  - Various fixes to the behaviors of methods
  - Removal of problematic dependencies
- Simplify find command using -delete
- Drop support for EL6/EL7 as they don't have List::Util ≥ 1.33

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.220-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed May 18 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.220-7
- Perl 5.24 re-rebuild of bootstrapped packages

* Mon May 16 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.220-6
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.220-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.220-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 10 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.220-3
- Perl 5.22 re-rebuild of bootstrapped packages

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.220-2
- Perl 5.22 rebuild

* Wed Nov 12 2014 Paul Howarth <paul@city-fan.org> - 1.220-1
- Update to 1.220
  - Incompatible behavior fixes on PPI::Statement::Sub->prototype
  - Improved parsing of various syntax elements
  - Code quality improvements
  - Various small documentation fixes
- BR: perl(IO::All) and perl(Capture::Tiny) to quieten warnings for author
  code during module build
- Fix line endings of new README.md file

* Sun Sep 07 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.218-3
- Perl 5.20 re-rebuild of bootstrapped packages

* Fri Aug 29 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.218-2
- Perl 5.20 rebuild

* Mon Aug 25 2014 Paul Howarth <paul@city-fan.org> - 1.218-1
- Update to 1.218
  - Fixes for various parsing and documentation bugs
  - 1MB limit on input document size removed
  - Moved repository to GitHub: https://github.com/adamkennedy/PPI
- This release by MITHALDU → update source URL
- Use %%license where possible

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.215-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Aug 14 2013 Jitka Plesnikova <jplesnik@redhat.com> - 1.215-14
- Perl 5.18 re-rebuild of bootstrapped packages

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.215-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 31 2013 Petr Pisar <ppisar@redhat.com> - 1.215-12
- Specify all dependencies

* Fri Jul 26 2013 Petr Pisar <ppisar@redhat.com> - 1.215-11
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.215-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Aug 25 2012 Paul Howarth <paul@city-fan.org> - 1.215-9
- classify buildreqs by usage
- BR: perl(Time::HiRes) for the test suite
- BR: perl(Pod::Simple) ≥ 3.14 for the release tests
- BR: at least version 0.17 of perl(Test::CPAN::Meta)
- bump perl(Test::Pod) version requirement to 1.44
- don't need to remove empty directories from the buildroot

* Thu Aug 16 2012 Petr Pisar <ppisar@redhat.com> - 1.215-8
- specify all dependencies

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.215-7
- rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 10 2012 Petr Pisar <ppisar@redhat.com> - 1.215-6
- perl 5.16 re-rebuild of bootstrapped packages

* Tue Jun 19 2012 Petr Pisar <ppisar@redhat.com> - 1.215-5
- perl 5.16 rebuild
- build-require Class::Inspector for tests

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.215-4
- rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Jul 21 2011 Paul Howarth <paul@city-fan.org> - 1.215-3
- always run test suite but don't run release tests when bootstrapping
- nobody else likes macros for commands
- clean up for modern rpm:
  - drop explicit buildroot tag
  - drop buildroot cleaning
  - drop %%defattr
  - use native provides filtering
- use a patch rather than scripting iconv to fix character encoding
- upstream file permissions no longer need fixing

* Tue Jun 28 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.215-2
- rebuild with Perl 5.14.1
- use perl_bootstrap macro

* Sun Mar 27 2011 Paul Howarth <paul@city-fan.org> - 1.215-1
- update to 1.215 (general fix release):
  - index_locations on an empty document no longer warns
  - Corrected a bug in line-spanning attribute support
  - Regression test for line-spanning attribute support
  - return { foo => 1 } should parse curlys as hash constructor, not block
    (CPAN RT#61305)
  - Fixed bug with map and regexp confusing PPI (CPAN RT#63943)
  - Updated copyright year to 2011
  - Fix bless {} probably contains a hash constructor (CPAN RT#64247)
  - Backed out glob fix
  - Fix cast can trump braces in PPI::Token::Symbol->symbol (CPAN RT#65199)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.213-3
- rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 21 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.213-2
- rebuild to fix problems with vendorarch/lib (#661697)

* Sat Jul 31 2010 Paul Howarth <paul@city-fan.org> - 1.213-1
- update to 1.213 (targeted bug fix, no changes to parsing or normal usage)
  - Updated to Module::Install 1.00
  - Updated module dependencies in xt author tests
  - Fixed extremely broken PPI::Token::Pod::merge and added test case
- bump perl(Perl::MinimumVersion) requirement to 1.25
- bump perl(Test::CPAN::Meta) requirement to 0.17
- bump perl(Test::Pod) requirement to 1.44

* Sat Jul 31 2010 Paul Howarth <paul@city-fan.org> - 1.212-1
- update to 1.212 (experimental/development support and bugfixes)
  - Fixed bug in ForLoop back-compatibility warning (CPAN RT#48819)
  - Added support for $ENV{X_TOKENIZER} --> $PPI::Lexer::X_TOKENIZER
  - Upgraded to Module::Install 0.93
  - Added support for $PPI::Lexer::X_TOKENIZER, for alternate tokenizers
  - Added an extra test case to validate we handle byte order marks properly
  - Moved author tests from t to xt
  - Fixed CPAN RT#26082: scalar { %%x } is misparsed
  - Fixed CPAN RT#26591: VMS patch for PPI 1.118
  - Fixed CPAN RT#44862: PPI cannot parse "package Foo::100;" correctly
  - Fixed CPAN RT#54208: PPI::Token::Quote::Literal::literal missing
- run release tests as well as regular test suite
- BR: perl(File::Find::Rule) >= 0.32, perl(File::Find::Rule::Perl) >= 1.09,
  perl(Perl::MinimumVersion) >= 1.24 and perl(Test::MinimumVersion) >= 0.101080
  for release tests

* Sat Jul 31 2010 Paul Howarth <paul@city-fan.org> - 1.210-1
- update to 1.210 (packaging fixes)
- use RELEASE_TESTING rather than AUTOMATED_TESTING for better test coverage

* Sat Jul 31 2010 Paul Howarth <paul@city-fan.org> - 1.209-1
- update to 1.209 (small optimisation release, no functional changes)

* Fri Jul 30 2010 Paul Howarth <paul@city-fan.org> - 1.208-1
- update to 1.208
  - don't assign '' to $^W, it generates a warning on Gentoo
  - added missing PPI::Token::Regexp fix to Changes file
  - updating Copyright to the new year
  - fixed #50309: literal() wrong result on "qw (a b c)"
  - PPI::Dumper no longer causes Elements to flush location data
  - PPI::Dumper no longer disables location information for non-Documents
  - +{ package => 1 } doesn't create a PPI::Statement::Package
  - extra methods in PPI::Token::Regexp and PPI::Token::QuoteLike::Regexp
- use %%{_fixperms} macro instead of our own chmod incantation

* Fri Jul 30 2010 Paul Howarth <paul@city-fan.org> - 1.206-6
- BR: perl(Task::Weaken) and perl(Test::CPAN::Meta) for improved test coverage
- enable AUTOMATED_TESTING
- use DESTDIR rather than PERL_INSTALL_ROOT

* Thu May 06 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.206-5
- Mass rebuild with perl-5.12.0

* Thu Feb 11 2010 Marcela Mašláňová <mmaslano@redhat.com> - 1.206-4
- fix filtering, provide versioned provides

* Wed Feb 10 2010 Marcela Mašláňová <mmaslano@redhat.com> - 1.206-3
- make rpmlint happy

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.206-2
- rebuild against perl 5.10.1

* Wed Oct  7 2009 Stepan Kasal <skasal@redhat.com> - 1.206-1
- new upstream version
- update build requires

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.203-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.203-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Sep  9 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.203-1
- update to 1.203

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.201-3
- Rebuild for perl 5.10 (again)

* Sun Jan 13 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.201-2
- rebuild for new perl

* Wed Dec 19 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 1.201-1
- bump to 1.201

* Sat Sep 23 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.118-1
- Update to 1.118.

* Wed Sep  6 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.117-1
- Update to 1.117.

* Sun Jun  4 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.115-2
- Removed the perl(IO::Scalar) build requirement.

* Sun Jun  4 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.115-1
- Update to 1.115.

* Wed May 10 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.113-1
- Update to 1.113.

* Tue Apr 25 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.112-1
- Update to 1.112.

* Sat Apr 22 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.111-1
- First build.
