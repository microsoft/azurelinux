## START: Set by rpmautospec
## (rpmautospec version 0.8.3)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 2;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Reduce debuginfo verbosity
%global optflags %(echo %{optflags} | sed 's/-g /-g1 /')

%bcond_with check
%bcond_with toolchain_clang

%if %{with toolchain_clang}
%global toolchain clang
%endif

%if %{undefined flatpak} && %{undefined rhel}
%if 0%{?fedora} >= 38
%bcond_without graphicsmagick
%else
%bcond_without imagemagick
%endif
%endif

%global inkscape_date 2023-11-16
%global date %(d=%{inkscape_date}; echo ${d//-/})
%global commit 91b66b078370477bd794fe0e1db149c34333dae8
%global shortcommit %(c=%{commit}; echo ${c:0:10})

Name:           inkscape
Version:        1.4.3
Release:        %autorelease
Summary:        Vector-based drawing program using SVG

License:        GPL-2.0-or-later AND CC-BY-3.0
URL:            https://inkscape.org/
Source0:        https://media.inkscape.org/dl/resources/file/inkscape-%{version}.tar.xz

# The signatures were uploaded by the responsible release manager, and includes release date and commit, not using macros because it's inconsistent.
Source1:        https://media.inkscape.org/media/resources/sigs/inkscape-1.4.3_2025-12-25_0d15f75042.tar.xz.sig

# Keyring(s)
Source10:       https://inkscape.org/~MarcJeanmougin/gpg/#/MarcJeanmougin.gpg


# Should we split this package and mark it as a Enhance,
# to clarify the upstream license for this package? -- mochaa, 2023-10-23
# Fedora Color Palette, GIMP format, CC-BY 3.0
Source100:      Fedora-Color-Palette.gpl

# Don't drop i686 until at least texlive no longer needs it -GC, 2023-08-10
#%%if 0%%{?fedora} >= 39
#ExcludeArch:    %%{ix86}
#%%endif

Provides: bundled(libcroco) = 0.6.99~gitb9e4b47
Provides: bundled(autotrace) = 0.40.0~git0de6201
Provides: bundled(libdepixelize) = 0~git19b7601
Provides: bundled(libuemf) = 0.2.8
Provides: bundled(adaptagrams) = 0~gitc8e3196

%if %{with toolchain_clang}
BuildRequires:  clang
%else
BuildRequires:  gcc-c++
%endif

BuildRequires:  cmake

BuildRequires:  gnupg2
BuildRequires:  dos2unix
BuildRequires:  desktop-file-utils
BuildRequires:  libappstream-glib
BuildRequires:  python3-rpm-macros

%if %{with check}
BuildRequires:  %{_bindir}/bc
BuildRequires:  %{_bindir}/convert
%endif

BuildRequires:  gettext-devel
BuildRequires:  pkgconfig(gtest)

%global gtk3_version 3.24

BuildRequires:  pkgconfig(gtkmm-3.0) >= %{gtk3_version}
BuildRequires:  pkgconfig(gdkmm-3.0) >= %{gtk3_version}
BuildRequires:  pkgconfig(gtk+-3.0) >= %{gtk3_version}
BuildRequires:  pkgconfig(gdk-3.0) >= %{gtk3_version}
BuildRequires:  pkgconfig(gtksourceview-4)
BuildRequires:  pkgconfig(gspell-1)

BuildRequires:  cmake(double-conversion)
BuildRequires:  pkgconfig(harfbuzz)
BuildRequires:  pkgconfig(pangocairo) >= 1.44
BuildRequires:  pkgconfig(pangoft2)
BuildRequires:  pkgconfig(fontconfig)
BuildRequires:  pkgconfig(gsl)
BuildRequires:  pkgconfig(gmodule-2.0)
BuildRequires:  pkgconfig(libsoup-2.4) >= 2.42
BuildRequires:  pkgconfig(bdw-gc)
BuildRequires:  pkgconfig(lcms2)
%if 0%{?fedora} >= 39
BuildRequires:  pkgconfig(2geom) >= 1.3.0
%endif
BuildRequires:  pkgconfig(poppler) >= 0.20.0
BuildRequires:  pkgconfig(poppler-glib) >= 0.20.0
BuildRequires:  pkgconfig(cairo-svg)
BuildRequires:  pkgconfig(librevenge-0.0)
BuildRequires:  pkgconfig(librevenge-stream-0.0)
BuildRequires:  pkgconfig(libwpg-0.3)
BuildRequires:  pkgconfig(libvisio-0.1)
BuildRequires:  pkgconfig(libcdr-0.1)

%if %{with imagemagick}
BuildRequires:  pkgconfig(ImageMagick++) < 7
%endif
%if %{with graphicsmagick}
BuildRequires:  pkgconfig(GraphicsMagick++)
%endif

BuildRequires:  pkgconfig(libjpeg)
BuildRequires:  pkgconfig(libpng) >= 1.2

BuildRequires:  pkgconfig(libxslt) >= 1.0.15
BuildRequires:  pkgconfig(libxml-2.0) >= 2.6.11

BuildRequires:  pkgconfig(zlib)
BuildRequires:  pkgconfig(readline)
BuildRequires:  pkgconfig(epoxy)

BuildRequires:  boost-devel >= 1.19.0
%if %{with toolchain_clang}
BuildRequires:  libomp-devel
%endif
BuildRequires:  potrace-devel

Requires:       python%{python3_pkgversion}-libs >= 3.7
Requires:       %{py3_dist inkex}
Requires:       python%{python3_pkgversion}-appdirs

# Weak dependencies for the LaTeX plugin
Suggests:       pstoedit
Suggests:       tex(latex)
Suggests:       tex(dvips)
Suggests:       texlive-amsmath
Suggests:       texlive-amsfonts
Suggests:       texlive-standalone

%description
Inkscape is a vector graphics editor, with capabilities similar to
Illustrator, CorelDraw, or Xara X, using the W3C standard Scalable Vector
Graphics (SVG) file format.  It is therefore a very useful tool for web
designers and as an interchange format for desktop publishing.

Inkscape supports many advanced SVG features (markers, clones, alpha
blending, etc.) and great care is taken in designing a streamlined
interface. It is very easy to edit nodes, perform complex path operations,
trace bitmaps and much more.

%package libs
Summary:        Shared libraries for Inkscape

%description libs
This package provides base libraries to share between Inkscape and Inkview.


%package view
Summary:        Viewing program for SVG files

%description view
Viewer for files in W3C standard Scalable Vector Graphics (SVG) file
format.


%package docs
Summary:        Documentation for Inkscape

%description docs
Tutorial and examples for Inkscape, a graphics editor for vector
graphics in W3C standard Scalable Vector Graphics (SVG) file format.


%prep
%{gpgverify} --keyring='%{SOURCE10}' --signature='%{SOURCE1}' --data='%{SOURCE0}'

%autosetup -n inkscape-1.4.3_2025-12-25_0d15f75042 -p1
%py3_shebang_fix .

# https://bugs.launchpad.net/inkscape/+bug/314381
# A couple of files have executable bits set,
# despite not being executable
find . -name '*.cpp' -print0 | xargs -0 chmod -x
find . -name '*.h' -print0 | xargs -0 chmod -x

%build
%cmake \
        -DWITH_GRAPHICS_MAGICK=%{?with_graphicsmagick:ON}%{!?with_graphicsmagick:OFF} \
        -DWITH_IMAGE_MAGICK=%{?with_imagemagick:ON}%{!?with_imagemagick:OFF} \
        -DBUILD_TESTING:BOOL=%{?with_check:ON}%{!?with_check:OFF}
%cmake_build


%install
%cmake_install

# Install Fedora Color Pallette
install -pm 644 %{SOURCE100} %{buildroot}%{_datadir}/inkscape/palettes/

%find_lang %{name} --with-man

rm -rf %{buildroot}%{_datadir}/inkscape/doc
rm -f %{buildroot}%{_datadir}/doc/inkscape/copyright

# Use system inkex
rm -rf %{buildroot}%{_datadir}/inkscape/extensions/inkex
ln -s %{python3_sitelib}/inkex %{buildroot}%{_datadir}/inkscape/extensions/inkex

%check
%if %{with check}
%ctest
%endif

# Validate appdata file
appstream-util validate-relax --nonet %{buildroot}%{_datadir}/metainfo/*.appdata.xml

# Validate desktop file
desktop-file-validate %{buildroot}%{_datadir}/applications/*.desktop

%pretrans -p <lua>
-- Remove directories that will become symlinks
dirs = {"%{_datadir}/inkscape/extensions/inkex"}
for i, path in ipairs(dirs) do
  st = posix.stat(path)
  if st and st.type == "directory" then
    status = os.rename(path, path .. ".rpmmoved")
    if not status then
      suffix = 0
      while not status do
        suffix = suffix + 1
        status = os.rename(path .. ".rpmmoved", path .. ".rpmmoved." .. suffix)
      end
      os.rename(path, path .. ".rpmmoved")
    end
  end
end


%files -f %{name}.lang
%{!?_licensedir:%global license %%doc}
%license COPYING
%doc AUTHORS NEWS.md README.md
%{_bindir}/inkscape
%dir %{_datadir}/inkscape
%{_datadir}/inkscape/attributes
%{_datadir}/inkscape/branding
%{_datadir}/inkscape/extensions
%{_datadir}/inkscape/filters
%{_datadir}/inkscape/icons
%{_datadir}/inkscape/keys
%{_datadir}/inkscape/markers
%{_datadir}/inkscape/palettes
%{_datadir}/inkscape/paint
%{_datadir}/inkscape/screens
%{_datadir}/inkscape/symbols
%{_datadir}/inkscape/templates
%{_datadir}/inkscape/ui
%{_datadir}/metainfo/org.inkscape.Inkscape.appdata.xml
%{_datadir}/applications/org.inkscape.Inkscape.desktop
%{_mandir}/man1/*.1*
%exclude %{_mandir}/man1/inkview.1*
%{_datadir}/inkscape/tutorials
%{_datadir}/inkscape/themes
%{_datadir}/icons/hicolor/*/apps/*.png
%{_datadir}/icons/hicolor/*/apps/*.svg
%{_datadir}/bash-completion/completions/inkscape
%ghost %{_datadir}/inkscape/extensions/inkex.removed


%files libs
%{!?_licensedir:%global license %%doc}
%license COPYING
%{_libdir}/inkscape/libinkscape_base.so*
%dir %{_libdir}/inkscape/
%ghost %{_datadir}/inkscape/extensions/inkex.rpmmoved*

%files view
%{!?_licensedir:%global license %%doc}
%license COPYING
%doc AUTHORS NEWS.md README.md
%{_bindir}/inkview
%{_mandir}/man1/inkview.1*
%{_mandir}/*/man1/inkview.1*


%files docs
%license COPYING
%dir %{_datadir}/inkscape
%{_datadir}/inkscape/examples


%changelog
## START: Generated by rpmautospec
* Thu Apr 30 2026 Daniel McIlvaney <damcilva@microsoft.com> - 1.4.3-2
- test: add initial lock files

* Fri Jan 02 2026 Gwyn Ciesla <gwync@protonmail.com> - 1.4.3-1
- 1.4.3

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Wed Jul 16 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.4.2-6
- Popper patch

* Wed Jul 16 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.4.2-5
- Popper patch

* Wed Jul 16 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.4.2-4
- Popper patch

* Wed Jul 16 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.4.2-3
- Popper patch

* Wed Jul 16 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.4.2-2
- Popper rebuild

* Tue May 13 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.4.2-1
- 1.4.2

* Thu Feb 20 2025 Marek Kasik <mkasik@redhat.com> - 1.4-6
- Rebuild for poppler 25.02.0

* Mon Feb 10 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.4-5
- Poppler rebuild

* Sun Feb 02 2025 Orion Poplawski <orion@nwra.com> - 1.4-4
- Rebuild with gsl 2.8

* Sun Feb 02 2025 Orion Poplawski <orion@nwra.com> - 1.4-3
- Add upstream patch to fix build with gcc 15 (FTBFS rhbz#2340648)

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Oct 14 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.4-1
- 1.4

* Mon Aug 26 2024 David King <amigadave@amigadave.com> - 1.3.2-12
- Rebuild against gspell

* Thu Aug 22 2024 Marek Kasik <mkasik@redhat.com> - 1.3.2-11
- Rebuild for poppler 24.08.0

* Tue Aug 06 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.3.2-10
- Poppler rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jul 03 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.3.2-8
- Require python3-appdirs

* Sat Jun 01 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.3.2-7
- Fix directory ownership

* Fri Feb 02 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.3.2-6
- Poppler rebuild.

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jan 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jan 17 2024 Jonathan Wakely <jwakely@redhat.com> - 1.3.2-3
- Rebuilt for Boost 1.83

* Wed Nov 29 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.3.2-2
- 1.3.2

* Wed Nov 29 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.3.2-1
- 1.3.2

* Wed Nov 08 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.3-7
- Use system inkex

* Thu Aug 24 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.3-6
- Use system lib2geom on f39+

* Thu Aug 10 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.3-5
- Bring back i686 on f39+

* Wed Aug 02 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.3-4
- No lto on i686

* Wed Aug 02 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.3-3
- Restore i686 for f38.
- Poppler rebuild.

* Tue Aug 01 2023 Kalev Lember <klember@redhat.com> - 1.3-2
- Add missing python3-requests requires (rhbz#2227974)

* Mon Jul 24 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.3-1
- 1.3

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.2-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jun 28 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.2.2-10
- aspell->hunspell

* Wed May 10 2023 Tomas Popela <tpopela@redhat.com> - 1.2.2-9
- Drop BR on dbus-glib as the project is not using it

* Wed Mar 08 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.2.2-8
- migrated to SPDX license

* Fri Feb 24 2023 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 1.2.2-7
- Fix build with GCC 13

* Mon Feb 20 2023 Jonathan Wakely <jwakely@redhat.com> - 1.2.2-6
- Rebuilt for Boost 1.81

* Fri Feb 03 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.2.2-5
- poppler rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Jan 09 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.2.2-3
- Require python3-pillow

* Tue Jan 03 2023 Carl George <carl@george.computer> - 1.2.2-2
- Build against GraphicsMagick instead of ImageMagick on F38+, resolves rhbz#2158052

* Tue Dec 06 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.2.2-1
- 1.2.2

* Tue Aug 23 2022 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.2.1-4
- Rebuild for gsl-2.7.1

* Tue Aug 02 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.2.1-3
- Poppler rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jul 14 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.2.1-1
- 1.2.1

* Mon May 23 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.2-2
- Add missing Requires on python3-cssselect

* Tue May 17 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.2-1
- 1.2

* Tue May 17 2022 Sérgio Basto <sergio@serjux.com> - 1.1.2-4
- ImageMagick is not intended to be on RHEL >= 8 (just on EPEL)

* Wed May 11 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.1.2-3
- ImageMagick build.

* Wed May 04 2022 Thomas Rodgers <trodgers@redhat.com> - 1.1.2-2
- Rebuilt for Boost 1.78

* Sun Feb 06 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.1.2-1
- 1.1.2

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jan 13 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.1.1-3
- Poppler rebuild, with upstream patches.

* Wed Nov 10 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.1.1-2
- Patch for Pango multiline issue.

* Thu Nov 04 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.1.1-1
- 1.1.1

* Wed Aug 18 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.1-10
- Cmake cleanup, BZ 1995130

* Thu Aug 12 2021 Björn Esser <besser82@fedoraproject.org> - 1.1-9
- poppler rebuild, again

* Fri Aug 06 2021 Jonathan Wakely <jwakely@redhat.com> - 1.1-8
- Rebuilt for Boost 1.76

* Mon Aug 02 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.1-7
- poppler rebuild.

* Tue Jul 27 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.1-6
- poppler rebuild.

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Jun 14 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.1-4
- Enable gspell.

* Wed May 26 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.1-3
- Require python3-appdirs

* Tue May 25 2021 Kalev Lember <klember@redhat.com> - 1.1-2
- Don't install development files for bundled 2geom

* Mon May 24 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.1-1
- 1.1

* Thu Feb 11 2021 Jan Horak <jhorak@redhat.com> - 1.0.2-2
- Added missing bundled source, removed libgdlmm depencency

* Mon Feb 01 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.0.2-1
- 1.0.2

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jan 12 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.0.1-4
- Poppler rebuild.

* Mon Jan 04 2021 Tomas Popela <tpopela@redhat.com> - 1.0.1-3
- Don't build with ImageMagick support in ELN/RHEL

* Fri Sep 11 2020 Kalev Lember <klember@redhat.com> - 1.0.1-2
- Fix appdata 1.0.1 release info

* Tue Sep 08 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.0.1-1
- 1.0.1

* Thu Sep 03 2020 Jeff Law <law@redhat.com> - 1.0-8
- Refine dynamic casts to avoid -Wnonnull warning with gcc-11

* Mon Aug 17 2020 Kalev Lember <klember@redhat.com> - 1.0-7
- Drop two unneeded dependencies
- Validate appdata file in check rather than install section
- Use desktop-file-validate instead of desktop-file-install
- Drop unused gtk2 buildrequires

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 14 2020 Tom Stellard <tstellar@redhat.com> - 1.0-5
- Use make macros
- https://fedoraproject.org/wiki/Changes/UseMakeBuildInstallMacro

* Mon Jul 13 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.0-4
- Poppler 0.90.0 rebuild.

* Tue Jun 23 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.0-3
- BR python3-setuptools.

* Thu May 07 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.0-2
- Fix runtime dependencies.

* Fri May 01 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.0-1
- 1.0 final

* Wed Apr 15 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.0-0.rc1.1
- Download version with extensions.

* Sat Apr 11 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.0-0.rc1
- 1.0 RC1

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-0.beta.5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jan 17 2020 Marek Kasik <mkasik@redhat.com> - 1.0-0.beta.4
- Rebuild for poppler-0.84.0

* Wed Dec 04 2019 Gwyn Ciesla <gwync@protonmail.com> - 1.0-0.beta.3
- 1.0 beta 2

* Mon Oct 14 2019 Gwyn Ciesla <gwync@protonmail.com> - 1.0-0.beta.2
- 1.0 beta 1

* Tue Sep 24 2019 Christoph Junghans <junghans@votca.org> - 1.0-0.beta.1
- Rebuild for libdouble-conversion

* Mon Sep 09 2019 Gwyn Ciesla <gwync@protonmail.com> - 1.0-0.beta
- 1.0 beta

* Mon Sep 09 2019 Kalev Lember <klember@redhat.com> - 0.92.4-12.git179c1e14
- Use upstream appdata

* Fri Aug 30 2019 Miro Hrončok <mhroncok@redhat.com> - 0.92.4-11.git179c1e14
- Explicitly depend on Python 3 interpreter
- Use python3 explicitly when building

* Mon Aug 26 2019 Gwyn Ciesla <gwync@protonmail.com> - 0.92.4-10.git179c1e14
- git snapshot for Python 3.

* Tue Aug 20 2019 Susi Lehtola <jussilehtola@fedoraproject.org> - 0.92.4-9
- Rebuilt for GSL 2.6.

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.92.4-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jun 20 2019 Kalev Lember <klember@redhat.com> - 0.92.4-7
- Don't hardcode /usr prefix

* Wed Jun 12 2019 Kalev Lember <klember@redhat.com> - 0.92.4-6
- Avoid ruby dep for flatpak builds

* Wed Mar 27 2019 Gwyn Ciesla <gwync@protonmail.com> - 0.92.4-5
- Build without -D_FORTIFY_SOURCE=2 to work around https://bugs.launchpad.net/inkscape/+bug/1778951

* Fri Feb 08 2019 Gwyn Ciesla <gwync@protonmail.com> - 0.92.4-4
- Drop gvfs.

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.92.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jan 25 2019 Marek Kasik <mkasik@redhat.com> - 0.92.4-2
- Rebuild for poppler-0.73.0

* Thu Jan 17 2019 Gwyn Ciesla <limburgher@gmail.com> - 0.92.4-1
- 0.92.4

* Tue Jan 15 2019 Gwyn Ciesla <limburgher@gmail.com> - 0.92.3-11
- End of line patch.

* Mon Jan 14 2019 Gwyn Ciesla <limburgher@gmail.com> - 0.92.3-10
- Alternate out of bounds patch.

* Fri Jan 11 2019 Gwyn Ciesla <limburgher@gmail.com> - 0.92.3-9
- Patch for out of bounds.

* Tue Dec 04 2018 Gwyn Ciesla <limburgher@gmail.com> - 0.92.3-8
- Add bundled provides.

* Tue Sep 11 2018 Gwyn Ciesla <limburgher@gmail.com> - 0.92.3-7
- Fix shebang handling.

* Tue Aug 28 2018 Michael Cronenworth <mike@cchtml.com> - 0.92.3-6
- Rebuild for ImageMagick 6.9.10

* Tue Aug 14 2018 Marek Kasik <mkasik@redhat.com> - 0.92.3-5
- Rebuild for poppler-0.67.0

* Fri Jul 20 2018 Debarshi Ray <rishi@fedoraproject.org> - 0.92.3-4
- Fix FTBFS due to Python2
- Remove GTK3-based BuildRequires

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.92.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jun 27 2018 Gwyn Ciesla <limburgher@gmail.com> - 0.92.3-2
- Fix for crash, 1575842.

* Tue Apr 17 2018 Gwyn Ciesla <limburgher@gmail.com> - 0.92.3-1
- 0.92.3.

* Fri Mar 23 2018 Marek Kasik <mkasik@redhat.com> - 0.92.2-8
- Rebuild for poppler-0.63.0

* Thu Mar 01 2018 Iryna Shcherbina <ishcherb@redhat.com> - 0.92.2-7
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Wed Feb 14 2018 David Tardon <dtardon@redhat.com> - 0.92.2-6
- rebuild for poppler 0.62.0

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.92.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jan 11 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.92.2-4
- Remove obsolete scriptlets

* Wed Nov 08 2017 David Tardon <dtardon@redhat.com> - 0.92.2-3
- rebuild for poppler 0.61.0

* Fri Oct 06 2017 David Tardon <dtardon@redhat.com> - 0.92.2-2
- rebuild for poppler 0.60.1

* Mon Sep 25 2017 Gwyn Ciesla <limburgher@gmail.com> - 0.92.2-1
- 0.92.2 final.

* Fri Sep 08 2017 David Tardon <dtardon@redhat.com> - 0.92.1-15.20170713bzr15740
- rebuild for poppler 0.59.0

* Tue Sep 05 2017 Adam Williamson <awilliam@redhat.com> - 0.92.1-14.20170713bzr15740
- Rebuild for ImageMagick 6 reversion, drop ImageMagick 7 patch

* Sun Aug 27 2017 Ville Skyttä <ville.skytta@iki.fi> - 0.92.1-13.20170713bzr15740
- Own the /usr/lib/inkscape dir
- %%langify non-English man pages

* Fri Aug 25 2017 Michael Cronenworth <mike@cchtml.com> - 0.92.1-12.20170713bzr15740
- Rebuilt for ImageMagick

* Tue Aug 08 2017 Gwyn Ciesla <limburgher@gmail.com> - 0.92.1-11.20170713bzr15740
- Require aspell-en

* Thu Aug 03 2017 David Tardon <dtardon@redhat.com> - 0.92.1-10.20170713bzr15740
- rebuild for poppler 0.57.0

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.92.1-9.20170713bzr15740
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Sun Jul 30 2017 Kevin Fenzi <kevin@scrye.com> - 0.92.1-8.20170713bzr15740
- Rebuilt for ImageMagick

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.92.1-7.20170713bzr15740
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Jul 13 2017 Gwyn Ciesla <limburgher@gmail.com> - 0.92.1-6.20170713bzr15740
- Updated snapshot.

* Fri Jun 23 2017 Gwyn Ciesla <limburgher@gmail.com> - 0.92.1-5.20170510bzr15686
- Move from gtkspell to gtkspell3, BZ 1464487.

* Wed May 10 2017 Gwyn Ciesla <limburgher@gmail.com> - 0.92.1-4.20170510bzr15686
- Update to fix on Wayland.
- Fix CFLAGS.

* Tue Mar 28 2017 David Tardon <dtardon@redhat.com> - 0.92.1-3.20170321bzr15604
- rebuild for poppler 0.53.0

* Tue Mar 21 2017 Gwyn Ciesla <limburgher@gmail.com> - 0.92.1-2.20170321bzr15604
- Snapshot to fix gcc7 FTBFS.

* Thu Feb 16 2017 Jon Ciesla <limburgher@gmail.com> - 0.92.1-1
- 0.92.1 final.

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.92.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Jan 05 2017 Jon Ciesla <limburgher@gmail.com> - 0.92.0-11
- 0.92 final.

* Fri Dec 30 2016 Jon Ciesla <limburgher@gmail.com> - 0.92-10.pre5
- 0.92pre5.

* Thu Dec 22 2016 Jon Ciesla <limburgher@gmail.com> - 0.92-9.pre4
- 0.92pre4.

* Fri Dec 16 2016 David Tardon <dtardon@redhat.com> - 0.92-8.pre3
- rebuild for poppler 0.50.0

* Mon Nov 28 2016 Jon Ciesla <limburgher@gmail.com> - 0.92-7.pre3
- 0.92pre3.
- Include Fedora Color Palette, BZ 981748

* Wed Nov 23 2016 David Tardon <dtardon@redhat.com> - 0.92-6.pre2
- rebuild for poppler 0.49.0

* Fri Oct 28 2016 Jon Ciesla <limburgher@gmail.com> - 0.92-5.pre2
- Require python-scour, BZ 1389772.

* Fri Oct 28 2016 Jon Ciesla <limburgher@gmail.com> - 0.92-4.pre2
- BR potrace-devel, BZ 1389772.

* Fri Oct 21 2016 Jon Ciesla <limburgher@gmail.com> - 0.92-3.pre2
- Fix release tag.

* Fri Oct 21 2016 Marek Kasik <mkasik@redhat.com> - 0.92-2.pre2
- Rebuild for poppler-0.48.0

* Wed Oct 19 2016 Jon Ciesla <limburgher@gmail.com> - 0.92-0.pre2
- 0.92pre2.

* Mon Jul 18 2016 Marek Kasik <mkasik@redhat.com> - 0.92-1.pre1
- Rebuild for poppler-0.45.0

* Tue Jun 14 2016 Jon Ciesla <limburgher@gmail.com> - 0.92-0.pre1
- 0.92pre1.
- Drop docs requirement on main package, BZ 1247239.

* Tue May 17 2016 Jon Ciesla <limburgher@gmail.com> - 0.92-0.pre0
- 0.92pre0, BZ 1336412.

* Tue May  3 2016 Marek Kasik <mkasik@redhat.com> - 0.91-27
- Rebuild for poppler-0.43.0

* Fri Apr 08 2016 Jon Ciesla <limburgher@gmail.com> - 0.91-26
- Fix FTBFS with patch from https://bugzilla.gnome.org/show_bug.cgi?id=586626

* Mon Feb 22 2016 Orion Poplawski <orion@cora.nwra.com>
- Rebuild for gsl 2.1

* Tue Feb 16 2016 Jonathan Underwood <jonathan.underwood@gmail.com> - 0.91-24
- Add Requires for gvfs

* Mon Feb 15 2016 Jonathan Underwood <jonathan.underwood@gmail.com> - 0.91-23
- Break appdata file out of spec into its own file
- Validate appdata file once installed
- Add BuildRequires for libappstream-glib (provides appstream-util)
- Remove commented out line in file list
- Re-add export CXXFLAGS="%%{optflags} -std=c++11" to fix build

* Mon Feb 15 2016 Jonathan Underwood <jonathan.underwood@gmail.com> - 0.91-22
- Drop --disable-strict-build since this is fixed:
  https://bugzilla.gnome.org/show_bug.cgi?id=752797
- Drop export CXXFLAGS="%%{optflags} -std=c++11" since that's now default

* Mon Feb 15 2016 Jonathan Underwood <jonathan.underwood@gmail.com> - 0.91-21
- Remove BuildRequires for  gnome-vfs2-devel

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.91-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jan 22 2016 Marek Kasik <mkasik@redhat.com> - 0.91-19
- Rebuild for poppler-0.40.0

* Fri Jan 15 2016 Jonathan Wakely <jwakely@redhat.com> - 0.91-18
- Rebuilt for Boost 1.60

* Wed Sep 23 2015 Kalev Lember <klember@redhat.com> - 0.91-17
- Fix the build with latest glibmm24

* Thu Aug 27 2015 Jonathan Wakely <jwakely@redhat.com> - 0.91-16
- Rebuilt for Boost 1.59

* Wed Aug 05 2015 Jonathan Wakely <jwakely@redhat.com> 0.91-15
- Rebuilt for Boost 1.58

* Tue Aug  4 2015 Jonathan Underwood <jonathan.underwood@gmail.com> - 0.91-14
- Remove some entries from unused Requires block that we now
  explicitly Require or Suggests.

* Tue Aug  4 2015 Jonathan Underwood <jonathan.underwood@gmail.com> - 0.91-13
- Add Suggests deps for packages needed to enable LaTeX fragment
  embedding

* Wed Jul 29 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.91-12
- Rebuilt for https://fedoraproject.org/wiki/Changes/F23Boost159

* Thu Jul 23 2015 Adam Williamson <awilliam@redhat.com> - 0.91-11
- --disable-strict-build (as gtkmm currently uses a deprecated glibmm symbol)

* Wed Jul 22 2015 David Tardon <dtardon@redhat.com>
- rebuild for Boost 1.58

* Wed Jul 22 2015 Marek Kasik <mkasik@redhat.com> - 0.91-10
- Rebuild (poppler-0.34.0)

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.91-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jun  5 2015 Marek Kasik <mkasik@redhat.com> - 0.91-8
- Rebuild (poppler-0.33.0)

* Wed Apr 29 2015 Kalev Lember <kalevlember@gmail.com> - 0.91-7
- Rebuilt for GCC 5 ABI change

* Thu Mar 26 2015 Richard Hughes <rhughes@redhat.com> - 0.91-6
- Add an AppData file for the software center

* Fri Mar 06 2015 Jon Ciesla <limburgher@gmail.com> - 0.91-5
- ImageMagick rebuild.

* Thu Feb 12 2015 Peter Robinson <pbrobinson@fedoraproject.org> 0.91-4
- Cleanup spec
- Use %%license
- Drop (now unneeded) perl requirements (rhbz#579390)
- Drop ChangeLog as details are covered in NEWS

* Wed Feb 04 2015 Petr Machata <pmachata@redhat.com> - 0.91-3
- Bump for rebuild.

* Fri Jan 30 2015 Jon Ciesla <limburgher@gmail.com> - 0.91-2
- Move tutorials into main package, BZ 1187686.

* Thu Jan 29 2015 Jon Ciesla <limburgher@gmail.com> - 0.91-1
- Latest upstream.

* Tue Jan 27 2015 Petr Machata <pmachata@redhat.com> - 0.48.5-7
- Rebuild for boost 1.57.0

* Fri Jan 23 2015 Marek Kasik <mkasik@redhat.com> - 0.48.5-6
- Rebuild (poppler-0.30.0)
- Backport commit "Fix build with poppler 0.29.0 (Bug #1399811)"

* Fri Jan 09 2015 Jon Ciesla <limburgher@gmail.com> - 0.48.5-5
- Added aspell support, BZ 1171934.

* Thu Nov 27 2014 Marek Kasik <mkasik@redhat.com> - 0.48.5-4
- Rebuild (poppler-0.28.1)

* Thu Aug 28 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.48.5-3
- Perl 5.20 rebuild

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.48.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Mon Jul 21 2014 Jon Ciesla <limburgher@gmail.com> - 0.48.5-1
- Latest bugfix release.
- Spurious comma patch upstreamed.
- Dropped Freetype, poppler, gc patches.

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.48.4-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Jun 03 2014 Jon Ciesla <limburgher@gmail.com> - 0.48.4-17
- Switch to lcms2.

* Tue May 27 2014 David Tardon <dtardon@redhat.com> - 0.48.4-16
- switch to librevenge-based import libs

* Fri May 23 2014 Petr Machata <pmachata@redhat.com> - 0.48.4-15
- Rebuild for boost 1.55.0

* Thu May 15 2014 Lubomir Rintel <lkundrak@v3.sk> - 0.48.4-14
- Fix build with new Poppler and GC (Sandro Mani, #1097945)

* Wed May 14 2014 Jon Ciesla <limburgher@gmail.com> - 0.48.4-13
- poppler rebuild.

* Mon Mar 31 2014 Jon Ciesla <limburgher@gmail.com> - 0.48.4-12
- ImageMagick rebuild.
- Patch for Freetype path.

* Wed Oct 09 2013 Jon Ciesla <limburgher@gmail.com> - 0.48.4-11
- ImageMagick rebuild.

* Mon Aug 19 2013 Marek Kasik <mkasik@redhat.com> - 0.48.4-10
- Rebuild (poppler-0.24.0)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.48.4-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 30 2013 Petr Machata <pmachata@redhat.com> - 0.48.4-8
- Rebuild for boost 1.54.0

* Wed Jul 24 2013 Petr Pisar <ppisar@redhat.com> - 0.48.4-7
- Perl 5.18 rebuild

* Tue Jun 25 2013 Jon Ciesla <limburgher@gmail.com> - 0.48.4-6
- libpoppler rebuild.

* Mon Mar 18 2013 Jon Ciesla <limburgher@gmail.com> - 0.48.4-5
- ImageMagick rebuild.

* Fri Feb 15 2013 Jon Ciesla <limburgher@gmail.com> - 0.48.4-4
- Fix FTBFS.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.48.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jan 18 2013 Marek Kasik <mkasik@redhat.com> - 0.48.4-2
- Rebuild (poppler-0.22.0)

* Thu Dec 06 2012 Jon Ciesla <limburgher@gmail.com> - 0.48.3.1-4
- 0.48.4, fix XXE security flaw.
- Correct man page ownership.

* Thu Dec 06 2012 Jon Ciesla <limburgher@gmail.com> - 0.48.3.1-4
- Fix directory ownership, BZ 873817.
- Fix previous changelog version.

* Mon Nov 19 2012 Nils Philippsen <nils@redhat.com> - 0.48.3.1-3
- update sourceforge download URL

* Thu Nov 01 2012 Jon Ciesla <limburgher@gmail.com> - 0.48.3.1-2
- Allow loading large XML, BZ 871012.

* Fri Oct 05 2012 Jon Ciesla <limburgher@gmail.com> - 0.48.3.1-1
- Lastest upstream.

* Thu Oct 04 2012 Jon Ciesla <limburgher@gmail.com> - 0.48.2-13
- Added dep on uniconvertor, BZ 796424.

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.48.2-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul 09 2012 Petr Pisar <ppisar@redhat.com> - 0.48.2-11
- Perl 5.16 rebuild

* Mon Jul  2 2012 Marek Kasik <mkasik@redhat.com> - 0.48.2-10
- Rebuild (poppler-0.20.1)

* Wed Jun 27 2012 Petr Pisar <ppisar@redhat.com> - 0.48.2-9
- Perl 5.16 rebuild

* Sat Jun 23 2012 Rex Dieter <rdieter@fedoraproject.org>
- 0.48.2-8
- fix icon/desktop-file scriptlets (#739375)
- drop .desktop vendor (f18+)
- inkscape doesn't build with poppler-0.20.0 (#822413)

* Fri Jun 15 2012 Petr Pisar <ppisar@redhat.com> - 0.48.2-7
- Perl 5.16 rebuild

* Mon Jun 11 2012 Adel Gadllah <adel.gadllah@gmail.com> - 0.48.2-6
- Rebuild for new poppler

* Wed Apr 11 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 0.48.2-5
- Rebuild for ImageMagik

* Thu Mar  8 2012 Daniel Drake <dsd@laptop.org> - 0.48.2-4
- Fix build with GCC 4.7

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.48.2-3
- Rebuilt for c++ ABI breakage

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.48.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Nov 15 2011 German Ruiz <germanrs@fedoraproject.org> - 0.48.2-1
- New upstream version
- Fix glib include compile problem
- Fix compilation against libpng-1.5

* Fri Oct 28 2011 Rex Dieter <rdieter@fedoraproject.org> - 0.48.1-10
- rebuild(poppler)

* Fri Sep 30 2011 Marek Kasik <mkasik@redhat.com> - 0.48.1-9
- Rebuild (poppler-0.18.0)

* Mon Sep 19 2011 Marek Kasik <mkasik@redhat.com> - 0.48.1-8
- Rebuild (poppler-0.17.3)

* Thu Jul 21 2011 Petr Sabata <contyk@redhat.com> - 0.48.1-7
- Perl mass rebuild

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 0.48.1-6
- Perl mass rebuild

* Fri Jul 15 2011 Marek Kasik <mkasik@redhat.com> - 0.48.1-5
- Rebuild (poppler-0.17.0)

* Sun Mar 13 2011 Marek Kasik <mkasik@redhat.com> - 0.48.1-4
- Rebuild (poppler-0.16.3)

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.48.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Feb 09 2011 Lubomir Rintel <lkundrak@v3.sk> - 0.48.1-2
- Re-enable GVFS for OCAL

* Mon Feb 07 2011 Lubomir Rintel <lkundrak@v3.sk> - 0.48.1-1
- Bump release

* Fri Feb 04 2011 Lubomir Rintel <lkundrak@v3.sk> - 0.48.0-10
- Drop gnome-vfs requirement
- Fix Rawhide build

* Sat Jan 01 2011 Rex Dieter <rdieter@fedoraproject.org> - 0.48.0-9
- rebuild (poppler)

* Wed Dec 15 2010 Rex Dieter <rdieter@fedoraproject.org> - 0.48.0-8
- rebuild (poppler)

* Wed Dec 08 2010 Caolán McNamara <caolanm@redhat.com> - 0.48.0-7
- rebuilt (libwpd)

* Sun Nov 14 2010 Lubomir Rintel <lkundrak@v3.sk> - 0.48.0-6
- rebuilt (poppler)

* Tue Oct 05 2010 Nils Philippsen <nils@redhat.com> - 0.48.0-5
- Rebuild for poppler update

* Wed Sep 29 2010 jkeating - 0.48.0-4
- Rebuilt for gcc bug 634757

* Wed Sep 29 2010 Dan Horák <dan[at]danny.cz> - 0.48.0-3
- drop the s390(x) ExcludeArch

* Mon Sep 20 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 0.48.0-2
- rebuild for new ImageMagick

* Wed Aug 25 2010 Lubomir Rintel <lkundrak@v3.sk> - 0.48.0-1
- New upstream release
- Drop el5 support

* Thu Aug 19 2010 Rex Dieter <rdieter@fedoraproject.org> - 0.48-0.5.20100505bzr
- rebuild (poppler)

* Tue Jul 27 2010 David Malcolm <dmalcolm@redhat.com> - 0.48-0.4.20100505bzr
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Tue Jun 01 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.48-0.3.20100505bzr
- Mass rebuild with perl-5.12.0

* Wed May 05 2010 Lubomir Rintel <lkundrak@v3.sk> - 0.48-0.2.20100505bzr
- Move to later snapshot
- Drop uniconvertor patch

* Tue Apr 06 2010 Caolán McNamara <caolanm@redhat.com> - 0.48-0.2.20100318bzr
- Resolves: rhbz#565106 fix inkscape-0.47-x11.patch to not clobber INKSCAPE_LIBS

* Thu Mar 18 2010 Lubomir Rintel <lkundrak@v3.sk> - 0.48-0.1.20100318bzr
- Update to latest bazaar snapshot

* Thu Feb 18 2010 Lubomir Rintel <lkundrak@v3.sk> - 0.47-7
- Fix build

* Wed Jan 20 2010 Stepan Kasal <skasal@redhat.com> - 0.47-6
- ExcludeArch: s390 s390x

* Fri Jan 15 2010 Stepan Kasal <skasal@redhat.com> - 0.47-5
- require perl(:MODULE_COMPAT_5.10.x) because the package requires libperl.so
- the same for inkscape-view

* Fri Jan  8 2010 Owen Taylor <otaylor@redhat.com> - 0.47-4
- Remove loudmouth BuildRequires; there is no current usage of loudmouth in the code

* Sun Dec 06 2009 Lubomir Rintel <lkundrak@v3.sk> - 0.47-2
- Fix Rawhide build.

* Wed Nov 25 2009 Lubomir Rintel <lkundrak@v3.sk> - 0.47-1
- Stable release

* Mon Nov 23 2009 Adam Jackson <ajax@redhat.com> 0.47-0.18.pre4.20091101svn
- Fix RHEL6 build.

* Mon Sep 07 2009 Lubomir Rintel <lkundrak@v3.sk> - 0.47-0.17.pre4.20091101svn
- Icon for main window (#532325)

* Mon Sep 07 2009 Lubomir Rintel <lkundrak@v3.sk> - 0.47-0.16.pre4.20091101svn
- Move to a later snapshot
- python-lxml and numpy seem to be rather popular, add them as hard deps

* Mon Sep 07 2009 Lubomir Rintel <lkundrak@v3.sk> - 0.47-0.16.pre3.20091017svn
- Move to a later snapshot

* Mon Sep 07 2009 Lubomir Rintel <lkundrak@v3.sk> - 0.47-0.16.pre3.20090925svn
- Move to a later snapshot
- Drop debugging compiler flags, enable optimizations again
- Make it build on everything since EL5 again

* Mon Sep 07 2009 Lubomir Rintel <lkundrak@v3.sk> - 0.47-0.16.pre2.20090907svn
- Move inkview man page to -view subpackage (#515358)
- Add license, etc. to main package

* Mon Sep 07 2009 Lubomir Rintel <lkundrak@v3.sk> - 0.47-0.15.pre2.20090907svn
- Update to a post-pre2 snapshot

* Mon Aug 10 2009 Lubomir Rintel <lkundrak@v3.sk> - 0.47-0.15.pre1.20090629svn
- Update to a post-pre1 snapshot
- Drop upstreamed CRC32 fix

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.47-0.14.pre0.20090629svn
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jun 29 2009 Lubomir Rintel <lkundrak@v3.sk> - 0.47-0.13.pre0.20090629svn
- Update to a newer snapshot

* Tue Jun 16 2009 Lubomir Rintel <lkundrak@v3.sk> - 0.47-0.12.pre0.20090616svn
- Update to post-pre0 snapshot

* Tue Jun 02 2009 Lubomir Rintel <lkundrak@v3.sk> - 0.47-0.11.20090602svn
- More recent snapshot
- Upstream removed rasterized icons again

* Sat May 23 2009 Lubomir Rintel <lkundrak@v3.sk> - 0.47-0.10.20090518svn
- Rebuild for new poppler

* Mon May 18 2009 Lubomir Rintel <lkundrak@v3.sk> - 0.47-0.9.20090518svn
- Update past upstream Beta release

* Mon May 18 2009 Lubomir Rintel <lkundrak@v3.sk> - 0.47-0.8.20090508svn
- Fix ODG export

* Fri May 08 2009 Lubomir Rintel <lkundrak@v3.sk> - 0.47-0.7.20090508svn
- Update to a post-alpha snapshot
- Upstream applied our GCC 4.4 patch

* Fri Apr 10 2009 Lubomir Rintel <lkundrak@v3.sk> - 0.47-0.6.20090410svn
- Update to newer snapshot
- Fix doc/incview reversed subpackage content

* Wed Mar 04 2009 Lubomir Rintel <lkundrak@v3.sk> - 0.47-0.6.20090301svn
- Rebuild for new ImageMagick

* Wed Mar 04 2009 Lubomir Rintel <lkundrak@v3.sk> - 0.47-0.5.20090301svn
- Split documentation and inkview into subpackages

* Mon Mar 02 2009 Lubomir Rintel <lkundrak@v3.sk> - 0.47-0.4.20090301svn
- Bump to later SVN snapshot to fix inkscape/+bug/331864
- Fix a startup crash when compiled with GCC 4.4
- It even runs now! :)

* Fri Feb 27 2009 Lubomir Rintel <lkundrak@v3.sk> - 0.47-0.4.20090227svn
- Enable the test suite

* Fri Feb 27 2009 Lubomir Rintel <lkundrak@v3.sk> - 0.47-0.3.20090227svn
- Past midnight! :)
- More recent snapshot, our gcc44 fixes now upstream
- One more gcc44 fix, it even compiles now
- We install icons now, update icon cache
- Disable inkboard, for it won't currently compile

* Thu Feb 26 2009 Lubomir Rintel <lkundrak@v3.sk> - 0.47-0.3.20090226svn
- Later snapshot
- Compile with GCC 4.4

* Tue Jan 06 2009 Lubomir Rintel <lkundrak@v3.sk> - 0.47-0.3.20090105svn
- Update to newer SVN
- Drop upstreamed patches
- Enable WordPerfect Graphics support
- Enable embedded Perl scripting
- Enable Imagemagick support
- Disable OpenSSL due to licensing issues

* Thu Aug 14 2008 Lubomir Rintel <lkundrak@v3.sk> - 0.47-0.3.20080814svn
- Update to today's SVN snapshot
- Drop the upstreamed poppler patch

* Wed Aug 13 2008 Lubomir Rintel <lkundrak@v3.sk> - 0.47-0.2.20080705svn
- Rediff patches for zero fuzz
- Use uniconvertor to handle CDR and WMF (#458845)

* Wed Jul 09 2008 Lubomir Rintel <lkundrak@v3.sk> - 0.47-0.1.20080705svn
- Subversion snapshot

* Wed Jul 09 2008 Lubomir Rintel <lkundrak@v3.sk> - 0.46-4
- Fix compile issues with newer gtk and poppler

* Thu Jun 26 2008 Lubomir Rintel <lkundrak@v3.sk> - 0.46-3
- Remove useless old hack, that triggered an assert after gtkfilechooser switched to gio

* Fri Apr 11 2008 Lubomir Kundrak <lkundrak@redhat.com> - 0.46-2.1
- More buildrequires more flexible, so that this builds on RHEL

* Sat Apr 05 2008 Lubomir Kundrak <lkundrak@redhat.com> - 0.46-2
- Fix LaTeX rendering, #441017

* Tue Mar 25 2008 Lubomir Kundrak <lkundrak@redhat.com> - 0.46-1
- 0.46 released

* Sun Mar 23 2008 Lubomir Kundrak <lkundrak@redhat.com> - 0.46-0.3.pre3
- Rebuild for newer Poppler

* Wed Mar 12 2008 Lubomir Kundrak <lkundrak@redhat.com> - 0.46-0.2.pre3
- Probably last prerelease?

* Fri Feb 22 2008 Lubomir Kundrak <lkundrak@redhat.com> - 0.46-0.2.pre2
- Panel icon sizes

* Sun Feb 17 2008 Lubomir Kundrak <lkundrak@redhat.com> - 0.46-0.1.pre2
- 0.46pre2
- Dropping upstreamed patches

* Sat Feb 16 2008 Lubomir Kundrak <lkundrak@redhat.com> - 0.45.1+0.46pre1-5
- Attempt to fix the font selector (#432892)

* Thu Feb 14 2008 Lubomir Kundrak <lkundrak@redhat.com> - 0.45.1+0.46pre1-4
- Tolerate recoverable errors in OCAL feeds
- Fix OCAL insecure temporary file usage (#432807)

* Wed Feb 13 2008 Lubomir Kundrak <lkundrak@redhat.com> - 0.45.1+0.46pre1-3
- Fix crash when adding text objects (#432220)

* Thu Feb 07 2008 Lubomir Kundrak <lkundrak@redhat.com> - 0.45.1+0.46pre1-2
- Build with gcc-4.3

* Wed Feb 06 2008 Lubomir Kundrak <lkundrak@redhat.com> - 0.45.1+0.46pre1-1
- 0.46 prerelease
- Minor cosmetic changes to satisfy the QA script
- Dependency on Boost
- Inkboard is not optional
- Merge from Denis Leroy's svn16571 snapshot:
- Require specific gtkmm24-devel versions
- enable-poppler-cairo
- No longer BuildRequire libsigc++20-devel

* Wed Dec  5 2007 Denis Leroy <denis@poolshark.org> - 0.45.1-5
- Rebuild with new openssl

* Sun Dec 02 2007 Lubomir Kundrak <lkundrak@redhat.com> - 0.45.1-4
- Added missing dependencies for modules (#301881)

* Sun Dec 02 2007 Lubomir Kundrak <lkundrak@redhat.com> - 0.45.1-3
- Satisfy desktop-file-validate, so that Rawhide build won't break

* Sat Dec 01 2007 Lubomir Kundrak <lkundrak@redhat.com> - 0.45.1-2
- Use GTK print dialog
- Added compressed SVG association (#245413)
- popt headers went into popt-devel, post Fedora 7
- Fix macro usage in changelog

* Wed Mar 21 2007 Denis Leroy <denis@poolshark.org> - 0.45.1-1
- Update to bugfix release 0.45.1
- Added R to ImageMagick-perl (#231563)

* Wed Feb  7 2007 Denis Leroy <denis@poolshark.org> - 0.45-1
- Update to 0.45
- Enabled inkboard, perl and python extensions
- Added patch for correct python autodetection
- LaTex patch integrated upstreamed, removed
- Some rpmlint cleanups

* Wed Dec  6 2006 Denis Leroy <denis@poolshark.org> - 0.44.1-2
- Added patches to fix LaTex import (#217699)
- Added patch to base postscript import on pstoedit plot-svg

* Thu Sep  7 2006 Denis Leroy <denis@poolshark.org> - 0.44.1-1
- Update to 0.44.1
- Removed png export patch, integrated upstream
- Some updated BRs

* Mon Aug 28 2006 Denis Leroy <denis@poolshark.org> - 0.44-6
- FE6 Rebuild

* Tue Aug 22 2006 Denis Leroy <denis@poolshark.org> - 0.44-5
- Removed skencil Require (bug 203229)

* Thu Aug 10 2006 Denis Leroy <denis@poolshark.org> - 0.44-4
- Added patch to fix png dpi export problem (#168406)

* Wed Aug  9 2006 Denis Leroy <denis@poolshark.org> - 0.44-3
- Bumping up release to fix upgrade path

* Wed Jun 28 2006 Denis Leroy <denis@poolshark.org> - 0.44-2
- Update to 0.44
- Removed obsolete patches
- Disabled experimental perl and python extensions
- Added pstoedit, skencil, gtkspell and LittleCms support
- Inkboard feature disabled pending further security tests

* Tue Feb 28 2006 Denis Leroy <denis@poolshark.org> - 0.43-3
- Rebuild

* Mon Jan 16 2006 Denis Leroy <denis@poolshark.org> - 0.43-2
- Updated GC patch, bug 171791

* Sat Dec 17 2005 Denis Leroy <denis@poolshark.org> - 0.43-1
- Update to 0.43
- Added 2 patches to fix g++ 4.1 compilation issues
- Enabled new jabber/loudmouth-based inkboard feature

* Mon Sep 26 2005 Denis Leroy <denis@poolshark.org> - 0.42.2-2
- rebuilt with newer glibmm

* Thu Sep  1 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 0.42.2-1
- update to 0.42.2

* Thu Aug 18 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 0.42-3
- rebuilt
- add patch to repair link-check of GC >= 6.5 (needs pthread and dl)

* Fri Jul 29 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 0.42-2
- Extend ngettext/dgettext patch for x86_64 build.

* Tue Jul 26 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 0.42-1
- update to 0.42 (also fixes #160326)
- BR gnome-vfs2-devel
- no files left in %%_libdir/inkscape
- include French manual page
- GCC4 patch obsolete, 64-bit patch obsolete, dgettext patch split off

* Tue May 31 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 0.41-7
- append another 64-bit related patch (dgettext configure check failed)

* Tue May 31 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 0.41-6
- remove explicit aclocal/autoconf calls in %%build as they create a
  bad Makefile for FC4/i386, which causes build to fail (#156228),
  and no comment explains where they were added/needed

* Tue May 31 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 0.41-5
- bump and rebuild as 0.41-4 failed in build system setup

* Wed May 25 2005 Jeremy Katz <katzj@redhat.com> - 0.41-4
- add patch for gcc4 problems (ignacio, #156228)
- fix build on 64bit boxes.  sizeof(int) != sizeof(void*)

* Sun May 22 2005 Jeremy Katz <katzj@redhat.com> - 0.41-3
- rebuild on all arches

* Thu Apr 07 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Wed Feb 09 2005 Phillip Compton <pcompton[AT]proteinmedia.com> - 0.41-1
- 0.41.
- enable python.

* Sat Dec 04 2004 Phillip Compton <pcompton[AT]proteinmedia.com> - 0.40-1
- 0.40.

* Tue Nov 16 2004 Phillip Compton <pcompton[AT]proteinmedia.com> - 0.40-0.pre3
- 0.40pre3.

* Thu Nov 11 2004 Phillip Compton <pcompton[AT]proteinmedia.com> - 0.39-0.fdr.2
- post/postun for new mime system.
- Dropped redundant BR XFree86-devel.

* Sun Aug 29 2004 Phillip Compton <pcompton[AT]proteinmedia.com> - 0:0.39-0.fdr.1
- 0.39.

* Sat Apr 10 2004 P Linnell <scribusdocs at atlantictechsolutions.com> 0:0.38.1-0.fdr.1
- respin real fix for Provides/Requires for perl(SpSVG)

* Fri Apr 9 2004 P Linnell <scribusdocs at atlantictechsolutions.com> 0:0.38.1-0.fdr.0
- respin with updated tarball with fix for postscript printing

* Thu Apr 8 2004 P Linnell <scribusdocs at atlantictechsolutions.com> 0:0.38-0.fdr.2
- respin to fix provides

* Thu Apr 8 2004 P Linnell <scribusdocs at atlantictechsolutions.com> 0:0.38.0.fdr.1
- version upgrade with many improvements and bug fixes

* Fri Mar 19 2004 P Linnell <scribusdocs at atlantictechsolutions.com> 0:0.37.0.fdr.7
- repsin - sourceforge does not allow reloading files with same name
* Tue Mar 16 2004 P Linnell <scribusdocs at atlantictechsolutions.com> 0:0.37.0.fdr.6
- fix typo in provides
* Tue Mar 16 2004 P Linnell <scribusdocs at atlantictechsolutions.com> 0:0.37.0.fdr.5
- add %%{release} to provides perl(SpSVG) = %%{epoch}:%%{version}:%%{release} only
* Tue Mar 16 2004 P Linnell <scribusdocs at atlantictechsolutions.com> 0:0.37.0.fdr.4
- add %%{release} to provides
* Sun Mar 14 2004 P Linnell <scribusdocs at atlantictechsolutions.com> 0:0.37.0.fdr.3
- add arch dependent flags
* Thu Mar 11 2004 P Linnell <scribusdocs at atlantictechsolutions.com> 0:0.37.0.fdr.2
- add libsigc++-devel instead of add libsigc++ - duh
- add BuildRequires:  perl-XML-Parser
- fix package name to follow package naming guidelines
* Mon Mar 1 2004   P Linnell <scribusdocs at atlantictechsolutions.com>   0:0.37.1.fdr.1
- disable static libs
- enable inkjar
* Tue Feb 10  2004 P Linnell <scribusdocs at atlantictechsolutions.com>   0:0.37.0.fdr.1
- pgp'd tarball from inkscape.org
- clean out the cvs tweaks in spec file
- enable gnome-print
- add the new tutorial files
- make sure .mo file gets packaged
- add provides: perlSVG
- submit to Fedora QA
* Sat Feb 7  2004 P Linnell <scribusdocs at atlantictechsolutions.com>
- rebuild of current cvs
- tweaks to build cvs instead of dist tarball
- add inkview
* Sat Dec 20 2003 P Linnell <scribusdocs at atlantictechsolutions.com>
- First crack at Fedora/RH spec file
- nuke gnome print - it won't work (bug is filed already)

## END: Generated by rpmautospec
