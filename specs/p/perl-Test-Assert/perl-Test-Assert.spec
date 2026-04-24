# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

 # Run release test
%if ! (0%{?rhel} && 0%{?rhel} < 8)
%bcond_without perl_Test_Assert_enables_release_test
%else
%bcond_with perl_Test_Assert_enables_release_test
%endif

# noarch, but to avoid *.list files interfering with signature test
%global debug_package %{nil}

# Store keys in a temp directory
%global gnupghome %(mktemp --directory)

Name:		perl-Test-Assert
Version:	0.0504
Release: 46%{?dist}
Summary:	Assertion methods for those who like JUnit
License:	GPL-1.0-or-later OR Artistic-1.0-Perl
URL:		https://metacpan.org/release/Test-Assert
Source0:	https://cpan.metacpan.org/modules/by-module/Test/Test-Assert-%{version}.tar.gz
# Upstream signing key, bug #1118362
Source1:	C0B10A5B.pub
Patch0:		Test-Assert-0.0504-Critic.patch
BuildArch:	noarch
# Module Build
BuildRequires:	coreutils
BuildRequires:	findutils
BuildRequires:	gnupg2
BuildRequires:	make
BuildRequires:	perl-generators
BuildRequires:	perl-interpreter
BuildRequires:	perl(Module::Build)
# Module Runtime
BuildRequires:	perl(constant)
BuildRequires:	perl(constant::boolean) >= 0.02
BuildRequires:	perl(Exception::Base) >= 0.21
BuildRequires:	perl(strict)
BuildRequires:	perl(Symbol::Util) >= 0.0202
BuildRequires:	perl(warnings)
# Test Suite
BuildRequires:	perl(Carp)
BuildRequires:	perl(Class::Inspector)
BuildRequires:	perl(Cwd)
BuildRequires:	perl(File::Basename)
BuildRequires:	perl(File::Spec)
BuildRequires:	perl(parent)
BuildRequires:	perl(Test::Builder)
BuildRequires:	perl(Test::More) >= 0.88
BuildRequires:	perl(Test::Unit::Lite) >= 0.11
# Release Tests
%if %{with perl_Test_Assert_enables_release_test}
BuildRequires:	patch
BuildRequires:	perl(File::Find)
BuildRequires:	perl(File::Slurp)
BuildRequires:	perl(Test::CheckChanges)
BuildRequires:	perl(Test::Distribution)
BuildRequires:	perl(Test::Kwalitee)
BuildRequires:	perl(Test::MinimumVersion)
BuildRequires:	perl(Test::Perl::Critic)
BuildRequires:	perl(Test::Pod) >= 1.14
BuildRequires:	perl(Test::Pod::Coverage) >= 1.04
BuildRequires:	perl(Test::Signature)
BuildRequires:	perl(Test::Spelling), hunspell-en
%endif
# Dependencies
# (none)

%description
This class provides a set of assertion methods useful for writing tests.
The API is based on JUnit4 and Test::Unit and the methods die on failure.

%prep
%setup -q -n Test-Assert-%{version}

