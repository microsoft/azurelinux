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

%global glib2_version 2.80.0

%global tarball_version %%(echo %{version} | tr '~' '.')

Name:           sysprof
Version:        49.0
Release:        %autorelease
Summary:        A system-wide Linux profiler

License:        GPL-2.0-or-later AND GPL-3.0-or-later AND CC-BY-SA-4.0 AND CC0-1.0 AND BSD-2-Clause-Patent
URL:            http://www.sysprof.com
Source0:        https://download.gnome.org/sources/sysprof/49/sysprof-%{tarball_version}.tar.xz

BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  gettext
BuildRequires:  itstool
BuildRequires:  meson
BuildRequires:  pkgconfig(gio-2.0) >= %{glib2_version}
BuildRequires:  pkgconfig(gio-unix-2.0) >= %{glib2_version}
BuildRequires:  pkgconfig(glib-2.0) >= %{glib2_version}
BuildRequires:  pkgconfig(gobject-2.0)
BuildRequires:  pkgconfig(gtk4)
BuildRequires:  pkgconfig(json-glib-1.0)
BuildRequires:  pkgconfig(libadwaita-1)
BuildRequires:  pkgconfig(libdebuginfod)
BuildRequires:  pkgconfig(libdex-1)
BuildRequires:  pkgconfig(libdw)
BuildRequires:  pkgconfig(libpanel-1)
BuildRequires:  pkgconfig(libsystemd)
BuildRequires:  pkgconfig(libunwind-generic)
BuildRequires:  pkgconfig(polkit-gobject-1)
BuildRequires:  pkgconfig(systemd)
BuildRequires:  /usr/bin/appstream-util
BuildRequires:  /usr/bin/desktop-file-validate

Requires:       glib2%{?_isa} >= %{glib2_version}
Requires:       hicolor-icon-theme
Requires:       %{name}-cli%{?_isa} = %{version}-%{release}

%description
Sysprof is a sampling CPU profiler for Linux that collects accurate,
high-precision data and provides efficient access to the sampled
calltrees.


%package        agent
Summary:        Sysprof agent utility

%description    agent
The %{name}-agent package contains the sysprof-agent program. It provides a P2P
D-Bus API to the process which can control subprocesses. It's used by IDE
tooling to have more control across container boundaries.


%package        cli
Summary:        Sysprof command line utility
# sysprofd needs turbostat
Requires:       kernel-tools
Requires:       libsysprof%{?_isa} = %{version}-%{release}

%description    cli
The %{name}-cli package contains the sysprof-cli command line utility.


%package     -n libsysprof
Summary:        Sysprof libraries
# Subpackage removed/obsoleted in F39
Obsoletes:      libsysprof-ui < 45.0

%description -n libsysprof
The libsysprof package contains the Sysprof libraries.


%package        capture-devel
Summary:        Development files for sysprof-capture static library
License:        BSD-2-Clause-Patent
Provides:       sysprof-capture-static = %{version}-%{release}

%description    capture-devel
The %{name}-capture-devel package contains the sysprof-capture static library and header files.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}-capture-devel%{?_isa} = %{version}-%{release}
Requires:       libsysprof%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%autosetup -p1 -n sysprof-%{tarball_version}


%build
%meson
%meson_build


%install
%meson_install
%find_lang %{name} --with-gnome


