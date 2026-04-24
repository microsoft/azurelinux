# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# include qt5,qt5-devel metapackages or not
# dropped for f32+
%if 0%{?fedora} < 32
%global metapackage 1
%endif

Name: qt5
# This version MUST remain in sync with Qt5 versions!
Version: 5.15.18
Release: 2%{?dist}
Summary: Qt5 meta package
License: GPL-3.0-only
URL:     https://getfedora.org/
Source0: macros.qt5
Source1: macros.qt5-srpm
Source2: qmake-qt5.sh

Requires: qt5-qdbusviewer
Requires: qt5-qt3d
Requires: qt5-qtbase
Requires: qt5-qtbase-gui
Requires: qt5-qtbase-mysql
Requires: qt5-qtbase-postgresql
Requires: qt5-qtconnectivity
Requires: qt5-qtdeclarative
Requires: qt5-qtdoc
Requires: qt5-qtgraphicaleffects
Requires: qt5-qtimageformats
Requires: qt5-qtlocation
Requires: qt5-qtmultimedia
Requires: qt5-qtquickcontrols
Requires: qt5-qtquickcontrols2
Requires: qt5-qtscript
Requires: qt5-qtsensors
Requires: qt5-qtserialport
Requires: qt5-qtsvg
Requires: qt5-qttools
Requires: qt5-qtwayland
Requires: qt5-qtwebchannel
## qtwebengine is not available on all archs, omit for now
## else, need to make qt5 arch'd and deps conditional (on arch)
#Requires: qt5-qtwebengine
Requires: qt5-qtwebsockets
Requires: qt5-qtx11extras
Requires: qt5-qtxmlpatterns

%description
%{summary}.

%package devel
Summary: Qt5 meta devel package
Requires: qt5-rpm-macros
Requires: qt5-qttools-static
Requires: qt5-qtdeclarative-static
Requires: qt5-qtbase-static
Requires: qt5-designer
Requires: qt5-qdoc
Requires: qt5-qhelpgenerator
Requires: qt5-linguist
Requires: qt5-qt3d-devel
Requires: qt5-qtbase-devel
Requires: qt5-qtconnectivity-devel
Requires: qt5-qtdeclarative-devel
Requires: qt5-qtlocation-devel
Requires: qt5-qtmultimedia-devel
Requires: qt5-qtscript-devel
Requires: qt5-qtsensors-devel
Requires: qt5-qtserialport-devel
Requires: qt5-qtsvg-devel
Requires: qt5-qttools-devel
Requires: qt5-qtwayland-devel
Requires: qt5-qtwebchannel-devel
#Requires: qt5-qtwebengine-devel
Requires: qt5-qtwebsockets-devel
Requires: qt5-qtx11extras-devel
Requires: qt5-qtxmlpatterns-devel

%description devel
%{summary}.

%package rpm-macros
Summary: RPM macros for building Qt5 and KDE Frameworks 5 packages
Conflicts: qt5-qtbase-devel < 5.6.0-0.23
%if 0%{?fedora} || 0%{?rhel} >= 8
Requires: cmake >= 3
%endif
%if 0%{?rhel} && 0%{?rhel} < 8
Requires: cmake3
%endif
Requires: gcc-c++
BuildArch: noarch
%description rpm-macros
%{summary}.

%package srpm-macros
Summary: RPM macros for source Qt5 packages
BuildArch: noarch
%description srpm-macros
%{summary}.

%package filesystem
Summary: Filesystem for Qt 5 packages
%description filesystem
Filesystem for Qt 5 packages.

