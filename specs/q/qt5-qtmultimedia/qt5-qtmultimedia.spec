# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global qt_module qtmultimedia

%global openal 1

%global gst 0.10
%if 0%{?fedora} || 0%{?rhel} > 7
%global gst 1.0
%endif

Summary: Qt5 - Multimedia support
Name:    qt5-%{qt_module}
Version: 5.15.18
Release: 2%{?dist}

# See LGPL_EXCEPTIONS.txt, LICENSE.GPL3, respectively, for exception details
License: LGPL-3.0-only OR GPL-3.0-only WITH Qt-GPL-exception-1.0
Url:     http://www.qt.io
%global majmin %(echo %{version} | cut -d. -f1-2)
Source0: https://download.qt.io/official_releases/qt/%{majmin}/%{version}/submodules/%{qt_module}-everywhere-opensource-src-%{version}.tar.xz

## upstream patches
## repo: https://invent.kde.org/qt/qt/qtmultimedia
## branch: kde/5.15
## git format-patch v5.15.16-lts-lgpl
Patch1:   0001-Pass-explicit-GL-api-when-initializing-GStreamer-bac.patch
Patch2:   0002-Drop-obsolete-QtOpengl-dependency.patch

Patch100: %{name}-gcc11.patch

# filter plugin/qml provides
%global __provides_exclude_from ^(%{_qt5_archdatadir}/qml/.*\\.so|%{_qt5_plugindir}/.*\\.so)$

BuildRequires: make
BuildRequires: qt5-qtbase-devel >= %{version}
BuildRequires: qt5-qtbase-private-devel
#libQt5Core.so.5(Qt_5_PRIVATE_API)(64bit)
#libQt5Gui.so.5(Qt_5_PRIVATE_API)(64bit)
%{?_qt5:Requires: %{_qt5}%{?_isa} = %{_qt5_version}}
BuildRequires: qt5-qtdeclarative-devel >= %{version}
BuildRequires: pkgconfig(alsa)
%if "%{?gst}" == "0.10"
BuildRequires: pkgconfig(gstreamer-interfaces-0.10)
%endif
BuildRequires: pkgconfig(gstreamer-%{gst})
BuildRequires: pkgconfig(gstreamer-app-%{gst})
BuildRequires: pkgconfig(gstreamer-audio-%{gst})
BuildRequires: pkgconfig(gstreamer-base-%{gst})
BuildRequires: pkgconfig(gstreamer-pbutils-%{gst})
BuildRequires: pkgconfig(gstreamer-plugins-bad-%{gst})
BuildRequires: pkgconfig(gstreamer-video-%{gst})
BuildRequires: pkgconfig(libpulse) pkgconfig(libpulse-mainloop-glib)
%if 0%{?openal}
BuildRequires: pkgconfig(openal)
%endif
BuildRequires: pkgconfig(xv)
# workaround missing dep
# /usr/include/gstreamer-1.0/gst/gl/wayland/gstgldisplay_wayland.h:26:10: fatal error: wayland-client.h: No such file or directory
BuildRequires: wayland-devel

Provides: bundled(fftreal) = 2.00

%description
The Qt Multimedia module provides a rich feature set that enables you to
easily take advantage of a platforms multimedia capabilites and hardware.
This ranges from the playback and recording of audio and video content to
the use of available devices like cameras and radios.

%package devel
Summary: Development files for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: qt5-qtbase-devel%{?_isa}
Requires: qt5-qtdeclarative-devel%{?_isa}
# Qt5Multimedia.pc containts:
# Libs.private: ... -lpulse-mainloop-glib -lpulse -lglib-2.0
Requires: pkgconfig(libpulse-mainloop-glib)
%description devel
%{summary}.

%package examples
Summary: Programming examples for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
%description examples
%{summary}.


%prep
%autosetup -n %{qt_module}-everywhere-src-%{version} -p1


%build
%{qmake_qt5} \
  CONFIG+=git_build \
  GST_VERSION=%{gst}

%make_build


%install
make install INSTALL_ROOT=%{buildroot}

