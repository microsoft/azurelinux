Name:           perl-DateTime-Format-Strptime
Epoch:          1
Version:        1.79
Release:        11%{?dist}
Summary:        Parse and format strptime and strftime patterns
License:        Artistic-2.0
URL:            https://metacpan.org/release/DateTime-Format-Strptime
Source0:        https://cpan.metacpan.org/modules/by-module/DateTime/DateTime-Format-Strptime-%{version}.tar.gz
BuildArch:      noarch
# Module Build
BuildRequires:  coreutils
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
# Module Runtime
BuildRequires:  perl(Carp)
BuildRequires:  perl(constant)
BuildRequires:  perl(DateTime) >= 1.00
BuildRequires:  perl(DateTime::Locale) >= 1.30
BuildRequires:  perl(DateTime::Locale::Base)
BuildRequires:  perl(DateTime::TimeZone) >= 2.09
BuildRequires:  perl(Exporter)
BuildRequires:  perl(Params::ValidationCompiler)
BuildRequires:  perl(parent)
BuildRequires:  perl(Specio) >= 0.33
BuildRequires:  perl(Specio::Declare)
BuildRequires:  perl(Specio::Exporter)
BuildRequires:  perl(Specio::Library::Builtins)
BuildRequires:  perl(Specio::Library::String)
BuildRequires:  perl(strict)
BuildRequires:  perl(Try::Tiny)
BuildRequires:  perl(warnings)
# Test Suite
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(FindBin)
BuildRequires:  perl(lib)
BuildRequires:  perl(Test::Builder)
BuildRequires:  perl(Test::Fatal)
BuildRequires:  perl(Test::More) >= 0.96
BuildRequires:  perl(Test::Warnings)
BuildRequires:  perl(utf8)
# Optional Tests
BuildRequires:  perl(CPAN::Meta) >= 2.120900
BuildRequires:  perl(CPAN::Meta::Prereqs)
# Dependencies
# (none)

%description
This module implements most of strptime(3), the POSIX function that is the
reverse of strftime(3), for DateTime. While strftime takes a DateTime and a
pattern and returns a string, strptime takes a string and a pattern and
returns the DateTime object associated.

%prep
%setup -q -n DateTime-Format-Strptime-%{version}

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
%doc Changes CODE_OF_CONDUCT.md CONTRIBUTING.md README.md
%{perl_vendorlib}/DateTime/
%{_mandir}/man3/DateTime::Format::Strptime.3*
%{_mandir}/man3/DateTime::Format::Strptime::Types.3*

%changelog
* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.79-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.79-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.79-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.79-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.79-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.79-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jun 01 2022 Jitka Plesnikova <jplesnik@redhat.com> - 1:1.79-5
- Perl 5.36 rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.79-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.79-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sat May 22 2021 Jitka Plesnikova <jplesnik@redhat.com> - 1:1.79-2
- Perl 5.34 rebuild

