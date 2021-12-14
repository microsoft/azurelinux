# Run optional test
%if ! 0%{?rhel}
%bcond_without perl_YAML_LibYAML_enables_optional_test
%else
%bcond_with perl_YAML_LibYAML_enables_optional_test
%endif

Name:           perl-YAML-LibYAML
Version:        0.81
Release:        3%{?dist}
Summary:        Perl YAML Serialization using XS and libyaml
License:        GPL+ or Artistic
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://metacpan.org/release/YAML-LibYAML
Source0:        https://cpan.metacpan.org/modules/by-module/YAML/YAML-LibYAML-%{version}.tar.gz#/perl-YAML-LibYAML-%{version}.tar.gz
Patch0:         YAML-LibYAML-0.79-Unbundled-libyaml.patch

# Build
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  libyaml >= 0.2.2
BuildRequires:  libyaml-devel >= 0.2.2
BuildRequires:  perl-devel
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(Config)
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  sed

# Module
BuildRequires:  perl(B::Deparse)
BuildRequires:  perl(base)
BuildRequires:  perl(constant)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
BuildRequires:  perl(XSLoader)

# Tests
BuildRequires:  perl(B)
BuildRequires:  perl(blib)
BuildRequires:  perl(Carp)
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(Devel::Peek)
BuildRequires:  perl(Encode)
BuildRequires:  perl(File::Find)
BuildRequires:  perl(File::Path)
BuildRequires:  perl(Filter::Util::Call)
BuildRequires:  perl(FindBin)
BuildRequires:  perl(IO::File)
BuildRequires:  perl(IO::Pipe)
BuildRequires:  perl(lib)
BuildRequires:  perl(Test::Builder)
BuildRequires:  perl(Test::More) >= 0.88
BuildRequires:  perl(Tie::Array)
BuildRequires:  perl(Tie::Hash)
BuildRequires:  perl(utf8)

%if %{with perl_YAML_LibYAML_enables_optional_test}
# Optional Tests
BuildRequires:  perl(Path::Class)
%endif

# Dependencies
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:       perl(B::Deparse)
Requires:       libyaml >= 0.2.2

# Avoid provides for perl shared objects
%{?perl_default_filter}

%description
Kirill Siminov's "libyaml" is arguably the best YAML implementation. The C
library is written precisely to the YAML 1.1 specification. It was originally
bound to Python and was later bound to Ruby.

%prep
%setup -q -n YAML-LibYAML-%{version}
# Unbundled libyaml, the source files are the same as in libyaml-0.2.2
# It was determined by comparing commits in upstream repo:
# https://github.com/yaml/libyaml/
%patch0 -p1 -b .orig
for file in api.c dumper.c emitter.c loader.c parser.c reader.c scanner.c \
    writer.c yaml.h yaml_private.h; do
    rm LibYAML/$file
    sed -i -e "/^LibYAML\/$file/d" MANIFEST
done

%build
perl Makefile.PL INSTALLDIRS=vendor OPTIMIZE="%{optflags}" NO_PACKLIST=1 NO_PERLLOCAL=1
%{make_build}

%install
%{make_install}
find %{buildroot} -type f -name '*.bs' -empty -delete
%{_fixperms} -c %{buildroot}

%check
make test

%files
%license LICENSE
%doc Changes CONTRIBUTING README
%{perl_vendorarch}/auto/YAML/
%{perl_vendorarch}/YAML/
%{_mandir}/man3/YAML::LibYAML.3*
%{_mandir}/man3/YAML::XS.3*
%{_mandir}/man3/YAML::XS::LibYAML.3*

%changelog
* Mon Nov 01 2021 Muhammad Falak <mwani@microsft.com> - 0.81-3
- Remove epoch

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1:0.81-2
- Initial CBL-Mariner import from Fedora 31 (license: MIT).

* Tue Jan 28 2020 Jitka Plesnikova <jplesnik@redhat.com> - 1:0.81-1
- Update to 0.81
  - Breaking Change: Set $YAML::XS::LoadBlessed default to false to make it
    more secure

* Thu Aug 22 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1:0.80-1
- Update to 0.80
  - Fix memory leak when loading invalid YAML

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.79-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Jun 12 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1:0.79-1
- Update to 0.79
  - Support aliasing scalars resolved as null or booleans
  - Add YAML::XS::LibYAML::libyaml_version()
  - Support standard !!int/!!float tags instead of dying
- Unbundled libyaml, it is identical with upstream 0.2.2

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1:0.78-2
- Perl 5.30 rebuild

