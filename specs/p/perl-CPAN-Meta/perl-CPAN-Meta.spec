# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           perl-CPAN-Meta
Summary:        Distribution metadata for a CPAN dist
Version:        2.150010
Release:        520%{?dist}
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/CPAN-Meta
Source0:        https://cpan.metacpan.org/authors/id/D/DA/DAGOLDEN/CPAN-Meta-%{version}.tar.gz
BuildArch:      noarch
# Build
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(Config)
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.17
# Module
BuildRequires:  perl(Carp)
BuildRequires:  perl(CPAN::Meta::Requirements) >= 2.121
BuildRequires:  perl(CPAN::Meta::YAML) >= 0.011
BuildRequires:  perl(Encode)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(JSON::PP) >= 2.27300
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(strict)
BuildRequires:  perl(version) >= 0.88
BuildRequires:  perl(warnings)
# Main test suite
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(File::Basename)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(File::Spec::Functions)
BuildRequires:  perl(File::Temp) >= 0.20
BuildRequires:  perl(IO::Dir)
BuildRequires:  perl(lib)
BuildRequires:  perl(overload)
BuildRequires:  perl(Storable)
BuildRequires:  perl(Test::More) >= 0.88
BuildRequires:  perl(utf8)
BuildRequires:  perl(vars)
# Runtime
Requires:       perl(CPAN::Meta::YAML) >= 0.011
Requires:       perl(Encode)
Requires:       perl(JSON::PP) >= 2.27300
Requires:       perl(version) >= 0.88

# Parse-CPAN-Meta merged into CPAN-Meta 2.150008
# Provide not added in order to avoid either epoch bump or self-obsoletion
Obsoletes:      perl-Parse-CPAN-Meta < 1:1.4422-2

# Avoid doc-file dependencies
%{?perl_default_filter}

# Remove under-specified dependencies
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\(CPAN::Meta::Converter\\)$
%global __requires_exclude %{__requires_exclude}|^perl\\(CPAN::Meta::Requirements\\)$

%description
Software distributions released to the CPAN include a META.json or, for older
distributions, META.yml, which describes the distribution, its contents, and
the requirements for building and installing the distribution. The data
structure stored in the META.json file is described in CPAN::Meta::Spec.

%prep
%setup -q -n CPAN-Meta-%{version}

