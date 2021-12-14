# Run optional test
%if ! (0%{?rhel})
%bcond_without perl_namespace_clean_enables_optional_test
%else
%bcond_with perl_namespace_clean_enables_optional_test
%endif

Name:		perl-namespace-clean
Summary:	Keep your namespace tidy
Version:	0.27
Release:	14%{?dist}
License:	GPL+ or Artistic
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:		https://metacpan.org/release/namespace-clean
Source0:	https://cpan.metacpan.org/authors/id/R/RI/RIBASUSHI/namespace-clean-%{version}.tar.gz#/perl-namespace-clean-%{version}.tar.gz
BuildArch:	noarch
# Module Build
BuildRequires:	coreutils
BuildRequires:	findutils
BuildRequires:	make
BuildRequires:	perl-generators
BuildRequires:	perl-interpreter >= 4:5.12
BuildRequires:	perl(ExtUtils::MakeMaker)
BuildRequires:	perl(File::Spec)
BuildRequires:	perl(File::Temp)
# Module Runtime
BuildRequires:	perl(B::Hooks::EndOfScope) >= 0.12
BuildRequires:	perl(base)
BuildRequires:	perl(constant)
BuildRequires:	perl(Exporter)
BuildRequires:	perl(Package::Stash) >= 0.23
BuildRequires:	perl(strict)
BuildRequires:	perl(vars)
BuildRequires:	perl(warnings)
# Test Suite
BuildRequires:	perl(Config)
BuildRequires:	perl(DB)
BuildRequires:	perl(File::Glob)
BuildRequires:	perl(FindBin)
BuildRequires:	perl(IPC::Open2)
BuildRequires:	perl(lib)
BuildRequires:	perl(sort)
BuildRequires:	perl(Test::More)
%if %{with perl_namespace_clean_enables_optional_test}
# Optional Tests
BuildRequires:	perl(Variable::Magic)
%endif
# Runtime
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:	perl(B::Hooks::EndOfScope) >= 0.12
Requires:	perl(Package::Stash) >= 0.23

# Avoid unwanted requires/provides that come with the test suite
%{?perl_default_filter}
# namespace::clean::_Util is a private package
%global __requires_exclude %{?__requires_exclude:__requires_exclude|}^perl\\(namespace::clean::_Util\\)

%description
When you define a function, or import one, into a Perl package, it will
naturally also be available as a method. This does not per se cause
problems, but it can complicate subclassing and, for example, plugin
classes that are included via multiple inheritance by loading them as
base classes.

The 'namespace::clean' pragma will remove all previously declared or
imported symbols at the end of the current package's compile cycle.
Functions called in the package itself will still be bound by their
name, but they won't show up as methods on your class or instances.

%prep
%setup -q -n namespace-clean-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
%{_fixperms} -c %{buildroot}

%check
make test

%files
%doc Changes t/
%{perl_vendorlib}/namespace/
%{_mandir}/man3/namespace::clean.3*

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.27-14
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.27-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.27-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.27-11
- Perl 5.30 rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.27-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.27-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jun 29 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.27-8
- Perl 5.28 rebuild

* Fri Feb  9 2018 Paul Howarth <paul@city-fan.org> - 0.27-7
- BR: perl-generators unconditionally

