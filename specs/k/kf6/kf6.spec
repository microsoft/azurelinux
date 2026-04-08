# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global debug_package %{nil}

Name:    kf6
# This version MUST remain in sync with KF6 versions!
Version: 6.23.0
Release: 1%{?dist}
Summary: Filesystem and RPM macros for KDE Frameworks 6
License: BSD-3-Clause
URL:     http://www.kde.org
Source0: macros.kf6
Source1: LICENSE

%description
Filesystem and RPM macros for KDE Frameworks 6

%package filesystem
Summary: Filesystem for KDE Frameworks 6
%if 0%{?fedora} >= 40 || 0%{?rhel} >= 10
Requires: kde-filesystem >= 5
%endif
%{?_qt6_version:Requires: qt6-qtbase >= %{_qt6_version}}
%description filesystem
Filesystem for KDE Frameworks 6.

%package rpm-macros
Summary: RPM macros for KDE Frameworks 6
Requires: cmake >= 3
Requires: qt6-rpm-macros >= 6
# misc build environment dependencies
Requires: gcc-c++
# for docs generation
Requires: doxygen
Requires: qt6-doc-devel
Requires: kde-qdoc-common
Requires: cmake(Qt6ToolsTools)
BuildArch: noarch
%description rpm-macros
RPM macros for building KDE Frameworks 6 packages.

%install
# See macros.kf6 where the directories are specified
mkdir -p %{buildroot}%{_prefix}/{lib,%{_lib}}/qt6/plugins/kf6/
mkdir -p %{buildroot}%{_prefix}/{lib,%{_lib}}/qt6/qml/org/kde/
mkdir -p %{buildroot}%{_includedir}/kf6
mkdir -p %{buildroot}%{_includedir}/KF6
mkdir -p %{buildroot}%{_datadir}/{kf6,kservices6,kservicetypes6}
mkdir -p %{buildroot}%{_datadir}/kio/servicemenus
mkdir -p %{buildroot}%{_datadir}/qlogging-categories6/
mkdir -p %{buildroot}%{_docdir}/qt6
mkdir -p %{buildroot}%{_libexecdir}/kf6
mkdir -p %{buildroot}%{_datadir}/kf6/
mkdir -p %{buildroot}%{_datadir}/locale/tok
%if ! (0%{?fedora} >= 40 || 0%{?rhel} >= 10)
mkdir -p %{buildroot}%{_prefix}/{lib,%{_lib}}/kconf_update_bin
mkdir -p %{buildroot}%{_datadir}/{config.kcfg,kconf_update}
mkdir -p %{buildroot}%{_datadir}/kpackage/{genericqml,kcms}
mkdir -p %{buildroot}%{_datadir}/knsrcfiles/
mkdir -p %{buildroot}%{_datadir}/solid/{actions,devices}
mkdir -p %{buildroot}%{_sysconfdir}/xdg/plasma-workspace/{env,shutdown}
%endif

install -Dpm644 %{_sourcedir}/macros.kf6 %{buildroot}%{_rpmconfigdir}/macros.d/macros.kf6
install -Dpm644 %{_sourcedir}/LICENSE %{buildroot}%{_datadir}/kf6/LICENSE
sed -i \
  -e "s|@@kf6_VERSION@@|%{version}|g" \
  %{buildroot}%{_rpmconfigdir}/macros.d/macros.kf6

%files filesystem
%{_datadir}/kf6/
%{_datadir}/kio/
%{_datadir}/kservices6/
%{_datadir}/kservicetypes6/
%{_datadir}/qlogging-categories6/
%{_docdir}/qt6/
%{_includedir}/kf6/
%{_includedir}/KF6/
%{_libexecdir}/kf6/
%{_prefix}/%{_lib}/qt6/plugins/kf6/
%{_prefix}/lib/qt6/plugins/kf6/
%{_prefix}/%{_lib}/qt6/qml/org/kde/
%{_prefix}/lib/qt6/qml/org/kde/
%{_datadir}/locale/tok
%if ! (0%{?fedora} >= 40 || 0%{?rhel} >= 10)
%{_datadir}/config.kcfg/
%{_datadir}/kconf_update/
%{_datadir}/knsrcfiles/
%{_datadir}/kpackage/
%{_datadir}/solid/
%{_prefix}/%{_lib}/kconf_update_bin/
%{_prefix}/lib/kconf_update_bin/
%{_sysconfdir}/xdg/plasma-workspace/
%endif

%files rpm-macros
%{_rpmconfigdir}/macros.d/macros.kf6

%changelog
* Thu Feb 12 2026 Steve Cossette <farchord@gmail.com> - 6.23.0-1
- 6.23.0

* Fri Jan 16 2026 Fedora Release Engineering <releng@fedoraproject.org> - 6.22.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Fri Jan 02 2026 farchord@gmail.com - 6.22.0-1
- 6.22.0

* Fri Dec 05 2025 Steve Cossette <farchord@gmail.com> - 6.21.0-1
- 6.21.0