# silence rpmlint warnings
perl -MConfig -pi -e 's,^#!.*perl,$Config{startperl},' t/*.t

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot} UNINST=0
find %{buildroot} -type f -name .packlist -delete
%{_fixperms} %{buildroot}

%check
make test

%files
%license LICENSE
%doc Changes CONTRIBUTING.mkdn history README Todo t/
%{perl_vendorlib}/CPAN/
%{perl_vendorlib}/Parse/
%{_mandir}/man3/CPAN::Meta.3*
%{_mandir}/man3/CPAN::Meta::Converter.3*
%{_mandir}/man3/CPAN::Meta::Feature.3*
%{_mandir}/man3/CPAN::Meta::History.3*
%{_mandir}/man3/CPAN::Meta::History::Meta_1_0.3*
%{_mandir}/man3/CPAN::Meta::History::Meta_1_1.3*
%{_mandir}/man3/CPAN::Meta::History::Meta_1_2.3*
%{_mandir}/man3/CPAN::Meta::History::Meta_1_3.3*
%{_mandir}/man3/CPAN::Meta::History::Meta_1_4.3*
%{_mandir}/man3/CPAN::Meta::Merge.3*
%{_mandir}/man3/CPAN::Meta::Prereqs.3*
%{_mandir}/man3/CPAN::Meta::Spec.3*
%{_mandir}/man3/CPAN::Meta::Validator.3*
%{_mandir}/man3/Parse::CPAN::Meta.3*

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.150010-520
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jul 07 2025 Jitka Plesnikova <jplesnik@redhat.com> - 2.150010-519
- Increase release to favour standalone package

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.150010-512
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.150010-511
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jun 10 2024 Jitka Plesnikova <jplesnik@redhat.com> - 2.150010-510
- Increase release to favour standalone package

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.150010-502
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.150010-501
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.150010-500
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jul 11 2023 Jitka Plesnikova <jplesnik@redhat.com> - 2.150010-499
- Increase release to favour standalone package

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.150010-490
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.150010-489
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon May 30 2022 Jitka Plesnikova <jplesnik@redhat.com> - 2.150010-488
- Increase release to favour standalone package

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.150010-479
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.150010-478
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 2.150010-477
- Increase release to favour standalone package

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.150010-458
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.150010-457
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jun 22 2020 Jitka Plesnikova <jplesnik@redhat.com> - 2.150010-456
- Increase release to favour standalone package

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.150010-440
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.150010-439
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu May 30 2019 Jitka Plesnikova <jplesnik@redhat.com> - 2.150010-438
- Increase release to favour standalone package

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.150010-418
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.150010-417
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jun 27 2018 Jitka Plesnikova <jplesnik@redhat.com> - 2.150010-416
- Increase release to favour standalone package

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.150010-396
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Dec 18 2017 Petr Pisar <ppisar@redhat.com> - 2.150010-395
- Rewrite shell bang according to used perl

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.150010-394
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Jun 03 2017 Jitka Plesnikova <jplesnik@redhat.com> - 2.150010-393
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.150010-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Aug 19 2016 Paul Howarth <paul@city-fan.org> - 2.150010-1
- Update to 2.150010
  Added:
  - Merged Parse::CPAN::Meta 1.4420 into this distribution
  Fixed:
  - CPAN::Meta::Prereqs now fully accepts phases and types starting with 'x_';
    new 'phases' and 'types_in' interfaces have been added
  - No longer relies on JSON backend for data structure cloning; this is much
    faster than using JSON::PP
  - The cloning routine would raise an error on expected types when it
    previously would stringify; the old behavior is restored
  - Fixed used of Encode in Parse::CPAN::Meta::load_json_string (cherry picked
    from Parse::CPAN::Meta 1.4422)
  - Added "use warnings" to Parse::CPAN::Meta
  - The YAML and JSON backend variables are ignored when building/testing the
    perl core itself, where non-core backends are not yet installed
  Tests:
  - The 'extra_mappings' feature for meta merging is now tested and documented
  - During tests, delete new environment variables added by Parse::CPAN::Meta
    1.4418
  Spec:
  - Clarifies acceptable values for booleans
  - Cleaned up text and links of historical specs
- Obsolete old perl-Parse-CPAN-Meta package
- Simplify find command using -delete

* Sat May 14 2016 Jitka Plesnikova <jplesnik@redhat.com> - 2.150005-365
- Increase release to favour standalone package

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.150005-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.150005-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 13 2015 Paul Howarth <paul@city-fan.org> - 2.150005-1
- Update to 2.150005
  - Metadata merging now does deep hash merging as long as keys don't conflict
  - Serialized CPAN::Meta objects now include a x_serialization_backend entry
  - Declared extra developer prereq
  - Added test for 'x_deprecated' field in "provides"
  - Noted explicitly that historical META spec files are licensed under the
    same terms as Perl
  - Changed some test data from UTF-8 to ASCII

* Thu Jun 04 2015 Jitka Plesnikova <jplesnik@redhat.com> - 2.150001-345
- Increase release to favour standalone package

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 2.150001-2
- Perl 5.22 rebuild

* Tue Mar 10 2015 Paul Howarth <paul@city-fan.org> - 2.150001-1
- Update to 2.150001
  - Include allowed values for license field in 1.x historic licenses rather
    than linking to Module::Build
  - Documented when fragment merging became available

* Tue Jan 13 2015 Petr Pisar <ppisar@redhat.com> - 2.143240-2
- Correct dependencies

* Thu Nov 20 2014 Paul Howarth <paul@city-fan.org> - 2.143240-1
- Update to 2.143240
  - Give correct path in nested merges such as resources
  - Removed strings test that should have been removed when
    CPAN::Meta::Requirements was removed to a separate dist

* Tue Nov 11 2014 Petr Šabata <contyk@redhat.com> - 2.142690-1
 - Update to 2.142690
  - Fixed use of incorrect method in CPAN::Meta::Merge implementation
  - Clarified documentation that no_index is a list of exclusions, and that
    indexers should generally exclude 'inc', 'xt' and 't' as well
  - CPAN::Meta::History::Meta_1_0 through 1_4 are added as a permanent
    record of 1.x versions of the metaspec

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 2.142060-2
- Perl 5.20 rebuild

* Mon Jul 28 2014 Paul Howarth <paul@city-fan.org> - 2.142060-1
- Update to 2.142060
  - Added ability for CPAN::Meta::Converter to convert metadata fragments
    (incomplete portions of a metadata structure)
  - Optimized internal use of JSON for datastructure cloning
  - Removed dependency on List::Util 1.33
  - Clarified language around 'dynamic_config' in the Spec
  - Clarified use of 'file' for the 'provides' field in the Spec
  - CPAN::Meta::Merge is a new class for merging two possibly overlapping
    instances of metadata, which will accept both CPAN::Meta objects and
    (possibly incomplete) hashrefs of metadata
- Use %%license

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.140640-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Mar 26 2014 Paul Howarth <paul@city-fan.org> - 2.140640-1
- Update to 2.140640
  - Improved bad version handling during META conversion
  - When downgrading multiple licenses to version 1.x META formats, if all the
    licenses are open source, the downgraded license will be "open_source", not
    "unknown"
  - Added a 'load_string' method that guesses whether the string is YAML or
    JSON
- Drop obsoletes/provides for old tests sub-package
- Classify buildreqs by usage
- Package upstream's CONTRIBUTING file
- Make %%files list more explicit

* Fri Oct 11 2013 Paul Howarth <paul@city-fan.org> - 2.132830-1
- Update to 2.132830
  - Fixed incorrectly encoded META.yml
  - META validation used to allow a scalar value when a list (i.e. array
    reference) was required for a field; this has been tightened and
    validation will now fail if a scalar value is given
  - Installation on Perls < 5.12 will uninstall older versions installed
    due to being bundled with ExtUtils::MakeMaker
  - Updated Makefile.PL logic to support PERL_NO_HIGHLANDER
  - Dropped ExtUtils::MakeMaker configure_requires dependency to 6.17
  - CPAN::Meta::Prereqs now has a 'merged_requirements' method for combining
    requirements across multiple phases and types
  - Invalid 'meta-spec' is no longer a fatal error: instead, it will usually
    be treated as spec version "1.0" (prior to formalization of the meta-spec
    field); conversion has some heuristics for guessing a version depending on
    other fields if 'meta-spec' is missing or invalid
- Don't need to remove empty directories from the buildroot

* Thu Sep  5 2013 Paul Howarth <paul@city-fan.org> - 2.132140-1
- update to latest upstream version

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.120921-291
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul 15 2013 Petr Pisar <ppisar@redhat.com> - 2.120921-290
- Increase release to favour standalone package

* Fri Jul 12 2013 Petr Pisar <ppisar@redhat.com> - 2.120921-6
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.120921-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.120921-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 06 2012 Petr Pisar <ppisar@redhat.com> - 2.120921-3
- Perl 5.16 rebuild

* Fri Jun 01 2012 Petr Pisar <ppisar@redhat.com> - 2.120921-2
- Build-require Data::Dumper for tests

* Mon Apr 02 2012 Iain Arnell <iarnell@gmail.com> 2.120921-1
- update to latest upstream version

* Fri Mar 30 2012 Iain Arnell <iarnell@gmail.com> 2.120900-1
- update to latest upstream version

* Sun Mar 04 2012 Iain Arnell <iarnell@gmail.com> 2.120630-1
- update to latest upstream version

* Wed Feb 22 2012 Iain Arnell <iarnell@gmail.com> 2.120530-1
- update to latest upstream version

* Sat Feb 04 2012 Iain Arnell <iarnell@gmail.com> 2.120351-1
- update to latest upstream version

* Sun Jan 22 2012 Iain Arnell <iarnell@gmail.com> 2.113640-3
- drop tests subpackage; move tests to main package documentation

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.113640-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jan  3 2012 Marcela Mašláňová <mmaslano@redhat.com> 2.113640-1
- update to latest version, which deprecated Version::Requirements

* Fri Sep 23 2011 Iain Arnell <iarnell@gmail.com> 2.112621-1
- update to latest upstream version
- clean up spec for modern rpmbuild

* Sat Aug 27 2011 Iain Arnell <iarnell@gmail.com> 2.112150-1
- update to latest upstream version

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 2.110930-2
- Perl mass rebuild

* Sun Apr 03 2011 Iain Arnell <iarnell@gmail.com> 2.110930-1
- update to latest upstream version

* Sat Apr 02 2011 Iain Arnell <iarnell@gmail.com> 2.110910-1
- update to latest upstream version

* Sun Mar 06 2011 Iain Arnell <iarnell@gmail.com> 2.110580-1
- update to latest upstream version
- drop BR perl(Storable)

* Sat Feb 26 2011 Iain Arnell <iarnell@gmail.com> 2.110550-1
- update to latest upstream version

* Thu Feb 17 2011 Iain Arnell <iarnell@gmail.com> 2.110440-1
- update to latest upstream
- drop BR perl(autodie)
- drop BR perl(Data::Dumper)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.110350-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Feb 04 2011 Iain Arnell <iarnell@gmail.com> 2.110350-1
- update to latest upstream version

* Wed Dec 15 2010 Marcela Maslanova <mmaslano@redhat.com> - 2.102400-2
- 661697 rebuild for fixing problems with vendorach/lib

* Sun Aug 29 2010 Iain Arnell <iarnell@gmail.com> 2.102400-1
- update by Fedora::App::MaintainerTools 0.006
- updating to latest GA CPAN version (2.102400)
- added a new br on perl(Carp) (version 0)
- added a new br on perl(Data::Dumper) (version 0)
- altered br on perl(ExtUtils::MakeMaker) (0 => 6.31)
- added a new br on perl(File::Spec) (version 0)
- added a new br on perl(File::Temp) (version 0.20)
- added a new br on perl(IO::Dir) (version 0)
- added a new br on perl(Scalar::Util) (version 0)
- added a new br on perl(Storable) (version 0)
- added a new br on perl(autodie) (version 0)
- added a new br on perl(version) (version 0.82)

* Thu Aug 05 2010 Iain Arnell <iarnell@gmail.com> 2.102160-1
- update to latest upstream

* Wed Jun 16 2010 Iain Arnell <iarnell@gmail.com> 2.101670-1
- update to latest upstream

* Mon Jun 14 2010 Iain Arnell <iarnell@gmail.com> 2.101610-1
- update to latest upstream

* Tue Jun 01 2010 Iain Arnell <iarnell@gmail.com> 2.101461-2
- rebuild for perl-5.12

* Fri May 28 2010 Iain Arnell <iarnell@gmail.com> 2.101461-1
- Specfile autogenerated by cpanspec 1.78.
- drop explicit requirements
