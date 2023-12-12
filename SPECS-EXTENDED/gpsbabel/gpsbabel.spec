%global gittag 1_8_0

Summary:        A tool to convert between various formats used by GPS devices
Name:           gpsbabel
Version:        1.8.0
Release:        4%{?dist}
License:        GPLv2+
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://www.gpsbabel.org
# Upstream's website hides tarball behind some ugly php script
# Original repo is at https://github.com/gpsbabel/gpsbabel
Source0:        https://github.com/GPSBabel/gpsbabel/archive/refs/tags/%{name}_1_8_0.tar.gz#/%{name}-%{version}.tar.gz
Source2:        %{name}.png
# No automatic phone home by default (RHBZ 668865)
Patch1:         0002-No-solicitation.patch

%ifarch %{qt5_qtwebengine_arches}
# HACK: Don't build GUI on archs not supported by qtwebengine
%global build_gui 1
BuildRequires:  qt5-qtwebchannel-devel
BuildRequires:  qt5-qtwebengine-devel
%endif
BuildRequires:  cmake
BuildRequires:  desktop-file-utils
BuildRequires:  libusb1-devel
BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qtserialport-devel
BuildRequires:  shapelib-devel
BuildRequires:  zlib-devel

%description
Converts GPS waypoint, route, and track data from one format type
to another.

%if 0%{?build_gui}
%package gui
Summary:        Qt GUI interface for GPSBabel
Requires:       %{name} = %{version}-%{release}

%description gui
Qt GUI interface for GPSBabel
%endif

%prep
%autosetup -n %{name}-%{name}_%{gittag} -p1

%build
%cmake \
  -DGPSBABEL_WITH_ZLIB=pkgconfig \
  -DGPS_BABEL_WITH_SHAPE_LIB=pkgconfig \
  -DGPSBABEL_WITH_SHAPELIB=pkgconfig \
  %{?!build_gui:-DGPSBABEL_MAPPREVIEW=OFF} \
  .
%cmake_build


%install
%cmake_install

install -m 0755 -d %{buildroot}/%{_bindir}
install -m 0755 -p gpsbabel %{buildroot}/%{_bindir}

%if 0%{?build_gui}
install -m 0755 -d %{buildroot}%{_bindir}/
install -m 0755 -p %{_vpath_builddir}/gui/GPSBabelFE/gpsbabelfe %{buildroot}%{_bindir}/

install -m 0755 -d %{buildroot}%{_qt5_translationdir}/
install -m 0644 -p gui/gpsbabelfe_*.qm     %{buildroot}%{_qt5_translationdir}/

install -m 0755 -d %{buildroot}%{_qt5_translationdir}/
install -m 0644 -p gui/coretool/gpsbabel_*.qm %{buildroot}%{_qt5_translationdir}/

install -m 0755 -d %{buildroot}%{_datadir}/gpsbabel
install -m 0644 -p gui/gmapbase.html %{buildroot}%{_datadir}/gpsbabel

desktop-file-install \
        --dir %{buildroot}/%{_datadir}/applications \
        gui/gpsbabel.desktop

install -m 0755 -d            %{buildroot}%{_datadir}/icons/hicolor/256x256/apps/
install -m 0644 -p %{SOURCE2} %{buildroot}%{_datadir}/icons/hicolor/256x256/apps/

%find_lang %{name} --with-qt --all-name
%endif

%check
make check

%files
%doc README* AUTHORS
%license COPYING
%{_bindir}/gpsbabel

