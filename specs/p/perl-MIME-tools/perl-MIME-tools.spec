# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Summary:	Modules for parsing and creating MIME entities in Perl
Name:		perl-MIME-tools
Version:	5.515
Release:	4%{?dist}
License:	GPL-1.0-or-later OR Artistic-1.0-Perl
URL:		https://metacpan.org/release/MIME-tools
Source0:	https://cpan.metacpan.org/modules/by-module/MIME/MIME-tools-%{version}.tar.gz
Patch0:		MIME-tools-5.510-UTF8.patch
BuildArch:	noarch
# ================ Module Build ======================
BuildRequires:	coreutils
BuildRequires:	make
BuildRequires:	perl-generators
BuildRequires:	perl-interpreter
BuildRequires:	perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:	perl(inc::Module::Install)
BuildRequires:	perl(Pod::Man)
BuildRequires:	sed
# ================ Module Runtime ====================
BuildRequires:	perl-MailTools		>= 1.50
BuildRequires:	perl(Carp)
BuildRequires:	perl(Convert::BinHex)
BuildRequires:	perl(Encode)
BuildRequires:	perl(Exporter)
BuildRequires:	perl(File::Path)	>= 1
BuildRequires:	perl(File::Spec)	>= 0.6
BuildRequires:	perl(File::Temp)	>= 0.18
BuildRequires:	perl(IO::File)		>= 1.13
BuildRequires:	perl(IO::Handle)
BuildRequires:	perl(IO::Select)
BuildRequires:	perl(Mail::Field)	>= 1.05
BuildRequires:	perl(Mail::Header)	>= 1.06
BuildRequires:	perl(Mail::Internet)	>= 1.28
BuildRequires:	perl(MIME::Base64)	>= 3.03
BuildRequires:	perl(MIME::QuotedPrint)
BuildRequires:	perl(version)
# ================ Test Suite ========================
BuildRequires:	perl(Cwd)
BuildRequires:	perl(Digest::MD5)
BuildRequires:	perl(Exporter)
BuildRequires:	perl(IO::Socket::INET)
BuildRequires:	perl(lib)
BuildRequires:	perl(Test::Deep)
BuildRequires:	perl(Test::More)
BuildRequires:	perl(Test::Pod)
BuildRequires:	perl(Test::Pod::Coverage)
# ================ Dependencies ======================
Requires:	perl(Convert::BinHex)

# Currently fails a couple of kwalitee tests
BuildConflicts:	perl(Test::Kwalitee)

%description
MIME-tools - modules for parsing (and creating!) MIME entities. Modules in this
toolkit: Abstract message holder (file, scalar, etc.), OO interface for
decoding MIME messages, an extracted and decoded MIME entity, Mail::Field
subclasses for parsing fields, a parsed MIME header (Mail::Header subclass),
parser and tool for building your own MIME parser, and utilities.

%prep
%setup -q -n MIME-tools-%{version}

# Remove bundled dependencies
rm -rv inc/
sed -i -e '/^inc\// d' MANIFEST

# Fix character encoding
%patch -P 0

# The more useful examples will go in %%{_bindir}
mkdir useful-examples
mv examples/mime{dump,encode,explode,postcard,send} useful-examples/

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%{make_build}

%install
%{make_install}
%{_fixperms} -c %{buildroot}

# Put the more useful examples in %%{_bindir}
install -d -m 755 %{buildroot}%{_bindir}
install -d -m 755 %{buildroot}%{_mandir}/man1
cd useful-examples
for ex in mime*
do
	install -p -m 755 ${ex} %{buildroot}%{_bindir}/
	pod2man ${ex} > %{buildroot}%{_mandir}/man1/${ex}.1
done
cd -

%check
# POD Coverage test fails due to lots of undocumented routines
TEST_POD_COVERAGE=0 make test

