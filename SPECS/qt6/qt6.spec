# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.


Name: qt6
# This version MUST remain in sync with Qt6 versions!
Version: 6.10.2
Release: 1%{?dist}
Summary: Qt6 meta package
License: GPL-3.0-only
URL:     https://getfedora.org/
Source0: macros.qt6
Source1: macros.qt6-srpm
Source2: qmake-qt6.sh
Source3: qt6qml.attr
Source4: qt6qml.prov

Requires: qt6-qt3d
Requires: qt6-qt5compat
Requires: qt6-qtbase
Requires: qt6-qtbase-gui
Requires: qt6-qtbase-mysql
Requires: qt6-qtbase-postgresql
Requires: qt6-qtcharts
Requires: qt6-qtconnectivity
Requires: qt6-qtdatavis3d
Requires: qt6-qtdeclarative
Requires: qt6-qtimageformats
Requires: qt6-qtlocation
Requires: qt6-qtmultimedia
Requires: qt6-qtnetworkauth
Requires: qt6-qtpositioning
Requires: qt6-qtquick3d
Requires: qt6-qtquicktimeline
Requires: qt6-qtremoteobjects
Requires: qt6-qtscxml
Requires: qt6-qtsensors
Requires: qt6-qtserialbus
Requires: qt6-qtserialport
Requires: qt6-qtshadertools
Requires: qt6-qtsvg
Requires: qt6-qttools
Requires: qt6-qtvirtualkeyboard
Requires: qt6-qtwayland
Requires: qt6-qtwebchannel
Requires: qt6-qtwebsockets


%description
%{summary}.

%package devel
Summary: Qt6 meta devel package
Requires: qt6-designer
Requires: qt6-linguist
Requires: qt6-qt3d-devel
Requires: qt6-qt5compat-devel
Requires: qt6-qtbase-devel
Requires: qt6-qtbase-static
Requires: qt6-qtcharts-devel
Requires: qt6-qtconnectivity-devel
Requires: qt6-qtdatavis3d-devel
Requires: qt6-qtdeclarative-devel
Requires: qt6-qtdeclarative-static
Requires: qt6-qtlocation-devel
Requires: qt6-qtmultimedia-devel
Requires: qt6-qtnetworkauth-devel
Requires: qt6-qtpositioning-devel
Requires: qt6-qtquick3d-devel
Requires: qt6-qtquicktimeline-devel
Requires: qt6-qtremoteobjects-devel
Requires: qt6-qtscxml-devel
Requires: qt6-qtsensors-devel
Requires: qt6-qtserialbus-devel
Requires: qt6-qtserialport-devel
Requires: qt6-qtshadertools-devel
Requires: qt6-qtsvg-devel
Requires: qt6-qttools-devel
Requires: qt6-qttools-static
Requires: qt6-qtvirtualkeyboard-devel
Requires: qt6-qtwayland-devel
Requires: qt6-qtwebchannel-devel
Requires: qt6-qtwebsockets-devel
Requires: qt6-rpm-macros

%description devel
%{summary}.

%package rpm-macros
Summary: RPM macros for building Qt6 and KDE Frameworks 6 packages
Requires: cmake >= 3
Requires: gcc-c++
BuildArch: noarch
%description rpm-macros
%{summary}.

%package srpm-macros
Summary: RPM macros for source Qt6 packages
BuildArch: noarch
%description srpm-macros
%{summary}.

%package filesystem
Summary: Filesystem for Qt6 packages
%description filesystem
Filesystem for Qt 6 packages.

