Vendor:         Microsoft Corporation
Distribution:   Mariner
Name:           perl-Parse-RecDescent
Version:        1.967015
Release:        11%{?dist}
Summary:        Generate Recursive-Descent Parsers
License:        (GPL+ or Artistic) and (GPLv2+ or Artistic)
# demo/demo_another_Cgrammar.pl:    GPLv2+ or Artistic
URL:            https://metacpan.org/release/Parse-RecDescent
Source0:        https://cpan.metacpan.org/authors/id/J/JT/JTBRAUN/Parse-RecDescent-%{version}.tar.gz#/perl-Parse-RecDescent-%{version}.tar.gz
Patch0:         Parse-RecDescent-1.967002-utf8.patch
BuildArch:      noarch
# Build:
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl-interpreter
BuildRequires:  perl-generators
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.58
BuildRequires:  perl(warnings)
# Run-time
BuildRequires:  perl(Carp)
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(strict)
BuildRequires:  perl(Text::Balanced) >= 1.95
BuildRequires:  perl(vars)
# Tests:
BuildRequires:  perl(Test::More)
# Optional tests:
BuildRequires:  perl(Test::Pod) >= 1.14
BuildRequires:  perl(Test::Warn)
# Runtime
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:       perl(Data::Dumper)

%description
Parse::RecDescent incrementally generates top-down recursive-descent
text parsers from simple yacc-like grammar specifications. It
provides:

 * Regular expressions or literal strings as terminals (tokens)
 * Multiple (non-contiguous) productions for any rule
 * Repeated and optional subrules within productions
 * Full access to Perl within actions specified as part of the grammar
 * Simple automated error reporting during parser generation and parsing
 * The ability to commit to, uncommit to, or reject particular
   productions during a parse
 * The ability to pass data up and down the parse tree ("down" via
   subrule argument lists, "up" via subrule return values)
 * Incremental extension of the parsing grammar (even during a parse)
 * Precompilation of parser objects
 * User-definable reduce-reduce conflict resolution via "scoring" of
   matching productions

%prep
%setup -q -n Parse-RecDescent-%{version}

# Recode as UTF8
%patch0 -p1

