# Run extra test
%if 0%{?perl_bootstrap:1} || ( 0%{?rhel} )
%bcond_with perl_B_Hooks_EndOfScope_enables_extra_test
%else
%bcond_without perl_B_Hooks_EndOfScope_enables_extra_test
%endif
# Run optional test
%bcond_without perl_B_Hooks_EndOfScope_enables_optional_test

Name:		perl-B-Hooks-EndOfScope
Version:	0.24
Release:	10%{?dist}
License:	GPL+ or Artistic
Vendor:         Microsoft Corporation
Distribution:   Mariner
Summary:	Execute code after scope compilation finishes
URL:		https://metacpan.org/release/B-Hooks-EndOfScope
Source0:	https://cpan.metacpan.org/authors/id/E/ET/ETHER/B-Hooks-EndOfScope-%{version}.tar.gz#/perl-B-Hooks-EndOfScope-%{version}.tar.gz
Patch0:		B-Hooks-EndOfScope-0.13-shellbangs.patch
BuildArch:	noarch
# Build
BuildRequires:	coreutils
BuildRequires:	findutils
BuildRequires:	make
BuildRequires:	perl-generators
BuildRequires:	perl-interpreter
BuildRequires:	perl(ExtUtils::MakeMaker)
BuildRequires:	perl(lib)
BuildRequires:	perl(Text::ParseWords)
# Dependencies of bundled ExtUtils::HasCompiler
BuildRequires:	perl(base)
BuildRequires:	perl(Config)
BuildRequires:	perl(DynaLoader)
BuildRequires:	perl(Exporter)
BuildRequires:	perl(File::Basename)
BuildRequires:	perl(File::Spec::Functions)
BuildRequires:	perl(File::Temp)
# Common Module Requirements
BuildRequires:	perl(Module::Implementation) >= 0.05
BuildRequires:	perl(Sub::Exporter::Progressive) >= 0.001006
BuildRequires:	perl(strict)
BuildRequires:	perl(warnings)
# PP Implementation Only
BuildRequires:	perl(Carp)
BuildRequires:	perl(constant)
BuildRequires:	perl(Hash::Util::FieldHash)
BuildRequires:	perl(Scalar::Util)
BuildRequires:	perl(Tie::Hash)
BuildRequires:	perl(Tie::StdHash)
# XS Implementation Only
BuildRequires:	perl(Variable::Magic) >= 0.48
# Test suite
BuildRequires:	perl(Config)
BuildRequires:	perl(Devel::Hide) >= 0.0007
BuildRequires:	perl(File::Glob)
BuildRequires:	perl(File::Spec)
BuildRequires:	perl(IPC::Open2)
BuildRequires:	perl(Test::More) >= 0.88
# Optional Tests
%if %{with perl_B_Hooks_EndOfScope_enables_optional_test}
BuildRequires:	perl(CPAN::Meta) >= 2.120900
BuildRequires:	perl(CPAN::Meta::Prereqs)
%endif
# Author/Release tests
# Note:
# * Test::Pod::No404s intentionally omitted as it would fail due to
#   missing connectivity in the koji build environment
# * ExtUtils::HasCompiler is bundled, so we don't need to BuildRequire it
%if %{with perl_B_Hooks_EndOfScope_enables_extra_test}
BuildRequires:	perl(blib)
BuildRequires:	perl(Encode)
BuildRequires:	perl(IO::Handle)
BuildRequires:	perl(IPC::Open3)
BuildRequires:	perl(Path::Tiny) >= 0.062
BuildRequires:	perl(Pod::Coverage::TrustPod)
BuildRequires:	perl(Pod::Wordlist)
BuildRequires:	perl(Test::CPAN::Changes)
BuildRequires:	perl(Test::CPAN::Meta)
BuildRequires:	perl(Test::Deep)
BuildRequires:	perl(Test::EOL)
BuildRequires:	perl(Test::Kwalitee) >= 1.21
BuildRequires:	perl(Test::MinimumVersion)
BuildRequires:	perl(Test::Mojibake)
BuildRequires:	perl(Test::More) >= 0.96
BuildRequires:	perl(Test::NoTabs)
BuildRequires:	perl(Test::Pod) >= 1.41
BuildRequires:	perl(Test::Pod::Coverage) >= 1.08
BuildRequires:	perl(Test::Portability::Files)
BuildRequires:	perl(Test::Spelling), hunspell-en
%endif
# Runtime
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

