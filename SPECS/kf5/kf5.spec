Name:         kf5
Version:      5.109.0
Release:      1%{?dist}
Summary:      Filesystem and RPM macros for KDE Frameworks 5
License:      BSD
URL:          http://www.kde.org
Vendor:       Microsoft Corporation
Distribution: Mariner

Source0: macros.kf5

Requires: %{name}-filesystem
Requires: %{name}-rpm-macros

%description
Filesystem and RPM macros for KDE Frameworks 5

%package filesystem
Summary: Filesystem for KDE Frameworks 5
# noarch -> arch transition
Obsoletes: kf5-filesystem < 5.10.0-2
%{?_qt5_version:Requires: qt5-qtbase%{?_isa} >= %{_qt5_version}}
%description filesystem
Filesystem for KDE Frameworks 5.

%package rpm-macros
Summary: RPM macros for KDE Frameworks 5
Requires: cmake
Requires: qt5-qtbase-devel >= 5.11
# misc build environment dependencies
Requires: gcc-c++
BuildArch: noarch
%description rpm-macros
RPM macros for building KDE Frameworks 5 packages.

%install
# See macros.kf5 where the directories are specified
mkdir -p %{buildroot}%{_prefix}/{lib,%{_lib}}/qt5/plugins/kf5/
mkdir -p %{buildroot}%{_prefix}/{lib,%{_lib}}/kconf_update_bin
mkdir -p %{buildroot}%{_includedir}/KF5
mkdir -p %{buildroot}%{_datadir}/{config.kcfg,kconf_update,kf5,kservicetypes5}
mkdir -p %{buildroot}%{_datadir}/kpackage/{genericqml,kcms}
mkdir -p %{buildroot}%{_datadir}/kservices5/ServiceMenus
mkdir -p %{buildroot}%{_datadir}/qlogging-categories5/
mkdir -p %{buildroot}%{_datadir}/solid/{actions,devices}
mkdir -p %{buildroot}%{_docdir}/qt5/
mkdir -p %{buildroot}%{_libexecdir}/kf5
mkdir -p %{buildroot}%{_sysconfdir}/xdg/plasma-workspace/{env,shutdown}

install -Dpm644 %{SOURCE0} %{buildroot}%{_rpmconfigdir}/macros.d/macros.kf5
sed -i \
  -e "s|@@KF5_VERSION@@|%{version}|g" \
  %{buildroot}%{_rpmconfigdir}/macros.d/macros.kf5

%files

%files filesystem
%{_sysconfdir}/xdg/plasma-workspace/
%{_prefix}/lib/qt5/plugins/kf5/
%{_prefix}/%{_lib}/qt5/plugins/kf5/
%{_prefix}/lib/kconf_update_bin/
%{_prefix}/%{_lib}/kconf_update_bin/
%{_includedir}/KF5/
%{_libexecdir}/kf5/
%{_datadir}/config.kcfg/
%{_datadir}/kconf_update/
%{_datadir}/kf5/
%{_datadir}/kpackage/
%{_datadir}/kservices5/
%{_datadir}/kservicetypes5/
%{_datadir}/knsrcfiles/
%{_datadir}/qlogging-categories5/
%{_datadir}/solid/
%{_docdir}/qt5/

%files rpm-macros
%{_rpmconfigdir}/macros.d/macros.kf5


%changelog
* Tue January 30 2024 Saul Paredes <saulparedes@microsoft.com> - 5.61.0-5
- Upgrade to 5.109.0

* Fri May 26 2023 Thien Trung Vuong <tvuong@microsoft.com> - 5.61.0-5
- License verified.

* Tue Mar 31 2020 Joe Schmitt <joschmit@microsoft.com> - 5.61.0-4
- Generate kf5 package

* Mon Mar 30 2020 Joe Schmitt <joschmit@microsoft.com> - 5.61.0-3
- Update Vendor and Distribution tags

* Mon Mar 30 2020 Mateusz Malisz <mamalisz@microsoft.com> - 5.61.0-2
- Initial CBL-Mariner import from Fedora 31 (license: MIT).

