# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:		perl-List-MoreUtils
Version:	0.430
Release:	14%{?dist}
Summary:	Provide the stuff missing in List::Util
# All code present in version 0.416: GPL-1.0-or-later OR Artistic-1.0-Perl
# All new code from version 0.417 onwards: Apache-2.0
License:	(GPL-1.0-or-later OR Artistic-1.0-Perl) AND Apache-2.0
URL:		https://metacpan.org/release/List-MoreUtils
Source0:	https://cpan.metacpan.org/modules/by-module/List/List-MoreUtils-%{version}.tar.gz
BuildArch:	noarch
# Module Build
BuildRequires:	coreutils
BuildRequires:	findutils
BuildRequires:	make
BuildRequires:	perl-generators
BuildRequires:	perl-interpreter
BuildRequires:	perl(base)
BuildRequires:	perl(Config)
BuildRequires:	perl(constant)
BuildRequires:	perl(ExtUtils::MakeMaker) >= 6.75
BuildRequires:	perl(File::Basename)
BuildRequires:	perl(File::Spec)
BuildRequires:	perl(File::Temp)
BuildRequires:	perl(IO::File)
BuildRequires:	perl(IO::Handle)
BuildRequires:	perl(lib)
BuildRequires:	perl(PerlIO)
BuildRequires:	perl(Scalar::Util)
BuildRequires:	perl(Text::ParseWords)
# Module Runtime
BuildRequires:	perl(Carp)
BuildRequires:	perl(Exporter::Tiny) >= 0.038
BuildRequires:	perl(List::MoreUtils::XS) >= 0.430
BuildRequires:	perl(parent)
BuildRequires:	perl(strict)
BuildRequires:	perl(vars)
BuildRequires:	perl(warnings)
# Test Suite
BuildRequires:	perl(Exporter)
BuildRequires:	perl(List::Util)
BuildRequires:	perl(Math::Trig)
BuildRequires:	perl(overload)
BuildRequires:	perl(POSIX)
BuildRequires:	perl(Storable)
BuildRequires:	perl(Test::Builder::Module)
BuildRequires:	perl(Test::More) >= 0.96
BuildRequires:	perl(Tie::Array)
# Optional Tests
%if ! ( 0%{?rhel} )
BuildRequires:	perl(Test::LeakTrace)
%endif
# Dependencies
Requires:	perl(Carp)
Requires:	perl(List::MoreUtils::XS) >= 0.430

%description
List::MoreUtils provides some trivial but commonly needed functionality
on lists that is not going to go into List::Util.

%prep
%setup -q -n List-MoreUtils-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PERLLOCAL=1 NO_PACKLIST=1
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}
%{_fixperms} -c %{buildroot}

%check
make test