%install
# See macros.qt6 where the directories are specified
mkdir -p %{buildroot}%{_prefix}/lib/qt6
mkdir -p %{buildroot}%{_prefix}/lib/qt6/bin
mkdir -p %{buildroot}%{_prefix}/lib/qt6/cmake
mkdir -p %{buildroot}%{_prefix}/lib/qt6/examples
mkdir -p %{buildroot}%{_prefix}/lib/qt6/imports
mkdir -p %{buildroot}%{_prefix}/lib/qt6/metatypes
mkdir -p %{buildroot}%{_prefix}/lib/qt6/modules
mkdir -p %{buildroot}%{_prefix}/lib/qt6/libexec
mkdir -p %{buildroot}%{_prefix}/lib/qt6/mkspecs
mkdir -p %{buildroot}%{_prefix}/lib/qt6/plugins
mkdir -p %{buildroot}%{_prefix}/lib/qt6/qml
%if "%{_lib}" != "lib"
mkdir -p %{buildroot}%{_prefix}/%{_lib}/qt6
mkdir -p %{buildroot}%{_prefix}/%{_lib}/qt6/bin
mkdir -p %{buildroot}%{_prefix}/%{_lib}/qt6/cmake
mkdir -p %{buildroot}%{_prefix}/%{_lib}/qt6/examples
mkdir -p %{buildroot}%{_prefix}/%{_lib}/qt6/imports
mkdir -p %{buildroot}%{_prefix}/%{_lib}/qt6/metatypes
mkdir -p %{buildroot}%{_prefix}/%{_lib}/qt6/modules
mkdir -p %{buildroot}%{_prefix}/%{_lib}/qt6/libexec
mkdir -p %{buildroot}%{_prefix}/%{_lib}/qt6/mkspecs
mkdir -p %{buildroot}%{_prefix}/%{_lib}/qt6/plugins
mkdir -p %{buildroot}%{_prefix}/%{_lib}/qt6/qml
%endif
mkdir -p %{buildroot}%{_datadir}/qt6
mkdir -p %{buildroot}%{_docdir}/qt6
mkdir -p %{buildroot}%{_includedir}/qt6
mkdir -p %{buildroot}%{_datadir}/qt6/translations


install -Dpm644 %{SOURCE0} %{buildroot}%{_rpmmacrodir}/macros.qt6
install -Dpm644 %{SOURCE1} %{buildroot}%{_rpmmacrodir}/macros.qt6-srpm
install -Dpm755 %{SOURCE2} %{buildroot}%{_bindir}/qmake-qt6.sh
install -Dpm644 %{SOURCE3} %{buildroot}%{_fileattrsdir}/qt6qml.attr
install -Dpm755 %{SOURCE4} %{buildroot}%{_rpmconfigdir}/qt6qml.prov
mkdir -p %{buildroot}%{_datadir}/qt6/wrappers
ln -s %{_bindir}/qmake-qt6.sh %{buildroot}%{_datadir}/qt6/wrappers/qmake-qt6
ln -s %{_bindir}/qmake-qt6.sh %{buildroot}%{_datadir}/qt6/wrappers/qmake

# substitute custom flags, and the path to binaries: binaries referenced from
# macros should not change if an application is built with a different prefix.
# %_libdir is left as /usr/%{_lib} (e.g.) so that the resulting macros are
# architecture independent, and don't hardcode /usr/lib or /usr/lib64.
sed -i \
  -e "s|@@QT6_CFLAGS@@|%{?qt6_cflags}|g" \
  -e "s|@@QT6_CXXFLAGS@@|%{?qt6_cxxflags}|g" \
  -e "s|@@QT6_RPM_LD_FLAGS@@|%{?qt6_rpm_ld_flags}|g" \
  -e "s|@@QT6_RPM_OPT_FLAGS@@|%{?qt6_rpm_opt_flags}|g" \
  -e "s|@@QMAKE@@|%{_prefix}/%%{_lib}/qt6/bin/qmake|g" \
  -e "s|@@QMAKE_QT6_WRAPPER@@|%{_bindir}/qmake-qt6.sh|g" \
  %{buildroot}%{_rpmconfigdir}/macros.d/macros.qt6

%if 0%{?metapackage}
mkdir -p %{buildroot}%{_docdir}/qt6
mkdir -p %{buildroot}%{_docdir}/qt6-devel
echo "- Qt6 meta package" > %{buildroot}%{_docdir}/qt6/README
echo "- Qt6 devel meta package" > %{buildroot}%{_docdir}/qt6-devel/README

%files
%{_docdir}/qt6/README

%files devel
%{_docdir}/qt6-devel/README
%endif

%files rpm-macros
%{_fileattrsdir}/qt6qml.attr
%{_rpmconfigdir}/qt6qml.prov
%{_rpmmacrodir}/macros.qt6
%{_bindir}/qmake-qt6.sh
%{_datadir}/qt6/wrappers/

%files srpm-macros
%{_rpmmacrodir}/macros.qt6-srpm


