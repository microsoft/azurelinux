# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           SDL2_image
Version:        2.8.8
Release: 3%{?dist}
Summary:        Image loading library for SDL

# IMG_png.c is LGPLv2+ and zlib, rest is just zlib
# nanosvg is zlib
# miniz is Public Domain
# Automatically converted from old format: LGPLv2+ and zlib - review is highly recommended.
License:        LicenseRef-Callaway-LGPLv2+ AND Zlib
URL:            https://github.com/libsdl-org/SDL_image
Source0:        https://github.com/libsdl-org/SDL_image/releases/download/release-%{version}/SDL2_image-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  automake
BuildRequires:  SDL2-devel
BuildRequires:  libavif-devel
BuildRequires:  libjpeg-devel
BuildRequires:  libjxl-devel
BuildRequires:  libpng-devel
BuildRequires:  libtiff-devel
BuildRequires:  libwebp-devel
BuildRequires:  make
BuildRequires:  chrpath
Provides:       bundled(miniz) = 1.15
# Some custom version of it
Provides:       bundled(nanosvg)

%description
Simple DirectMedia Layer (SDL) is a cross-platform multimedia library
designed to provide fast access to the graphics frame buffer and audio
device.  This package contains a simple library for loading images of
various formats (BMP, PPM, PCX, GIF, JPEG, PNG) as SDL surfaces.

%package devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%autosetup -p1
sed -i -e 's/\r//g' README.txt CHANGES.txt

%build
./autogen.sh
%configure --disable-dependency-tracking \
           --disable-jpg-shared \
           --disable-png-shared \
           --disable-tif-shared \
           --disable-webp-shared \
           --disable-jxl-shared \
           --disable-avif-shared \
           --disable-static
sed -i -e 's! -shared ! -Wl,--as-needed\0!g' libtool
%make_build

%install
%make_install
mkdir -p %{buildroot}%{_bindir}
./libtool --mode=install /usr/bin/install showimage %{buildroot}%{_bindir}/showimage2
chrpath -d %{buildroot}%{_bindir}/showimage2

rm -f %{buildroot}%{_libdir}/*.la

%ldconfig_scriptlets

%files
%license LICENSE.txt
%doc CHANGES.txt
%{_bindir}/showimage2
%{_libdir}/libSDL2_image-2.0.so.*

%files devel
%doc README.txt
%{_libdir}/libSDL2_image.so
%{_includedir}/SDL2/SDL_image.h
%dir %{_libdir}/cmake
%{_libdir}/cmake/SDL2_image/
%{_libdir}/pkgconfig/SDL2_image.pc

%changelog
* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Mar 27 2025 Sérgio Basto <sergio@serjux.com> - 2.8.8-1
- Update SDL2_image to 2.8.8
- Resolves: rhbz#2354332

* Mon Mar 03 2025 Sérgio Basto <sergio@serjux.com> - 2.8.6-1
- Update SDL2_image to 2.8.6

* Sun Feb 02 2025 Sérgio Basto <sergio@serjux.com> - 2.8.4-3
- Rebuild for jpegxl (libjxl) 0.11.1

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Jan 01 2025 Sérgio Basto <sergio@serjux.com> - 2.8.4-1
- Update SDL2_image to 2.8.4

* Wed Sep 04 2024 Miroslav Suchý <msuchy@redhat.com> - 2.8.2-7
- convert license to SPDX

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Mar 13 2024 Sérgio Basto <sergio@serjux.com> - 2.8.2-5
- Rebuild for jpegxl (libjxl) 0.10.2

* Wed Mar 06 2024 Sérgio Basto <sergio@serjux.com> - 2.8.2-4
- add jpegxl and avif as shared libs

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Jan 02 2024 Fedora Release Monitoring <release-monitoring@fedoraproject.org> - 2.8.2-1
- Update to 2.8.2 (#2256488)

* Thu Dec 14 2023 Fedora Release Monitoring <release-monitoring@fedoraproject.org> - 2.8.1-1
- Update to 2.8.1 (#2253627)

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sun Jun 18 2023 Sérgio Basto <sergio@serjux.com> - 2.6.3-2
- Mass rebuild for jpegxl-0.8.1

* Thu Mar 16 2023 Pete Walter <pwalter@fedoraproject.org> - 2.6.3-1
- Update to 2.6.3

* Wed Jan 18 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Dec 03 2022 Pete Walter <pwalter@fedoraproject.org> - 2.6.2-1
- Update to 2.6.2

* Thu Dec 01 2022 Kalev Lember <klember@redhat.com> - 2.6.1-4
- Rebuild for new libavif

* Sun Oct 23 2022 Robert-André Mauchin <zebob.m@gmail.com> - 2.6.1-3
- Rebuild for new libavif

* Sun Oct 23 2022 Robert-André Mauchin <zebob.m@gmail.com> - 2.6.1-2
- Rebuild for new libavif

* Thu Aug 04 2022 Pete Walter <pwalter@fedoraproject.org> - 2.6.1-1
- Update to 2.6.1

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.5-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jan 19 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.5-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Jan 25 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.5-5
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Jul 16 2019 Pete Walter <pwalter@fedoraproject.org> - 2.0.5-1
- Update to 2.0.5

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Nov 06 2018 Pete Walter <pwalter@fedoraproject.org> - 2.0.4-1
- Update to 2.0.4

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sun Mar  4 2018 Peter Robinson <pbrobinson@fedoraproject.org> 2.0.3-1
- Update to 2.0.3

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jan 31 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.0.2-3
- Switch to %%ldconfig_scriptlets

* Wed Nov 01 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.0.2-2
- Add Provides: bundled(nanosvg) and add zlib to License

* Wed Nov 01 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.0.2-1
- Update to 2.0.2

* Wed Oct 11 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.0.1-8
- Fixed security vulnerability in XCF image loader

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 01 2017 Sandro Mani <manisandro@gmail.com> - 2.0.1-4
- Rebuild (libwebp)

* Tue Jan 03 2017 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 2.0.1-3
- Stop requiring pkgconfig

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sun Jan 10 2016 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 2.0.1-1
- Update to 2.0.1 (RHBZ #1296751)

* Mon Dec 28 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 2.0.0-9
- Rebuilt for libwebp soname bump

* Tue Jun 16 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Aug 15 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Jun 06 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Apr 15 2014 Dan Horák <dan[at]danny.cz> - 2.0.0-5
- fix FTBFS on big endian arches

* Fri Jan 03 2014 Kalev Lember <kalevlember@gmail.com> - 2.0.0-4
- Rebuilt for libwebp soname bump

* Fri Sep  6 2013 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 2.0.0-3
- showimage -> showimage2 (rhbz 1005324)

* Fri Sep  6 2013 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 2.0.0-2
- Move README.txt to -devel subpackage

* Fri Sep  6 2013 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 2.0.0-1
- Based on SDL_image