## .prl/.la file love
# nuke .prl reference(s) to %%buildroot, excessive (.la-like) libs
pushd %{buildroot}%{_qt5_libdir}
for prl_file in *.prl ; do
  sed -i -e "/^QMAKE_PRL_BUILD_DIR/d" ${prl_file}
  if [ -f "$(basename ${prl_file} .prl).so" ]; then
    rm -fv "$(basename ${prl_file} .prl).la"
    sed -i -e "/^QMAKE_PRL_LIBS/d" ${prl_file}
  fi
done
popd


%ldconfig_scriptlets

%files
%license LICENSE.*
%{_qt5_libdir}/libQt5Multimedia.so.5*
%{_qt5_libdir}/libQt5MultimediaQuick.so.5*
%{_qt5_libdir}/libQt5MultimediaWidgets.so.5*
%{_qt5_libdir}/libQt5MultimediaGstTools.so.5*
%if 0%{?openal}
%{_qt5_archdatadir}/qml/QtAudioEngine/
%endif
%{_qt5_archdatadir}/qml/QtMultimedia/
%{_qt5_plugindir}/audio/
%{_qt5_plugindir}/mediaservice/
%{_qt5_plugindir}/playlistformats/
%dir %{_qt5_libdir}/cmake/Qt5Multimedia/
%{_qt5_libdir}/cmake/Qt5Multimedia/Qt5Multimedia_*Plugin.cmake
%dir %{_qt5_libdir}/cmake/Qt5MultimediaWidgets/

