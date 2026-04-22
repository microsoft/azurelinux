## START: Set by rpmautospec
## (rpmautospec version 0.8.4)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 5;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%bcond barcode 0%{?fedora}

Name:		mupdf
%global libname libmupdf
%global pypiname mupdf
Version:	1.27.1
%global somajor 27
%global sominor 1
%global soname %{somajor}.%{sominor}
%global pkgconfig %{_libdir}/pkgconfig
# upstream prerelease versions tags need to be translated to Fedorian
%global upversion %{version}
Release:	%autorelease
Summary:	A lightweight PDF viewer and toolkit
License:	AGPL-3.0-or-later
URL:		http://mupdf.com/
Source0:	http://mupdf.com/downloads/archive/%{name}-%{upversion}-source.tar.gz
Source1:	%{name}.desktop
Source2:	%{name}-gl.desktop

# Fedora specific patches:
# Do not bug me if Artifex relies on local fork
Patch:		0001-Do-not-complain-to-your-friendly-local-distribution-.patch
# Do not generate wrong form of dependencies
Patch:		0001-setup.py-do-not-require-libclang-and-swig.patch
# Do install shared libraries in the python tree
Patch:		0001-setup.py-do-not-bundle-c-and-c-libs-in-wheel.patch
# Suggested upstream:
# Avoid core dump of python bindings with gcc15
# https://github.com/ArtifexSoftware/mupdf/pull/55
Patch:		0001-pdf_choice_widget_options2-avoid-core-dump-with-_GLI.patch
# Do not apply CXXFLAGS to swig
# https://github.com/ArtifexSoftware/mupdf/pull/56
Patch:		0001-do-not-use-CXXFLAGS-with-swig.patch
# Be more helpful with the new warning in 1.26.x
# https://github.com/ArtifexSoftware/mupdf/pull/74
Patch:		0001-pdf_font-report-font-name-in-warning.patch
# Upstreamable:
Patch:		0001-mupdfwrap_test-adjust-to-mupdf-1.27.x.patch
# Upstream master branch:
Patch:		0001-Bug-709029-Fix-incorrect-error-case-free-of-pixmap.patch

BuildRequires:	gcc gcc-c++ make binutils desktop-file-utils coreutils pkgconfig
BuildRequires:	openjpeg2-devel desktop-file-utils
BuildRequires:	libjpeg-devel freetype-devel libXext-devel curl-devel
BuildRequires:	harfbuzz-devel openssl-devel mesa-libEGL-devel
BuildRequires:	mesa-libGL-devel mesa-libGLU-devel libXi-devel libXrandr-devel
BuildRequires:	gumbo-parser-devel leptonica-devel tesseract-devel
BuildRequires:	freeglut-devel
BuildRequires:	jbig2dec-devel brotli-devel
BuildRequires:	swig python3-clang python3-devel
%if %{with barcode}
BuildRequires:	zxing-cpp-devel zint-devel
%endif

Requires:	%{name}-libs%{_isa} = %{version}-%{release}

# We need to build against the Artifex fork of lcms2 so that we are thread safe
# (see bug #1553915). Artifex make sure to rebase against upstream, who refuse
# to integrate Artifex's changes. 
Provides:	bundled(lcms2-devel) = lcms2.16^65.gf75fad7
# muPDF needs the muJS sources for the build even if we build against the system
# version so bundling them is the safer choice.
Provides:	bundled(mujs-devel) = 1.3.7^2.g33c83d8
# muPDF builds only against in-tree extract which is versioned along with ghostpdl.
Provides:	bundled(extract) = 10.05

%description
MuPDF is a lightweight PDF viewer and toolkit written in portable C.
The renderer in MuPDF is tailored for high quality anti-aliased
graphics. MuPDF renders text with metrics and spacing accurate to
within fractions of a pixel for the highest fidelity in reproducing
the look of a printed page on screen.
MuPDF has a small footprint. A binary that includes the standard
Roman fonts is only one megabyte. A build with full CJK support
(including an Asian font) is approximately seven megabytes.
MuPDF has support for all non-interactive PDF 1.7 features, and the
toolkit provides a simple API for accessing the internal structures of
the PDF document. Example code for navigating interactive links and
bookmarks, encrypting PDF files, extracting fonts, images, and
searchable text, and rendering pages to image files is provided.

%package devel
Summary:	C Development files for %{name}
Requires:	%{name}-libs%{_isa} = %{version}-%{release}

