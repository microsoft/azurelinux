Summary:        Low-level interface to lzma compression library
Name:           perl-Compress-Raw-Lzma
Version:        2.101
Release:        4%{?dist}
License:        GPL+ OR Artistic
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://metacpan.org/release/Compress-Raw-Lzma
Source0:        https://cpan.metacpan.org/modules/by-module/Compress/Compress-Raw-Lzma-%{version}.tar.gz
Source1:        LICENSE.PTR

# Module Build
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  perl-devel
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  xz-devel
BuildRequires:  perl(Config)
BuildRequires:  perl(ExtUtils::Constant)
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(File::Copy)
BuildRequires:  perl(File::Spec::Functions)
BuildRequires:  perl(FindBin)
BuildRequires:  perl(lib)
BuildRequires:  perl(Module::CoreList)

# Module Runtime
BuildRequires:  perl(AutoLoader)
BuildRequires:  perl(Carp)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(UNIVERSAL)
BuildRequires:  perl(XSLoader)
BuildRequires:  perl(bytes)
BuildRequires:  perl(constant)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)

%if %{with_check}
# Test Suite
BuildRequires:  perl(File::Path)
BuildRequires:  perl(Test::More)

# Optional Tests
BuildRequires:  xz
BuildRequires:  perl(Test::CPAN::Meta)
BuildRequires:  perl(Test::CPAN::Meta::JSON)
BuildRequires:  perl(Test::NoWarnings)
BuildRequires:  perl(Test::Pod) >= 1.00
%endif

# Built-against version is embedded in module, so we have a strict version dependency
Requires:       xz-libs%{?_isa} = %((pkg-config --modversion liblzma 2>/dev/null || echo 0) | tr -dc '[0-9.]')
# Runtime
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:       perl(XSLoader)
# Don't "provide" private Perl libs
%{?perl_default_filter}

%description
This module provides a Perl interface to the lzma compression library.
It is used by IO::Compress::Lzma.

%prep
%setup -q -n Compress-Raw-Lzma-%{version}

# Remove bundled test modules
rm -rv t/Test/
perl -i -ne 'print $_ unless m{^t/Test/}' MANIFEST

%build
perl Makefile.PL \
  INSTALLDIRS=vendor \
  NO_PACKLIST=1 \
  NO_PERLLOCAL=1 \
  OPTIMIZE="%{optflags}"
%make_build

%install
%make_install
find %{buildroot} -type f -name '*.bs' -empty -delete
%{_fixperms} -c %{buildroot}

cp %{SOURCE1} .

%check
%make_build test

%files
%license LICENSE.PTR
%doc Changes README
%{perl_vendorarch}/auto/Compress/
%{perl_vendorarch}/Compress/
%{_mandir}/man3/Compress::Raw::Lzma.3*

%changelog
* Wed Jan 19 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.101-4
- Initial CBL-Mariner import from Fedora 36 (license: MIT).
- License verified.

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.101-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 2.101-2
- Perl 5.34 rebuild

* Sat Feb 20 2021 Paul Howarth <paul@city-fan.org> - 2.101-1
- Update to 2.101 (no changes)

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.100-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Jan  7 2021 Paul Howarth <paul@city-fan.org> - 2.100-1
- Update to 2.100
  - Expose liblzma's 'preset_dict' feature
  - Trim whitespace

* Sat Aug  1 2020 Paul Howarth <paul@city-fan.org> - 2.096-1
- Update to 2.096 (no changes)

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.095-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 21 2020 Paul Howarth <paul@city-fan.org> - 2.095-1
- Update to 2.095 (no changes)
- Modernize spec using %%{make_build} and %%{make_install}

