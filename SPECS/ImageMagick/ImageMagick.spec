# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%bcond_without tests

%bcond_without libheif

%if 0%{?flatpak}
%bcond_with perl
%else
%bcond_without perl
%endif

# Disable automatic .la file removal
%global __brp_remove_la_files %nil

Name:           ImageMagick
Epoch:          1
Version:        7.1.1.47
Release:        7%{?dist}
Summary:        An X application for displaying and manipulating images

%global VER %(foo=%{version}; echo ${foo:0:5})
%global Patchlevel %(foo=%{version}; echo ${foo:6})
%global libsover 10
%global subsover VERS_10.0
%global libcxxsover 5
License:        ImageMagick
URL:            https://imagemagick.org/
Source0:        https://imagemagick.org/archive/releases/%{name}-%{VER}-%{Patchlevel}.tar.xz
Source1:        https://imagemagick.org/archive/releases/%{name}-%{VER}-%{Patchlevel}.tar.xz.asc
Source2:        ImageMagick.keyring

BuildRequires:  pkgconfig(bzip2)
BuildRequires:  pkgconfig(freetype2)
BuildRequires:  pkgconfig(libjpeg)
BuildRequires:  pkgconfig(libpng)
BuildRequires:  pkgconfig(libtiff-4)
BuildRequires:  giflib-devel
BuildRequires:  pkgconfig(zlib)
%if %{with perl}
BuildRequires:  perl-devel >= 5.8.1
BuildRequires:  perl-generators
%endif
BuildRequires:  libgs-devel
# Used in configure to check device availability
BuildRequires:  ghostscript
BuildRequires:  pkgconfig(ddjvuapi)
BuildRequires:  pkgconfig(libwmf)
BuildRequires:  pkgconfig(jasper)
BuildRequires:  libtool-ltdl-devel
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xext)
BuildRequires:  pkgconfig(xt)
BuildRequires:  pkgconfig(lcms2)
BuildRequires:  pkgconfig(libxml-2.0)
BuildRequires:  pkgconfig(librsvg-2.0)
%if 0%{?rhel} && 0%{?rhel} < 9
BuildRequires:  pkgconfig(IlmBase), pkgconfig(OpenEXR) < 2.5.6
%else
BuildRequires:  pkgconfig(OpenEXR)
%endif
BuildRequires:  pkgconfig(fftw3)
BuildRequires:  pkgconfig(libwebp)
BuildRequires:  jbigkit-devel
BuildRequires:  pkgconfig(libjxl)
BuildRequires:  pkgconfig(libopenjp2) >= 2.1.0
BuildRequires:  pkgconfig(libcgraph) >= 2.9.0
BuildRequires:  pkgconfig(raqm)
%if 0%{?fedora} || 0%{?rhel} > 8
BuildRequires:  pkgconfig(lqr-1)
%endif
BuildRequires:  pkgconfig(libraw) >= 0.14.8
# Ultra HDR support available of Fedora 43 and onward
%if 0%{?fedora} >= 43
BuildRequires:  pkgconfig(libuhdr) >= 1.3.0
%endif
BuildRequires:  pkgconfig(libzstd)
BuildRequires:  pkgconfig(libzip) >= 1.0.0
BuildRequires:  pkgconfig(pango) >= 1.28.1
BuildRequires:  pkgconfig(pangocairo) >= 1.28.1
BuildRequires:  urw-base35-fonts-devel
BuildRequires:  autoconf automake gcc gcc-c++
BuildRequires:  make
BuildRequires:  gnupg2
# for doc
BuildRequires:  doxygen

Requires:       %{name}-libs%{?_isa} = %{epoch}:%{version}-%{release}
# allow smooth upgrade for 3rd party repository
# providing latest version/soname as ImageMagick7
Obsoletes:      %{name}7            < %{epoch}:%{version}-%{release}
Provides:       %{name}7            = %{epoch}:%{version}-%{release}

%description
ImageMagick is an image display and manipulation tool for the X
Window System. ImageMagick can read and write JPEG, TIFF, PNM, GIF,
and Photo CD image formats. It can resize, rotate, sharpen, color
reduce, or add special effects to an image, and when finished you can
either save the completed work in the original format or a different
one. ImageMagick also includes command line programs for creating
animated or transparent .gifs, creating composite images, creating
thumbnail images, and more.

ImageMagick is one of your choices if you need a program to manipulate
and display images. If you want to develop your own applications
which use ImageMagick code or APIs, you need to install
ImageMagick-devel as well.


%package devel
Summary:        Library links and header files for ImageMagick app development
Requires:       %{name}%{?_isa} = %{epoch}:%{version}-%{release}
Requires:       %{name}-libs%{?_isa} = %{epoch}:%{version}-%{release}
Obsoletes:      %{name}7-devel       < %{epoch}:%{version}-%{release}
Provides:       %{name}7-devel       = %{epoch}:%{version}-%{release}

%description devel
ImageMagick-devel contains the library links and header files you'll
need to develop ImageMagick applications. ImageMagick is an image
manipulation program.

If you want to create applications that will use ImageMagick code or
APIs, you need to install ImageMagick-devel as well as ImageMagick.
You do not need to install it if you just want to use ImageMagick,
however.


%package libs
Summary: ImageMagick libraries to link with
Obsoletes: %{name}7-libs < %{epoch}:%{version}-%{release}
Provides:  %{name}7-libs = %{epoch}:%{version}-%{release}
# These may be used for some functions
Recommends: urw-base35-fonts
# default font is OpenSans-Regular
Recommends: open-sans-fonts

%description libs
This packages contains a shared libraries to use within other applications.


%package djvu
Summary: DjVu plugin for ImageMagick
Requires: %{name}-libs%{?_isa} = %{epoch}:%{version}-%{release}
Obsoletes: %{name}7-djvu       < %{epoch}:%{version}-%{release}
Provides:  %{name}7-djvu       = %{epoch}:%{version}-%{release}

%description djvu
This packages contains a plugin for ImageMagick which makes it possible to
save and load DjvU files from ImageMagick and libMagickCore using applications.


%if %{with libheif}
%package heic
Summary: HEIC plugin for ImageMagick
BuildRequires:  pkgconfig(libheif) >= 1.4.0
Requires:       %{name}-libs%{?_isa} = %{epoch}:%{version}-%{release}

%description heic
This packages contains a plugin for ImageMagick which makes it possible to
save and load HEIC files from ImageMagick and libMagickCore using applications.
%endif


%package doc
Summary: ImageMagick html documentation
Obsoletes: %{name}7-doc < %{epoch}:%{version}-%{release}
Provides:  %{name}7-doc = %{epoch}:%{version}-%{release}

%description doc
ImageMagick documentation, this package contains usage (for the
commandline tools) and API (for the libraries) documentation in html format.
Note this documentation can also be found on the ImageMagick website:
http://www.imagemagick.org/


%if %{with perl}
%package perl
Summary:        ImageMagick perl bindings
Requires:       %{name}-libs%{?_isa} = %{epoch}:%{version}-%{release}
Obsoletes:      %{name}7-perl        < %{epoch}:%{version}-%{release}
Provides:       %{name}7-perl        = %{epoch}:%{version}-%{release}

%description perl
Perl bindings to ImageMagick.

Install ImageMagick-perl if you want to use any perl scripts that use
ImageMagick.
%endif


%package c++
Summary:        ImageMagick Magick++ library (C++ bindings)
Requires:       %{name}-libs%{?_isa} = %{epoch}:%{version}-%{release}
Obsoletes:      %{name}7-c++         < %{epoch}:%{version}-%{release}
Provides:       %{name}7-c++         = %{epoch}:%{version}-%{release}

%description c++
This package contains the Magick++ library, a C++ binding to the ImageMagick
graphics manipulation library.

Install ImageMagick-c++ if you want to use any applications that use Magick++.


%package c++-devel
Summary:        C++ bindings for the ImageMagick library
Requires:       %{name}-c++%{?_isa} = %{epoch}:%{version}-%{release}
Requires:       %{name}-devel%{?_isa} = %{epoch}:%{version}-%{release}
Obsoletes:      %{name}7-c++-devel    < %{epoch}:%{version}-%{release}
Provides:       %{name}7-c++-devel    = %{epoch}:%{version}-%{release}

%description c++-devel
ImageMagick-devel contains the static libraries and header files you'll
need to develop ImageMagick applications using the Magick++ C++ bindings.
ImageMagick is an image manipulation program.

If you want to create applications that will use Magick++ code
or APIs, you'll need to install ImageMagick-c++-devel, ImageMagick-devel and
ImageMagick.
You don't need to install it if you just want to use ImageMagick, or if you
want to develop/compile applications using the ImageMagick C interface,
however.


%prep
%{gpgverify} --keyring=%{SOURCE2} --signature=%{SOURCE1} --data=%{SOURCE0}
%autosetup -p1 -n %{name}-%{VER}-%{Patchlevel}


%build
autoconf -f -i -v
# Reduce thread contention, upstream sets this flag for Linux hosts
export CFLAGS="%{optflags} -DIMPNG_SETJMP_IS_THREAD_SAFE"
%configure \
        --enable-shared \
        --disable-static \
        --with-modules \
%if %{with perl}
        --with-perl \
        --with-perl-options="INSTALLDIRS=vendor %{?perl_prefix} CC='%__cc -L$PWD/magick/.libs' LDDLFLAGS='-shared -L$PWD/magick/.libs'" \
