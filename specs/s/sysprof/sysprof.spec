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
Version:        50.0
Release:        %autorelease
Summary:        A system-wide Linux profiler

License:        GPL-2.0-or-later AND GPL-3.0-or-later AND CC-BY-SA-4.0 AND CC0-1.0 AND BSD-2-Clause-Patent
URL:            http://www.sysprof.com
Source0:        https://download.gnome.org/sources/sysprof/50/sysprof-%{tarball_version}.tar.xz

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
* Tue Sep 01 2026 Unknown User <please-configure-git-user@example.com> - 50.0-2
- Uncommitted changes

* Tue Mar 17 2026 Milan Crha <mcrha@redhat.com> - 50.0-1
- Update to 50.0

* Mon Mar 02 2026 Jan Grulich <jgrulich@redhat.com> - 50~rc-4
- Packit: drop upstream_project_url and rely on release-monitoring only

* Wed Feb 25 2026 Jan Grulich <jgrulich@redhat.com> - 50~rc-3
- Packit: drop fast_forward_merge_into as current stable branches diverge

* Tue Feb 24 2026 Jan Grulich <jgrulich@redhat.com> - 50~rc-2
- RPMAUTOSPEC: unresolvable merge
## END: Generated by rpmautospec
