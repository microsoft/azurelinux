# Run optional test
%if ! (0%{?rhel})
%bcond_without perl_DateTime_enables_optional_test
%else
%bcond_with perl_DateTime_enables_optional_test
%endif

Name:           perl-DateTime
Epoch:          2
Version:        1.65
Release:        6%{?dist}
Summary:        Date and time object for Perl
License:        Artistic-2.0
URL:            https://metacpan.org/release/DateTime
Source0:        https://cpan.metacpan.org/modules/by-module/DateTime/DateTime-%{version}.tar.gz
# Build:
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  perl-devel
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
# Run-time:
BuildRequires:  perl(Carp)
BuildRequires:  perl(DateTime::Locale) >= 1.06
BuildRequires:  perl(DateTime::TimeZone) >= 2.44
BuildRequires:  perl(Dist::CheckConflicts) >= 0.02
BuildRequires:  perl(integer)
BuildRequires:  perl(namespace::autoclean) >= 0.19
BuildRequires:  perl(overload)
BuildRequires:  perl(Params::ValidationCompiler) >= 0.26
BuildRequires:  perl(parent)
BuildRequires:  perl(POSIX)
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(Specio) >= 0.18
BuildRequires:  perl(Specio::Declare)
BuildRequires:  perl(Specio::Exporter)
BuildRequires:  perl(Specio::Library::Builtins)
BuildRequires:  perl(Specio::Library::Numeric)
BuildRequires:  perl(Specio::Library::String)
BuildRequires:  perl(Specio::Subs)
BuildRequires:  perl(strict)
BuildRequires:  perl(Try::Tiny)
BuildRequires:  perl(warnings)
BuildRequires:  perl(warnings::register)
# Optional Run-time:
BuildRequires:  perl(XSLoader)
# Tests:
BuildRequires:  perl(CPAN::Meta::Check) >= 0.011
BuildRequires:  perl(CPAN::Meta::Requirements)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(Test::Fatal)
BuildRequires:  perl(Test::More) >= 0.96
BuildRequires:  perl(Test::Warnings) >= 0.005
BuildRequires:  perl(Test::Without::Module)
BuildRequires:  perl(utf8)
%if %{with perl_DateTime_enables_optional_test} && !%{defined perl_bootstrap}
# Optional Tests:
BuildRequires:  perl(CPAN::Meta) >= 2.120900
BuildRequires:  perl(DateTime::Format::Strptime)
BuildRequires:  perl(Storable)
BuildRequires:  perl(Test::Warn)
%endif
# Dependencies:
Requires:       perl(XSLoader)

# Avoid provides from DateTime.so
%{?perl_default_filter}

# Filter under-specified dependencies
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\((DateTime::Locale|DateTime::TimeZone)\\)$

%description
DateTime is a class for the representation of date/time combinations.  It
represents the Gregorian calendar, extended backwards in time before its
creation (in 1582). This is sometimes known as the "proleptic Gregorian
calendar". In this calendar, the first day of the calendar (the epoch), is the
first day of year 1, which corresponds to the date which was (incorrectly)
believed to be the birth of Jesus Christ.

%prep
%setup -q -n DateTime-%{version}

%build
perl Makefile.PL \
  INSTALLDIRS=vendor \
  OPTIMIZE="%{optflags}" \
  NO_PACKLIST=1 \
  NO_PERLLOCAL=1
%{make_build}

%install
%{make_install}
find %{buildroot} -type f -name '*.bs' -empty -delete
%{_fixperms} -c %{buildroot}

%check
make test

%files
%license LICENSE
%doc Changes CODE_OF_CONDUCT.md CONTRIBUTING.md CREDITS README.md TODO
%{perl_vendorarch}/auto/DateTime/
%{perl_vendorarch}/DateTime/
%{perl_vendorarch}/DateTime.pm
%{_mandir}/man3/DateTime.3*
%{_mandir}/man3/DateTime::Conflicts.3*
%{_mandir}/man3/DateTime::Duration.3*
%{_mandir}/man3/DateTime::Infinite.3*
%{_mandir}/man3/DateTime::LeapSecond.3*
%{_mandir}/man3/DateTime::Types.3*

