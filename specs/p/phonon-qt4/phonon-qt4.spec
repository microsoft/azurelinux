# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Summary: Multimedia framework api for Qt4
Name:    phonon-qt4
Version: 4.10.3
Release: 28%{?dist}
License: LGPL-2.0-or-later
URL:     https://community.kde.org/Phonon

%global revision %(echo %{version} | cut -d. -f3)
%if %{revision} >= 50
%global stable unstable
%else
%global stable stable
%endif
Source0: https://download.kde.org/%{stable}/phonon/%{version}/phonon-%{version}.tar.xz

## upstream patches

## upstreamable patches
# avoid rpath
Patch10: phonon-rpath_use_link_path.patch
# avoid gcc errors/warnings about use of deprecated _BSD_SOURCE (use _DEFAULT_SOURCE instead) 
Patch11: phonon-DEFAULT_SOURCE.patch

Patch12: phonon-qt4-fix_cmake.patch

# filter plugins
%global __provides_exclude_from ^(%{_qt4_plugindir}/.*\\.so)$

BuildRequires: make
BuildRequires: automoc4 >= 0.9.86
BuildRequires: cmake
BuildRequires: extra-cmake-modules
BuildRequires: kde4-macros(api)
BuildRequires: pkgconfig
BuildRequires: pkgconfig(glib-2.0)
BuildRequires: pkgconfig(libpulse-mainloop-glib) > 0.9.15
BuildRequires: pkgconfig(libxml-2.0)
# Qt4
BuildRequires: pkgconfig(QtDBus)
BuildRequires: pkgconfig(QtDesigner)
BuildRequires: pkgconfig(QtOpenGL)
# added explict dep, despite qt-devel already depending on it
BuildRequires: gcc-c++

Requires: kde-filesystem
Recommends: phonon-qt4-backend-gstreamer%{?_isa}

# phonon -> phonon-qt4 transition
Obsoletes: phonon < 4.10.3-10
Provides:  phonon = %{version}-%{release}
Provides:  phonon%{?_isa} = %{version}-%{release}

%description
%{summary}.

%package devel
Summary: Developer files for phonon
Requires: %{name}%{?_isa} = %{version}-%{release}
Obsoletes: phonon-devel < 4.10.3-10
Provides:  phonon-devel = %{version}-%{release}
Provides:  phonon-devel%{?_isa} = %{version}-%{release}
%description devel
%{summary}.


%prep
%setup -q -n phonon-%{version}

%patch -P10 -p1 -b .10
%patch -P11 -p1 -b .11
%patch -P12 -p1 -b .12


%build
%cmake \
  -DCMAKE_BUILD_TYPE:STRING="Release" \
  -DCMAKE_DISABLE_FIND_PACKAGE_QZeitgeist:BOOL=ON \
  -DPHONON_BUILD_DECLARATIVE_PLUGIN:BOOL=OFF \
  -DPHONON_INSTALL_QT_COMPAT_HEADERS:BOOL=ON \
  -DPHONON_QT_IMPORTS_INSTALL_DIR=%{_qt4_importdir} \
  -DPHONON_QT_MKSPECS_INSTALL_DIR=%{_qt4_datadir}/mkspecs/modules \
  -DPHONON_QT_PLUGIN_INSTALL_DIR=%{_qt4_plugindir}/designer

%cmake_build


%install
%cmake_install

# own these dirs
mkdir -p %{buildroot}%{_kde4_libdir}/kde4/plugins/phonon_backend/
mkdir -p %{buildroot}%{_kde4_datadir}/kde4/services/phononbackends/
mkdir -p %{buildroot}%{_qt5_plugindir}/phonon4qt5_backend


%check
export PKG_CONFIG_PATH="%{buildroot}%{_datadir}/pkgconfig:%{buildroot}%{_libdir}/pkgconfig${PKG_CONFIG_PATH:+:}${PKG_CONFIG_PATH}"
test "$(pkg-config --modversion phonon)" = "%{version}"

%files
%license COPYING.LIB
%{_libdir}/libphonon.so.4*
%{_libdir}/libphononexperimental.so.4*
%{_qt4_plugindir}/designer/libphononwidgets.so
%dir %{_datadir}/phonon/
%dir %{_kde4_libdir}/kde4/plugins/phonon_backend/
%dir %{_kde4_datadir}/kde4/services/phononbackends/

