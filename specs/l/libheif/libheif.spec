## START: Set by rpmautospec
## (rpmautospec version 0.8.3)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 7;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global somajor 1
# this is used for breaking a self-dependency on build, via
# two paths, first:
# libheif BuildRequires: pkgconfig(sdl2) == sdl2-compat-devel
# sdl2-compat-devel -> sdl2-compat
# sdl2-compat -> SDL3
# SDL3 -> libdecor
# libdecor -> gtk3
# gtk3 -> gtk-update-icon-cache
# gtk-update-icon-cache -> gdk-pixbuf2
# gdk-pixbuf2 -> glycin-libs
# glycin-libs -> glycin-loaders
# glycin-loaders -> libheif
# second:
# heif-pixbuf-loader BuildRequires: pkgconfig(gdk-pixbuf-2.0) == gdk-pixbuf2-devel
# gdk-pixbuf2-devel -> gdk-pixbuf2
# gdk-pixbuf2 -> glycin-libs
# glycin-libs -> glycin-loaders
# glycin-loaders -> libheif
%bcond bootstrap 0

Name:           libheif
Version:        1.20.2
Release:        %autorelease
Summary:        HEIF and AVIF file format decoder and encoder

License:        LGPL-3.0-or-later and MIT
URL:            https://github.com/strukturag/libheif
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz
Patch0:         libheif-no-hevc-tests.patch

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  ninja-build
BuildRequires:  pkgconfig(aom)
BuildRequires:  pkgconfig(dav1d)
BuildRequires:  pkgconfig(libbrotlidec)
BuildRequires:  pkgconfig(libjpeg)
BuildRequires:  pkgconfig(libopenjp2)
BuildRequires:  pkgconfig(libpng)
%if !%{with bootstrap}
BuildRequires:  pkgconfig(sdl2)
%endif
BuildRequires:  pkgconfig(zlib)
%ifnarch %{ix86}
# openh264 is not available for i686, see:
# https://bugzilla.redhat.com/show_bug.cgi?id=2393742
BuildRequires:  pkgconfig(openh264)
BuildRequires:  pkgconfig(openjph) >= 0.18.0
%endif
%if ! (0%{?rhel} && 0%{?rhel} <= 9)
BuildRequires:  pkgconfig(libsharpyuv)
BuildRequires:  pkgconfig(rav1e)
BuildRequires:  pkgconfig(SvtAv1Enc)
%endif

Obsoletes:      heif-pixbuf-loader < %{version}-%{release}

%description
libheif is an ISO/IEC 23008-12:2017 HEIF and AVIF (AV1 Image File Format)
file format decoder and encoder.

%files
%license COPYING
%doc README.md
%{_libdir}/%{name}.so.%{somajor}{,.*}
%dir %{_libdir}/%{name}

# ----------------------------------------------------------------------

%package        tools
Summary:        Tools for manipulating HEIF files
License:        MIT
Requires:       %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       shared-mime-info

%description    tools
This package provides tools for manipulating HEIF files.

%files tools
%{_bindir}/heif-*
%{_mandir}/man1/heif-*
%{_datadir}/thumbnailers/heif.thumbnailer

# ----------------------------------------------------------------------

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%files devel
%{_includedir}/%{name}/
%{_libdir}/cmake/%{name}/
%{_libdir}/pkgconfig/%{name}.pc
%{_libdir}/%{name}.so

# ----------------------------------------------------------------------


%prep
%setup -q
%patch 0 -p1
rm -rf third-party/


%build
%cmake \
 -GNinja \
 -DBUILD_TESTING=ON \
 -DCMAKE_COMPILE_WARNING_AS_ERROR=OFF \
 -DPLUGIN_DIRECTORY=%{_libdir}/%{name} \
 -DWITH_DAV1D=ON \
 -DWITH_DAV1D_PLUGIN=OFF \
 -DWITH_JPEG_DECODER=ON \
 -DWITH_JPEG_ENCODER=ON \
 -DWITH_OpenJPEG_DECODER=ON \
 -DWITH_OpenJPEG_DECODER_PLUGIN=OFF \
 -DWITH_OpenJPEG_ENCODER=ON \
 -DWITH_OpenJPEG_ENCODER_PLUGIN=OFF \