%files filesystem
%dir %{_prefix}/lib/qt6
%dir %{_prefix}/lib/qt6/bin
%dir %{_prefix}/lib/qt6/cmake
%dir %{_prefix}/lib/qt6/examples
%dir %{_prefix}/lib/qt6/imports
%dir %{_prefix}/lib/qt6/metatypes
%dir %{_prefix}/lib/qt6/modules
%dir %{_prefix}/lib/qt6/libexec
%dir %{_prefix}/lib/qt6/mkspecs
%dir %{_prefix}/lib/qt6/plugins
%dir %{_prefix}/lib/qt6/qml
%if "%{_lib}" != "lib"
%dir %{_prefix}/%{_lib}/qt6
%dir %{_prefix}/%{_lib}/qt6/bin
%dir %{_prefix}/%{_lib}/qt6/cmake
%dir %{_prefix}/%{_lib}/qt6/examples
%dir %{_prefix}/%{_lib}/qt6/imports
%dir %{_prefix}/%{_lib}/qt6/metatypes
%dir %{_prefix}/%{_lib}/qt6/modules
%dir %{_prefix}/%{_lib}/qt6/libexec
%dir %{_prefix}/%{_lib}/qt6/mkspecs
%dir %{_prefix}/%{_lib}/qt6/plugins
%dir %{_prefix}/%{_lib}/qt6/qml
%endif
%dir %{_datadir}/qt6
%dir %{_docdir}/qt6
%dir %{_includedir}/qt6
%dir %{_datadir}/qt6/translations


%changelog
* Mon Feb 09 2026 Jan Grulich <jgrulich@redhat.com> - 6.10.2-1
- 6.10.2

* Mon Jan 19 2026 Marcin Juszkiewicz <mjuszkiewicz@redhat.com> - 6.10.1-3
- Add riscv64 support to qt6_qtwebengine_arches macro

* Sat Jan 17 2026 Fedora Release Engineering <releng@fedoraproject.org> - 6.10.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Thu Nov 20 2025 Jan Grulich <jgrulich@redhat.com> - 6.10.1-1
- 6.10.1

* Tue Oct 07 2025 Jan Grulich <jgrulich@redhat.com> - 6.10.0-1
- 6.10.0

* Thu Sep 25 2025 Jan Grulich <jgrulich@redhat.com> - 6.10.0~rc-1
- 6.10.0 RC

* Thu Aug 28 2025 Jan Grulich <jgrulich@redhat.com> - 6.9.2-1
- 6.9.2

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 6.9.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jun 02 2025 Jan Grulich <jgrulich@redhat.com> - 6.9.1-1
- 6.9.1

* Tue Apr 15 2025 Pavel Solovev <daron439@gmail.com> - 6.9.0-2
- Enable configuration summary

* Wed Apr 02 2025 Jan Grulich <jgrulich@redhat.com> - 6.9.0-1
- 6.9.0

* Fri Mar 21 2025 Jan Grulich <jgrulich@redhat.com> - 6.9.0~rc-1
- 6.9.0 RC

* Mon Feb 17 2025 Jan Grulich <jgrulich@redhat.com> - 6.8.2-2
- Add ppc64le support to qt6_qtwebengine_arches macro

* Fri Jan 31 2025 Jan Grulich <jgrulich@redhat.com> - 6.8.2-1
- 6.8.2

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 6.8.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Dec 10 2024 Jan Grulich <jgrulich@redhat.com> - 6.8.1-4
- Create lib64 directories only on 64bit architectures

* Thu Dec 05 2024 Jan Grulich <jgrulich@redhat.com> - 6.8.1-3
- Fix qt6_metatypesdir macro

* Thu Dec 05 2024 Jan Grulich <jgrulich@redhat.com> - 6.8.1-2
- Add qt6_metatypesdir and qt6_descriptionsdir macros

* Mon Dec 02 2024 Jan Grulich <jgrulich@redhat.com> - 6.8.1-1
- 6.8.1

* Wed Oct 09 2024 Jan Grulich <jgrulich@redhat.com> - 6.8.0-1
- 6.8.0

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.7.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jul 15 2024 Jan Grulich <jgrulich@redhat.com> - 6.7.2-2
- Introduce qt6-filesystem package

* Mon Jul 01 2024 Jan Grulich <jgrulich@redhat.com> - 6.7.2-1
- 6.7.2

* Tue May 21 2024 Jan Grulich <jgrulich@redhat.com> - 6.7.1-1
- 6.7.1

* Tue Apr 02 2024 Jan Grulich <jgrulich@redhat.com> - 6.7.0-1
- 6.7.0

* Sun Jan 28 2024 Jan Grulich <jgrulich@redhat.com> - 6.6.2-1
- 6.6.2

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.6.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.6.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jan 03 2024 Alessandro Astone <ales.astone@gmail.com> - 6.6.1-3
- Make qml dependency generator script executable

* Tue Dec 05 2023 Yaakov Selkowitz <yselkowitz@fedoraproject.org> - 6.6.1-2
- Auto-generate qt6qml() virtual provides

