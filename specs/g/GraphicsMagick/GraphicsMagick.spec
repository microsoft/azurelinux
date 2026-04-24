# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.


%global _with_quantum_depth --with-quantum-depth=16
%global _enable_quantum_library_names --enable-quantum-library-names
%global libQ -Q16

# Disable automatic .la file removal
%global __brp_remove_la_files %nil

%if ! 0%{?flatpak}
%global perl 1
%endif

%if 0%{?rhel} > 7
%global urw_font_bundle 1
%endif

%global multilib_archs x86_64 %{ix86} ppc64 ppc64le ppc s390x s390 sparc64 sparcv9

%global __provides_exclude_from ^%{_libdir}/GraphicsMagick-%{version}/.*\\.(la|so)$

Name: GraphicsMagick
Version: 1.3.45
Release: 6%{?dist}
Summary: An ImageMagick fork, offering faster image generation and better quality
Url: http://www.graphicsmagick.org/
License: MIT

Source0: http://downloads.sourceforge.net/sourceforge/graphicsmagick/GraphicsMagick-%{version}.tar.xz
# bundle urw-fonts if needed
Source1: urw-fonts-1.0.7pre44.tar.bz2

# workaround multilib conflicts with GraphicsMagick-config
Patch100: GraphicsMagick-1.3.42-multilib.patch

# upstreamable patches
Patch50: GraphicsMagick-1.3.31-perl_linkage.patch

BuildRequires: bzip2-devel
BuildRequires: freetype-devel
BuildRequires: gcc-c++
BuildRequires: giflib-devel
BuildRequires: jasper-devel
BuildRequires: jbigkit-devel
BuildRequires: lcms2-devel
BuildRequires: libheif-devel
BuildRequires: libjpeg-devel
BuildRequires: libjxl-devel
BuildRequires: libpng-devel
BuildRequires: librsvg2-devel
BuildRequires: libtiff-devel
BuildRequires: libtool-ltdl-devel
BuildRequires: libwebp-devel
BuildRequires: libwmf-devel
BuildRequires: libxml2-devel
BuildRequires: libX11-devel libXext-devel libXt-devel
BuildRequires: lpr
BuildRequires: make
BuildRequires: p7zip
%if 0%{?perl}
BuildRequires: perl-devel
BuildRequires: perl-generators
BuildRequires: perl(ExtUtils::MakeMaker)
%endif
BuildRequires: xdg-utils
BuildRequires: xz-devel
BuildRequires: zlib-devel
## %%check stuff
BuildRequires: time

%if 0%{?urw_font_bundle}
%global urw_font_path %{_datadir}/GraphicsMagick-%{version}/urw-fonts
%else
%global urw_font_path %{_datadir}/X11/fonts/urw-fonts
BuildRequires: urw-base35-fonts-legacy
Requires: urw-base35-fonts-legacy
%endif

%description
GraphicsMagick is a comprehensive image processing package which is initially
based on ImageMagick 5.5.2, but which has undergone significant re-work by
the GraphicsMagick Group to significantly improve the quality and performance
of the software.

%package devel
Summary: Libraries and header files for GraphicsMagick app development
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
GraphicsMagick-devel contains the Libraries and header files you'll
need to develop GraphicsMagick applications. GraphicsMagick is an image
manipulation program.

If you want to create applications that will use GraphicsMagick code or
APIs, you need to install GraphicsMagick-devel as well as GraphicsMagick.
You do not need to install it if you just want to use GraphicsMagick,
however.

%package doc
Summary: GraphicsMagick documentation
BuildArch: noarch

%description doc
Documentation for GraphicsMagick.

%if 0%{?perl}
%package perl
Summary: GraphicsMagick perl bindings
Requires: %{name}%{?_isa} = %{version}-%{release}

%description perl
Perl bindings to GraphicsMagick.

Install GraphicsMagick-perl if you want to use any perl scripts that use
GraphicsMagick.
%endif

