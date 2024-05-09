# Run optional test
%if ! 0%{?rhel}
%bcond_without perl_YAML_Syck_enables_optional_test
%else
%bcond_with perl_YAML_Syck_enables_optional_test
%endif

Name:           perl-YAML-Syck
Version:        1.32
Release:        2%{?dist}
Summary:        Fast, lightweight YAML loader and dumper
License:        BSD and MIT
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://metacpan.org/release/YAML-Syck
Source0:        https://cpan.metacpan.org/modules/by-module/YAML/YAML-Syck-%{version}.tar.gz#/perl-YAML-Syck-%{version}.tar.gz
# Module Build
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  perl-devel
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(ExtUtils::MakeMaker)
# Dependencies of bundled ExtUtils::HasCompiler
BuildRequires:  perl(base)
BuildRequires:  perl(Carp)
BuildRequires:  perl(Config)
BuildRequires:  perl(DynaLoader)
BuildRequires:  perl(ExtUtils::Mksymlists)
BuildRequires:  perl(File::Basename)
BuildRequires:  perl(File::Spec::Functions)
BuildRequires:  perl(File::Temp)
# Module Runtime
BuildRequires:  perl(constant)
# DynaLoader not used if XSLoader is available
BuildRequires:  perl(Exporter)
BuildRequires:  perl(strict)
BuildRequires:  perl(vars)
BuildRequires:  perl(XSLoader)
# Test Suite
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(FindBin)
BuildRequires:  perl(IO::File)
BuildRequires:  perl(Storable)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Tie::Hash)
BuildRequires:  perl(utf8)
BuildRequires:  perl(warnings)
# Optional Tests
%if %{with perl_YAML_Syck_enables_optional_test}
BuildRequires:  perl(Devel::Leak)
BuildRequires:  perl(JSON)
BuildRequires:  perl(Symbol)
%endif
# Dependencies
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

# Avoid provides for private perl objects
%{?perl_default_filter}

%description
This module provides a Perl interface to the libsyck data serialization
library. It exports the Dump and Load functions for converting Perl data
structures to YAML strings, and the other way around.

%prep
%setup -q -n YAML-Syck-%{version}

# Unbundle core and unused modules
rm -rvf inc/{Module,Scalar,Test}

%build
perl Makefile.PL INSTALLDIRS=vendor OPTIMIZE="%{optflags} -DI_STDLIB=1 -DI_STRING=1"
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name '*.bs' -empty -delete
%{_fixperms} -c %{buildroot}

%check
make test

%files
%license COPYING
%doc Changes COMPATIBILITY README.md
%{perl_vendorarch}/auto/YAML/
%{perl_vendorarch}/YAML/
%{perl_vendorarch}/JSON/
%{_mandir}/man3/JSON::Syck.3*
%{_mandir}/man3/YAML::Syck.3*

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.32-2
- Initial CBL-Mariner import from Fedora 31 (license: MIT).

* Tue Jan 28 2020 Paul Howarth <paul@city-fan.org> - 1.32-1
- Update to 1.32
  - Interface Change: Change default for LoadBlessed to false
  - Remove YAML::Syck tests that parse META.yml
  - Switch to github actions for testing
  - Remove 'use vars' from code in favor of 'our'

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.31-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.31-3
- Perl 5.30 rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.31-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Oct 26 2018 Paul Howarth <paul@city-fan.org> - 1.31-1
- Update to 1.31
  - Switch to ExtUtils::MakeMaker for builder
  - Switch official issue tracker and repo to github
  - MANIFEST warning is now fixed; also shipping additional tests because of
    this
- Make sure <stdlib.h> and <string.h> are included, quietens lots of warnings

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.30-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.30-6
- Perl 5.28 rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.30-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.30-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.30-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.30-2
- Perl 5.26 rebuild