%description
This module allows you to execute code when Perl has finished compiling the
surrounding scope.

%prep
%setup -q -n B-Hooks-EndOfScope-%{version}

# Remove shellbangs from tests to placate rpmlint
%patch0

# British-English spelling LICENCE upsets US spell checker
echo LICENCE >> xt/author/pod-spell.t

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
%{_fixperms} -c %{buildroot}

%check
%if %{with perl_B_Hooks_EndOfScope_enables_extra_test}
export AUTHOR_TESTING=1
%endif
make test
%if %{with perl_B_Hooks_EndOfScope_enables_extra_test}
make test TEST_FILES="$(echo $(find xt/ -name '*.t'))"
%endif

%files
%license LICENCE
%doc Changes CONTRIBUTING README t/
%{perl_vendorlib}/B/
%{_mandir}/man3/B::Hooks::EndOfScope.3*
%{_mandir}/man3/B::Hooks::EndOfScope::PP.3*
%{_mandir}/man3/B::Hooks::EndOfScope::XS.3*

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.24-10
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.24-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.24-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Jun 02 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.24-7
- Perl 5.30 re-rebuild of bootstrapped packages

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.24-6
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.24-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.24-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sun Jul 01 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.24-3
- Perl 5.28 re-rebuild of bootstrapped packages

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.24-2
- Perl 5.28 rebuild

* Tue Apr 24 2018 Paul Howarth <paul@city-fan.org> - 0.24-1
- Update to 0.24
  - Fix memory corruption on perls 5.8.0 - 5.8.3
  - Improve use of constants in compile-time perl version checks
- BR: perl-generators unconditionally
- Drop legacy Group: tag

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.21-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.21-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jun 07 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.21-4
- Perl 5.26 re-rebuild of bootstrapped packages

* Mon Jun 05 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.21-3
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.21-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu May 26 2016 Paul Howarth <paul@city-fan.org> - 0.21-1
- Update to 0.21
  - Work with Object::Remote by removing require() call on Tie::StdHash in PP

* Wed May 18 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.20-3
- Perl 5.24 re-rebuild of bootstrapped packages

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.20-2
- Perl 5.24 rebuild

* Sat May  7 2016 Paul Howarth <paul@city-fan.org> - 0.20-1
- Update to 0.20
  - Remove unnecessary and erroneous extra crud in inc/