%ifnarch %{ix86}
 -DWITH_OpenH264_DECODER=ON \
 -DWITH_OpenH264_ENCODER=ON \
 -DWITH_OPENJPH_DECODER=ON \
 -DWITH_OPENJPH_ENCODER=ON \
 -DWITH_OPENJPH_ENCODER_PLUGIN=OFF \
%endif
%if ! (0%{?rhel} && 0%{?rhel} <= 9)
 -DWITH_RAV1E=ON \
 -DWITH_RAV1E_PLUGIN=OFF \
 -DWITH_SvtEnc=ON \
 -DWITH_SvtEnc_PLUGIN=OFF \
%endif
%if %{with bootstrap}
 -DWITH_EXAMPLE_HEIF_VIEW=OFF \
%endif
 -DWITH_UNCOMPRESSED_CODEC=ON \
 -DWITH_GDK_PIXBUF=OFF \
 -Wno-dev

%cmake_build


%install
%cmake_install

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

multilibFileVersions %{buildroot}%{_includedir}/%{name}/heif_version.h


%check
%ctest


%changelog
## START: Generated by rpmautospec
* Thu Apr 30 2026 Daniel McIlvaney <damcilva@microsoft.com> - 1.20.2-7
- test: add initial lock files

* Thu Oct 02 2025 Robert-André Mauchin <eclipseo@mauchin.fr> - 1.20.2-6
- Rebuild for svt-av1 3.1.2

* Tue Sep 16 2025 Michael Catanzaro <mcatanzaro@redhat.com> - 1.20.2-5
- Remove obsolete pixbuf loader

