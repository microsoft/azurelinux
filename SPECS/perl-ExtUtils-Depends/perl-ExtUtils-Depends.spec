Name:           perl-ExtUtils-Depends
Version:        0.8000
Release:        6%{?dist}
Summary:        Easily build XS extensions that depend on XS extensions
License:        GPL+ or Artistic
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://metacpan.org/release/ExtUtils-Depends
Source0:        https://cpan.metacpan.org/modules/by-module/ExtUtils/ExtUtils-Depends-%{version}.tar.gz#/perl-ExtUtils-Depends-%{version}.tar.gz
BuildArch:      noarch
# Module Build
BuildRequires:  coreutils
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(Cwd)
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
# Module Runtime
BuildRequires:  perl(Carp)
BuildRequires:  perl(Config)
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(DynaLoader)
BuildRequires:  perl(File::Find)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(IO::File)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# Test Suite
BuildRequires:  perl(base)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(File::Path)
BuildRequires:  perl(File::Spec::Functions)
BuildRequires:  perl(File::Temp)
BuildRequires:  perl(FindBin)
BuildRequires:  perl(lib)
BuildRequires:  perl(Test::More)
# Runtime
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:       perl(DynaLoader)

%description
This module tries to make it easy to build Perl extensions that use
functions and typemaps provided by other Perl extensions. This means
that a Perl extension is treated like a shared library that provides
also a C and an XS interface besides the Perl one.

%prep
%setup -q -n ExtUtils-Depends-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PERLLOCAL=1 NO_PACKLIST=1
%{make_build}

%install
%{make_install}
%{_fixperms} -c %{buildroot}

%check
make test

%files
%doc Changes README
%{perl_vendorlib}/ExtUtils/
%{_mandir}/man3/ExtUtils::Depends.3*

%changelog
* Thu Aug 22 2024 Neha Agarwal <nehaagrwal@microsoft.com> - 0.8000-6
- Promote package to Core repository.

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.8000-5
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.8000-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.8000-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu May 30 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.8000-2
- Perl 5.30 rebuild

* Wed Apr 10 2019 Paul Howarth <paul@city-fan.org> - 0.8000-1
- Update to 0.8000
  - Bump version so https://metacpan.org/pod/ExtUtils::Depends shows the
    correct ExtUtils::Depends module
  - Quote directories with spaces