* Wed Aug 07 2019 Rex Dieter <rdieter@fedoraproject.org> - 5.61.0-1
- 5.61.0

* Mon Jul 29 2019 Rex Dieter <rdieter@fedoraproject.org> - 5.60.0-3
- -filesystem: ++%{_kf5_datadir}/qlogging-categories5/

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5.60.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Jul 13 2019 Rex Dieter <rdieter@fedoraproject.org> - 5.60.0-1
- 5.60.0
- BR: qt5 >= 5.11

* Thu Jun 06 2019 Rex Dieter <rdieter@fedoraproject.org> - 5.59.0-1
- 5.59.0

* Thu May 23 2019 Rex Dieter <rdieter@fedoraproject.org> - 5.58.0-2
- -rpm-macros: enforce min qt5 dep (5.10)

* Tue May 07 2019 Rex Dieter <rdieter@fedoraproject.org> - 5.58.0-1
- 5.58.0

* Mon Apr 08 2019 Rex Dieter <rdieter@fedoraproject.org> - 5.57.0-1
- 5.57.0

* Tue Mar 05 2019 Rex Dieter <rdieter@fedoraproject.org> - 5.56.0-1
- 5.56.0

* Mon Feb 04 2019 Rex Dieter <rdieter@fedoraproject.org> - 5.55.0-1
- 5.55.0

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5.54.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Jan 09 2019 Rex Dieter <rdieter@fedoraproject.org> -  5.54.0-1
- 5.54.0

* Sun Dec 09 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.53.0-1
- 5.53.0

* Sun Nov 04 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.52.0-1
- 5.52.0

* Wed Oct 10 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.51.0-1
- 5.51.0

* Tue Sep 04 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.50.0-1
- 5.50
- .spec cosmetics
- macros.kf5: use %%_metainfodir explicitly

* Tue Aug 07 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.49.0-1
- 5.49.0

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5.48.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jul 09 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.48.0-2
- fix %%kf5_qmldir definition (since %%_qt5_prefix change in rawhide)

* Sun Jul 08 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.48.0-1
- 5.48.0

* Sat Jun 02 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.47.0-1
- 5.47.0

* Sat May 05 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.46.0-1
- 5.46.0

* Sun Apr 08 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.45.0-1
- 5.45.0

* Sat Mar 03 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.44.0-1
- 5.44.0

* Wed Feb 07 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.43.0-1
- 5.43.0