%check
appstream-util validate-relax --nonet %{buildroot}%{_datadir}/metainfo/*.metainfo.xml
desktop-file-validate %{buildroot}%{_datadir}/applications/*.desktop


%files
%license COPYING
%doc NEWS README.md AUTHORS
%{_bindir}/sysprof
%{_datadir}/applications/org.gnome.Sysprof.desktop
%{_datadir}/dbus-1/services/org.gnome.Sysprof.service
%{_datadir}/icons/hicolor/*/*/*
%{_metainfodir}/org.gnome.Sysprof.metainfo.xml
%{_datadir}/mime/packages/sysprof-mime.xml

%files agent
%license COPYING
%{_bindir}/sysprof-agent

%files cli -f %{name}.lang
%license COPYING
%{_bindir}/sysprof-cli
%{_bindir}/sysprof-cat
%{_libexecdir}/sysprofd
%{_libexecdir}/sysprof-live-unwinder
%{_datadir}/dbus-1/system.d/org.gnome.Sysprof3.conf
%{_datadir}/dbus-1/system-services/org.gnome.Sysprof3.service
%{_datadir}/polkit-1/actions/org.gnome.sysprof3.policy
%{_unitdir}/sysprof3.service

%files -n libsysprof
%license COPYING COPYING.gpl-2
%{_libdir}/libsysprof-6.so.6*
%{_libdir}/libsysprof-memory-6.so
%{_libdir}/libsysprof-speedtrack-6.so
%{_libdir}/libsysprof-tracer-6.so

%files capture-devel
%license src/libsysprof-capture/COPYING
%dir %{_includedir}/sysprof-6
%{_includedir}/sysprof-6/sysprof-address.h
%{_includedir}/sysprof-6/sysprof-capture-condition.h
%{_includedir}/sysprof-6/sysprof-capture-cursor.h
%{_includedir}/sysprof-6/sysprof-capture.h
%{_includedir}/sysprof-6/sysprof-capture-reader.h
%{_includedir}/sysprof-6/sysprof-capture-types.h
%{_includedir}/sysprof-6/sysprof-capture-writer.h
%{_includedir}/sysprof-6/sysprof-clock.h
%{_includedir}/sysprof-6/sysprof-collector.h
%{_includedir}/sysprof-6/sysprof-macros.h
%{_includedir}/sysprof-6/sysprof-platform.h
%{_includedir}/sysprof-6/sysprof-version.h
%{_includedir}/sysprof-6/sysprof-version-macros.h
%{_libdir}/libsysprof-capture-4.a
%{_libdir}/pkgconfig/sysprof-capture-4.pc

%files devel
%{_includedir}/sysprof-6/
%{_libdir}/libsysprof-6.so
%{_libdir}/pkgconfig/sysprof-6.pc
%{_datadir}/dbus-1/interfaces/org.gnome.Sysprof.Agent.xml
%{_datadir}/dbus-1/interfaces/org.gnome.Sysprof3.Profiler.xml
%{_datadir}/dbus-1/interfaces/org.gnome.Sysprof3.Service.xml


%changelog
## START: Generated by rpmautospec
* Thu Apr 30 2026 Daniel McIlvaney <damcilva@microsoft.com> - 49.0-2
- test: add initial lock files

* Mon Sep 15 2025 Michael Catanzaro <mcatanzaro@redhat.com> - 49.0-1
- Update to 49.0

* Fri Sep 05 2025 Michael Catanzaro <mcatanzaro@redhat.com> - 49~rc-1
- Update to 49.rc

* Fri Aug 29 2025 Michael Catanzaro <mcatanzaro@redhat.com> - 49~alpha-3
- Fix changelog and use %%autorelease

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 49~alpha-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jun 30 2025 Milan Crha <mcrha@redhat.com> - 49~alpha-1
- Update to 49.alpha

* Mon Mar 17 2025 nmontero <nmontero@redhat.com> - 48.0-1
- Update to 48.0

* Tue Mar 11 2025 nmontero <nmontero@redhat.com> - 48~rc-1
- Update to 48~rc

* Thu Mar 06 2025 Fabio Valentini <decathorpe@gmail.com> - 48~beta-1
- Update to 48.beta

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 47.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Dec 02 2024 nmontero <nmontero@redhat.com> - 47.2-1
- Update to 47.2

* Tue Nov 05 2024 nmontero <nmontero@redhat.com> - 47.1-1
- Update to 47.1

* Mon Sep 16 2024 David King <amigadave@amigadave.com> - 47.0-1
- Update to 47.0

* Thu Aug 08 2024 nmontero <nmontero@redhat.com> - 47~beta-1
- Update to 47.beta

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 47~alpha-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jul 05 2024 David King <amigadave@amigadave.com> - 47~alpha-1
- Update to 47.alpha

* Sat Mar 16 2024 David King <amigadave@amigadave.com> - 46.0-1
- Update to 46.0

* Fri Mar 08 2024 David King <amigadave@amigadave.com> - 46~rc-1
- Update to 46.rc

* Mon Feb 19 2024 David King <amigadave@amigadave.com> - 46~beta-1
- Update to 46.beta

* Sun Feb 18 2024 David King <amigadave@amigadave.com> - 45.2-1
- Update to 45.2

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 45.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Oct 24 2023 Kalev Lember <klember@redhat.com> - 45.1-1
- Update to 45.1

* Thu Sep 21 2023 Kalev Lember <klember@redhat.com> - 45.0-1
- Update to 45.0
- Remove and obsolete libsysprof-ui subpackage
- Drop RHEL libunwind build conditionals as it's no longer an optional dep

* Fri Aug 11 2023 Yaakov Selkowitz <yselkowi@redhat.com> - 3.48.0-3
- Disable libunwind in RHEL builds

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.48.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sun Mar 19 2023 David King <amigadave@amigadave.com> - 3.48.0-1
- Update to 3.48.0

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.46.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Sep 16 2022 Kalev Lember <klember@redhat.com> - 3.46.0-1
- Update to 3.46.0

* Mon Aug 08 2022 Kalev Lember <klember@redhat.com> - 3.45.1-1
- Update to 3.45.1
- Add new -agent subpackage for sysprof-agent

* Thu Jul 28 2022 Kalev Lember <klember@redhat.com> - 3.45.0-2
- Remove old conflicts

* Thu Jul 28 2022 Kalev Lember <klember@redhat.com> - 3.45.0-1
- Update to 3.45.0

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.44.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sat Mar 19 2022 David King <amigadave@amigadave.com> - 3.44.0-1
- Update to 3.44.0

* Wed Mar 09 2022 David King <amigadave@amigadave.com> - 3.43.90-1
- Update to 3.43.90

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.42.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Nov 05 2021 Kalev Lember <klember@redhat.com> - 3.42.1-2
- Build with libunwind support

* Fri Nov 05 2021 Kalev Lember <klember@redhat.com> - 3.42.1-1
- Update to 3.42.1

* Tue Sep 21 2021 Kalev Lember <klember@redhat.com> - 3.42.0-1
- Update to 3.42.0

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.40.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Mar 23 2021 Kalev Lember <klember@redhat.com> - 3.40.1-1
- Update to 3.40.1

* Mon Mar 22 2021 Kalev Lember <klember@redhat.com> - 3.40.0-1
- Update to 3.40.0

* Tue Mar 16 2021 Kalev Lember <klember@redhat.com> - 3.39.94-2
- Add explicit conflicts to help with upgrades

* Thu Feb 25 2021 Kalev Lember <klember@redhat.com> - 3.39.94-1
- Update to 3.39.94

* Thu Feb 25 2021 Kalev Lember <klember@redhat.com> - 3.39.92-5
- Revert "Move org.gnome.Sysprof3.Profiler.xml to sysprof-capture-devel"

* Wed Feb 24 2021 Kalev Lember <klember@redhat.com> - 3.39.92-4
- Move org.gnome.Sysprof3.Profiler.xml to sysprof-capture-devel

* Wed Feb 24 2021 Kalev Lember <klember@redhat.com> - 3.39.92-3
- Update minimum required glib2 version

* Wed Feb 24 2021 Kalev Lember <klember@redhat.com> - 3.39.92-2
- Split sysprof-capture library and header files out to sysprof-capture-
  devel

* Wed Feb 24 2021 Kalev Lember <klember@redhat.com> - 3.39.92-1
- Update to 3.39.92

* Mon Feb 22 2021 Kalev Lember <klember@redhat.com> - 3.39.90-2
- Specify pic for static libsysprof-capture

* Thu Feb 18 2021 Kalev Lember <klember@redhat.com> - 3.39.90-1
- Update to 3.39.90

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.38.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Oct 20 2020 Kalev Lember <klember@redhat.com> - 3.38.1-2
- Rebuild

* Fri Oct 16 2020 Kalev Lember <klember@redhat.com> - 3.38.1-1
- Update to 3.38.1

* Sun Sep 20 2020 Kalev Lember <klember@redhat.com> - 3.38.0-2
- Split out a separate libsysprof package and avoid -devel subpackage
  depending on the GUI app.

* Sat Sep 12 2020 Kalev Lember <klember@redhat.com> - 3.38.0-1
- Update to 3.38.0

* Mon Sep 07 2020 Kalev Lember <klember@redhat.com> - 3.37.92-1
- Update to 3.37.92

* Mon Aug 17 2020 Kalev Lember <klember@redhat.com> - 3.37.90-1
- Update to 3.37.90

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.36.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sat Mar 07 2020 Kalev Lember <klember@redhat.com> - 3.36.0-2
- Fix the build on 32 bit hosts

* Sat Mar 07 2020 Kalev Lember <klember@redhat.com> - 3.36.0-1
- Update to 3.36.0

* Mon Mar 02 2020 Kalev Lember <klember@redhat.com> - 3.35.92-1
- Update to 3.35.92

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.35.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jan 10 2020 Kalev Lember <klember@redhat.com> - 3.35.3-1
- Update to 3.35.3

* Wed Dec 11 2019 Adam Williamson <awilliam@redhat.com> - 3.35.2-1
- Bump to new release (per hergertme and fmuellner)

* Mon Oct 07 2019 Kalev Lember <klember@redhat.com> - 3.34.1-1
- Update to 3.34.1

* Tue Sep 10 2019 Kalev Lember <klember@redhat.com> - 3.34.0-1
- Update to 3.34.0

* Thu Sep 05 2019 Kalev Lember <klember@redhat.com> - 3.33.92-2
- Set minimum required glib2 version

* Thu Sep 05 2019 Kalev Lember <klember@redhat.com> - 3.33.92-1
- Update to 3.33.92

* Tue Aug 27 2019 Kalev Lember <klember@redhat.com> - 3.33.90-2
- Add kernel-tools runtime dep for turbostat

* Mon Aug 26 2019 Kalev Lember <klember@redhat.com> - 3.33.90-1
- Update to 3.33.90

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.33.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Jul 19 2019 Kalev Lember <klember@redhat.com> - 3.33.3-1
- Update to 3.33.3

* Wed Mar 13 2019 Kalev Lember <klember@redhat.com> - 3.32.0-1
- Update to 3.32.0

* Tue Feb 19 2019 Kalev Lember <klember@redhat.com> - 3.31.91-1
- Update to 3.31.91

* Thu Feb 07 2019 Kalev Lember <klember@redhat.com> - 3.31.90-1
- Update to 3.31.90

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.31.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jan 10 2019 Kalev Lember <klember@redhat.com> - 3.31.1-2
- Backport new API for gnome-builder

* Tue Oct 09 2018 Kalev Lember <klember@redhat.com> - 3.31.1-1
- Update to 3.31.1

* Wed Sep 26 2018 Kalev Lember <klember@redhat.com> - 3.30.1-1
- Update to 3.30.1

* Fri Sep 07 2018 Kalev Lember <klember@redhat.com> - 3.30.0-2
- Drop ldconfig scriptlets

* Fri Sep 07 2018 Kalev Lember <klember@redhat.com> - 3.30.0-1
- Update to 3.30.0

* Tue Jul 31 2018 Florian Weimer <fweimer@redhat.com> - 3.28.1-4
- Rebuild with fixed binutils

* Sun Jul 29 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 3.28.1-3
- BR: gcc/gcc-c++

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.28.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Apr 10 2018 Kalev Lember <klember@redhat.com> - 3.28.1-1
- Update to 3.28.1

* Wed Mar 14 2018 Kalev Lember <klember@redhat.com> - 3.28.0-1
- Update to 3.28.0

* Mon Mar 05 2018 Kalev Lember <klember@redhat.com> - 3.27.92-1
- Update to 3.27.92

* Sat Mar 03 2018 Kalev Lember <klember@redhat.com> - 3.27.91-2
- Backport a patch to fix the build on 32 bit arches

* Sat Mar 03 2018 Kalev Lember <klember@redhat.com> - 3.27.91-1
- Update to 3.27.91
- Switch to the meson build system

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.26.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Feb 03 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 3.26.1-3
- Switch to %%ldconfig_scriptlets

* Fri Jan 05 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 3.26.1-2
- Remove obsolete scriptlets

* Sun Oct 08 2017 Kalev Lember <klember@redhat.com> - 3.26.1-1
- Update to 3.26.1

* Sat Sep 16 2017 Kalev Lember <klember@redhat.com> - 3.26.0-1
- Update to 3.26.0

* Thu Sep 07 2017 Kalev Lember <klember@redhat.com> - 3.25.92-1
- Update to 3.25.92

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.24.1-3
- Rebuilt for
  https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.24.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Apr 11 2017 Kalev Lember <klember@redhat.com> - 3.24.1-1
- Update to 3.24.1

* Mon Mar 20 2017 Kalev Lember <klember@redhat.com> - 3.24.0-1
- Update to 3.24.0

* Thu Mar 16 2017 Kalev Lember <klember@redhat.com> - 3.23.92-1
- Update to 3.23.92

* Wed Mar 01 2017 Kalev Lember <klember@redhat.com> - 3.23.91-2
- Add appdata validation

* Wed Mar 01 2017 Kalev Lember <klember@redhat.com> - 3.23.91-1
- Update to 3.23.91

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.22.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Nov 29 2016 Kalev Lember <klember@redhat.com> - 3.22.3-1
- Update to 3.22.3

* Wed Nov 02 2016 Kalev Lember <klember@redhat.com> - 3.22.2-1
- Update to 3.22.2

* Wed Oct 12 2016 Kalev Lember <klember@redhat.com> - 3.22.1-2
- Don't use -Werror for builds

* Wed Oct 12 2016 Kalev Lember <klember@redhat.com> - 3.22.1-1
- Update to 3.22.1

* Wed Sep 21 2016 Kalev Lember <klember@redhat.com> - 3.22.0-2
- Split out sysprof-cli and libsysprof-ui subpackages

* Wed Sep 21 2016 Kalev Lember <klember@redhat.com> - 3.22.0-1
- Update to 3.22.0

* Mon Sep 05 2016 Peter Robinson <pbrobinson@gmail.com> - 3.21.91-2
- Build on all arches now generic atomics supported

* Fri Sep 02 2016 Kalev Lember <klember@redhat.com> - 3.21.91-1
- Update to 3.21.91

* Tue Aug 23 2016 Kalev Lember <klember@redhat.com> - 3.21.90-2
- Enable building for arm architectures

* Tue Aug 23 2016 Kalev Lember <klember@redhat.com> - 3.21.90-1
- Update to 3.21.90

* Mon Aug 08 2016 Kalev Lember <klember@redhat.com> - 3.20.0-2
- Modernize spec file

* Mon Aug 08 2016 Kalev Lember <klember@redhat.com> - 3.20.0-1
- Update to 3.20.0

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jun 19 2015 Dennis Gilmore <dennis@ausil.us> - 1.2.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Aug 18 2014 Peter Robinson <pbrobinson@fedoraproject.org> - 1.2.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Dennis Gilmore <dennis@ausil.us> - 1.2.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Dennis Gilmore <dennis@ausil.us> - 1.2.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jun 28 2013 Gianluca Sforna <giallu@gmail.com> - 1.2.0-4
- fix udev rule path (#979545)

* Fri Feb 15 2013 Dennis Gilmore <dennis@ausil.us> - 1.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Sep 16 2012 Gianluca Sforna <giallu@gmail.com> - 1.2.0-2
- New upstream release

* Sun Sep 16 2012 Gianluca Sforna <giallu@gmail.com> - 1.2.0-1
- New upstream release

* Sat Jul 21 2012 Dennis Gilmore <dennis@ausil.us> - 1.1.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Dennis Gilmore <dennis@ausil.us> - 1.1.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Nov 07 2011 Adam Jackson <ajax@redhat.com> - 1.1.8-2
- Rebuild to break bogus libpng dependency

* Thu Jul 28 2011 Gianluca Sforna <giallu@gmail.com> - 1.1.8-1
- New upstream release

* Fri Jun 24 2011 Gianluca Sforna <giallu@gmail.com> - 1.1.6-4
- Fix missing icon (#558089)

* Wed Feb 09 2011 Dennis Gilmore <dennis@ausil.us> - 1.1.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jul 29 2010 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.6-2
- dist-git conversion

* Tue Jun 08 2010 Gianluca Sforna <giallu@fedoraproject.org> - 1.1.6-1
- New upstream release

* Wed Nov 25 2009 Bill Nottingham <notting@fedoraproject.org> - 1.1.2-8
- Fix typo that causes a failure to update the common directory. (releng
  #2781)

* Mon Sep 28 2009 Gianluca Sforna <giallu@fedoraproject.org> - 1.1.2-7
- Incorporate suggestions from package review - Require kernel 2.6.31 -
  Updated description

* Sun Sep 27 2009 Gianluca Sforna <giallu@fedoraproject.org> - 1.1.2-6
- Forgot to revive Makefile

* Sun Sep 27 2009 Gianluca Sforna <giallu@fedoraproject.org> - 1.1.2-5
- Revive sysprof package

* Tue Feb 19 2008 Jesse Keating <jkeating@fedoraproject.org> - 1.0.9-4
- Autorebuild for GCC 4.3

* Thu Dec 27 2007 Gianluca Sforna <giallu@fedoraproject.org> - 1.0.9-3
- add subpackage with kernel module sources - obsolete kmod-sysprof - add
  patch for warning user about missing module - add README.Fedora file with
  module build procedure

* Fri Dec 07 2007 Jesse Keating <jkeating@fedoraproject.org> - 1.0.9-2
- Rebuild for deps

* Sat Dec 01 2007 Gianluca Sforna <giallu@fedoraproject.org> - 1.0.9-1
- version update to 1.0.9 - drop kernel module - do not add category
  X-Fedora to desktop file

* Tue Aug 28 2007 Gianluca Sforna <giallu@fedoraproject.org> - 1.0.8-2
- update License field

* Thu Dec 21 2006 Gianluca Sforna <giallu@fedoraproject.org> - 1.0.8-1
- version update to 1.0.8

* Tue Nov 21 2006 Gianluca Sforna <giallu@fedoraproject.org> - 1.0.7-1
- new sources

* Wed Nov 01 2006 Gianluca Sforna <giallu@fedoraproject.org> - 1.0.5-1
- version updated to 1.0.5

* Sun Oct 08 2006 Gianluca Sforna <giallu@fedoraproject.org> - 1.0.3-3
- ExclusiveArch: i386 -> %%{ix86}

* Sat Oct 07 2006 Gianluca Sforna <giallu@fedoraproject.org> - 1.0.3-2
- Do not build for ppc (the kmod does not support it)

* Wed Oct 04 2006 Gianluca Sforna <giallu@fedoraproject.org> - 1.0.3-1
- auto-import sysprof-1.0.3-4 on branch devel from sysprof-1.0.3-4.src.rpm
## END: Generated by rpmautospec
