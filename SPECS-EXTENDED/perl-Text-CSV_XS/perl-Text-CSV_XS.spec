Vendor:         Microsoft Corporation
Distribution:   Mariner
Name:           perl-Text-CSV_XS
Version:        1.41
Release:        2%{?dist}
Summary:        Comma-separated values manipulation routines
License:        GPL+ or Artistic
URL:            https://metacpan.org/release/Text-CSV_XS
Source0:        https://cpan.metacpan.org/modules/by-module/Text/Text-CSV_XS-%{version}.tgz
# Build:
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  perl-devel
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(Config::Tiny)
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
# Run-time:
BuildRequires:  perl(Carp)
# Specific version ≥ 2.92 for Encode is recommended but not required
BuildRequires:  perl(Encode)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(IO::Handle)
BuildRequires:  perl(strict)
BuildRequires:  perl(UNIVERSAL::isa)
BuildRequires:  perl(vars)
BuildRequires:  perl(warnings)
BuildRequires:  perl(XSLoader)
# Tests:
BuildRequires:  perl(base)
BuildRequires:  perl(charnames)
BuildRequires:  perl(Config)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Tie::Scalar)
# Dependencies
Requires:       perl(:MODULE_COMPAT_%(eval "$(perl -V:version)"; echo $version))
# Specific version ≥ 2.92 for Encode is recommended but not required
Requires:       perl(Encode)
# IO::Handle is loaded by XS code
Requires:       perl(IO::Handle)
Requires:       perl(UNIVERSAL::isa)

%{?perl_default_filter}

%description
Text::CSV provides facilities for the composition and decomposition of
comma-separated values.  An instance of the Text::CSV class can combine
fields into a CSV string and parse a CSV string into fields.

%prep
%setup -q -n Text-CSV_XS-%{version}