* Mon Jan 22 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.42.0-5
- own /usr/share/kpackage/{genericqml,kcms} (#1536892)

* Tue Jan 16 2018 Karsten Hopp <karsten@redhat.com> - 5.42.0-4
- fix conditional

* Tue Jan 16 2018 Karsten Hopp <karsten@redhat.com> - 5.42.0-3
- fix cmake3 macro name

* Wed Jan 10 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.42.0-2
- kf5-rpm-macros: fix %%_kf5_metainfodir macro for < f28 (#1532930)

* Mon Jan 08 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.42.0-1
- 5.42.0

* Wed Jan 03 2018 Rex Dieter <rdieter@fedoraproject.org> 5.41.0-2
- own /usr/share/config.kcfg (shared with kde-filesystem)

* Mon Dec 04 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.41.0-1
- 5.41.0

* Wed Nov 15 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.40.0-2
- %%_kf5_metainfodir => %%_kf5_datadir/metainfo

* Fri Nov 10 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.40.0-1
- 5.40.0

* Thu Nov 09 2017 Troy Dawson <tdawson@redhat.com> - 5.39.0-2
- Cleanup conditionals

* Sun Oct 08 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.39.0-1
- 5.39.0

* Mon Sep 11 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.38.0-1
- 5.38

* Fri Aug 25 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.37.0-1
- 5.37

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.36.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.36.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jul 03 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.36.0-1
- 5.36.0

* Sun Jun 04 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.35.0-1
- 5.35.0

* Mon May 15 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.34.0-1
- 5.34.0

* Mon Apr 03 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.33.0-1
- 5.33.0

* Sat Mar 04 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.32.0-1
- 5.32.0

* Thu Mar 02 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.31.0-2
- kf5-rpm-macros: Requires: qt5-rpm-macros gcc-c++

* Mon Feb 06 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.31.0-1
- 5.31.0

* Fri Dec 16 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.29.0-1
- 5.29.0

* Mon Oct 03 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.27.0-1
- 5.27.0

* Wed Sep 07 2016 Daniel Vrátil <dvratil@fedoraproject.org> - 5.26.0-1
- KDE Frameworks 5.26.0

* Mon Aug 08 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.25.0-2
- introduce %%_kf5_metainfodir => %%_kf5_datadir/appdata, set KDE_INSTALL_METAINFODIR accordingly

* Sun Aug 07 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.25.0-1
- 5.25.0

* Wed Jul 06 2016 Daniel Vrátil <dvratil@fedoraproject.org> - 5.24.0-1
- KDE Frameworks 5.24.0

* Tue Jun 07 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.23.0-1
- 5.23.0

* Thu Jun 02 2016 Than Ngo <than@redhat.com> - 5.22.0-5
- drop -O3 from default release build type flags

* Sun May 15 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.22.0-4
- rpm-macros: revert KDE_INSTALL_INCLUDEDIR change, set CMAKE_INSTALL_INCLUDEDIR_KF5 instead

* Sat May 14 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.22.0-3
- rpm-macros: fix archdatadir, MKSPECS_INSTALL_DIR

* Sat May 14 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.22.0-2
- rpm-macros: fix KDE_INSTALL_INCLUDEDIR

* Mon May 09 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.22.0-1
- KDE Frameworks 5.22.0
- rpm-macros: update to use -DKDE_INSTALL_... style definitions

* Mon Apr 04 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.21.0-1
- KDE Frameworks 5.21.0

* Mon Mar 14 2016 Daniel Vrátil <dvratil@fedoraproject.org> - 5.20.0-1
- KDE Frameworks 5.20.0

* Thu Feb 11 2016 Daniel Vrátil <dvratil@fedoraproject.org> - 5.19.0-1
- KDE Frameworks 5.19.0

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 5.18.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jan 14 2016 Rex Dieter <rdieter@fedoraproject.org> 5.18.0-4
- -rpm-macros: Requires: qt5-qtbase-devel

* Thu Jan 14 2016 Rex Dieter <rdieter@fedoraproject.org> 5.18.0-3
- -rpm-macros: add cmake deps as needed

* Fri Jan 08 2016 Rex Dieter <rdieter@fedoraproject.org> 5.18.0-2
- +kconf_update_bin, omit dup'd %%changelog entry

* Sun Jan 03 2016 Daniel Vrátil <dvratil@fedoraproject.org> - 5.18.0-1
- KDE Frameworks 5.18.0

* Sun Dec 13 2015 Helio Chissini de Castro <helio@kde.org> - 5.17.0-2
- Prepare to cmake3 epel

* Tue Dec 08 2015 Daniel Vrátil <dvratil@fedoraproject.org> - 5.17.0-1
- KDE Frameworks 5.17.0

* Wed Nov 18 2015 Rex Dieter <rdieter@fedoraproject.org> - 5.16.0-3
- kf5-filesystem: add versioned qt5-qtbase dep

* Mon Nov 16 2015 Rex Dieter <rdieter@fedoraproject.org> 5.16.0-2
- +%%{_datadir}/{kservices5{,/ServiceMenus},kservicetypes5,solid{,/actions,/devices}}

* Sun Nov 08 2015 Daniel Vrátil <dvratil@fedoraproject.org> - 5.16.0-1
- KDE Frameworks 5.16.0

* Thu Oct 08 2015 Daniel Vrátil <dvratil@redhat.com> - 5.15.0-1
- KDE Frameworks 5.15.0

* Wed Sep 16 2015 Daniel Vrátil <dvratil@redhat.com> - 5.14.0-1
- KDE Frameworks 5.14.0

* Wed Aug 19 2015 Daniel Vrátil <dvratil@redhat.com> - 5.13.0-1
- KDE Frameworks 5.13.0

* Wed Aug 19 2015 Rex Dieter <rdieter@fedoraproject.org> 5.13.0-0.2
- macros.kf5: add %%_kf5_version

* Tue Aug 11 2015 Daniel Vrátil <dvratil@redhat.com> - 5.13.0-0.1
- KDE Frameworks 5.13

* Fri Jul 17 2015 Daniel Vrátil <dvratil@redhat.com> - 5.12.0
- KDE Frameworks 5.12.0

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.11.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 10 2015 Rex Dieter <rdieter@fedoraproject.org> 5.11.0-2
- own %%_datadir/kconf_update

* Wed Jun 10 2015 Daniel Vrátil <dvratil@redhat.com> - 5.11.0-1
- KDE Frameworks 5.11.0

* Wed Jun 03 2015 Rex Dieter <rdieter@fedoraproject.org> 5.10.0-2
- own %%{_datadir}/kf5, make -filesystem arch'd

* Mon May 11 2015 Daniel Vrátil <dvratil@redhat.com> - 5.10.0-1
- KDE Frameworks 5.10.0

* Tue Apr 07 2015 Daniel Vrátil <dvratil@redhat.com> - 5.9.0-1
- KDE Frameworks 5.9.0

* Mon Mar 16 2015 Daniel Vrátil <dvratil@redhat.com> - 5.8.0-1
- KDE Frameworks 5.8.0

* Tue Feb 10 2015 Daniel Vrátil <dvratil@redhat.com> - 5.7.0-2
- add %%find_lang_kf5 macro to macros.kf5 to workaround %%find_lang bugs

* Mon Feb 09 2015 Daniel Vrátil <dvratil@redhat.com> - 5.7.0-1
- KDE Frameworks 5.7.0

* Fri Jan 30 2015 Rex Dieter <rdieter@fedoraproject.org> 5.6.0-2
- own /etc/xdg/plasma-workspace/, /etc/xdg/plasma-workspace/{env,shutdown}

* Tue Jan 06 2015 Daniel Vrátil <dvratil@redhat.com> - 5.6.0-1
- KDE Frameworks 5.6.0

* Sat Dec 06 2014 Daniel Vrátil <dvratil@redhat.com> - 5.5.0-1
- KDE Frameworks 5.5.0

* Mon Nov 24 2014 Rex Dieter <rdieter@fedoraproject.org> 5.4.0-2
- macros.kf5: PATH, prepend %%_qt5_bindir instead of %%_kf5_bindir (ie, /usr/bin)

* Mon Nov 03 2014 Daniel Vrátil <dvratil@redhat.com> - 5.3.0-1
- KDE Frameworks 5.4.0

* Tue Oct 14 2014 Rex Dieter <rdieter@fedoraproject.org> 5.3.0-2
- macros.kf5: -DCMAKE_USE_RELATIVE_PATHS:BOOL=ON

* Wed Oct 08 2014 Daniel Vrátil <dvratil@redhat.com> - 5.3.0-1
- KDE Frameworks 5.3.0

* Mon Sep 15 2014 Daniel Vrátil <dvratil@redhat.com> - 5.2.0-1
- KDE Frameworks 5.2.0

* Wed Sep 03 2014 Rex Dieter <rdieter@fedoraproject.org> 5.1.0-3
- %%cmake_kf5: add -DKDE_INSTALL_USE_QT_SYS_PATHS=ON

* Thu Aug 21 2014 Daniel Vrátil <dvratil@redhat.com> - 5.1.0-2
- Add new KF5-specific variables to our CMake command

* Wed Aug 06 2014 Daniel Vrátil <dvratil@redhat.com> - 5.1.0-1
- KDE Frameworks 5.1.0

* Sat Jul 19 2014 Rex Dieter <rdieter@fedoraproject.org> 5.0.0-2
- Release: +%%{?dist}

* Wed Jul 09 2014 Daniel Vrátil <dvratil@redhat.com> - 5.0.0-1
- KDE Frameworks 5.0.0

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.99.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Jun 04 2014 Daniel Vrátil <dvratil@redhat.com> 4.99.0-6
- Remove kf5 suffix from -DPLUGIN_INSTALL_DIR as packages now specify that on their own

* Wed Jun 04 2014 Daniel Vrátil <dvratil@redhat.com> 4.99.0-5
- Point -DLIBEXEC_INSTALL_DIR to %%{_libexecdir} to fix duplicated path

* Wed May 14 2014 Daniel Vrátil <dvratil@redhat.com> 4.99.0-4
- Make LIB_INSTALL_DIR relative, otherwise /usr/usr/lib64/... is generated by CMake

* Tue May 06 2014 Daniel Vrátil <dvratil@redhat.com> 4.99.0-3
- Define KF5_INCLUDE_INSTALL_DIR

* Mon May 05 2014 Daniel Vrátil <dvratil@redhat.com> 4.99.0-2
- Define KF5_LIBEXEC_INSTALL_DIR

* Mon May 05 2014 Daniel Vrátil <dvratil@redhat.com> 4.99.0-1
- KDE Frameworks 4.99.0

* Mon Apr 28 2014 Daniel Vrátil <dvratil@redhat.com> 4.98.0-8
- Remove INCLUDE_INSTALL_DIR, since we use the default one

* Tue Apr 22 2014 Daniel Vrátil <dvratil@redhat.com> 4.98.0-7
- Make DATA_INSTALL_DIR relative, so that CMake config files don't point to /usr/usr/share

* Tue Apr 22 2014 Daniel Vrátil <dvratil@redhat.com> 4.98.0-6
- Explicitly set BIN_INSTALL_DIR to be absolute, otherwise CMake complains

* Mon Apr 21 2014 Daniel Vrátil <dvratil@redhat.com> 4.98.0-5
- Fix _kf5_sysconfdir and set some install paths in cmake_kf5

* Wed Apr 16 2014 Daniel Vrátil <dvratil@redhat.com> 4.98.0-4
- Rename base package to kf5
- Create -filesystem, -rpm-macros subpackges

* Fri Apr 11 2014 Daniel Vrátil <dvratil@redhat.com> 4.98.0-3
- Fix build
- Use %%global instead of %%define
- Use install instead of cp

* Fri Apr 11 2014 Daniel Vrátil <dvratil@redhat.com> 4.98.0-2
- Fix some installation dirs in the macros.kf5 file

* Mon Mar 31 2014 Jan Grulich <jgrulich@redhat.com> 4.98.0-1
- Update to KDE Frameworks 5 Beta 1 (4.98.0)

* Wed Mar 05 2014 Jan Grulich <jgrulich@redhat.com> 4.97.0-1
- Update to KDE Frameworks 5 Alpha 2 (4.97.0)

* Thu Feb 13 2014 Daniel Vrátil <dvraitl@redhat.com> 4.96.0-2
- Remove unnecessary mkdirs

* Wed Feb 12 2014 Daniel Vrátil <dvratil@redhat.com> 4.96.0-1
- Update to KDE Frameworks 5 Alpha 1 (4.96.0)

* Wed Feb 05 2014 Daniel Vrátil <dvratil@redhat.com> 4.96.0-0.1.20140205git
- Update to pre-release snapshot of 4.96.0

* Thu Jan 16 2014 Daniel Vrátil <dvratil@redhat.com> 4.95.0-4
- fix definition of QT_PLUGIN_INSTALL_DIR in RPM macros

* Thu Jan 16 2014 Daniel Vrátil <dvratil@redhat.com> 4.95.0-2
- fix install dirs definitions in RPM macros

* Thu Jan 09 2014 Daniel Vrátil <dvratil@redhat.com> 4.95.0-1
- Update to KDE Frameworks 5 TP1 (4.95.0)

* Tue Jan  7 2014 Daniel Vrátil <dvratil@redhat.com>
- export XDG_DATA_DIRS

* Mon Jan  6 2014 Daniel Vrátil <dvratil@redhat.com>
- alter XDG_DATA_DIRS in cmake_kf5 RPM macro
- add _kf5_mandir RPM macro

* Sat Jan  4 2014 Daniel Vrátil <dvratil@redhat.com>
- initial version
