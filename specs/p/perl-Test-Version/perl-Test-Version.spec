# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:		perl-Test-Version
Version:	2.09
Release: 28%{?dist}
Summary:	Check to see that versions in modules are sane
License:	Artistic-2.0
URL:		https://metacpan.org/release/Test-Version
Source0:	https://cpan.metacpan.org/modules/by-module/Test/Test-Version-%{version}.tar.gz
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
BuildRequires:	perl(Carp)
BuildRequires:	perl(Exporter)
BuildRequires:	perl(File::Find::Rule::Perl)
BuildRequires:	perl(Module::Metadata) >= 1.000020
BuildRequires:	perl(parent)
BuildRequires:	perl(strict)
BuildRequires:	perl(Test::Builder)
BuildRequires:	perl(Test::More) >= 0.96
BuildRequires:	perl(version) >= 0.86
BuildRequires:	perl(warnings)
# ===================================================================
# Regular test suite requirements
# ===================================================================
BuildRequires:	perl(blib) >= 1.01
BuildRequires:	perl(CPAN::Meta) >= 2.120900
BuildRequires:	perl(Cwd)
BuildRequires:	perl(File::Find)
BuildRequires:	perl(File::Spec)
BuildRequires:	perl(File::Temp)
BuildRequires:	perl(IO::Handle)
BuildRequires:	perl(IPC::Open3)
BuildRequires:	perl(Test::Exception)
BuildRequires:	perl(Test::Tester)
# ===================================================================
# Author/Release test requirements
#
# Don't run these tests or include their requirements if we're
# bootstrapping, as many of these modules require each other for
# their author/release tests.
# ===================================================================
%if 0%{!?perl_bootstrap:1}
BuildRequires:	perl(Pod::Coverage::TrustPod)
BuildRequires:	perl(Test::CPAN::Changes) >= 0.19
BuildRequires:	perl(Test::CPAN::Meta::JSON)
BuildRequires:	perl(Test::EOL)
BuildRequires:	perl(Test::MinimumVersion)
BuildRequires:	perl(Test::Perl::Critic)
BuildRequires:	perl(Test::Pod) >= 1.41
BuildRequires:	perl(Test::Pod::Coverage) >= 1.08
BuildRequires:	perl(Test::Portability::Files)
%endif
# ===================================================================
# Runtime dependencies
# ===================================================================
Requires:	perl(Test::More) >= 0.96

%description
This module's goal is to be a one stop shop for checking to see that your
versions across your dist are sane.

%prep
%setup -q -n Test-Version-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
%{_fixperms} -c %{buildroot}

%check
make test
%if 0%{!?perl_bootstrap:1}
make test TEST_FILES="$(echo $(find xt/ -name '*.t'))"
%endif

%files
%license LICENSE
%doc Changes CONTRIBUTING README
%{perl_vendorlib}/Test/
%{_mandir}/man3/Test::Version.3*

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.09-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.09-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.09-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.09-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.09-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.09-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.09-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.09-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jun 03 2022 Jitka Plesnikova <jplesnik@redhat.com> - 2.09-19
- Perl 5.36 re-rebuild of bootstrapped packages

* Tue May 31 2022 Jitka Plesnikova <jplesnik@redhat.com> - 2.09-18
- Perl 5.36 rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.09-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.09-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon May 24 2021 Jitka Plesnikova <jplesnik@redhat.com> - 2.09-15
- Perl 5.34 re-rebuild of bootstrapped packages

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 2.09-14
- Perl 5.34 rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.09-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.09-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jun 26 2020 Jitka Plesnikova <jplesnik@redhat.com> - 2.09-11
- Perl 5.32 re-rebuild of bootstrapped packages

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 2.09-10
- Perl 5.32 rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.09-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.09-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Jun 02 2019 Jitka Plesnikova <jplesnik@redhat.com> - 2.09-7
- Perl 5.30 re-rebuild of bootstrapped packages

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 2.09-6
- Perl 5.30 rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.09-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.09-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sat Jun 30 2018 Jitka Plesnikova <jplesnik@redhat.com> - 2.09-3
- Perl 5.28 re-rebuild of bootstrapped packages

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 2.09-2
- Perl 5.28 rebuild