* Fri Feb 09 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.27-6
- Escape macros in %%changelog

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.27-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.27-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jun 05 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.27-3
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.27-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu May 19 2016 Paul Howarth <paul@city-fan.org> - 0.27-1
- Update to 0.27
  - Allow packages to be cleaned multiple times
  - Ensure the debugger workarounds are applied only when DB::sub is actively
    used (they are superfluous otherwise)
  - Work around P5#72210, resulting in fails on 5.8.8 -Duselongdouble
  - Fix incorrect name in META (CPAN RT#107813)
- BR: perl-generators where available
- Simplify find command using -delete

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.26-3
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.26-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Oct  7 2015 Paul Howarth <paul@city-fan.org> - 0.26-1
- Update to 0.26
  - Exclusively use Package::Stash::PP on perls < 5.8.7 until a fixed
    Package::Stash::XS ships - breakage keeps getting re-introduced
    (CPAN RT#74151, CPAN RT#107343)
  - Explicitly document the late runtime binding of 'sort SUBNAME ...'
    (CPAN RT#101247)
  - No longer rely on Sub::Identify - either use Sub::Util or B (CPAN RT#96945)
- Classify buildreqs by usage
- Filter dependency on private package namespace::clean::_Util
- Drop EL-6 support since build requirements can't be met there

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.25-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.25-4
- Perl 5.22 rebuild

* Fri Aug 29 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.25-3
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.25-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Mar  5 2014 Paul Howarth <paul@city-fan.org> - 0.25-1
- Update to 0.25
  - Fix incorrect ExtUtils::CBuilder detection routine leading to Makefile.PL
    crashes when EU::CB is not available
- Drop obsoletes/provides for old tests sub-package
- Drop EL-5 support since build requirements can't be met there

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.24-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul 29 2013 Petr Pisar <ppisar@redhat.com> - 0.24-3
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.24-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Dec  5 2012 Paul Howarth <paul@city-fan.org> - 0.24-1
- Update to 0.24
  - Properly skip debugger test when optional deps not available
  - Make sure pure-perl tests pass correctly on space-containing paths
    (CPAN RT#77528)
  - Remove all the pure-perl fallback code and depend on PP-capable
    B::H::EOS 0.12
- Module no longer attempts to use Hash::Util::FieldHash, so drop filters
- BR: perl(Sub::Identify) and perl(Sub::Name) unconditionally
- BR: perl(base), perl(ExtUtils::CBuilder) and perl(lib)
- Drop BR: perl(FindBin), not dual-lived upstream
- Update patch for building with old Test::More versions

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.23-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 19 2012 Petr Pisar <ppisar@redhat.com> - 0.23-2
- Perl 5.16 rebuild

* Sun Mar 11 2012 Paul Howarth <paul@city-fan.org> - 0.23-1
- Update to 0.23
  - Rely on B::Hooks::EndOfScope version 0.10 to fix issues with new
    Module::Runtime versions (≥ 0.012) on perl 5.10 due to incorrect hook
    firing due to %%^H localisation
  - Fix failures on 5.13.6 due to incorrect version number threshold
    (CPAN RT#74683)
- Don't need to remove empty directories from buildroot
- Drop %%defattr, redundant since rpm 4.4

* Fri Jan 27 2012 Paul Howarth <paul@city-fan.org> - 0.22-1
- Update to 0.22
  - Limit the debugger workarounds to perls between 5.8.8 and 5.14, extend
    debugger support to all perl versions (CPAN RT#69862)
  - If possible, automatically install (but not load) the debugger workaround
    libraries on perls between 5.8.8 and 5.14 (CPAN RT#72368)
  - Add back dropped NAME section (CPAN RT#70259)
  - Simplify the ≥ 5.10 PP variant even more - move the hook from DESTROY
    into DELETE
  - Force explicit callback invocation order on 5.8 PP
  - Replace the %%^H tie approach with fieldhashes, which fixes all known
    corner cases and caveats on supported perls ≥ 5.8.1 (CPAN RT#73402)
  - Compile away the debugger fixup on perls ≥ 5.15.5
- Only BR:/R: Sub::Identify and Sub::Name for perl versions where they're
  actually needed
- Reinstate compatibility with old distributions like EL-5
  - Patch test suite to work with Test::More < 0.88 if necessary
  - Filter dependency on Hash::Util::FieldHash on perl 5.8.x
  - Add back buildroot definition, %%clean section, %%defattr etc.
- Only include tests if we have %%{perl_default_filter} to avoid the unwanted
  requires/provides that come with them
- Drop redundant buildreq perl(CPAN)
- Make %%files list more explicit
- Use tabs

* Sun Jan 22 2012 Iain Arnell <iarnell@gmail.com> - 0.21-3
- Drop tests subpackage; move tests to main package documentation

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.21-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Oct 02 2011 Iain Arnell <iarnell@gmail.com> - 0.21-1
- Update to latest upstream version
- Clean up spec for modern rpmbuild

* Wed Jul 20 2011 Petr Sabata <contyk@redhat.com> - 0.20-3
- Perl mass rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jan 08 2011 Iain Arnell <iarnell@gmail.com> - 0.20-1
- Update to latest upstream version
- Update BR perl(Package::Stash) >= 0.22

* Tue Dec 21 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.18-2
- Rebuild to fix problems with vendorarch/lib (#661697)

* Sun Aug 01 2010 Iain Arnell <iarnell@gmail.com> - 0.18-1
- Update by Fedora::App::MaintainerTools 0.006
- Updating to latest GA CPAN version (0.18)
- Added a new br on perl(Exporter) (version 0)
- Altered br on perl(ExtUtils::MakeMaker) (6.42 => 6.31)
- Added a new br on perl(Package::Stash) (version 0.03)
- Added a new br on perl(constant) (version 0)
- Added a new br on perl(vars) (version 0)
- Dropped old BR on perl(Symbol)
- Dropped old requires on perl(Symbol)
- Manually drop unnecessary requires

* Tue May 04 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.14-1
- Mass rebuild with perl-5.12.0 & update

* Tue Feb 23 2010 Chris Weyl <cweyl@alumni.drew.edu> - 0.13-2
- Update by Fedora::App::MaintainerTools 0.003
- PERL_INSTALL_ROOT => DESTDIR

* Fri Feb 05 2010 Chris Weyl <cweyl@alumni.drew.edu> - 0.13-1
- Update filtering perl_default_filter
- Auto-update to 0.13 (by cpan-spec-update 0.01)
- Altered br on perl(ExtUtils::MakeMaker) (0 => 6.42)
- Added a new br on perl(Sub::Identify) (version 0.04)
- Added a new br on perl(Sub::Name) (version 0.04)
- Altered br on perl(Test::More) (0.62 => 0.88)
- Added a new br on CPAN (inc::Module::AutoInstall found)
- Added a new req on perl(B::Hooks::EndOfScope) (version 0.07)
- Added a new req on perl(Sub::Identify) (version 0.04)
- Added a new req on perl(Sub::Name) (version 0.04)
- Added a new req on perl(Symbol) (version 0)

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.11-3
- Rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Apr 02 2009 Chris Weyl <cweyl@alumni.drew.edu> - 0.11-1
- Update to 0.11

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.09-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Dec 02 2008 Chris Weyl <cweyl@alumni.drew.edu> - 0.09-1
- Update to 0.09
- Note BR change from Scope::Guard to B::Hooks::EndOfScope

* Mon Sep 08 2008 Chris Weyl <cweyl@alumni.drew.edu> - 0.08-2
- Bump

* Sat Sep 06 2008 Chris Weyl <cweyl@alumni.drew.edu> - 0.08-1
- Initial Fedora packaging
- Generated with cpan2dist (CPANPLUS::Dist::Fedora version 0.0.1)