* Thu Nov 13 2025 Steve Cossette <farchord@gmail.com> - 6.20.0-1
- 6.20.0

* Sun Oct 05 2025 Steve Cossette <farchord@gmail.com> - 6.19.0-1
- 6.19.0

* Tue Sep 16 2025 Steve Cossette <farchord@gmail.com> - 6.18.0-1
- 6.18.0

* Fri Aug 01 2025 Steve Cossette <farchord@gmail.com> - 6.17.0-1
- 6.17.0

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 6.16.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sun Jul 06 2025 Yaakov Selkowitz <yselkowi@redhat.com> - 6.16.0-2
- Fix api doc generation for flatpak builds

* Sat Jul 05 2025 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 6.16.0-1
- 6.16.0

* Tue Jun 17 2025 Steve Cossette <farchord@gmail.com> - 6.15.0-2
- Bump for 'add new kf6 macros for api doc generation' MR (#12)

* Sat May 03 2025 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 6.14.0-1
- 6.14.0

* Sun Apr 06 2025 Steve Cossette <farchord@gmail.com> - 6.13.0-1
- 6.13.0

* Fri Mar 07 2025 Steve Cossette <farchord@gmail.com> - 6.12.0-1
- 6.12.0

* Fri Feb 07 2025 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 6.11.0-1
- 6.11.0

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 6.10.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jan 03 2025 Steve Cossette <farchord@gmail.com> - 6.10.0-1
- 6.10.0

* Sat Dec 14 2024 Steve Cossette <farchord@gmail.com> - 6.9.0-1
- 6.9.0

* Sat Nov 02 2024 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 6.8.0-1
- 6.8.0

* Fri Oct 04 2024 Steve Cossette <farchord@gmail.com> - 6.7.0-1
- 6.7.0

* Mon Sep 16 2024 Steve Cossette <farchord@gmail.com> - 6.6.0-1
- 6.6.0

* Mon Sep 02 2024 Yaakov Selkowitz <yselkowi@redhat.com> - 6.5.0-2
- Make %%stable_kf6 and %%maj_min_kf6 usable for other components

* Sat Aug 10 2024 Steve Cossette <farchord@gmail.com> - 6.5.0-1
- 6.5.0

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Jul 06 2024 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 6.4.0-1
- 6.4.0

* Sat Jun 01 2024 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 6.3.0-1
- 6.3.0

* Sat May 04 2024 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 6.2.0-1
- 6.2.0

* Wed Apr 10 2024 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 6.1.0-1
- 6.1.0

* Fri Apr 05 2024 Yaakov Selkowitz <yselkowi@redhat.com> - 6.0.0-3
- Define KDE_INSTALL_QTQCHDIR in %%cmake_kf6

* Thu Mar 7 2024 Marie Loise Nolden <loise@kde.org> - 6.0.0-2
- fix missing Qt6ToolsTools which are required for automatic qch building

* Wed Feb 21 2024 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 6.0.0-1
- 6.0.0

* Wed Jan 31 2024 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 5.249.0-1
- 5.249.0

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.248.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.248.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jan 10 2024 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 5.248.0-1
- 5.248.0

* Mon Jan 08 2024 Neal Gompa <ngompa@fedoraproject.org> - 5.247.0-2
- Add -DBUILD_QCH:BOOL=ON for qch file generation by default

* Wed Dec 20 2023 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 5.247.0-1
- 5.247.0

* Sat Dec 02 2023 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 5.246.0-1
- 5.246.0

* Fri Nov 24 2023 Yaakov Selkowitz <yselkowi@redhat.com> - 5.245.0-2
- Update servicemenus path

* Fri Nov 10 2023 Alessandro Astone <ales.astone@gmail.com> - 5.245.0-1
- 5.245.0
- Fix macros for unstable releases

* Sun Nov 05 2023 Steve Cossette <farchord@gmail.com> - 5.240.0-4
- Migrated/copied framework version macros from the kf5 package

* Sun Oct 08 2023 Steve Cossette <farchord@gmail.com> - 5.240.0-3
- Added ownership of the Toki Pona locale to kf6-filesystem

* Thu Sep 21 2023 Neal Gompa <ngompa@fedoraproject.org> - 5.240.0-2
- Add KDE QML paths to -filesystem subpackage (#2239699)

* Sat Sep 16 2023 Neal Gompa <ngompa@fedoraproject.org> - 5.240.0-1
- Set version matching extra-cmake-modules base version

* Fri Sep 15 2023 Neal Gompa <ngompa@fedoraproject.org> - 0.0-1
- Version reset in preparation for kf6 initial release

* Thu Sep 14 2023 Yaakov Selkowitz <yselkowi@redhat.com> - 7-2
- Use kde-filesystem for unversioned directories in F40+

* Fri Sep 8 2023 Justin Zobel <justin@1707.io> 7-1
- Create and own /usr/include/KF6

* Thu Mar 2 2023 Justin Zobel <justin@1707.io> 6-1
- Initial Version

