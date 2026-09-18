# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# noarch, but to avoid debug* files interfering with manifest test:
%global debug_package %{nil}

# Similarly, for package note feature
%undefine _package_note_file

Name:		perl-Test-Mojibake
Version:	1.3
Release:	34%{?dist}
Summary:	Check your source for encoding misbehavior
License:	GPL-1.0-or-later OR Artistic-1.0-Perl
URL:		https://metacpan.org/release/Test-Mojibake
Source0:	https://cpan.metacpan.org/modules/by-module/Test/Test-Mojibake-%{version}.tar.gz
BuildArch:	noarch
# ===================================================================
# Module build requirements
# ===================================================================
BuildRequires:	coreutils
BuildRequires:	findutils
BuildRequires:	make
BuildRequires:	perl-generators
BuildRequires:	perl-interpreter
BuildRequires:	perl(ExtUtils::MakeMaker)
# ===================================================================
# Module requirements
# ===================================================================
BuildRequires:	perl(File::Spec::Functions)
BuildRequires:	perl(Pod::Usage)
BuildRequires:	perl(strict)
BuildRequires:	perl(Test::Builder)
BuildRequires:	perl(warnings)
# ===================================================================
# Optional module requirements
# ===================================================================
BuildRequires:	perl(Unicode::CheckUTF8)
# ===================================================================
# Regular test suite requirements
# ===================================================================
BuildRequires:	perl(blib)
BuildRequires:	perl(Test::Builder::Tester)
BuildRequires:	perl(Test::More) >= 0.96
BuildRequires:	perl(Test::Script)
# ===================================================================
# Author/Release test requirements
#
# Don't run these tests or include their requirements if we're
# bootstrapping, as many of these modules require each other for
# their author/release tests.
# ===================================================================
%if 0%{!?perl_bootstrap:1}
BuildRequires:	perl(Perl::Critic) >= 1.094
BuildRequires:	perl(Pod::Coverage::TrustPod)
BuildRequires:	perl(Test::CPAN::Changes)
BuildRequires:	perl(Test::CPAN::Meta)
BuildRequires:	perl(Test::CPAN::Meta::JSON)
BuildRequires:	perl(Test::DistManifest)
BuildRequires:	perl(Test::EOL)
BuildRequires:	perl(Test::HasVersion)
BuildRequires:	perl(Test::MinimumVersion)
BuildRequires:	perl(Test::NoTabs)
BuildRequires:	perl(Test::Perl::Critic)
BuildRequires:	perl(Test::Pod) >= 1.41
BuildRequires:	perl(Test::Pod::Coverage) >= 1.08
BuildRequires:	perl(Test::Portability::Files)
BuildRequires:	perl(Test::Synopsis)
%if 0%{?fedora} < 39 && 0%{?rhel} < 10
BuildRequires:	perl(Test::Vars)
%endif
BuildRequires:	perl(Test::Version)
# Modules only available from EL-8
%if 0%{?fedora} || 0%{?rhel} > 7
BuildRequires:	perl(Perl::Critic::Policy::Modules::ProhibitModuleShebang)
BuildRequires:	perl(Test::Kwalitee) >= 1.21
BuildRequires:	perl(Test::Pod::LinkCheck)
%endif
%endif
# ===================================================================
# Dependencies
# ===================================================================
# Unicode::CheckUTF8 is an optional requirement that significantly speeds up
# this module
Requires:	perl(Unicode::CheckUTF8)

%description
Many modern text editors automatically save files using UTF-8 codification.
However, the perl interpreter does not expect it by default. Whilst this does
not represent a big deal on (most) backend-oriented programs, Web framework
(Catalyst, Mojolicious) based applications will suffer so-called Mojibake
(literally: "unintelligible sequence of characters"). Even worse: if an editor
saves BOM (Byte Order Mark, U+FEFF character in Unicode) at the start of a
script with the executable bit set (on Unix systems), it won't execute at all,
due to shebang corruption.

Avoiding codification problems is quite simple:

 * Always use utf8/use common::sense when saving source as UTF-8
 * Always specify =encoding utf8 when saving POD as UTF-8
 * Do neither of above when saving as ISO-8859-1
 * Never save BOM (not that it's wrong; just avoid it as you'll barely
   notice its presence when in trouble)

However, if you find yourself upgrading old code to use UTF-8 or trying to
standardize a big project with many developers, each one using a different
platform/editor, reviewing all files manually can be quite painful, especially
in cases where some files have multiple encodings (note: it all started when I
realized that gedit and derivatives are unable to open files with character
conversion tables).