%if 0%{?build_gui}
%files gui -f %{name}.lang
%doc gui/{AUTHORS,README*,TODO}
%license gui/COPYING*
%{_bindir}/gpsbabelfe
%{_datadir}/gpsbabel
%{_datadir}/applications/*
%{_datadir}/icons/hicolor/256x256/apps/*
%endif

%changelog
* Wed Aug 09 2023 Archana Choudhary <archana1@microsoft.com> - 1.8.0-4
- Initial CBL-Mariner import from Fedora 37 (license: MIT)
- License verified
- Add check section

* Tue Aug 02 2022 Fedora Release Engineering <corsepiu@fedoraproject.org> - 1.8.0-3
- Build against libusb1 instead of libusb (F37FTBS, RHBZ#2113432).

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sat Jan 22 2022 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.8.0-1
- Update to 1.8.0.
- Drop unused patches.
- Drop qtwebkit (Upstream unsupported).

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Sep 03 2020 Jeff Law <law@redhat.com> - 1.7.0-2
- Drop local extern decl for errno (again)

* Thu Aug 13 2020 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.7.0-1
- Update to 1.7.0.
- Rework patches.

* Wed Jul 29 2020 Jeff Law <law@redhat.com> - 1.6.0-6
- Avoid function local external declaration of errno

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu May 23 2019 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.6.0-2
- Add 0007-Reflect-gpsbabelfe-bin-having-been-renamed-into-gpsb.patch (tstevens4).
- Add 0008-Pickup-translations-from-usr-share-qt5-translations.patch (tstevens4).
- Add 0009-Fix-loading-of-meta-catalogs.patch (tstevens4).
- Install gui/coretool/gpsbabel_*.qm into %%{_qt5_translationdir}.

* Fri May 03 2019 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.6.0-1
- Update to 1.6.0
- Rebase patches
- Drop BR: minizip* (Dropped by upstream).
- Reflect gpsbabelfe-bin having been renamed into gpsbabelfe.
- Drop support for fedora < 28.

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.4-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Sep 05 2018 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.5.4-12
- Add 0009-Remove-SHAPE-ZLIB-MINIZIP-from-LIBOBJS.patch (RHBZ#1625204).

* Tue Aug 28 2018 Patrik Novotný <panovotn@redhat.com> - 1.5.4-11
- change requires to minizip-compat(-devel) rhbz#1609830, rhbz#1615381

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.4-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Apr 03 2018 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.5.4-9
- Add 0008-Correctly-read-diff-and-terr-from-geo-format.patch (RHBZ#1561337)

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.4-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Aug 14 2017 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.5.4-7
- Re-add non-gui-packages on Archs not supported by qtwebengine (RHBZ#1481163).

* Mon Aug 07 2017 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.5.4-6
- Add 0007-Added-geojson-read-capablity-moved-magic-strings-to-.patch (F27FTBFS).
- Switch to using qtwebengine on Fedora >= 27.
  Drop archs not supporting qtwebengine.

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Jan 16 2017 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.5.4-2
- Switch back to qtwebkit on Fedora <= 26.

* Sun Jan 15 2017 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.5.4-1
- Update to gpsbabel-1.5.4.
- Rebase patches.
- Build against qt5/qt5-qtwebengine.
- Use %%qt5_translationdir.
- Misc. *spec cleanup.

* Sun Dec 11 2016 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.5.3-6
- Add %%{__make}, %%{__perl}.

* Sun Dec 11 2016 Igor Gnatenko <ignatenko@redhat.com> - 1.5.3-5
- Rebuild for shapelib SONAME bump

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Feb 02 2016 Rex Dieter <rdieter@fedoraproject.org> - 1.5.3-3
- use %%qmake_qt4 macro to ensure proper build flags

* Wed Jan 27 2016 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.5.3-2
- Add %%license to *-gui.

* Thu Jan 07 2016 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.5.3-1
- Upstream update.
- Rebase patches.
- Reflect upstream shipping malpackaged tarballs.
- Unbundle minizip.
- Remove gpsbabel-tarball.
- Introduce %%license.

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 1.5.2-2
- Rebuilt for GCC 5 C++11 ABI change

* Fri Jan 09 2015 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.5.2-1
- Upstream update.
- Rebase patches.
- Reflect upstream having stopped providing tarballs:
  - Add gpsbabel-tarball.
  - Remove gpsbabel-download-latest.py.

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Apr 16 2014 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.5.0-1
- Update to 1.5.0.
- Rebase/rework patches.
- Rework spec.

* Tue Apr 15 2014 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.4.4-6
- Update gpsbabel-1.4.3-use-system-shapelib.patch to fix FTBFS.
- More spec modernization.

* Wed Jul 31 2013 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.4.4-5
- Modernize spec.
- Drop Fedora < 14.
- Really apply patch25 (missed in *-3).
- Fix broken %%changelog date.

* Tue Jul 30 2013 Conrad Meyer <cemeyer@uw.edu> - 1.4.4-4
- Fix Garmin .fit file handling (RHBZ 989851).

* Sun Mar 24 2013 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.4.4-3
- Add aarch64 (RHBZ 925480).

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Sep 17 2012 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.4.4-1
- Upstream update.
- Rebase patches.
- Use upstream gpsbabel.desktop.
- Address RHBZ 668865.
- Fix gzFile pointer abuse.
- Install gmapbase.html to /usr/share/gpsbabel.

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Jul 21 2011 Petr Sabata <contyk@redhat.com> - 1.4.2-6
- Rebuild for libusb-config (#715220)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jan 13 2011 Hans Ulrich Niedermann <hun@n-dimensional.de> - 1.4.2-4
- Have this spec file build on f12,f13,f14,f15,el6. (el6 without GUI).
- Rename local copy of style3.css
- Ship translations for the GUI
- Enforce network less doc build with xsltproc --nonet

* Tue Jan 11 2011 Hans Ulrich Niedermann <hun@n-dimensional.de> - 1.4.2-2
- Shut up desktop-file-install warnings
- Comment the patches in the spec file

* Tue Jan 11 2011 Hans Ulrich Niedermann <hun@n-dimensional.de> - 1.4.2-1
- Update to 1.4.2
- Document how to get source tarball via HTTP POST
- Use Fedora's system shapelib instead of gpsbabel's bundled shapelib parts
- Use new mktemp based BuildRoot
- Build and view gpsbabel.html without network access
- Avoid rpm macros for scriptlet commands
- Remove x bit also from src files in subdirectories
- Add Additional Category to .desktop file: Geography

* Fri Sep 17 2010 Mikhail Kalenkov <mikhail.kalenkov@gmail.com> - 1.4.1-2
- build documentation (gpsbabel.html)

* Thu Sep 16 2010 Mikhail Kalenkov <mikhail.kalenkov@gmail.com> - 1.4.1-1
- update to 1.4.1

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Nov 05 2008 Douglas E. Warner <silfreed@silfreed.net> - 1.3.6-1
- update to 1.3.6

* Fri May 09 2008 Douglas E. Warner <silfreed@silfreed.net> - 1.3.5-1
- update to 1.3.5
- switching out variables for macros; adding macros for commands
- fixing license to be GPLv2+
- adding patch to fix re-running autoconf
- perserving times when installing gpsbabel

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.3.4-2
- Autorebuild for GCC 4.3

* Tue Dec 18 2007 Douglas E. Warner <silfreed@silfreed.net> - 1.3.4-1
- Update to 1.3.4

* Thu Apr 19 2007 Roozbeh Pournader <roozbeh@farsiweb.info> - 1.3.3-1
- Make first Fedora spec based on the one provided upstream