%package c++
Summary: GraphicsMagick Magick++ library (C++ bindings)
Requires: %{name}%{?_isa} = %{version}-%{release}

%description c++
This package contains the GraphicsMagick++ library, a C++ binding to the 
GraphicsMagick graphics manipulation library.

Install GraphicsMagick-c++ if you want to use any applications that use 
GraphicsMagick++.

%package c++-devel
Summary: C++ bindings for the GraphicsMagick library
Requires: %{name}-c++%{?_isa} = %{version}-%{release}
Requires: %{name}-devel%{?_isa} = %{version}-%{release}

%description c++-devel
GraphicsMagick-devel contains the Libraries and header files you'll
need to develop GraphicsMagick applications using the Magick++ C++ bindings.
GraphicsMagick is an image manipulation program.

If you want to create applications that will use Magick++ code
or APIs, you'll need to install GraphicsMagick-c++-devel, ImageMagick-devel and
GraphicsMagick.
You don't need to install it if you just want to use GraphicsMagick, or if you
want to develop/compile applications using the GraphicsMagick C interface,
however.

%prep
%autosetup -p1

%if 0%{?urw_font_bundle}
mkdir -p urw-fonts
tar --directory=urw-fonts/ -xf %{SOURCE1}
rm -f urw-fonts/ChangeLog urw-fonts/README* urw-fonts/fonts*
%endif

for f in ChangeLog.{2006,2008,2009,2012} NEWS.txt ; do
    iconv -f iso-8859-2 -t utf8 < $f > $f.utf8
    touch -r $f $f.utf8 ; mv -f $f.utf8 $f
done

# Avoid lib64 rpaths (FIXME: recheck this on newer releases)
%if "%{_libdir}" != "/usr/lib"
sed -i.rpath -e 's|"/lib /usr/lib|"/%{_lib} %{_libdir}|' configure
%endif


%build
%configure \
           --enable-shared --disable-static \
           --docdir=%{_pkgdocdir} \
           --with-lcms2 \
           --with-magick_plus_plus \
           --with-modules \
%if 0%{?flatpak}
           --without-perl \
%else
           --with-perl \
           --with-perl-options="INSTALLDIRS=vendor %{?perl_prefix}" \
%endif
           %{?_with_quantum_depth} \
           %{?_enable_quantum_library_names} \
           --with-threads \
           --with-wmf \
           --with-x \
           --with-xml \
           --without-dps \
           --without-gslib \
           --with-gs-font-dir=%{urw_font_path}

%make_build
%if 0%{?perl}
%make_build perl-build
%endif


%install
%make_install

%if 0%{?perl}
%make_install -C PerlMagick