Enter the Test::Mojibake ;)

%prep
%setup -q -n Test-Mojibake-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
%{_fixperms} -c %{buildroot}

%check
make test %{!?perl_bootstrap:AUTHOR_TESTING=1 RELEASE_TESTING=1} \
%if ! 0%{?fedora} && 0%{?rhel} < 8
	TEST_FILES="$(echo $(find t/ -name '*.t' | grep -Fv release-kwalitee.t))"
%endif

%files
%license LICENSE
%doc Changes README
%{_bindir}/scan_mojibake
%{perl_vendorlib}/Test/
%{_mandir}/man1/scan_mojibake.1*
%{_mandir}/man3/Test::Mojibake.3*

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-34
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-33
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-32
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jan 26 2024 Paul Howarth <paul@city-fan.org> - 1.3-31
- Drop BR: perl(Test::Vars) from Fedora 39 onwards as Test::Vars is FTBFS with
  Perl 5.38

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-30
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-29
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jun 03 2022 Jitka Plesnikova <jplesnik@redhat.com> - 1.3-25
- Perl 5.36 re-rebuild of bootstrapped packages

* Wed Jun 01 2022 Jitka Plesnikova <jplesnik@redhat.com> - 1.3-24
- Perl 5.36 rebuild

* Fri Mar 11 2022 Paul Howarth <paul@city-fan.org> - 1.3-23
- Fix FTBFS triggered by package note feature
- Use %%license unconditionally
- Drop workarounds for EL-6 support

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon May 24 2021 Jitka Plesnikova <jplesnik@redhat.com> - 1.3-20
- Perl 5.34 re-rebuild of bootstrapped packages

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 1.3-19
- Perl 5.34 rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jun 26 2020 Jitka Plesnikova <jplesnik@redhat.com> - 1.3-16
- Perl 5.32 re-rebuild of bootstrapped packages

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 1.3-15
- Perl 5.32 rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Oct 29 2019 Paul Howarth <paul@city-fan.org> - 1.3-13
- Spec tidy up
  - Use author-independent source URL
  - Drop some legacy conditionals
  - Drop redundant buildroot cleaning in %%install section

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Jun 02 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.3-11
- Perl 5.30 re-rebuild of bootstrapped packages

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.3-10
- Perl 5.30 rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sun Jul 01 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.3-7
- Perl 5.28 re-rebuild of bootstrapped packages

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.3-6
- Perl 5.28 rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jun 07 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.3-3
- Perl 5.26 re-rebuild of bootstrapped packages

* Mon Jun 05 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.3-2
- Perl 5.26 rebuild