chmod -c a-x examples/*

# Upstream does this on purpose (2011-03-23):
# "As Text::CSV_XS is so low-level, most of these files are actually *examples*
# and not ready-to-run out-of-the-box scripts that work as expected, though
# I must admit that some have evolved into being like that."
#find . -type f -exec sed -i '1s/pro/usr/' {} \;

%build
perl Makefile.PL \
  INSTALLDIRS=vendor \
  OPTIMIZE="%{optflags}" \
  NO_PACKLIST=true \
  NO_PERLLOCAL=true
%{make_build}

%install
%{make_install}
find %{buildroot} -type f -name '*.bs' -empty -delete
%{_fixperms} -c %{buildroot}

%check
%{make_build} test

%files
%doc ChangeLog CONTRIBUTING.md README examples/
%{perl_vendorarch}/Text/
%{perl_vendorarch}/auto/Text/
%{_mandir}/man3/Text::CSV_XS.3*

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.41-2
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Sun Feb 16 2020 Paul Howarth <paul@city-fan.org> - 1.41-1
- Update to 1.41
  - Update to Devel::PPPort-3.56
  - csv2xls uses sheetname as csv2xlsx
  - csv2xlsx: support images (each image gets its own tab)
  - More docs (data validation)
  - It's 2020
  - No binary literals in fixed error messages
  - Fix auto_diag > 2 to die when headers are used (GH#19)

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.40-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sun Sep 15 2019 Paul Howarth <paul@city-fan.org> - 1.40-1
- Update to 1.40
  - Update to Devel::PPPort-3.52
  - Development perl is now 5.28.2
  - [csv2xlsx] sheetnames are restricted to 31 characters
  - Generate cpanfile
  - Add munge type "db"
  - [csv2xls/csv2xlsx] do not generate xls/xlsx on empty CSV (GH#18)
  - New: support $csv->formula (sub { ... })
  - Support stacked encodings
- Use %%{make_build} and %%{make_install}

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.39-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.39-2
- Perl 5.30 rebuild

* Sat Mar 16 2019 Paul Howarth <paul@city-fan.org> - 1.39-1
- Update to 1.39
  - It's 2019
  - Fix tests to skip on Encode failing (GH#17)
  - Tested on Z/OS (s390x - Hercules)
  - Test with new Module::CPANTS::Analyse
  - Add options -w/-b/-Z to csvdiff
  - Fix strict on streaming EOF
  - Now also tested with cperl

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.38-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Jan  2 2019 Paul Howarth <paul@city-fan.org> - 1.38-1
- Update to 1.38
  - Name the duplicate headers on error 1013
  - Add missing attributes to default list (documentation only)
  - Add support for combined keys
  - Look at $NO_COLOR for csvdiff
  - Add support for key-value pair

* Thu Sep 27 2018 Paul Howarth <paul@city-fan.org> - 1.37-1
- Update to 1.37
  - Moved pod-tests from t to xt
  - Add munge as alias for munge_column_names
  - Update to Devel::PPPort-3.43
  - Simplified ref-check defines in XS (GH#12)
  - Tested against perl-5.29.3

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.36-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.36-2
- Perl 5.28 rebuild

* Tue Jun 26 2018 Paul Howarth <paul@city-fan.org> - 1.36-1
- Update to 1.36
  - Now also tested on FreeBSD-11.1
  - Update to Devel::PPPort-3.42
  - Fixed memory leak
  - Add undef_str attribute
  - Tested against perl-5.28.0
  - Move from DynaLoader to XSLoader
  - Tested on Synology DSM
- Switch upstream from search.cpan.org to metacpan.org

* Wed Mar 21 2018 Paul Howarth <paul@city-fan.org> - 1.35-1
- Update to 1.35
  - Remove META.yml from MANIFEST.skip
  - Use UNIVERSAL::isa to protect against unblessed references
  - Fix -Wformat warning (CPAN RT#123729)
  - Make detect_bom result available
  - It's 2018
  - Add csv (out => \"skip") - suppress output deliberately
  - Allow sub as top-level filter
  - Tested against Test2::Harness-0.001062 (yath test)
  - Tested against perl-5.27.10

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.34-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Nov  6 2017 Paul Howarth <paul@city-fan.org> - 1.34-1
- Update to 1.34
  - Bad arg for formula (like "craok") will now die with error 1500
  - Row report in formula reporting was off by 1
  - Add a prominent section about BOM handling
  - Make sheet label more portable (csv2xlsx)
  - Allow munge => \%%hash
  - Preserve first row in csv (set_column_names => 0)

* Fri Oct 20 2017 Paul Howarth <paul@city-fan.org> - 1.33-1
- Update to 1.33
  - Small additional fix for eol = \r + BOM
  - Updated documentation for example files
  - Add support for formula actions (GH#11)
    - csv2xls and csv2xlsx now warn by default
  - Reset file info on ->header call (CPAN RT#123320)

* Sun Sep 17 2017 Paul Howarth <paul@city-fan.org> - 1.32-1
- Update to 1.32
  - Add keep_headers attribute to csv()
  - Fix on_in when used in combination with key
  - Fail on invalid arguments to csv
  - Fix header method on EOL = CR (CPAN RT#122764)

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.31-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.31-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Jun 15 2017 Paul Howarth <paul@city-fan.org> - 1.31-1
- Update to 1.31
  - Fix already decoded BOM in headers
  - New options in csv-check
  - Some perlcritic
  - "escape" is alias for "escape_char" for consistency
  - Code cleanup and more tests (Devel::Cover)
  - Improve csv-check auto-sep-detection

* Sat Jun 10 2017 Paul Howarth <paul@city-fan.org> - 1.30-1
- Update to 1.30
  - Add csv (..., out => ...) syntax examples (GH#7)
  - Disable escape_null for undefined escape_char
  - Fix ->say for bound columns (CPAN RT#121576)
  - Update to Devel::PPPort 3.36
  - Tested under 5.26.0 and 5.27.0
  - Documentation changes and additions

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.29-2
- Perl 5.26 rebuild

* Wed Apr 26 2017 Paul Howarth <paul@city-fan.org> - 1.29-1
- Update to 1.29
  - More docs for bind_columns (CPAN RT#121350)
  - New attribute "strict" (also addresses CPAN RT#121350)
- Drop redundant Group: tag

* Wed Mar 22 2017 Paul Howarth <paul@city-fan.org> - 1.28-1
- Update to 1.28
  - Fix length problem with bound empty fields and UTF-8 (CPAN RT#120655)

* Fri Mar  3 2017 Paul Howarth <paul@city-fan.org> - 1.27-1
- Update to 1.27
  - Remove unneeded done_testing
  - Attribute sep/sep_char is not allowed to be undefined
  - Increased test coverage: added errors 1008 and 1014
  - Default for escape_null in csv() is now false
  - It's 2017
  - New error code for illegal argument(s)/parameter(s) (CPAN RT#119827)
  - Fix tests for perl without dot in @INC
  - Fix crlf issue for csv() on Windows (CPAN RT#120466)

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.26-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Nov 30 2016 Paul Howarth <paul@city-fan.org> - 1.26-1
- Update to 1.26
  - Disable some Unicode-related tests for unhealthy $PERL_UNICODE
    (CPAN RT#117856)
  - is_missing(0) on empty line returns 1 for keep_meta_info=true (GH#27)

* Mon Aug 29 2016 Paul Howarth <paul@city-fan.org> - 1.25-1
- Update to 1.25
  - Allow lc, uc, and coderef for csv() headers attribute
  - Document for eof when the last line has an error (CPAN RT#115954)
  - Allow csv() to call header() with all supported arguments
  - Add some docs for bind_columns

* Sat Jul  9 2016 Paul Howarth <paul@city-fan.org> - 1.24-1
- Update to 1.24
  - Fix typo in docs example code (GH#4)
  - Set auto-wrap on for csv2xls with embedded newlines
  - Add examples/csv2xlsx, the MSExcel-2007+ version of csv2xls; includes new
    feature to merge multiple CSV's into a single xlsx
  - Slight modification in examples
  - Fix parse error in complex option combo (CPAN RT#115953)
- BR: perl-generators

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.23-2
- Perl 5.24 rebuild

* Sat Mar 26 2016 Paul Howarth <paul@city-fan.org> - 1.23-1
- Update to 1.23
  - Skip unsupported encodings
  - Reorganize Unicode section and mention layers
  - Amend some UTF-8 tests for PERL_UNICODE settings
  - Fix crash on error in parsing with bound columns (CPAN RT#113279)
  - Add predefined filters (not_blank, not_empty, filled)

* Wed Feb 24 2016 Paul Howarth <paul@city-fan.org> - 1.22-1
- Update to 1.22
  - Small doc updates regarding blank_is_undef
  - Precedence error in doc
  - Add new method header

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.21-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jan  6 2016 Paul Howarth <paul@city-fan.org> - 1.21-1
- Update to 1.21
  - Clarify documentation (CPAN RT#110941)
  - Alias %%_ to row in hashref mode for csv function attributes on_in and
    before_out
  - Examples now use defined-or and thus require perl-5.10 or up
  - Fix \r\n ending with allow_loose_escapes

* Fri Oct  9 2015 Paul Howarth <paul@city-fan.org> - 1.20-1
- Update to 1.20
  - Use "say" in synopsis
  - Remove needless special characters in doc section
  - Change doc =item attributes for new to =head for index
  - Add known_attributes function/method
  - Add contributor notes
  - Allow undef as value for aliased attributes
- Explicitly BR: perl-devel, needed for EXTERN.h

* Wed Jun 17 2015 Paul Howarth <paul@city-fan.org> - 1.19-1
- Update to 1.19
  - Guard tests against $PERL_UNICODE
  - Numeric options were sometimes interpreted as boolean
  - Safer meta_info use

* Fri Jun 05 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.18-2
- Perl 5.22 rebuild

* Sun May 24 2015 Paul Howarth <paul@city-fan.org> - 1.18-1
- Update to 1.18
  - Add quote_empty attribute
  - Add database NULL documentation
  - Inherit csv attributes in csv() when called in void context
  - Micro-optimisation for combine/print (empty fields will be faster)

* Sun Apr 26 2015 Paul Howarth <paul@city-fan.org> - 1.17-1
- Update to 1.17
  - Enable overruling $csv in csv()
  - Allow encoding to be shortened to enc in csv()
  - Allow filter to alter content
  - Add say (print with default eol => $\)
  - Allow MS sep=; on first line (CPAN RT#100304)

* Mon Mar  2 2015 Paul Howarth <paul@city-fan.org> - 1.16-1
- Update to 1.16:
  - filter made more useful (access to other fields)

* Wed Feb 11 2015 Paul Howarth <paul@city-fan.org> - 1.15-1
- Update to 1.15:
  - Remove perl recommendation from META as it breaks cpan clients

* Mon Feb  2 2015 Paul Howarth <paul@city-fan.org> - 1.14-1
- Update to 1.14:
  - Move to github
  - Add csv (filter => {});
  - Change csv ()'s void context behavior

* Mon Jan  5 2015 Paul Howarth <paul@city-fan.org> - 1.13-1
- Update to 1.13:
  - Simplify code path for old perl
  - Fix quote_binary (CPAN RT#100676)
  - Fix csv() for hashrefs with aliased headers
  - Update copyright to 2015
- Drop upstreamed UTF8 patch

* Sun Nov 16 2014 Paul Howarth <paul@city-fan.org> - 1.12-1
- Update to 1.12:
  - Add field number to error_diag
  - Fixed non-IO parsing multi-byte EOL
  - Fixed a possible missed multi-byte EOL
  - Allow hashref for csv()'s headers attribute
  - Allow encoding on all output handles in csv()
  - Include doc changes as ticketed in the Text::CSV queue
  - Fix parallel testing issue
  - Allow csv as method call (not using the object)
  - Rename quote_null to escape_null
  - Give meaning to keep_meta_info on output
- Add patch to recode documentation as UTF8

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.11-2
- Perl 5.20 rebuild

* Wed Aug 20 2014 Petr Šabata <contyk@redhat.com> - 1.11-1
- 1.11 bump

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Aug 09 2014 Petr Šabata <contyk@redhat.com> - 1.10-1
- 1.10 bump

* Thu Jun 12 2014 Petr Šabata <contyk@redhat.com> - 1.09-1
- 1.09 bugfix bump

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.08-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon May 26 2014 Petr Šabata <contyk@redhat.com> - 1.08-1
- 1.08 bump

* Wed Apr 30 2014 Petr Šabata <contyk@redhat.com> - 1.07-1
- 1.07 bump

* Mon Apr 28 2014 Petr Šabata <contyk@redhat.com> - 1.06-1
- 1.06 bump

* Tue Mar 18 2014 Petr Šabata <contyk@redhat.com> - 1.05-1
- 1.05 bump

* Tue Feb 25 2014 Petr Šabata <contyk@redhat.com> - 1.04-1
- 1.04 bump

* Tue Jan 28 2014 Petr Šabata <contyk@redhat.com> - 1.03-1
- 1.03 bump

* Wed Nov 20 2013 Petr Šabata <contyk@redhat.com> - 1.02-1
- 1.02 bump

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.01-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Jul 20 2013 Petr Pisar <ppisar@redhat.com> - 1.01-3
- Perl 5.18 rebuild

* Fri Jul 19 2013 Petr Pisar <ppisar@redhat.com> - 1.01-2
- Perl 5.18 rebuild

* Thu Jun 20 2013 Petr Šabata <contyk@redhat.com> - 1.01-1
- 1.01 bump

* Fri Jun 14 2013 Petr Šabata <contyk@redhat.com> - 1.00-1
- 1.00 bugfix bump

* Tue Jun 11 2013 Petr Šabata <contyk@redhat.com> - 0.99-1
- 0.99 bump

* Mon Jun 10 2013 Petr Šabata <contyk@redhat.com> - 0.98-1
- 0.98 bump

* Tue Apr 02 2013 Petr Šabata <contyk@redhat.com> - 0.97-1
- 0.97 bump, performance enhancement

* Wed Mar 27 2013 Petr Šabata <contyk@redhat.com> - 0.96-1
- 0.96 bump

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.95-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Jan 14 2013 Petr Pisar <ppisar@redhat.com> - 0.95-1
- 0.95 bump

* Tue Dec 04 2012 Petr Pisar <ppisar@redhat.com> - 0.94-1
- 0.94 bump

* Wed Nov 21 2012 Petr Pisar <ppisar@redhat.com> - 0.93-1
- 0.93 bump

* Wed Nov 14 2012 Petr Pisar <ppisar@redhat.com> - 0.92-1
- 0.92 bump

* Mon Nov 05 2012 Petr Pisar <ppisar@redhat.com> - 0.91-2
- Correct dependencies

* Wed Aug 22 2012 Petr Šabata <contyk@redhat.com> - 0.91-1
- 0.91 bump (mostly test-cases updates)

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.90-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 28 2012 Petr Pisar <ppisar@redhat.com> - 0.90-2
- Perl 5.16 rebuild

* Tue Jun 19 2012 Petr Šabata <contyk@redhat.com> - 0.90-1
- 0.90 bump

* Tue Jun 12 2012 Petr Pisar <ppisar@redhat.com> - 0.88-2
- Perl 5.16 rebuild

* Mon Mar 19 2012 Petr Pisar <ppisar@redhat.com> - 0.88-1
- 0.88 bump
- Fix parsing fields that contain excessive $/

* Wed Mar 14 2012 Petr Šabata <contyk@redhat.com> - 0.87-1
- 0.87 bump
- Remove command macros and defattr

* Tue Jan 24 2012 Marcela Mašláňová <mmaslano@redhat.com> - 0.86-1
- update to 0.86

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.85-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Sep 08 2011 Petr Sabata <contyk@redhat.com> - 0.85-1
- 0.85 bump

* Mon Aug 08 2011 Petr Sabata <contyk@redhat.com> - 0.83a-1
- 0.83a bump

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.82-2
- Perl mass rebuild

* Mon May  9 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.82-1
- update to 0.82

* Wed Mar 23 2011 Petr Sabata <psabata@redhat.com> - 0.81-2
- Revert example scripts interpreter changes

* Wed Mar 23 2011 Petr Sabata <psabata@redhat.com> - 0.81-1
- 0.81 version bump
- Changed script interpreters in various example files
- Convert ChangeLog to proper UTF8
- Removed buildroot garbage

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.80-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jan  3 2011 Petr Sabata <psabata@redhat.com> - 0.80-1
- 0.80 version bump

* Thu Dec  2 2010 Petr Sabata <psabata@redhat.com> - 0.79-1
- 0.79 version bump

* Mon Oct 18 2010 Petr Sabata <psabata@redhat.com> - 0.76-1
- 0.76 version bump

* Mon Oct 11 2010 Petr Sabata <psabata@redhat.com> - 0.75-1
- 0.75 version bump

* Mon Oct 04 2010 Petr Pisar <ppisar@redhat.com> - 0.74-1
- 0.74 bump

* Wed Sep 08 2010 Petr Pisar <ppisar@redhat.com> - 0.73-1
- 0.73 bump

* Fri May 07 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.72-2
- Mass rebuild with perl-5.12.0

* Wed Mar 17 2010 Chris Weyl <cweyl@alumni.drew.edu> 0.72-1
- PERL_INSTALL_ROOT => DESTDIR, add perl_default_filter (XS module)
- auto-update to 0.72 (by cpan-spec-update 0.01) (DBIx::Class needed a newer
  Text::CSV, which in turn can only leverage Text::CSV_XS >= 0.70)
- added a new br on perl(ExtUtils::MakeMaker) (version 0)
- added a new br on perl(IO::Handle) (version 0)
- added a new br on perl(Test::Harness) (version 0)
- added a new br on perl(Test::More) (version 0)
- added a new br on perl(Tie::Scalar) (version 0)

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 0.69-2
- rebuild against perl 5.10.1

* Mon Nov  2 2009 Stepan Kasal <skasal@redhat.com> - 0.69
- new upstream release

* Wed Oct  7 2009 Marcela Mašláňová <mmaslano@redhat.com> - 0.68-1
- update to new upstream release

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.58-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.58-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Dec 10 2008 Lubomir Rintel <lkundrak@v3.sk> - 0.58-1
- Update to latest upstream
- SvUPGRADE patch upstreamed

* Tue Jul 08 2008 Lubomir Rintel <lkundrak@v3.sk> - 0.52-2
- Actually solving the issue mentioned in previous change

* Tue Jul 08 2008 Lubomir Rintel <lkundrak@v3.sk> - 0.52-1
- Updated to 0.52 to solve an issue with perl 5.10

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.30-5
- Rebuild for perl 5.10 (again)

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.30-4
- Autorebuild for GCC 4.3

* Sat Feb  2 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.30-3
- rebuild for new perl

* Wed Aug 29 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> - 0.30-2
- Rebuild for selinux ppc32 issue.

* Sat Jun 23 2007 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.30-1
- Update to 0.30.

* Sat Jun 16 2007 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.29-1
- Update to 0.29.

* Sat Jun 16 2007 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.27-1
- Update to 0.27.
- New upstream maintainer.

* Thu Sep  7 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.23-5
- Rebuild for FC6.

* Wed Feb 22 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.23-4
- Rebuild for FC5 (perl 5.8.8).

* Wed Feb 22 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.23-3
- The wonders of CVS problems (released skipped).

* Thu Jan  5 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.23-2
- Build section: simplified RPM_OPT_FLAGS handling (#175898).

* Sat Nov 05 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.23-1
- First build.
