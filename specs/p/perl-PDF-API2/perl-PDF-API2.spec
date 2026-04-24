# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           perl-PDF-API2
Version:        2.048
Release: 2%{?dist}
Summary:        Perl module for creation and modification of PDF files
# lib/PDF/API2.pm:  LGPL-2.1-or-later
# lib/PDF/API2/Resource/XObject/Image/PNM.pm: GPL-1.0-or-later OR Artistic-1.0-Perl
#                                             (taken from Image::PBMLib)
# lib/PDF/API2/Basic/PDF/Null.pm:   Artistic-1.0-Perl OR MIT (MIT grant in
#                                   COPYING-PDF_API2_Basic_PDF-Martin_Hosken)
# lib/PDF/API2/Matrix.pm:   GPL-1.0-or-later OR Artistic-1.0-Perl
# LICENSE:          LGPL-2.1 text
# README:           LGPL-2.1-or-later
License:        LGPL-2.1-or-later AND (GPL-1.0-or-later OR Artistic-1.0-Perl) AND (MIT OR Artistic-1.0-Perl)
URL:            https://metacpan.org/release/PDF-API2
Source0:        https://cpan.metacpan.org/authors/id/S/SS/SSIMMS/PDF-API2-%{version}.tar.gz 
# MIT license grant from Marin Hosken, CPAN RT#133691
Source1:        COPYING-PDF_API2_Basic_PDF-Martin_Hosken
Patch1:         font-location.patch
# Fix inserting LZW-compressed 8-bit TIFF images, bug #1378895, CPAN RT#118047
Patch2:         PDF-API2-2.033-Use-libtiff-to-decode-image-data-in-TIFF-fixing-RT-1.patch

BuildArch:      noarch
BuildRequires:  coreutils
BuildRequires:  glibc-common
BuildRequires:  make
BuildRequires:  perl-interpreter
BuildRequires:  perl-generators
BuildRequires:  perl(Config)
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# Run-time:
BuildRequires:  perl(base)
BuildRequires:  perl(Carp)
BuildRequires:  perl(Compress::Zlib) >= 1.0
BuildRequires:  perl(constant)
BuildRequires:  perl(Encode)
BuildRequires:  perl(English)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(File::Basename)
BuildRequires:  perl(File::Temp)
BuildRequires:  perl(FileHandle)
BuildRequires:  perl(Font::TTF::Font)
BuildRequires:  perl(Graphics::TIFF)
BuildRequires:  perl(IO::File)
BuildRequires:  perl(List::Util)
BuildRequires:  perl(Math::Trig)
BuildRequires:  perl(POSIX)
BuildRequires:  perl(Scalar::Util)
# Storable is required by Unicode::UCD
BuildRequires:  perl(Storable)
BuildRequires:  perl(Unicode::UCD)
BuildRequires:  perl(vars)
# Tests:
# ImageMagick for convert tool
BuildRequires:  ImageMagick
# libtiff-tools for tiffcp tool
BuildRequires:  libtiff-tools
BuildRequires:  perl(File::Find)
BuildRequires:  perl(GD)
BuildRequires:  perl(Test::Exception)
BuildRequires:  perl(Test::Memory::Cycle)
BuildRequires:  perl(Test::More)
Requires:       dejavu-sans-fonts
Requires:       dejavu-sans-mono-fonts
Requires:       dejavu-serif-fonts
Requires:       perl(Compress::Zlib) >= 1.0
Requires:       perl(Storable)

# Filter under-specified dependencies
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\(Compress::Zlib\\)$

%description
A Perl Module Chain to facilitate the Creation and Modification of High-Quality
"Portable Document Format (aka. PDF)" Files.

%package tests
Summary:        Tests for %{name}
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       perl-Test-Harness
# ImageMagick for convert tool
Requires:       ImageMagick
# libtiff-tools for tiffcp tool
Requires:       libtiff-tools

%description tests
Tests from %{name}. Execute them
with "%{_libexecdir}/%{name}/test".