* Thu Apr 26 2018 Paul Howarth <paul@city-fan.org> - 2.09-1
- Update to 2.09
  - Handle common special characters on Windows in taint mode

* Wed Feb 21 2018 Paul Howarth <paul@city-fan.org> - 2.07-1
- Update to 2.07
  - Support running in taint mode

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.05-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.05-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jun 07 2017 Jitka Plesnikova <jplesnik@redhat.com> - 2.05-4
- Perl 5.26 re-rebuild of bootstrapped packages

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 2.05-3
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.05-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun Sep 18 2016 Paul Howarth <paul@city-fan.org> - 2.05-1
- Update to 2.05
  - Bump requirement for newer version of Module::Metadata (again); required
    for ignore_unindexable

* Thu Jun 23 2016 Paul Howarth <paul@city-fan.org> - 2.04-1
- Update to 2.04
  - Bump requirement for a newer version of Module::Metadata
    (the version that comes with Perl 5.14 cannot handle package block syntax)
- BR: perl-generators
- Simplify find command using -delete

* Wed May 18 2016 Jitka Plesnikova <jplesnik@redhat.com> - 2.03-4
- Perl 5.24 re-rebuild of bootstrapped packages

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 2.03-3
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.03-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Jun 29 2015 Paul Howarth <paul@city-fan.org> - 2.03-1
- Update to 2.03
  - Added 'multiple' option to check each version inside a .pm file with
    multiple packages
  - Remove annoying warnings when version_ok called by itself (GH#5)

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.01-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 10 2015 Jitka Plesnikova <jplesnik@redhat.com> - 2.01-3
- Perl 5.22 re-rebuild of bootstrapped packages
- Disable using of Test::Vars with Perl 5.22

* Thu Jun 04 2015 Jitka Plesnikova <jplesnik@redhat.com> - 2.01-2
- Perl 5.22 rebuild

* Tue May 19 2015 Paul Howarth <paul@city-fan.org> - 2.01-1
- Update to 2.01
  - Fix failing test in t/all-generated.t

* Thu May  7 2015 Paul Howarth <paul@city-fan.org> - 2.00-1
- Update to 2.00
  - Added filename_match setting

* Wed May  6 2015 Paul Howarth <paul@city-fan.org> - 1.050000-1
- Update to 1.05
  - New maintainer (PLICEASE) updated meta
- Retained six-digit version number for rpm to maintain upgrade path, until
  upstream reaches version 2 anyway

* Tue Oct 21 2014 Paul Howarth <paul@city-fan.org> - 1.004001-1
- Update to 1.004001
  - Improved consistent check diagnostics (GH#11)

* Mon Oct 20 2014 Paul Howarth <paul@city-fan.org> - 1.004000-1
- Update to 1.004000
  - Add consistent check (GH#10)

* Wed Sep 24 2014 Paul Howarth <paul@city-fan.org> - 1.003001-1
- Update to 1.003001
  - Skip packages unindexable by pause (GH#4)
  - Remove inline and remove _get_version; trying to skip test there won't work
    (GH#4)

* Sun Sep 07 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.002004-6
- Perl 5.20 re-rebuild of bootstrapped packages

* Thu Aug 28 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.002004-5
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.002004-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Jan 27 2014 Paul Howarth <paul@city-fan.org> - 1.002004-3
- Bootstrap build for epel7 done

* Mon Jan 27 2014 Paul Howarth <paul@city-fan.org> - 1.002004-2
- Bootstrap epel7 build

* Thu Nov 21 2013 Paul Howarth <paul@city-fan.org> - 1.002004-1
- Update to 1.002004
  - Fix bugs in argument handling
  - Fix whitespace

* Tue Oct 15 2013 Paul Howarth <paul@city-fan.org> - 1.002003-1
- Update to 1.002003
  - Fix synopsis (https://github.com/xenoterracide/Test-Version/pull/6)
  - Change Dist::Zilla plugins
  - Remove old documentation that no longer applies
  - Fix misgithap
  - More dist.ini updates
- Update patches and buildreqs as needed
- Drop support for old rpm versions as this package's requirements will never
  be satisfied in EPEL-5

* Wed Aug 14 2013 Jitka Plesnikova <jplesnik@redhat.com> - 1.002001-13
- Perl 5.18 re-rebuild of bootstrapped packages

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.002001-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul 22 2013 Petr Pisar <ppisar@redhat.com> - 1.002001-11
- Perl 5.18 rebuild

* Fri Jun 14 2013 Paul Howarth <paul@city-fan.org> - 1.002001-10
- Fix FTBFS with current test modules
  - Disable Test::Kwalitee's "use_strict" test
  - Schwern not in dictionary

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.002001-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.002001-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 10 2012 Petr Pisar <ppisar@redhat.com> - 1.002001-7
- Perl 5.16 re-rebuild of bootstrapped packages

* Wed Jun 13 2012 Petr Pisar <ppisar@redhat.com> - 1.002001-6
- Perl 5.16 rebuild

* Thu Jun  7 2012 Paul Howarth <paul@city-fan.org> - 1.002001-5
- If we don't have buildreqs aspell-en and perl(Pod::Wordlist::hanekomu), we
  don't need perl(Test::Spelling) either

* Thu Jun  7 2012 Marcela Mašláňová <mmaslano@redhat.com> - 1.002001-4
- Conditionalize aspell-en dependency

* Tue Apr 24 2012 Paul Howarth <paul@city-fan.org> - 1.002001-3
- Don't BR: perl(Pod::Wordlist::hanekomu) for RHEL-7+ either (#815759)

* Tue Apr 24 2012 Paul Howarth <paul@city-fan.org> - 1.002001-2
- RHEL-7+ package cannot BR: perl(Test::Kwalitee) from EPEL (#815759)

* Wed Mar 14 2012 Paul Howarth <paul@city-fan.org> - 1.002001-1
- Update to 1.002001:
  - Fix metadata caused by a bug in DZP::GitHub after asking repo to be
    unlinked from gitpan
- Don't need to remove empty directories from buildroot
- Use %%{_fixperms} macro rather than our own chmod incantation
- Use DESTDIR rather than PERL_INSTALL_ROOT
- Drop %%defattr, redundant since rpm 4.4
- Don't attempt to run author/release tests when bootstrapping

* Tue Jan 10 2012 Paul Howarth <paul@city-fan.org> - 1.002000-1
- Update to 1.002000:
  - Use Module::Metadata - apparently it's closer to how Perl works than
    Module::Extract::VERSION
  - Use perl decimal style semantic versioning because of bugs in EUMM with
    vstring versions
  - Allow disabling of 'has_version'
  - Require at least 1 version
  - Allow for checking that a module is_strict
  - Fix some issues in the pod
- BR: perl(Module::Metadata) rather than perl(Module::Extract::VERSION)
- BR: perl(Test::Exception) and perl(Test::Requires) for test suite
- BR: perl(strict) and perl(warnings) for completeness

* Thu Aug 11 2011 Paul Howarth <paul@city-fan.org> - 1.0.0-3
- Don't run the author/release tests when bootstrapping
- BR: perl(Test::DistManifest) unconditionally
- Additional BR's for improved release test coverage:
  - perl(Pod::Wordlist::hanekomu)
  - perl(Test::CPAN::Meta::JSON)
  - perl(Test::Mojibake)
  - perl(Test::Spelling) ≥ 0.12 and aspell-en
  - perl(Test::Vars)

* Thu Aug  4 2011 Paul Howarth <paul@city-fan.org> - 1.0.0-2
- Sanitize for Fedora submission

* Wed Aug  3 2011 Paul Howarth <paul@city-fan.org> - 1.0.0-1
- Initial RPM version