# perlmagick: fix perl path of demo files
%{__perl} -MExtUtils::MakeMaker -e 'MY->fixin(@ARGV)' PerlMagick/demo/*.pl

find %{buildroot} -name "*.bs" |xargs rm -fv
find %{buildroot} -name ".packlist" |xargs rm -fv
find %{buildroot} -name "perllocal.pod" |xargs rm -fv

ls -l %{buildroot}%{perl_vendorarch}/auto/Graphics/Magick/Magick.so
chmod 755 %{buildroot}%{perl_vendorarch}/auto/Graphics/Magick/Magick.so

# perlmagick: build files list
find %{buildroot}/%{_libdir}/perl* -type f -print \
    | sed "s@^%{buildroot}@@g" > perl-pkg-files 
find %{buildroot}%{perl_vendorarch} -type d -print \
    | sed "s@^%{buildroot}@%dir @g" \
    | grep -v '^%dir %{perl_vendorarch}$' \
    | grep -v '/auto$' >> perl-pkg-files 
if [ -z perl-pkg-files ] ; then
    echo "ERROR: EMPTY FILE LIST"
    exit -1
fi
%endif

rm -rfv %{buildroot}%{_datadir}/GraphicsMagick
# Keep config
rm -rfv %{buildroot}%{_datadir}/%{name}-%{version}/[a-b,d-z,A-Z]*
rm -fv  %{buildroot}%{_libdir}/lib*.la

%if 0%{?urw_font_bundle}
mkdir -p %{buildroot}%{urw_font_path}/
install -p -m644 urw-fonts/* \
  %{buildroot}%{urw_font_path}/
%endif

# fix multilib issues
%ifarch %{multilib_archs}
mv %{buildroot}%{_includedir}/GraphicsMagick/magick/magick_types.h \
   %{buildroot}%{_includedir}/GraphicsMagick/magick/magick_types-%{__isa_bits}.h

cat >%{buildroot}%{_includedir}/GraphicsMagick/magick/magick_types.h <<EOF
#ifndef MAGICK_TYPES_MULTILIB
#define MAGICK_TYPES_MULTILIB

#include <bits/wordsize.h>

#if __WORDSIZE == 32
# include "magick/magick_types-32.h"
#elif __WORDSIZE == 64
# include "magick/magick_types-64.h"
#else
# error "unexpected value for __WORDSIZE macro"
#endif

#endif
EOF
%endif


%check
%if 0%{?perl}
make test -C PerlMagick ||:
%endif
time \
%make_build check ||:
# multilib hack only supports 32/64 bits for now
%ifarch %{multilib_archs}
%if ! (%{__isa_bits} == 32 || %{__isa_bits} == 64)
echo "multilib hack currently only supports 64/32 bits, not %{__isa_bits} (yet)"
exit 1
%endif
%endif


%ldconfig_scriptlets

%files
%dir %{_pkgdocdir}
%license %{_pkgdocdir}/Copyright.txt
%{_libdir}/libGraphicsMagick%{?libQ}.so.3*
%{_libdir}/libGraphicsMagickWand%{?libQ}.so.2*
%{_bindir}/[a-z]*
%{_libdir}/GraphicsMagick-%{version}/
%{_datadir}/GraphicsMagick-%{version}/
%{_mandir}/man[145]/[a-z]*

%files devel
%{_bindir}/GraphicsMagick-config
%{_bindir}/GraphicsMagickWand-config
%{_libdir}/libGraphicsMagick.so
%{_libdir}/libGraphicsMagickWand.so
%{_libdir}/pkgconfig/GraphicsMagick.pc
%{_libdir}/pkgconfig/GraphicsMagickWand.pc
%dir %{_includedir}/GraphicsMagick/
%{_includedir}/GraphicsMagick/magick/
%{_includedir}/GraphicsMagick/wand/
%{_mandir}/man1/GraphicsMagick-config.*
%{_mandir}/man1/GraphicsMagickWand-config.*

%files doc
%dir %{_pkgdocdir}
%{_pkgdocdir}/ChangeLog*
%{_pkgdocdir}/*.txt
%{_pkgdocdir}/www/

%ldconfig_scriptlets c++

%files c++
%{_libdir}/libGraphicsMagick++%{?libQ}.so.12*

%files c++-devel
%{_bindir}/GraphicsMagick++-config
%{_includedir}/GraphicsMagick/Magick++/
%{_includedir}/GraphicsMagick/Magick++.h
%{_libdir}/libGraphicsMagick++.so
%{_libdir}/pkgconfig/GraphicsMagick++.pc
%{_mandir}/man1/GraphicsMagick++-config.*

%if 0%{?perl}
%files perl -f perl-pkg-files
%{_mandir}/man3/*
%doc PerlMagick/demo/ PerlMagick/Changelog PerlMagick/README.txt
%endif


%changelog
* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.45-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jul 07 2025 Jitka Plesnikova <jplesnik@redhat.com> - 1.3.45-4
- Perl 5.42 rebuild

* Sun Feb 02 2025 Sérgio Basto <sergio@serjux.com> - 1.3.45-3
- Rebuild for jpegxl (libjxl) 0.11.1

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.45-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Sep 24 2024 Peter Robinson <pbrobinson@fedoraproject.org> - 1.3.45-1
- Update to 1.3.45
- Enable JPEG XL and HEIF support
- Drop EOL releases and ancient obsoletes
- Minor spec modifications

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.42-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jun 10 2024 Jitka Plesnikova <jplesnik@redhat.com> - 1.3.42-2
- Perl 5.40 rebuild

* Wed Feb 28 2024 Orion Poplawski <orion@nwra.com> - 1.3.42-1
- Update to 1.3.42 (FTBFS bz#2264352)

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.40-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.40-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jan 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.40-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Nov 28 2023 Orion Poplawski <orion@nwra.com> - 1.3.40-4
- Rebuild for jasper 4.1

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.40-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jul 11 2023 Jitka Plesnikova <jplesnik@redhat.com> - 1.3.40-2
- Perl 5.38 rebuild

* Fri Feb 17 2023 Rex Dieter <rdieter@fedoraproject.org> 1.3.40-1
- 1.3.40

* Wed Jan 18 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.38-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Oct 31 2022 David King <amigadave@amigadave.com> - 1.3.38-4
- Rebuild against libxml2 (#2138022)

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.38-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon May 30 2022 Jitka Plesnikova <jplesnik@redhat.com> - 1.3.38-2
- Perl 5.36 rebuild

* Mon Mar 28 2022 Rex Dieter <rdieter@fedoraproject.org> - 1.3.38-1
- 1.3.38 (#2068787)

* Mon Feb 28 2022 Neal Gompa <ngompa@fedoraproject.org> - 1.3.37-1
- 1.3.37 (#2031567)

* Sun Feb 13 2022 Josef Ridky <jridky@redhat.com> - 1.3.36-8
- Rebuilt for libjasper.so.6

* Mon Jan 24 2022 Timm Bäder <tbaeder@redhat.com> - 1.3.36-7
- Disable automatic .la file removal
- https://fedoraproject.org/wiki/Changes/RemoveLaFiles

* Wed Jan 19 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.36-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.36-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 1.3.36-4
- Perl 5.34 rebuild

* Mon Jan 25 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.36-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jan 25 2021 Rex Dieter <rdieter@fedoraproject.org> - 1.3.36-2
- fix bundled urw font install (#1911008)

* Wed Dec 30 2020 Rex Dieter <rdieter@fedoraproject.org> - 1.3.36-1
- 1.3.36
- fix urw font path, Requires: urw-base35-fonts-legacy (#1847187)
- bundle urw fonts on epel8+ (no urw-base3-fonts-legacy provided)

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.35-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jun 22 2020 Jitka Plesnikova <jplesnik@redhat.com> - 1.3.35-2
- Perl 5.32 rebuild

* Thu Feb 27 2020 Rex Dieter <rdieter@fedoraproject.org> - 1.3.35-1
- 1.3.35

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.34-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Dec 30 2019 Rex Dieter <rdieter@fedoraproject.org> - 1.3.34-1
- 1.3.34

* Sat Aug 17 2019 Rex Dieter <rdieter@fedoraproject.org> - 1.3.33-1
- 1.3.33
- use %%perl feature macro (instead of %%flatpak) everywhere

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.32-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Jul 17 2019 Kalev Lember <klember@redhat.com> - 1.3.32-2
- Disable perl support for flatpak builds

* Mon Jun 17 2019 Rex Dieter <rdieter@fedoraproject.org> - 1.3.32-1
- 1.3.32

* Thu May 30 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.3.31-6
- Perl 5.30 rebuild

* Fri Feb 01 2019 Caolán McNamara <caolanm@redhat.com> - 1.3.31-5
- Rebuilt for fixed libwmf soname

* Thu Jan 31 2019 Kalev Lember <klember@redhat.com> - 1.3.31-4
- Rebuilt for libwmf soname bump

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.31-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Dec 05 2018 Rex Dieter <rdieter@fedoraproject.org> - 1.3.31-2
- GraphicsMagic-perl 1.3.31 is broken (#1655294)

* Tue Nov 20 2018 Rex Dieter <rdieter@fedoraproject.org> - 1.3.31-1
- GraphicsMasgick-1.3.31

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.30-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sun Jul 01 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.3.30-2
- Perl 5.28 rebuild

* Sun Jul 01 2018 Rex Dieter <rdieter@fedoraproject.org> - 1.3.30-1
- GraphicsMagick-1.3.30

* Wed Jun 27 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.3.29-2
- Perl 5.28 rebuild

* Wed May 02 2018 Rex Dieter <rdieter@fedoraproject.org> - 1.3.29-1
- 1.3.29 (#1574031])

* Wed Mar 07 2018 Rex Dieter <rdieter@fedoraproject.org> - 1.3.28-4
- BR: gcc-c++, %%make_build %%make_install %%ldconfig_scriptlets

* Fri Feb 16 2018 Rex Dieter <rdieter@fedoraproject.org> - 1.3.28-3
- use %%ldconfig_scriptlets
- s/libungif/giflib

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.28-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Jan 22 2018 Rex Dieter <rdieter@fedoraproject.org> - 1.3.28-1
- 1.3.28

* Mon Dec 11 2017 Rex Dieter <rdieter@fedoraproject.org> - 1.3.27-1
- 1.3.27

* Sat Aug 12 2017 Ville Skyttä <ville.skytta@iki.fi> - 1.3.26-10
- Own doc dir

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.26-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Sun Jul 30 2017 Florian Weimer <fweimer@redhat.com> - 1.3.26-8
- Rebuild with binutils fix for ppc64le (#1475636)

* Thu Jul 27 2017 Rex Dieter <rdieter@fedoraproject.org> - 1.3.26-7
- 2017-11643 (#1475497)

* Thu Jul 27 2017 Rex Dieter <rdieter@fedoraproject.org> - 1.3.26-6
- CVE-2017-11102 (#1473728)
- CVE-2017-11139 (#1473739)
- CVE-2017-11140 (#1473750)
- CVE-2017-11636 (#1475456)
- CVE-2017-11637 (#1475452)
- CVE-2017-11638 (#1475708)
- CVE-2017-11641 (#1475489)

* Thu Jul 27 2017 Rex Dieter <rdieter@fedoraproject.org> - 1.3.26-5
- .spec cleanup, drop deprecated stuff
- update filtering
- restore %%check

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.26-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jul 19 2017 Rex Dieter <rdieter@fedoraproject.org> - 1.3.26-3
- CVE-2017-11403 (#1472214)

* Fri Jul 07 2017 Igor Gnatenko <ignatenko@redhat.com> - 1.3.26-2
- Rebuild due to bug in RPM (RHBZ #1468476)

* Wed Jul 05 2017 Rex Dieter <rdieter@fedoraproject.org> - 1.3.26-1
- 1.3.26
- CVE-2017-10794 (#1467655)
- CVE-2017-10799 (#1467372)
- CVE-2017-10800 (#1467381)

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.3.25-7
- Perl 5.26 rebuild

* Thu Mar 02 2017 Rex Dieter <rdieter@fedoraproject.org> - 1.3.25-6
- CVE-2017-6335 (#1427975)

* Thu Mar 02 2017 Rex Dieter <rdieter@fedoraproject.org> - 1.3.25-5
- CVE-2016-7800 (#1381148)
- CVE-2016-7996, CVE-2016-7997 (#1383223)
- CVE-2016-8682, CVE-2016-8683, CVE-2016-8684 (#1385583)

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.25-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 01 2017 Sandro Mani <manisandro@gmail.com> - 1.3.25-3
- Rebuild (libwebp)

* Thu Dec 01 2016 Orion Poplawski <orion@cora.nwra.com> - 1.3.25-2
- Rebuild for jasper 2.0

* Thu Sep 08 2016 Rex Dieter <rdieter@fedoraproject.org> - 1.3.25-1
- 1.3.25
- -doc: fix case where %%licensedir is undefined

* Mon May 30 2016 Rex Dieter <rdieter@fedoraproject.org> - 1.3.24-1
- 1.3.24

* Sat May 14 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.3.23-6
- Perl 5.24 rebuild

* Fri Mar 04 2016 Rex Dieter <rdieter@fedoraproject.org> - 1.3.23-5
- LCMS support broken in GraphicsMagick 1.3.23 (#1314898)
- simplify .spec conditionals (EOL fedora releases mostly)

* Mon Feb 08 2016 Rex Dieter <rdieter@fedoraproject.org> - 1.3.23-4
- make .spec el5/el6-compatible again

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.23-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Dec 28 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 1.3.23-2
- Rebuilt for libwebp soname bump

* Sat Nov 07 2015 Rex Dieter <rdieter@fedoraproject.org> 1.3.23-1
- 1.3.23

* Sun Oct 04 2015 Rex Dieter <rdieter@fedoraproject.org> 1.3.22-1
- 1.3.22, filter provides

* Tue Jun 16 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.21-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.3.21-3
- Perl 5.22 rebuild

* Fri Apr 24 2015 Orion Poplawski <orion@cora.nwra.com> - 1.3.21-2
- Rebuild for gcc 5 C++11 again

* Mon Mar 09 2015 Rex Dieter <rdieter@fedoraproject.org> 1.3.21-1
- 1.3.21

* Wed Feb 18 2015 Orion Poplawski <orion@cora.nwra.com> - 1.3.20-5
- Rebuild for gcc 5 C++11

* Thu Aug 28 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.3.20-4
- Perl 5.20 rebuild

* Thu Aug 28 2014 Rex Dieter <rdieter@fedoraproject.org> 1.3.20-3
- go back to original L%02d format variant

* Mon Aug 25 2014 Rex Dieter <rdieter@fedoraproject.org> 1.3.20-2
- better fix for CVE-2014-1947 (#1064098,#1083082)

* Wed Aug 20 2014 Rex Dieter <rdieter@fedoraproject.org> 1.3.20-1
- 1.3.20, CVE-2014-1947 (#1064098,#1083082)

* Fri Aug 15 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.19-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Wed Aug 13 2014 Orion Poplawski <orion@cora.nwra.com> - 1.3.19-8
- Rebuild for libjbig soname bump

* Fri Jun 06 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.19-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun May 11 2014 Rex Dieter <rdieter@fedoraproject.org> 1.3.19-6
- handle upgrade path for introduction of -doc subpkg in 1.3.19-4

* Mon Feb 03 2014 Remi Collet <remi@fedoraproject.org> - 1.3.19-5
- upstream patch, drop debug output (#1060665)

* Sat Jan 25 2014 Ville Skyttä <ville.skytta@iki.fi> - 1.3.19-4
- Split docs into -doc subpackage, drop README.txt (#1056306).
- Drop no longer needed BrowseDelegateDefault modification.
- Convert docs to UTF-8.

* Thu Jan 09 2014 Rex Dieter <rdieter@fedoraproject.org> 1.3.19-3
- ppc64le is a multilib arch (#1051208)

* Wed Jan 01 2014 Rex Dieter <rdieter@fedoraproject.org> 1.3.19-2
- BR: jbigkit, libwebp, xdg-utils, xz

* Wed Jan 01 2014 Rex Dieter <rdieter@fedoraproject.org> 1.3.19-1
- 1.3.19 (#1047676)

* Tue Oct 15 2013 Rex Dieter <rdieter@fedoraproject.org> 1.3.18-5
- trim changelog

* Fri Aug 02 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.18-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 1.3.18-3
- Perl 5.18 rebuild

* Wed Jun 26 2013 Rex Dieter <rdieter@fedoraproject.org> 1.3.18-2
- GraphicsMagick needs to recognize aarch64 as 64bit arch (#978351)

* Mon Mar 11 2013 Rex Dieter <rdieter@fedoraproject.org> - 1.3.18-1
- 1.3.18 (#920064)
- add %%rhel conditionals

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.17-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jan 18 2013 Adam Tkac <atkac redhat com> - 1.3.17-3
- rebuild due to "jpeg8-ABI" feature drop

* Fri Dec 21 2012 Adam Tkac <atkac redhat com> - 1.3.17-2
- rebuild against new libjpeg

* Tue Oct 16 2012 Rex Dieter <rdieter@fedoraproject.org> - 1.3.17-1
- GraphicsMagick-1.3.17 (#866377)
- GraphicsMagick 1.3.13 update breaks some PNGs (#788246)
- --enable-quantum-library-names on f19+

* Mon Aug 20 2012 Rex Dieter <rdieter@fedoraproject.org> 1.3.16-5
- CVE-2012-3438 GraphicsMagick: png_IM_malloc() size argument (#844106, #844107)

* Mon Aug 20 2012 Rex Dieter <rdieter@fedoraproject.org> 1.3.16-4
- link GraphicsMagick against lcms2 instead of lcms1 (#849778)

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.16-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 27 2012 Petr Pisar <ppisar@redhat.com> - 1.3.16-2
- Perl 5.16 rebuild

* Sun Jun 24 2012 Rex Dieter <rdieter@fedoraproject.org>
- 1.3.16-1
- GraphicsMagick-1.3.16
- GraphicsMagick-devel and GraphicsMagick-c++-devel multilib conflict (#566361)

* Mon Jun 11 2012 Petr Pisar <ppisar@redhat.com> - 1.3.15-3
- Perl 5.16 rebuild

* Tue May 08 2012 Rex Dieter <rdieter@fedoraproject.org> 1.3.15-2
- rebuild (libtiff)

* Sat Apr 28 2012 Rex Dieter <rdieter@fedoraproject.org> 1.3.15-1
- 1.3.15

* Sun Feb 26 2012 Rex Dieter <rdieter@fedoraproject.org> 1.3.14-1
- 1.3.14

* Mon Jan 23 2012 Rex Dieter <rdieter@fedoraproject.org> 1.3.13-4
- -devel: omit seemingly extraneous dependencies

* Mon Jan 23 2012 Rex Dieter <rdieter@fedoraproject.org> 1.3.13-3
- BR: perl(ExtUtils::MakeMaker)

* Mon Jan 23 2012 Rex Dieter <rdieter@fedoraproject.org> 1.3.13-2
- Bad font configuration (#783906)
- re-introduce perl_linkage patch, fixes %%check

* Thu Jan 12 2012 Rex Dieter <rdieter@fedoraproject.org> 1.3.13-1
- 1.3.13

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.12-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 1.3.12-7
- Rebuild for new libpng

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.3.12-6
- Perl mass rebuild

* Fri Jun 10 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.3.12-5
- Perl 5.14 mass rebuild

* Tue Apr 26 2011 Rex Dieter <rdieter@fedoraproject.org> 1.3.12-4
- delegates.mgk could use some care (#527117)
- -perl build is bad (#527143)
- wrong default font paths (#661664)
- need for 16-bit support, f16+ for now (#699414)
- tighten subpkg deps via %%_isa

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.12-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jun 01 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.3.12-2
- Mass rebuild with perl-5.12.0

* Mon Mar 08 2010 Rex Dieter <rdieter@fedoraproject.org> - 1.3.12-1
- GraphicsMagick-1.3.12

* Tue Feb 23 2010 Rex Dieter <rdieter@fedoraproject.org> - 1.3.11-1
- GraphicsMagick-1.3.11

* Mon Dec 28 2009 Rex Dieter <rdieter@fedoraproject.org> - 1.3.7-4
- CVE-2009-1882 (#503017)

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 1.3.7-3
- rebuild against perl 5.10.1

* Fri Nov 06 2009 Rex Dieter <rdieter@fedoraproject.org> - 1.3.7-2
- cleanup/uncruftify .spec

* Thu Sep 17 2009 Rex Dieter <rdieter@fedoraproject.org> - 1.3.7-1
- GraphicsMagick-1.3.7

* Mon Aug  3 2009 Ville Skyttä <ville.skytta at iki.fi> - 1.3.6-2
- Use lzma-compressed upstream source tarball.

* Wed Jul 29 2009 Rex Dieter <rdieter@fedoraproject.org> 1.3.6-1
- GraphicsMagick-1.3.6

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jun 30 2009 Rex Dieter <rdieter@fedoraproject.org> - 1.3.5-1
- GraphicsMagick-1.3.5, ABI break (#487605)
- --without-libgs (for now, per upstream advice)
- BR: jasper-devel

* Tue Jun 30 2009 Rex Dieter <rdieter@fedoraproject.org> - 1.1.15-1
- GraphicsMagick-1.1.15
- fix BuildRoot
- multiarch conflicts in GraphicsMagick (#341381)
- broken -L in GraphicsMagick.pc (#456466)
- %%files: track sonames

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.14-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Sep 11 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.1.14-3
- own all files properly

* Thu Sep 11 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.1.14-2
- turns out we do need gcc43 patch

* Thu Sep 11 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.1.14-1
- update to 1.1.14
- fix perl issue (bz 454087)

* Sun Jun 01 2008 Dennis Gilmore <dennis@ausil.us> - 1.1.10-4
- sparc64 is a 64 bit arch

* Mon Feb 11 2008 Andreas Thienemann <andreas@bawue.net> - 1.1.10-3
- Added patch to include cstring instead of string, fixing gcc4.3 build issue

* Mon Feb 11 2008 Andreas Thienemann <andreas@bawue.net> - 1.1.10-2
- Rebuilt against gcc 4.3

* Mon Jan 28 2008 Andreas Thienemann <andreas@bawue.net> - 1.1.10-1
- Upgraded to 1.1.10
- Fixed linking problem with the Perl module. #365901

* Wed Aug 29 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> - 1.1.8-3
- Rebuild for selinux ppc32 issue.

* Sun Jul 29 2007 Andreas Thienemann <andreas@bawue.net> - 1.1.8-2
- Building without gslib support as it results in segfaults.

* Sat Jul 28 2007 Andreas Thienemann <andreas@bawue.net> - 1.1.8-1
- Update to new maintainance release 1.1.8

* Wed Mar 07 2007 Andreas Thienemann <andreas@bawue.net> - 1.1.7-7
- Fix potential CVE-2007-0770 issue.
- Added perl-devel BuildReq

* Fri Dec 01 2006 Rex Dieter <rexdieter[AT]users.sf.net> - 1.1.7-6
- *really* fix magick_config-64.h (bug #217959)
- make buildable on rhel4 too.

* Fri Dec 01 2006 Rex Dieter <rexdieter[AT]users.sf.net> - 1.1.7-5
- fix magick-config-64.h (bug #217959)

* Sun Nov 29 2006 Andreas Thienemann <andreas@bawue.net> - 1.1.7-3
- Fixed devel requirement.

* Sun Nov 26 2006 Andreas Thienemann <andreas@bawue.net> - 1.1.7-2
- Fixed various stuff

* Mon Jul 24 2006 Andreas Thienemann <andreas@bawue.net> - 1.1.7-1
- Initial Package for FE based on ImageMagick.spec
