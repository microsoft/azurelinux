Summary:	A tiny replacement for Module::Build
Name:		perl-Module-Build-Tiny
Version:	0.051
Release:	1%{?dist}
License:	GPL+ or Artistic
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:		https://metacpan.org/release/Module-Build-Tiny
Source0:	https://cpan.metacpan.org/modules/by-module/Module/Module-Build-Tiny-%{version}.tar.gz#/perl-Module-Build-Tiny-%{version}.tar.gz
BuildArch:	noarch
# Module Build
BuildRequires:	perl-generators
BuildRequires:	perl-interpreter
# Module
BuildRequires:	perl(CPAN::Meta)
BuildRequires:	perl(DynaLoader)
BuildRequires:	perl(Exporter) >= 5.57
BuildRequires:	perl(ExtUtils::CBuilder)
BuildRequires:	perl(ExtUtils::Config) >= 0.003
BuildRequires:	perl(ExtUtils::Helpers) >= 0.020
BuildRequires:	perl(ExtUtils::Install)
BuildRequires:	perl(ExtUtils::InstallPaths) >= 0.002
BuildRequires:	perl(ExtUtils::ParseXS)
BuildRequires:	perl(File::Path)
BuildRequires:	perl(File::Spec::Functions)
BuildRequires:	perl(Getopt::Long) >= 2.36
BuildRequires:	perl(JSON::PP) >= 2
BuildRequires:	perl(Pod::Man)
BuildRequires:	perl(TAP::Harness::Env)
# Test
BuildRequires:	perl(blib)
BuildRequires:	perl(Carp)
BuildRequires:	perl(Cwd)
BuildRequires:	perl(Data::Dumper)
BuildRequires:	perl(File::ShareDir)
BuildRequires:	perl(File::Spec)
BuildRequires:	perl(File::Temp)
BuildRequires:	perl(IO::File)
BuildRequires:	perl(IPC::Open2)
BuildRequires:	perl(IPC::Open3)
BuildRequires:	perl(Test::More) >= 0.88
BuildRequires:	perl(Test::Pod) >= 1.41
BuildRequires:	perl(XSLoader)
# Runtime
Requires:	perl(DynaLoader)
Requires:	perl(ExtUtils::CBuilder)
Requires:	perl(ExtUtils::ParseXS)
Requires:	perl(Pod::Man)
Requires:	perl(TAP::Harness::Env)
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

# ExtUtils::CBuilder in EL-8 has no dependency on gcc or c++ (#1547165)
# so pull them in ourselves
%if 0%{?el8}
BuildRequires:	gcc, gcc-c++
Requires:	gcc, gcc-c++
%endif

%description
Many Perl distributions use a Build.PL file instead of a Makefile.PL file to
drive distribution configuration, build, test and installation. Traditionally,
Build.PL uses Module::Build as the underlying build system. This module
provides a simple, lightweight, drop-in replacement.

Whereas Module::Build has over 6,700 lines of code; this module has less than
70, yet supports the features needed by most pure-Perl distributions.

%prep
%setup -q -n Module-Build-Tiny-%{version}

%build
perl Build.PL --installdirs=vendor
./Build

%install
./Build install --destdir=%{buildroot} --create_packlist=0
%{_fixperms} -c %{buildroot}

%check
./Build test --verbose

%files
%license LICENSE
%doc Changes README Todo
%{perl_vendorlib}/Module/
%{_mandir}/man3/Module::Build::Tiny.3*