* Mon Jul 13 2020 Paul Howarth <paul@city-fan.org> - 2.094-1
- Update to 2.094
  - Fix issue with Append mode and SvOOK (GH#4)

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 2.093-5
- Perl 5.32 rebuild

* Mon Mar 30 2020 Paul Howarth <paul@city-fan.org> - 2.093-4
- Rebuild for xz 5.2.5

* Fri Feb 14 2020 Petr Pisar <ppisar@redhat.com> - 2.093-3
- Unbundle test dependencies

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.093-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sun Dec  8 2019 Paul Howarth <paul@city-fan.org> - 2.093-1
- Update to 2.093
  - Lzma.xs: Add allocator to lzma_properties_decode (GH#2)

* Mon Dec  2 2019 Paul Howarth <paul@city-fan.org> - 2.092-1
- Update to 2.092
  - Use lzma_allocator (GH#2)

* Sun Nov 24 2019 Paul Howarth <paul@city-fan.org> - 2.091-1
- Update to 2.091
  - More updates for memory leak in raw_decoder (GH#1)
  - Silence compiler warning

* Sun Nov 10 2019 Paul Howarth <paul@city-fan.org> - 2.090-1
- Update to 2.090
  - Fix memory leak in raw_decoder (GH#1)

* Sun Nov  3 2019 Paul Howarth <paul@city-fan.org> - 2.089-1
- Update to 2.089 (no changes)

* Sun Nov  3 2019 Paul Howarth <paul@city-fan.org> - 2.088-1
- Update to 2.088
  - Add support details in documentation

* Mon Aug 12 2019 Paul Howarth <paul@city-fan.org> - 2.087-1
- Update to 2.087 (no changes)

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.086-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 2.086-2
- Perl 5.30 rebuild

* Mon Apr  1 2019 Paul Howarth <paul@city-fan.org> - 2.086-1
- Update to 2.086
  - Moved source to github: https://github.com/pmqs/Compress-Raw-Lzma
  - Add META_MERGE to Makefile.PL
  - Added meta-json.t and meta-yaml.t

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.085-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sun Jan 13 2019 Paul Howarth <paul@city-fan.org> - 2.085-1
- Update to 2.085
  - Test harness can use a lot of memory; on systems with small memory,
    t/050interop-xz.t can fail, so free memory before invoking xz
    (CPAN RT#128194)

* Mon Jan  7 2019 Paul Howarth <paul@city-fan.org> - 2.084-1
- Update to 2.084 (no changes)

* Wed Jan  2 2019 Paul Howarth <paul@city-fan.org> - 2.083-1
- Update to 2.083 (no changes)
- Drop legacy Group: tag

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.082-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 2.082-3
- Perl 5.28 rebuild

* Sat May 12 2018 Paul Howarth <paul@city-fan.org> - 2.082-2
- Rebuild for xz 5.2.4 in Fedora 28 onwards

* Mon Apr 16 2018 Paul Howarth <paul@city-fan.org> - 2.082-1
- Update to 2.082
  - README: Document clash with older version of liblzma (CPAN RT#125046)
  - Lzma.pm: Fix typo in pod (CPAN RT#125093)

* Mon Apr  9 2018 Paul Howarth <paul@city-fan.org> - 2.081-1
- Update to 2.081
  - Previous release used $^W instead of use warnings - fixed

* Wed Apr  4 2018 Paul Howarth <paul@city-fan.org> - 2.080-1
- Update to 2.080 (no changes)

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.074-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.074-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.074-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 2.074-2
- Perl 5.26 rebuild

* Mon Feb 20 2017 Paul Howarth <paul@city-fan.org> - 2.074-1
- Update to 2.074
  - Lzma.xs: comment out unused variables and remove C++-ism (CPAN RT#120272)
  - Make failure when LZMA_VERSION != lzma_version_number more explicit
  - Added interface to LZMA_VERSION and LZMA_VERSION_STRING

* Mon Feb 13 2017 Paul Howarth <paul@city-fan.org> - 2.072-1
- Update to 2.072
  - Fix for Makefile.PL depending on . in @INC (CPAN RT#120084)
  - Use of Compress::Raw::Lzma::RawDecoder failed with large amount of data
    (CPAN RT#105460)
  - AppendOutput for "encode" methods said default was 1; it is actually 0

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.070-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Jan  2 2017 Paul Howarth <paul@city-fan.org> - 2.070-2
- Rebuild for xz-5.2.3

* Thu Dec 29 2016 Paul Howarth <paul@city-fan.org> - 2.070-1
- Update to 2.070
  - Fix wrong FLAG_APPEND_OUTPUT logic (CPAN RT#119207)
- Simplify find commands using -empty and -delete

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 2.069-4
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.069-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Sep 29 2015 Paul Howarth <paul@city-fan.org> - 2.069-2
- Rebuild for xz-5.2.2

* Sun Sep 27 2015 Paul Howarth <paul@city-fan.org> - 2.069-1
- Update to 2.069 (no changes)

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.068-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jun 05 2015 Jitka Plesnikova <jplesnik@redhat.com> - 2.068-4
- Perl 5.22 rebuild

* Fri Feb 27 2015 Paul Howarth <paul@city-fan.org> - 2.068-3
- Rebuild for xz-5.2.1 in Rawhide

* Tue Jan  6 2015 Paul Howarth <paul@city-fan.org> - 2.068-2
- Rebuild for xz-5.2.0 in Rawhide (#1179255)

* Wed Dec 24 2014 Paul Howarth <paul@city-fan.org> - 2.068-1
- Update to 2.068 (no changes)

* Tue Dec  9 2014 Paul Howarth <paul@city-fan.org> - 2.067-1
- Update to 2.067 (no changes)
- Classify buildreqs by usage

* Mon Sep 22 2014 Paul Howarth <paul@city-fan.org> - 2.066-1
- Update to 2.066 (no changes)

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 2.064-4
- Perl 5.20 rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.064-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.064-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Feb  2 2014 Paul Howarth <paul@city-fan.org> - 2.064-1
- Update to 2.064
  - Handle non-PVs better (CPAN RT#91558)

* Sun Nov  3 2013 Paul Howarth <paul@city-fan.org> - 2.063-1
- Update to 2.063 (no changes)

* Mon Aug 12 2013 Paul Howarth <paul@city-fan.org> - 2.062-1
- Update to 2.062
  - Fix typos (CPAN RT#86418)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.061-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jul 18 2013 Petr Pisar <ppisar@redhat.com> - 2.061-2
- Perl 5.18 rebuild

* Mon May 27 2013 Paul Howarth <paul@city-fan.org> - 2.061-1
- Update to 2.061
  - Silence compiler warning by making 2nd parameter to DispStream a const char*

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.060-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Jan  8 2013 Paul Howarth <paul@city-fan.org> - 2.060-1
- Update to 2.060 (no changes)

* Sun Nov 25 2012 Paul Howarth <paul@city-fan.org> - 2.059-1
- Update to 2.059
  - Copy-on-write support

* Tue Nov 13 2012 Paul Howarth <paul@city-fan.org> - 2.058-1
- Update to 2.058
  - Update to ppport.h that includes SvPV_nomg_nolen
  - Added PERL_NO_GET_CONTEXT

* Mon Aug  6 2012 Paul Howarth <paul@city-fan.org> - 2.055-1
- Update to 2.055
  - Fix misuse of magic in API (CPAN RT#78080)

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.052-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul 09 2012 Petr Pisar <ppisar@redhat.com> - 2.052-4
- Perl 5.16 rebuild

* Thu Jul  5 2012 Paul Howarth <paul@city-fan.org> - 2.052-3
- Rebuild for xz 5.1.2alpha in Rawhide
- BR: perl(AutoLoader), perl(constant), perl(Exporter), perl(lib) and
  perl(Test::NoWarnings)
- BR:/R: perl(XSLoader), the module's preferred dynamic object loader

* Mon Jun 11 2012 Petr Pisar <ppisar@redhat.com> - 2.052-2
- Perl 5.16 rebuild

* Sun Apr 29 2012 Paul Howarth <paul@city-fan.org> - 2.052-1
- Update to 2.052 (fix to allow building with C++)
- Don't need to remove empty directories from buildroot

* Sat Feb 18 2012 Paul Howarth <paul@city-fan.org> - 2.049-1
- Update to 2.049 (README wasn't included in the distribution)
- Drop redundant %%defattr

* Sun Jan 29 2012 Paul Howarth <paul@city-fan.org> - 2.048-1
- Update to 2.048 (set minimum Perl version to 5.6)

* Tue Jan 10 2012 Paul Howarth <paul@city-fan.org> - 2.045-2
- Rebuild for gcc 4.7 in Rawhide

* Sun Dec  4 2011 Paul Howarth <paul@city-fan.org> - 2.045-1
- Update to 2.045
  - Moved FAQ.pod to IO::Compress

* Sun Dec  4 2011 Paul Howarth <paul@city-fan.org> - 2.044-1
- Update to 2.044
  - Moved FAQ.pod under the lib directory so it can get installed

* Mon Nov 21 2011 Paul Howarth <paul@city-fan.org> - 2.043-1
- Update to 2.043 (no changes)

* Fri Nov 18 2011 Paul Howarth <paul@city-fan.org> - 2.042-1
- Update to 2.042 (no changes)

* Sat Oct 29 2011 Paul Howarth <paul@city-fan.org> - 2.040-1
- Update to 2.040
  - Croak if attempt to freeze/thaw compression object (CPAN RT#69985)
- BR: perl(Carp)

* Sun Oct 16 2011 Jindrich Novy <jnovy@redhat.com> - 2.037-3
- Rebuild against new xz

* Wed Jun 22 2011 Paul Howarth <paul@city-fan.org> - 2.037-2
- Perl mass rebuild

* Wed Jun 22 2011 Paul Howarth <paul@city-fan.org> - 2.037-1
- Update to 2.037 (no changes)

* Mon Jun 20 2011 Paul Howarth <paul@city-fan.org> - 2.036-2
- Perl mass rebuild

* Mon Jun 20 2011 Paul Howarth <paul@city-fan.org> - 2.036-1
- Update to 2.036
  - A number of changes to facilitate adding LZMA support to
    IO::Compress::Zip : IO::Uncompress::Unzip:
    - Added preset filters Lzma::Filter::Lzma1::Preset and
      Lzma::Filter::Lzma2::Preset
   - Added forZip option to Compress::Raw::Lzma::Encoder
   - Added properties option to Compress::Raw::Lzma::RawDecoder

* Sun Jun 19 2011 Marcela Mašláňová <mmaslano@redhat.com> - 2.035-3
- Perl mass rebuild

* Mon May 23 2011 Paul Howarth <paul@city-fan.org> - 2.035-2
- Rebuild for xz 5.0.3

* Sat May  7 2011 Paul Howarth <paul@city-fan.org> - 2.035-1
- Update to 2.035 (no changes)

* Tue May  3 2011 Paul Howarth <paul@city-fan.org> - 2.034-1
- Update to 2.034 (document the change of default MemLimit in 2.033)

* Mon Apr  4 2011 Paul Howarth <paul@city-fan.org> - 2.033-4
- Rebuild for xz 5.0.2

* Wed Feb  9 2011 Paul Howarth <paul@city-fan.org> - 2.033-3
- Add explicit version dependency on xz-libs since the version number built
  against is embedded into the module and can cause failures in users of this
  module if they compare build-time and run-time versions of liblzma

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.033-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jan 11 2011 Paul Howarth <paul@city-fan.org> - 2.033-1
- Update to 2.033 (changed default MemLimit from 128 MB to unlimited)

* Fri Jan  7 2011 Paul Howarth <paul@city-fan.org> - 2.032-1
- Update to 2.032 (no changes)

* Wed Oct 27 2010 Paul Howarth <paul@city-fan.org> - 2.031-1
- Update to 2.031
  - Changed to build with XZ 5.0.0
  - Dropped symbolic constants provided by subblock.h (CPAN RT#62461)
- Drop xz 5.x patch, no longer needed

* Tue Oct 26 2010 Paul Howarth <paul@city-fan.org> - 2.030-2
- Patch out subfilter constants, not supported in xz 5.x (CPAN RT#62461)

* Mon Jul 26 2010 Paul Howarth <paul@city-fan.org> - 2.030-1
- Update to 2.030 (no changes)

* Fri May 14 2010 Paul Howarth <paul@city-fan.org> - 2.029-3
- Rebuild for perl 5.12.0

* Tue May 11 2010 Paul Howarth <paul@city-fan.org> - 2.029-2
- Drop redundant buildroot tag

* Sat May  8 2010 Paul Howarth <paul@city-fan.org> - 2.029-1
- Update to 2.029 (test harness copes with memory shortage)

* Mon May  3 2010 Paul Howarth <paul@city-fan.org> - 2.028-1
- Update to 2.028
  - Remove 'Persistent' option from  Lzma::Filter::Lzma (CPAN RT#57080)
  - Silence a pile of compiler warnings
- Drop patch for CPAN RT#57080, no longer needed

* Thu Apr 29 2010 Paul Howarth <paul@city-fan.org> - 2.027-1
- Initial RPM version
