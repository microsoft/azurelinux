# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           perl-Test-Spelling
Version:        0.25
Release:        19%{?dist}
Summary:        Check for spelling errors in POD files
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/Test-Spelling
Source0:        https://cpan.metacpan.org/modules/by-module/Test/Test-Spelling-%{version}.tar.gz
BuildArch:      noarch
# Module Build
BuildRequires:  coreutils
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
# Module Runtime
BuildRequires:  hunspell
BuildRequires:  perl(Carp)
BuildRequires:  perl(Exporter) >= 5.57
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(IPC::Run3) >= 0.044
BuildRequires:  perl(Pod::Spell) >= 1.01
BuildRequires:  perl(strict)
BuildRequires:  perl(Symbol)
BuildRequires:  perl(Test::Builder)
BuildRequires:  perl(Text::Wrap)
BuildRequires:  perl(warnings)
# Test Suite
BuildRequires:  glibc-langpack-en
BuildRequires:  hunspell-en
BuildRequires:  perl(Test::More) >= 0.88
BuildRequires:  perl(Test::Tester)
BuildRequires:  perl(utf8)
# Optional Tests
BuildRequires:  perl(CPAN::Meta) >= 2.120900
# Dependencies
Requires:       hunspell
Requires:       perl(Carp)

%description
"Test::Spelling" lets you check the spelling of a POD file, and report
its results in standard "Test::Simple" fashion. This module requires the
hunspell program.

%prep
%setup -q -n Test-Spelling-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%{make_build}

%install
%{make_install}
%{_fixperms} -c %{buildroot}

%check
LANG=en_US make test

%files
%license LICENSE
%doc Changes README
%{perl_vendorlib}/Test/
%{_mandir}/man3/Test::Spelling.3*

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.25-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.25-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.25-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.25-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.25-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.25-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.25-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.25-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jun 01 2022 Jitka Plesnikova <jplesnik@redhat.com> - 0.25-11
- Perl 5.36 rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.25-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.25-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sat May 22 2021 Jitka Plesnikova <jplesnik@redhat.com> - 0.25-8
- Perl 5.34 rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.25-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.25-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 0.25-5
- Perl 5.32 rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.25-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.25-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.25-2
- Perl 5.30 rebuild

* Wed May 29 2019 Paul Howarth <paul@city-fan.org> - 0.25-1
- Update to 0.25
  - Re-worded the documentation
  - Ordered documented functions in alphabetical order
  - Fixed up the synopsis
  - Put function usage examples directly below the function name; this makes it
    easier to get clickable links for functions in metacpan
  - Documented get_pod_parser
  - Moved hunspell up to the preferred checker

* Tue May 28 2019 Paul Howarth <paul@city-fan.org> - 0.24-1
- Update to 0.24
  - Fix up the prereqs somewhat
  - Revert the unicode support added in the last release as it caused some
    test breakage

