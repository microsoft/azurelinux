Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Name:           perl-GD
Version:        2.83
Release:        1%{?dist}
Summary:        Perl interface to the GD graphics library
License:        GPL-1.0-or-later OR Artistic-2.0
URL:            https://metacpan.org/release/GD
Source0:        https://cpan.metacpan.org/modules/by-module/GD/GD-%{version}.tar.gz#/perl-GD-%{version}.tar.gz
Patch1:         GD-2.77-cflags.patch
# Module Build
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  gcc
BuildRequires:  gd-devel >= 2.0.28
BuildRequires:  make
BuildRequires:  perl-devel
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(Config)
BuildRequires:  perl(ExtUtils::Constant) >= 0.23
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(ExtUtils::PkgConfig)
BuildRequires:  perl(File::Basename)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(File::Which)
BuildRequires:  perl(Getopt::Long)
# Module Runtime
BuildRequires:  perl(AutoLoader)
BuildRequires:  perl(Carp)
BuildRequires:  perl(DynaLoader)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(FileHandle)
BuildRequires:  perl(Math::Trig)
BuildRequires:  perl(strict)
BuildRequires:  perl(Symbol)
BuildRequires:  perl(vars)
# Test Suite
# Note: optional test requirement perl(Test::Fork) not currently available in Fedora
BuildRequires:  perl(constant)
BuildRequires:  perl(FindBin)
BuildRequires:  perl(IO::Dir)
BuildRequires:  perl(lib)
BuildRequires:  perl(Test)
BuildRequires:  perl(Test::More) >= 0.88
BuildRequires:  perl(Test::NoWarnings) >= 1.00
BuildRequires:  perl(warnings)
# Dependencies
Requires:       gd >= 2.0.28

%global __provides_exclude %{?__provides_exclude:__provides_exclude|}^perl\\(GD::Polygon\\)$
%{?perl_default_filter}

%description
This is a auto-loadable interface module for GD, a popular library
for creating and manipulating PNG files. With this library you can
create PNG images on the fly or modify existing files.

%prep
%setup -q -n GD-%{version}

# Upstream wants -Wformat=1 but we don't
%patch -P 1

# Fix shellbangs in sample scripts
perl -pi -e 's|/usr/local/bin/perl\b|%{__perl}|' \
      demos/{*.{pl,cgi},truetype_test}

%build
perl Makefile.PL INSTALLDIRS=vendor OPTIMIZE="%{optflags}"
make

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name '*.bs' -empty -delete
find %{buildroot} -type f -name .packlist -delete
%{_fixperms} -c %{buildroot}

%check
make test TEST_VERBOSE=1

%files
%license LICENSE
%doc ChangeLog README README.QUICKDRAW demos/
%{_bindir}/bdf2gdfont.pl
%{perl_vendorarch}/auto/GD/
%{perl_vendorarch}/GD.pm
%{perl_vendorarch}/GD/
%{_mandir}/man1/bdf2gdfont.pl.1*
%{_mandir}/man3/GD.3*
%{_mandir}/man3/GD::Group.3*
%{_mandir}/man3/GD::Image.3*
%{_mandir}/man3/GD::Polygon.3*
%{_mandir}/man3/GD::Polyline.3*
%{_mandir}/man3/GD::Simple.3*

%changelog
* Thu Feb 27 2025 Sumit Jena <v-sumitjena@microsoft.com> - 1.16-1
- Update to version 1.16
- License verified

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.71-5
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.71-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.71-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 2.71-2
- Perl 5.30 rebuild