* Tue May  3 2016 Paul Howarth <paul@city-fan.org> - 0.19-1
- Update to 0.19
  - More Makefile.PL updates
  - Makefile.PL now checks for a working compiler using ExtUtils::HasCompiler
    (inlined into the build) rather than ExtUtils::CBuilder (CPAN RT#113685)
- Simplify find command using -delete
- Fix EPEL conditional - only currently buildable for EPEL 7 onwards
- Drop BR: for Test::Pod::No404s, which breaks koji builds

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.15-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.15-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 10 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.15-3
- Perl 5.22 re-rebuild of bootstrapped packages

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.15-2
- Perl 5.22 rebuild

* Fri May 15 2015 Paul Howarth <paul@city-fan.org> - 0.15-1
- Update to 0.15
  - Updated the tooling for generating Makefile.PL
  - Removed Tie::StdHash from prereqs, which is not require()able as a module
    on its own, despite being indexed (GH #3)
  - Fixed the addition in release 0.14 of Hash::Util::FieldHash as a
    prerequisite (which is not available prior to perl 5.010) for pure-perl
    installations (CPAN RT#104435)

* Sun Feb  1 2015 Paul Howarth <paul@city-fan.org> - 0.14-1
- Update to 0.14
  - Line numbers in shipped code are now the same as the repository source, for
    easier debugging
  - More accurate dynamic prereq declarations
- Use %%license

* Sun Sep 07 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.13-5
- Perl 5.20 re-rebuild of bootstrapped packages

* Fri Aug 29 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.13-4
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Jan 15 2014 Paul Howarth <paul@city-fan.org> - 0.13-2
- Bootstrap EPEL-7 build

* Wed Jan  8 2014 Paul Howarth <paul@city-fan.org> - 0.13-1
- Update to 0.13
  - Variable::Magic added as a runtime recommendation for greater visibility
    (CPAN RT#89245)
  - Fixed broken logic in compiler detection on older perls
  - Fixed inaccurate repository metadata
- This release by ETHER -> update source URL
- Drop Pod Coverage patch, no longer needed
- Update shellbang patch
- Don't run the release tests when bootstrapping

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 24 2013 Petr Pisar <ppisar@redhat.com> - 0.12-3
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Dec  5 2012 Paul Howarth <paul@city-fan.org> - 0.12-1
- Update to 0.12
  - Complete pure-perl implementation in addition to the one based on
    Variable::Magic; you can specify the implementation explicitly by use-ing
    B::Hooks::EndOfScope::PP or B::Hooks::EndOfScope::XS, or by setting
    $ENV{B_HOOKS_ENDOFSCOPE_IMPLEMENTATION} to either 'XS' or 'PP'
  - Switch from using Sub::Exporter to the more conservative
    Sub::Exporter::Progressive
- Add patch to fix POD coverage issues in new pure-perl implementation
- This release by BOBTFISH -> update source URL
- BR: perl(ExtUtils::CBuilder) ≥ 0.26, perl(Devel::Hide) ≥ 0.0007,
  perl(Module::Implementation) ≥ 0.05 and perl(Module::Runtime) ≥ 0.012
- BR: perl(Sub::Exporter::Progressive) rather than perl(Sub::Exporter)
- BR: perl(base), perl(constant), perl(Hash::Util::FieldHash) and
  perl(Scalar::Util) for the pure-perl implementation

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 15 2012 Petr Pisar <ppisar@redhat.com> - 0.11-2
- Perl 5.16 rebuild

* Thu Feb 23 2012 Paul Howarth <paul@city-fan.org> - 0.11-1
- Update to 0.11 (a minor efficiency improvement)
- Bump perl(Variable::Magic) version requirement to 0.48

* Thu Feb 16 2012 Paul Howarth <paul@city-fan.org> - 0.10-1
- Update to 0.10 (stop propagating our magic through localisation)
- Package LICENSE file
- Downgrade ExtUtils::MakeMaker version requirement to 6.30
- Upgrade Test::More version requirement to 0.89
- Drop Test::Pod version requirement for EPEL-6 spec compatibility
- BR: perl(Test::EOL) and perl(Test::NoTabs) for additional test coverage
- Clean up for modern rpmbuild since we have no branches prior to EPEL-6
  - Don't specify BuildRoot:
  - Skip cleaning of buildroot in %%install
  - Remove %%clean section
  - Drop redundant %%defattr
- Remove shellbangs from tests to placate rpmlint

* Tue Jan 17 2012 Paul Howarth <paul@city-fan.org> - 0.09-1
- Update to 0.09 (improve distribution metadata)
- Run release tests too
- BR: perl(Pod::Coverage::TrustPod), perl(Test::Pod) and
  perl(Test::Pod::Coverage) for release tests
- Spec clean-up:
  - Make %%files list more explicit
  - Use DESTDIR rather than PERL_INSTALL_ROOT
  - Use tabs
  - Split buildreqs by Build/Module/Tests/Release tests

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.08-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 0.08-7
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.08-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 15 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.08-5
- Rebuild to fix problems with vendorarch/lib (#661697)

* Thu Apr 29 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.08-4
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.08-3
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.08-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun May 17 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.08-1
- auto-update to 0.08 (by cpan-spec-update 0.01)
- altered br on perl(ExtUtils::MakeMaker) (0 => 6.42)
- altered br on perl(Variable::Magic) (0.31 => 0.34)

* Sun Mar 08 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.07-1
- update to 0.07

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.04-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Nov 08 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.04-1
- update for submission

* Sat Nov 08 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.04-0.1
- initial RPM packaging
- generated with cpan2dist (CPANPLUS::Dist::RPM version 0.0.5)