* Mon May  3 2021 Paul Howarth <paul@city-fan.org> - 1:1.79-1
- Update to 1.79
  - Fix too-strict type checking for time zones: this module now uses the same
    check as DateTime itself, which allows for things that don't subclass
    DateTime::TimeZone as long as they provide the same API (GH#30)

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.78-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Dec 16 2020 Paul Howarth <paul@city-fan.org> - 1:1.78-1
- Update to 1.78
  - Fix tests for new failure caused by locale data changes in DateTime::Locale
    1.29 (GH#28)
  - Added a warning about using locale-specific patterns; some of these patterns
    can change quite a bit as the locale data is updated, so using them for
    parsing does not produce stable results across time - this is what caused
    the test failures that this release fixes

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.77-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 1:1.77-2
- Perl 5.32 rebuild

* Mon Mar  2 2020 Paul Howarth <paul@city-fan.org> - 1:1.77-1
- Update to 1.77
  - When the parsed string contained an invalid time zone offset (parsed with
    "%%z") like "-9999", the error handling set in the parser's constructor was
    ignored and an exception was always thrown (GH#25)
- Use %%{make_build} and %%{make_install}

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.76-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.76-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1:1.76-2
- Perl 5.30 rebuild

* Fri Feb  8 2019 Paul Howarth <paul@city-fan.org> - 1:1.76-1
- Update to 1.76
  - The ability to set the pattern, time_zone, and locale via accessor methods
    has been removed; this was deprecated over three years ago in version 1.60
    (it also turns out that the setting was actually broken for a long time but
    no one seemed to notice)
- Package new upstream document CODE_OF_CONDUCT.md

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.75-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.75-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jun 29 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1:1.75-3
- Perl 5.28 rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.75-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Dec 26 2017 Paul Howarth <paul@city-fan.org> - 1:1.75-1
- Update to 1.75
  - Fixed tests to pass with blead Perl (GH#19)

* Fri Aug  4 2017 Paul Howarth <paul@city-fan.org> - 1:1.74-1
- Update to 1.74
  - Fix text not to rely on a very specific exception message from Specio; this
    was broken in 0.39 (GH#18)

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.73-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jun 06 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1:1.73-3
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.73-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb  1 2017 Paul Howarth <paul@city-fan.org> - 1:1.73-1
- Update to 1.73
  - The format_datetime method now checks that the object it is given isa
    DateTime object (GH#17)

* Wed Jan 25 2017 Paul Howarth <paul@city-fan.org> - 1:1.72-1
- Update to 1.72
  - By default, the word boundary checks added in 1.69 are now off; you can
    enable them by passing "strict => 1" to the constructor (GH#15)
  - Switched from Params::Validate to Params::ValidationCompiler
  - Require DateTime::Locale 1.05; this fixes some test failures seen on CPAN
    Testers
  - Require DateTime::TimeZone 2.09 because you should really update this on a
    regular basis
  - Require Specio 0.33 to fix other test failures seen on CPAN (I hope)

* Sun Dec 11 2016 Paul Howarth <paul@city-fan.org> - 1:1.70-1
- Update to 1.70
  - The word boundary check supposedly added in 1.67 didn't really work
    properly, and still matched too much (GH#11)
  - Added docs for several formats that have long been supported but not
    documented; these are %%P, %%c, %%x, and %%X (GH#10)
  - Altered the conversion specifier %%z to accept ±HH, ±HHMM, ±HH:MM and Z;
    previously only ±HHMM were accepted (GH#13)

* Mon May 16 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1:1.68-2
- Perl 5.24 rebuild

* Mon May  9 2016 Paul Howarth <paul@city-fan.org> - 1:1.68-1
- Update to 1.68
  - Author tests are no longer in t/, which makes running tests for non-authors
    much faster (CPAN RT#114237)

* Fri Apr  1 2016 Paul Howarth <paul@city-fan.org> - 1:1.67-1
- Update to 1.67
  - Fixed a regression introduced in 1.60; older versions of this library would
    match dates pretty much anywhere in a string, so "%%Y-%%m-%%d" would match
    a string like "abcd1234-12-30efgh" - this is probably too permissive, but
    we definitely want to match on word boundaries so that we match
    "log.2016-03-31" (GH#3)

* Tue Mar 29 2016 Paul Howarth <paul@city-fan.org> - 1:1.66-1
- Update to 1.66
  - Added a zone_map constructor argument; this lets you supply a mapping for
    ambiguous time zone abbreviations (CPAN RT#74762)

* Sun Mar 20 2016 Paul Howarth <paul@city-fan.org> - 1:1.65-1
- 1.65 bump
- License is now Artistic 2.0

* Mon Feb 22 2016 Petr Šabata <contyk@redhat.com> - 1:1.64-1
- 1.64 bump

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.63-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jan 14 2016 Petr Šabata <contyk@redhat.com> - 1:1.63-1
- 1.63 bump
- Modernize the SPEC file

* Mon Dec 21 2015 Petr Šabata <contyk@redhat.com> - 1:1.62-1
- 1.62 bump

* Sat Nov 14 2015 Paul Howarth <paul@city-fan.org> - 1:1.61-1
- 1.61 bump

* Sun Nov  8 2015 Paul Howarth <paul@city-fan.org> - 1:1.60-1
- 1.60 bump

* Thu Oct 08 2015 Petr Pisar <ppisar@redhat.com> - 1:1.57-1
- 1.57 bump

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5600-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.5600-3
- Perl 5.22 rebuild

* Fri Aug 29 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.5600-2
- Perl 5.20 rebuild

* Tue Aug 12 2014 Petr Pisar <ppisar@redhat.com> - 1.5600-1
- 1.56 bump

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5500-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun May  4 2014 Paul Howarth <paul@city-fan.org> - 1.5500-1
- Update to 1.55 (rpm version 1.5500 to maintain upgrade path)
  - If diagnostic is true for an object, it will now use Test::More::diag()
    under the test harness rather than printing to STDOUT
  - The %%z specifier will now parse UTC offsets with a colon like "+01:00"
    (CPAN RT#91458)
  - Made the regexes to parse day and months abbreviations and names a little
    more specificl as it stood, they tended to eat up more non-word characters
    than they should, so a pattern like '%%a%%m%%d_%%Y' broke on a date like
    'Fri0215_2013' - the day name would be parsed as 'Fri02' and the month
    would not be parsed at all (CPAN RT#93863, CPAN RT#93865)
- Specify all dependencies
- Use DESTDIR rather than PERL_INSTALL_ROOT

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5400-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 31 2013 Petr Pisar <ppisar@redhat.com> - 1.5400-2
- Perl 5.18 rebuild

* Wed Apr  3 2013 Paul Howarth <paul@city-fan.org> - 1.5400-1
- Update to 1.54 (rpm version 1.5400 to maintain upgrade path)
  - Packaging cleanup, including listing Test::More as a test prereq, not a
    runtime prereq (CPAN RT#76128)
  - Shut up "unescaped braces in regex" warning from 5.17.0 (CPAN RT#77514)
  - A fix in DateTime.pm 1.00 broke a test in this distro (CPAN RT#84371)
  - Require DateTime.pm 1.00 because without it tests will break
- Specify all dependencies
- This release by DROLSKY -> update source URL
- Drop %%defattr, redundant since rpm 4.4
- Don't need to remove empty directories from the buildroot
- Don't use macros for commands
- Make %%files list more explicit

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5000-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5000-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 20 2012 Petr Pisar <ppisar@redhat.com> - 1.5000-6
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5000-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Jul 21 2011 Petr Sabata <contyk@redhat.com> - 1.5000-4
- Perl mass rebuild

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 1.5000-3
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5000-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 22 2010 Steven Pritchard <steve@kspei.com> 1.5000-1
- Update to 1.5000.

* Thu Dec 16 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.2000-3
- Rebuild to fix problems with vendorarch/lib (#661697)

* Tue Jun 15 2010 Petr Sabata <psabata@redhat.com> - 1.2000-1
- Update to the latest upstream release

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.1000-2
- Mass rebuild with perl-5.12.0

* Tue Feb 16 2010 Paul Howarth <paul@city-fan.org> 1.1000-1
- Fix FTBFS (#564718) by bumping buildreq version of perl(DateTime) from 0.4304
  to 0.44 (RPM considers 0.4304 > 0.44, unlike perl) and bumping version to
  1.1000 for compatibility with DateTime::Locale 0.43 (upstream ticket 19)
- Update buildreq version requirement for perl(DateTime::Locale) to 0.43
- Drop test patch, no longer needed
- Run additional tests for full locale coverage

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> 1.0800-4
- Rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> 1.0800-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> 1.0800-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Aug 29 2008 Steven Pritchard <steve@kspei.com> 1.0800-1
- Update to 1.0800.
- Update versions on build dependencies.

* Tue Jul 08 2008 Steven Pritchard <steve@kspei.com> 1.0702-3
- Patch t/004_locale_defaults.t to work around change in DateTime::Locale.

* Tue Mar 04 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.0702-2
- Rebuild for new perl

* Thu Jan 03 2008 Steven Pritchard <steve@kspei.com> 1.0702-1
- Update to 1.0702.
- Drop charset patch.
- Update License tag.
- BR Test::More.

* Tue Apr 17 2007 Steven Pritchard <steve@kspei.com> 1.0700-3
- Use fixperms macro instead of our own chmod incantation.
- BR ExtUtils::MakeMaker.

* Sat Sep 16 2006 Steven Pritchard <steve@kspei.com> 1.0700-2
- Fix find option order.

* Mon Jul 03 2006 Steven Pritchard <steve@kspei.com> 1.0700-1
- Specfile autogenerated by cpanspec 1.66.
- Fix License.
- Remove versioned DateTime deps (0.1402 > 0.30 according to rpm).
- Remove versioned explicit dependencies that rpmbuild picks up.
- Substitute literal "©" for E<169> in pod documentation.  (The result
  should be the same, but apparently the man page conversion is generating
  something that rpmlint doesn't like.)