# Fix permissions and script interpreters
chmod -c a-x demo/* tutorial/*
perl -pi -e 's|^#!\s?/usr/local/bin/perl\b|#!/usr/bin/perl|' demo/*

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
%doc Changes README ToDo demo/ tutorial/
%{perl_vendorlib}/Parse/
%{_mandir}/man3/Parse::RecDescent.3*

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.967015-11
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.967015-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.967015-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.967015-8
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.967015-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.967015-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.967015-5
- Perl 5.28 rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.967015-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.967015-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.967015-2
- Perl 5.26 rebuild

* Wed Apr 05 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.967015-1
- Update to 1.967015

* Sun Apr  2 2017 Paul Howarth <paul@city-fan.org> - 1.967014-1
- Update to 1.967014
  - Add a newline to package declaration lines in precompiled parsers, to keep
    CPAN from indexing them (CPAN RT#110404)
  - Provide repository and bugtracker entries in MYMETA.* (CPAN RT#110403)
  - Update tests to handle '.' no longer being part of @INC in perl-5.26.0
    (CPAN RT#120415)

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.967013-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.967013-3
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.967013-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Sep 28 2015 Paul Howarth <paul@city-fan.org> - 1.967013-1
- Update to 1.967013
  - Wrap Data::Dumper->Dump() to localize some $Data::Dumper::VARS to control
    the dumped output; in particular, Data::Dumper::Terse=1 was reported to
    break parser generation (CPAN RT#107355)

* Mon Sep 14 2015 Paul Howarth <paul@city-fan.org> - 1.967012-1
- Update to 1.967012
  - Base the standalone precompiled parser's runtime name on the parser's
    class, rather than use the fixed "Parse::RecDescent::_Runtime"; this
    prevents "already defined" warnings when two standalone precompiled
    parsers are used
  - Add support for allowing precompiled parsers to share a common runtime via
    the Precompile({-runtime_class}) option and the PrecompiledRuntime()
    function
  - Warn on creation of Precompiled parsers that depend on Parse::RecDescent
  - NON-BACKWARDS COMPATIBLE CHANGE: Change the global <skip:> directive to
    use eval similarly to the other <skip:> directives, rather than being
    single-quoted in the resulting parser
  - Correct some typos in the documentation (CPAN RT#87185)
  - Sort hash keys and rulenames when generating code; this keeps the output
    text for a given input text the same, reducing differences in automated
    builds (CPAN RT#102160)
  - Precompiled parsers now document which $Parse::RecDescent::VERSION was
    used to generate them (CPAN RT#77001)
- Switch to ExtUtils::MakeMaker flow

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.967009-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jun 05 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.967009-10
- Perl 5.22 rebuild

* Thu Aug 28 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.967009-9
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.967009-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.967009-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul 22 2013 Petr Pisar <ppisar@redhat.com> - 1.967009-6
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.967009-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Nov 01 2012 Petr Pisar <ppisar@redhat.com> - 1.967009-4
- One demo file is licensed as (GPLv2+ or Artistic)

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.967009-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 14 2012 Petr Pisar <ppisar@redhat.com> - 1.967009-2
- Perl 5.16 rebuild

* Mon Mar 19 2012 Petr Pisar <ppisar@redhat.com> - 1.967009-1
- 1.967009 bump

* Sat Feb 11 2012 Paul Howarth <paul@city-fan.org> - 1.967006-1
- Update to 1.967006 (#789560)
  - Localize the OUT filehandle during Precompile
  - Document the <autotree:Base::Class> form of the <autotree> directive
  - Provide a simple test for the <autotree> directive, t/autotree.t; renamed
    basics.t to ensure it runs before autotree.t
  - Allow a global <skip:> directive that functions the same as modifying
    $Parse::RecDescent::skip prior to compiling a grammar
  - Require that the $file returned by caller() be eq '-', rather than merely
    starting with '-'
  - Warn on empty productions followed by other productions: the empty
    production always matches, so following productions will never be reached
  - NON-BACKWARDS COMPATIBLE CHANGE: a repetition directive such as 'id(s /,/)'
    correctly creates a temporary @item variable to hold the 'id's that are
    matched. That @item variable is then used to set the real $item[] entry for
    that repetition. The same treatment is now given to %%item. Formerly, in a
    production like:
      id ',' id(s /,/)
    matched against:
      xxx, yyy, zzz
    The $item{id} entry that should be 'xxx' is overwritten by 'yyy' and then
    'zzz' prior to the action being executed. Now 'yyy' and 'zzz' set
    $item{id}, but in the private %%item, which goes out of scope once the
    repetition match completes.
  - EXPERIMENTAL: when precompiling, optionally create a standalone parser by
    including most of the contents of Parse::RecDescent in the resulting
    Precompiled output
  - Accept an optional $options hashref to Precompile, which can be used to
    specify $options->{-standalone}, which currently defaults to false
  - The subroutines import, Precompile and Save are not included in the
    Precompile'd parser
  - The included Parse::RecDescent module is renamed to
    Parse::RecDescent::_Runtime to avoid namespace conflicts with an installed
    and use'd Parse::RecDescent
  - Add a new t/precompile.t to test precompilation
  - Add a new $_FILENAME global to Parse::RecDescent to make it easy for the
    Precompile method to find the module
  - Remove the prototype from _generate; it is not required, and it caused
    t/precompile.t (which ends up re-defining a lot of Parse::RecDescent
    subroutines) to fail needlessly, as the calls to _generate in Replace and
    Extend normally do not see the prototype, but do when re-defined
  - POD documentation for standalone parsers added
  - Added ExtUtils::MakeMaker build/configure version requirements
    (CPAN RT#74787)
- BR: perl(Test::Pod) and perl(Test::Warn) for additional test coverage
- Use a patch rather than scripted iconv to fix character encoding
- Improve %%summary
- Tidy %%description
- Make %%files list more explicit
- Don't use macros for commands
- Don't need to specify compiler flags for pure-perl package
- Drop redundant 'find' commands from %%install

* Tue Jan 31 2012 Petr Šabata <contyk@redhat.com> - 1.967003-1
- 1.967003 bump (backwards-incompatible changes)
- Spec cleanup and modernization
- New Source URL
- Install to vendor

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.965001-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.965001-4
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.965001-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 21 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.965001-2
- rebuild to fix problems with vendorarch/lib (#661697)

* Fri Sep 24 2010 Marcela Mašláňová <mmaslano@redhat.com> 1.965001-1
- update
- use Module::Build

* Tue May 04 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.964-2
- Mass rebuild with perl-5.12.0

* Fri Feb 19 2010 Marcela Mašláňová <mmaslano@redhat.com> 1.964-1
- update, fix previous issue and https://rt.cpan.org/Public/Bug/Display.html?id=53948

* Tue Feb 16 2010 Marcela Mašláňová <mmaslano@redhat.com> 1.963-2
- apply upstream patch https://rt.cpan.org/Public/Bug/Display.html?id=54457
  which should fix problems with rebuilds of other modules

* Tue Feb  9 2010 Paul Howarth <paul@city-fan.org> 1.963-1
- update to 1.963 (fix subtle bug in leftop and rightop due to removal of $&)
- recode Changes as utf-8
- more script interpreter fixes

* Sun Sep 27 2009 Chris Weyl <cweyl@alumni.drew.edu> 1.962.2-1
- updated for latest GA SQL::Translator
- add default filtering
- auto-update to 1.962.2 (by cpan-spec-update 0.01)
- added a new br on perl(Text::Balanced) (version 0)

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.96-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.96-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb  2 2009 Stepan Kasal <skasal@redhat.com> - 1.96-1
- new upstream version

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.95.1-5
- Rebuild for perl 5.10 (again)

* Sun Jan 20 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.95.1-4
- rebuild for new perl

* Wed Nov 14 2007 Robin Norwood <rnorwood@redhat.com> - 1.95.1-3
- Apply fixes from package review:
  - Remove BR: perl
  - Use iconv to convert file to utf-8
  - Include BR: perl(Test::Pod)
  - Fix old changelog entry
- Resolves: bz#226274

* Tue Oct 16 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 1.95.1-2
- add BR: perl(version), perl(Test::More)

* Tue Oct 16 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 1.95.1-1
- bump to 1.95.1
- correct license tag (now under perl license)
- add BR: perl(ExtUtils::MakeMaker)

* Fri Jul 20 2007 Robin Norwood <rnorwood@redhat.com> - 1.94-6.fc8
- Bring fixes from EPEL build into F8
- Fix minor specfile issues
- Package the docs as well

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.94-5.2.1
- rebuild

* Fri Feb 03 2006 Jason Vas Dias <jvdias@redhat.com> - 1.94-5.2
- rebuild for new perl-5.8.8

* Fri Dec 16 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt for new gcc

* Fri Dec 16 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt for new gcj

* Thu Apr 21 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.94-5
- #155620
- Bring up to date with current Fedora.Extras perl spec template.

* Wed Sep 22 2004 Chip Turner <cturner@redhat.com> 1.94-4
- rebuild

* Tue Feb 17 2004 Chip Turner <cturner@redhat.com> 1.94-2
- fix rm to not be interactive (bz115997)

* Fri Feb 13 2004 Chip Turner <cturner@redhat.com> 1.94-1
- update to 1.94

* Tue Aug  6 2002 Chip Turner <cturner@redhat.com>
- automated release bump and build

* Sat Jul 20 2002 Chip Turner <cturner@localhost.localdomain>
- remove Text::Balanced modules since they are now in core perl

* Thu Jun 27 2002 Chip Turner <cturner@redhat.com>
- description update

* Fri Jun 07 2002 cturner@redhat.com
- Specfile autogenerated