%install
mkdir -p %{buildroot}%{_prefix}/{lib,%{_lib}}/qt5
mkdir -p %{buildroot}%{_prefix}/{lib,%{_lib}}/qt5/bin
mkdir -p %{buildroot}%{_prefix}/{lib,%{_lib}}/qt5/cmake
mkdir -p %{buildroot}%{_prefix}/{lib,%{_lib}}/qt5/examples
mkdir -p %{buildroot}%{_prefix}/{lib,%{_lib}}/qt5/imports
mkdir -p %{buildroot}%{_prefix}/{lib,%{_lib}}/qt5/metatypes
mkdir -p %{buildroot}%{_prefix}/{lib,%{_lib}}/qt5/modules
mkdir -p %{buildroot}%{_prefix}/{lib,%{_lib}}/qt5/libexec
mkdir -p %{buildroot}%{_prefix}/{lib,%{_lib}}/qt5/mkspecs
mkdir -p %{buildroot}%{_prefix}/{lib,%{_lib}}/qt5/plugins
mkdir -p %{buildroot}%{_prefix}/{lib,%{_lib}}/qt5/qml
mkdir -p %{buildroot}%{_datadir}/qt5
mkdir -p %{buildroot}%{_docdir}/qt5
mkdir -p %{buildroot}%{_includedir}/qt5
mkdir -p %{buildroot}%{_datadir}/qt5/translations

install -Dpm644 %{SOURCE0} %{buildroot}%{_rpmconfigdir}/macros.d/macros.qt5
install -Dpm644 %{SOURCE1} %{buildroot}%{_rpmconfigdir}/macros.d/macros.qt5-srpm
install -Dpm755 %{SOURCE2} %{buildroot}%{_bindir}/qmake-qt5.sh
mkdir -p %{buildroot}%{_datadir}/qt5/wrappers
ln -s %{_bindir}/qmake-qt5.sh %{buildroot}%{_datadir}/qt5/wrappers/qmake-qt5
ln -s %{_bindir}/qmake-qt5.sh %{buildroot}%{_datadir}/qt5/wrappers/qmake

# substitute custom flags, and the path to binaries: binaries referenced from
# macros should not change if an application is built with a different prefix.
# %_libdir is left as /usr/%{_lib} (e.g.) so that the resulting macros are
# architecture independent, and don't hardcode /usr/lib or /usr/lib64.
sed -i \
  -e "s|@@QT5_CFLAGS@@|%{?qt5_cflags}|g" \
  -e "s|@@QT5_CXXFLAGS@@|%{?qt5_cxxflags}|g" \
  -e "s|@@QT5_RPM_LD_FLAGS@@|%{?qt5_rpm_ld_flags}|g" \
  -e "s|@@QT5_RPM_OPT_FLAGS@@|%{?qt5_rpm_opt_flags}|g" \
  -e "s|@@QMAKE@@|%{_prefix}/%%{_lib}/qt5/bin/qmake|g" \
  -e "s|@@QMAKE_QT5_WRAPPER@@|%{_bindir}/qmake-qt5.sh|g" \
  %{buildroot}%{_rpmconfigdir}/macros.d/macros.qt5

%if 0%{?metapackage}
mkdir -p %{buildroot}%{_docdir}/qt5
mkdir -p %{buildroot}%{_docdir}/qt5-devel
echo "- Qt5 meta package" > %{buildroot}%{_docdir}/qt5/README
echo "- Qt5 devel meta package" > %{buildroot}%{_docdir}/qt5-devel/README

%files
%{_docdir}/qt5/README

%files devel
%{_docdir}/qt5-devel/README
%endif

%files rpm-macros
%{_rpmconfigdir}/macros.d/macros.qt5
%{_bindir}/qmake-qt5.sh
%{_datadir}/qt5/wrappers/

%files srpm-macros
%{_rpmconfigdir}/macros.d/macros.qt5-srpm