# Drop exec bits and avoid doc-file dependencies
chmod -c -x eg/*

# Import upstream's GPG key so we don't need to fetch it from a keyserver
# when running the signature test
export GNUPGHOME=%{gnupghome}
gpg2 --import %{SOURCE1}

%build
perl Build.PL --installdirs=vendor
./Build

%install
./Build install --destdir=%{buildroot} --create_packlist=0
%{_fixperms} -c %{buildroot}

%check
# === MAIN TEST SUITE === #

./Build test

# ===  RELEASE TESTS  === #
%if %{with perl_Test_Assert_enables_release_test}

export GNUPGHOME=%{gnupghome}
RELEASE_TESTS="$(echo xt/*.t)"

# Don't run the copyright test as it will fail after the year of module release
RELEASE_TESTS="$(echo $RELEASE_TESTS | sed 's|xt/copyright.t||')"

# Don't run the spelling test yet as we need to add extra stopwords
RELEASE_TESTS="$(echo $RELEASE_TESTS | sed 's|xt/pod_spell.t||')"

# Don't run the perlcritic test yet as we need to patch the code
RELEASE_TESTS="$(echo $RELEASE_TESTS | sed 's|xt/perlcritic.t||')"

# Signature test would fail on recent distros due to presence of MYMETA.*
[ -f MYMETA.yml ] && mv MYMETA.yml ..
[ -f MYMETA.json ] && mv MYMETA.json ..

RELEASE_TESTING=1 ./Build test --test_files "$RELEASE_TESTS"

# Put any MYMETA.* files back where they were
[ -f ../MYMETA.yml ] && mv ../MYMETA.yml .
[ -f ../MYMETA.json ] && mv ../MYMETA.json .

# Patch the code to tidy it and turn off one check before running the perlcritic test
patch -p0 < %{P:0}
./Build test --test_files xt/perlcritic.t
patch -p0 -R < %{P:0}

# Fix the POD Spell test and run it
mv xt/pod_spellrc xt/pod_spellrc.orig
(
	cat xt/pod_spellrc.orig
	echo "'fail'"
	echo "JUnit4"
	echo "value1"
	echo "value2"
) > xt/pod_spellrc
./Build test --test_files xt/pod_spell.t
mv xt/pod_spellrc.orig xt/pod_spellrc

%endif

%clean
rm -rf %{buildroot} %{gnupghome}

%files
%license LICENSE
%doc Changes README eg/
%{perl_vendorlib}/Exception/
%{perl_vendorlib}/Test/
%{_mandir}/man3/Exception::Assertion.3*
%{_mandir}/man3/Test::Assert.3*

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.0504-45
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.0504-44
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.0504-43
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.0504-42
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.0504-41
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.0504-40
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.0504-39
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.0504-38
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jun 01 2022 Jitka Plesnikova <jplesnik@redhat.com> - 0.0504-37
- Perl 5.36 rebuild

* Fri Mar 11 2022 Paul Howarth <paul@city-fan.org> - 0.0504-36
- Use %%license unconditionally

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.0504-35
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.0504-34
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sat May 22 2021 Jitka Plesnikova <jplesnik@redhat.com> - 0.0504-33
- Perl 5.34 rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.0504-32
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Nov 10 2020 Paul Howarth <paul@city-fan.org> - 0.0504-31
- Use author-independent source URL
- Use mktemp to create GNUPGHOME, simplifying build process

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.0504-30
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 0.0504-29
- Perl 5.32 rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.0504-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.0504-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.0504-26
- Perl 5.30 rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.0504-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.0504-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jun 29 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.0504-23
- Perl 5.28 rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.0504-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.0504-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jun 06 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.0504-20
- Perl 5.26 rebuild

* Wed Apr 12 2017 Paul Howarth <paul@city-fan.org> - 0.0504-19
- Fix FTBFS in presence of GPG agent (#1441315)

* Wed Apr  5 2017 Paul Howarth <paul@city-fan.org> - 0.0504-18
- Classify buildreqs by usage
- Use gnupg2 rather than gnupg
- Use %%license where possible
- Turn off exec bits in examples to avoid doc-file dependencies
- Drop legacy Group: tag

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.0504-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon May 16 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.0504-16
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.0504-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0504-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jun 08 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.0504-13
- Perl 5.22 rebuild

* Fri Aug 29 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.0504-12
- Perl 5.20 rebuild

* Thu Jul 10 2014 Paul Howarth <paul@city-fan.org> - 0.0504-11
- Tidy the code to pass the Critic test even if
  Perl::Critic::Policy::ValuesAndExpressions::ProhibitNullStatements is
  installed (part of Perl-Critic-Pulp distribution) (#1118374)

* Thu Jul 10 2014 Petr Pisar <ppisar@redhat.com> - 0.0504-10
- Bundle upstream signing key (bug #1118362)
- Build-conflict with Perl::Critic::Pulp due to release tests (bug #1118374)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0504-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0504-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 31 2013 Petr Pisar <ppisar@redhat.com> - 0.0504-7
- Perl 5.18 rebuild

* Fri Jun 21 2013 Paul Howarth <paul@city-fan.org> - 0.0504-6
- Tweak the perlcritic test, which has discovered something to moan about

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0504-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0504-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jun 23 2012 Petr Pisar <ppisar@redhat.com> - 0.0504-3
- Perl 5.16 rebuild

* Fri Mar  9 2012 Paul Howarth <paul@city-fan.org> - 0.0504-2
- Run the release tests too
  - Extract upstream tarball in a subdir to avoid interference with signature/
    manifest tests
  - BR: perl(File::Slurp)
  - BR: perl(Test::CheckChanges)
  - BR: perl(Test::Distribution)
  - BR: perl(Test::Kwalitee)
  - BR: perl(Test::MinimumVersion)
  - BR: perl(Test::Perl::Critic)
  - BR: perl(Test::Pod)
  - BR: perl(Test::Pod::Coverage)
  - BR: perl(Test::Signature)
  - BR: perl(Test::Spelling), hunspell-en

* Fri Mar  9 2012 Paul Howarth <paul@city-fan.org> - 0.0504-1
- Update to 0.0504:
  - Fixed error message for assert_deep_equals
  - Uses Symbol::Util as exported; all exported symbols can be removed with
    "no Test::Assert" statement
  - Minor refactoring of "assert_deep_equals" method and its private methods
  - Require Symbol::Util ≥ 0.0202 and constant::boolean ≥ 0.02
  - Build requires Class::Inspector
  - The ":assert" tag also imports the "ASSERT" constant
- Spec clean-up:
  - Include LICENSE file
  - Include eg/ directory as %%doc
  - Add %%{?perl_default_filter} to avoid doc-file dependencies from examples
  - BR: Perl core modules that might be dual-lived
  - Don't need to remove empty directories from buildroot
  - Make %%files list more explicit
  - Drop %%defattr, redundant since rpm 4.4
  - Drop buildroot definition and cleaning, redundant since rpm 4.6
  - Don't use macros for commands
  - Drop unnecessary dependency filtering
  - Use tabs

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0501-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Jun 23 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.0501-8
- Perl mass rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0501-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 22 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.0501-6
- Rebuild to fix problems with vendorarch/lib (#661697)

* Thu May 06 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.0501-5
- Mass rebuild with perl-5.12.0

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 0.0501-4
- Rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0501-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0501-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Jan 29 2009 Allisson Azevedo <allisson@gmail.com> - 0.0501-1
- Initial rpm release