%description devel
The mupdf-devel package contains library and header files for developing
C applications that use the mupdf library.

%package libs
Summary:	C Library files for %{name}

%description libs
The mupdf-libs package contains the mupdf C library files.

%package cpp-devel
Summary:	C++ Development files for %{name}
Requires:	%{name}-cpp-libs%{_isa} = %{version}-%{release}

%description cpp-devel
The mupdf-cpp-devel package contains library and header files for developing
C++ applications that use the mupdf library.

%package cpp-libs
Summary:	C++ Library files for %{name}
Requires:	%{name}-libs%{_isa} = %{version}-%{release}

%description cpp-libs
The mupdf-cpp-libs package contains the mupdf C++ library files.

%package -n python3-%{pypiname}
Summary:	Python bindings for %{name}
Requires:	%{name}-libs%{_isa} = %{version}-%{release}
Requires:	%{name}-cpp-libs%{_isa} = %{version}-%{release}

%description -n python3-%{pypiname}
The python3-%{pypiname} package contains low level mupdf python bindings.

%prep
%autosetup -p1 -n %{name}-%{upversion}-source
for d in $(ls thirdparty | grep -v -e extract -e lcms2 -e mujs)
do
	rm -rf thirdparty/$d
done
# avoid overwriting the proper README by the doc build instructions
rm -f docs/README

echo > user.make "\
	USE_SYSTEM_LIBS := yes
	USE_SYSTEM_MUJS := no # build needs source anyways
	USE_TESSERACT := yes
	VENV_FLAG :=
	barcode := %{?with_barcode:yes}%{!?with_barcode:no}
	build := release
	shared := yes
	verbose := yes
"

# c++ and python install targets rebuild unconditionally. Avoid multiple rebuilds:
sed -i -e '/^install-shared-c++:/s/ c++//' Makefile
sed -i -e '/^install-shared-python:/s/ python//' Makefile
# distribution builds are without experimental API:
sed -i -e '/DZXING_EXPERIMENTAL_API/ d' Makelists
%if %{without barcode}
# enforce same setting as above for py bindings:
sed -i -e 's/barcode=yes/barcode=no/' scripts/wrap/__main__.py
%endif

%generate_buildrequires
%pyproject_buildrequires -R

%build
export XCFLAGS="%{build_cflags} -fPIC -DJBIG_NO_MEMENTO -DTOFU -DTOFU_CJK_EXT"
export XCXXFLAGS="%{build_cxxflags} -fPIC -DJBIG_NO_MEMENTO -DTOFU -DTOFU_CJK_EXT"
make %{?_smp_mflags} shared c++
# Use the same build directory which make uses:
export MUPDF_SETUP_BUILD_DIR=build/shared-release
# Use stable python directories:
export MUPDF_SETUP_VERSION=%{version}
%pyproject_wheel

# Create pkgconfig file:
cat > mupdf.pc << EOF
prefix=%{_prefix}
exec_prefix=%{_exec_prefix}
libdir=%{_libdir}
includedir=%{_includedir}

Name: mupdf
Description: Library for rendering PDF documents
Requires.private: freetype2
Version: %{version}
Libs: -L${libdir} -lmupdf
Libs.private: -lmujs -lgumbo -lopenjp2 -ljbig2dec -ljpeg -lz -lm
Cflags: -I${includedir}
EOF

%install
make DESTDIR=%{buildroot} install install-shared-c install-shared-c++ prefix=%{_prefix} libdir=%{_libdir} pydir=%{python3_sitearch} SO_INSTALL_MODE=755
%pyproject_install
%pyproject_save_files -L %{pypiname}
# handle docs on our own
rm -rf %{buildroot}/%{_docdir}
desktop-file-install --dir=%{buildroot}%{_datadir}/applications %{SOURCE1}
desktop-file-install --dir=%{buildroot}%{_datadir}/applications %{SOURCE2}
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/scalable/apps
install -p -m644 docs/logo/mupdf-logo.svg %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/mupdf.svg
install -p -m644 docs/logo/mupdf-logo.svg %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/mupdf-gl.svg
mkdir -p %{buildroot}/%{pkgconfig}
install -p -m 0644 mupdf.pc %{buildroot}/%{pkgconfig}
find %{buildroot}/%{_mandir} -type f -exec chmod 0644 {} \;
find %{buildroot}/%{_includedir} -type f -exec chmod 0644 {} \;
cd %{buildroot}/%{_bindir} && ln -s %{name}-x11 %{name}