* Wed May 22 2019 Paul Howarth <paul@city-fan.org> - 0.23-1
- Update to 0.23
  - Fixed some documentation errors
  - Added unicode support (GH#10)
  - Bump Perl prereq to 5.8 now that we support unicode
  - Don't inherit from Exporter (GH#9)
  - Bump Exporter prereq to 5.57

* Thu Apr 25 2019 Paul Howarth <paul@city-fan.org> - 0.22-1
- Update to 0.22
  - No . in @INC should no longer be an issue (CPAN RT#120425)
  - Removed the POD spelling test from /t as it's now in /xt
  - Forego usage of inc::Module::Install for EU::MM
  - List out all prereqs individually; provide cpanfile
  - Use dzil to build the dist
  - Convert the README to markdown
  - Add a LICENSE file
  - Clean up the Changes log
- Modernize spec using %%{make_build} and %%{make_install}

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.20-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.20-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jun 29 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.20-11
- Perl 5.28 rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.20-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.20-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jun 06 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.20-8
- Perl 5.26 rebuild

* Thu May 18 2017 Petr Pisar <ppisar@redhat.com> - 0.20-7
- Fix building on Perl without "." in @INC (CPAN RT#120425)

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.20-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon May 16 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.20-5
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.20-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.20-2
- Perl 5.22 rebuild

* Tue Oct  7 2014 Paul Howarth <paul@city-fan.org> - 0.20-1
- Update to 0.20
  - Add a sorted list of your most commonly misspelled words to the end of
    all_pod_files_spelling_ok to aid stopword list creation and bulk
    correction
- Classify buildreqs by usage
- Update hunspell preference patch

* Fri Aug 29 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.19-5
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.19-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.19-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Jul 21 2013 Petr Pisar <ppisar@redhat.com> - 0.19-2
- Perl 5.18 rebuild

* Sun May  5 2013 Paul Howarth <paul@city-fan.org> - 0.19-1
- Update to 0.19:
  - For more consistent results, avoid using the user's local aspell dictionary
    (CPAN RT#84869)
- Update hunspell preference patch

* Fri Apr 26 2013 Paul Howarth <paul@city-fan.org> - 0.18-1
- Update to 0.18:
  - Work around Pod::Spell limitations
  - Improve case handling
  - Improve test failure reporting
  - Include more useful info in Test-Spelling's own test suite

* Mon Jan 28 2013 Paul Howarth <paul@city-fan.org> - 0.17-1
- Update to 0.17:
  - Use IPC::Run3 instead of IPC::Open3

* Fri Dec 21 2012 Paul Howarth <paul@city-fan.org> - 0.16-1
- Update to 0.16:
  - Allow use of a custom POD parser rather than Pod::Spell using
    set_pod_parser
- Re-diff patch to avoid shipping .orig file

* Wed Nov 21 2012 Jitka Plesnikova <jplesnik@redhat.com> - 0.15-5
- Update dependencies
- Don't need to remove empty directories from the buildroot
- Drop %%defattr, redundant since rpm 4.4

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.15-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 11 2012 Petr Pisar <ppisar@redhat.com> - 0.15-3
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Aug 23 2011 Paul Howarth <paul@city-fan.org> - 0.15-1
- Update to 0.15:
  - Begin adding actual tests (hilariously, adding the suggested t/pod-spell.t
    to this dist to test itself found a typo: "stopwards")
- BR: perl(Test::Tester) and hunspell-en

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.14-2
- Perl mass rebuild

* Fri May 27 2011 Paul Howarth <paul@city-fan.org> - 0.14-1
- Update to 0.14:
  - Fix an error when using add_stopwords("constant","strings") (CPAN RT#68471)

* Wed Apr 27 2011 Paul Howarth <paul@city-fan.org> - 0.13-1
- Update to 0.13:
  - Make alternatives checking more robust by reading the spellchecker's STDERR

* Tue Apr 26 2011 Paul Howarth <paul@city-fan.org> - 0.12-1
- Update to 0.12:
  - Best Practical has taken over maintainership of this module
  - Try various spellcheck programs instead of hardcoding the ancient `spell`
    (CPAN RT#56483)
  - Remove temporary files more aggressively (CPAN RT#41586)
  - Fixed by not creating them at all - instead we now use IPC::Open3
  - Remove suggestion to use broken `aspell -l` (CPAN RT#28967)
  - Add set_pod_file_filter for skipping translations, etc. (CPAN RT#63755)
  - Skip tests in all_pod_files_spelling_ok if there is no working spellchecker
  - Provide a has_working_spellchecker so you can skip your own tests if
    there's no working spellchecker
  - Switch to Module::Install
  - Rewrite and modernize a lot of the documentation
  - Decruftify code, such as by using Exporter and lexical filehandles
  - Support .plx files
- This release by SARTAK -> update source URL
- Rewrite hunspell patch to just favour hunspell over aspell
- BR: perl(IPC::Open3)

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 22 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.11-10
- Rebuild to fix problems with vendorarch/lib (#661697)

* Fri May 07 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.11-9
- Mass rebuild with perl-5.12.0

* Fri Jan 29 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 0.11-8
- actually apply patch. :P

* Wed Jan 20 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 0.11-7
- use hunspell instead of aspell (bz 508643)

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 0.11-6
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.11-3
- Rebuild for perl 5.10 (again)

* Sun Jan 13 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.11-2
- rebuild for new perl

* Tue Dec 19 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.11-1
- First build.