* Tue Sep 09 2025 Dominik 'Rathann' Mierzejewski <dominik@greysector.net> - 1.20.2-4
- disable openh264 on i686 (resolves rhbz#2393742)

* Sun Sep 07 2025 Fabio Valentini <decathorpe@gmail.com> - 1.20.2-3
- Un-bootstrap again

* Sun Sep 07 2025 Fabio Valentini <decathorpe@gmail.com> - 1.20.2-2
- Bootstrap even harder

* Sun Sep 07 2025 Simone Caronni <negativo17@gmail.com> - 1.20.2-1
- Update to 1.20.2

* Sat Sep 06 2025 Adam Williamson <awilliam@redhat.com> - 1.20.1-9
- Non-bootstrap build for openjph

* Sat Sep 06 2025 Adam Williamson <awilliam@redhat.com> - 1.20.1-8
- Add a bootstrap build path to break a glycin-related dep loop

* Sat Sep 06 2025 Adam Williamson <awilliam@redhat.com> - 1.20.1-7
- Drop the openjph build conditional

* Sat Sep 06 2025 Simone Caronni <negativo17@gmail.com> - 1.20.1-6
- Rebuild for updated depdencies

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.20.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sun Jul 06 2025 Dominik Mierzejewski <dominik@greysector.net> - 1.20.1-1
- update to 1.20.1 (resolves rhbz#2375931)
- build heif-view tool (requires SDL2)
- add explicit build dependency on zlib

* Sun Apr 27 2025 Packit <hello@packit.dev> - 1.19.8-1
- Update to version 1.19.8
- Resolves: rhbz#2362578

* Mon Mar 17 2025 Dominik Mierzejewski <dominik@greysector.net> - 1.19.7-1
- update to 1.19.7 (resolves rhbz#2349315)
- enable OpenJPH and drop i686 ifarch for it, it builds fine there now

* Thu Mar 13 2025 Fabio Valentini <decathorpe@gmail.com> - 1.19.5-4
- Rebuild for noopenh264 2.6.0

* Wed Feb 05 2025 Robert-André Mauchin <zebob.m@gmail.com> - 1.19.5-3
- Rebuilt for aom 3.11.0

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.19.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sun Nov 24 2024 Packit <hello@packit.dev> - 1.19.5-1
- Update to version 1.19.5
- Resolves: rhbz#2327307

* Sun Nov 17 2024 Dominik Mierzejewski <dominik@greysector.net> - 1.19.3-3
- disable OpenJPH encoder support to work-around crashes

* Sat Nov 16 2024 Sérgio Basto <sergio@serjux.com> - 1.19.3-2
- Add support to multilib in devel sub-package
- Resolves: rhbz#2279891

* Tue Nov 12 2024 Dominik Mierzejewski <dominik@greysector.net> - 1.19.3-1
- update to 1.19.3 (resolves rhbz#2295525)
- drop obsolete patches
- enable OpenH264, OpenJPH (64-bit only) and Brotli decoders
- run tests unconditionally, they no longer require special build options
- drop conditional hevc subpackage
- use fewer wildcards in the file lists
- stop building rav1e and svt AV1 encoders as plugins

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.17.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Apr 13 2024 Robert-André Mauchin <zebob.m@gmail.com> - 1.17.6-`1
- Update to 1.17.6
- Security fix for CVE-2024-25269
- Close: rhbz#2255512
- Fix: rhbz#2267897

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.17.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.17.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 12 2024 Fabio Valentini <decathorpe@gmail.com> - 1.17.5-2
- Rebuild for dav1d 1.3.0

* Fri Dec 15 2023 Dominik Mierzejewski <dominik@greysector.net> - 1.17.5-2
- Update to 1.17.5 (rhbz#2244583)
- Backport fixes for: CVE-2023-49460 (rhbz#2253575, rhbz#2253576)
                      CVE-2023-49462 (rhbz#2253567, rhbz#2253568)
                      CVE-2023-49463 (rhbz#2253565, rhbz#2253566)
                      CVE-2023-49464 (rhbz#2253562, rhbz#2253563)
- Simplify conditionals for rav1e and svt-av1 encoders
- Enable JPEG2000 and dav1d decoders/encoders

* Fri Sep 08 2023 Dominik Mierzejewski <dominik@greysector.net> - 1.16.2-2
- Enable uncompressed codec (rhbz#2237849)
- Run tests conditionally (requires making all symbols visible)
- Disable HEVC tests when building without HEVC codec

* Fri Jul 28 2023 Orion Poplawski <orion@nwra.com> - 1.16.2-1
- Update to 1.16.2

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.16.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri May 05 2023 Neal Gompa <ngompa@fedoraproject.org> - 1.16.1-1
- Update to 1.16.1

* Sun Apr 30 2023 Dominik Mierzejewski <dominik@greysector.net> - 1.15.2-2
- backport fix for issue#590

* Tue Apr 11 2023 Sandro <devel@penguinpee.nl> - 1.15.2-1
- Update to 1.15.2 (RHBZ#2183664)
- Drop patch

* Fri Mar 17 2023 Neal Gompa <ngompa@fedoraproject.org> - 1.15.1-2
- Adapt for Fedora

* Fri Feb 17 2023 Leigh Scott <leigh123linux@gmail.com> - 1.15.1-1
- Update to 1.15.1

* Sat Jan 07 2023 Leigh Scott <leigh123linux@gmail.com> - 1.14.2-1
- Update to 1.14.2
- Switch back to autotools to build due to cmake issues (rfbz#6550}

* Thu Jan 05 2023 Leigh Scott <leigh123linux@gmail.com> - 1.14.1-1
- Update to 1.14.1

* Mon Dec 19 2022 Leigh Scott <leigh123linux@gmail.com> - 1.14.0-4
- Don't build rav1e and SVT-AV1 as plugins (rfbz#6532)

* Mon Dec 05 2022 Nicolas Chauvet <kwizart@gmail.com> - 1.14.0-3
- Fix for SvtAv1Enc in devel - rfbz#6521

* Wed Nov 23 2022 Nicolas Chauvet <kwizart@gmail.com> - 1.14.0-2
- Enable svt-av1 on el9

* Tue Nov 15 2022 Leigh Scott <leigh123linux@gmail.com> - 1.14.0-1
- Update to 1.14.0

* Fri Sep 02 2022 Leigh Scott <leigh123linux@gmail.com> - 1.13.0-1
- Update to 1.13.0

* Sun Aug 07 2022 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 1.12.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild and ffmpeg
  5.1

* Thu Jun 23 2022 Robert-André Mauchin <zebob.m@gmail.com> - 1.12.0-5
- Rebuilt for new dav1d, rav1e and jpegxl

* Wed Feb 09 2022 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 1.12.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Nov 25 2021 Nicolas Chauvet <kwizart@gmail.com> - 1.12.0-3
- Rebuilt

* Tue Aug 03 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.12.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Jun 14 2021 Leigh Scott <leigh123linux@gmail.com> - 1.12.0-1
- Update to 1.12.0

* Sun Jun 13 2021 Robert-André Mauchin <zebob.m@gmail.com> - 1.11.0-3
- Rebuild for new aom

* Wed Apr 14 2021 Leigh Scott <leigh123linux@gmail.com> - 1.11.0-2
- Rebuild for new x265

* Sat Feb 20 2021 Leigh Scott <leigh123linux@gmail.com> - 1.11.0-1
- Update to 1.11.0

* Wed Feb 03 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.10.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sat Dec 19 2020 Leigh Scott <leigh123linux@gmail.com> - 1.10.0-1
- Update to 1.10.0

* Mon Dec 14 2020 Leigh Scott <leigh123linux@gmail.com> - 1.9.1-3
- Actually do the dav1d rebuild

* Mon Dec 14 2020 Robert-André Mauchin <zebob.m@gmail.com> - 1.9.1-2
- Rebuild for dav1d SONAME bump

* Tue Oct 27 2020 Leigh Scott <leigh123linux@gmail.com> - 1.9.1-1
- Update to 1.9.1

* Fri Aug 28 2020 Leigh Scott <leigh123linux@gmail.com> - 1.8.0-1
- Update to 1.8.0

* Tue Aug 18 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.7.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 08 2020 Leigh Scott <leigh123linux@gmail.com> - 1.7.0-2
- Rebuilt

* Thu Jun 04 2020 Leigh Scott <leigh123linux@gmail.com> - 1.7.0-1
- Update to 1.7.0

* Sun May 31 2020 Leigh Scott <leigh123linux@gmail.com> - 1.6.2-3
- Rebuild for new x265 version

* Sun Feb 23 2020 RPM Fusion Release Engineering <leigh123linux@googlemail.com> - 1.6.2-2
- Rebuild for x265

* Mon Feb 10 2020 Leigh Scott <leigh123linux@gmail.com> - 1.6.2-1
- Update to 1.6.2

* Tue Feb 04 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Nov 28 2019 Leigh Scott <leigh123linux@googlemail.com> - 1.6.0-1
- Update to 1.6.0
- Rebuilt for x265

* Sun Nov 03 2019 Leigh Scott <leigh123linux@googlemail.com> - 1.5.1-1
- Update to 1.5.1

* Fri Aug 09 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.4.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Jul 02 2019 Nicolas Chauvet <kwizart@gmail.com> - 1.4.0-3
- Rebuilt for x265

* Mon Mar 04 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Feb 28 2019 Leigh Scott <leigh123linux@googlemail.com> - 1.4.0-1
- Update to 1.4.0

* Thu Jan 03 2019 Leigh Scott <leigh123linux@googlemail.com> - 1.3.2-2
- Rebuild for new x265 for el7

* Thu Nov 29 2018 Leigh Scott <leigh123linux@googlemail.com> - 1.3.2-1
- First build

## END: Generated by rpmautospec