%changelog
* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2:1.65-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jun 12 2024 Jitka Plesnikova <jplesnik@redhat.com> - 2:1.65-5
- Perl 5.40 re-rebuild of bootstrapped packages

* Tue Jun 11 2024 Jitka Plesnikova <jplesnik@redhat.com> - 2:1.65-4
- Perl 5.40 rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2:1.65-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2:1.65-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Nov  6 2023 Paul Howarth <paul@city-fan.org> - 2:1.65-1
- Update to 1.65 (rhbz#2248104)
  - Fix builds on macOS with Perls before 5.22.0; this seems to have the same
    issue as Windows on older Perls (GH#141)

* Mon Oct 23 2023 Paul Howarth <paul@city-fan.org> - 2:1.63-1
- Update to 1.63 (rhbz#2245551)
  - Switched to using the 'Perl_isfinite' function instead of trying to
    implement this ourselves in XS code; this should fix quadmath builds on
    Windows (GH#139)

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2:1.59-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jul 12 2023 Jitka Plesnikova <jplesnik@redhat.com> - 2:1.59-4
- Perl 5.38 re-rebuild of bootstrapped packages

* Tue Jul 11 2023 Jitka Plesnikova <jplesnik@redhat.com> - 2:1.59-3
- Perl 5.38 rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2:1.59-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Oct 24 2022 Paul Howarth <paul@city-fan.org> - 2:1.59-1
- Update to 1.59
  - Fixed tests to pass with DateTime::Locale 1.37+ (GH#34)
- Use SPDX-format license tag

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2:1.58-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jun 03 2022 Jitka Plesnikova <jplesnik@redhat.com> - 2:1.58-3
- Perl 5.36 re-rebuild of bootstrapped packages

* Wed Jun 01 2022 Jitka Plesnikova <jplesnik@redhat.com> - 2:1.58-2
- Perl 5.36 rebuild

* Tue Apr 19 2022 Paul Howarth <paul@city-fan.org> - 2:1.58-1
- Update to 1.58
  - Fixed tests so that they ignore the value set in the
    'PERL_DATETIME_DEFAULT_TZ' env var, if one exists (GH#128)

* Thu Mar  3 2022 Paul Howarth <paul@city-fan.org> - 2:1.57-1
- Update to 1.57
  - The last release would die if Sub::Util was not available, but this
    should just be an optional requirement (GH#131); this is the second
    time I've introduced this bug, so now there's a test to make sure
    that DateTime can be loaded if Sub::Util is not installed, which will
    hopefully prevent a third occurrence of this bug

* Thu Mar  3 2022 Paul Howarth <paul@city-fan.org> - 2:1.56-1
- Update to 1.56
  - The DateTime->from_epoch constructor now accepts a single, non-hashref
    argument, and validates it as an epoch value (GH#119)

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2:1.55-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Dec 24 2021 Paul Howarth <paul@city-fan.org> - 2:1.55-1
- Update to 1.55
  - Another documentation fix release; this fixes some mistakes, fixes some
    broken links, and removes all references to the long-dead datetime.perl.org

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2:1.54-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon May 24 2021 Jitka Plesnikova <jplesnik@redhat.com> - 2:1.54-5
- Perl 5.34 re-rebuild of bootstrapped packages

* Mon May 24 2021 Jitka Plesnikova <jplesnik@redhat.com> - 2:1.54-4
- Perl 5.34 re-rebuild of bootstrapped packages

* Sun May 23 2021 Jitka Plesnikova <jplesnik@redhat.com> - 2:1.54-3
- Perl 5.34 rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2:1.54-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sat Dec  5 2020 Paul Howarth <paul@city-fan.org> - 2:1.54-1
- Update to 1.54
  - Documentation updates

* Mon Nov  9 2020 Paul Howarth <paul@city-fan.org> - 2:1.53-1
- Update to 1.53
  - Added a $dt->rfc3339 method, based on discussion in GH#109

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2:1.52-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jun 26 2020 Jitka Plesnikova <jplesnik@redhat.com> - 2:1.52-3
- Perl 5.32 re-rebuild of bootstrapped packages

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 2:1.52-2
- Perl 5.32 rebuild

* Mon Mar  2 2020 Paul Howarth <paul@city-fan.org> - 2:1.52-1
- Update to 1.52
  - Added a $dt->is_between($dt1, $dt2) method (based on GH#97)
  - Simplify the calculation of leap seconds in XS (GH#91); this is a little
    more efficient for most use cases (anything with future or recent past
    datetimes)

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2:1.51-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2:1.51-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Jun 02 2019 Jitka Plesnikova <jplesnik@redhat.com> - 2:1.51-3
- Perl 5.30 re-rebuild of bootstrapped packages

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 2:1.51-2
- Perl 5.30 rebuild

* Mon Apr 22 2019 Paul Howarth <paul@city-fan.org> - 2:1.51-1
- Update to 1.51
  - Fix CLDR formatting of 'S' pattern with more than 9 digits of precision;
    while we only store nanoseconds in the DateTime object we should still be
    able to handle an arbitrary number of digits properly (GH#89)
- Modernize spec using %%{make_build} and %%{make_install}

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2:1.50-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Aug  2 2018 Paul Howarth <paul@city-fan.org> - 2:1.50-1
- Update to 1.50
  - The %%F strftime pattern incorrectly zero-padded numbers less than four
    digits; according to POSIX::strftime, this should output the year as-is
    without padding (GH#83)

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2:1.49-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jun 29 2018 Jitka Plesnikova <jplesnik@redhat.com> - 2:1.49-2
- Perl 5.28 rebuild

* Mon May 21 2018 Paul Howarth <paul@city-fan.org> - 2:1.49-1
- Update to 1.49
  - Updated the ppport.h with the latest version of Devel::PPPort, which fixes
    a compilation warning when compiling with 5.27.11 (GH#81)
- Switch upstream from search.cpan.org to metacpan.org

* Mon Mar 26 2018 Paul Howarth <paul@city-fan.org> - 2:1.48-1
- Update to 1.48
  - The last release would die if Sub::Util was not available, but this should
    just be an optional requirement (GH#77, GH#78)

* Mon Mar 26 2018 Paul Howarth <paul@city-fan.org> - 2:1.47-1
- Update to 1.47
  - DateTime::Duration->multiply now only allows integer multipliers (GH#73)
  - Added is_last_day_of_quarter() and is_last_day_of_year() methods (GH#72)
  - When an exception was thrown while adding a duration, the object could be
    left in a broken state with the duration partially applied; subsequent
    addition or subtraction would produce the wrong results (GH#74)
- Add patch to support use without Sub::Util (GH#77, GH#78)

* Mon Feb 12 2018 Paul Howarth <paul@city-fan.org> - 2:1.46-1
- Update to 1.46
  - Fixed the formatting for the CLDR "S" symbol, which in some cases would
    round up to 1 instead of truncating a value, e.g. the "SSS" symbol would
    format 999,999,999 nanoseconds as "1.000" (GH#71)

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2:1.45-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sun Dec 31 2017 Paul Howarth <paul@city-fan.org> - 2:1.45-1
- Update to 1.45
  - Added month_length(), quarter_length() and year_length() methods (GH#70)

* Tue Aug 22 2017 Paul Howarth <paul@city-fan.org> - 2:1.44-1
- Update to 1.44
  - Added a stringify() method, which does exactly the same thing as
    stringification overloading does (GH#58)
  - Added an is_last_day_of_month() method to indicate whether or not an object
    falls on the last day of its month (GH#60)

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2:1.43-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2:1.43-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jun 06 2017 Jitka Plesnikova <jplesnik@redhat.com> - 2:1.43-2
- Perl 5.26 rebuild

* Tue May 30 2017 Paul Howarth <paul@city-fan.org> - 2:1.43-1
- Update to 1.43
  - Added a small optimization for boolification overloading: rather than
    relying on a fallback to stringification, we now return true directly,
    which is a little faster in cases like "if ($might_be_dt) { ... }"
  - The datetime() method now accepts a single argument to use as the separator
    between the date and time portion; this defaults to "T"
- Drop redundant Group: tag

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2:1.42-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 26 2016 Paul Howarth <paul@city-fan.org> - 2:1.42-1
- Update to 1.42
  - The DateTime::Duration->add and ->subtract methods now accept
    DateTime::Duration objects; this used to work by accident but is now done
    intentionally, with docs and tests (GH#50)

* Thu Nov 17 2016 Paul Howarth <paul@city-fan.org> - 2:1.41-1
- Update to 1.41
  - The DateTime->add and ->subtract methods now accept DateTime::Duration
    objects; this used to work by accident but is now done intentionally, with
    docs and tests (GH#45)

* Sun Nov 13 2016 Paul Howarth <paul@city-fan.org> - 2:1.40-1
- Update to 1.40
  - Switched from RT to the GitHub issue tracker

* Mon Sep 19 2016 Paul Howarth <paul@city-fan.org> - 2:1.39-1
- Update to 1.39
  - Replaced Params::Validate with Params::ValidationCompiler and Specio
    - In my benchmarks this makes constructing a new DateTime object about 14%%
      faster
    - However, it slows down module load time by about 100 milliseconds (1/10
      of a second) on my desktop system with a primed cache (so really
      measuring compile time, not disk load time)
  - When you pass a locale to $dt->set you will now get a warning suggesting
    you should use $dt->set_locale instead (CPAN RT#115420)
  - Bump minimum required Perl to 5.8.4 from 5.8.1
- Use NO_PERLLOCAL=1 so we can use "make install"

* Sun Aug  7 2016 Paul Howarth <paul@city-fan.org> - 2:1.36-1
- Update to 1.36
  - Require namespace::autoclean 0.19

* Sat Aug  6 2016 Paul Howarth <paul@city-fan.org> - 2:1.35-1
- Update to 1.35
  - Use namespace::autoclean in all packages that import anything; without
    cleaning the namespace, DateTime ends up with "methods" like try and catch
    (from Try::Tiny), which can lead to very confusing bugs (CPAN RT#115983)

* Wed Jul  6 2016 Paul Howarth <paul@city-fan.org> - 2:1.34-1
- Update to 1.34
  - Added the leap second coming on December 31, 2016

* Wed Jun 29 2016 Paul Howarth <paul@city-fan.org> - 2:1.33-1
- Update to 1.33
  - When you pass a locale to $dt->set you will now get a warning suggesting
    you should use $dt->set_locale instead (CPAN RT#115420)
  - Added support for $dt->truncate( to => 'quarter' ) (GH#17)
  - Fixed the $dt->set docs to say that you cannot pass a locale (even though
    you can but you'll get a warning) and added more docs for $dt->set_locale
  - Require DateTime::Locale 1.05
  - Require DateTime::TimeZone 2.00
- Take advantage of NO_PACKLIST option in recent EU:MM

* Sun May 22 2016 Paul Howarth <paul@city-fan.org> - 2:1.28-1
- Update to 1.28
  - Fixed handling of some floating point epochs; since DateTime treated the
    epoch like a string instead of a number, certain epochs with a non-integer
    value ended up treated like integers (Perl is weird) (GH#15, fixes GH#6)

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 2:1.27-2
- Perl 5.24 rebuild

* Sat May 14 2016 Paul Howarth <paul@city-fan.org> - 2:1.27-1
- Update to 1.27
  - Added an environment variable PERL_DATETIME_DEFAULT_TZ to globally set the
    default time zone (GH#14); using this is very dangerous - be careful!
- BR: perl-generators

* Tue Mar 22 2016 Paul Howarth <paul@city-fan.org> - 2:1.26-1
- Update to 1.26
  - Switched from Module::Build to ExtUtils::MakeMaker (GH#13)

* Mon Mar  7 2016 Paul Howarth <paul@city-fan.org> - 2:1.25-1
- Update to 1.25
  - DateTime->from_object would die if given a DateTime::Infinite object; now
    it returns another DateTime::Infinite object (CPAN RT#112712)
- Simplify find command using -empty and -delete

* Tue Mar  1 2016 Paul Howarth <paul@city-fan.org> - 2:1.24-1
- Update to 1.24
  - The last release partially broke $dt->time; if you passed a value to use
    as unit separator, it was ignored (CPAN RT#112585)

* Mon Feb 29 2016 Paul Howarth <paul@city-fan.org> - 2:1.23-1
- Update to 1.23
  - Fixed several issues with the handling of non-integer values passed to
    from_epoch() (GH#11)
    - This method was simply broken for negative values, which would end up
      being incremented by a full second, so for example -0.5 became 0.5
    - The method did not accept all valid float values; specifically, it did
      not accept values in scientific notation
    - Finally, this method now rounds all non-integer values to the nearest
      millisecond, which matches the precision we can expect from Perl itself
      (53 bits) in most cases
  - Make all DateTime::Infinite objects return the system's representation of
    positive or negative infinity for any method that returns a number or
    string representation (year(), month(), ymd(), iso8601(), etc.); previously
    some of these methods could return "Nan", "-Inf--Inf--Inf", and other
    confusing outputs (CPAN RT#110341)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2:1.21-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Nov 13 2015 Paul Howarth <paul@city-fan.org> - 2:1.21-1
- Update to 1.21
  - Make all tests pass with the current DateTime::Locale
- Explicitly BR: perl-devel, needed for EXTERN.h

* Fri Jul 24 2015 Petr Pisar <ppisar@redhat.com> - 2:1.20-1
- 1.20 bump

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:1.18-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 2:1.18-2
- Perl 5.22 rebuild

* Tue Jan  6 2015 Paul Howarth <paul@city-fan.org> - 2:1.18-1
- 1.18 bump

* Mon Jan  5 2015 Paul Howarth <paul@city-fan.org> - 2:1.17-1
- 1.17 bump
- Use %%license
- Make %%files list more explicit

* Mon Jan  5 2015 Paul Howarth <paul@city-fan.org> - 2:1.14-1
- 1.14 bump

* Wed Sep 03 2014 Jitka Plesnikova <jplesnik@redhat.com> - 2:1.12-2
- Perl 5.20 rebuild

* Tue Sep 02 2014 Petr Pisar <ppisar@redhat.com> - 2:1.12-1
- 1.12 bump

* Fri Aug 29 2014 Jitka Plesnikova <jplesnik@redhat.com> - 2:1.10-4
- Perl 5.20 rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:1.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:1.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 07 2014 Petr Pisar <ppisar@redhat.com> - 2:1.10-1
- 1.10 bump

* Fri Mar 14 2014 Paul Howarth <paul@city-fan.org> - 2:1.08-1
- 1.08 bump

* Mon Feb 10 2014 Paul Howarth <paul@city-fan.org> - 2:1.07-1
- 1.07 bump

* Fri Jan 03 2014 Petr Pisar <ppisar@redhat.com> - 2:1.06-1
- 1.06 bump

* Tue Dec 10 2013 Petr Pisar <ppisar@redhat.com> - 2:1.04-1
- 1.04 bump

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:1.03-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 30 2013 Petr Pisar <ppisar@redhat.com> - 2:1.03-2
- Perl 5.18 rebuild

* Tue Jun 25 2013 Jitka Plesnikova <jplesnik@redhat.com> - 2:1.03-1
- 1.03 bump

* Tue Apr 02 2013 Petr Šabata <contyk@redhat.com> - 2:1.01-1
- 1.01 bump

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:0.78-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Nov 19 2012 Petr Pisar <ppisar@redhat.com> - 2:0.78-1
- 0.78 bump

* Thu Oct 18 2012 Petr Pisar <ppisar@redhat.com> - 2:0.77-1
- 0.77 bump

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:0.70-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 20 2012 Petr Pisar <ppisar@redhat.com> - 2:0.70-4
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:0.70-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Aug 18 2011 Iain Arnell <iarnell@gmail.com> 2:0.70-2
- Additional (Build)Requires from unofficial review

* Mon Aug 15 2011 Iain Arnell <iarnell@gmail.com> 2:0.70-1
- Unbundle DateTime::TimeZone and DateTime::Locale
- Bump epoch and revert to upstream versioning
- Specfile regenerated by cpanspec 1.78.
- Update description

* Wed Jul 20 2011 Petr Sabata <contyk@redhat.com> - 1:0.7000-3
- Perl mass rebuild

* Mon Jul 04 2011 Iain Arnell <iarnell@gmail.com> 1:0.7000-2
- update DateTime::TimeZone to 1.35 (Olson 2011h)
- add rpm 4.9 filtering macros

* Fri May 13 2011 Iain Arnell <iarnell@gmail.com> 1:0.7000-1
- update DateTime to 0.70

* Wed May 04 2011 Iain Arnell <iarnell@gmail.com> 1:0.6900-1
- update DateTime to 0.69
- update DateTime::TimeZone to 1.34 (Olson 2011g)

* Sun Apr 24 2011 Iain Arnell <iarnell@gmail.com> 1:0.6600-6
- fix the testing for loop

* Sun Apr 24 2011 Iain Arnell <iarnell@gmail.com> 1:0.6600-5
- update DateTime::TimeZone to 1.33 (Olson 2011f)

* Wed Apr 06 2011 Iain Arnell <iarnell@gmail.com> 1:0.6600-4
- update DateTime::TimeZone to 1.32 (Olson 2011e)

* Sat Mar 26 2011 Iain Arnell <iarnell@gmail.com> 1:0.6600-3
- update DateTime::TimeZone to 1.31
- DateTime::TimeZone no longer has Build.PL; use Makefile.PL
- whitespace cleanup
- clean up .packlist

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.6600-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Dec 12 2010 Steven Pritchard <steve@kspei.com> 1:0.6600-1
- Update DateTime to 0.66.
- Update DateTime::TimeZone to 1.26.
- Update URL for FAQ in description.
- BR Class::Load and parent.

* Sat Oct 09 2010 Iain Arnell <iarnell@gmail.com> 1:0.6300-1
- Update DateTime to 0.63
- Update DateTime::TimeZone to 1.22
- DateTime license changed from "GPL+ or Artistic" to "Artistic 2.0"
- Fix DTLocale/Changelog encoding

* Mon Jun 14 2010 Petr Sabata <psabata@redhat.com> - 1:0.5300-4
- perl-DateTime-Locale-0.45 update

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 1:0.5300-3
- Mass rebuild with perl-5.12.0

* Wed Jan 27 2010 Stepan Kasal <skasal@redhat.com> - 1:0.5300-2
- new upstream version of DateTime-TimeZone

* Fri Jan 15 2010 Stepan Kasal <skasal@redhat.com> - 1:0.5300-1
- new upstream version
- use Build.PL as Makefile.PL no longer exists
- use iconv to recode to utf-8, not a patch
- update BuildRequires
- drop Provides: perl(DateTime::TimeZoneCatalog), it is no longer there
- use filtering macros

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1:0.4501-4
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.4501-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.4501-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Dec 09 2008 Steven Pritchard <steve@kspei.com> 1:0.4501-1
- Update to DateTime 0.4501.

* Mon Nov 10 2008 Steven Pritchard <steve@kspei.com> 1:0.4401-1
- Update to DateTime 0.4401.
- Update to DateTime::Locale 0.42.
- Update to DateTime::TimeZone 0.8301.

* Mon Sep 08 2008 Steven Pritchard <steve@kspei.com> 1:0.4304-2
- Update to DateTime::TimeZone 0.7904.

* Tue Jul 15 2008 Steven Pritchard <steve@kspei.com> 1:0.4304-1
- Update to DateTime 0.4304.
- Update to DateTime::TimeZone 0.78.
- Update to DateTime::Locale 0.41.

* Tue Jul 08 2008 Steven Pritchard <steve@kspei.com> 1:0.4302-2
- Update to DateTime::TimeZone 0.7701.

* Sat May 31 2008 Steven Pritchard <steve@kspei.com> 1:0.4302-1
- Update to DateTime 0.4302.
- Update to DateTime::TimeZone 0.77.
- Update to DateTime::Locale 0.4001.
- BR List::MoreUtils.
- Define IS_MAINTAINER so we run the pod tests.

* Thu May 15 2008 Steven Pritchard <steve@kspei.com> 1:0.42-1
- Update to DateTime 0.42.
- Update to DateTime::TimeZone 0.75.
- Update FAQ URL in description.

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1:0.41-5
- Rebuild for perl 5.10 (again)

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1:0.41-4
- Autorebuild for GCC 4.3

* Thu Jan 24 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1:0.41-3
- rebuild for new perl

* Tue Dec 11 2007 Steven Pritchard <steve@kspei.com> 1:0.41-2
- Update License tag.
- Update to DateTime::TimeZone 0.70.

* Mon Sep 17 2007 Steven Pritchard <steve@kspei.com> 1:0.41-1
- Update to DateTime 0.41.
- Update to DateTime::Locale 0.35.
- Update to DateTime::TimeZone 0.67.

* Wed Aug 29 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> - 1:0.39-2
- Rebuild for selinux ppc32 issue.

* Sun Jul 22 2007 Steven Pritchard <steve@kspei.com> 1:0.39-1
- Update to DateTime 0.39.
- Update to DateTime::TimeZone 0.6603.

* Thu Jul 05 2007 Steven Pritchard <steve@kspei.com> 1:0.38-2
- BR Test::Output.

* Mon Jul 02 2007 Steven Pritchard <steve@kspei.com> 1:0.38-1
- Update to DateTime 0.38.
- Update to DateTime::TimeZone 0.6602.
- BR Test::Pod::Coverage.

* Mon Apr 02 2007 Steven Pritchard <steve@kspei.com> 1:0.37-3
- Drop BR DateTime::Format::* to avoid circular build deps.

* Mon Apr 02 2007 Steven Pritchard <steve@kspei.com> 1:0.37-2
- Filter Win32::TieRegistry dependency.
- Do the provides filter like we do in cpanspec.
- Drop some macro usage.

* Sat Mar 31 2007 Steven Pritchard <steve@kspei.com> 1:0.37-1
- Update to DateTime 0.37.
- Update to DateTime::TimeZone 0.63.

* Tue Mar 13 2007 Steven Pritchard <steve@kspei.com> 1:0.36-2
- Update to DateTime::Locale 0.34.
- Update to DateTime::TimeZone 0.62.

* Mon Jan 22 2007 Steven Pritchard <steve@kspei.com> 1:0.36-1
- Update to Date::Time 0.36.
- Update to DateTime::Locale 0.33.
- Update to DateTime::TimeZone 0.59.

* Fri Nov 03 2006 Steven Pritchard <steve@kspei.com> 1:0.35-1
- Update to DateTime 0.35.
- Update to DateTime::Locale 0.3101.
- LICENSE.icu seems to have been renamed LICENSE.cldr.
- Update to DateTime::TimeZone 0.54.
- Use fixperms macro instead of our own chmod incantation.
- Convert DateTime::LeapSecond to UTF-8 to avoid a rpmlint warning.

* Tue Aug 29 2006 Steven Pritchard <steve@kspei.com> 1:0.34-3
- Update to DateTime::TimeZone 0.48.

* Mon Aug 28 2006 Steven Pritchard <steve@kspei.com> 1:0.34-2
- Update to DateTime::TimeZone 0.47.

* Mon Aug 14 2006 Steven Pritchard <steve@kspei.com> 1:0.34-1
- Update to DateTime 0.34.

* Fri Jul 28 2006 Steven Pritchard <steve@kspei.com> 1:0.32-1
- Update to DateTime 0.32.
- Improve Summary, description, and source URLs.
- Fix find option order.

* Thu Jul 13 2006 Steven Pritchard <steve@kspei.com> 1:0.31-2
- BR DateTime::Format::ICal and DateTime::Format::Strptime for better
  test coverage.

* Wed May 24 2006 Steven Pritchard <steve@kspei.com> 1:0.31-1
- Update DateTime to 0.31.
- Update DateTime::TimeZone to 0.46.

* Mon Feb 27 2006 Steven Pritchard <steve@kspei.com> 1:0.30-3
- Bump Epoch (argh, 0.2901 > 0.30 to rpm)
- Update DateTime::TimeZone to 0.42

* Sat Feb 18 2006 Steven Pritchard <steve@kspei.com> 0.30-2
- Update DateTime::TimeZone to 0.41

* Tue Jan 10 2006 Steven Pritchard <steve@kspei.com> 0.30-1
- Update DateTime to 0.30
- Update DateTime::TimeZone to 0.40

* Fri Sep 16 2005 Paul Howarth <paul@city-fan.org> 0.2901-2
- Unpack each tarball only once
- Use Module::Build's build script where available
- Help each module find the others when needed
- Clean up files list
- Include additional documentation from DT::Locale & DT::TimeZone
- Add BR: perl(File::Find::Rule) & perl(Test::Pod) to improve test coverage
- Remove unversioned provides of perl(DateTime) & perl(DateTime::TimeZone)

* Wed Aug 31 2005 Steven Pritchard <steve@kspei.com> 0.2901-1
- Specfile autogenerated.