* Mon Feb  6 2017 Paul Howarth <paul@city-fan.org> - 1.3-1
- Update to 1.3
  - Minor fixes to pass the release tests
  - Add MetaJSON plugin (GH#12)
  - Add new optional dependency on Unicode::CheckUTF8::PP, a Pure Perl
    implementation of Unicode::CheckUTF8
  - Fixed off-by-one (GH#10)
  - Fixed SYNOPSIS
- Work around bug in GNU tar 1.15.1 that breaks extracting tarballs made with
  unknown extended attributes on old distributions
- Drop EL-5 build support
- Update patches as needed

* Wed May 18 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.1-5
- Perl 5.24 re-rebuild of bootstrapped packages

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.1-4
- Perl 5.24 rebuild

* Fri Feb 19 2016 Paul Howarth <paul@city-fan.org> - 1.1-3
- Make SYNOPSIS compilable perl (#1309966)
- Use %%license where possible

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Sep  3 2015 Paul Howarth <paul@city-fan.org> - 1.1-1
- Update to 1.1
  - Distribution maintenance
  - Handle the case where all_files_encoding_ok has no files to test by
    skipping all tests
- Re-enable use of Test::Vars with Perl 5.22
- Avoid the Kwalitee test if we don't have a recent enough Test::Kwalitee
- Update patches as needed

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 10 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.0-6
- Perl 5.22 re-rebuild of bootstrapped packages
- Disable using of Test::Vars with Perl 5.22

* Fri Jun 05 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.0-5
- Perl 5.22 rebuild

* Sun Sep 07 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.0-4
- Perl 5.20 re-rebuild of bootstrapped packages

* Thu Aug 28 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.0-3
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 21 2014 Paul Howarth <paul@city-fan.org> - 1.0-1
- Update to 1.0
  - Use proper source for ASCII-only characters
  - Dist::Zilla-related updates
  - Fixing the "comment in regexp" other way around
  - Fix regex to properly ignore comments
- Update EPEL support patches

* Mon Jan 27 2014 Paul Howarth <paul@city-fan.org> - 0.9-3
- Bootstrap build for epel7 done

* Mon Jan 27 2014 Paul Howarth <paul@city-fan.org> - 0.9-2
- Bootstrap epel7 build

* Mon Jan 20 2014 Paul Howarth <paul@city-fan.org> - 0.9-1
- Update to 0.9
  - More consistent UTF-8 naming in docs
  - Dist::Zilla maintenance
  - Fixed shebang in scan_mojibake
    (https://github.com/creaktive/Test-Mojibake/issues/7)
- Update patch for building with old Test::More versions

* Wed Aug 14 2013 Jitka Plesnikova <jplesnik@redhat.com> - 0.8-4
- Perl 5.18 re-rebuild of bootstrapped packages

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Jul 21 2013 Petr Pisar <ppisar@redhat.com> - 0.8-2
- Perl 5.18 rebuild

* Sat Jan 26 2013 Paul Howarth <paul@city-fan.org> - 0.8-1
- Update to 0.8
  - Fixed cyclic t/ deps
  - Added the standalone scan_mojibake utility
  - Listed Unicode::CheckUTF8 as a recommended prerequisite
  - Recognize utf8::all
  - Passes perlcritic harsh
- Drop BR: perl(File::Spec)
- BR: perl(File::Spec::Functions), perl(Pod::Usage) and perl(Test::Script)
- BR: perl(Test::Pod::LinkCheck) where available
- Perl::Critic ≥ 1.094 now needed for the 'equivalent_modules' parameter in
  TestingAndDebugging::RequireUseStrict, unavailable in EPEL-5
- Update patch for building with old Test::More versions
- Drop %%defattr, redundant since rpm 4.4

* Mon Oct  1 2012 Paul Howarth <paul@city-fan.org> - 0.7-1
- Update to 0.7
  - Fixed multiple =encoding behavior
  - More deterministic t/01-bad-check.t

* Sat Sep 29 2012 Paul Howarth <paul@city-fan.org> - 0.6-1
- Update to 0.6
  - Fixed incorrect test examples
- Reinstate BR: perl(Test::Kwalitee) now that kwalitee test is back

* Thu Sep 27 2012 Paul Howarth <paul@city-fan.org> - 0.5-1
- Update to 0.5
  - Attempt to fix https://github.com/creaktive/Test-Mojibake/issues/2
    (don't fail when no lib directory exists)
  - Kwalitee won't complain any more
- Kwalitee test dropped upstream, so no longer need BR: perl(Test::Kwalitee)

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 10 2012 Petr Pisar <ppisar@redhat.com> - 0.4-3
- Perl 5.16 re-rebuild of bootstrapped packages

* Thu Jun 28 2012 Petr Pisar <ppisar@redhat.com> - 0.4-2
- Perl 5.16 rebuild

* Tue Jun 26 2012 Paul Howarth <paul@city-fan.org> - 0.4-1
- Update to 0.4
  - _detect_utf8: PP version now handles overlong UTF-8 sequences
  - Tests update (96% coverage)
  - Dist::Zilla update
- BR: perl(Perl::Critic::Policy::Modules::ProhibitModuleShebang),
  perl(Test::EOL) and perl(Test::Version)
- BR: perl(Test::Kwalitee), perl(Test::MinimumVersion),
  perl(Test::Perl::Critic) and perl(Test::Synopsis) unconditionally
- Drop support for building for EPEL-4
- Drop patch for building with ExtUtils::MakeMaker < 6.30
- Update patch for building with Test::More < 0.88
- Add patch to support building without Test::Version
- Add workaround for the old version of PPI in EPEL-5 not being able to
  handle the unicode byte order mark in t/bom.pl, which breaks
  t/release-minimum-version.t
- Don't need to remove empty directories from the buildroot
- Use DESTDIR rather than PERL_INSTALL_ROOT

* Mon Jun 11 2012 Petr Pisar <ppisar@redhat.com> - 0.3-5
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Oct  4 2011 Paul Howarth <paul@city-fan.org> - 0.3-3
- BR/R: perl(Unicode::CheckUTF8) for improved performance

* Thu Aug 11 2011 Paul Howarth <paul@city-fan.org> - 0.3-2
- Sanitize for Fedora/EPEL submission

* Thu Aug 11 2011 Paul Howarth <paul@city-fan.org> - 0.3-1
- Initial RPM version