%files
%license COPYING
%doc README ChangeLog
# Adding examples introduces additional deps, but these are all satisfied by
# perl, perl-MIME-tools, and perl-MailTools, which are all deps anyway.
%doc examples/
%{perl_vendorlib}/MIME/
%{_bindir}/mimedump
%{_bindir}/mimeencode
%{_bindir}/mimeexplode
%{_bindir}/mimepostcard
%{_bindir}/mimesend
%{_mandir}/man1/mimedump.1*
%{_mandir}/man1/mimeencode.1*
%{_mandir}/man1/mimeexplode.1*
%{_mandir}/man1/mimepostcard.1*
%{_mandir}/man1/mimesend.1*
%{_mandir}/man3/MIME::Body.3*
%{_mandir}/man3/MIME::Decoder.3*
%{_mandir}/man3/MIME::Decoder::Base64.3*
%{_mandir}/man3/MIME::Decoder::BinHex.3*
%{_mandir}/man3/MIME::Decoder::Binary.3*
%{_mandir}/man3/MIME::Decoder::Gzip64.3*
%{_mandir}/man3/MIME::Decoder::NBit.3*
%{_mandir}/man3/MIME::Decoder::QuotedPrint.3*
%{_mandir}/man3/MIME::Decoder::UU.3*
%{_mandir}/man3/MIME::Entity.3*
%{_mandir}/man3/MIME::Field::ConTraEnc.3*
%{_mandir}/man3/MIME::Field::ContDisp.3*
%{_mandir}/man3/MIME::Field::ContType.3*
%{_mandir}/man3/MIME::Field::ParamVal.3*
%{_mandir}/man3/MIME::Head.3*
%{_mandir}/man3/MIME::Parser.3*
%{_mandir}/man3/MIME::Parser::Filer.3*
%{_mandir}/man3/MIME::Parser::Reader.3*
%{_mandir}/man3/MIME::Parser::Results.3*
%{_mandir}/man3/MIME::Tools.3*
%{_mandir}/man3/MIME::WordDecoder.3*
%{_mandir}/man3/MIME::Words.3*

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 5.515-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 5.515-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.515-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Apr 26 2024 Paul Howarth <paul@city-fan.org> - 5.515-1
- Update to 5.515
  -  Fix the "version" setting in META.yml (no functional changes)

* Wed Feb  7 2024 Paul Howarth <paul@city-fan.org> - 5.514-1
- Update to 5.514
  - Move the guts of the ambiguous_content method to MIME::Head
  - Add MIME::Entity->ambiguous_content that returns true if this entity or
    any of its parts, recursively, has a MIME::Head whose ambiguous_content
    method returns true
  - Keep MIME::Parser->ambiguous_content as a cached version of the most
    recently parsed $entity->ambiguous_content
  - Add some missing files to MANIFEST

