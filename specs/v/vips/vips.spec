## START: Set by rpmautospec
## (rpmautospec version 0.8.4)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 2;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global vips_version_base 8.17
%global vips_version %{vips_version_base}.3
%global vips_soname_major 42

Name:		vips
Version:	%{vips_version}
Release:	%autorelease
Summary:	C/C++ library for processing large images

License:	LGPL-2.1-or-later
URL:		https://www.libvips.org/
Source0:	https://github.com/libvips/libvips/releases/download/v%{version}/%{name}-%{version}.tar.xz

BuildRequires:	meson
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(gobject-introspection-1.0)
BuildRequires:	pkgconfig(expat)
BuildRequires:	pkgconfig(fftw3)
BuildRequires:	pkgconfig(libhwy)
BuildRequires:	pkgconfig(lcms2)
BuildRequires:	pkgconfig(imagequant)
BuildRequires:	pkgconfig(OpenEXR)
BuildRequires:	pkgconfig(Imath)
BuildRequires:	pkgconfig(matio)
BuildRequires:	pkgconfig(cfitsio)
BuildRequires:	pkgconfig(pangoft2)
BuildRequires:	pkgconfig(zlib)
BuildRequires:	pkgconfig(cgif)
BuildRequires:	pkgconfig(spng)
BuildRequires:	pkgconfig(libjpeg)
BuildRequires:	pkgconfig(libjxl)
BuildRequires:	pkgconfig(libheif)
BuildRequires:	pkgconfig(libtiff-4)
BuildRequires:	pkgconfig(libwebp)
BuildRequires:	pkgconfig(libexif)
BuildRequires:	pkgconfig(libarchive)
BuildRequires:	pkgconfig(librsvg-2.0)
BuildRequires:	pkgconfig(libopenjp2)
BuildRequires:	pkgconfig(openslide)
BuildRequires:	pkgconfig(poppler-glib)
BuildRequires:	pkgconfig(MagickWand)
BuildRequires:	nifticlib-devel

BuildRequires:	gcc-c++
BuildRequires:	pkgconfig
BuildRequires:	gettext
BuildRequires:	gi-docgen
BuildRequires:	doxygen

# bc command used in test suite
BuildRequires:	bc

# Not available as system library
Provides:	bundled(libnsgif)

# Optional plugins
Recommends: %{name}-jxl
Recommends: %{name}-heif
Recommends: %{name}-magick
Recommends: %{name}-openslide
Recommends: %{name}-poppler

%description
VIPS is an image processing library. It is good for very large images
(even larger than the amount of RAM in your machine), and for working
with color.

This package should be installed if you want to use a program compiled
against VIPS.


%package devel
Summary:	Development files for %{name}
Requires:	vips%{?_isa} = %{version}-%{release}

%description devel
The %{name}-devel package contains the header files and
libraries necessary for developing programs using VIPS.


%package tools
Summary:	Command-line tools for %{name}
Requires:	vips%{?_isa} = %{version}-%{release}

%description tools
The %{name}-tools package contains command-line tools for working with VIPS.


%package doc
Summary:	Documentation for %{name}
BuildArch:	noarch
Conflicts:	%{name} < %{version}-%{release}, %{name} > %{version}-%{release}

%description doc
The %{name}-doc package contains extensive HTML documentation about VIPS and
its C++ API.


%package jxl
Summary:	JPEG XL support for %{name}
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description jxl
The %{name}-jxl package contains the jxl module for VIPS, providing JPEG XL
support.


%package heif
Summary:	HEIF support for %{name}
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description heif
The %{name}-heif package contains the heif module for VIPS, providing AVIF
support.


%package openslide
Summary:	OpenSlide support for %{name}
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description openslide
The %{name}-openslide package contains the OpenSlide module for VIPS.


%package poppler
Summary:	Poppler support for %{name}
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description poppler
The %{name}-poppler package contains the Poppler module for VIPS.


%package magick
Summary:	Magick support for %{name} using ImageMagick7
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description magick
The %{name}-magick package contains the Magick module for VIPS using
ImageMagick7.


%prep
%autosetup -p1