* Mon Nov 27 2023 Jan Grulich <jgrulich@redhat.com> - 6.6.1-1
- 6.6.1

* Tue Oct 10 2023 Jan Grulich <jgrulich@redhat.com> - 6.6.0-1
- 6.6.0

* Sun Oct 01 2023 Justin Zobel <justin.zobel@gmail.com> - 6.5.3-1
- Update to 6.5.3

* Tue Sep 05 2023 Yaakov Selkowitz <yselkowi@redhat.com> - 6.5.2-3
- Fix %%qt6_qtwebengine_arches

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 6.5.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jul 21 2023 Jan Grulich <jgrulich@redhat.com> - 6.5.2-1
- 6.5.2

* Mon May 22 2023 Jan Grulich <jgrulich@redhat.com> - 6.5.1-1
- 6.5.1

* Mon Apr 03 2023 Jan Grulich <jgrulich@redhat.com> - 6.5.0-1
- 6.5.0

* Thu Mar 23 2023 Jan Grulich <jgrulich@redhat.com> - 6.4.2-4
- 6.4.3

* Tue Jan 31 2023 Jan Grulich <jgrulich@redhat.com> - 6.4.2-3
- migrated to SPDX license

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 6.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Jan 16 2023 Jan Grulich <jgrulich@redhat.com> - 6.4.2-1
- 6.4.2

* Wed Nov 23 2022 Jan Grulich <jgrulich@redhat.com> - 6.4.1-1
- 6.4.1

* Mon Oct 31 2022 Jan Grulich <jgrulich@redhat.com> - 6.4.0-1
- 6.4.0

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 6.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jul 13 2022 Jan Grulich <jgrulich@redhat.com> - 6.3.1-1
- 6.3.1

* Wed Apr 13 2022 Jan Grulich <jgrulich@redhat.com> - 6.3.0-1
- 6.3.0

* Mon Jan 31 2022 Jan Grulich <jgrulich@redhat.com> - 6.2.3-1
- 6.2.3

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 6.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Dec 14 2021 Jan Grulich <jgrulich@redhat.com> - 6.2.2-1
- 6.2.2

* Fri Oct 29 2021 Jan Grulich <jgrulich@redhat.com> - 6.2.1-1
- 6.2.1

* Fri Oct 29 2021 Jan Grulich <jgrulich@redhat.com> - 6.2.0-2
- 6.2.1

* Thu Sep 30 2021 Jan Grulich <jgrulich@redhat.com> - 6.2.0-1
- 6.2.0

* Mon Sep 27 2021 Jan Grulich <jgrulich@redhat.com> - 6.2.0~rc2-1
- 6.2.0 - rc2

* Tue Sep 21 2021 Jan Grulich <jgrulich@redhat.com> - 6.2.0~rc-2
- Drop qt6-qtquickcontrols2 from required packages

* Sat Sep 18 2021 Jan Grulich <jgrulich@redhat.com> - 6.2.0~rc-1
- 6.2.0 - rc

* Mon Sep 13 2021 Jan Grulich <jgrulich@redhat.com> - 6.2.0~beta4-3
- Drop qt6_exclude_arch macro

* Mon Sep 13 2021 Jan Grulich <jgrulich@redhat.com> - 6.2.0~beta4-2
- Add qt6_exclude_arch macro

* Fri Sep 10 2021 Jan Grulich <jgrulich@redhat.com> - 6.2.0~beta4-1
- 6.2.0 - beta4

* Mon Aug 30 2021 Jan Grulich <jgrulich@redhat.com> - 6.2.0~beta3-1
- 6.2.0 - beta3

* Thu Aug 12 2021 Jan Grulich <jgrulich@redhat.com> - 6.1.2-1
- 6.1.2

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 6.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Jun 07 2021 Jan Grulich <jgrulich@redhat.com> - 6.1.1-1
- 6.1.1

* Mon May 24 2021 Jan Grulich <jgrulich@redhat.com> - 6.1.0-2
- Fix path to libexecdir

* Thu May 06 2021 Jan Grulich <jgrulich@redhat.com> - 6.1.0-1
- 6.1.0

* Mon Apr 05 2021 Jan Grulich <jgrulich@redhat.com> - 6.0.3-1
- 6.0.3

* Thu Feb 04 2021 Jan Grulich <jgrulich@redhat.com> - 6.0.1-1
- 6.0.1

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jan 06 2021 Jan Grulich <jgrulich@redhat.com> - 6.0.0-1
- 6.0.0