# https://bugzilla.redhat.com/show_bug.cgi?id=1223956
# replacing symlink with a dir
%pretrans devel -p <lua>
path = "%{_includedir}/phonon/Phonon"
st = posix.stat(path)
if st and st.type == "link" then
  os.remove(path)
end

%files devel
%license %{_datadir}/phonon/buildsystem/COPYING-CMAKE-SCRIPTS
%{_datadir}/dbus-1/interfaces/org.kde.Phonon.AudioOutput.xml
%{_datadir}/phonon/buildsystem/
%{_libdir}/cmake/phonon/
%dir %{_includedir}/KDE
%{_includedir}/KDE/Phonon/
%{_includedir}/phonon/
%{_libdir}/pkgconfig/phonon.pc
%{_libdir}/libphonon.so
%{_libdir}/libphononexperimental.so
%{_qt4_datadir}/mkspecs/modules/qt_phonon.pri

%changelog
* Sun Sep 14 2025 Antonio Trande <sagitter@fedoraproject.org> - 4.10.3-28
- Fix rhbz#2381097 rhbz#2381360

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4.10.3-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4.10.3-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Jan 08 2025 Alessandro Astone <ales.astone@gmail.com> - 4.10.3-25
- Fix build dependency on kde4 macros

* Wed Sep 04 2024 Miroslav Suchý <msuchy@redhat.com> - 4.10.3-24
- convert license to SPDX

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.10.3-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.10.3-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.10.3-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.10.3-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.10.3-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.10.3-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.10.3-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.10.3-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.10.3-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Aug 11 2020 Rex Dieter <rdieter@fedoraproject.org> - 4.10.3-14
- fix FTBFS

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.10.3-13
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.10.3-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Rex Dieter <rdieter@fedoraproject.org> - 4.10.3-11
- qt4-only compat package
- fix URL
- bump Release to ensure upgrade path from non-compat pkg
- add explicit BR: gcc-c++
- add comments for each patch
- -devel: %%license: COPYING-CMAKE-SCRIPTS

* Wed Jul 31 2019 Rex Dieter <rdieter@fedoraproject.org> - 4.10.3-1
- 4.10.3

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.10.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Apr 22 2019 Rex Dieter <rdieter@fedoraproject.org> - 4.10.2-3
- rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.10.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Jan 15 2019 Rex Dieter <rdieter@fedoraproject.org> - 4.10.2-1
- 4.10.2

* Mon Sep 24 2018 Owen Taylor <otaylor@redhat.com> - 4.10.1-3
- Pass Qt paths we'll use in the file list to CMake
- In %%check, augment PKG_CONFIG_PATH, not replace it

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.10.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Apr 27 2018 Rex Dieter <rdieter@fedoraproject.org> - 4.10.1-1
- 4.10.1

* Wed Feb 28 2018 Rex Dieter <rdieter@fedoraproject.org> - 4.10.0-4
- Recommends: phonon-backend-gstreamer
- drop versioned pulseaudio

* Wed Feb 28 2018 Adam Williamson <awilliam@redhat.com> - 4.10.0-3
- Back to a non-bootstrap build

* Wed Feb 28 2018 Adam Williamson <awilliam@redhat.com> - 4.10.0-2
- Bootstrapping build (to fix bogus dependency error in gstreamer backend)

* Fri Feb 23 2018 Rex Dieter <rdieter@fedoraproject.org> - 4.10.0-1
- 4.10.0
- .spec cleanup/cosmetics

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.9.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.9.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.9.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Feb 20 2017 Rex Dieter <rdieter@fedoraproject.org> - 4.9.1-3
- rebuild (cmake.prov)

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.9.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Jan 25 2017 Rex Dieter <rdieter@fedoraproject.org> - 4.9.1-1
- phonon-4.9.1
- better handle optional (default off) features: declarative, zeitgeist

* Mon Jan 02 2017 Rex Dieter <rdieter@math.unl.edu> - 4.9.0-4
- filter plugin provides

