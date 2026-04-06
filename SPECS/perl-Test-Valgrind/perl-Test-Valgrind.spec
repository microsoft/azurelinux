# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Build --with debug_valgrind for multi-arch build and additional valgrind debugging
%bcond_with debug_valgrind

# A noarch-turned-arch package should not have debuginfo
%global debug_package %{nil}

Name:		perl-Test-Valgrind
Summary:	Generate suppressions, analyze and test any command with valgrind
Version:	1.19
Release:	28%{?dist}
License:	GPL-1.0-or-later OR Artistic-1.0-Perl
URL:		https://metacpan.org/release/Test-Valgrind
Source0:	https://cpan.metacpan.org/modules/by-module/Test/Test-Valgrind-%{version}.tar.gz
Patch1:		Test-Valgrind-1.19-Perl_pp_entersub.patch
%if !%{with debug_valgrind}
BuildArch:	noarch
%endif
# Module Build
BuildRequires:	coreutils
BuildRequires:	findutils
BuildRequires:	gcc
BuildRequires:	make
BuildRequires:	perl-devel
BuildRequires:	perl-generators
BuildRequires:	perl-interpreter
BuildRequires:	perl(ExtUtils::Install) >= 1.38
BuildRequires:	perl(ExtUtils::MakeMaker)
BuildRequires:	sed
# Module Runtime
BuildRequires:	perl(base)
BuildRequires:	perl(Carp)
BuildRequires:	perl(Config)
BuildRequires:	perl(Digest::MD5)
BuildRequires:	perl(DynaLoader)
BuildRequires:	perl(Env::Sanctify)
BuildRequires:	perl(ExtUtils::MM)
BuildRequires:	perl(Fcntl)
BuildRequires:	perl(File::HomeDir) >= 0.86
BuildRequires:	perl(File::Path)
BuildRequires:	perl(File::Spec)
BuildRequires:	perl(File::Temp) >= 0.19
BuildRequires:	perl(Filter::Util::Call)
BuildRequires:	perl(IO::Select)
BuildRequires:	perl(List::Util)
BuildRequires:	perl(overload)
BuildRequires:	perl(Perl::Destruct::Level)
BuildRequires:	perl(POSIX)
BuildRequires:	perl(Scalar::Util)
BuildRequires:	perl(strict)
BuildRequires:	perl(Test::Builder)
BuildRequires:	perl(warnings)
BuildRequires:	perl(XML::Twig)
BuildRequires:	perl(XML::Twig::Elt)
BuildRequires:	valgrind >= 3.1.0
# Test Suite
BuildRequires:	perl(lib)
BuildRequires:	perl(Test::More)
BuildRequires:	perl(Time::HiRes)
BuildRequires:	perl(XSLoader)
# Dependencies
Requires:	perl(Carp)
Requires:	perl(Config)
Requires:	perl(Digest::MD5)
Requires:	perl(DynaLoader)
Requires:	perl(File::HomeDir) >= 0.86
Requires:	perl(File::Path)
Requires:	perl(File::Temp) >= 0.14
Requires:	perl(Filter::Util::Call)
Requires:	perl(Perl::Destruct::Level)
Requires:	perl(XML::Twig)
Requires:	perl(XML::Twig::Elt)
Requires:	valgrind >= 3.1.0

%description
The Test::Valgrind::* API lets you run Perl code through the memcheck tool of
the valgrind memory debugger, to test for memory errors and leaks. The
Test::Valgrind module itself is a front-end to this API. If they aren't
available yet, it will first generate suppressions for the current perl
interpreter and store them in the portable flavor of
~/.perl/Test-Valgrind/suppressions/$VERSION. The actual run will then take
place, and tests will be passed or failed according to the result of the
analysis.

The complete API is much more versatile than this. By declaring an appropriate
Test::Valgrind::Command class, you can run any executable (that is, not only
Perl scripts) under valgrind, generate the corresponding suppressions
on-the-fly and convert the analysis result to TAP output so that it can be
incorporated into your project's test suite. If you're not interested in
producing TAP, you can output the results in whatever format you like (for
example HTML pages) by defining your own Test::Valgrind::Action class.

%prep
%setup -q -n Test-Valgrind-%{version}

# Without debuginfo, the symbol 'Perl_pp_entersub' is not always
# appearing in the valgrind trace report, causing t/20-bad.t to fail
# as a result of not recognizing the trace record
#
# This is a workaround to help the test identify the trace correctly
%patch -P 1