%endif
        --with-x \
        --with-threads \
        --with-magick_plus_plus \
        --with-gslib \
        --with-pango \
        --with-fftw \
        --with-wmf \
        --with-webp \
        --with-openexr \
        --with-rsvg \
        --with-xml \
        --with-urw-base35-font-dir="%{urw_base35_fontpath}" \
        --without-dps \
        --enable-openmp \
        --without-gcc-arch \
        --with-jbig \
        --with-jxl \
        --with-openjp2 \
        --with-raw \
%if 0%{?fedora} || 0%{?rhel} > 8
        --with-lqr \
%if 0%{?fedora} >= 43
        --with-uhdr \
%endif
%endif
        --with-gvc \
        --with-raqm \
%if %{with libheif}
           --with-heic \
%endif

# Do *NOT* use %%{?_smp_mflags}, this causes PerlMagick to be silently misbuild
make
# Generate API docs
make html-local


%install
%make_install

# Compatibility symlinks for headers for IM6->IM7 transition
ln -sr %{buildroot}%{_includedir}/%{name}-7/MagickCore %{buildroot}%{_includedir}/%{name}-7/magick
ln -sr %{buildroot}%{_includedir}/%{name}-7/MagickWand %{buildroot}%{_includedir}/%{name}-7/wand

# Do NOT remove .la files for codecs
# https://bugzilla.opensuse.org/show_bug.cgi?id=579798
# Delete *ONLY* _libdir/*.la files! .la files used internally to handle plugins - BUG#185237!!!
rm %{buildroot}%{_libdir}/*.la

%if %{with perl}
# fix weird perl module permissions
chmod 755 %{buildroot}%{perl_vendorarch}/auto/Image/Magick/Q16HDRI/Q16HDRI.so

# perlmagick: fix perl path of demo files
%{__perl} -MExtUtils::MakeMaker -e 'MY->fixin(@ARGV)' PerlMagick/demo/*.pl

# perlmagick: cleanup various perl tempfiles from the build which get installed
find %{buildroot} -name "*.bs" |xargs rm -f
find %{buildroot} -name ".packlist" |xargs rm -f
find %{buildroot} -name "perllocal.pod" |xargs rm -f

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

# fix multilib issues: Rename the provided file with platform-bits in name.
# Create platform independent file inplace of the provided one and conditionally
# include the required one.
# $1 - filename.h to process.
function multilibFileVersions(){
mv $1 ${1%%.h}-%{__isa_bits}.h

local basename=$(basename $1)

cat >$1 <<EOF
#include <bits/wordsize.h>

#if __WORDSIZE == 32
# include "${basename%%.h}-32.h"
#elif __WORDSIZE == 64
# include "${basename%%.h}-64.h"
#else
# error "unexpected value for __WORDSIZE macro"
#endif
EOF
}

multilibFileVersions %{buildroot}%{_includedir}/%{name}-7/MagickCore/magick-config.h
multilibFileVersions %{buildroot}%{_includedir}/%{name}-7/MagickCore/magick-baseconfig.h
multilibFileVersions %{buildroot}%{_includedir}/%{name}-7/MagickCore/version.h

find %{buildroot} -type f -name "*%{subsover}*" >/dev/null 2>&1
if [ $? -ne 0 ]; then
    echo Error: No files containing %{subsover} found
    exit 1
fi

%check
%if %{with tests}
export LD_LIBRARY_PATH=%{buildroot}/%{_libdir}
%make_build check
%endif
rm PerlMagick/demo/Generic.ttf


%files
%doc NOTICE AUTHORS.txt
%license LICENSE
%{_bindir}/[a-z]*
%{_mandir}/man[145]/[a-z]*
%{_mandir}/man1/%{name}.*

%files libs
%doc NOTICE AUTHORS.txt
%license LICENSE
%{_libdir}/libMagickCore-7.Q16HDRI.so.%{libsover}{,.*}
%{_libdir}/libMagickWand-7.Q16HDRI.so.%{libsover}{,.*}
%{_libdir}/%{name}-%{VER}
%{_datadir}/%{name}-7
%exclude %{_libdir}/%{name}-%{VER}/modules-Q16HDRI/coders/djvu.*
%if %{with libheif}
%exclude %{_libdir}/%{name}-%{VER}/modules-Q16HDRI/coders/heic.*
%endif
%dir %{_sysconfdir}/%{name}-7
%config(noreplace) %{_sysconfdir}/%{name}-7/*.xml

%files devel
%{_bindir}/MagickCore-config
%{_bindir}/MagickWand-config
%{_libdir}/libMagickCore-7.Q16HDRI.so
%{_libdir}/libMagickWand-7.Q16HDRI.so
%{_libdir}/pkgconfig/MagickCore.pc
%{_libdir}/pkgconfig/MagickCore-7.Q16HDRI.pc
%{_libdir}/pkgconfig/ImageMagick.pc
%{_libdir}/pkgconfig/ImageMagick-7.Q16HDRI.pc
%{_libdir}/pkgconfig/MagickWand.pc
%{_libdir}/pkgconfig/MagickWand-7.Q16HDRI.pc
%dir %{_includedir}/%{name}-7
%{_includedir}/%{name}-7/MagickCore/
%{_includedir}/%{name}-7/MagickWand/
%{_includedir}/%{name}-7/magick
%{_includedir}/%{name}-7/wand
%{_mandir}/man1/MagickCore-config.*
%{_mandir}/man1/MagickWand-config.*

%files djvu
%{_libdir}/%{name}-%{VER}/modules-Q16HDRI/coders/djvu.*

%if %{with libheif}
%files heic
%{_libdir}/%{name}-%{VER}/modules-Q16HDRI/coders/heic.*
%endif

%files doc
%doc %{_datadir}/doc/%{name}-7

%files c++
%doc Magick++/AUTHORS
%license Magick++/LICENSE
%{_libdir}/libMagick++-7.Q16HDRI.so.%{libcxxsover}{,.*}

%files c++-devel
%doc Magick++/demo
%{_bindir}/Magick++-config
%{_includedir}/%{name}-7/Magick++/
%{_includedir}/%{name}-7/Magick++.h
%{_libdir}/libMagick++-7.Q16HDRI.so
%{_libdir}/pkgconfig/Magick++.pc
%{_libdir}/pkgconfig/Magick++-7.Q16HDRI.pc
%{_mandir}/man1/Magick++-config.*

%if %{with perl}
%files perl -f perl-pkg-files
%{_mandir}/man3/*
%doc PerlMagick/demo/ PerlMagick/Changelog PerlMagick/README.txt
%endif

%changelog
* Sat Jan 31 2026 Luya Tshimbalanga <luya@fedoraproject.org> - 1:7.1.1.47-7
- Enable uhdr (Ultra HDR) support
- Resolves: rhbz#2343774

* Fri Jan 16 2026 Fedora Release Engineering <releng@fedoraproject.org> - 1:7.1.1.47-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Fri Jan 16 2026 Fedora Release Engineering <releng@fedoraproject.org> - 1:7.1.1.47-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Thu Oct 09 2025 Jaroslav Škarvada <jskarvad@redhat.com> - 1:7.1.1.47-4
- Rebuilt for new graphviz

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1:7.1.1.47-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jul 07 2025 Jitka Plesnikova <jplesnik@redhat.com> - 1:7.1.1.47-2
- Perl 5.42 rebuild

* Sun Mar 30 2025 Packit <hello@packit.dev> - 1:7.1.1.47-1
- Update to version 7.1.1.47
- Resolves: rhbz#2356054

* Wed Mar 19 2025 Packit <hello@packit.dev> - 1:7.1.1.46-1
- Update to version 7.1.1.46
- Resolves: rhbz#2353310

* Mon Mar 10 2025 Packit <hello@packit.dev> - 1:7.1.1.45-1
- Update to version 7.1.1.45
- Resolves: rhbz#2351049

* Sun Feb 23 2025 Packit <hello@packit.dev> - 1:7.1.1.44-1
- Update to version 7.1.1.44
- Resolves: rhbz#2347163

* Sun Feb 02 2025 Sérgio Basto <sergio@serjux.com> - 1:7.1.1.43-3
- Rebuild on side-tag

* Sun Feb 02 2025 Sérgio Basto <sergio@serjux.com> - 1:7.1.1.43-2
- Rebuild for jpegxl (libjxl) 0.11.1

* Tue Jan 28 2025 Packit <hello@packit.dev> - 1:7.1.1.43-1
- Update to version 7.1.1.43
- Resolves: rhbz#2334042
- Fix files of ImageMagick-heic in 2 sub-packages (#2330605)

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1:7.1.1.41-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sun Nov 17 2024 Packit <hello@packit.dev> - 1:7.1.1.41-1
- Update to version 7.1.1.41
- Resolves: rhbz#2326736

* Thu Nov 14 2024 Sérgio Basto <sergio@serjux.com> - 1:7.1.1.40-2
- Revert map changes breaking ABI

* Sat Nov 09 2024 Packit <hello@packit.dev> - 1:7.1.1.40-1
- Update to version 7.1.1.40
- Resolves: rhbz#2324946

* Fri Oct 25 2024 Packit <hello@packit.dev> - 1:7.1.1.39-1
- Update to version 7.1.1.39
- Resolves: rhbz#2316866

* Fri Sep 06 2024 Sérgio Basto <sergio@serjux.com> - 1:7.1.1.38-1
- Update ImageMagick to 7.1.1.38 (#2293863)

* Thu Aug 08 2024 Sérgio Basto <sergio@serjux.com> - 1:7.1.1.33-3
- Build with Epoch for ELN

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:7.1.1.33-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jun 17 2024 Sérgio Basto <sergio@serjux.com> - 1:7.1.1.33-1
- Update ImageMagick to 7.1.1.33 (#2259429)
- Sync with Remi's RPM

* Mon Jun 10 2024 Jitka Plesnikova <jplesnik@redhat.com> - 1:7.1.1.26-9
- Perl 5.40 rebuild

* Wed Apr 24 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 1:7.1.1.26-8
- Rebuilt for openexr 3.2.4

* Wed Mar 13 2024 Sérgio Basto <sergio@serjux.com> - 1:7.1.1.26-7
- Rebuild for jpegxl (libjxl) 0.10.2

* Wed Feb 14 2024 Sérgio Basto <sergio@serjux.com> - 1:7.1.1.26-6
- Rebuild for jpegxl (libjxl) 0.9.2 with soname bump

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:7.1.1.26-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:7.1.1.26-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jan 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:7.1.1.26-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 15 2024 Sérgio Basto <sergio@serjux.com> - 1:7.1.1.26-2
- fix PKG_CONFIG_LIBDIR

* Mon Jan 08 2024 Fedora Release Monitoring <release-monitoring@fedoraproject.org> - 1:7.1.1.26-1
- Update to 7.1.1.26 (#2239345)

* Tue Aug 22 2023 Sérgio Basto <sergio@serjux.com> - 1:7.1.1.15-1
- Update ImageMagick to 7.1.1.15 (#2217558)

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:7.1.1.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sun Jul 16 2023 Fedora Release Monitoring <release-monitoring@fedoraproject.org> - 1:7.1.1.13-1
- Update to 7.1.1.13 (#2217558)

* Tue Jul 11 2023 Jitka Plesnikova <jplesnik@redhat.com> - 1:7.1.1.11-3
- Perl 5.38 rebuild

* Sun Jun 18 2023 Sérgio Basto <sergio@serjux.com> - 1:7.1.1.11-2
- Mass rebuild for jpegxl-0.8.1

* Mon May 29 2023 Fedora Release Monitoring <release-monitoring@fedoraproject.org> - 1:7.1.1.11-1
- Update to 7.1.1.11 (#2210875)

* Mon May 22 2023 Fedora Release Monitoring <release-monitoring@fedoraproject.org> - 1:7.1.1.10-1
- Update to 7.1.1.10 (#2207788)

* Sat Apr 22 2023 Fedora Release Monitoring <release-monitoring@fedoraproject.org> - 1:7.1.1.8-1
- Update to 7.1.1.8 (#2181846)

* Mon Mar 27 2023 Luya Tshimbalanga <luya@fedoraproject.org> - 1:7.1.1.4-3
- Stop requiring ghostcripts-x11 upon request for security issue

* Thu Mar 23 2023 Kalev Lember <klember@redhat.com> - 1:7.1.1.4-2
- Fix missing epoch in ImageMagick-heic requires (#2181176)

* Wed Mar 22 2023 Sérgio Basto <sergio@serjux.com> - 1:7.1.1.4-1
- Update ImageMagick to 7.1.1.4 (#2176749)
- Add support to libheif and add html docs

* Mon Mar 13 2023 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1:7.1.0-62-2
- Backport upstream fix for GetPageGeometry misbehavior (bug 2177631)

* Thu Feb 23 2023 Sérgio Basto <sergio@serjux.com> - 1:7.1.0.62-1
- Update ImageMagick to 7.1.0.62

* Sun Jan 29 2023 Luya Tshimbalanga <luya@fedoraproject.org> - 1:7.1.0.57-4
- Actually rebuilt for ghostcripts 10.0.0

* Tue Jan 24 2023 Luya Tshimbalanga <luya@fedoraproject.org> - 1:7.1.0.57-3
- Rebuilt for ghostcripts 10.0.0

* Wed Jan 18 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:7.1.0.57-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Jan 03 2023 Neal Gompa <ngompa@fedoraproject.org> - 1:7.1.0.57-1
- Rebase to ImageMagick v7

* Thu Dec 22 2022 Sérgio Basto <sergio@serjux.com> - 1:6.9.12.70-1
- Update ImageMagick to 6.9.12.70 (#2150658)

* Tue Dec 20 2022 Gwyn Ciesla <gwync@protonmail.com> - 1:6.9.12.67-2
- LibRaw rebuild

* Mon Nov 21 2022 Sérgio Basto <sergio@serjux.com> - 1:6.9.12.67-1
- Update ImageMagick to 6.9.12.67 (#2133270)

* Tue Sep 27 2022 Sérgio Basto <sergio@serjux.com> - 1:6.9.12.64-1
- Update ImageMagick to 6.9.12.64 (#2129597)

* Tue Sep 13 2022 Sérgio Basto <sergio@serjux.com> - 1:6.9.12.63-1
- Update ImageMagick to 6.9.12.63 (#2125990)

* Wed Sep 07 2022 Sérgio Basto <sergio@serjux.com> - 1:6.9.12.62-1
- Update ImageMagick to 6.9.12.62 (#2121962)
- Fixes CVE-2021-3574 (#2124540, #2124541, #2124542)

* Sun Aug 21 2022 Sérgio Basto <sergio@serjux.com> - 1:6.9.12.61-1
- Update ImageMagick to 6.9.12.61 (#2105662)

* Thu Jul 21 2022 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1:6.9.12.58-3
- Workaround for json convertion abort (#2107201)

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:6.9.12.58-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sat Jul 09 2022 Sérgio Basto <sergio@serjux.com> - 1:6.9.12.58-1
- Update ImageMagick to 6.9.12.58 (#2105662)

* Sat Jul 09 2022 Sérgio Basto <sergio@serjux.com> - 1:6.9.12.56-1
- Update ImageMagick to 6.9.12.56 (#2105662)

* Thu Jun 16 2022 Sérgio Basto <sergio@serjux.com> - 1:6.9.12.52-1
- Update ImageMagick to 6.9.12.52 (#2092110)

* Mon May 30 2022 Jitka Plesnikova <jplesnik@redhat.com> - 1:6.9.12.50-2
- Perl 5.36 rebuild

* Sun May 29 2022 Sérgio Basto <sergio@serjux.com> - 1:6.9.12.50-1
- Update ImageMagick to 6.9.12.50 (#2087046)

* Fri May 20 2022 Sandro Mani <manisandro@gmail.com> - 1:6.9.12.48-4
- Rebuild for gdal-3.5.0 and/or openjpeg-2.5.0

* Mon May 16 2022 Sérgio Basto <sergio@serjux.com> - 1:6.9.12.48-3
- Don't use the %{?eln} macro, you should use %{?rhel} recommended by Stephen
  Gallagher

* Sun May 08 2022 Sérgio Basto <sergio@serjux.com> - 1:6.9.12.48-2
- Support eln
- add support libzst
- should we enable hdri ?

* Sun May 08 2022 Sérgio Basto <sergio@serjux.com> - 1:6.9.12.48-1
- Update ImageMagick to 6.9.12.48
- Change the way of calculte VER and Patchlevel which will fix the-new-hotness/release-monitoring.org's scratch build
- Sync with Fedora builds

* Mon Mar 28 2022 Luya Tshimbalanga <luya@fedoraproject.org> - 1:6.9.12.44-1
- New upstream release 6.9.12.44

* Wed Mar 23 2022 Luya Tshimbalanga <luya@fedoraproject.org> - 1:6.9.12.43-1
- New upstream release 6.9.12.43

* Tue Mar 15 2022 Luya Tshimbalanga <luya@fedoraproject.org> - 1:6.9.12.42-1
- New upstream release 6.9.12.42

* Thu Feb 17 2022 Luya Tshimbalanga <luya@fedoraproject.org> - 1:6.9.12.40-1
- New upstream release 6.9.12-40 (#2051040)

* Sat Jan 29 2022 Luya Tshimbalanga <luya@fedoraproject.org> - 1:6.9.12.37-1
- Update to 6.9.12.37 (#2034280)

* Mon Jan 24 2022 Timm Bäder <tbaeder@redhat.com> - 1:6.9.12.32-3
- Disable automatic .la file removal
- https://fedoraproject.org/wiki/Changes/RemoveLaFiles

* Wed Jan 19 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:6.9.12.32-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Dec 06 2021 Luya Tshimbalanga <luya@fedoraproject.org> - 1:6.9.12-32
- Update to 6.9.12-32 (#2029637)

* Tue Nov 23 2021 Sérgio Basto <sergio@serjux.com> - 1:6.9.12-31
- Update ImageMagick to 6.9.12-31 (#2025909)

* Mon Nov 22 2021 Sérgio Basto <sergio@serjux.com> - 1:6.9.12-30
- Update ImageMagick to 6.9.12-30 (#2017126)

* Sun Oct 31 2021 Fedora Release Monitoring <release-monitoring@fedoraproject.org> - 1:6.9.12-28
- Update to 6.9.12-28 (resolves #2017126)

* Tue Oct 26 2021 Fedora Release Monitoring <release-monitoring@fedoraproject.org> - 1:6.9.12-27
- Update to 6.9.12-27 (#2017126)

* Mon Oct 04 2021 Fedora Release Monitoring <release-monitoring@fedoraproject.org> - 1:6.9.12-25
- Update to 6.9.12-25 (#1869912)
- New url address
- Use pkgconfig for depending packages

* Fri Aug 27 2021 Vít Ondruch <vondruch@redhat.com> - 1:6.9.11.27-8
- Fix segfaults on s390x with rubygem-acitvestorage test suite.
  Resolves: rhbz#1993193

* Sun Aug 22 2021 Richard Shaw <hobbes1069@gmail.com> - 1:6.9.11.27-7
- Rebuild for OpenEXR/Imath 3.1.

* Tue Aug 10 2021 Richard Shaw <hobbes1069@gmail.com> - 1:6.9.11.27-6
- Rebuild for OpenEXR/Imath 3.

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:6.9.11.27-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 1:6.9.11.27-4
- Perl 5.34 rebuild

* Mon Jan 25 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:6.9.11.27-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Jan 01 2021 Richard Shaw <hobbes1069@gmail.com> - 1:6.9.11.27-2
- Rebuild for OpenEXR 2.5.3.

* Tue Aug 11 2020 Michael Cronenworth <mike@cchtml.com> - 1:6.9.11.27-1
- Update to 6.9.11.27

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:6.9.11.22-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jul  2 2020 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1:6.9.11.22-2
- Backport upstream patch to make ruby rmagick test pass (bug 1844192)

* Mon Jun 29 2020 Michael Cronenworth <mike@cchtml.com> - 1:6.9.11.22-1
- Update to 6.9.11.22

* Sat Jun 27 2020 Jitka Plesnikova <jplesnik@redhat.com> - 1:6.9.11.21-2
- Perl 5.32 re-rebuild updated packages

* Thu Jun 25 2020 Michael Cronenworth <mike@cchtml.com> - 1:6.9.11.21-1
- Update to 6.9.11.21

* Mon Jun 22 2020 Jitka Plesnikova <jplesnik@redhat.com> - 1:6.9.11.16-2
- Perl 5.32 rebuild

* Wed Jun 03 2020 Michael Cronenworth <mike@cchtml.com> - 1:6.9.11.16-1
- Update to 6.9.11.16
- Drop extra BRs on -devel package (RHBZ#1835344)

* Mon May 11 2020 Gwyn Ciesla <gwync@protonmail.com> - 1:6.9.10.86-3
- Rebuild for new LibRaw

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:6.9.10.86-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Jan 13 2020 Michael Cronenworth <mike@cchtml.com> - 1:6.9.10.86-1
- Update to 6.9.10.86

* Tue Nov 26 2019 Michael Cronenworth <mike@cchtml.com> - 1:6.9.10.75-1
- Update to 6.9.10.75

* Fri Oct 04 2019 Pete Walter <pwalter@fedoraproject.org> - 1:6.9.10.67-1
- Update to 6.9.10.67

* Sat Sep 21 2019 Pete Walter <pwalter@fedoraproject.org> - 1:6.9.10.65-1
- Update to 6.9.10.65

* Fri Sep 13 2019 Michael Cronenworth <mike@cchtml.com> - 1:6.9.10.64-1
- Update to 6.9.10.64
- Set threading option (https://src.fedoraproject.org/rpms/ImageMagick/pull-request/2)
- Enable more image formats (RHBZ#1485823)

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:6.9.10.28-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu May 30 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1:6.9.10.28-3
- Perl 5.30 rebuild

* Thu Apr 11 2019 Richard Shaw <hobbes1069@gmail.com> - 1:6.9.10.28-2
- Rebuild for OpenEXR/Ilmbase 2.3.0.

* Mon Feb 18 2019 Pete Walter <pwalter@fedoraproject.org> - 1:6.9.10.28-1
- Update to 6.9.10.28

* Mon Feb 11 2019 Pete Walter <pwalter@fedoraproject.org> - 1:6.9.10.27-1
- Update to 6.9.10-27

* Tue Feb 05 2019 Pete Walter <pwalter@fedoraproject.org> - 1:6.9.10.25-1
- Update to 6.9.10-25

* Fri Feb 01 2019 Caolán McNamara <caolanm@redhat.com> - 1:6.9.10.23-4
- Rebuilt for fixed libwmf soname

* Thu Jan 31 2019 Kalev Lember <klember@redhat.com> - 1:6.9.10.23-3
- Rebuilt for libwmf soname bump

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:6.9.10.23-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Jan 02 2019 Michael Cronenworth <mike@cchtml.com> - 1:6.9.10.23-1
- Update to 6.9.10-23

* Tue Aug 28 2018 Michael Cronenworth <mike@cchtml.com> - 1:6.9.10.10-2
- Always ship .la files for codecs

* Tue Aug 28 2018 Michael Cronenworth <mike@cchtml.com> - 1:6.9.10.10-1
- Update to 6.9.10-10

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:6.9.9.38-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1:6.9.9.38-2
- Perl 5.28 rebuild

* Mon Mar 12 2018 Michael Cronenworth <mike@cchtml.com> - 1:6.9.9.38-1
- Update to 6.9.9-38

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:6.9.9.33-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Jan 15 2018 Michael Cronenworth <mike@cchtml.com> - 1:6.9.9.33-1
- Update to 6.9.9-33
- Update ghostscript package name dependencies (RHBZ#1534655)

* Sat Dec 23 2017 Michael Cronenworth <mike@cchtml.com> - 1:6.9.9.27-1
- Update to 6.9.9-27

* Tue Nov 07 2017 Michael Cronenworth <mike@cchtml.com> - 1:6.9.9.22-1
- Update to 6.9.9-22

* Wed Oct 11 2017 Michael Cronenworth <mike@cchtml.com> - 1:6.9.9.19-1
- Update to 6.9.9-19

* Tue Sep 26 2017 Michael Cronenworth <mike@cchtml.com> - 1:6.9.9.15-1
- Update to 6.9.9-15

* Thu Sep 14 2017 Peter Walter <pwalter@fedoraproject.org> - 1:6.9.9.13-1
- Update to 6.9.9-13

* Wed Sep  6 2017 Remi Collet <remi@fedoraproject.org> -  1:6.9.9.9-3
- fix inter-package dependency using epoch
- only bump epoch in F27+

* Tue Sep 05 2017 Adam Williamson <awilliam@redhat.com> - 1:6.9.9.9-2
- Bump epoch to 1 (for F27 and Rawhide reversion from 7.0.6)

* Thu Aug 24 2017 Michael Cronenworth <mike@cchtml.com> - 6.9.9.9-1
- Update to 6.9.9-9 (for F27 and Rawhide, revert to 6.9.9-9)

* Thu Aug 24 2017 Adam Williamson <awilliam@redhat.com> - 7.0.6.9-4
- Correct versioning (patchlevel is *upstream*, not downstream)

* Thu Aug 24 2017 Dan Horák <dan[at]danny.cz> - 7.0.6-9.3
- temporarily disable 2 tests failing on big endian arches (#1484579)

* Wed Aug 23 2017 Moez Roy <moez.roy@gmail.com> - 7.0.6-9.2
- update to latest upstream

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 6.9.9.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Sun Jul 30 2017 Florian Weimer <fweimer@redhat.com> - 6.9.9.3-2
- Rebuild with binutils fix for ppc64le (#1475636)

* Thu Jul 27 2017 Kevin Fenzi <kevin@scrye.com> - 6.9.9.3-1
- Update to 6.9.9-3. Fixes bug #1299275
- Fix CVE-2017-11644 ImageMagick: Memory-Leak in ReadMATImage() coders/mat.c - bug #1475485
- Fix CVE-2017-11639 ImageMagick: heap-based buffer over-read in the WriteCIPImage() function in coders/cip.c - bug #1475470
- Fix CVE-2017-11640 ImageMagick: NULL pointer dereference in WritePTIFImage() in coders/tiff.c - bug #1475463
- Fix CVE-2017-11523 ImageMagick: Endless loop in ReadTXTImage function in coders/txt.c - bug #1474845
- Fix CVE-2017-11446 CVE-2017-11478 ImageMagick: various flaws - bug #1474363,1474391
- Fix CVE-2017-11360 ImageMagick: Resource exhaustion in ReadRLEImage function - bug #1473847
- Fix CVE-2017-11188 ImageMagick: Resource exhaustion in ReadDPXImage function in coders\dpx.c - bug #1473824
- Fix CVE-2017-11448 ImageMagick: Info leak from from uninitialized memory in ReadJPEGImage function - bug #1473801
- Fix CVE-2017-11447 ImageMagick: Memory leak in ReadSCREENSHOTImage function in coders/screenshot.c - bug #1473798
- Fix CVE-2017-11449 ImageMagick: coders/mpc.c don't validade blob sizes of stdin image input - bug #1473796
- Fix CVE-2017-11450 ImageMagick: Too short JPEG data causes denial of service in coders/jpeg.c - bug #1473774
- Fix CVE-2017-11141 ImageMagick: Memory exhaustion in ReadMATImage function in coders\mat.c - bug #1473757
- Fix CVE-2017-10928 ImageMagick: heap-based buffer over-read in the GetNextToken function - bug #1473717
- Fix CVE-2017-11352 ImageMagick: Improper EOF handling in coders/rle.c can trigger crash (Incomplete fix for CVE-2017-9144) - bug #1471835
- Fix CVE-2017-10995 ImageMagick: Out-of-bounds heap read in mng_get_long function - bug #1471121
- Fix CVE-2017-11170 ImageMagick: Memory leak in ReadTGAImage function when processing TGA or VST file - bug #1470669
- Fix CVE-2017-6941 CVE-2017-6942 CVE-2017-6943 CVE-2017-8352 ImageMagick: various flaws - bug #1445676,1445677,1445679,1449253
- Fix CVE-2017-9141 CVE-2017-9142 CVE-2017-9143 CVE-2017-9144 ImageMagick: various flaws - bug #1455578,1455581,1455583,1455584
- Fix CVE-2016-9559 ImageMagick: Null pointer dereference in tiff.c - bug #1398189,1398198,1413898
- Fix CVE-2017-5507 ImageMagick: Memory leak in mpc file handling - bug #1414444
- Fix CVE-2016-10146 ImageMagick: Memory leak in caption and label handling - bug #1414446
- Fix CVE-2017-5508 ImageMagick: Heap-buffer-overflow in PushQuantumPixel - bug #1414445
- Fix CVE-2016-10070 ImageMagick: Out-of-bounds read in mat.c - bug #1410510
- Fix CVE-2017-5506 ImageMagick: Double-free memory corruption in profile.c - bug #1414442
- Fix CVE-2016-10064 ImageMagick: Buffer overflow in tiff.c - bug #1410478
- Fix CVE-2016-10071 ImageMagick: Out-of-bounds read in mat.c - bug #1410513
- Fix CVE-2016-10059 ImageMagick: TIFF file buffer overflow - bug #1410469
- Fix CVE-2016-10057 ImageMagick: Buffer overflow in CALS coder - bug #1410466
- Fix CVE-2016-10052 ImageMagick: Out-of-bounds write in exif (jpeg) reader - bug #1410459
- Fix CVE-2016-10050 ImageMagick: Heap overflow when reading corrupt RLE files - bug #1410454
- Fix CVE-2016-10049 ImageMagick: Buffer overflow when reading corrupt RLE files - bug #1410452
- Fix CVE-2016-10046 ImageMagick: Buffer overflow in draw.c - bug #1410448
- Fix CVE-2016-8677 ImageMagick: Memory allocation failure in AcquireQuantumPixel - bug #1385698
- Fix CVE-2016-6906 ImageMagick: Mogrify heap-use-after-free in attribute.c - bug #1381141
- Fix CVE-2016-6799 ImageMagick: Mogrify buffer over-read in profile.c - bug #1381138
- ImageMagick: Hang when supplying file ending with colon to identify - bug #1380428
- Fix CVE-2014-9907 CVE-2015-8957 CVE-2015-8958 CVE-2015-8959 CVE-2016-6823 CVE-2016-6101 CVE-2016-6513 CVE-2016-6514 CVE-2016-6515 CVE-2016-6516 CVE-2016-6517 CVE-2016-6518 CVE-2016-6519 CVE-2016-6520 CVE-2016-6521 ... ImageMagick: various flaws - bug #1378734,1378735,1378736,1378738,1378733,1378739,1378741,1378743,1378744,1378745,1378746,1378747,1378748,1378751,1378754,1378756,1378757,1378758,1378759,1378760,1378761,1378762,1378763,1378764,1378765,1378767,1378768,1378772,1378773,1378775,1378776,1378777,1378790
- Fix CVE-2016-5010 ImageMagick: Out-of-bounds read when processing crafted tiff file  - bug #1354500,1361578

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 6.9.3.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 6.9.3.0-7
- Perl 5.26 rebuild

* Sat Mar 11 2017 Remi Collet <remi@fedoraproject.org> - 6.9.3.0-6
- flag configuration files #1374050
- fix inter-package dependencies #1422773

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 6.9.3.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 01 2017 Sandro Mani <manisandro@gmail.com> - 6.9.3.0-4
- Rebuild (libwebp)

* Sat May 14 2016 Jitka Plesnikova <jplesnik@redhat.com> - 6.9.3.0-3
- Perl 5.24 rebuild

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 6.9.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jan 06 2016 Pavel Alexeev <Pahan@Hubbitus.info> - 6.9.3.0-1
- New upstream version 6.9.3-0. Bz#1293081.

* Mon Dec 28 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 6.9.2.7-2
- Rebuilt for libwebp soname bump

* Fri Dec 04 2015 Pavel Alexeev <Pahan@Hubbitus.info> - 6.9.2.7-1
- Update to new upstream release 6.9.2-6 (bz#1224581)
- Drop fix-XPM patch.
- No so-name change, so will update in stable branch to fix also: bz#1267391
    (JPEG 2000 support), bz#1269556 (security buff overflow in coders/icon.c),
    bz#1269567 (Double free vulnerabilities in coders/{pict.c,tga.c})
- Solving miltilib conflict - bz#1208347 - add patch ImageMagick-6.9.2-6-multiarch-implicit-pkgconfig-dir.patch.
- Drop old options: --with-lcms2, --without-included-ltdl, --with-ltdl-include, --with-ltdl-lib
- Some spec cleanup (including README utf recoding, rpath clean hacks).

* Sat Nov 21 2015 Pavel Alexeev <Pahan@Hubbitus.info> - 6.9.1.3-0.beta.4
- Add patch fix-XPM.patch (upstream fix for #1217178).

* Tue Jun 16 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.9.1.3-0.beta.3.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Jun 09 2015 Jitka Plesnikova <jplesnik@redhat.com> - 6.9.1.3-0.beta.3.1
- Perl 5.22 rebuild

* Mon Jun 08 2015 Pavel Alexeev <Pahan@Hubbitus.info> - 6.9.1.3-0.beta.3
- Add --disable-silent-rules, --with-jbig (and BR jbigkit-devel), --with-openjp2 (and BR openjpeg2-devel >= 2.1.0) by mail request from Remi Collet.

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 6.9.1.3-0.beta.2.1
- Perl 5.22 rebuild

* Wed May 27 2015 Pavel Alexeev <Pahan@Hubbitus.info> - 6.9.1.3-0.beta.2
- Again readd --without-gcc-arch to configure, to gone also -mtune gcc option (https://fedorahosted.org/fesco/ticket/1443)

* Thu May 21 2015 Pavel Alexeev <Pahan@Hubbitus.info> - 6.9.1.3-0.beta.1
- Build beta 6.9.1-3 to gone -march (https://fedorahosted.org/fesco/ticket/1443)

* Sat May 16 2015 Pavel Alexeev <Pahan@Hubbitus.info> - 6.9.1.2-3
- Enable back gcc arch optimization (--without-gcc-arch) #1213828 - GCC updated, problem should be gone.

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 6.9.1.2-2
- Disable gcc arch optimization (#1213828)

* Mon Apr 20 2015 Pavel Alexeev <Pahan@Hubbitus.info> - 6.9.1.2-1
- New version 6.9.1-2 - bz#1204371.

* Mon Mar 09 2015 Pavel Alexeev <Pahan@Hubbitus.info> - 6.9.0.10-1
- New version 6.9.0-10 - bz#1197400.

* Mon Feb 23 2015 Pavel Alexeev <Pahan@Hubbitus.info> - 6.9.0.9-1
- New version 6.9.0-9 - bz#1087263.
- So-name bump: libMagick++-6.Q16.so.3 -> libMagick++-6.Q16.so.6 (ML: https://lists.fedoraproject.org/pipermail/devel/2015-March/208814.html)

* Wed Nov 26 2014 Rex Dieter <rdieter@fedoraproject.org> - 6.8.8.10-8
- revert workaround

* Tue Nov 25 2014 Rex Dieter <rdieter@fedoraproject.org> - 6.8.8.10-7
- rebuild (openexr)
- 'make check' non-fatal as temp workaround for FTBFS (#1142784)

* Tue Aug 26 2014 Jitka Plesnikova <jplesnik@redhat.com> - 6.8.8.10-6
- Perl 5.20 rebuild

* Fri Aug 15 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.8.8.10-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Jun 06 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.8.8.10-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Apr 2 2014 Pavel Alexeev <Pahan@Hubbitus.info> - 6.8.8.10-3
- Concretize soname versions.

* Sat Mar 29 2014 Pavel Alexeev <Pahan@Hubbitus.info> - 6.8.8.10-2
- Update to 6.8.8-10 with hope to fix CVE-2014-1958 (bz#1067276, bz#1067277, bz#1067278), CVE-2014-1947, CVE-2014-2030 (bz#1064098)
- Enable %%check by Alexander Todorov suggestion - bz#1076671.
- Add %%{?_smp_mflags} into make install and check (not main compilation).

* Mon Jan 6 2014 Pavel Alexeev <Pahan@Hubbitus.info> - 6.8.7.0-4
- Drop BR giflib-devel (bz#1039378)

* Thu Jan 02 2014 Orion Poplawski <orion@cora.nwra.com> - 6.8.7.0-3
- Rebuild for libwebp soname bump

* Wed Nov 27 2013 Rex Dieter <rdieter@fedoraproject.org> 6.8.7.0-2
- rebuild (openexr)

* Fri Nov 08 2013 Kyle McMartin <kyle@fedoraproject.org>
- Use %%__isa_bits instead of hardcoding the list of 64-bit architectures.

* Mon Oct 7 2013 Pavel Alexeev <Pahan@Hubbitus.info> - 6.8.7.0-1
- Update to 6.8.7-0 to fix badurl (http://www.mail-archive.com/devel@lists.fedoraproject.org/msg67796.html)

* Sun Sep 08 2013 Rex Dieter <rdieter@fedoraproject.org> - 6.8.6.3-4
- rebuild (openexr)

* Fri Aug 02 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.8.6.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jul 18 2013 Petr Pisar <ppisar@redhat.com> - 6.8.6.3-2
- Perl 5.18 rebuild

* Mon Jul 1 2013 Pavel Alexeev <Pahan@Hubbitus.info> - 6.8.6.3-1
- Update to 6.8.6-3.
- Added aarch64 to list of 64bit arches (bz#978339).

* Wed Jun 12 2013 Pavel Alexeev <Pahan@Hubbitus.info> - 6.5.5.10-1
- Update to 6.8.5-10 upstream version (bz#720285).
- By Remi Collet request (bz#969760) enable those features in ImageMagick:
        --with-lcms2 (instead of --with-lcms): lcms2-devel
        --with-openexr: OpenEXR-devel
        --with-webp: libwebp-devel

* Thu Apr 18 2013 Pavel Alexeev <Pahan@Hubbitus.info> - 6.8.3.9-2
- Enable fftw to do Fourier transforms (add BuildRequires: fftw-devel) - bz#950254 by Søren Sandmann Pedersen request.

* Sun Mar 10 2013 Pavel Alexeev <Pahan@Hubbitus.info> - 6.8.3.9-1
- Update to 6.8.3-9 (so-naming scheme change to *-6.so) (ml: http://www.mail-archive.com/devel@lists.fedoraproject.org/msg57163.html).
- Split out libs subpackage by Remi Collet request (bz#849065).

* Sun Mar 10 2013 Rex Dieter <rdieter@fedoraproject.org> - 6.7.8.9-5
- rebuild (OpenEXR)

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.7.8.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jan 18 2013 Adam Tkac <atkac redhat com> - 6.7.8.9-3
- rebuild due to "jpeg8-ABI" feature drop

* Fri Dec 21 2012 Adam Tkac <atkac redhat com> - 6.7.8.9-2
- rebuild against new libjpeg

* Sat Aug 11 2012 Pavel Alexeev <Pahan@Hubbitus.info> - 6.7.8.9-1
- Update to 6.7.8-9 to fix CVE-2012-3437 (bz#844101, 844103).

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.7.7.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 11 2012 Petr Pisar <ppisar@redhat.com> - 6.7.7.5-2
- Perl 5.16 rebuild

* Sat Jun 2 2012 Pavel Alexeev <Pahan@Hubbitus.info> - 6.7.7.5-1
- Update to 6.7.7-5 version. Prepare and update in stable Fedora 16 to address security problems (f.e. bz#808159).

* Fri May 11 2012 Pavel Alexeev <Pahan@Hubbitus.info> - 6.7.6.5-2
- Rebuild due libtiff update http://www.mail-archive.com/devel@lists.fedoraproject.org/msg42846.html

* Tue Apr 10 2012 Pavel Alexeev <Pahan@Hubbitus.info> - 6.7.6.5-1
- Update to 6.7.6.5 to fix security issues: bz#807993, bz#807994, bz#807997,
        bz#808159, bz#804591, bz#804588

* Sat Feb 25 2012 Pavel Alexeev <Pahan@Hubbitus.info> - 6.7.5.6-1
- Update by request https://bugzilla.redhat.com/show_bug.cgi?id=755827#c8
- Delete multilib patch as it should be in main sources.
- Replace $RPM_BUILD_ROOT by %%buildroot

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.7.1.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Dec 05 2011 Adam Jackson <ajax@redhat.com> 6.7.1.9-2
- Rebuild for new libpng

* Mon Aug 22 2011 Pavel Alexeev <Pahan@Hubbitus.info> - 6.7.1.9-1
- New version 6.7.1-9.

* Thu Jul 21 2011 Petr Sabata <contyk@redhat.com> - 6.7.0.10-3
- Perl mass rebuild

* Wed Jul 20 2011 Petr Sabata <contyk@redhat.com> - 6.7.0.10-2
- Perl mass rebuild

* Wed Jun 22 2011 Pavel Alexeev <Pahan@Hubbitus.info> - 6.7.0.10-1
- Update to 6.7.0-10.

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 6.6.8.4-3
- Perl mass rebuild

* Fri Jun 10 2011 Marcela Mašláňová <mmaslano@redhat.com> - 6.6.8.4-2
- Perl 5.14 mass rebuild

* Tue Mar 15 2011 Pavel Alexeev <Pahan@Hubbitus.info> - 6.6.8.4-1
- Add BR liblqr-1-devel (BZ#683159)
- Update to new version (BZ#579458) 6.6.8-4

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.6.5.10-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Dec 17 2010 Pavel Alexeev <Pahan@Hubbitus.info> - 6.6.5.10-18
- Add BR OpenEXR-devel to support OpenEXR format (BZ#663705)

* Thu Nov 25 2010 Pavel Alexeev <Pahan@Hubbitus.info> - 6.6.5.10-17
- New version 6.6.5-10.
- Add --enable-hdri switch by request of Petr Vlašic.

* Thu Sep 30 2010 Pavel Alexeev <Pahan@Hubbitus.info> - 6.6.4.8-16
- Rebuild against new ghostscript in rawhide.
- Update to 6.6.4-8 version.

* Wed Sep 29 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 6.6.4.1-15
- rebuild against new ghostscript

* Fri Sep 17 2010 Rex Dieter <rdieter@fedoraproject.org> - 6.6.4.1-14
- %%files: track sonames, so as not to be surprised by future ABI breaks

* Tue Sep 14 2010 Pavel Alexeev <Pahan@Hubbitus.info> - 6.6.4.1-13
- Update to 6.6.4-1 to fix FBFS BZ#631169.

* Fri Jul 30 2010 Pavel Alexeev <Pahan@Hubbitus.info> - 6.6.2.1-12
- Add %%doc LICENSE as it required new Licensing Guidelines Update
        ( https://fedoraproject.org/wiki/Packaging:LicensingGuidelines )

* Wed Jun 23 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 6.6.2.1-11
- Rebuild (to fix downgrade after perl-5.12.0-rebuild tag)

* Tue Jun 1 2010 Pavel Alexeev <Pahan@Hubbitus.info> - 6.6.2.1-10
- New version 6.6.2-1 (BZ#579458, BZ#565940 - http://www.imagemagick.org/discourse-server/viewtopic.php?f=3&t=16320)
- Replace %%define by %%global

* Tue Jun 01 2010 Marcela Maslanova <mmaslano@redhat.com> - 6.6.0.2-9
- Mass rebuild with perl-5.12.0

* Sat Mar 6 2010 Pavel Alexeev <Pahan@Hubbitus.info> - 6.6.0.2-8
- Update to 6.6.0-2 (BZ#570766)

* Tue Jan 5 2010 Pavel Alexeev <Pahan@Hubbitus.info> - 6.5.8.10-6
- Update to 6.5.8-10 (BZ#547806)
- Change source tarball from .tar.lzma to .tar.xz folow to upstream.

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 6.5.4.7-5
- rebuild against perl 5.10.1

* Mon Nov 30 2009 Pavel Alexeev <Pahan@Hubbitus.info> - 6.5.4.7-4
- Explude file Generic.ttf from -perl subpackage demos. Demos perfectly work without it, but with bundled font
  package does not pass QA (Unfortunately no bugreport there, only mail from Nicolas Mailhot)

* Mon Aug 3 2009 Pavel Alexeev <Pahan@Hubbitus.info> - 6.5.4.7-3
- Update to version 6.5.4-6
- Use lzma-compressed source tarball as sugested by Ville Skyttä (BZ#515319)

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.5.3.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jun 15 2009 Hans de Goede <hdegoede@redhat.com> 6.5.3.7-1
- New upstream release 6.5.3-6

* Mon Apr 13 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 6.5.1.2-1
- update to 6.5.1-2

* Fri Mar 13 2009 Hans de Goede <hdegoede@redhat.com> 6.4.9.6-2
- Fix undefined warning in magick-type.h (#489453)
- Do not link PerlMagick against system ImageMagick, but against the just
  build one

* Mon Mar  9 2009 Hans de Goede <hdegoede@redhat.com> 6.4.9.6-1
- New upstream release 6.4.9-6

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.4.5.5-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Jan 30 2009 Hans de Goede <hdegoede@redhat.com> 6.4.5.5-8
- Remove (TM) from description as per new guidelines

* Sat Jan 17 2009 Rakesh Pandit <rakesh@fedoraproject.org> 6.4.5.5-7
- Corrected the wrong release and bumped

* Sat Jan 17 2009 Rakesh Pandit <rakesh@fedoraproject.org> 6.4.5.5-6
- Rebuild with new djvulibre

* Sat Dec 27 2008 Hans de Goede <hdegoede@redhat.com> 6.4.5.5-5
- Remove 2 included copies of the non Free artbrush font (rh 477399)

* Wed Dec 10 2008 Hans de Goede <hdegoede@redhat.com> 6.4.5.5-4
- Do not pass -jX to make when building, this breaks PerlMagick (rh 475554)

* Wed Nov 19 2008 Hans de Goede <hdegoede@redhat.com> 6.4.5.5-3
- Remove --without-windows-font-dir from configure args, specifying it
  makes ImageMagick search for windows fonts in the "no/" dir (rh 472244)

* Fri Nov 14 2008 Hans de Goede <hdegoede@redhat.com> 6.4.5.5-2
- Enable djvu support, put the new djvu plugin into a separate -djvu
  subpackage because of deps (rh 225897)

* Fri Nov 14 2008 Hans de Goede <hdegoede@redhat.com> 6.4.5.5-1
- New upstream release 6.4.5-5
- Various specfile fixes from merge review (rh 225897)
- Fix building with new libtool (rh 471468)

* Thu Nov 13 2008 Hans de Goede <hdegoede@redhat.com> 6.4.0.10-3
- Rebuild for new libtool (rh 471468)

* Sun Jul 27 2008 Hans de Goede <jwrdegoede@fedoraproject.org> 6.4.0.10-2
- Fix ownership of /usr/include/ImageMagick (bz 444647)
- By Remi request (bz#969760) enable those features in ImageMagick:
        --with-lcms2 (instead of --with-lcms): lcms2-devel
        --with-openexr: OpenEXR-devel
        --with-webp: libwebp-devel

* Sat Apr 26 2008 Hans de Goede <jwrdegoede@fedoraproject.org> 6.4.0.10-1
- New upstream release 6.4.0.10
- This fixes conversion of 24 bpp windows icons (bz 440136)
- Don't reuse GError structs, that upsets glib2 (bz 325211)
- Use the system ltdl, not the included copy (bz 237475)
- Fix various multilib conflicts (bz 341561)
- Use xdg-open instead of htmlview (bz 388451)
- Some small specfile cleanups (utf-8 stuff & others) fixing rpmlint warnings

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 6.3.8.1-3
- Rebuild for perl 5.10 (again)

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 6.3.8.1-2
- Autorebuild for GCC 4.3

* Thu Jan 24 2008 Tom "spot" Callaway <tcallawa@redhat.com> 6.3.8.1-1
- update to 6.3.8.1
- rebuild for new perl
- fix license tag
- fix rpath issues
- add sparc64 to 64bit arch list

* Fri Sep 21 2007 Norm Murray <nmurray@redhat.com> 6.3.5.9-1.fc8
- rebase to 6.3.5.9
- fix build with missing open() arg
- add build require of jasper-devel, remove windows font dir
- update multilib patch

* Thu Apr  5 2007 Norm Murray <nmurray@redhat.com> 6.3.2.9-3.fc7
- heap overflows (#235075, CVE-2007-1797)

* Fri Mar 30 2007 Norm Murray <nmurray@redhat.com> 6.3.2.9-2.fc7
- perlmagick build fix (#231259)

* Fri Mar  2 2007 Norm Murray <nmurray@redhat.com> 6.3.2.9-1.fc7.0
- update to 6.3.2-9

* Wed Aug 23 2006 Matthias Clasen <mclasen@redhat.com> - 6.2.8.0-3.fc6
- fix several integer and buffer overflows (#202193, CVE-2006-3743)
- fix more integer overflows (#202771, CVE-2006-4144)

* Mon Jul 24 2006 Matthias Clasen <mclasen@redhat.com> - 6.2.8.0-2
- Add missing BRs

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 6.2.8.0-1.1
- rebuild

* Fri Jun  9 2006 Matthias Clasen <mclasen@redhat.com> - 6.2.8-1
- Update to 6.2.8

* Fri Jun  2 2006 Matthias Clasen <mclasen@redhat.com> - 6.2.5.4-7
- Fix multilib issues

* Thu May 25 2006 Matthias Clasen <mclasen@redhat.com> - 6.2.5.4-6
- Fix a heap overflow CVE-2006-2440 (#192279)
- Include required .la files

* Mon Mar 20 2006 Matthias Clasen <mclasen@redhat.com> - 6.2.5.4-5
- Don't ship .la and .a files (#185237)

* Mon Feb 13 2006 Jesse Keating <jkeating@redhat.com> - 6.2.5.4-4.2.1
- rebump for build order issues during double-long bump

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 6.2.5.4-4.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 6.2.5.4-4.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Mon Jan 30 2006 Matthias Clasen <mclasen@redhat.com> 6.2.5.4-4
- Make -devel require lcms-devel (#179200)

* Mon Jan 23 2006 Matthias Clasen <mclasen@redhat.com> 6.2.5.4-3
- Fix linking of DSOs.  (#176695)

* Mon Jan  9 2006 Matthias Clasen <mclasen@redhat.com> 6.2.5.4-2
- fix a format string vulnerability (CVE-2006-0082)

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Tue Nov  1 2005 Matthias Clasen <mclasen@redhat.com> 6.2.5.4-1
- Switch requires to modular X
- Update to 6.2.5

* Tue Sep 20 2005 Matthias Clasen <mclasen@redhat.com> 6.2.4.6-1
- Update to 6.2.4-6
- Drop upstreamed patches
- Disable DPS (#158984)
- Add missing requires (#165931)

* Thu Jun  9 2005 Tim Waugh <twaugh@redhat.com> 6.2.2.0-4
- Rebuilt for fixed ghostscript.

* Mon Jun  6 2005 Tim Waugh <twaugh@redhat.com> 6.2.2.0-3
- Rebuilt for new ghostscript.

* Thu May 26 2005  <mclasen@redhat.com> - 6.2.2.0-2
- fix a denial of service in the xwd coder (#158791, CAN-2005-1739)

* Tue Apr 26 2005 Matthias Clasen <mclasen@redhat.com> - 6.2.2.0-1
- Update to 6.2.2 to fix a heap corruption issue
  in the pnm coder.

* Mon Apr 25 2005  Matthias Clasen <mclasen@redhat.com> - 6.2.1.7-4
- .la files for modules are needed, actually

* Mon Apr 25 2005  Matthias Clasen <mclasen@redhat.com> - 6.2.1.7-3
- Really remove .la files for modules

* Mon Apr 25 2005  <mclasen@redhat.com> - 6.2.1.7-1
- Update to 6.2.1
- Include multiple improvements and bugfixes
  by Rex Dieter et al (111961, 145466, 151196, 149970,
  146518, 113951, 145449, 144977, 144570, 139298)

* Sun Apr 24 2005  <mclasen@redhat.com> - 6.2.0.7-3
- Make zip compression work for tiff (#154045)

* Wed Mar 16 2005  <mclasen@redhat.com> - 6.2.0.7-2
- Update to 6.2.0 to fix a number of security issues:
  #145112 (CAN-2005-05), #151265 (CAN-2005-0397)
- Drop a lot of upstreamed patches

* Wed Mar  2 2005 Matthias Clasen <mclasen@redhat.com> 6.0.7.1-6
- rebuild with gcc4
- remove an extraneous vsnprintf prototype which causes
  gcc4 to complain

* Mon Oct 11 2004 Tim Waugh <twaugh@redhat.com> 6.0.7.1-4
- The devel subpackage requires XFree86-devel (bug #126509).
- Fixed build requirements (bug #120776).  From Robert Scheck.

* Tue Sep 14 2004 Karsten Hopp <karsten@redhat.de> 6.0.7.1-3
- move *.mgk files (#132007, #131708, #132397)

* Sun Sep 12 2004 Karsten Hopp <karsten@redhat.de> 6.0.7.1-1
- update to 6.0.7 Patchlevel 1, fixes #132106

* Sat Sep 4 2004 Bill Nottingham <notting@redhat.com> 6.0.6.2-2
- move libWand out of -devel, fix requirements (#131767)

* Wed Sep 01 2004 Karsten Hopp <karsten@redhat.de> 6.0.6.2-1
- update to latest stable version
- get rid of obsolete patches
- fix remaining patches

* Sat Jun 19 2004 Alan Cox <alan@redhat.com>
- Easyfixes (#124791) - fixed missing dependancy between -devel and
  libexif-devel

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Mar 23 2004 Karsten Hopp <karsten@redhat.de> 5.5.7.15-1.3
- freetype patch to fix convert (#115716)

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Sun Jan 25 2004 Nils Philippsen <nphilipp@redhat.com> 5.5.7.15-0.2
- make perl module link against the built library instead of the installed one

* Thu Jan 22 2004 Nils Philippsen <nphilipp@redhat.com> 5.5.7.15-0.1
- version 5.5.7 patchlevel 15

* Mon Oct 13 2003 Nils Philippsen <nphilipp@redhat.com> 5.5.7.10-0.1
- rebuild with release 0.1 to not block an official update package

* Wed Sep 10 2003 Nils Philippsen <nphilipp@redhat.com> 5.5.7.10-2
- hack around libtool stupidity
- disable automake patch as we require automake-1.7 anyway

* Wed Sep 10 2003 Nils Philippsen <nphilipp@redhat.com> 5.5.7.10-1
- version 5.5.7 patchlevel 10

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu May 29 2003 Tim Powers <timp@redhat.com> 5.5.6-4
- rebuild for RHEL to fix broken deps

* Thu May 15 2003 Tim Powers <timp@redhat.com> 5.5.6-3
- rebuild again to fix broken dep on libMagick.so.5

* Mon May 12 2003 Karsten Hopp <karsten@redhat.de> 5.5.6-2
- rebuild

* Fri May 09 2003 Karsten Hopp <karsten@redhat.de> 5.5.6-1
- update
- specfile fixes
  #63897 (_target instead of _arch)
  #74521 (SRPM doesn't compile)
  #80441 (RFE: a newer version of ImageMagick is available)
  #88450 (-devel package missing dependancy)
  #57396 (convert won't read RAW format images)
- verified that the upstream version fixes the following bugreports:
  #57544 (display cannot handle many xpm's which both ee and rh71 display can)
  #63727 (ImageMagick fails to handle RGBA files)
  #73864 (composite dumps core on certain operations)
  #78242 (Header files for c missing in devel rpms)
  #79783 (magick_config.h is missing from ImageMagick-c++-devel)
  #80117 (Documentation is installed twice by RPM )
  #82762 (Trouble with browsing help files)
  #85760 (Segmentation fault)
  #86120 (eps->ppm convert crashes)

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Sat Jan  4 2003 Jeff Johnson <jbj@redhat.com> 5.4.7-9
- use internal dep generator.

* Mon Dec 16 2002 Tim Powers <timp@redhat.com> 5.4.7-8
- rebuild

* Sat Dec 14 2002 Tim Powers <timp@redhat.com> 5.4.7-7
- don't use rpms internal dep generator

* Fri Nov 22 2002 Tim Powers <timp@redhat.com>
- fix perl paths in file list

* Thu Nov 21 2002 Tim Powers <timp@redhat.com>
- lib64'ize
- don't throw stuff in /usr/X11R6, that's for X only
- remove files we aren't shipping

* Sat Aug 10 2002 Elliot Lee <sopwith@redhat.com>
- rebuilt with gcc-3.2 (we hope)

* Tue Jul 23 2002 Tim Powers <timp@redhat.com> 5.4.7-4
- build using gcc-3.2-0.1

* Wed Jul 03 2002 Karsten Hopp <karsten@redhat.de> 5.4.7-3
- fix non-cpp headers in -devel package
- fix #62157 (wrong path for include files in ImageMagick-devel)
- fix #63897 (use _target instead of _arch) in libtool workaround
- fix #65860, #65780 (tiff2ps) expands images to >10 MB Postscript files.

* Mon Jul 01 2002 Karsten Hopp <karsten@redhat.de> 5.4.7-1
- update
- fix localdoc patch
- fix %%files section
- disable nonroot patch
- fix #62100,55950,62162,63136 (display doesn't start form gnome menu)
- fix libtool workaround
- moved Magick*-config into -devel package (#64249)

* Sun May 26 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Mon May  6 2002 Bernhard Rosenkraenzer <bero@redhat.com> 5.4.6-1
- 5.4.6

* Thu Mar 14 2002 Bernhard Rosenkraenzer <bero@redhat.com> 5.4.3.11-1
- Update to pl 11

* Fri Feb 22 2002 Bernhard Rosenkraenzer <bero@redhat.com> 5.4.3.5-1
- Update to 5.4.3 pl5; this fixes #58080

* Thu Jan 17 2002 Bernhard Rosenkraenzer <bero@redhat.com> 5.4.2.3-1
- Patchlevel 3

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Fri Jan  4 2002 Bernhard Rosenkraenzer <bero@redhat.com> 5.4.2.2-1
- Update to 5.4.2-2
- Fix #57923, also don't hardcode netscape as html viewer

* Wed Dec  5 2001 Bernhard Rosenkraenzer <bero@redhat.com> 5.4.1-1
- 5.4.1
- Link against new libstdc++

* Fri Nov  9 2001 Bernhard Rosenkraenzer <bero@redhat.com> 5.4.0.5-1
- 5.4.0.5
- Make the error message when trying to display an hpgl file more
  explicit (#55875)

* Mon Nov  5 2001 Bernhard Rosenkraenzer <bero@redhat.com> 5.4.0.3-1
- 5.4.0.3
- Fix names of man pages

* Mon Oct 22 2001 Bernhard Rosenkraenzer <bero@redhat.com> 5.4.0-1
- 5.4.0
- work around build system breakage causing applications to be named
  %%{_arch}-redhat-linux-foo rather than foo

* Wed Sep 19 2001 Bernhard Rosenkraenzer <bero@redhat.com> 5.3.9-1
- 5.3.9

* Mon Aug 27 2001 Bernhard Rosenkraenzer <bero@redhat.com> 5.3.8-3
- Add delegates.mgk back, got lost during the update to 5.3.8 (Makefile bug)
  (#52611)

* Mon Aug 20 2001 Bernhard Rosenkraenzer <bero@redhat.com> 5.3.8-2
- Remove Magick++ includes from -devel, they're already in -c++-devel
  (#51590)

* Sat Jul 28 2001 Bernhard Rosenkraenzer <bero@redhat.com> 5.3.8-1
- 5.3.8 (bugfix release)

* Fri Jul 27 2001 Than Ngo <than@redhat.com> 5.3.7-3
- fix to build Perlmagic on s390 s390x

* Thu Jul 26 2001 Bernhard Rosenkraenzer <bero@redhat.com> 5.3.7-2
- Add delegates.mgk to the package (#50725)

* Tue Jul 24 2001 Bernhard Rosenkraenzer <bero@redhat.com> 5.3.7-1
- 5.3.7
- Fix build without previously installed ImageMagick-devel (#49816)
- Move perl bindings to a separate package.

* Mon Jul  9 2001 Bernhard Rosenkraenzer <bero@redhat.com> 5.3.6-2
- Fix build as non-root again
- Shut up rpmlint

* Tue Jul  3 2001 Bernhard Rosenkraenzer <bero@redhat.com> 5.3.6-1
- 5.3.6
- Get rid of the ia64 patch, it's no longer needed since glibc was fixed

* Sat Jun 16 2001 Than Ngo <than@redhat.com>
- update to 5.3.5
- cleanup specfile

* Sat May 19 2001 Bernhard Rosenkraenzer <bero@redhat.com> 5.3.3-2
- 5.3.3-respin, fixes #41196

* Tue May  1 2001 Bernhard Rosenkraenzer <bero@redhat.com> 5.3.3-1
- 5.3.3
- Add a desktop file for "display" (RFE#17417)

* Sun Apr 15 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- 5.3.2
- work around bugs in ia64 glibc headers

* Mon Jan 08 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- remove patch for s390, it is not necessary

* Mon Jan  1 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- 5.2.7

* Wed Dec 27 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- 5.2.6

* Mon Dec 18 2000 Than Ngo <than@redhat.com>
- ported to s390

* Mon Sep 25 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- 5.2.4
- Fix up and package the C++ bindings in the new c++/c++-devel packages.

* Wed Aug  2 2000 Matt Wilson <msw@redhat.com>
- rebuild against new libpng

* Wed Jul 19 2000 Nalin Dahyabhai <nalin@redhat.com>
- include images with docs (#10312)

* Thu Jul 13 2000 Matt Wilson <msw@redhat.com>
- don't build with -ggdb, use -g instead.

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Mon Jul  3 2000 Florian La Roche <laroche@redhat.com>
- update to 5.2.2 beta

* Mon Jul  3 2000 Florian La Roche <laroche@redhat.com>
- update to 5.2.1, redone patches as they failed

* Fri Jun 30 2000 Matt Wilson <msw@redhat.com>
- remove hacks to move perl man pages
- don't include the perl*/man stuff, these files go in /usr/share/man now.