%files devel
%{_qt5_headerdir}/QtMultimedia/
%{_qt5_headerdir}/QtMultimediaQuick/
%{_qt5_headerdir}/QtMultimediaWidgets/
%{_qt5_headerdir}/QtMultimediaGstTools/
%{_qt5_libdir}/libQt5Multimedia.so
%{_qt5_libdir}/libQt5Multimedia.prl
%{_qt5_libdir}/libQt5MultimediaQuick.so
%{_qt5_libdir}/libQt5MultimediaQuick.prl
%{_qt5_libdir}/libQt5MultimediaWidgets.so
%{_qt5_libdir}/libQt5MultimediaWidgets.prl
%{_qt5_libdir}/libQt5MultimediaGstTools.so
%{_qt5_libdir}/libQt5MultimediaGstTools.prl
%{_qt5_libdir}/cmake/Qt5Multimedia/Qt5MultimediaConfig*.cmake
%{_qt5_libdir}/cmake/Qt5MultimediaWidgets/Qt5MultimediaWidgetsConfig*.cmake
%{_qt5_libdir}/cmake/Qt5MultimediaGstTools/Qt5MultimediaGstToolsConfig*.cmake
%{_qt5_libdir}/cmake/Qt5MultimediaQuick/Qt5MultimediaQuickConfig*.cmake
%{_qt5_libdir}/pkgconfig/Qt5Multimedia.pc
%{_qt5_libdir}/pkgconfig/Qt5MultimediaWidgets.pc
%{_qt5_archdatadir}/mkspecs/modules/*.pri

%if 0%{?_qt5_examplesdir:1}
%files examples
%license LICENSE.FDL
%{_qt5_examplesdir}/
%endif


%changelog
* Tue Nov 04 2025 Jan Grulich <jgrulich@redhat.com> - 5.15.18-1
- 5.15.18

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 5.15.17-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon May 26 2025 Jan Grulich <jgrulich@redhat.com> - 5.15.17-1
- 5.15.17

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 5.15.16-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jan 09 2025 Zephyr Lykos <fedora@mochaa.ws> - 5.15.16-1
- 5.15.16

* Wed Sep 04 2024 Jan Grulich <jgrulich@redhat.com> - 5.15.15-1
- 5.15.15

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.15.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed May 29 2024 Jan Grulich <jgrulich@redhat.com> - 5.15.14-1
- 5.15.14

* Sat May 25 2024 Fabio Valentini <decathorpe@gmail.com> - 5.15.13-2
- Rebuild for gstreamer-plugins-bad 1.24.

* Thu Mar 14 2024 Jan Grulich <jgrulich@redhat.com> - 5.15.13-1
- 5.15.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.15.12-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.15.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Jan 02 2024 Jan Grulich <jgrulich@redhat.com> - 5.15.12-1
- 5.15.12

* Fri Oct 06 2023 Jan Grulich <jgrulich@redhat.com> - 5.15.11-1
- 5.15.11

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 5.15.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon Jun 12 2023 Jan Grulich <jgrulich@redhat.com> - 5.15.10-1
- 5.15.10

* Tue Apr 11 2023 Jan Grulich <jgrulich@redhat.com> - 5.15.9-1
- 5.15.9

* Tue Jan 31 2023 Jan Grulich <jgrulich@redhat.com> - 5.15.8-3
- migrated to SPDX license

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 5.15.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jan 05 2023 Jan Grulich <jgrulich@redhat.com> - 5.15.8-1
- 5.15.8

* Mon Oct 31 2022 Jan Grulich <jgrulich@redhat.com> - 5.15.7-1
- 5.15.7

* Tue Sep 20 2022 Jan Grulich <jgrulich@redhat.com> - 5.15.6-1
- 5.15.6

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 5.15.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jul 13 2022 Jan Grulich <jgrulich@redhat.com> - 5.15.5-1
- 5.15.5

* Mon May 16 2022 Jan Grulich <jgrulich@redhat.com> - 5.15.4-1
- 5.15.4

* Fri Mar 04 2022 Jan Grulich <jgrulich@redhat.com> - 5.15.3-1
- 5.15.3

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 5.15.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 5.15.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 5.15.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Nov 24 07:54:14 CET 2020 Jan Grulich <jgrulich@redhat.com> - 5.15.2-2
- Rebuild for qtbase with -no-reduce-relocations option

* Fri Nov 20 09:30:46 CET 2020 Jan Grulich <jgrulich@redhat.com> - 5.15.2-1
- 5.15.2

* Fri Oct 16 2020 Jeff Law <law@redhat.com> - 5.15.1-2
- Fix missing #include for gcc-11

* Thu Sep 10 2020 Jan Grulich <jgrulich@redhat.com> - 5.15.1-1
- 5.15.1

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.14.2-3
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.14.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sat Apr 04 2020 Rex Dieter <rdieter@fedoraproject.org> - 5.14.2-1
- 5.14.2

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.13.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Dec 09 2019 Jan Grulich <jgrulich@redhat.com> - 5.13.2-1
- 5.13.2

* Tue Sep 24 2019 Jan Grulich <jgrulich@redhat.com> - 5.12.5-1
- 5.12.5

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5.12.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Jun 28 2019 Rex Dieter <rdieter@fedoraproject.org> - 5.12.4-3
- rebuild (qtbase)

* Fri Jun 28 2019 Rex Dieter <rdieter@fedoraproject.org> - 5.12.4-2
- rebuild (qtbase)

* Fri Jun 14 2019 Jan Grulich <jgrulich@redhat.com> - 5.12.4-1
- 5.12.4

* Tue Jun 04 2019 Jan Grulich <jgrulich@redhat.com> - 5.12.3-1
- 5.12.3

* Fri Feb 15 2019 Rex Dieter <rdieter@fedoraproject.org> - 5.12.1-1
- 5.12.1

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5.11.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Dec 07 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.11.3-1
- 5.11.3

* Fri Sep 21 2018 Jan Grulich <jgrulich@redhat.com> - 5.11.2-1
- 5.11.2

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5.11.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.11.1-1
- 5.11.1

* Sun May 27 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.11.0-1
- 5.11.0
- use %%make_build %%ldconfig_scriptlets

* Wed Feb 14 2018 Jan Grulich <jgrulich@redhat.com> - 5.10.1-1
- 5.10.1

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5.10.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Dec 19 2017 Jan Grulich <jgrulich@redhat.com> - 5.10.0-1
- 5.10.0

* Thu Nov 23 2017 Jan Grulich <jgrulich@redhat.com> - 5.9.3-1
- 5.9.3

* Wed Nov 22 2017 Troy Dawson <tdawson@redhat.com> - 5.9.2-3
- Fix spec file conditionals

* Tue Oct 17 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.9.2-2
- BR: qt5-qtbase-private-devel

* Mon Oct 09 2017 Jan Grulich <jgrulich@redhat.com> - 5.9.2-1
- 5.9.2

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.9.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.9.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jul 19 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.9.1-1
- 5.9.1

* Fri Jun 16 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.9.0-2
- drop shadow/out-of-tree builds (#1456211,QTBUG-37417)

* Wed May 31 2017 Helio Chissini de Castro <helio@kde.org> - 5.9.0-1
- Upstream official release

* Fri May 26 2017 Helio Chissini de Castro <helio@kde.org> - 5.9.0-0.1.rc
- Upstream Release Candidate retagged

* Tue May 09 2017 Helio Chissini de Castro <helio@kde.org> - 5.9.0-0.beta.3
- Upstream beta 3

* Fri Mar 31 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.8.0-2
- -devel: pkgconfig(libpulse-mainloop-glib) (#1438077)

* Mon Jan 30 2017 Helio Chissini de Castro <helio@kde.org> - 5.8.0-1
- New upstream version

* Mon Jan 02 2017 Rex Dieter <rdieter@math.unl.edu> - 5.7.1-4
- filter plugin provides too

* Mon Jan 02 2017 Rex Dieter <rdieter@math.unl.edu> - 5.7.1-3
- filter qml provides

* Sat Dec 10 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.7.1-2
- 5.7.1 dec5 snapshot, drop cmake/pkgconfig style BR

* Wed Nov 09 2016 Helio Chissini de Castro <helio@kde.org> - 5.7.1-1
- New upstream version

* Mon Jul 04 2016 Helio Chissini de Castro <helio@kde.org> - 5.7.0-2
- Compiled with gcc

* Mon Jun 13 2016 Helio Chissini de Castro <helio@kde.org> - 5.7.0-1
- Qt 5.7.0 release

* Thu Jun 09 2016 Jan Grulich <jgrulich@redhat.com> - 5.6.1-1
- Update to 5.6.1

* Sun Mar 20 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.6.0-3
- rebuild

* Fri Mar 18 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.6.0-2
- rebuild

* Mon Mar 14 2016 Helio Chissini de Castro <helio@kde.org> - 5.6.0-1
- 5.6.0 final release

* Tue Feb 23 2016 Helio Chissini de Castro <helio@kde.org> - 5.6.0-0.8.rc
- Update to final RC

* Mon Feb 15 2016 Helio Chissini de Castro <helio@kde.org> - 5.6.0-0.7
- Update RC release

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 5.6.0-0.6.beta
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Dec 28 2015 Rex Dieter <rdieter@fedoraproject.org> 5.6.0-0.5.beta
- update source URL, use %%license, BR: cmake

* Mon Dec 21 2015 Helio Chissini de Castro <helio@kde.org> - 5.6.0-0.4
- Update to final beta release

* Fri Dec 11 2015 Rex Dieter <rdieter@fedoraproject.org> - 5.6.0-0.3
- include BR: qt5-qdoc only in -doc subpkg
- restore bootstrap macro support
- make openal support unconditional (#1069231)

* Thu Dec 10 2015 Helio Chissini de Castro <helio@kde.org> - 5.6.0-0.2
- Official beta release

* Tue Nov 03 2015 Helio Chissini de Castro <helio@kde.org> - 5.6.0-0.1
- Start to implement 5.6.0 beta

* Mon Oct 26 2015 Rex Dieter <rdieter@fedoraproject.org> 5.5.1-4
- pull in upstream fixes, QTBUG-48939 in particular

* Thu Oct 22 2015 Rex Dieter <rdieter@fedoraproject.org> 5.5.1-3
- drop gst support on el6 (QTBUG-48939)

* Thu Oct 15 2015 Helio Chissini de Castro <helio@kde.org> - 5.5.1-2
- Update to final release 5.5.1

* Tue Sep 29 2015 Helio Chissini de Castro <helio@kde.org> - 5.5.1-1
- Update to Qt 5.5.1 RC1

* Wed Jul 29 2015 Rex Dieter <rdieter@fedoraproject.org> 5.5.0-3
- -docs: BuildRequires: qt5-qhelpgenerator, standardize bootstrapping

* Thu Jul 16 2015 Rex Dieter <rdieter@fedoraproject.org> 5.5.0-2
- tighten qtbase dep (#1233829)

* Wed Jul 1 2015 Helio Chissini de Castro <helio@kde.org> 5.5.0-1
- New final upstream release Qt 5.5.0

* Wed Jun 24 2015 Helio Chissini de Castro <helio@kde.org> - 5.5.0-0.2.rc
- Update for official RC1 released packages

* Wed Jun 17 2015 Daniel Vrátil <dvratil@redhat.com> - 5.5.0-0.1.rc
- Qt 5.5.0 RC1

* Wed Jun 03 2015 Jan Grulich <jgrulich@redhat.com> - 5.4.2-1
- 5.4.2

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 5.4.1-3
- Rebuilt for GCC 5 C++11 ABI change

* Fri Feb 27 2015 Rex Dieter <rdieter@fedoraproject.org> - 5.4.1-2
- rebuild (gcc5)

* Tue Feb 24 2015 Jan Grulich <jgrulich@redhat.com> 5.4.1-1
- 5.4.1

* Thu Dec 11 2014 Rex Dieter <rdieter@fedoraproject.org> 5.4.0-1
- 5.4.0 (final) + backported gst1 support from dev/ branch

* Tue Nov 18 2014 Rex Dieter <rdieter@fedoraproject.org> 5.4.0-0.3.20141118.gst1
- wip/gstreamer1 snapshot (#1149885)

* Mon Nov 03 2014 Rex Dieter <rdieter@fedoraproject.org> 5.4.0-0.2.beta
- out-of-tree build, use %%qmake_qt5

* Sun Oct 19 2014 Rex Dieter <rdieter@fedoraproject.org> 5.4.0-0.1.beta
- 5.4.0-beta

* Wed Sep 17 2014 Rex Dieter <rdieter@fedoraproject.org> - 5.3.2-1
- 5.3.2

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.3.1-2.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Thu Jul 17 2014 Rex Dieter <rdieter@fedoraproject.org> 5.3.1-1.1
- rebuild (for pulseaudio, bug #1117683)

* Tue Jun 17 2014 Jan Grulich <jgrulich@redhat.com> - 5.3.1-1
- 5.3.1

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 21 2014 Jan Grulich <jgrulich@redhat.com> 5.3.0-1
- 5.3.0

* Mon May 05 2014 Rex Dieter <rdieter@fedoraproject.org> 5.2.1-2
- use standard (same as qtbase) .prl sanitation

* Wed Feb 05 2014 Rex Dieter <rdieter@fedoraproject.org> 5.2.1-1
- 5.2.1

* Mon Jan 27 2014 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-3
- build -examples only if supported

* Sun Jan 26 2014 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-2
- -examples subpkg

* Thu Dec 12 2013 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-1
- 5.2.0

* Mon Dec 02 2013 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-0.10.rc1
- 5.2.0-rc1

* Sun Nov 10 2013 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-0.4.beta1
- rebuild (arm/qreal)

* Thu Oct 24 2013 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-0.3.beta1
- 5.2.0-beta1

* Wed Oct 16 2013 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-0.2.alpha
- bootstrap ppc

* Wed Oct 02 2013 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-0.1.alpha
- 5.2.0-alpha
- -doc subpkg

* Sat Sep 07 2013 Rex Dieter <rdieter@fedoraproject.org> 5.1.1-2
- ExclusiveArch: %%{ix86} x86_64 %%{arm} (to match qt5-qtdeclarative)

* Thu Aug 29 2013 Rex Dieter <rdieter@fedoraproject.org> 5.1.1-1
- 5.1.1

* Wed Aug 28 2013 Rex Dieter <rdieter@fedoraproject.org> 5.0.2-3
- update Source URL (and refetch tarball)
- improved summary/description

* Thu May 09 2013 Rex Dieter <rdieter@fedoraproject.org> 5.0.2-2
- BR: qt5-qtdeclarative-devel

* Thu Apr 11 2013 Rex Dieter <rdieter@fedoraproject.org> 5.0.2-1
- 5.0.2

* Sat Feb 23 2013 Rex Dieter <rdieter@fedoraproject.org> 5.0.1-1
- first try