* Thu Apr 20 2017 Paul Howarth <paul@city-fan.org> - 1.30-1
- Update to 1.30
  - Fix handling carriage return after c-indicator (CPAN RT#41141)
  - Fix CHECK_UTF8 SEGV with empty len=0 strings (CPAN RT#61562)
  - Add missing function declarations
  - Tighten the TODO tests; no passing TODOs now, but still JSON
  - SingleQuote and \/ and \u roundtrips do fail
- Drop EL-5 support
  - Drop Group: and BuildRoot: tags
  - Drop buildroot cleaning in %%install
  - Drop explicit %%clean section

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.29-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.29-6
- Perl 5.24 rebuild

* Wed Apr 20 2016 Paul Howarth <paul@city-fan.org> - 1.29-5
- Fix FTBFS due to missing buildreq perl-devel
- Simplify find commands using -empty and -delete

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.29-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.29-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.29-2
- Perl 5.22 rebuild

* Tue Dec 16 2014 Paul Howarth <paul@city-fan.org> - 1.29-1
- Update to 1.29
  - Upstreamed fix for test failures on PPC and ARM (CPAN RT#83825)
  - Fix crash in syck_emit on platforms with long long pointers
- Use %%license

* Thu Dec 11 2014 Petr Pisar <ppisar@redhat.com> - 1.28-1
- 1.28 bump

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.27-6
- Perl 5.20 rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.27-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.27-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.27-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jul 18 2013 Petr Pisar <ppisar@redhat.com> - 1.27-2
- Perl 5.18 rebuild

* Tue May 21 2013 Paul Howarth <paul@city-fan.org> 1.27-1
- Update to 1.27
  - Fix for hash randomization in yaml-alias.t on perl 5.18.0 (CPAN RT#84882,
    CPAN RT#84466)

* Mon Mar 11 2013 Paul Howarth <paul@city-fan.org> 1.25-1
- Update to 1.25
  - Bump version number and release to fix a MANIFEST mistake in 1.24

* Sun Mar 10 2013 Paul Howarth <paul@city-fan.org> 1.24-2
- Work around test failures on PPC and ARM (#919806, CPAN RT#83825)

* Thu Mar  7 2013 Paul Howarth <paul@city-fan.org> 1.24-1
- Update to 1.24
  - Implement $JSON::Syck::MaxDepth
  - Prevent failure when the same object is seen twice during Dump
  - Prevent YAML from being influenced by the previous change
  - MinGW64 compatibility (CPAN RT#78363)

* Wed Feb 27 2013 Paul Howarth <paul@city-fan.org> 1.23-1
- Update to 1.23
  - Synchronize JSON::Syck with YAML::Syck version number
  - Add DumpInto functions (YAML+Syck), which dump into a provided scalar
    instead of a newly-allocated one
  - Modify DumpFile functions to output directly to the specified
    file/filehandle instead of buffering all output in memory
  - Avoid modifying numbers into strings when emitting
  - Fix error message typo: s/existant/existent/g
  - Fix for non-printable character detection
  - Quote if non-printable characters are present
  - Make sure that LoadBlessed=0 blocks all blessing
  - Start listing primary repo as https://github.com/toddr/YAML-Syck
  - README refreshed via perldoc -t
- Require perl(XSLoader) at runtime
- Drop %%defattr, redundant since rpm 4.4
- Don't need to remove empty directories from the buildroot
- Don't use macros for commands
- Use DESTDIR rather than PERL_INSTALL_ROOT
- Make %%files list more explicit

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.20-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.20-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 20 2012 Petr Pisar <ppisar@redhat.com> - 1.20-2
- Perl 5.16 rebuild

* Wed Jun 20 2012 Petr Pisar <ppisar@redhat.com> - 1.20-1
- 1.20 bump

* Sat Jun 16 2012 Petr Pisar <ppisar@redhat.com> - 1.17-5
- Perl 5.16 rebuild
- Specify all dependencies

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.17-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jul 20 2011 Iain Arnell <iarnell@gmail.com> - 1.17 -3
- Perl mass rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.17-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 07 2010 Steven Pritchard <steve@kspei.com> 1.17-1
- Update to 1.17.
- Update Source0 URL.
- BR JSON (for tests).

* Fri May 07 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.07-4
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.07-3
- rebuild against perl 5.10.1

* Tue Oct  6 2009 Marcela Mašláňová <mmaslano@redhat.com> - 1.07-2
- fix license

* Sun Sep 27 2009 Chris Weyl <cweyl@alumni.drew.edu> 1.07-1
- auto-update to 1.07 (by cpan-spec-update 0.01)

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.05-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.05-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Jun 09 2008 Steven Pritchard <steve@kspei.com> 1.05-1
- Update to 1.05.

* Mon Mar  3 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.04-2
- rebuild for new perl (again)

* Wed Feb 20 2008 Steven Pritchard <steve@kspei.com> 1.04-1
- Update to 1.04.

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.01-3
- Autorebuild for GCC 4.3

* Fri Feb  8 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.01-2
- rebuild for new perl

* Mon Jan 28 2008 Steven Pritchard <steve@kspei.com> 1.01-1
- Update to 1.01.

* Tue Oct 16 2007 Steven Pritchard <steve@kspei.com> 0.98-1
- Update to 0.98.

* Tue Sep 18 2007 Steven Pritchard <steve@kspei.com> 0.97-1
- Update to 0.97.

* Sun Aug 12 2007 Steven Pritchard <steve@kspei.com> 0.96-1
- Update to 0.96.

* Fri Aug 03 2007 Steven Pritchard <steve@kspei.com> 0.95-1
- Update to 0.95.

* Fri Jul 13 2007 Steven Pritchard <steve@kspei.com> 0.94-1
- Update to 0.94.

* Wed Jun 27 2007 Steven Pritchard <steve@kspei.com> 0.91-1
- Update to 0.91.

* Sat May 19 2007 Steven Pritchard <steve@kspei.com> 0.85-1
- Update to 0.85.

* Fri May 04 2007 Chris Weyl <cweyl@alumni.drew.edu> 0.82-3
- add perl split BR's

* Fri May 04 2007 Chris Weyl <cweyl@alumni.drew.edu> 0.82-2
- bump

* Thu Feb 01 2007 Steven Pritchard <steve@kspei.com> 0.82-1
- Specfile autogenerated by cpanspec 1.69.1.
- Remove explicit build dependency on perl.
- Include JSON module.
- BR Devel::Leak (for tests).