* Tue Feb 12 2019 Paul Howarth <paul@city-fan.org> - 2.71-1
- Update to 2.71
  - Skip Test::Fork on freebsd (GH#25)
- Filter unversioned provide of perl(GD::Polygon)

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.70-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jan 11 2019 Paul Howarth <paul@city-fan.org> - 2.70-1
- Update to 2.70
  - Fixes for hardened CCFLAGS with -Werror (CPAN RT#128167)

* Mon Aug 27 2018 Tom Callaway <spot@fedoraproject.org> - 2.69-1
- update to 2.69

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.68-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 2.68-2
- Perl 5.28 rebuild

* Mon Feb 19 2018 Paul Howarth <paul@city-fan.org> - 2.68-1
- Update to 2.68
  - Fix GD::Polygon->clear (CPAN RT#124463)

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.67-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Nov 15 2017 Paul Howarth <paul@city-fan.org> - 2.67-1
- Update to 2.67
  - Fix thread-safety for GD::Simple %%COLORS (GH#26)
  - Fix arc start-angle docs (CPAN RT#123277)
  - Improve setBrush docs (CPAN RT#123194)
  - Improve StringFT docs (CPAN RT#123193)
  - Replace MacOSX by darwin, and not by Mac OS X/macOS as suggested in GH#24
  - Add GD::Image->_file method and the helper GD::supportsFileType
    (CPAN RT#60488)

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.66-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.66-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 2.66-2
- Perl 5.26 rebuild

* Mon Apr 24 2017 Paul Howarth <paul@city-fan.org> - 2.66-1
- Update to 2.66
  - Throw proper error on newFrom* with not-existing file
  - Add t/transp.t from CPAN RT#40525
  - Improve multiple gd.h warning (CPAN RT#54366)
  - Better documentation for GD::Simple->arc
  - Fix ANIMGIF with libgd 2.3.0-dev

* Sun Apr 23 2017 Paul Howarth <paul@city-fan.org> - 2.65-1
- Update to 2.65
  - Fix --gdlib_config_path to accept an argument

* Sun Apr 23 2017 Paul Howarth <paul@city-fan.org> - 2.64-1
- Update to 2.64
  - Add CONFIGURE_REQUIRES META
  - Add --gdlib_config_path
  - Add Image Filters: scatter, pixelate, negate, grayscale, brightness,
    contrast, color, selectiveBlur, edgeDetectQuick, gaussianBlur, emboss,
    meanRemoval, smooth, copyGaussianBlurred
  - Add palette methods: createPaletteFromTrueColor, neuQuant (but
    discouraged), colorMatch
  - Add interpolation methods: copyScale, copyRotateInterpolated,
    interpolationMethod
  - Add double GD::VERSION
  - Add all gd.h constants
  - Fixed wrong <5.14 code generated with ExtUtils::Constants (CPAN RT#121297);
    only generate const-xs.inc when it's missing
  - Add -liconv on hpux too (our pkgconfig parser cannot handle it)
  - Renamed VERSION() to LIBGD_VERSION() (CPAN RT#121307); it was treated
    magically by "use GD 2.18"
  - Update doc for LIBGD_VERSION()
  - Fix 5.6.2, which does not have float in its typemap

* Sat Apr 22 2017 Paul Howarth <paul@city-fan.org> - 2.60-1
- Update to 2.60
  - Add missing methods newFromWBMP, newFromXbm (CPAN RT #68784) and some
    missing docs
  - Add --lib_fontconfig_path, --fcgi options
  - Rewrote most of the XS code
  - Clean up Makefile.PL (GH#20)

* Fri Apr 21 2017 Paul Howarth <paul@city-fan.org> - 2.59-1
- Update to 2.59
  - Remove Build.PL, fix permissions, fix for missing gdlib-config
  - Fix feature extraction ≥ 2.2 (CPAN RT#119459)
  - Add alpha method
  - Improve option handling
  - Fix metadata
  - Fix Jpeg magic number detection (CPAN RT#26146)
  - Fix RGB-HSV roundtrips (CPAN RT#120572)
  - Fix -print-search-dirs errors (CPAN RT#106265)
  - Co-maint to RURBAN
  - Add hv_fetchs, CI smokers
  - Add GD::VERSION_STRING API
  - Honor --lib_gd_path specific gdlib-config
  - Loosen the comparison tests with GDIMAGETYPE ne gd2
  - Improve gdlib-config parsing (GH#17), esp. with 2.0.34
  - Error on failing libgd calls
  - Fix colorClosestAlpha, colorAllocateAlpha
  - Add missing documentation
- This release by RURBAN → update source URL
- Switch to ExtUtils::MakeMaker flow
- Drop legacy Group: tag

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.56-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 01 2017 Sandro Mani <manisandro@gmail.com> - 2.56-10
- Rebuild (libwebp)

* Fri Jul 22 2016 Tom Callaway <spot@fedoraproject.org> - 2.56-9
- rebuild to lose libvpx dep

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 2.56-8
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.56-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Dec 14 2015 Paul Howarth <paul@city-fan.org> - 2.56-6
- Mark the flaky image comparison test as TODO (#1291200, CPAN RT#100294)

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.56-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jun 05 2015 Jitka Plesnikova <jplesnik@redhat.com> - 2.56-4
- Perl 5.22 rebuild

* Mon Apr  6 2015 Tom Callaway <spot@fedoraproject.org> - 2.56-3
- rebuild against libvpx 1.4.0

* Mon Jan 12 2015 Tom Callaway <spot@fedoraproject.org> - 2.56-2
- do not package bdftogd here, that lives in gd-progs

* Tue Dec  2 2014 Paul Howarth <paul@city-fan.org> - 2.56-1
- Update to 2.56
  - Fix misleading warning message about location of gd.h file
  - Fix regression tests to run on Ubuntu 12.04 64bit
  - Point to Gabor Szabo's GD::Simple tutorial, and fix link to repository
  - Fix image corruption in rotate180 when image height is odd
  - Great simplification of regression framework ought to fix make test problems
  - Remove archaic qd.pl (for creating QuickDraw picts) from distribution
- Switch to Module::Build flow as EU::MM flow is broken (CPAN RT#99901)
- Include upstream's LICENSE file (license now GPL+ or Artistic 2.0)
- Tests no longer failing on ppc

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 2.50-4
- Perl 5.20 rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.50-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.50-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Dec 12 2013 Tom Callaway <spot@fedoraproject.org> - 2.50-1
- update to 2.50

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.49-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 2.49-2
- Perl 5.18 rebuild

* Tue Jun 11 2013 Remi Collet <rcollet@redhat.com> - 2.49-1
- update to 2.49
- ignore GD tests 2..10, results are "visibly" correct #973139

* Tue Jun 11 2013 Remi Collet <rcollet@redhat.com> - 2.46-4
- rebuild for new GD 2.1.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.46-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Jan 21 2013 Adam Tkac <atkac redhat com> - 2.46-2
- rebuild due to "jpeg8-ABI" feature drop

* Thu Oct 25 2012 Petr Šabata <contyk@redhat.com> - 2.46-1
- 2.46 bump
- Specify all dependencies
- Drop command macros
- Modernize the spec and clean whitespace

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.44-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 11 2012 Petr Pisar <ppisar@redhat.com> - 2.44-11
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.44-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Nov 10 2011 Iain Arnell <iarnell@gmail.com> 2.44-9
- Rebuild for libpng 1.5

* Sat Jun 18 2011 Iain Arnell <iarnell@gmail.com> 2.44-8
- patch to avoid issue with ExtUtils::MakeMaker and CCFLAGS
  see http://bugs.debian.org/cgi-bin/bugreport.cgi?bug=628522
- clean up spec for modern rpmbuild
- use perl_default_filter

* Wed Jun 15 2011 Marcela Mašláňová <mmaslano@redhat.com> - 2.44-7
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.44-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 16 2010 Marcela Maslanova <mmaslano@redhat.com> - 2.44-5
- 661697 rebuild for fixing problems with vendorach/lib

* Sun May 02 2010 Marcela Maslanova <mmaslano@redhat.com> - 2.44-4
- Mass rebuild with perl-5.12.0

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 2.44-3
- rebuild against perl 5.10.1

* Thu Oct 29 2009 Stepan Kasal <skasal@redhat.com> - 2.44-2
- give up tests on ppc

* Mon Oct  5 2009 Stepan Kasal <skasal@redhat.com> - 2.44-1
- new upstream version
- run tests always
- do not add bdf_scripts/ to docs
- switch off the test that fails in i686 koji

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.41-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Mar 16 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 2.41-2
- fix Makefile.PL to install GD/Group.pm (bz 490429)

* Fri Mar 13 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 2.41-1
- update to 2.41

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.39-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Jul 21 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.39-1
- update to 2.39

* Fri Apr  4 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.35-7
- tests work fine locally, one fails in mock, maybe needs a desktop?
  conditionalized them, default off.

* Fri Apr  4 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.35-6
- license fix

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.35-5
- Rebuild for perl 5.10 (again)

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2.35-4
- Autorebuild for GCC 4.3

* Thu Jan 24 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.35-3
- rebuild for new perl

* Mon Oct 15 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 2.35-2.1
- add BR: perl(ExtUtils::MakeMaker)

* Sun Oct  8 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.35-2
- Removed a duplicate file (bdf_scripts/bdf2gdfont.PLS).

* Tue Sep  5 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.35-1
- Update to 2.35.

* Sat Jun  3 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.34-1
- Update to 2.34.

* Wed Mar  8 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.32-1
- Update to 2.32.

* Tue Feb 21 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.31-1
- Update to 2.31.

* Wed Feb 15 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.30-3
- Missing BR: fontconfig-devel.

* Mon Feb 13 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.30-2
- Modular X (libX11-devel, libXpm-devel).

* Fri Oct 21 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.30-1
- Update to 2.30.

* Mon Aug  8 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.28-1
- Update to 2.28.

* Tue Jul 19 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.25-1
- Update to 2.25.

* Wed Apr  6 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 2.23-2
- rebuilt

* Wed Mar  9 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.23-1
- Update to 2.23.

* Thu Dec 09 2004 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0:2.19-1
- Update to 2.19.
- GIF support has been restored in gd 2.0.28.
- Module autoconfigures itself with the gdlib-config program.

* Mon Jun 28 2004 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0:2.12-0.fdr.3
- Avoid RPATH problem in FC1 (bug 1756).
- Replaced hardcoded value by rpmmacro (%%{__perl}) (bug 1756).

* Mon Jun 14 2004 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0:2.12-0.fdr.2
- Bring up to date with current fedora.us perl spec template.

* Sat Feb  7 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:2.12-0.fdr.1
- Update to 2.12.
- Reduce directory ownership bloat.

* Tue Nov 18 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:2.11-0.fdr.1
- Update to 2.11.

* Sat Oct 11 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:1.41-0.fdr.1
- First build.