%check
# test import of python module and basic functionality
LD_LIBRARY_PATH='%{buildroot}%{_libdir}' %{py3_test_envvars} %{python3} scripts/mupdfwrap_test.py thirdparty/lcms2/doc/*.pdf

%files
%license COPYING
%doc README CHANGES docs/*
%{_bindir}/*
%{_datadir}/applications/mupdf*.desktop
%{_datadir}/icons/hicolor/*/apps/*
%{_mandir}/man1/*.1.gz

%files devel
%{_includedir}/%{name}
%{_libdir}/%{libname}.so
%{pkgconfig}/mupdf.pc

%files libs
%license COPYING
%{_libdir}/%{libname}.so.%{soname}
%{_libdir}/%{libname}.so.%{somajor}

%files cpp-devel
%{_includedir}/%{name}
%{_libdir}/%{libname}cpp.so

%files cpp-libs
%license COPYING
%{_libdir}/%{libname}cpp.so.%{soname}
%{_libdir}/%{libname}cpp.so.%{somajor}

%files -n python3-%{pypiname} -f %{pyproject_files}
%license COPYING
%{python3_sitearch}/_%{pypiname}.so

%changelog
## START: Generated by rpmautospec
* Wed Apr 22 2026 azldev <azurelinux@microsoft.com> - 1.27.1-5
- Latest state for mupdf

* Thu Feb 12 2026 Michael J Gruber <mjg@fedoraproject.org> - 1.27.1-4
- add versioned requires to make rpminspect happy

* Tue Feb 10 2026 Michael J Gruber <mjg@fedoraproject.org> - 1.27.1-3
- ship pkgconfig file (rhbz#2430595)

* Tue Feb 10 2026 Michael J Gruber <mjg@fedoraproject.org> - 1.27.1-2
- fix CVE-2026-25556

* Thu Feb 05 2026 Michael J Gruber <mjg@fedoraproject.org> - 1.27.1-1
- rebase to 1.27.1 (rhbz#2412002)
- changes to mutool run to bring it into sync with WASM library
- improvements for text extraction
- improved HTML+CSS support
- mutool grep: new tool to search for text in documents
- various bugfixes

* Fri Jan 16 2026 Fedora Release Engineering <releng@fedoraproject.org> - 1.26.9-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Tue Oct 28 2025 Michael J Gruber <mjg@fedoraproject.org> - 1.26.9-4
- rebuild for swig 4.4.0

* Wed Sep 24 2025 Michael J Gruber <mjg@fedoraproject.org> - 1.26.9-3
- fix CVE-2025-55780

* Tue Sep 23 2025 Michael J Gruber <mjg@fedoraproject.org> - 1.26.9-2
- fix rhbz#2391345

* Mon Sep 22 2025 Michael J Gruber <mjg@fedoraproject.org> - 1.26.9-1
- rebase to 1.26.9 (rhbz#2390306)
- various bugfixes

* Sun Sep 21 2025 Michael J Gruber <mjg@fedoraproject.org> - 1.26.3-6
- fix FTBFS with clang 20/21

* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 1.26.3-5
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 1.26.3-4
- Rebuilt for Python 3.14.0rc2 bytecode

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.26.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sun Jun 29 2025 Michael J Gruber <mjg@fedoraproject.org> - 1.26.3-2
- Be more helpful with the new font warning

* Sun Jun 29 2025 Michael J Gruber <mjg@fedoraproject.org> - 1.26.3-1
- rebase to 1.26.3 (rhbz#2352660)
- various bugfixes
- build with brotli compression
- build with barcode support on Fedora
- new CSV output format

* Wed Jun 04 2025 Python Maint <python-maint@redhat.com> - 1.25.4-3
- Rebuilt for Python 3.14

* Sat Mar 22 2025 Michael J Gruber <mjg@fedoraproject.org> - 1.25.4-2
- Work around pip 25/pyproject_hooks 1.2.0 path meddling (rhbz#2353480)

* Sat Feb 08 2025 Michael J Gruber <mjg@fedoraproject.org> - 1.25.4-1
- rebase to 1.25.4 (rhbz#2341961)
- various bugfixes

* Tue Feb 04 2025 Michael J Gruber <mjg@fedoraproject.org> - 1.25.2-5
- use release build

* Tue Feb 04 2025 Michael J Gruber <mjg@fedoraproject.org> - 1.25.2-4
- use proper flags

* Tue Feb 04 2025 Michael J Gruber <mjg@fedoraproject.org> - 1.25.2-3
- avoid core dump of python bindings with gcc15

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.25.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Dec 11 2024 Michael J Gruber <mjg@fedoraproject.org> - 1.25.2-1
- rebase to 1.25.2 (rhbz#2309092)
- various fixes all across the board
- enhanced redaction, structured text and annotation features
- new tool "mutool audit" to create summary of PDF file composition

* Tue Nov 12 2024 Sandro Mani <manisandro@gmail.com> - 1.24.6-4
- Rebuild (tesseract)

* Wed Sep 25 2024 Michel Lind <salimma@fedoraproject.org> - 1.24.6-3
- Rebuild for tesseract-5.4.1-3 (soversion change from 5.4.1 to just 5.4)

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.24.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jul 10 2024 Michael J Gruber <mjg@fedoraproject.org> - 1.24.6-1
- rebase to 1.24.5 (rhbz#2290729)
- various bugfixes all across the board

* Thu Jun 20 2024 Michael J Gruber <mjg@fedoraproject.org> - 1.24.2-5
- Create stable wheel dirs during build

* Thu Jun 13 2024 Sandro Mani <manisandro@gmail.com> - 1.24.2-4
- Rebuild for tesseract-5.4.1

* Sun Jun 09 2024 Python Maint <python-maint@redhat.com> - 1.24.2-3
- Rebuilt for Python 3.13

* Thu Jun 06 2024 Michael J Gruber <mjg@fedoraproject.org> - 1.24.2-2
- Shut off Artifex' suggestion to complain to distribution managers.

* Wed May 29 2024 Michael J Gruber <mjg@fedoraproject.org> - 1.24.2-1
- rebase to 1.24.2
- Fix dashing of lines that move out of clip.
- Fix sanitize filter behaviour for empty clip paths.
- Fix errors when filtering type3 font.

* Tue Apr 16 2024 Yaakov Selkowitz <yselkowi@redhat.com> - 1.24.1-2
- Fix flatpak build

* Wed Apr 03 2024 Michael J Gruber <mjg@fedoraproject.org> - 1.24.1-1
- rebase to 1.24.1 (rhbz#2272640)
- fix text movement on sanitisation

* Fri Mar 22 2024 Michael J Gruber <mjg@fedoraproject.org> - 1.24.0-2
- fix FTBFS of (at least) qpdfview

* Wed Mar 20 2024 Michael J Gruber <mjg@fedoraproject.org> - 1.24.0-1
- rebase to 1.24.0 (rhbz#2270341)
- support more formats (office xml, text, gzipped)
- `mutool bake` command
- redaction options for line art and images
- Art, Bleed, Media, and Trim boxes for PDF page sizes
- various fixes and improvements

* Tue Mar 19 2024 Tom Stellard <tstellar@redhat.com> - 1.23.10-9
- Fix build with llvm18

* Tue Mar 19 2024 Michael J Gruber <mjg@fedoraproject.org> - 1.23.10-8
- avoid multiple rebuilds

* Fri Mar 08 2024 Michael J Gruber <mjg@fedoraproject.org> - 1.23.10-7
- reduce jbig2dec requirements

* Fri Mar 01 2024 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.23.10-6
- Rebuild for gumbo-parse-0.12.1

* Tue Feb 20 2024 Michael J Gruber <mjg@fedoraproject.org> - 1.23.10-5
- streamline make invocation

* Tue Feb 20 2024 Michael J Gruber <mjg@fedoraproject.org> - 1.23.10-4
- build python bindings

* Fri Feb 16 2024 Michael J Gruber <mjg@fedoraproject.org> - 1.23.10-3
- build C and C++ libraries

* Fri Feb 16 2024 Michael J Gruber <mjg@fedoraproject.org> - 1.23.10-2
- Make so executable

* Tue Feb 06 2024 Michael J Gruber <mjg@fedoraproject.org> - 1.23.10-1
- rebase to 1.23.10 (rhbz#2257282)
- minor fixes

* Tue Feb 06 2024 Michael J Gruber <mjg@fedoraproject.org> - 1.23.9-2
- switch to shared libraries

* Tue Feb 06 2024 Michael J Gruber <mjg@fedoraproject.org> - 1.23.9-1
- rebase to 1.23.9 (rhbz#2257282)
- fixes around redaction feature

* Tue Feb 06 2024 Michael J Gruber <mjg@fedoraproject.org> - 1.23.8-1
- rebase to 1.23.8 (rhbz#2257282)
- fixes and adjustments for shared library builds

* Tue Feb 06 2024 Michael J Gruber <mjg@fedoraproject.org> - 1.23.7-8
- set jbig2dec version dependent on fedora version

* Sun Jan 28 2024 Sandro Mani <manisandro@gmail.com> - 1.23.7-7
- Rebuild (tesseract)

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.23.7-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Michael J Gruber <mjg@fedoraproject.org> - 1.23.7-5
- fix time type on i686

* Wed Dec 27 2023 Michael J Gruber <mjg@fedoraproject.org> - 1.23.7-3
- rebuild against fixed leptonica

* Tue Dec 26 2023 Michael J Gruber <mjg@fedoraproject.org> - 1.23.7-2
- adjust to changed leptonica lib name

* Sat Dec 02 2023 Michael J Gruber <mjg@fedoraproject.org> - 1.23.7-1
- rebase to 1.23.7 (rhbz#2249851)
- various bug fixes

* Tue Nov 07 2023 Michael J Gruber <mjg@fedoraproject.org> - 1.23.5-1
- rebase to 1.23.5 (rhbz#2243150)
- Use CropBox as origin for fitz space in PDF documents.
- Various fixes.

* Wed Oct 11 2023 Michael J Gruber <mjg@fedoraproject.org> - 1.23.4-1
- rebase to 1.23.4 (rhbz#2243150)
- default to use CropBox rather than MediaBox
- minor bugfixes

* Sat Oct 07 2023 Sandro Mani <manisandro@gmail.com> - 1.23.3-3
- Rebuild (tesseract)

* Sun Oct 01 2023 Michael J Gruber <mjg@fedoraproject.org> - 1.23.3-2
- fix mutool draw mask endianness on s390x (rhbz#2241203)

* Tue Sep 05 2023 Michael J Gruber <mjg@fedoraproject.org> - 1.23.3-1
- rebase to 1.23.3 (rhbz#2233551)
- Support CropBox, TrimBox, BleedBox, and ArtBox in PDF tools and viewers.
- PhotoShop PSD image support.
- mutool poster: Option to split in RTL direction.
- mutool run: changed many methods to match Java and new WASM library.

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.22.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jul 14 2023 Sandro Mani <manisandro@gmail.com> - 1.22.2-2
- Rebuild (tesseract)

* Thu Jun 22 2023 Michael J Gruber <mjg@fedoraproject.org> - 1.22.2-1
- rebase to 1.22.2 (rhbz#2215574)
- Various bugfixes

* Thu May 11 2023 Michael J Gruber <mjg@fedoraproject.org> - 1.22.1-1
- rebase to 1.22.1 (rhbz#2186766)
- Fix redaction of unmasked images.

* Sat Apr 15 2023 Michael J Gruber <mjg@fedoraproject.org> - 1.22.0-1
- rebase to 1.22.0 (rhbz#2186766)
- Adds new command line tools (mutool recolor and trim) and output format
  (JPEG).
- Overall improvements and enhancements.

* Thu Apr 06 2023 Sandro Mani <manisandro@gmail.com> - 1.21.1-7
- Rebuild (tesseract)

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.21.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Dec 23 2022 Sandro Mani <manisandro@gmail.com> - 1.21.1-5
- Rebuild (tesseract)

* Wed Dec 21 2022 Sandro Mani <manisandro@gmail.com> - 1.21.1-4
- Rebuild (leptonica)

* Tue Dec 20 2022 Michael J Gruber <mjg@fedoraproject.org> - 1.21.1-3
- fix png_write_band (rhbz#2154545) (gsbz#706227)

* Sat Dec 17 2022 Michael J Gruber <mjg@fedoraproject.org> - 1.21.1-2
- SPDX migration

* Tue Dec 13 2022 Michael J Gruber <mjg@fedoraproject.org> - 1.21.1-1
- rebase to 1.21.1 (rhbz#2152708)

* Fri Nov 11 2022 Michael J Gruber <mjg@fedoraproject.org> - 1.21.0-1
- rebase to 1.21.0 (rhbz#2140776)

* Thu Oct 27 2022 Michael J Gruber <mjg@fedoraproject.org> - 1.21.0~rc1-1
- rebase to 1.21.0-rc1

* Fri Aug 12 2022 Michael J Gruber <mjg@fedoraproject.org> - 1.20.3-1
- rebase to 1.20.3 (bz #2104499)

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.20.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jul 08 2022 Sandro Mani <manisandro@gmail.com> - 1.20.0-2
- Rebuild (tesseract)

* Wed Jun 15 2022 Michael J Gruber <mjg@fedoraproject.org> - 1.20.0-1
- rebase to 1.20.0 (bz #2094792)

* Wed Jun 15 2022 Michael J Gruber <mjg@fedoraproject.org> - 1.20.0~rc2-1
- rebase to 1.20.0-rc2

* Wed Jun 15 2022 Michael J Gruber <mjg@fedoraproject.org> - 1.20.0~rc1-1
- rebase to 1.20.0-rc1

* Fri May 20 2022 Sandro Mani <manisandro@gmail.com> - 1.19.0-9
- Rebuild for gdal-3.5.0 and/or openjpeg-2.5.0

* Wed Mar 09 2022 Sandro Mani <manisandro@gmail.com> - 1.19.0-8
- Rebuild for tesseract-5.1.0

* Fri Feb 25 2022 Sandro Mani <manisandro@gmail.com> - 1.19.0-7
- Bump as F36 needs another rebuild

* Fri Feb 25 2022 Sandro Mani <manisandro@gmail.com> - 1.19.0-6
- Rebuild (leptonica)

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.19.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Sun Dec 19 2021 Sandro Mani <manisandro@gmail.com> - 1.19.0-4
- Rebuild (tesseract)

* Tue Dec 14 2021 Sandro Mani <manisandro@gmail.com> - 1.19.0-3
- Rebuild (tesseract)

* Tue Oct 12 2021 Michael J Gruber <mjg@fedoraproject.org> - 1.19.0-2
- enable OCR (leptonica/tesseract)

* Wed Oct 06 2021 Michael J Gruber <mjg@fedoraproject.org> - 1.19.0-1
- rebase to 1.19.0

* Tue Sep 14 2021 Sahana Prasad <sahana@redhat.com> - 1.18.0-9
- Rebuilt with OpenSSL 3.0.0

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.18.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jul 14 2021 Scott Talbert <swt@techie.net> - 1.18.0-7
- Enable DroidSansFallback font

* Wed Feb 24 2021 Michael J Gruber <mjg@fedoraproject.org> - 1.18.0-6
- remove obsolete PyMuPDF support

* Tue Feb 23 2021 Michael J Gruber <mjg@fedoraproject.org> - 1.18.0-5
- CVE-2021-3407 (bz #1931964, bz#1931965)

* Tue Jan 26 2021 Michael J Gruber <mjg@fedoraproject.org> - 1.18.0-4
- (original date: Thu Oct 29 2020)
- remove obsolete patch

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.18.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Oct 08 2020 Michael J Gruber <mjg@fedoraproject.org> - 1.18.0-2
- support PyMuPDF

* Thu Oct 08 2020 Michael J Gruber <mjg@fedoraproject.org> - 1.18.0-1
- bugfix and feature release
- bz #1886338 #1886339 #1886083

* Sun Oct 04 2020 Michael J Gruber <mjg@fedoraproject.org> - 1.18.0-0.1.rc1
- properly name the rc prerelease
- update versions of bundled libs

* Sat Oct 03 2020 Michael J Gruber <mjg@fedoraproject.org> - 1.18.0-rc1
- mupdf 1.18.0-rc1 test

* Fri Sep 18 2020 Michael J Gruber <mjg@fedoraproject.org> - 1.17.0-4
- rebuild with jbig2dec 0.19

* Mon Jul 27 2020 Michael J Gruber <mjg@fedoraproject.org> - 1.17.0-3
- depend on exact jbig2dec version (bz 1861103)

* Sun May 31 2020 Michael J Gruber <mjg@fedoraproject.org> - 1.17.0-2
- fix signature check crash

* Mon May 11 2020 Michael J Gruber <mjg@fedoraproject.org> - 1.17.0-1
- rebase to 1.17.0 (bz #1831652)

* Wed Feb 05 2020 Michael J Gruber <mjg@fedoraproject.org> - 1.16.1-3
- fix build with gcc 10

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.16.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Aug 16 2019 Michael J Gruber <mjg@fedoraproject.org> - 1.16.1-1
- rebase to 1.16.1

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.15.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue May 07 2019 Michael J Gruber <mjg@fedoraproject.org> - 1.15.0-1
- rebase to 1.15.0

* Mon Apr 29 2019 Michael J Gruber <mjg@fedoraproject.org> - 1.15rc1-1
- rc1 test

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.14.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Nov 15 2018 Michael J Gruber <mjg@fedoraproject.org> - 1.14.0-7
- work around missing mesa EGl dependency

* Thu Nov 15 2018 Michael J Gruber <mjg@fedoraproject.org> - 1.14.0-6
- signature handling fix needs more patches than claimed

* Thu Nov 15 2018 Michael J Gruber <mjg@fedoraproject.org> - 1.14.0-5
- fix signature handling

* Thu Nov 15 2018 Michael J Gruber <mjg@fedoraproject.org> - 1.14.0-4
- bz #1644444 #1644445

* Thu Nov 15 2018 Michael J Gruber <mjg@fedoraproject.org> - 1.14.0-3
- bz #1626481 #1626484

* Thu Nov 15 2018 Michael J Gruber <mjg@fedoraproject.org> - 1.14.0-2
- bz #1626483 #1626484

* Thu Nov 15 2018 Michael J Gruber <mjg@fedoraproject.org> - 1.14.0-1
- rebase to 1.14.0

* Mon Oct 01 2018 Michael J Gruber <mjg@fedoraproject.org> - 1.14rc1-3
- mupdf-gl desktop entry

* Mon Oct 01 2018 Michael J Gruber <mjg@fedoraproject.org> - 1.14rc1-2
- enable libcrypto

* Wed Sep 26 2018 Michael J Gruber <mjg@fedoraproject.org> - 1.14rc1-1
- rc test
- adjust to new build system setup

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.13.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sun Jun 10 2018 Michael J Gruber <mjg@fedoraproject.org> - 1.13.0-8
- CVE-2018-10289 (rh bz #1573050) (gs bz #699271)

* Wed Jun 06 2018 Michael J Gruber <mjg@fedoraproject.org> - 1.13.0-7
- fix license field (bug #1586328)

* Sun Jun 03 2018 Michael J Gruber <mjg@fedoraproject.org> - 1.13.0-6
- fix lcms2art build on big endian

* Fri May 18 2018 Michael J Gruber <mjg@fedoraproject.org> - 1.13.0-5
- fix BR (pulled in by freeglut-devel before)

* Mon Apr 23 2018 Michael J Gruber <mjg@fedoraproject.org> - 1.13.0-4
- bundle unicode safe freeglut

* Mon Apr 23 2018 Michael J Gruber <mjg@fedoraproject.org> - 1.13.0-3
- include (now non-empty) libmupdfthird.a again (fixes bug #1553915 for zathura-pdf-mupdf)

* Fri Apr 20 2018 Michael J Gruber <mjg@fedoraproject.org> - 1.13.0-2
- bundle thread-safe lcms2 (fixes bug #1553915)

* Fri Apr 20 2018 Michael J Gruber <mjg@fedoraproject.org> - 1.13.0-1
- rebase to 1.13.0 (rh bz #1569993)

* Fri Apr 13 2018 Michael J Gruber <mjg@fedoraproject.org> - 1.12.0-6
- install svg icon

* Fri Apr 13 2018 Michael J Gruber <mjg@fedoraproject.org> - 1.12.0-6
- install svg icon

* Wed Feb 14 2018 Michael J Gruber <mjg@fedoraproject.org> - 1.12.0-5
- CVE-2018-6192 (rh bz #1539845 #1539846) (gs bz #698916)
- CVE-2018-6544 (rh bz #1542264 #1542265) (gs bz #698830 #698965)
- CVE-2018-1000051 (rh bz #1544847 #1544848) (gs bz #698825 #698873)

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Feb 06 2018 Michael J Gruber <mjg@fedoraproject.org> - 1.12.0-4
- CVE-2018-6187 (rh bz #1538432 #1538433) (gs bz #698908)

* Wed Jan 24 2018 Michael J Gruber <mjg@fedoraproject.org> - 1.12.0-2
- CVE-2017-17858 (rh bz #1537952) (gs bz #698819)
- CVE-2018-5686 (gs bz #698860)

* Thu Dec 14 2017 Michael J Gruber <mjg@fedoraproject.org> - 1.12.0-1
- rebase to 1.12
- follow switch from GLFW to GLUT
- follow switch to new version scheme

* Sun Nov 26 2017 Michael J Gruber <mjg@fedoraproject.org> - 1.12rc1-1
- rc test

* Sat Nov 11 2017 Michael J Gruber <mjg@fedoraproject.org> - 1.11-9
- CVE-2017-15369
- CVE-2017-15587

* Sat Nov 11 2017 Michael J Gruber <mjg@fedoraproject.org> - 1.11-8
- repair FTBFS from version specific patch in 412e729 ("New release 1.11", 2017-04-11)

* Sat Nov 11 2017 Michael J Gruber <mjg@fedoraproject.org> - 1.11-7
- rebuild with jbig2dec 0.14 (#1456731)

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.11-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.11-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue May 09 2017 Pavel Zhukov <landgraf@fedoraproject.org> - 1.11-4
- Rebuild with new jbig2dec (#1443933)

* Fri Apr 14 2017 Pavel Zhukov <landgraf@fedoraproject.org> - 1.11-3
- Fix mupdf-gl build (#1442384)

* Tue Apr 11 2017 Pavel Zhukov <landgraf@fedoraproject.org> - 1.11-1
- New release 1.11 (#1441186)

* Thu Apr  6 2017 Pavel Zhukov <landgraf@fedoraproject.org> - 1.10a-5
- Fix stack consumption CVE (#1439643)

* Thu Mar  2 2017 Pavel Zhukov <landgraf@fedoraproject.org> - 1.10a-4
- fix buffer overflow (#1425338)

* Thu Mar 02 2017 Michael J Gruber <mjg@fedoraproject.org> - 1.10a-3
- Several packaging fixes

* Thu Feb 23 2017 Pavel Zhukov <landgraf@fedoraproject.org> - 1.10a-2
- Add comment with explanation of disabled debuginfo
- Fix make verbose output

* Sat Feb 11 2017 Pavel Zhukov <pzhukov@redhat.com> - 1.10a-1
- New release (1.10a)

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sat Nov 28 2015 Pavel Zhukov <landgraf@fedoraproject.org> -1.8-1
- New release (#1280518)

* Sat Nov 28 2015 Pavel Zhukov <landgraf@fedoraproject.org> -1.7a-4
- Disable memento

* Wed Nov 18 2015 Petr Šabata <contyk@redhat.com> - 1.7a-3
- Package the license text with the %%license macro
- Don't use the %%version macro in filenames, it's not helpful
- Added extra handling for the docs; %%_docdir is no longer autopackaged,
  plus we want to install the license text elsewhere

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7a-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jun 01 2015  Pavel Zhukov <landgraf@fedoraproject.org> - 1.7a-1
- New release 1.7a (#1219482)
* Wed May 06 2015  Pavel Zhukov <landgraf@fedoraproject.org> - 1.7-1
- New release 1.7 (#1210318)
- Fix segfault in obj_close routine (#1202137, #1215752)

* Wed May 06 2015 Pavel Zhukov <landgraf@fedoraproject.org> - 1.5-6
- Fix executable name in desktop file

* Sat Oct 11 2014 Pavel Zhukov <landgraf@fedoraproject.org> - 1.5-5
- Add missed curl-devel

* Fri Jul 04 2014 Pavel Zhukov <landgraf@fedoraproject.org> - 1.5-3
- Add fPIC flag (#1109589)
- Add curl-devel to BR (#1114566)

* Sun Jun 15 2014 Pavel Zhukov <landgraf@fedoraproject.org> - 1.5-2
- Add fix for new openjpeg2

* Sun Jun 15 2014 Pavel Zhukov <landgraf@fedoraproject.org> - 1.5-1
- New release 1.5 (#1108710)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue May  6 2014 Pavel Zhukov <landgraf@fedoraproject.org> - 1.4-1
- New release 1.4 (#1087287)

* Fri Jan 24 2014 Pavel Zhukov <landgraf@fedoraproject.org> - 1.1-5
- Fix stack overflow (#1056699)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Jan 21 2013 Adam Tkac <atkac redhat com> - 1.1-2
- rebuild due to "jpeg8-ABI" feature drop

* Wed Jan 09 2013 Pavel Zhukov <landgraf@fedoraproject.org> - 1.1-1
- New release

* Sun May 20 2012  Pavel Zhukov <landgraf@fedoraproject.org> - 1.0-1
- New release

* Wed Mar 14 2012  Pavel Zhukov <landgraf@fedoraproject.org> - 0.9-2
- Fix buffer overflow (#752388)

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

## END: Generated by rpmautospec