* Sun May 19 2019 Paul Howarth <paul@city-fan.org> - 1:0.78-1
- Update to 0.78
  - Fix double free/core dump when Dump()ing binary data (GH#91)
  - Update config.h from libyaml
- Modernize spec using %%{make_build} and %%{make_install}

* Tue Apr 16 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1:0.77-1
- Update to 0.77
 - Update libyaml to version 0.2.2 - Most important change for users is that
   plain urls in flow style can be parsed now

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.76-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Jan 02 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1:0.76-1
- Update to 0.76
  - Add $Indent - number of spaces when dumping
  - Fix typo and links in docs

* Sat Nov  3 2018 Paul Howarth <paul@city-fan.org> - 1:0.75-1
- Update to 0.75
  - Implement $LoadCode

* Mon Sep  3 2018 Paul Howarth <paul@city-fan.org> - 1:0.74-1
- Update to 0.74
  - Fix tests on older perls
  - Support back to perl 5.8.1

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.72-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jul 09 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1:0.72-1
- Update to 0.72
  - Update to libyaml 0.2.1 - It's forbidden now to escape single
    quotes inside double quotes
  - When disabling $LoadBlessed, return scalars not refs
  - Save anchors also for blessed scalars

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1:0.70-2
- Perl 5.28 rebuild

* Sun Jun 10 2018 Paul Howarth <paul@city-fan.org> - 1:0.70-1
- Update to 0.70
  - Fix format specifier/argument mismatch (GH#79)
  - Travis CI: Test on Perl 5.26 (GH#80)
  - Fix a C90-compatibility issue (GH#81)
- Switch upstream from search.cpan.org to metacpan.org

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.69-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Dec 28 2017 Paul Howarth <paul@city-fan.org> - 1:0.69-1
- Update to 0.69
  - Security fix: Add $LoadBlessed option to turn on/off loading objects
    (GH#73, GH#74)

* Tue Dec 19 2017 Paul Howarth <paul@city-fan.org> - 1:0.68-1
- Update to 0.68
  - Fix regex roundtrip (GH#69, GH#70)
  - Fix loading of many regexes (GH#64, GH#71)

* Thu Nov 16 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1:0.67-1
- Update to 0.67
  - Support standard tags !!str, !!map and !!seq instead of dying (GH#67)
  - Support JSON::PP::Boolean and boolean.pm via $YAML::XS::Boolean (GH#66)

* Fri Aug 18 2017 Paul Howarth <paul@city-fan.org> - 1:0.66-1
- Update to 0.66
  - Dump() was modifying original data, adding a PV to numbers (GH#32, GH#55)

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.65-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.65-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1:0.65-2
- Perl 5.26 rebuild

* Fri May 19 2017 Paul Howarth <paul@city-fan.org> - 1:0.65-1
- Update to 0.65
  - Prevent warning about unused variables (GH#59)
  - Clarify documentation about exported functions

* Sun Apr  9 2017 Paul Howarth <paul@city-fan.org> - 1:0.64-1
- Update to 0.64
  - use lib FindBin::Bin in tests, preparing for perl 5.26 where '.' gets
    removed from @INC (GH#54)
  - Use the latest libyaml sources
  - Lazy load B::Deparse for faster startup time (GH#52, GH#53)
- Drop redundant Group: tag
- Add provide for bundled(libyaml)

* Tue Mar  7 2017 Paul Howarth <paul@city-fan.org> - 1:0.63-2
- Revert to 0.63; the 0.71 release was unauthorized

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.71-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Sep  8 2016 Paul Howarth <paul@city-fan.org> - 0.71-1
- Update to 0.71
  - Merge with libyaml 0.1.7 upstream
  - cperl fixes for fake_signatures
  - libyaml fix C++-compat errors
  - Improve Makefile for Win32
  - Improve ppport_sort.h
  - Implement new NonStrict mode (for perl5 compat)
  - libyaml reformat, minor optimizations, fix warnings
  - Update documentation
  - Use error codes, return undef on error
  - Abstract the loader functionality to load_impl(), dump_impl() not yet
  - Rearrange static funcs (not decl in header)
  - DumpFile,LoadFile is now XS only, and do accept mg pv, io objects and
    fileglobs; support filename in error messages
  - Support $YAML::XS::NonStrict loader
  - Add dumper options Indent, BestWidth, Canonical, Unicode, Encoding,
    LineBreak, OpenEnded (kept defaults)
  - Add loader option NonStrict, Encoding (kept defaults)
  - Fix default emitter_set_width (2 ⇒ 80)
  - Fix the tests for the new default IndentlessMap=0 and check also
    IndentlessMap=1
  - Enable 2 more test/glob.t tests
  - Fix dump_yaml in test/TestYAMLTests.pm
  - Avoid duplicate checks against NULL
- This release by RURBAN → update source URL

* Fri Jul  8 2016 Paul Howarth <paul@city-fan.org> - 0.63-1
- Update to 0.63
  - Fix memory leaks (GH#48)
- BR: perl-generators
- Simplify find command using -empty

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.62-2
- Perl 5.24 rebuild

* Mon Feb 22 2016 Paul Howarth <paul@city-fan.org> - 0.62-1
- Update to 0.62
  - Fix for detecting filehandles (GH#42)
- This release by TINITA → update source URL

* Sun Feb 21 2016 Paul Howarth <paul@city-fan.org> - 0.61-1
- Update to 0.61
  - Allow reading from and writing to IO::Handle (and derived) objects (GH#37)

* Wed Feb 10 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.60-1
- 0.60 bump

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.59-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.59-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.59-2
- Perl 5.22 rebuild

* Tue Jan 27 2015 Paul Howarth <paul@city-fan.org> - 0.59-1
- Update to 0.59
  - Better scalar dump heuristics (PR/23)
  - More closely match YAML.pm

* Wed Jan 21 2015 Paul Howarth <paul@city-fan.org> - 0.58-1
- Update to 0.58
  - Add a VERSION statement to YAML::LibYAML (GH#8)
- This release by INGY → update source URL

* Fri Jan 16 2015 Paul Howarth <paul@city-fan.org> - 0.57-1
- Update to 0.57
  - Update copyright year
  - Use Swim cpan-tail block functions in doc
  - Format string fixes (PR#21, CPAN RT#46507, CVE-2012-1152)
- This release by NAWGLAN → update source URL
- Drop patch for format string fixes, upstreamed at long last

* Wed Dec 24 2014 Paul Howarth <paul@city-fan.org> - 0.55-1
- Update to 0.55
  - Get YAML::XS using latest libyaml

* Sun Nov 30 2014 Paul Howarth <paul@city-fan.org> - 0.54-1
- Update to 0.54
  - Fix for an edge case in scanner that results in an assert() failing
    (https://bitbucket.org/xi/libyaml/issue/10/wrapped-strings-cause-assert-failure)
    (CVE-2014-9130)
- Drop upstreamed patches for CVE-2013-6393 and CVE-2014-2525

* Tue Nov 18 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.52-3
- Update BRs (bz#1165198)

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.52-2
- Perl 5.20 rebuild

* Sun Aug 24 2014 Paul Howarth <paul@city-fan.org> - 0.52-1
- Update to 0.52
  - Fix e1 test failure on 5.21.4

* Mon Aug 18 2014 Paul Howarth <paul@city-fan.org> - 0.51-1
- Update to 0.51 (various minor tidy-ups, no functional changes)

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.47-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Aug  9 2014 Paul Howarth <paul@city-fan.org> - 0.47-1
- Update to 0.47:
  - Fix swim errors
- Include upstream license file

* Wed Aug 06 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.46-1
- 0.46 bump

* Tue Aug 05 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.45-1
- 0.45 bump

* Mon Jul 14 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.44-1
- 0.44 bump

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.41-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Mar 27 2014 Paul Howarth <paul@city-fan.org> - 0.41-4
- Fix LibYAML input sanitization errors (CVE-2014-2525)
- Fix heap-based buffer overflow when parsing YAML tags (CVE-2013-6393)

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.41-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 0.41-2
- Perl 5.18 rebuild

* Wed Mar 13 2013 Paul Howarth <paul@city-fan.org> - 0.41-1
- Update to 0.41:
  - Removed C++ // style comments, for better portability

* Tue Feb 12 2013 Paul Howarth <paul@city-fan.org> - 0.39-1
- Update to 0.39:
  - Using the latest libyaml codebase
    (https://github.com/yaml/libyaml/tree/perl-yaml-xs)
  - Changes have been made to start moving libyaml to 1.2

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.38-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 11 2012 Petr Pisar <ppisar@redhat.com> - 0.38-3
- Perl 5.16 rebuild
- Build-require Data::Dumper

* Thu Mar 29 2012 Paul Howarth <paul@city-fan.org> - 0.38-2
- Fix various format string vulnerabilities (CVE-2012-1152, CPAN RT#46507)
- De-duplicate buildreqs, with Module>Install>Tests priority
- Install to vendor directories
- Don't need to remove empty directories from buildroot
- Don't use macros for commands
- Make %%files list more explicit
- Tidy %%description

* Fri Jan 13 2012 Marcela Mašláňová <mmaslano@redhat.com> - 0.38-1
- Bump to 0.38

* Fri Sep 30 2011 Petr Sabata <contyk@redhat.com> - 0.37-1
- 0.37 bump
- Remove defattr
- Correct BR

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.35-2
- Perl mass rebuild

* Mon Apr 04 2011 Petr Sabata <psabata@redhat.com> - 0.35-1
- 0.35 bump
- Removing obsolete buildroot stuff

* Wed Mar 16 2011 Paul Howarth <paul@city-fan.org> - 0.34-4
- Improve overly-generic package summary
- README is already UTF-8 encoded in version 0.34 so don't try converting it

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.34-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Sep 29 2010 jkeating - 0.34-2
- Rebuilt for gcc bug 634757

* Fri Sep 24 2010 Marcela Mašláňová <mmaslano@redhat.com> - 0.34-1
- update

* Thu Jun  3 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.33-1
- update

* Fri May 07 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.32-6
- Mass rebuild with perl-5.12.0

* Sat Mar 27 2010 Chris Weyl <cweyl@alumni.drew.edu> - 0.32-5
- perl_default_filter, PERL_INSTALL_ROOT => DESTDIR

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.32-4
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.32-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Apr 29 2009 Marcela Mašláňová <mmaslano@redhat.com> 0.32-2
- add BR

* Wed Apr 29 2009 Marcela Mašláňová <mmaslano@redhat.com> 0.32-1
- Specfile autogenerated by cpanspec 1.78.
