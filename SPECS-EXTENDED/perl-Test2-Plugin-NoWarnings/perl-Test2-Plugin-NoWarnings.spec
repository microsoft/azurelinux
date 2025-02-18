Name:		perl-Test2-Plugin-NoWarnings
Version:	0.10
Release:	2%{?dist}
Summary:	Fail if tests warn
License:	Artistic-2.0
URL:		https://metacpan.org/release/Test2-Plugin-NoWarnings
Source0:	https://cpan.metacpan.org/authors/id/D/DR/DROLSKY/Test2-Plugin-NoWarnings-%{version}.tar.gz
BuildArch:	noarch
# Build
BuildRequires:	coreutils
BuildRequires:	make
BuildRequires:	perl-generators
BuildRequires:	perl-interpreter
BuildRequires:	perl(ExtUtils::MakeMaker) > 6.75
# Module Runtime
BuildRequires:	perl(Carp)
BuildRequires:	perl(parent)
BuildRequires:	perl(strict)
BuildRequires:	perl(Test2) >= 1.302167
BuildRequires:	perl(Test2::API)
BuildRequires:	perl(Test2::Event)
BuildRequires:	perl(Test2::Util::HashBase)
BuildRequires:	perl(warnings)
# Test Suite
BuildRequires:	perl(File::Spec)
BuildRequires:	perl(IPC::Run3)
BuildRequires:	perl(Module::Pluggable)
BuildRequires:	perl(Test2::Require::Module)
BuildRequires:	perl(Test2::V0)
BuildRequires:	perl(Test::More) >= 0.96
# Optional Tests
BuildRequires:	perl(CPAN::Meta) >= 2.120900
BuildRequires:	perl(CPAN::Meta::Prereqs)
# Dependencies
# (none)

%description
Loading this plugin causes your tests to fail if there are any warnings while
they run. Each warning generates a new failing test and the warning content is
outputted via diag.

This module uses $SIG{__WARN__}, so if the code you're testing sets this, then
this module will stop working.

%prep
%setup -q -n Test2-Plugin-NoWarnings-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PERLLOCAL=1 NO_PACKLIST=1
%{make_build}

%install
%{make_install}
%{_fixperms} -c %{buildroot}

%check
make test

%files
%license LICENSE
%doc Changes CODE_OF_CONDUCT.md README.md
%{perl_vendorlib}/Test2/
%{_mandir}/man3/Test2::Event::Warning.3*
%{_mandir}/man3/Test2::Plugin::NoWarnings.3*

%changelog
* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sun Apr  7 2024 Paul Howarth <paul@city-fan.org> - 0.10-1
- Update to 0.10
  - Previously, when tests were run via prove without the verbose flag and
    there was a warning that caused a test failure, there was no output
    indicating that a warning caused the failure; this has now been corrected
    and you'll see output that includes "Unexpected warning"

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.09-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.09-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.09-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.09-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.09-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jun 01 2022 Jitka Plesnikova <jplesnik@redhat.com> - 0.09-7
- Perl 5.36 rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.09-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.09-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 0.09-4
- Perl 5.34 rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.09-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.09-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 30 2020 Paul Howarth <paul@city-fan.org> - 0.09-1
- Update to 0.09
  - Don't emit a failing test if there is a warning _after_ done_testing() is
    called (based on GH#3)

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 0.08-3
- Perl 5.32 rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.08-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Oct 11 2019 Paul Howarth <paul@city-fan.org> - 0.08-1
- Update to 0.08
  - Use IPC::Run3 instead of Capture::Tiny for all tests, which fixes an issue
    with the 'tap-bug-in-test2.t' on Windows (CPAN RT#129294)

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.07-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.07-2
- Perl 5.30 rebuild

* Mon Apr 22 2019 Paul Howarth <paul@city-fan.org> - 0.07-1
- Update to 0.07
  - Reverted back to using the Warning event type, since the bug in the Test2
    core that caused this to be a problem has since been fixed
  - Replaced use of Test2::Bundle::Extended with Test2::V0
- Package new document CODE_OF_CONDUCT.md
- Modernize spec using %%{make_build} and %%{make_install}

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.06-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.06-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.06-4
- Perl 5.28 rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.06-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.06-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jun 19 2017 Paul Howarth <paul@city-fan.org> - 0.06-1
- Update to 0.06
  - Warnings inside a subtest were not emitted as TAP events, breaking the TAP
    and making for great confusion: this is because of a bug in the core TAP
    formatter (https://github.com/Test-More/test-more/issues/776); warnings
    are now emitted as Ok events instead of Warning events

* Mon Jun 05 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.05-3
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.05-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Nov  8 2016 Paul Howarth <paul@city-fan.org> - 0.05-1
- Update to 0.05
  - Skip compile.t on Windows; this test uses IPC::Run3, which doesn't seem to
    work well on that platform (CPAN RT#118443)

* Thu Oct 27 2016 Paul Howarth <paul@city-fan.org> - 0.04-2
- We provide Test2::Event::Warning so we don't need to build-require it

* Mon Oct 24 2016 Paul Howarth <paul@city-fan.org> - 0.04-1
- Update to 0.04
  - Load Test2::Event::Warning in the plugin instead of relying on Test2 to do
    it for us; this should avoid the bug fixed in the previous version and
    eliminates the need for the INIT block, which caused its own problems

* Tue Oct 18 2016 Paul Howarth <paul@city-fan.org> - 0.03-1
- Update to 0.03
  - Add the $SIG{__WARN__} hook in an INIT block; we really don't want to
    trigger this because of a compile-time warning, and because of a bug in
    Test::Builder, this can actually cause the warning to be lost entirely
    (https://github.com/Test-More/test-more/issues/729)
  - The Test2::Event::Warning event now returns true for increments_count,
    which means that the test failure caused by a warning will not be output
    as a TAP test line; previously this was just seen as a diag line, which
    could be quite confusing
    (https://github.com/Test-More/test-more/issues/728)

* Mon Sep 19 2016 Paul Howarth <paul@city-fan.org> - 0.02-3
- Drop unused BR: findutils (#1377228)

* Mon Sep 19 2016 Paul Howarth <paul@city-fan.org> - 0.02-2
- Sanitize for Fedora submission

* Sun Sep 18 2016 Paul Howarth <paul@city-fan.org> - 0.02-1
- Initial RPM version