* Thu Jun 15 2000 Nalin Dahyabhai <nalin@redhat.com>
- disable optimization on Alpha and Sparc

* Wed Jun 14 2000 Nalin Dahyabhai <nalin@redhat.com>
- update to 5.2.0
- update URL
- remove redundant CXXFLAGS=$RPM_OPT_FLAGS

* Thu Jun  1 2000 Matt Wilson <msw@redhat.com>
- bootstrap rebuilt to nuke broken libbz2 deps
- add Prefix: tag such that the FHS macros work properly

* Wed May 17 2000 Trond Eivind Glomsrød <teg@redhat.com>
- now compiles with bzip2 1.0
- changed buildroot to include version

* Fri May  5 2000 Bill Nottingham <notting@redhat.com>
- fix compilation with new perl

* Sat Mar 18 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- 5.1.1

* Thu Feb  3 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Rebuild to get compressed man pages

* Thu Nov 18 1999 Michael K. Johnson <johnsonm@redhat.com>
- ugly hack to print with lpr instead of lp

* Mon Aug 30 1999 Bill Nottingham <notting@redhat.com>
- update to 4.2.9

* Tue Aug 17 1999 Bill Nottingham <notting@redhat.com>
- update to 4.2.8

* Fri Apr 09 1999 Cristian Gafton <gafton@redhat.com>
- include the perl man pages as well