%changelog
* Mon Dec 16 2024 Jyoti Kanase <v-jykanase@microsoft.com> - 0.051-1
- Update to 0.051 
- License verified

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.039-17
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.039-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Aug 23 2019 Paul Howarth <paul@city-fan.org> - 0.039-15
- Use author-independent URLs
- Work around ExtUtils::CBuilder in EL-8 having no dependency on gcc or gcc-c++
  (#1547165)

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.039-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.039-13
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.039-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.039-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jun 29 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.039-10
- Perl 5.28 rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.039-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.039-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.039-7
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.039-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.039-5
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.039-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.039-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jun 05 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.039-2
- Perl 5.22 rebuild

* Mon Oct 13 2014 Paul Howarth <paul@city-fan.org> - 0.039-1
- Update to 0.039
  - Supply basename to *.PL files as its args

* Mon Sep 22 2014 Paul Howarth <paul@city-fan.org> - 0.038-1
- Update to 0.038
  - Scrub PERL_MB_OPT in tests too

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.037-2
- Perl 5.20 rebuild

* Mon Jul 28 2014 Paul Howarth <paul@city-fan.org> - 0.037-1
- Update to 0.037
  - Scrub environment variable in tests
- Use %%license

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.036-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May  2 2014 Paul Howarth <paul@city-fan.org> - 0.036-1
- Update to 0.036
  - Add --jobs argument to MBT
  - Add xs directory to include list

* Tue Feb 18 2014 Paul Howarth <paul@city-fan.org> - 0.035-1
- Update to 0.035
  - Fix install test in absence of a compiler

* Wed Jan 22 2014 Paul Howarth <paul@city-fan.org> - 0.034-1
- Update to 0.034
  - Make install tests more platform independent

* Tue Jan 21 2014 Paul Howarth <paul@city-fan.org> - 0.033-1
- Update to 0.033
  - Require Getopt::Long 2.36
  - Add install tests

* Mon Jan 20 2014 Paul Howarth <paul@city-fan.org> - 0.032-1
- Update to 0.032
  - Process argument sources separately
  - Use mod2fname appropriately
- BR:/R: perl(DynaLoader)
- BR: perl(GetOpt::Long) ≥ 2.36 for GetOptionsFromArray
- Drop dependencies on TAP::Harness as we only use TAP::Harness::Env

* Fri Oct 11 2013 Paul Howarth <paul@city-fan.org> - 0.030-1
- Update to 0.030
  - Respect harness environmental variables
  - Add main dir to include path
  - 'include_dirs' must be a list ref, not just a string (CPAN RT#54606)
- BR:/R: perl(TAP::Harness) ≥ 3.29

* Mon Sep 30 2013 Paul Howarth <paul@city-fan.org> - 0.028-1
- Update to 0.028
  - Revert "Removed clean and realclean actions"
  - Build .c and .o in temp/ instead of lib
  - Got rid of IO layers
  - Separate libdoc and bindoc checks

* Mon Sep  9 2013 Paul Howarth <paul@city-fan.org> - 0.027-1
- Update to 0.027
  - Various documentation updates

* Tue Aug 20 2013 Paul Howarth <paul@city-fan.org> - 0.026-1
- Update to 0.026
  - Safe PERL_MB_OPT during configuration stage

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.025-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 24 2013 Petr Pisar <ppisar@redhat.com> - 0.025-2
- Perl 5.18 rebuild

* Fri Jul 12 2013 Paul Howarth <paul@city-fan.org> - 0.025-1
- Update to 0.025
  - Use local tempdir

* Sun Jun 30 2013 Paul Howarth <paul@city-fan.org> - 0.024-1
- Update to 0.024
  - Generate man pages in the correct section

* Wed Jun 12 2013 Paul Howarth <paul@city-fan.org> - 0.023-1
- Update to 0.023
  - Implement --pureperl-only
  - Skip compilation test when not having a compiler

* Sat Jun  1 2013 Paul Howarth <paul@city-fan.org> - 0.022-1
- Update to 0.022
  - Fix dirname code for toplevel XS modules

* Mon May 27 2013 Paul Howarth <paul@city-fan.org> - 0.021-1
- Update to 0.021
  - Add XS support
  - Only manify if really installable
- BR:/R: perl(ExtUtils::CBuilder) and perl(ExtUtils::ParseXS)
- BR: perl(XSLoader) for the test suite

* Mon May 20 2013 Paul Howarth <paul@city-fan.org> - 0.020-1
- Update to 0.020
  - Accept a --create_packlist argument

* Tue Apr 30 2013 Paul Howarth <paul@city-fan.org> - 0.019-1
- Update to 0.019
  - Accept --pureperl-only
- Bump perl(ExtUtils::Helpers) version requirement to 0.020

* Thu Apr 25 2013 Paul Howarth <paul@city-fan.org> - 0.018-1
- Update to 0.018
  - Lazily load Pod::Man and TAP::Harness
  - Don't manify unless necessary
- Bump perl(ExtUtils::Helpers) version requirement to 0.019
- Explicitly require perl(Pod::Man) and perl(TAP::Harness) ≥ 3.0

* Tue Apr 23 2013 Paul Howarth <paul@city-fan.org> - 0.017-2
- Updates following package review (#947455)
  - BR: perl(ExtUtils::Config) for module
  - BR: perl(File::ShareDir) for test suite
  - Drop BR: perl(File::Basename) and perl(File::Find), not dual-lived

* Mon Apr 15 2013 Paul Howarth <paul@city-fan.org> - 0.017-1
- Update to 0.017
  - Switched back from JSON to JSON::PP
  - Remove dependency on File::Find::Rule
  - Switched back to ExtUtils::Helpers for detildefy
  - Drop .modulebuildrc support per Lancaster consensus
  - Fix loading of File::Find
  - Fix redefined warning for find
- Drop BR: perl(ExtUtils::BuildRC), perl(File::Find::Rule), perl(File::HomeDir),
  perl(File::pushd)
- BR: perl(JSON::PP) rather than perl(JSON), and perl(Pod::Man)
- Bump perl(ExtUtils::Helpers) version requirement to 0.017 to avoid the need
  for a workaround for misplaced manpage

* Thu Apr  4 2013 Paul Howarth <paul@city-fan.org> - 0.014-1
- Update to 0.014
  - Added sharedir support
  - Fixed Synopsis
  - Make blib/arch, to satisfy blib.pm
  - Removed dependencies on Test::Exception, Capture::Tiny and File::Slurp

* Mon Apr  1 2013 Paul Howarth <paul@city-fan.org> - 0.013-2
- Sanitize for Fedora submission

* Mon Apr  1 2013 Paul Howarth <paul@city-fan.org> - 0.013-1
- Initial RPM version