%build
# Upstream recommends enabling auto-vectorization of inner loops:
# https://github.com/libvips/libvips/pull/212#issuecomment-68177930
export CFLAGS="%{optflags} -ftree-vectorize"
export CXXFLAGS="%{optflags} -ftree-vectorize"
# TODO remove `-Dnifti-prefix-dir=/usr`:
# https://github.com/libvips/libvips/pull/2882#issuecomment-1165686117
# https://github.com/NIFTI-Imaging/nifti_clib/pull/140
%meson \
    -Dnifti-prefix-dir=/usr \
    -Dcpp-docs=true \
    -Ddocs=true \
    -Dpdfium=disabled \
    %{nil}

%meson_build


%install
%meson_install

# locale stuff
%find_lang vips%{vips_version_base}


%check
%meson_test


%files -f vips%{vips_version_base}.lang
%doc ChangeLog README.md
%license LICENSE
%{_libdir}/*.so.%{vips_soname_major}*
%{_libdir}/girepository-1.0
%dir %{_libdir}/vips-modules-%{vips_version_base}


%files devel
%{_includedir}/vips
%{_libdir}/*.so
%{_libdir}/pkgconfig/*
%{_datadir}/gir-1.0


%files tools
%{_bindir}/*
%{_mandir}/man1/*


%files doc
%{_docdir}/vips
%{_docdir}/vips-cpp
%license LICENSE


%files jxl
%{_libdir}/vips-modules-%{vips_version_base}/vips-jxl.so


%files heif
%{_libdir}/vips-modules-%{vips_version_base}/vips-heif.so


%files openslide
%{_libdir}/vips-modules-%{vips_version_base}/vips-openslide.so


%files poppler
%{_libdir}/vips-modules-%{vips_version_base}/vips-poppler.so


%files magick
%{_libdir}/vips-modules-%{vips_version_base}/vips-magick.so


%changelog
## START: Generated by rpmautospec
* Wed Apr 22 2026 azldev <azurelinux@microsoft.com> - 8.17.3-2
- Latest state for vips

* Tue Dec 09 2025 Adam Goode <adam@spicenitz.org> - 8.17.3-1
- Include missing changes for latest release

* Tue Dec 09 2025 Adam Goode <adam@spicenitz.org> - 8.17.2-2
- Update to vips 8.17.3

* Fri Sep 19 2025 Kleis Auke Wolthuizen <fedora@kleisauke.nl> - 8.17.2-1
- Update to 8.17.2

* Tue Sep 09 2025 Sandro Mani <manisandro@gmail.com> - 8.17.1-3
- Rebuild (libimagequant)

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 8.17.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jul 07 2025 Kleis Auke Wolthuizen <fedora@kleisauke.nl> - 8.17.1-1
- Update to 8.17.1
- Resolves: rhbz#2351373
- Migrate API documentation to gi-docgen
- Drop dependency on python3-cairo (due to vipsprofile removal)

* Sat May 24 2025 Kleis Auke Wolthuizen <fedora@kleisauke.nl> - 8.16.1-2
- Build vips-doc package as noarch

* Tue Apr 08 2025 Kleis Auke Wolthuizen <fedora@kleisauke.nl> - 8.16.1-1
- Update to 8.16.1
- Drop patch merged upstream
- Refresh descriptions for vips-devel and vips-doc

* Sun Feb 02 2025 Sérgio M. Basto <sergio@serjux.com> - 8.16.0-5
- Rebuild for jpegxl (libjxl) 0.11.1

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 8.16.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sun Nov 03 2024 Adam Goode <adam@spicenitz.org> - 8.16.0-3
- Fix build on s390x

* Sat Nov 02 2024 Adam Goode <adam@spicenitz.org> - 8.16.0-2
- Use autorelease and autochangelog

* Wed Oct 30 2024 Kleis Auke Wolthuizen <fedora@kleisauke.nl> - 8.16.0-1
- Update to 8.16.0
- Migrate to SPDX license
- Don't ignore test failures on s390x
- Update outdated comments and URLs
- Cleanup Requires

* Wed Sep 04 2024 Miroslav Suchý <msuchy@redhat.com> - 8.15.1-10
- convert license to SPDX

* Wed Aug 21 2024 Ankur Sinha (Ankur Sinha Gmail) <sanjay.ankur@gmail.com> - 8.15.1-9
- rebuilt for nifticlib 3.x (again)

* Tue Aug 20 2024 Ankur Sinha (Ankur Sinha Gmail) <sanjay.ankur@gmail.com> - 8.15.1-8
- feat: rebuilt for nifticlib 3.x

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 8.15.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Apr 24 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 8.15.1-6
- Rebuilt for openexr 3.2.4

* Mon Apr 22 2024 Gwyn Ciesla <gwync@protonmail.com> - 8.15.1-5
- matio rebuild

* Wed Mar 13 2024 Sérgio M. Basto <sergio@serjux.com> - 8.15.1-4
- Rebuild for jpegxl (libjxl) 0.10.2

* Wed Feb 14 2024 Sérgio M. Basto <sergio@serjux.com> - 8.15.1-3
- Rebuild for jpegxl (libjxl) 0.9.2 with soname bump

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 8.15.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jan 20 2024 Kleis Auke Wolthuizen <fedora@kleisauke.nl> - 8.15.1-1
- Update to 8.15.1
- Use libhwy in favor of liborc
- Use libarchive in favor of libgsf

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 8.14.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 20 2023 Kleis Auke Wolthuizen <fedora@kleisauke.nl> - 8.14.2-1
- Update to 8.14.2
- Migrate build to Meson
- Add vips-heif plugin
- Add bc build dependency
- Move gtk-doc docs from vips-devel to vips-doc
- Drop libpng build dependency in favor of spng
- Drop python3-devel build dependency

* Sun Jun 18 2023 Sérgio M. Basto <sergio@serjux.com> - 8.13.3-11
- Mass rebuild for jpegxl-0.8.1

* Sun Jun 18 2023 Sérgio M. Basto <sergio@serjux.com> - 8.13.3-10
- Mass rebuild for jpegxl-0.8.1

* Sat Mar 04 2023 Sandro Mani <manisandro@gmail.com> - 8.13.3-9
- Fix typo

* Sat Mar 04 2023 Sandro Mani <manisandro@gmail.com> - 8.13.3-8
- Ignore s390x test failure for now

* Sat Mar 04 2023 Sandro Mani <manisandro@gmail.com> - 8.13.3-7
- Rebuild (libimagequant)

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 8.13.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jan 12 2023 Maxwell G <gotmax@e.email> - 8.13.3-5
- Rebuild for cfitsio 4.2

* Tue Jan 10 2023 Mamoru TASAKA <mtasaka@fedoraproject.org> - 8.13.3-4
- Backport upstream fix for emitting finish signal for target_end

* Fri Jan 06 2023 Neal Gompa <ngompa@fedoraproject.org> - 8.13.3-3
- Rebuild for ImageMagick 7

* Thu Dec 29 2022 Maxwell G <gotmax@e.email> - 8.13.3-2
- Rebuild for cfitsio 4.2

* Thu Dec 01 2022 Philipp Trulson <philipp@trulson.de> - 8.13.3-1
- Update to 8.13.3

* Tue Nov 01 2022 Lumir Balhar <lbalhar@redhat.com> - 8.12.2-5
- Switch from pathfix.py to %%py3_shebang_fix

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 8.12.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jun 23 2022 Robert-André Mauchin <zebob.m@gmail.com> - 8.12.2-3
- Rebuilt for new jpegxl

* Fri May 20 2022 Sandro Mani <manisandro@gmail.com> - 8.12.2-2
- Rebuild for gdal-3.5.0 and/or openjpeg-2.5.0

* Mon Apr 11 2022 Adam Goode <adam@spicenitz.org> - 8.12.2-1
- New upstream release

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 8.11.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Sun Nov 21 2021 Orion Poplawski <orion@nwra.com> - 8.11.3-8
- Rebuild for hdf5 1.12.1

* Sun Oct 17 2021 Mamoru TASAKA <mtasaka@fedoraproject.org> - 8.11.3-7
- Rebuild against new ImageMagick

* Wed Sep 01 2021 Vít Ondruch <vondruch@redhat.com> - 8.11.3-6
- Re-enable testing for ppc64le.

* Sun Aug 22 2021 Richard Shaw <hobbes1069@gmail.com> - 8.11.3-5
- Disable testing for ppc64le.

* Sun Aug 22 2021 Richard Shaw <hobbes1069@gmail.com> - 8.11.3-4
- Rebuild for OpenEXR/Imath 3.1.

* Wed Aug 18 2021 Vít Ondruch <vondruch@redhat.com> - 8.11.3-3
- Enable test suite

* Tue Aug 17 2021 Orion Poplawski <orion@nwra.com> - 8.11.3-2
- Rebuild for hdf5 1.10.7 (again)

* Mon Aug 16 2021 Adam Goode <adam@spicenitz.org> - 8.11.3-1
- Update to 8.11.3

* Tue Aug 10 2021 Orion Poplawski <orion@nwra.com> - 8.11.2-9
- Rebuild for hdf5 1.10.7

* Mon Aug 02 2021 Richard Shaw <hobbes1069@gmail.com> - 8.11.2-8
- Rebuild for OpenEXR/Imath 3.

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 8.11.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Jul 05 2021 Benjamin Gilbert <bgilbert@backtick.net> - 8.11.2-6
- Add doxygen C++ docs to vips-devel

* Mon Jul 05 2021 Benjamin Gilbert <bgilbert@backtick.net> - 8.11.2-5
- Drop some redundant version restrictions

* Mon Jul 05 2021 Benjamin Gilbert <bgilbert@backtick.net> - 8.11.2-4
- Textual cleanups

* Mon Jul 05 2021 Benjamin Gilbert <bgilbert@backtick.net> - 8.11.2-3
- Update sources

* Mon Jul 05 2021 Remi Collet <remi@fedoraproject.org> - 8.11.2-2
- missing arch suffix, missing bundled(libnsgif) information

* Sun Jul 04 2021 Remi Collet <remi@fedoraproject.org> - 8.11.2-1
- update to 8.11.2

* Tue Jun 29 2021 Remi Collet <remi@fedoraproject.org> - 8.11.1-1
- update to 8.11.1

* Thu Jun 17 2021 Remi Collet <remi@fedoraproject.org> - 8.11.0-2
- add dependency on libopenjpg2

* Thu Jun 10 2021 Remi Collet <remi@fedoraproject.org> - 8.11.0-1
- update to 8.11.0 split plugins in sub-packages

* Mon Apr 05 2021 Gwyn Ciesla <gwync@protonmail.com> - 8.10.6-1
- 8.10.6, matio rebuild.

* Wed Feb 03 2021 Benjamin Gilbert <bgilbert@backtick.net> - 8.10.5-6
- Rebuild for cfitsio

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 8.10.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sat Jan 09 2021 Tom Stellard <tstellar@redhat.com> - 8.10.5-4
- Add BuildRequires: make

* Fri Jan 08 2021 Vít Ondruch <vondruch@redhat.com> - 8.10.5-3
- One more rebuild to really pick the right OpenEXR version.

* Fri Jan 01 2021 Richard Shaw <hobbes1069@gmail.com> - 8.10.5-2
- Rebuild for OpenEXR 2.5.3.

* Sun Dec 20 2020 Benjamin Gilbert <bgilbert@backtick.net> - 8.10.5-1
- 8.10.5

* Tue Dec 15 2020 Benjamin Gilbert <bgilbert@backtick.net> - 8.10.4-1
- 8.10.4

* Mon Oct 12 2020 Benjamin Gilbert <bgilbert@backtick.net> - 8.10.2-1
- 8.10.2

* Mon Oct 12 2020 Benjamin Gilbert <bgilbert@backtick.net> - 8.10.1-1
- 8.10.1

* Mon Oct 12 2020 Benjamin Gilbert <bgilbert@backtick.net> - 8.9.2-1
- 8.9.2

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 8.9.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jun 25 2020 Orion Poplawski <orion@nwra.com> - 8.9.1-2
- Rebuild for hdf5 1.10.6

* Wed Apr 08 2020 Adam Goode <adam@spicenitz.org> - 8.9.1-1
- 8.9.1

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 8.8.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jan 17 2020 Marek Kasik <mkasik@redhat.com> - 8.8.4-3
- Rebuild for poppler-0.84.0

* Mon Dec 09 2019 Benjamin Gilbert <bgilbert@backtick.net> - 8.8.4-2
- Disable orc on Fedora 31 for RHBZ 1780443

* Fri Dec 06 2019 Benjamin Gilbert <bgilbert@backtick.net> - 8.8.4-1
- 8.8.4

* Sat Sep 21 2019 Benjamin Gilbert <bgilbert@backtick.net> - 8.8.3-2
- Remember to upload 8.8.3

* Sat Sep 21 2019 Benjamin Gilbert <bgilbert@backtick.net> - 8.8.3-1
- 8.8.3

* Sun Sep 01 2019 Benjamin Gilbert <bgilbert@backtick.net> - 8.8.2-2
- Add python3-cairo dependency for vipsprofile

* Sun Sep 01 2019 Benjamin Gilbert <bgilbert@backtick.net> - 8.8.2-1
- 8.8.2; run vipsprofile with Python 3

* Mon Aug 19 2019 Miro Hrončok <miro@hroncok.cz> - 8.7.4-5
- Rebuilt for Python 3.8

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 8.7.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Apr 11 2019 Richard Shaw <hobbes1069@gmail.com> - 8.7.4-3
- Rebuild for OpenEXR 2.3.0.

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 8.7.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jan 18 2019 Benjamin Gilbert <bgilbert@backtick.net> - 8.7.4-1
- 8.7.4

* Tue Jan 08 2019 Benjamin Gilbert <bgilbert@backtick.net> - 8.7.3-1
- 8.7.3

* Sat Dec 08 2018 Benjamin Gilbert <bgilbert@backtick.net> - 8.7.2-1
- 8.7.2

* Sat Nov 17 2018 Benjamin Gilbert <bgilbert@backtick.net> - 8.7.1-1
- 8.7.1

* Fri Oct 05 2018 Benjamin Gilbert <bgilbert@backtick.net> - 8.7.0-1
- 8.7.0

* Wed Oct 03 2018 Benjamin Gilbert <bgilbert@backtick.net> - 8.6.5-5
- Drop Python 2 subpackage for
  https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Wed Oct 03 2018 Benjamin Gilbert <bgilbert@backtick.net> - 8.6.5-4
- Update package URLs

* Tue Aug 28 2018 Michael Cronenworth <mike@cchtml.com> - 8.6.5-3
- Rebuild for ImageMagick 6.9.10

* Tue Jul 31 2018 Florian Weimer <fweimer@redhat.com> - 8.6.5-2
- Rebuild with fixed binutils

* Sat Jul 28 2018 Benjamin Gilbert <bgilbert@backtick.net> - 8.6.5-1
- 8.6.5

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 8.6.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jul 02 2018 Miro Hrončok <miro@hroncok.cz> - 8.6.4-6
- Rebuilt for Python 3.7

* Sat Jun 30 2018 Benjamin Gilbert <bgilbert@backtick.net> - 8.6.4-5
- Don't assume /usr/bin/python is python2

* Sat Jun 30 2018 Benjamin Gilbert <bgilbert@backtick.net> - 8.6.4-4
- Add rpmlintrc

* Sat Jun 30 2018 Benjamin Gilbert <bgilbert@backtick.net> - 8.6.4-3
- Switch libjpeg-turbo BuildRequires to pkgconfig()

* Tue Jun 19 2018 Miro Hrončok <miro@hroncok.cz> - 8.6.4-2
- Rebuilt for Python 3.7

* Sun Jun 17 2018 Benjamin Gilbert <bgilbert@backtick.net> - 8.6.4-1
- 8.6.4

* Sun Jun 17 2018 Benjamin Gilbert <bgilbert@backtick.net> - 8.6.2-6
- Drop ldconfig scriptlets per new policy

* Sat May 26 2018 Christian Dersch <lupinix@mailbox.org> - 8.6.2-5
- rebuilt for cfitsio 3.450

* Fri Feb 23 2018 Christian Dersch <lupinix@mailbox.org> - 8.6.2-4
- rebuilt for cfitsio 3.420 (so version bump)

* Sun Feb 11 2018 Sandro Mani <manisandro@gmail.com> - 8.6.2-3
- Rebuild (giflib)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 8.6.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sun Feb 04 2018 Benjamin Gilbert <bgilbert@backtick.net> - 8.6.2-1
- 8.6.2

* Sun Jan 21 2018 Benjamin Gilbert <bgilbert@backtick.net> - 8.6.1-1
- 8.6.1

* Sun Dec 17 2017 Benjamin Gilbert <bgilbert@backtick.net> - 8.6.0-1
- 8.6.0

* Thu Nov 23 2017 Benjamin Gilbert <bgilbert@backtick.net> - 8.5.9-2
- Rename python-gobject-base dependency to python2-gobject-base

* Sun Nov 19 2017 Benjamin Gilbert <bgilbert@backtick.net> - 8.5.9-1
- 8.5.9

* Wed Sep 06 2017 Adam Williamson <awilliam@redhat.com> - 8.5.8-2
- Rebuild for ImageMagick 6 reversion

* Wed Aug 30 2017 Benjamin Gilbert <bgilbert@backtick.net> - 8.5.8-1
- 8.5.8

* Sun Aug 27 2017 Benjamin Gilbert <bgilbert@backtick.net> - 8.5.7-4
- Rebuild for ImageMagick

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 8.5.7-3
- Rebuilt for
  https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Mon Jul 31 2017 Kevin Fenzi <kevin@scrye.com> - 8.5.7-2
- Rebuild for new ImageMagick

* Sun Jul 30 2017 Benjamin Gilbert <bgilbert@backtick.net> - 8.5.7-1
- 8.5.7

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 8.5.6-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Jun 17 2017 Benjamin Gilbert <bgilbert@backtick.net> - 8.5.6-5
- Upstream switched from libxml2 to expat

* Sat Jun 17 2017 Benjamin Gilbert <bgilbert@backtick.net> - 8.5.6-4
- Rename Python packages per policy

* Sat Jun 17 2017 Benjamin Gilbert <bgilbert@backtick.net> - 8.5.6-3
- Add missing arch-specific Python provide

* Sat Jun 17 2017 Benjamin Gilbert <bgilbert@backtick.net> - 8.5.6-2
- Update for pygobject3 rename; use -base on Python 3

* Sat Jun 17 2017 Benjamin Gilbert <bgilbert@backtick.net> - 8.5.6-1
- 8.5.6

* Mon May 15 2017 Fedora Release Engineering <releng@fedoraproject.org> - 8.4.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 8.4.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 01 2017 Sandro Mani <manisandro@gmail.com> - 8.4.4-3
- Rebuild (libwebp)

* Thu Dec 22 2016 Miro Hrončok <miro@hroncok.cz> - 8.4.4-2
- Rebuild for Python 3.6

* Sun Nov 13 2016 Benjamin Gilbert <bgilbert@backtick.net> - 8.4.4-1
- 8.4.4

* Thu Oct 13 2016 Benjamin Gilbert <bgilbert@backtick.net> - 8.4.2-1
- 8.4.2

* Sun Sep 25 2016 Benjamin Gilbert <bgilbert@backtick.net> - 8.4.1-1
- 8.4.1

* Sat Aug 06 2016 Benjamin Gilbert <bgilbert@backtick.net> - 8.3.3-1
- 8.3.3

* Tue Jul 19 2016 Fedora Release Engineering <releng@fedoraproject.org> - 8.3.1-3
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_
  Packages

* Tue Jul 05 2016 Benjamin Gilbert <bgilbert@backtick.net> - 8.3.1-2
- Rebuilt for matio 1.5.7

* Tue May 10 2016 Benjamin Gilbert <bgilbert@backtick.net> - 8.3.1-1
- 8.3.1

* Thu Apr 14 2016 Benjamin Gilbert <bgilbert@backtick.net> - 8.3.0-1
- 8.3.0

* Mon Mar 28 2016 Benjamin Gilbert <bgilbert@backtick.net> - 8.2.3-1
- 8.2.3

* Sun Feb 21 2016 Benjamin Gilbert <bgilbert@backtick.net> - 8.2.2-3
- BuildRequire gcc-c++ per new policy

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 8.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jan 26 2016 Benjamin Gilbert <bgilbert@backtick.net> - 8.2.2-1
- 8.2.2

* Thu Jan 21 2016 Orion Poplawski <orion@cora.nwra.com> - 8.2.1-2
- Rebuild for hdf5 1.8.16

* Mon Jan 11 2016 Benjamin Gilbert <bgilbert@backtick.net> - 8.2.1-1
- 8.2.1

* Mon Dec 28 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 8.1.1-3
- Rebuilt for libwebp soname bump

* Tue Nov 10 2015 Peter Robinson <pbrobinson@fedoraproject.org> - 8.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Sun Oct 18 2015 Benjamin Gilbert <bgilbert@backtick.net> - 8.1.1-1
- 8.1.1

* Sun Oct 18 2015 Benjamin Gilbert <bgilbert@backtick.net> - 8.0.2-4
- Drop with_python3 %%global

* Fri Jun 19 2015 Dennis Gilmore <dennis@ausil.us> - 8.0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun May 17 2015 Orion Poplawski <orion@cora.nwra.com> - 8.0.2-2
- Rebuild for hdf5 1.8.15

* Wed May 06 2015 Benjamin Gilbert <bgilbert@backtick.net> - 8.0.2-1
- 8.0.2

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 7.42.3-2
- Rebuilt for GCC 5 C++11 ABI change

* Fri Feb 13 2015 Benjamin Gilbert <bgilbert@backtick.net> - 7.42.3-1
- 7.42.3

* Thu Feb 05 2015 Benjamin Gilbert <bgilbert@backtick.net> - 7.42.2-1
- 7.42.2

* Wed Jan 07 2015 Orion Poplawski <orion@cora.nwra.com> - 7.42.1-2
- Rebuild for hdf5 1.8.14

* Sun Dec 28 2014 Benjamin Gilbert <bgilbert@backtick.net> - 7.42.1-1
- 7.42.1

* Tue Nov 25 2014 Rex Dieter <rdieter@math.unl.edu> - 7.40.11-2
- rebuild (openexr)

* Wed Nov 05 2014 Benjamin Gilbert <bgilbert@backtick.net> - 7.40.11-1
- 7.40.11

* Thu Sep 25 2014 Benjamin Gilbert <bgilbert@backtick.net> - 7.40.9-1
- 7.40.9

* Fri Aug 22 2014 Benjamin Gilbert <bgilbert@backtick.net> - 7.40.6-1
- 7.40.6

* Mon Aug 18 2014 Peter Robinson <pbrobinson@fedoraproject.org> - 7.40.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Aug 12 2014 Benjamin Gilbert <bgilbert@backtick.net> - 7.40.5-1
- 7.40.5

* Sat Jul 26 2014 Benjamin Gilbert <bgilbert@backtick.net> - 7.40.4-1
- 7.40.4

* Tue Jul 22 2014 Kalev Lember <kalevlember@gmail.com> - 7.40.3-2
- Rebuilt for gobject-introspection 1.41.4

* Tue Jul 08 2014 Benjamin Gilbert <bgilbert@backtick.net> - 7.40.3-1
- 7.40.3

* Sun Jun 29 2014 Benjamin Gilbert <bgilbert@backtick.net> - 7.40.2-1
- 7.40.2

* Sun Jun 22 2014 Benjamin Gilbert <bgilbert@backtick.net> - 7.38.6-1
- 7.38.6

* Sun Jun 08 2014 Dennis Gilmore <dennis@ausil.us> - 7.38.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Mar 31 2014 Benjamin Gilbert <bgilbert@backtick.net> - 7.38.5-2
- Rebuild for ImageMagick

* Wed Mar 26 2014 Benjamin Gilbert <bgilbert@backtick.net> - 7.38.5-1
- 7.38.5

* Tue Jan 21 2014 Benjamin Gilbert <bgilbert@backtick.net> - 7.38.1-1
- 7.38.1

* Sun Jan 19 2014 Benjamin Gilbert <bgilbert@backtick.net> - 7.36.5-5
- Trim gitignore

* Fri Jan 10 2014 Orion Poplawski <orion@nwra.com> - 7.36.5-4
- Trim sources

* Thu Jan 09 2014 Benjamin Gilbert <bgilbert@backtick.net> - 7.36.5-3
- Rebuild for cfitsio

* Thu Jan 02 2014 Benjamin Gilbert <bgilbert@backtick.net> - 7.36.5-2
- Rebuild for libwebp

* Mon Dec 23 2013 Benjamin Gilbert <bgilbert@backtick.net> - 7.36.5-1
- 7.36.5

* Thu Nov 28 2013 Rex Dieter <rdieter@math.unl.edu> - 7.36.3-2
- rebuild (openexr)

* Wed Nov 13 2013 Benjamin Gilbert <bgilbert@backtick.net> - 7.36.3-1
- 7.36.3

* Sat Oct 05 2013 Benjamin Gilbert <bgilbert@backtick.net> - 7.36.0-1
- 7.36.0

* Tue Sep 10 2013 Benjamin Gilbert <bgilbert@backtick.net> - 7.34.2-2
- Rebuild for ilmbase 2.0

* Tue Aug 06 2013 Benjamin Gilbert <bgilbert@backtick.net> - 7.34.2-1
- 7.34.2

* Sun Aug 04 2013 Dennis Gilmore <dennis@ausil.us> - 7.34.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jul 12 2013 Orion Poplawski <orion@nwra.com> - 7.34.0-2
- Rebuild for cfitsio 3.350

* Sat Jun 29 2013 Benjamin Gilbert <bgilbert@backtick.net> - 7.34.0-1
- 7.34.0

* Fri Jun 28 2013 Kalev Lember <kalevlember@gmail.com> - 7.32.4-2
- Rebuilt with libpng 1.6

* Thu Jun 13 2013 Benjamin Gilbert <bgilbert@backtick.net> - 7.32.4-1
- 7.32.4

* Thu May 16 2013 Orion Poplawski <orion@nwra.com> - 7.32.3-2
- Rebuild for hdf5 1.8.11

* Sat Apr 27 2013 Benjamin Gilbert <bgilbert@backtick.net> - 7.32.3-1
- 7.32.3

* Fri Mar 22 2013 Benjamin Gilbert <bgilbert@backtick.net> - 7.32.1-1
- 7.32.1

* Thu Mar 21 2013 Benjamin Gilbert <bgilbert@backtick.net> - 7.32.0-5
- Rebuild for cfitsio

* Sun Mar 17 2013 Benjamin Gilbert <bgilbert@backtick.net> - 7.32.0-4
- Rebuild for ImageMagick

* Sun Mar 10 2013 Rex Dieter <rdieter@math.unl.edu> - 7.32.0-3
- rebuild (OpenEXR)

* Fri Mar 08 2013 Benjamin Gilbert <bgilbert@backtick.net> - 7.32.0-2
- Fix double configure run

* Thu Mar 07 2013 Benjamin Gilbert <bgilbert@backtick.net> - 7.32.0-1
- 7.32.0-1

* Fri Feb 15 2013 Dennis Gilmore <dennis@ausil.us> - 7.30.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Jan 21 2013 Adam Tkac <atkac@redhat.com> - 7.30.7-2
- Rebuild due to "jpeg8-ABI" feature drop

* Thu Jan 17 2013 Benjamin Gilbert <bgilbert@backtick.net> - 7.30.7-1
- 7.30.7

* Thu Nov 15 2012 Benjamin Gilbert <bgilbert@backtick.net> - 7.30.5-1
- 7.30.5

* Tue Oct 16 2012 Benjamin Gilbert <bgilbert@backtick.net> - 7.30.3-2
- #866302 was fixed; remove workaround

* Mon Oct 15 2012 Benjamin Gilbert <bgilbert@backtick.net> - 7.30.3-1
- 7.30.3

* Sun Jul 22 2012 Dennis Gilmore <dennis@ausil.us> - 7.28.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 07 2012 Adam Jackson <ajax@redhat.com> - 7.28.2-2
- Rebuild for new libmatio

* Fri Apr 13 2012 Adam Goode <adam@spicenitz.org> - 7.28.2-1
- New release

* Mon Jan 16 2012 Adam Goode <adam@spicenitz.org> - 7.26.7-1
- 7.26.7

* Sat Jan 14 2012 Dennis Gilmore <dennis@ausil.us> - 7.26.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 7.26.3-2
- Rebuild for new libpng

* Sat Sep 03 2011 Adam Goode <adam@spicenitz.org> - 7.26.3-1
- New upstream release

* Fri Aug 12 2011 Adam Goode <adam@spicenitz.org> - 7.24.7-6
- Fix ordering of changelog

* Fri Aug 12 2011 Adam Goode <adam@spicenitz.org> - 7.24.7-5
- RPMAUTOSPEC: unresolvable merge
## END: Generated by rpmautospec