* Tue Apr 06 1999 Michael K. Johnson <johnsonm@redhat.com>
- remove --enable-16bit because it damages interoperability

* Mon Apr  5 1999 Bill Nottingham <notting@redhat.com>
- update to 4.2.2
- change ChangeLog to refer to actual dates.
- strip binaries

* Thu Apr  1 1999 Bill Nottingham <notting@redhat.com>
- add more files. Oops.

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 2)

* Wed Mar 10 1999 Bill Nottingham <notting@redhat.com>
- version 4.2.1

* Tue Jan 19 1999 Michael K. Johnson <johnsonm@redhat.com>
- changed group

* Tue Jan 19 1999 Cristian Gafton <gafton@redhat.com>
- hacks to make it work with the new perl
- version 4.1.0 (actually installs the sonames as 4.0.10... doh!)
- make sure the libraries have the x bit on

* Wed Jun 10 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr

* Thu May 07 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Tue Apr 21 1998 Cristian Gafton <gafton@redhat.com>
- updated to 4.0.5

* Wed Apr 08 1998 Cristian Gafton <gafton@redhat.com>
- updated to 4.0.4
- added BuildRoot

* Thu Oct 23 1997 Donnie Barnes <djb@redhat.com>
- updated from 3.8.3 to 3.9.1
- removed PNG patch (appears to be fixed)

* Wed Oct 15 1997 Erik Troan <ewt@redhat.com>
- build against new libpng

* Thu Jul 10 1997 Erik Troan <ewt@redhat.com>
- built against glibc

* Thu Mar 20 1997 Michael Fulbright <msf@redhat.com>
- updated to version 3.8.3.
- updated source and url tags.