%prep
%autosetup -p1 -n PDF-API2-%{version}
install -m 0644 %{SOURCE1} ./

# fix interpreter in example files
for file in contrib/pdf-{de,}optimize.pl; do
    perl -MConfig -pi -e 's|^#!.*perl\b|$Config{startperl}|' "$file"
done

# make mode on included contrib 0644 to keep from triggering
# rpmlint warning and additional auto-requires
chmod a-x contrib/*

# recode Changes as UTF-8
iconv -f iso-8859-1 -t utf-8 < Changes > Changes.utf8
mv -f Changes.utf8 Changes

# Help file to recognise the Perl scripts and normalize shebangs
for F in t/*.t; do
    perl -i -MConfig -ple 'print $Config{startperl} if $. == 1 && !s{\A#!.*perl\b}{$Config{startperl}}' "$F"
    chmod +x "$F"
done

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%{make_build}

%install
%{make_install}

# Install tests
mkdir -p %{buildroot}%{_libexecdir}/%{name}
cp -a t %{buildroot}%{_libexecdir}/%{name}
rm -f %{buildroot}%{_libexecdir}/%{name}/t/author-critic.t
rm -f %{buildroot}%{_libexecdir}/%{name}/t/author-pod-syntax.t
perl -i -pe 's{\^\blib\b}{^%{perl_vendorlib}}' %{buildroot}/%{_libexecdir}/%{name}/t/00-all-usable.t
perl -i -pe 's{\blib\b}{%{perl_vendorlib}/PDF}' %{buildroot}/%{_libexecdir}/%{name}/t/00-all-usable.t
cat > %{buildroot}%{_libexecdir}/%{name}/test << 'EOF'
#!/bin/bash
set -e
# Some tests write into temporary files/directories. The easiest solution
# is to copy the tests into a writable directory and execute them from there.
DIR=$(mktemp -d)
pushd "$DIR"
cp -a %{_libexecdir}/%{name}/* ./
prove -I . -j "$(getconf _NPROCESSORS_ONLN)"
popd
rm -rf "$DIR"
EOF
chmod +x %{buildroot}%{_libexecdir}/%{name}/test

%{_fixperms} %{buildroot}/*

# we will not include the dejavu fonts in this package, we'll just require the
# deja-vu font packages and change the search location (patch0)
rm -rf %{buildroot}/%{perl_vendorlib}/PDF/API2/fonts


%check
export HARNESS_OPTIONS=j$(perl -e 'if ($ARGV[0] =~ /.*-j([0-9][0-9]*).*/) {print $1} else {print 1}' -- '%{?_smp_mflags}')
make test