* Thu May 05 2016 Rex Dieter <rdieter@fedoraproject.org> - 4.9.0-3
- drop revert, fix in other components instead (knotifications, knotifyconfig)

* Fri Apr 29 2016 Rex Dieter <rdieter@fedoraproject.org> - 4.9.0-2
- revert upstream commit causing regression (kde#337276)

* Thu Apr 21 2016 Rex Dieter <rdieter@fedoraproject.org> - 4.9.0-1
- phonon-4.9.0, disable qzeitgeist support

* Wed Apr 20 2016 Rex Dieter <rdieter@fedoraproject.org> - 4.8.3-12
- rebuild (qt5)

* Mon Apr 18 2016 Rex Dieter <rdieter@fedoraproject.org> 4.8.3-11
- rebuild (qt)

* Sun Apr 03 2016 Rex Dieter <rdieter@fedoraproject.org> - 4.8.3-10
- FindPhononInternal.cmake: fix _BSD_SOURCE is deprecated warnings
- FindPhononInternal.cmake: do proper includes, fix FTBFS using Qt-5.6

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 4.8.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Dec 21 2015 Rex Dieter <rdieter@fedoraproject.org> 4.8.3-8
- move xml dbus interface files to -devel, use %%license

* Tue Sep 15 2015 Rex Dieter <rdieter@fedoraproject.org> 4.8.3-7
- -devel: add lua scriptlet workaround for symlink->dir (#1223956)

* Mon Jul 06 2015 Rex Dieter <rdieter@fedoraproject.org> 4.8.3-6
- backport upstream fixes, mostly for Qt5-fPIC-related FTBFS (#1239789)

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.8.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu May 07 2015 Rex Dieter <rdieter@fedoraproject.org> 4.8.3-4
- %%build: -DPHONON_INSTALL_QT_COMPAT_HEADERS (instead of our own symlink hack)

* Thu May 07 2015 Rex Dieter <rdieter@fedoraproject.org> 4.8.3-3
- %%build: -DCMAKE_BUILD_TYPE="Release" (sets -DNDEBUG -DQT_NO_DEBUG)

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 4.8.3-2
- Rebuilt for GCC 5 C++11 ABI change

* Fri Dec 12 2014 Rex Dieter <rdieter@fedoraproject.org> 4.8.3-1
- phonon-4.8.3

* Tue Nov 04 2014 Rex Dieter <rdieter@fedoraproject.org> 4.8.2-1
- phonon-4.8.2

* Sun Oct 19 2014 Rex Dieter <rdieter@fedoraproject.org> 4.8.1-2
- remove qt5-qttools workaround

* Fri Oct 17 2014 Rex Dieter <rdieter@fedoraproject.org> 4.8.1-1
- phonon-4.8.1

* Mon Sep 08 2014 Rex Dieter <rdieter@fedoraproject.org> 4.8.0-2
- 4.8.0

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.7.80-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Thu Aug 14 2014 Rex Dieter <rdieter@fedoraproject.org> 4.7.80-1
- 4.7.80

* Thu Jul 17 2014 Rex Dieter <rdieter@fedoraproject.org> 4.7.2-1.1
- rebuild (for pulseaudio, bug #1117683)

* Mon Jun 23 2014 Rex Dieter <rdieter@fedoraproject.org> 4.7.2-1
- phonon-4.7.2

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.7.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 28 2014 Rex Dieter <rdieter@fedoraproject.org> 4.7.1-3
- use better upstream fix for rootDir issue

* Wed Mar 26 2014 Rex Dieter <rdieter@fedoraproject.org> 4.7.1-2
- backport some upstream fixes, one that fixes building with cmake-3 particularly

* Fri Dec 06 2013 Rex Dieter <rdieter@fedoraproject.org> 4.7.1-1
- phonon-4.7.1

* Fri Nov 15 2013 Rex Dieter <rdieter@fedoraproject.org> 4.7.0-8
- more upstream fixes, upstreamable rpath_use_link_path handling

* Mon Nov 11 2013 Rex Dieter <rdieter@fedoraproject.org> 4.7.0-7
- workaround rootDir bogosity

* Mon Nov 11 2013 Rex Dieter <rdieter@fedoraproject.org> 4.7.0-6
- Ensure-the-PulseAudio-envrionment-is-set-up (kde#327279)

* Mon Nov 11 2013 Rex Dieter <rdieter@fedoraproject.org> 4.7.0-5
- rebuild (qt5 qreal/arm)

* Sun Nov 10 2013 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.7.0-4
- really fix rpath handling (the upstream version of the patch is incomplete)

* Wed Nov 06 2013 Rex Dieter <rdieter@fedoraproject.org> 4.7.0-3
- disable bootstrap

* Tue Nov 05 2013 Rex Dieter <rdieter@fedoraproject.org> 4.7.0-2
- use upstream version of rpath patch

* Tue Nov 05 2013 Rex Dieter <rdieter@fedoraproject.org> 4.7.0-1
- phonon-4.7.0, Qt5 support

* Wed Oct 30 2013 Rex Dieter <rdieter@fedoraproject.org> - 4.6.0-9
- pull in upstream fixes
- PhononConfig.cmake: fix/workaround regression'y cmake behavior

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.6.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.6.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Jul 31 2012 Than Ngo <than@redhat.com> - 4.6.0-6
- add rhel/fedora condition

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.6.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun May 20 2012 Rex Dieter <rdieter@fedoraproject.org> 4.6.0-4
- refresh rpath patch

* Wed Mar 28 2012 Than Ngo <than@redhat.com> - 4.6.0-3
- fix syntax in *.pri file

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 20 2011 Rex Dieter <rdieter@fedoraproject.org> 4.6.0-1
- 4.6.0

* Wed Dec 07 2011 Rex Dieter <rdieter@fedoraproject.org> 4.5.57-4.20111031
- fix plugindir usage (#760039)

* Wed Nov 02 2011 Rex Dieter <rdieter@fedoraproject.org> 4.5.57-3.20111031
- fix release

* Mon Oct 31 2011 Rex Dieter <rdieter@fedoraproject.org> 4.5.57-1.20111031
- 20111031 snapshot

* Mon Oct 31 2011 Rex Dieter <rdieter@fedoraproject.org> 4.5.57-2.20110914
- rebuild (qzeitgeist)

* Fri Sep 23 2011 Rex Dieter <rdieter@fedoraproject.org> 4.5.57-1.20110914
- 4.5.57 20110914 snapshot
- pkgconfig-style deps

* Tue May 24 2011 Rex Dieter <rdieter@fedoraproject.org> 4.5.0-3
- BR: libqzeitgeist-devel

* Fri Apr 08 2011 Rex Dieter <rdieter@fedoraproject.org> 4.5.0-2
- avoid Conflicts with judicious (Build)Requires: qt4(-devel) instead

* Fri Mar 25 2011 Rex Dieter <rdieter@fedoraproject.org> 4.5.0-1
- phonon-4.5.0
- qt-designer-plugin-phonon moved here (from qt)

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.4.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jan 21 2011 Rex Dieter <rdieter@fedoraproject.org> 4.4.4-2
- re-instate allow-stop-empty-source match from mdv

* Fri Jan 21 2011 Rex Dieter <rdieter@fedoraproject.org> 4.4.4-1
- phonon-4.4.4

* Wed Jan 05 2011 Rex Dieter <rdieter@fedoraproject.org> - 4.4.4-0.1.20110104
- Requires: phonon-backend

* Wed Jan 05 2011 Rex Dieter <rdieter@fedoraproject.org> - 4.4.4-0.0.20110104
- phonon-4.4.4 snapshot (sans backends)
- bootstrap without Requires: phonon-backend

* Tue Nov 30 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.4.3-2
- recognize audio/flac in gstreamer backend (kde#257488)

* Wed Nov 24 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.4.3-1
- phonon-4.4.3

* Mon Nov 22 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.4.3-0.4.20101122
- phonon-4.4.3 20101122 snapshot

* Fri Nov 12 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.4.3-0.3.20101112
- phonon-4.4.3 20101112 snapshot

* Tue Oct 19 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.4.3-0.2.20100909
- Requires: kde-filesystem (#644571)
- own %%{_kde4_libdir}/kde4 (<f15) (#644571)

* Thu Sep 09 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.4.3-0.1.20100909
- phonon-4.4.3 20100909 snapshot

* Tue Jun 08 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.4.2-1
- phonon-4.4.2

* Sat Apr 24 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.4.1-2
- phonon-backend-xine-4.4.1 (with pulseaudio) = no audio (kde#235193)

* Thu Apr 22 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.4.1-1
- phonon-4.4.1

* Thu Apr 01 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.4.0-3
- add minimal pulseaudio runtime dep

* Wed Mar 17 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.4.0-2
- pa glib/qt eventloop patch (kde#228324)

* Tue Mar 16 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.4.0-1
- phonon-4.4.0 final

* Fri Mar 12 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.4.0-0.3
- phonon-4.3.80-pulse-devicemove-rejig.patch (from mdv)

* Wed Feb 24 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.4.0-0.2
- preliminary phonon-4.4.0 tarball

* Fri Jan 22 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.3.80-6
- sync w/mdv patches

* Fri Jan 22 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.3.80-5.2
- F11: patch/modularize pa device-manager bits 

* Fri Jan 22 2010 Kevin Kofler <Kevin@tigcc.ticalc.org> - 4.3.80-5.1
- F11: port the old PA device priorities patch as we don't have PA integration

* Thu Jan 21 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.3.80-5
- no sound with phonon-xine/pulseaudio (kde#223662, rh#553945)

* Thu Jan 21 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.3.80-4
- snarf mdv patches

* Mon Jan 18 2010 Than Ngo <than@redhat.com> - 4.3.80-3
- backport GStreamer backend bugfixes, fix random disappearing sound under KDE

* Thu Dec 03 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.3.80-2
- phonon-4.3.80 (upstream tarball, yes getting ridiculous now)

* Thu Dec 03 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.3.80-1.20091203
- phonon-4.3.80 (20091203 snapshot)

* Thu Dec 03 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.3.50-6.20091203
- phonon-4.3.50 (20091203 snapshot)

* Mon Nov 30 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.3.50-5.20091124
- backend-gstreamer: Requires: gstreamer-plugins-good

* Fri Nov 27 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.3.50-4.20091124
- ln -s ../KDE/Phonon %%_includedir/phonon/Phonon (qt/phonon compat)

* Wed Nov 18 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.3.50-3.20091124
- phonon-4.3.50 (20091124 snapshot)
- enable pulseaudio integration (F-12+)

* Wed Nov 18 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.3.50-2.20091118
- phonon-4.3.50 (20091118 snapshot)

* Mon Oct 19 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.3.50-1.20091019
- phonon-4.3.50 (20091019 snapshot)

* Sat Oct 03 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.3.1-102
- Requires: qt4 >= 4.5.2-21 (f12+)

* Tue Sep 29 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.3.1-101
- revert to kde/phonon
- inflate to Release: 101
- -backend-gstreamer: Epoch: 2

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.3.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jun 18 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.3.1-11
- fix for '#' in filenames

* Tue Jun 09 2009 Than Ngo <than@redhat.com> - 4.3.1-10
- make InitialPreference=9

* Sun Jun 07 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.3.1-9
- optimize scriptlets
- Req: phonon >= %%phonon_version_major

* Fri Jun 05 2009 Kevin Kofler <Kevin@tigcc.ticalc.org> - 4.3.1-8
- restore patches to the xine backend

* Fri Jun 05 2009 Than Ngo <than@redhat.com> - 4.3.1-7
- only xine-backend

* Wed May 20 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.3.1-6
- phonon-backend-gstreamer multilib conflict (#501816)

* Wed May 20 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.3.1-5
- s/ImageMagick/GraphicsMagick/, avail on more secondary archs, is faster,
  yields better results.

* Mon May 04 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.3.1-4
- fix Source0 Url
- xine backend will not play files with non-ascii names (kdebug#172242)

* Sat Apr 11 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.3.1-3
- optimize scriptlets
- Provides/Requires: phonon-backend%%{_isa} ...

* Tue Mar  3 2009 Lukáš Tinkl <ltinkl@redhat.com> - 4.3.1-2
- backport GStreamer backend bugfixes (UTF-8 file handling, volume
fader)

* Fri Feb 27 2009 Than Ngo <than@redhat.com> - 4.3.1-1
- 4.3.1

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.3.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Feb 01 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.3.0-5
- put icons in the right subpkg

* Thu Jan 29 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.3.0-4
- Requires: phonon-backend >= %%version
- move icons to hicolor theme and into -backend subpkgs
- BR: libxcb-devel
- move phonon-gstreamer.svg to sources

* Mon Jan 26 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.3.0-3
- BR: automoc4 >= 0.9.86

* Fri Jan 23 2009 Kevin Kofler <Kevin@tigcc.ticalc.org> - 4.3.0-2
- fix typo in postun scriptlet (introduced in 4.2.96-3)

* Thu Jan 22 2009 Than Ngo <than@redhat.com> - 4.3.0-1
- 4.3.0

* Thu Jan 08 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.2.96-3
- new tarball
- put icons/scriptlets into main pkg
- Requires: phonon-backend

* Thu Jan 08 2009 Lorenzo Villani <lvillani@binaryhelix.net> - 4.2.96-2
- add gstreaer-logo.svg

* Thu Jan 08 2009 Lorenzo Villani <lvillani@binaryhelix.net> - 4.2.96-1
- 4.2.96
- rebase phonon-4.2.0-pulseaudio.patch (-> phonon-4.2.96-pulseaudio.patch)
- rebase phonon-4.2.70-xine-pulseaudio.patch 
  (-> phonon-4.2.96-xine-pulseaudio.patch)

* Fri Dec 12 2008 Rex Dieter <rdieter@fedoraproject.org> 4.2.80-3
- rebuild for pkgconfig deps

* Tue Nov 25 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.2.80-2
- phonon-backend-xine: don't Obsolete/Provide itself, Provides: phonon-backend

* Tue Nov 25 2008 Than Ngo <than@redhat.com> 4.2.80-1
- 4.2.80

* Fri Nov 21 2008 Lorenzo Villani <lvillani@binaryhelix.net> - 4.2.80-0.1.20081121svn887051
- Use subversion (4.2.80) snapshot
- phonon-backend-xine subpkg
- make VERBOSE=1
- make install/fast
- Xine backend is in phonon now, add xine-lib-devel as BR
- BR cmake >= 2.6.0
- forward-port xine pulseaudio patch

* Tue Sep 30 2008 Than Ngo <than@redhat.com> 4.2.0-7
- fix tranparent issue by convert

* Tue Sep 30 2008 Than Ngo <than@redhat.com> 4.2.0-6
- add missing icon

* Wed Sep 17 2008 Rex Dieter <rdieter@fedoraproject.org> 4.2.0-5
- Requires: phonon-backend-xine

* Sun Aug 10 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.2.0-4
- rename -backend-gst back to -backend-gstreamer (longer name as -backend-xine)
  The GStreamer backend isn't ready to be the default, and KDE 4.1 also defaults
  to the Xine backend when both are installed.
- fix PulseAudio not being the default in the Xine backend (4.2 regression)

* Sat Aug 02 2008 Rex Dieter <rdieter@fedoraproject.org> 4.2.0-3
- -backend-gst: Obsoletes: -backend-gstreamer < 4.2.0-2

* Thu Jul 24 2008 Rex Dieter <rdieter@fedoraproject.org> 4.2.0-2
- rename -backend-gstreamer -> backend-gst

* Wed Jul 23 2008 Rex Dieter <rdieter@fedoraproject.org> 4.2.0-1
- phonon-4.2.0

* Mon Jul 14 2008 Rex Dieter <rdieter@fedoraproject.org> 4.2-0.4.beta2
- BR: automoc4
- -backend-gstreamer subpkg

* Tue Jul 01 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.2-0.3.beta2
- drop automoc libsuffix patch, no longer needed

* Fri Jun 20 2008 Rex Dieter <rdieter@fedoraproject.org> 4.2-0.2.beta2
- phonon 4.2beta2 (aka 4.1.83)

* Sat Jun 14 2008 Rex Dieter <rdieter@fedoraproject.org> 4.2-0.1.20080614svn820634
- first try