%files
%license ARTISTIC-1.0 GPL-1 LICENSE
%doc Changes README.md
%{perl_vendorlib}/List/
%{_mandir}/man3/List::MoreUtils.3*
%{_mandir}/man3/List::MoreUtils::Contributing.3*
%{_mandir}/man3/List::MoreUtils::PP.3*

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.430-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.430-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.430-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.430-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.430-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.430-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.430-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.430-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue May 31 2022 Jitka Plesnikova <jplesnik@redhat.com> - 0.430-6
- Perl 5.36 rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.430-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.430-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 0.430-3
- Perl 5.34 rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.430-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Oct 21 2020 Paul Howarth <paul@city-fan.org> - 0.430-1
- Update to 0.430
  - Fix failing installation in parallel make (GH#38)
  - Infrastructure improvements and tooling updates, lots of author tests with
    corresponding fixes added
  - Added slide and slideatatime functions
  - Documentation fixes (GH#21, GH#33, GH#34, CPAN RT#126029, CPAN RT#132043,
    CPAN RT#132940)
  - Bump List::MoreUtils::XS requirement to 0.430
- Use author-independent source URL

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.428-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 0.428-9
- Perl 5.32 rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.428-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.428-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.428-6
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.428-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.428-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jun 29 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.428-3
- Perl 5.28 rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.428-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Dec 12 2017 Paul Howarth <paul@city-fan.org> - 0.428-1
- Update to 0.428
  - Fix GH#22 (Upgrading from LMU 0.416 to split XS/PP version will fail),
    this time hopefully the right way (CPAN RT#123310)
  - Fix GH#29 (pairwise() PP implementation add tail undefs if array sizes
    differ)

* Fri Oct 13 2017 Paul Howarth <paul@city-fan.org> - 0.426-1
- Update to 0.426
  - Fix broken arrayify prototype
  - Revert removal of old List::MoreUtils::XS parts
  - Re-introduce Config::AutoConf (CPAN RT#122875)
  - Bump required version of List::MoreUtils::XS to 0.426, if XS is available

* Thu Sep  7 2017 Paul Howarth <paul@city-fan.org> - 0.425-1
- Update to 0.425
  - Makefile.PL: modify PREREQ_PM instead of recommend dynamically

* Tue Aug 22 2017 Paul Howarth <paul@city-fan.org> - 0.423-1
- Update to 0.423
  - Sync version with List::MoreUtils::XS
  - Add some new functions: qsort (XS only), binsert, bremove, listcmp,
    arrayify (CPAN RT#17230), samples (CPAN RT#77562), minmaxstr
    (CPAN RT#106401), lower_bound, upper_bound, equal_range, frequencies
    occurrences, mode (CPAN RT#91991), zip6 (CPAN RT#42921), reduce_0,
    reduce_1, reduce_u
  - Add examples for binsert/bremove (LMU::XS GH#1)
  - Improve tests
  - Make List::MoreUtils::XS independent from List::MoreUtils
  - Improve Makefile.PL regarding some build artifacts
  - Update tests to latest List::MoreUtils::XS
  - Recommend List::MoreUtils::XS 0.423
- BR:/R: LMU::XS ≥ 0.423 as there is no longer a bootstrapping issue

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.419-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jun 05 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.419-2
- Perl 5.26 rebuild

* Fri Apr  7 2017 Paul Howarth <paul@city-fan.org> - 0.419-1
- Update to 0.419
  - Makefile.PL failed due to unescaped paths interpolated in regex pattern
    (CPAN RT#120799)

* Thu Mar 30 2017 Paul Howarth <paul@city-fan.org> - 0.418-1
- Update to 0.418
  - Divorce List::MoreUtils and List::MoreUtils::XS
  - Change license to Apache 2.0 to avoid code stealing without credits
  - Don't support Perl 5.6 out of the box any more
  - Fix CPAN RT#120235: uniq examples are incorrect
  - Remove things that will be never done from TODO list (GH#18)
  - Spelling fixes
- Package is now noarch

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.416-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Jul  6 2016 Paul Howarth <paul@city-fan.org> - 0.416-1
- Update to 0.416
  - Change the way how the XS part is loaded as a result of CPAN RT#115808
  - Fix some spelling errors (CPAN RT#115807)
  - Requires XSLoader 0.22
- Package newly-shipped license files
- Drop now-redundant provides patch

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.415-2
- Perl 5.24 rebuild

* Mon May  2 2016 Paul Howarth <paul@city-fan.org> - 0.415-1
- Update to 0.415
  - Fix CPAN RT#75727: After's XS implementation call XSRETURN(-1) when it
    doesn't find an element
  - Fix CPAN RT#113117: XS's minmax() sometimes return undef (perl ≥ 5.20)
  - Explicit test for thesis in CPAN RT#110998: XS implementation of pairwise
    fails with memory allocation error when there are more return values than
    in original lists - thesis is proven wrong
  - Efficiency improvements
  - Improve some tests to get clearer reports
  - Distinguish between "Makefile.PL finds a .git directory" and
    "Makefile.PL runs in maintainer mode"
- Simplify find command using -delete

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.413-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.413-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 13 2015 Paul Howarth <paul@city-fan.org> - 0.413-1
- Update to 0.413
  - Fix compiling in c++ mode (deprecated, but some people seem to require it)
    (CPAN RT#104690)

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.412-2
- Perl 5.22 rebuild

* Wed May 20 2015 Paul Howarth <paul@city-fan.org> - 0.412-1
- Update to 0.412
  - Move generation of test endpoints to author stage as requested per issue/#9
  - Add a rough guide for contributors
  - Fix CPAN RT#103251 to avoid removing bundled stuff by accident
  - Fix compilation errors under cl

* Mon Mar 30 2015 Paul Howarth <paul@city-fan.org> - 0.410-1
- Update to 0.410
  - Fix CPAN RT#102885: uniq bug broke tied array
  - Fix issue/8: Macros introduced in dfd851147f cause problems with MSVC
  - Update ppport.h from 3.25 to 3.31
  - Fix multiple mg_get can break weird ties
  - Fix test run using PERL5OPT=d:Confess
  - Use base instead of parent, 'cause parent isn't bundled before 5.10.1
  - Update bundled bootstrap modules
    - Data::Tumbler to 0.010
    - Test::WriteVariants to 0.012
    - Config::AutoConf to 0.311
  - Fix spelling (and add stop-words for names etc. in author tests)

* Wed Mar 18 2015 Paul Howarth <paul@city-fan.org> - 0.408-1
- Update to 0.408
  - Fix CPAN RT#102840: uniq broken for call-by-function-return
  - Fix CPAN RT#102853: hent_val accesses
  - Fix CPAN RT#102833: Compilation error with perl 5.21.7+
  - Fix regex for CPAN RT#44518 test

* Wed Mar 18 2015 Paul Howarth <paul@city-fan.org> - 0.407-1
- Update to 0.407
  - Added one(), onlyidx(), onlyval() (CPAN RT#73134) and onlyres()
  - Improve XS maintainability
  - Document how uniq/distinct deal with undef (CPAN RT#49800)
  - Add bsearchidx to satisfy CPAN RT#63470
  - Add singleton to satisfy CPAN RT#94382
  - Fix CPAN RT#82039 - uniq changes the type of its arguments
  - Fix CPAN RT#44518 again

* Tue Mar  3 2015 Paul Howarth <paul@city-fan.org> - 0.406-1
- Update to 0.406
  - Add new functions firstres and lastres in addition to firstidx, lastidx,
    firstval and lastval
  - Regenerate MANIFEST to bundle README.md

* Sat Feb 14 2015 Paul Howarth <paul@city-fan.org> - 0.405-1
- Update to 0.405
  - Fix CPAN RT#78527 - first_val/last_val in documentation
  - Fix CPAN RT#102055 - ExtUtils::MakeMaker required version absurdly high
  - Fix compiler issue for older/ansi-c89 compilers
  - Remove local compat workarounds in favour for ppport.h

* Thu Jan 29 2015 Paul Howarth <paul@city-fan.org> - 0.404-1
- Update to 0.404
  - Fix ancient toolchains (PREREQ_PM & Co. set appropriately)
  - Bump version required of Test::More to 0.96 (#toolchain calls it a "sane
    subset")
  - Fix some meta-data #toolchain pointed out

* Tue Jan 27 2015 Paul Howarth <paul@city-fan.org> - 0.403-1
- Update to 0.403
  - Remove most recent stable perl recommendation from meta to work around
    misbehaving CPAN clients blocking update
  - Update copyright date
  - Ensure AUTHOR is a string on older toolchains

* Wed Jan  7 2015 Paul Howarth <paul@city-fan.org> - 0.402-1
- Update to 0.402 (significant and slightly incompatible update - see Changes)
- This release by REHSACK → update source URL
- Classify buildreqs by usage
- Modernize spec as this isn't going to anywhere older than F-22

* Sun Sep 07 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.33-15
- Perl 5.20 re-rebuild of bootstrapped packages

* Fri Aug 29 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.33-14
- Perl 5.20 rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.33-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.33-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Aug 14 2013 Jitka Plesnikova <jplesnik@redhat.com> - 0.33-11
- Perl 5.18 re-rebuild of bootstrapped packages

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.33-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jul 26 2013 Petr Pisar <ppisar@redhat.com> - 0.33-9
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.33-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Oct 17 2012 Paul Howarth <paul@city-fan.org> - 0.33-7
- BR:/R: perl(Carp)
- BR: perl(constant), perl(Exporter) and perl(ExtUtils::CBuilder)
- Add commentary regarding non-use of Test::LeakTrace for EL-7 builds
- Use Test::LeakTrace for EL-5 builds
- Drop support for EL-4 builds since it was EOL-ed ages ago
- Drop %%defattr, redundant since rpm 4.4
- Don't need to remove empty directories from the buildroot
- Remove more command macros

* Mon Oct 15 2012 Petr Pisar <ppisar@redhat.com> - 0.33-6
- Do not build-require Test::LeakTrace on RHEL 7

* Fri Jul 27 2012 Tom Callaway <spot@fedoraproject.org> - 0.33-5
- Add epel filtering mechanism

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.33-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 10 2012 Petr Pisar <ppisar@redhat.com> - 0.33-3
- Perl 5.16 re-rebuild of bootstrapped packages

* Tue Jun 19 2012 Petr Pisar <ppisar@redhat.com> - 0.33-2
- Perl 5.16 rebuild

* Tue Jan 24 2012 Paul Howarth <paul@city-fan.org> - 0.33-1
- Update to 0.33
  - Updated can_xs to fix a bug in it
- Reinstate compatibility with old distributions like EL-5
- Drop Test::More version requirement to 0.42
- BR: perl(ExtUtils::MakeMaker)
- BR: perl(Test::LeakTrace) except on EL-4/EL-5 where it's not available
- BR: perl(Pod::Simple), perl(Test::CPAN::Meta), perl(Test::MinimumVersion)
  (if we're not bootstrapping) and perl(Test::Pod), and run the developer tests
  too
- Don't use macros for commands
- Use %%{_fixperms} macro rather than our own chmod incantation
- Make %%files list more specific
- Use tabs

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.32-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jul 18 2011 Petr Sabata <contyk@redhat.com> - 0.32-3
- Perl mass rebuild

* Tue Jul 12 2011 Tom Callaway <spot@fedoraproject.org> - 0.32-2
- Rebuild to fix broken rawhide deps

* Sat Jul 02 2011 Iain Arnell <iarnell@gmail.com> - 0.32-1
- Update to latest upstream version

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.30-3
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.30-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jan 03 2011 Iain Arnell <iarnell@gmail.com> - 0.30-1
- Update to latest upstream version
- Clean up spec for modern rpmbuild
- Use perl_default_filter
- Remove unnecessary buildrequires

* Mon Dec 20 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.22-12
- Rebuild to fix problems with vendorarch/lib (#661697)

* Mon May 03 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.22-11
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.22-10
- Rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.22-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.22-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.22-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Feb 28 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.22-6
- Rebuild normally, second pass

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.22-5
- Rebuild for perl 5.10 (again), tests disabled for first pass

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.22-4
- Autorebuild for GCC 4.3

* Mon Jan 14 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.22-3
- Rebuild normally, second pass

* Fri Jan 11 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.22-2.1
- Rebuild for new perl, first pass, disable TPC and tests

* Sun Sep 10 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.22-2
- Rebuild for FC6

* Mon Jul  3 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.22-1
- Update to 0.22

* Mon Jun 19 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.21-1
- Update to 0.21

* Sat Jun 10 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.20-1
- Update to 0.20

* Sat Apr 22 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.19-1
- First build