* Fri Jan 26 2024 Paul Howarth <paul@city-fan.org> - 5.513-1
- Update to 5.513
  - Add MIME::Parser->ambiguous_content to indicate one of several types of
    ambiguous MIME content that could be security risks
  - Add the '@duplicate_parameters' pseudo-parameter to let caller detect
    duplicate MIME parameters on a MIME header

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.512-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.512-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Jan  9 2024 Paul Howarth <paul@city-fan.org> - 5.512-1
- Update to 5.512
  - Use much larger chunk sizes for Base-64 encoding, which reduces both
    encoding time and space overhead (CPAN RT#128400, CPAN RT#130110)

* Wed Jan  3 2024 Paul Howarth <paul@city-fan.org> - 5.511-1
- Update to 5.511
  - Silence a warning if used with a development version of MIME::QuotedPrint
    (CPAN RT#149225, CPAN RT#150118)

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 5.510-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 5.510-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 5.510-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jul  7 2022 Paul Howarth <paul@city-fan.org> - 5.510-1
- Update to 5.510
  - Update author contact info
  - Make code work in taint mode
  - Clarify MIME::Entity documentation
- Use %%license unconditionally

* Wed Jun 01 2022 Jitka Plesnikova <jplesnik@redhat.com> - 5.509-18
- Perl 5.36 rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 5.509-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 5.509-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 5.509-15
- Perl 5.34 rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 5.509-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.509-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 5.509-12
- Perl 5.32 rebuild

* Tue Mar 10 2020 Paul Howarth <paul@city-fan.org> - 5.509-11
- Modernize spec
  - Drop bundled modules and depend on them instead
  - Use %%{make_build} and %%{make_install}

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.509-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Aug 27 2019 Paul Howarth <paul@city-fan.org> - 5.509-9
- Use an author-independent source URL

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 5.509-8
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5.509-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5.509-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 5.509-5
- Perl 5.28 rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5.509-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.509-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jun 05 2017 Jitka Plesnikova <jplesnik@redhat.com> - 5.509-2
- Perl 5.26 rebuild

* Thu Apr  6 2017 Paul Howarth <paul@city-fan.org> - 5.509-1
- Update to 5.509
  - Makefile.PL failed with no '.' in @INC (CPAN RT#120871)
  - Test t/Ref.t failed on Windows install (CPAN RT#118262)
  - MIME::Parser::parse_data() should check what it gets back (CPAN RT#119166)
  - Allow \r\n to be used as line-end delimiter when outputting MIME message
    (CPAN RT#119568)
- Drop EL-5 support (should have happened years ago, dependencies not available)
  - Drop BuildRoot: and Group: tags
  - Drop explicit buildroot cleaning in %%install section
  - Drop explicit %%clean section

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.508-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Aug 30 2016 Paul Howarth <paul@city-fan.org> - 5.508-1
- Update to 5.508
  - Fix test broken by Perl update (CPAN RT#113887)
- BR: perl-generators

* Mon May 16 2016 Jitka Plesnikova <jplesnik@redhat.com> - 5.507-4
- Perl 5.24 rebuild

* Fri Apr 22 2016 Paul Howarth <paul@city-fan.org> - 5.507-3
- Work around behaviour change in MailTools > 2.14 (#1329082, CPAN RT#113887)
- Simplify find command using -delete

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 5.507-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Sep 30 2015 Paul Howarth <paul@city-fan.org> - 5.507-1
- Update to 5.507
  - Fix parsing bug (CPAN RT#105455)
  - Fix typo that broke MIME::Body::incore->open() on Perl 5.20

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.506-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 5.506-2
- Perl 5.22 rebuild

* Thu Apr 23 2015 Paul Howarth <paul@city-fan.org> - 5.506-1
- Update to 5.506
  - Update maintainer's name to "Dianne Skoll"
- Use %%license where possible
- Update UTF8 patch
- Classify buildreqs by usage

* Thu Aug 28 2014 Jitka Plesnikova <jplesnik@redhat.com> - 5.505-3
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.505-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Nov 14 2013 Paul Howarth <paul@city-fan.org> - 5.505-1
- Update to 5.505
  - Fix documentation typos (CPAN RT#80473, CPAN RT#87783)
  - Fix broken test (CPAN RT#84668)
  - Don't run Kwalitee tests unless author or release tests are enabled
    (CPAN RT#87094)
  - Fix bug in header parsing that would fail to parse a header like:
    Content-Type: ; name="malware.zip"

* Fri Jul 26 2013 Petr Pisar <ppisar@redhat.com> - 5.504-4
- Perl 5.18 rebuild

* Thu Jul 25 2013 Paul Howarth <paul@city-fan.org> - 5.504-3
- Don't try to run the kwalitee test, as it fails a couple of kwalitee metrics
  with Test::Kwalitee 1.09

* Thu Jan 31 2013 Paul Howarth <paul@city-fan.org> - 5.504-1
- Update to 5.504
  - Fix encoding of MIME parameters that contain a quoted string: "like \"this"
    (CPAN RT#80433)
  - Suppress useless warnings from tests (CPAN RT#80679)
  - Fix long-standing bug in encode_mimewords that can break multi-byte
    encodings such as UTF-8 (CPAN RT#5462)

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.503-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jun 23 2012 Petr Pisar <ppisar@redhat.com> - 5.503-2
- Perl 5.16 rebuild

* Fri Jun  8 2012 Paul Howarth <paul@city-fan.org> - 5.503-1
- Update to 5.503
  - Avoid inappropriately untainting data (CPAN RT#67119)
  - Localise $\ to avoid parsing problems if it's set elsewhere (CPAN RT#71041)
  - Improve exorcising of filenames (CPAN RT#71677)
  - Fix potential race condition in t/Smtpsend.t (CPAN RT#68879)
  - Allow native I/O on File::Handle objects (CPAN RT#72538)
  - Add "recommends Convert::BinHex" clause to Makefile.PL (CPAN RT#72223)
  - Add module_name to Makefile.PL (CPAN RT#77138)
  - Fix "Uninitialized value" warning (CPAN RT#77190)
  - Don't run t/Smtpsend.t on systems that lack fork() (CPAN RT#77351)
  - Add "use strict" everywhere (CPAN RT#77582)
- Don't need to remove empty directories from the buildroot
- Drop %%defattr, redundant since rpm 4.4
- Require perl(Convert::BinHex) to support BinHex-encoded mail

* Thu Jan 12 2012 Paul Howarth <paul@city-fan.org> - 5.502-5
- Fedora 17 mass rebuild

* Wed Oct 26 2011 Paul Howarth <paul@city-fan.org> - 5.502-4
- Use patch rather than scripted iconv to fix character encoding
- Use DESTDIR rather than PERL_INSTALL_ROOT
- Nobody else likes macros for commands
- Use %%{_fixperms} macro rather than our own chmod incantation
- Explicitly specify all manpages in %%files list
- The Makefile.PL --skipdeps option is no longer needed

* Wed Oct 26 2011 Marcela Mašláňová <mmaslano@redhat.com> - 5.502-3
- Own only man pages of this packages (conflict with Perl package)

* Wed Jul 20 2011 Petr Sabata <contyk@redhat.com> - 5.502-2
- Perl mass rebuild

* Tue Mar  8 2011 Paul Howarth <paul@city-fan.org> - 5.502-1
- Update to 5.502
  - Fix parsing bug (CPAN RT#66025)
  - Fix typo (CPAN RT#65387)
  - Fix unit tests on Perl 5.8.x (CPAN RT#66188)
  - Fix unit test failure on Win32 (CPAN RT#66286)

* Thu Feb 17 2011 Paul Howarth <paul@city-fan.org> - 5.501-1
- Update to 5.501
  - Add build_requires 'Test::Deep'; to Makefile (CPAN RT#64659)
  - Fix spelling errors (CPAN RT#64610)
  - Fix double-decoding bug when decoding RFC-2231-encoded parameters
    (CPAN RT#65162)
  - Fix inappropriate inclusion of CR characters in parsed headers
    (CPAN RT#65681)
  - Document that MIME::WordDecoder is mostly deprecated
  - Document that MIME::Head->get(...) can include a trailing newline
  - Increase buffer size from 2kB to 8kB in MIME::Entity and MIME::Body
    (part of CPAN RT#65162)
- This release by DSKOLL -> update source URL

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.500-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jan 10 2011 Paul Howarth <paul@city-fan.org> - 5.500-1
- Update to 5.500
  - cleanup: IO-Stringy is no longer used
  - cleanup: remove auto_install from Makefile.PL
  - RT#22684: fix deadlock in filter() when invoking external programs
    such as gzip
  - RT#60931: if preamble is empty, make sure it's still empty after
    round-tripping through MIME::Entity
  - RT#63739: properly decode RFC2231 encodings in attachment filenames
- New build requirements:
  - perl(IO::Handle)
  - perl(Mail::Field) >= 1.05
  - perl(Mail::Header) >= 1.01
  - perl(Mail::Internet) >= 1.0203
  - perl(Test::Deep)
- Drop buildreq perl(IO::Stringy)

* Mon Dec 20 2010 Marcela Maslanova <mmaslano@redhat.com> - 5.428-3
- Rebuild to fix problems with vendorarch/lib (#661697)

* Mon May 03 2010 Marcela Maslanova <mmaslano@redhat.com> - 5.428-2
- Mass rebuild with perl-5.12.0

* Thu Apr 22 2010 Paul Howarth <paul@city-fan.org> - 5.428-1
- Update to 5.428
  - RT#56764: build release with a newer Module::Install
  - RT#52924: ensure we add <> around Content-id data
  - RT#48036: make mimesend example script a bit more useful
  - RT#43439: fix for parsing of doubled ; in multipart headers
  - RT#41632: if RFC-2231 and non-RFC-2231 params present, use only RFC-2231
  - RT#40715: reference Encode::MIME::Header in docs
  - RT#39985: correct POD typos
  - Only bind to localhost in smtpsend test, not all interfaces
- Specify --skipdeps in Makefile.PL invocation to prevent use of CPAN module
- Buildreq perl(Test::Kwalitee) for additional test coverage
- Tidy up %%description and other largely cosmetic spec changes

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 5.427-4
- Rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.427-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.427-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Jul  1 2008 Paul Howarth <paul@city-fan.org> 5.427-1
- Update to 5.427
- Require and BuildRequire perl(IO::File) >= 1.13

* Wed Mar 19 2008 Paul Howarth <paul@city-fan.org> 5.426-1
- Update to 5.426
- Now require File::Temp >= 0.18
- Add POD tests, coverage disabled because of lack of coverage from upstream

* Tue Mar 11 2008 Paul Howarth <paul@city-fan.org> 5.425-1
- Update to 5.425
- Add note about File::Temp requirement
- New upstream maintainer -> updated URL for source
- Given that this package will not build on old distributions, don't cater
  for handling old versions of MIME::QuotedPrint in %%check and buildreq
  perl(MIME::Base64) >= 3.03
- Buildreq perl(File::Path) >= 1, perl(File::Spec) >= 0.6, and
  perl(IO::Stringy) >= 2.110
- Only include README as %%doc, not README*
- Dispense with provides filter, no longer needed

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 5.420-6
- Rebuild for perl 5.10 (again)

* Sun Jan 20 2008 Tom "spot" Callaway <tcallawa@redhat.com> 5.420-5
- rebuild for new perl

* Mon Aug 13 2007 Paul Howarth <paul@city-fan.org> 5.420-4
- Clarify license as GPL v1 or later, or Artistic (same as perl)
- Add buildreq perl(Test::More)

* Tue Apr 17 2007 Paul Howarth <paul@city-fan.org> 5.420-3
- Buildrequire perl(ExtUtils::MakeMaker)
- Fix argument order for find with -depth

* Tue Aug  8 2006 Paul Howarth <paul@city-fan.org> 5.420-2
- Install the more useful examples in %%{_bindir} (#201691)

* Wed Apr 19 2006 Paul Howarth <paul@city-fan.org> - 5.420-1
- 5.420
- Cosmetic changes reflecting new maintainer's preferences
- Examples remain executable since they don't introduce new dependencies
- Simplify provides filter

* Mon Jan 16 2006 Ville Skyttä <ville.skytta at iki.fi> - 5.419-1
- 5.419.
- Don't provide perl(main).

* Tue Oct  4 2005 Paul Howarth <paul@city-fan.org> - 5.418-2
- License is same as perl (GPL or Artistic), not just Artistic

* Mon Oct  3 2005 Ville Skyttä <ville.skytta at iki.fi> - 5.418-1
- 5.418.
- Cosmetic specfile cleanups.

* Wed Apr  6 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 5.417-2
- rebuilt

* Sat Jan 22 2005 Ville Skyttä <ville.skytta at iki.fi> - 0:5.417-1
- Update to 5.417.

* Wed Jan  5 2005 Ville Skyttä <ville.skytta at iki.fi> - 0:5.416-0.fdr.1
- Update to 5.416.

* Thu Oct 28 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:5.415-0.fdr.1
- Update to 5.415.

* Thu Oct  7 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:5.414-0.fdr.1
- Update to 5.414.

* Wed Sep 15 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:5.413-0.fdr.1
- Update to 5.413, includes the mimedefang patches.
- Bring up to date with current fedora.us Perl spec template.

* Sat Feb  7 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:5.411-0.fdr.6.a
- Install into vendor dirs.
- BuildRequire perl-MailTools (bug 373).

* Sat Aug 16 2003 Dams <anvil[AT]livna.org> 0:5.411-0.fdr.5.a
- Hopefully fixed BuildRequires (for make test)
- rm-ing perllocal.pod instead of excluding it

* Sat Jul 12 2003 Dams <anvil[AT]livna.org> 0:5.411-0.fdr.4.a
- Package is now noarch

* Fri Jul 11 2003 Dams <anvil[AT]livna.org> 0:5.411-0.fdr.3.a
- Changed Group tag value
- make test in build section
- Added missing directory

* Wed Jun 25 2003 Dams <anvil[AT]livna.org> 0:5.411-0.fdr.2.a
- Now using roaringpenguin tarball

* Sun Jun 15 2003 Dams <anvil[AT]livna.org>
- Initial build.