%files
%license LICENSE COPYING-PDF_API2_Basic_PDF-Martin_Hosken
%doc Changes PATENTS README
%doc contrib
%{perl_vendorlib}/PDF/
%{_datadir}/man/man3/*
# files that are not relevent to this OS
%exclude %{perl_vendorlib}/PDF/API2/Win32.pm

%files tests
%{_libexecdir}/%{name}

%changelog
* Mon Sep 01 2025 Jitka Plesnikova <jplesnik@redhat.com> - 2.048-1
- 2.048 bump (rhbz#2391895)

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.047-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.047-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.047-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon May 20 2024 Jitka Plesnikova <jplesnik@redhat.com> - 2.047-1
- 2.047 bump (rhbz#2281424)

* Wed May 15 2024 Jitka Plesnikova <jplesnik@redhat.com> - 2.046-1
- 2.046 bump (rhbz#2280650)

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.045-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.045-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Sep 26 2023 Jitka Plesnikova <jplesnik@redhat.com> - 2.045-1
- 2.045 bump (rhbz#2240644)

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.044-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.044-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Nov 21 2022 Jitka Plesnikova <jplesnik@redhat.com> - 2.044-1
- 2.044 bump

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.043-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jun 01 2022 Jitka Plesnikova <jplesnik@redhat.com> - 2.043-3
- Perl 5.36 rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.043-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Dec 09 2021 Jitka Plesnikova <jplesnik@redhat.com> - 2.043-1
- 2.043 bump

* Fri Sep 17 2021 Jitka Plesnikova <jplesnik@redhat.com> - 2.042-1
- 2.042 bump

* Mon Aug 02 2021 Jitka Plesnikova <jplesnik@redhat.com> - 2.041-1
- 2.041 bump

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.040-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 2.040-2
- Perl 5.34 rebuild

* Wed Apr 14 2021 Jitka Plesnikova <jplesnik@redhat.com> - 2.040-1
- 2.040 bump

* Fri Mar 05 2021 Jitka Plesnikova <jplesnik@redhat.com> - 2.039-1
- 2.039 bump
- Package tests

* Fri Feb 05 2021 Petr Pisar <ppisar@redhat.com> - 2.038-3
- Correct a license to "LGPLv2+ and (GPL+ or Artistic) and (MIT or Artistic)"

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.038-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Sep 01 2020 Jitka Plesnikova <jplesnik@redhat.com> - 2.038-1
- 2.038 bump

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.037-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 2.037-2
- Perl 5.32 rebuild

* Thu Feb 06 2020 Jitka Plesnikova <jplesnik@redhat.com> - 2.037-1
- 2.037 bump

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.036-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Sep 18 2019 Jitka Plesnikova <jplesnik@redhat.com> - 2.036-1
- 2.036 bump

* Mon Aug 12 2019 Jitka Plesnikova <jplesnik@redhat.com> - 2.035-1
- 2.035 bump

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.034-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Jul 01 2019 Jitka Plesnikova <jplesnik@redhat.com> - 2.034-1
- 2.034 bump

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 2.033-8
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.033-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.033-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jun 29 2018 Jitka Plesnikova <jplesnik@redhat.com> - 2.033-5
- Perl 5.28 rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.033-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Jul 28 2017 Petr Pisar <ppisar@redhat.com> - 2.033-3
- Fix inserting LZW-compressed 8-bit TIFF images (bug #1378895)

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.033-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Jul 07 2017 Petr Pisar <ppisar@redhat.com> - 2.033-1
- 0.33 bump

* Mon Jul 03 2017 Jitka Plesnikova <jplesnik@redhat.com> - 2.032-1
- 2.032 bump

* Mon Jun 05 2017 Jitka Plesnikova <jplesnik@redhat.com> - 2.031-3
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.031-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Jan 30 2017 Jitka Plesnikova <jplesnik@redhat.com> - 2.031-1
- 2.031 bump

* Mon Oct 17 2016 Jitka Plesnikova <jplesnik@redhat.com> - 2.030-1
- 2.030 bump

* Mon Oct 10 2016 Jitka Plesnikova <jplesnik@redhat.com> - 2.029-1
- 2.029 bump

* Wed Jun 29 2016 Jitka Plesnikova <jplesnik@redhat.com> - 2.028-1
- 2.028 bump

* Mon May 16 2016 Jitka Plesnikova <jplesnik@redhat.com> - 2.027-2
- Perl 5.24 rebuild

* Thu Mar 31 2016 Jitka Plesnikova <jplesnik@redhat.com> - 2.027-1
- 2.027 bump

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.025-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Nov 09 2015 Jitka Plesnikova <jplesnik@redhat.com> - 2.025-1
- 2.025 bump

* Tue Aug 11 2015 Jitka Plesnikova <jplesnik@redhat.com> - 2.023-2
- Add require perl(Storable)

* Mon Jun 22 2015 Jitka Plesnikova <jplesnik@redhat.com> - 2.023-1
- 2.023 bump

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.021-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 2.021-4
- Perl 5.22 rebuild

* Thu Aug 28 2014 Jitka Plesnikova <jplesnik@redhat.com> - 2.021-3
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.021-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Mar 11 2014 Bernard Johnson <bjohnson@symetrix.com> - 2.021-1
- v 2.021 (bz #902236)

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.020-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jul 25 2013 Petr Pisar <ppisar@redhat.com> - 2.020-1
- 2.020 bump

* Wed Jul 24 2013 Petr Pisar <ppisar@redhat.com> - 2.019-6
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.019-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.019-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 15 2012 Petr Pisar <ppisar@redhat.com> - 2.019-3
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.019-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Oct  2 2011 Tom Callaway <spot@fedoraproject.org> - 2.019-1
- update to 2.019

* Wed Jul 20 2011 Petr Sabata <contyk@redhat.com> - 2.016-3
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.016-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jan 30 2011 Bernard Johnson <bjohnson@symetrix.com> - 2.016-1
- v 2.016 (bz #672666)
- rebased font location patch

* Tue Dec 21 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.73-5
- 661697 rebuild for fixing problems with vendorach/lib

* Tue May 04 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.73-4
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.73-3
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.73-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jun 05 2009 Bernard Johnson <bjohnson@symetrix.com> - 0.73-1
- v 0.73-1

* Wed Feb 25 2009 Paul Howarth <paul@city-fan.org> - 0.72.003-2
- fix dejavu-* dependencies again
- recode TODO as UTF-8
- simplify perl requires filter

* Mon Dec 01 2008 Bernard Johnson <bjohnson@symetrix.com> - 0.72.003-1
- v 0.72.003

* Sat Nov 29 2008 Bernard Johnson <bjohnson@symetrix.com> - 0.72-2
- [Bug 473556] Fix dejavu-* dependencies

* Wed Nov 12 2008 Bernard Johnson <bjohnson@symetrix.com> - 0.72-1
- v 0.72

* Sun Oct 19 2008 Bernard Johnson <bjohnson@symetrix.com> - 0.71.001-2
- bump for cvs tag

* Sun Oct 19 2008 Bernard Johnson <bjohnson@symetrix.com> - 0.71.001-1
- v 0.71.001

* Tue Sep 30 2008 Bernard Johnson <bjohnson@symetrix.com> - 0.69-6
- fix patch fuzz
- change patch numbering

* Thu May 22 2008 Bernard Johnson <bjohnson@symetrix.com> - 0.69-5
- bump rel for new sources in F-7

* Thu May 22 2008 Bernard Johnson <bjohnson@symetrix.com> - 0.69-4
- fix dejavu font path (bz #447505)

* Thu Mar 06 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.69-3
Rebuild for new perl

* Mon Jan 21 2008 Bernard Johnson <bjohnson@symetrix.com> - 0.69-2
- patch .orig files packaged (bz #427762)

* Fri Jan 18 2008 Bernard Johnson <bjohnson@symetrix.com> - 0.69-1
- 0.69

* Mon Nov 12 2007 Bernard Johnson <bjohnson@symetrix.com> - 0.66-1
- 0.66

* Sun Oct 28 2007 Bernard Johnson <bjohnson@symetrix.com> - 0.65-1
- 0.65

* Sun Aug 19 2007 Bernard Johnson <bjohnson@symetrix.com> - 0.62-2
- update license tag to LGPLv2+
- remove CHANGELOG references

* Sun Aug 19 2007 Bernard Johnson <bjohnson@symetrix.com> - 0.62-1
- 0.62

* Thu May 03 2007 Bernard Johnson <bjohnson@symetrix.com> - 0.60-3
- update MANIFEST to remove 027_winfont that gets removed
- add missing BR perl(Test::More) and perl(XML::Parser::Expat)

* Sun Apr 29 2007 Bernard Johnson <bjohnson@symetrix.com> - 0.60-2
- remove fonts and depend on dejavu-fonts and dejavu-fonts-experimental
- change font search path
- remove font docs

* Sat Apr 28 2007 Bernard Johnson <bjohnson@symetrix.com> - 0.60-1
- v 0.60
- deliberately remove 027_winfont example as it wants Win32.pm
- BR on perl(Ext::MakeMaker) rather than perl

* Fri Apr 06 2007 Bernard Johnson <bjohnson@symetrix.com> - 0.59.002-2
- moving resource to docs was a mistake, fix it

* Thu Apr 05 2007 Bernard Johnson <bjohnson@symetrix.com> - 0.59.002-1
- initial release