%files filesystem
%dir %{_prefix}/lib/qt5
%dir %{_prefix}/%{_lib}/qt5
%dir %{_prefix}/lib/qt5/bin
%dir %{_prefix}/%{_lib}/qt5/bin
%dir %{_prefix}/lib/qt5/cmake
%dir %{_prefix}/%{_lib}/qt5/cmake
%dir %{_prefix}/lib/qt5/examples
%dir %{_prefix}/%{_lib}/qt5/examples
%dir %{_prefix}/lib/qt5/imports
%dir %{_prefix}/%{_lib}/qt5/imports
%dir %{_prefix}/lib/qt5/metatypes
%dir %{_prefix}/%{_lib}/qt5/metatypes
%dir %{_prefix}/lib/qt5/modules
%dir %{_prefix}/%{_lib}/qt5/modules
%dir %{_prefix}/lib/qt5/libexec
%dir %{_prefix}/%{_lib}/qt5/libexec
%dir %{_prefix}/lib/qt5/mkspecs
%dir %{_prefix}/%{_lib}/qt5/mkspecs
%dir %{_prefix}/lib/qt5/plugins
%dir %{_prefix}/%{_lib}/qt5/plugins
%dir %{_prefix}/lib/qt5/qml
%dir %{_prefix}/%{_lib}/qt5/qml
%dir %{_datadir}/qt5
%dir %{_docdir}/qt5
%dir %{_includedir}/qt5
%dir %{_datadir}/qt5/translations


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

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.15.14-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jul 15 2024 Jan Grulich <jgrulich@redhat.com> - 5.15.14-2
- Introduce qt5-filesystem package

* Wed May 29 2024 Jan Grulich <jgrulich@redhat.com> - 5.15.14-1
- 5.15.14

* Mon May 06 2024 Liu Yang <Yang.Liu.sn@gmail.com> - 5.15.13-2
- Add riscv64 to macro %qt5_qtwebengine_arches.

* Mon Mar 11 2024 Jan Grulich <jgrulich@redhat.com> - 5.15.13-1
- 5.15.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.15.12-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.15.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Jan 02 2024 Jan Grulich <jgrulich@redhat.com> - 5.15.12-1
- 5.15.12

* Sun Oct 08 2023 Jan Grulich <jgrulich@redhat.com> - 5.15.11-1
- 5.15.11

* Fri Oct 06 2023 Jan Grulich <jgrulich@redhat.com> - 5.15.10-3
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

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 5.15.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 5.15.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 5.15.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Nov 20 08:56:04 CET 2020 Jan Grulich <jgrulich@redhat.com> - 5.15.2-1
- 5.15.2

* Thu Sep 10 2020 Jan Grulich <jgrulich@redhat.com> - 5.15.1-1
- 5.15.1

* Wed Aug 19 2020 Troy Dawson <tdawson@redhat.com> - 5.14.2-5
- fix rpm-macros for RHEL builds

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.14.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Apr 06 2020 Rex Dieter <rdieter@fedoraproject.org> - 5.14.2-3
- drop qt5,qt5-devel metapackages f32+

* Mon Apr 06 2020 Rex Dieter <rdieter@fedoraproject.org> - 5.14.2-2
- qt5-devel: drop R: qt5-qtenginio-devel