- Modernize spec using features from ExtUtils::MakeMaker ≥ 6.76

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.405-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.405-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.405-8
- Perl 5.28 rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.405-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.405-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.405-5
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.405-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.405-3
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.405-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Dec  1 2015 Paul Howarth <paul@city-fan.org> - 0.405-1
- Update to 0.405
  - Remove MYMETA.* from MANIFEST file (CPAN RT#108554)

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.404-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.404-2
- Perl 5.22 rebuild

* Fri Jan 30 2015 Paul Howarth <paul@city-fan.org> - 0.404-1
- Update to 0.404
  - Depends.pm: sort deps in save_config() and get_makefile_vars()
    (CPAN RT#101602)
  - Use / to make ::load filename, not File::Spec - perldoc -f require

* Mon Jan  5 2015 Paul Howarth <paul@city-fan.org> - 0.403-1
- Update to 0.403
  - Avoid using Test::More::done_testing() for to support building
    out-of-the-box on older perls

* Mon Oct 20 2014 Paul Howarth <paul@city-fan.org> - 0.402-1
- Update to 0.402
  - Set Data::Dumper::Sortkeys = 1 in ExtUtils::Depends->save_config()
    (CPAN RT#99260)

* Sun Sep 07 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.401-2
- Perl 5.20 rebuild

* Fri Sep  5 2014 Paul Howarth <paul@city-fan.org> - 0.401-1
- Update to 0.401
  - Add README changes created by 'make dist' from the POD
  - Rename test modules
  - Test old/new schemes with .pm files
  - Move old/new scheme tests from middle of other stuff to end
  - Rename test packages to 8.3 unique
- This release by XAOC → update source URL

* Thu Aug 28 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.400-2
- Perl 5.20 rebuild

* Thu Aug 14 2014 Paul Howarth <paul@city-fan.org> - 0.400-1
- Update to 0.400
  - Depends.pm: use $DLEXT instead of $SO for library filename extensions
  - MANIFEST: remove MYMETA.* files
  - Use DynaLoader::mod2fname if available
  - Added Android support
  - In addition to the package variables $inc, $libs and @typemaps, write an
    'Inline' method to <package>::Install::Files for easier interoperability
    with the Inline module
  - Accompany the 'Inline' method with a 'deps' method in
    <package>::Install::Files in addition to the @deps package variable
  - Make ExtUtils::Depends->load use the 'Inline' and 'deps' methods by
    default, falling back to the package variables if the methods are not
    defined
  - Make the docs recommend the 'Inline' and 'deps' approach for creating
    <package>::Install::Files manually, without ExtUtils::Depends::save_config
- This release by TSCH → update source URL
- BR:/R: perl(DynaLoader)
- As we now need Test::More ≥ 0.88, drop EL-5 support

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.308-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon May 19 2014 Paul Howarth <paul@city-fan.org> - 0.308-1
- Update to 0.308
  - Fix win32 test failure in t/02_save_load.t (CPAN RT#95301)

* Tue Apr 29 2014 Paul Howarth <paul@city-fan.org> - 0.307-1
- Update to 0.307
  - $Data::Dumper::Terse set to 1 broke save_config
  - Document API expected by ::load function
- Classify buildreqs by usage
- Make %%files list more explicit
- Use DESTDIR rather than PERL_INSTALL_ROOT
- Don't use macros for commands

* Mon Sep 30 2013 Paul Howarth <paul@city-fan.org> - 0.306-1
- Update to 0.306
  - Fixed typo in RT queue URL (CPAN RT#88960)

* Tue Sep  3 2013 Paul Howarth <paul@city-fan.org> - 0.305-1
- Update to 0.305
  - Makefile.PL: converted to CPAN::Meta::Spec v2
  - Updated license in RPM spec file (CPAN RT#88196)
  - Updated contact info and added git repo info to POD
  - Add comments for find_extra_libs method (CPAN RT#43900)
  - Fixed typo (CPAN RT#86572)
- This release by XAOC -> update source URL

* Fri Aug 16 2013 Paul Howarth <paul@city-fan.org> - 0.304-1
- Update to 0.304
  - More robust detection of gcc toolchains on Win32 (CPAN RT#62455)
  - Don't assume dlltool is called 'dlltool' on Win32+gcc - ask Config.pm
    instead (CPAN RT#62455)
- Don't need to remove empty directories from the buildroot
- Drop %%defattr, redundant since rpm 4.4

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.303-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 0.303-8
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.303-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.303-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 11 2012 Petr Pisar <ppisar@redhat.com> - 0.303-5
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.303-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.303-3
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.303-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 23 2010 Steven Pritchard <steve@kspei.com> 0.303-1
- Update to 0.303.
- Update Source0 URL.

* Thu Dec 16 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.302-5
- Rebuild to fix problems with vendorarch/lib (#661697)

* Sat May 01 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.302-4
- Mass rebuild with perl-5.12.0

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.302-3
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.302-2
- rebuild against perl 5.10.1

* Fri Jul 31 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.302-1
- auto-update to 0.302 (by cpan-spec-update 0.01)
- added a new br on perl(Data::Dumper) (version 0)
- added a new br on perl(File::Spec) (version 0)
- added a new br on perl(IO::File) (version 0)

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.301-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.301-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Dec 12 2008 Steven Pritchard <steve@kspei.com> 0.301-1
- Update to 0.301.

* Thu May 15 2008 Steven Pritchard <steve@kspei.com> 0.300-1
- Update to 0.300.
- Clean up to match cpanspec output.
- Fix find option order.
- Use fixperms macro instead of our own chmod incantation.
- Update Source0 URL.
- BR Test::More.

* Tue Feb  5 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.205-6
- rebuild for new perl

* Mon Oct 15 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 0.205-5.1
- correct license tag
- add BR: perl(ExtUtils::MakeMaker)

* Fri Sep  8 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.205-5
- Rebuild for FC6.

* Wed Feb 15 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.205-4
- Rebuild for FC5 (perl 5.8.8).

* Thu Dec 29 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.205-3
- Dist tag.

* Wed Apr  6 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 0.205-2
- rebuilt

* Tue Feb 15 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0:0.205-1
- Update to 0.205.

* Sun Oct  3 2004 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0:0.204-0.fdr.1
- Update to 0.204.

* Sun Jul 18 2004 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0:0.202-0.fdr.1
- First build.