# Avoid doc-file deps and fix shellbangs
sed -i -e 's|^#!/usr/bin/env perl|#!/usr/bin/perl|' samples/map.pl
chmod -c -x samples/map.pl

%if %{with debug_valgrind}
# Create a wrapper script for valgrind so we can see how it's being used
mkdir bin
cat << 'EOF' > bin/valgrind
#!/bin/bash

echo "### valgrind " "$@" >> valgrind.output
/usr/bin/valgrind "$@" | tee -a valgrind.output
EOF
chmod 755 bin/valgrind
%endif

%build
perl Makefile.PL INSTALLDIRS=vendor OPTIMIZE="%{optflags}"
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name '*.bs' -empty -delete
%{_fixperms} -c %{buildroot}

# The package is noarch; the XS code included is for testing purposes and is
# not part of the module itself
if [ "%{perl_vendorarch}" != "%{perl_vendorlib}" ]; then
	mkdir -p %{buildroot}%{perl_vendorlib}
	mv %{buildroot}%{perl_vendorarch}/* %{buildroot}%{perl_vendorlib}/
fi

%check
%if %{with debug_valgrind}
# Pick up our local valgrind script
PATH=$(pwd)/bin:$PATH
%endif
make test

%files
%doc Changes README samples/
%{perl_vendorlib}/Test/
%{_mandir}/man3/Test::Valgrind.3*
%{_mandir}/man3/Test::Valgrind::Action.3*
%{_mandir}/man3/Test::Valgrind::Action::Captor.3*
%{_mandir}/man3/Test::Valgrind::Action::Suppressions.3*
%{_mandir}/man3/Test::Valgrind::Action::Test.3*
%{_mandir}/man3/Test::Valgrind::Carp.3*
%{_mandir}/man3/Test::Valgrind::Command.3*
%{_mandir}/man3/Test::Valgrind::Command::Aggregate.3*
%{_mandir}/man3/Test::Valgrind::Command::Perl.3*
%{_mandir}/man3/Test::Valgrind::Command::PerlScript.3*
%{_mandir}/man3/Test::Valgrind::Component.3*
%{_mandir}/man3/Test::Valgrind::Parser.3*
%{_mandir}/man3/Test::Valgrind::Parser::Suppressions::Text.3*
%{_mandir}/man3/Test::Valgrind::Parser::Text.3*
%{_mandir}/man3/Test::Valgrind::Parser::XML.3*
%{_mandir}/man3/Test::Valgrind::Parser::XML::Twig.3*
%{_mandir}/man3/Test::Valgrind::Report.3*
%{_mandir}/man3/Test::Valgrind::Session.3*
%{_mandir}/man3/Test::Valgrind::Suppressions.3*
%{_mandir}/man3/Test::Valgrind::Tool.3*
%{_mandir}/man3/Test::Valgrind::Tool::memcheck.3*
%{_mandir}/man3/Test::Valgrind::Util.3*
%{_mandir}/man3/Test::Valgrind::Version.3*

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.19-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.19-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.19-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.19-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.19-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jul 30 2023 Paul Howarth <paul@city-fan.org> - 1.19-23
- Fix FTBFS in Fedora 39 due to failing t/20-bad.t (rhbz#2222854)

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.19-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.19-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.19-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jun 01 2022 Jitka Plesnikova <jplesnik@redhat.com> - 1.19-20
- Perl 5.36 rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.19-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.19-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sun May 23 2021 Jitka Plesnikova <jplesnik@redhat.com> - 1.19-17
- Perl 5.34 rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.19-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.19-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 1.19-14
- Perl 5.32 rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.19-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sun Sep 22 2019 Paul Howarth <paul@city-fan.org> - 1.19-12
- Use author-independent source URL

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.19-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.19-10
- Perl 5.30 rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.19-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.19-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sat Jun 30 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.19-7
- Perl 5.28 rebuild

* Tue Feb 13 2018 Paul Howarth <paul@city-fan.org> - 1.19-6
- Add build option --with debug_valgrind
- Fix shellbang in samples/map.pl
- Drop EL-5 support
  - Drop legacy BuildRoot: and Group: tags
  - Drop explicit buildroot cleaning in %%install section
  - Drop explicit %%clean section
  - Drop support for building with File::Temp < 0.19 and
    ExtUtils::Install < 1.3702

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.19-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.19-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jun 05 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.19-3
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.19-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Aug  2 2016 Paul Howarth <paul@city-fan.org> - 1.19-1
- Update to 1.19
  - valgrind 3.1x will no longer be treated as valgrind 3.1.0, causing the
    wrong command line arguments to be used (Debian bug 832833)
  - The number of callers is now capped at 24, as this is the maximum number
    supported by valgrind; a higher number of frames could lead to the
    generation of unusable suppressions in both old and recent versions of
    valgrind
- BR: perl-generators
- Simplify find commands using -empty and -delete

* Mon May 16 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.18-3
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.18-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Nov 16 2015 Paul Howarth <paul@city-fan.org> - 1.18-1
- Update to 1.18
  - A new Test::Valgrind::Version class has been added to represent valgrind
    version numbers, instead of lazily relying on version.pm
  - The detection of the valgrind executable has been slightly improved to
    cover some edge cases
  - Test failures on Windows, or with old versions of Test::More or File::Temp,
    have been addressed
  - A few extraneous warnings displayed by some tests when they were run with
    old versions of Test::Harness were silenced
- Drop bumped version requirements from previous build, no longer needed

* Sun Nov 15 2015 Paul Howarth <paul@city-fan.org> - 1.17-1
- Update to 1.17
  - The Test::Valgrind tests will now be skipped when the default and
    user-supplied suppressions files do not refer to any perl-related symbol;
    this behaviour can be overridden by passing 'allow_no_supp => 1' to
    Test::Valgrind->import
  - Fix CPAN RT#101934: t/20-bad.t failing on armv7hl; while the root cause of
    this issue is probably not at Test::Valgrind's level, it should
    nevertheless not run the tests when the suppression files are obviously
    insufficient
  - The accuracy of the default perl suppression file has been improved
  - The tests will be more reliably skipped when no valgrind or no suppressions
    are found
  - Segmentation faults during the analysis are now more gracefully handled
  - 'no_def_supp => 1' will no longer cause the extra suppressions to be
    ignored
  - t/20-bad.t will no longer run the extra tests when no valgrind can be found
    (this was a regression in version 1.15)
- Bump version requirements for File::Temp/Test::Builder usage in test suite
- Drop redundant %%{?perl_default_filter}

* Sat Oct 31 2015 Paul Howarth <paul@city-fan.org> - 1.15-1
- Update to 1.15
  - The new 'regen_def_supp' option can be passed to Test::Valgrind->import to
    forcefully regenerate the default suppression file
  - Fix build failures of the dummy XS code with PERL_IMPLICIT_SYS perls
  - Fix handshake failures in tests with recent perls built with PERL_POISON
  - Test: Improved diagnostics on failure
  - Freshen Makefile.PL

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.14-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.14-5
- Perl 5.22 rebuild

* Wed Feb  4 2015 Paul Howarth <paul@city-fan.org> - 1.14-4
- Classify buildreqs by usage

* Fri Aug 29 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.14-3
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Sep  1 2013 Paul Howarth <paul@city-fan.org> - 1.14-1
- Update to 1.14
  - This is a maintenance release; the code contains no functional change
  - POD headings are now properly linkable
  - Author tests are no longer bundled with this distribution
  - The stack traces used in t/20-bad.t have been made more predictable when
    compiler optimizations are in use
- Drop buildreqs only needed for author tests

* Wed Aug 14 2013 Jitka Plesnikova <jplesnik@redhat.com> - 1.13-10
- Perl 5.18 re-rebuild of bootstrapped packages

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.13-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jul 25 2013 Petr Pisar <ppisar@redhat.com> - 1.13-8
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.13-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.13-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 10 2012 Petr Pisar <ppisar@redhat.com> - 1.13-5
- Perl 5.16 re-rebuild of bootstrapped packages

* Mon Jun 18 2012 Petr Pisar <ppisar@redhat.com> - 1.13-4
- Perl 5.16 rebuild

* Thu May  3 2012 Paul Howarth <paul@city-fan.org> - 1.13-3
- Incorporate suggestions from package review (#803057)
  - BR: perl(Pod::Coverage) ≥ 0.18
  - BR: perl(XSLoader)
  - BR: at least version 1.22 of perl(Test::Pod)
  - BR: at least version 1.08 of perl(Test::Pod::Coverage)

* Tue Mar 13 2012 Paul Howarth <paul@city-fan.org> - 1.13-2
- Sanitize for Fedora submission
  - Use Fedora-style dist tag
  - Drop %%defattr, redundant since rpm 4.4

* Mon Mar 12 2012 Paul Howarth <paul@city-fan.org> - 1.13-1
- Initial RPM version