* Sat Apr 04 2020 Rex Dieter <rdieter@fedoraproject.org> - 5.14.2-1
- 5.14.2
- drop qt5-qtwebkit from metapackage (hasn't been a core qt5 pkg for awhile)

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.13.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Dec 09 2019 Jan Grulich <jgrulich@redhat.com> - 5.13.2-1
- 5.13.2

* Tue Sep 24 2019 Jan Grulich <jgrulich@redhat.com> - 5.12.5-1
- 5.12.5

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5.12.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Jun 11 2019 Jan Grulich <jgrulich@redhat.com> - 5.12.4-1
- 5.12.4

* Tue Jun 04 2019 Jan Grulich <jgrulich@redhat.com> - 5.12.3-1
- 5.12.3

* Thu Feb 14 2019 Rex Dieter <rdieter@fedoraproject.org> - 5.12.1-1
- 5.12.1

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5.11.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Dec 07 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.11.3-1
- 5.11.3

* Fri Sep 21 2018 Jan Grulich <jgrulich@redhat.com> - 5.11.2-1
- 5.11.2

* Tue Aug 21 2018 Owen Taylor <otaylor@redhat.com> - 5.11.1-4
- rpm-macros: always refer to binaries in their installed location, even if %%_libdir
  and %%_bindir are redefined.

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5.11.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jun 29 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.11.1-2
- %%_qt5_prefix=%%_prefix (was %%_libdir/qt5}

* Tue Jun 19 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.11.1-1
- 5.11.1

* Sat Jun 02 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.11.0-2
- rpm-macros: do not define _qt5_archdatadir, _qt5_bindir in terms of _qt5_prefix anymore

* Sat May 26 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.11.0-1
- 5.11.0

* Wed Mar 07 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.10.1-1
- 5.10.1
- rpm-macros: Requires: gcc-c++

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5.10.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jan 24 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.10.0-4
- macros.qt5: fix path to qmake-qt5.sh wrapper

* Wed Jan 24 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.10.0-3
- use noarch-friendly paths for qmake-qt5.sh wrapper

* Wed Jan 24 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.10.0-2
- provide qmake-qt5.sh wrapper and new macro: %%qmake_qt5_wrapper

* Wed Jan 03 2018 Rex Dieter <rdieter@fedoraproject.org> 5.10.0-1
- 5.10.0

* Wed Jan 03 2018 Rex Dieter <rdieter@fedoraproject.org> 5.9.3-1
- 5.9.3

* Tue Oct 10 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.9.2-1
- 5.9.2

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.9.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jul 19 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.9.1-1
- 5.9.1

* Thu Jun 01 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.9.0-2
- drop -fno-delete-null-pointer-checks hack/workaround

* Sat Apr 15 2017 Helio Chissini de Castro <helio@kde.org> - 5.9.0-1
- Up to match upcoming 5.9.0

* Fri Mar 31 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.8.0-3
- rebuild

* Fri Jan 27 2017 Helio Chissini de Castro <helio@kde.org> - 5.8.0-1
- Tie to new upstream release

* Mon Jan 02 2017 Rex Dieter <rdieter@math.unl.edu> - 5.7.1-2
- drop Requires: qt5-gstreamer qt5-qtacountsservice qt5-qtconfiguration (not from qtproject.org)

* Wed Nov 09 2016 Helio Chissini de Castro <helio@kde.org> - 5.7.1-1
- Prepare for new release

* Tue Sep 27 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.7.0-10
- s/%%rhel/%%epel/ , cmake3 is only available in epel

* Wed Sep 14 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.7.0-9
- install the right macros.qt5-srpm file

* Wed Sep 14 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.7.0-8
- introduce -srpm-macros (initially defines %%qt5_qtwebengine_arches)
- -devel: drop Requires: qt5-qtwebengine-devel (since not all archs are supported)

* Sat Jul 23 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.7.0-7
- drop Requires: qt5-qtwebengine (not available on all archs)

* Tue Jul 12 2016 Helio Chissini de Castro <helio@kde.org> - 5.7.0-6
- Fix macros with invalid substitutions.

* Wed Jul 06 2016 Helio Chissini de Castro <helio@kde.org> - 5.7.0-5
- Fix typo. Thanks to Diego Herrera.
- Add macro qt5_includedir as more logical than headerdir. Old one still available

* Mon Jul 04 2016 Helio Chissini de Castro <helio@kde.org> - 5.7.0-4
- Clang is not default anymore. End of experimentation phase

* Wed Jun 15 2016 Helio Chissini de Castro <helio@kde.org> - 5.7.0-3
- Move package to be qt5 and create meta packages
- Add new macro for qml dir

* Mon Jun 13 2016 Helio Chissini de Castro <helio@kde.org> - 5.7.0-2
- Test repositories using clang by default


* Thu Jun 09 2016 Helio Chissini de Castro <helio@kde.org> - 5.7.0-1
- Decouple macros from main qtbase package
