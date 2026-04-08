# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Disable X11 for RHEL
%bcond x11 %[%{undefined rhel}]

%global commit c96b1944419fb49837253705be41961f2b3e6159
%global shortcommit %{sub %{commit} 1 7}
%global commitdate 20260112
%global gititer 1


Name:           plasma-login-manager
Version:        6.6.0
Release:        1%{?dist}
License:        BSD-3-Clause and CC0-1.0 and (GPL-2.0-only or GPL-3.0-only) and GPL-2.0-or-later and LGPL-2.0-or-later and LGPL-2.1-or-later
Summary:        QML based login manager from KDE

URL:            https://invent.kde.org/plasma/plasma-login-manager
Source0: http://download.kde.org/%{stable_kf6}/plasma/%{maj_ver_kf6}.%{min_ver_kf6}.%{bug_ver_kf6}/%{name}-%{version}.tar.xz
Source1: http://download.kde.org/%{stable_kf6}/plasma/%{maj_ver_kf6}.%{min_ver_kf6}.%{bug_ver_kf6}/%{name}-%{version}.tar.xz.sig

# README.scripts
Source10:       README.scripts
# sysconfig snippet
Source11:       plasmalogin.sysconfig
# sysusers config file. note these are shipped in the upstream tarball
# but we cannot use the files from the tarball for %pre scriptlet
# generation, so we duplicate them as source files for that purpose;
# this is an ugly hack that should be removed if it becomes possible.
# see https://lists.fedoraproject.org/archives/list/devel@lists.fedoraproject.org/thread/TFDMAU7KLMSQTKPJELHSM6PFVXIZ56GK/
Source12:       plasmalogin.sysusers
# sample plasmalogin.conf generated with plasmalogin --example-config, and entries commented-out
Source13:       plasmalogin.conf

# upstream patches

# proposed patches

# downstream patches
## plasmalogin.service: +EnvironmentFile=-/etc/sysconfig/plasmalogin
Patch1001:      plasmalogin-environment_file.patch
## Workaround for https://pagure.io/fedora-kde/SIG/issue/87
Patch1002:      plasmalogin-rpmostree-tmpfiles-hack.patch

Provides:       service(graphical-login) = plasmalogin

BuildRequires:  desktop-file-utils
BuildRequires:  cmake >= 3.22
BuildRequires:  extra-cmake-modules
BuildRequires:  gcc-c++
BuildRequires:  pam-devel
BuildRequires:  pkgconfig(libsystemd)
BuildRequires:  pkgconfig(systemd)
BuildRequires:  pkgconfig(xcb)
BuildRequires:  pkgconfig(xcb-xkb)
BuildRequires:  cmake(Qt6Core)
BuildRequires:  cmake(Qt6DBus)
BuildRequires:  cmake(Qt6Gui)
BuildRequires:  cmake(Qt6Qml)
BuildRequires:  cmake(Qt6Quick)
BuildRequires:  cmake(Qt6LinguistTools)
BuildRequires:  cmake(Qt6ShaderTools)
BuildRequires:  cmake(Qt6Test)
BuildRequires:  cmake(Qt6QuickTest)
BuildRequires:  cmake(KF6Config)
BuildRequires:  cmake(KF6Package)
BuildRequires:  cmake(KF6WindowSystem)
BuildRequires:  cmake(KF6I18n)
BuildRequires:  cmake(KF6DBusAddons)
BuildRequires:  cmake(KF6KCMUtils)
BuildRequires:  cmake(KF6Auth)
BuildRequires:  cmake(KF6KIO)
BuildRequires:  cmake(KF6KirigamiPlatform)
BuildRequires:  cmake(PlasmaQuick)
BuildRequires:  cmake(LayerShellQt)
BuildRequires:  cmake(LibKWorkspace)
BuildRequires:  cmake(LibKLookAndFeel)
BuildRequires:  cmake(KF6Screen)
# verify presence to pull defaults from /etc/login.defs
BuildRequires:  shadow-utils
BuildRequires:  systemd
BuildRequires:  systemd-rpm-macros
BuildRequires:  kf6-rpm-macros

# for jxl support
Requires:       kf6-kimageformats%{?_isa}

%if %{with x11}
Requires:       xorg-x11-xinit
%endif
%{?systemd_requires}

Requires:      kf6-filesystem
Requires:      kf6-kauth
Requires(pre): shadow-utils

Requires:      kde-settings-plasma

# Requires kwin-wayland
Requires:      kwin-wayland%{?_isa}
Requires:      (kcm-plasmalogin%{?_isa} if plasma-systemsettings%{?_isa})

%description
Plasma Login provides a display manager for KDE Plasma
and with an new frontend providing a greeter,
wallpaper plugin integration and a System Settings module (KCM).

%package -n kcm-plasmalogin
Summary: KDE KCM for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: dbus-common
Requires: plasma-systemsettings%{?_isa}
Requires: polkit
Requires: qt6-filesystem

%description -n kcm-plasmalogin
%{summary}.

%prep
%autosetup -p1


%conf
%cmake_kf6 \
  -DCMAKE_BUILD_TYPE:STRING="Release" \
  -DPAM_OS_CONFIGURATION:STRING="fedora" \
  -DSESSION_COMMAND:PATH=/etc/X11/xinit/Xsession \
  -DWAYLAND_SESSION_COMMAND:PATH=/etc/plasmalogin/wayland-session


%build
%cmake_build


%install
%cmake_install

%find_lang plasma_login
%find_lang kcm_plasmalogin


mkdir -p %{buildroot}%{_sysconfdir}/plasmalogin.conf.d
mkdir -p %{buildroot}%{_prefix}/lib/plasmalogin/plasmalogin.conf.d

install -Dpm 644 %{SOURCE10} %{buildroot}%{_datadir}/plasmalogin/scripts/README.scripts
install -Dpm 644 %{SOURCE11} %{buildroot}%{_sysconfdir}/sysconfig/plasmalogin
install -Dpm 644 %{SOURCE13} %{buildroot}%{_sysconfdir}/plasmalogin.conf

mkdir -p %{buildroot}/run/plasmalogin
mkdir -p %{buildroot}%{_localstatedir}/lib/plasmalogin
mkdir -p %{buildroot}%{_sysconfdir}/plasmalogin/
cp -a %{buildroot}%{_datadir}/plasmalogin/scripts/* \
      %{buildroot}%{_sysconfdir}/plasmalogin/
# we're using /etc/X11/xinit/Xsession (by default) instead
rm -fv %{buildroot}%{_sysconfdir}/plasmalogin/Xsession

# De-conflict the dbus file
mv %{buildroot}%{_datadir}/dbus-1/system.d/org.freedesktop.DisplayManager.conf \
   %{buildroot}%{_datadir}/dbus-1/system.d/org.freedesktop.DisplayManager-plasmalogin.conf


%check
desktop-file-validate %{buildroot}/%{_datadir}/applications/kcm_plasmalogin.desktop


%pre
%sysusers_create_compat %{SOURCE12}


%post
%systemd_post plasmalogin.service
%systemd_user_post plasma-login.service plasma-login-kwin_wayland.service plasma-login-wayland.target plasma-wallpaper.service


%preun
%systemd_preun plasmalogin.service
%systemd_user_preun plasma-login.service plasma-login-kwin_wayland.service plasma-login-wayland.target plasma-wallpaper.service


%postun
%systemd_postun plasmalogin.service
%systemd_user_postun plasma-login.service plasma-login-kwin_wayland.service plasma-login-wayland.target plasma-wallpaper.service


%files -f plasma_login.lang
%license LICENSE LICENSE.* LICENSES/*
%doc README.md
%dir %{_sysconfdir}/plasmalogin/
%dir %{_sysconfdir}/plasmalogin.conf.d
%dir %{_prefix}/lib/plasmalogin
%dir %{_prefix}/lib/plasmalogin/plasmalogin.conf.d
%config(noreplace) %{_sysconfdir}/plasmalogin/*
%config(noreplace) %{_sysconfdir}/plasmalogin.conf
%config(noreplace) %{_sysconfdir}/sysconfig/plasmalogin
%{_prefix}/lib/pam.d/plasmalogin*
%{_datadir}/dbus-1/system.d/org.freedesktop.DisplayManager-plasmalogin.conf
%{_bindir}/plasmalogin
%{_bindir}/startplasma-login-wayland
%{_bindir}/plasma-login-wallpaper
%{_libexecdir}/plasmalogin-helper
%{_libexecdir}/plasmalogin-helper-start-x11user
%{_libexecdir}/plasma-login-greeter
%{_tmpfilesdir}/plasmalogin.conf
%{_sysusersdir}/plasmalogin.conf
%attr(0711, root, plasmalogin) %dir /run/plasmalogin
%attr(1770, plasmalogin, plasmalogin) %dir %{_localstatedir}/lib/plasmalogin
%{_unitdir}/plasmalogin.service
%{_userunitdir}/plasma-login.service
%{_userunitdir}/plasma-login-kwin_wayland.service
%{_userunitdir}/plasma-login-wayland.target
%{_userunitdir}/plasma-wallpaper.service
%dir %{_datadir}/plasmalogin
%{_datadir}/plasmalogin/scripts/


%files -n kcm-plasmalogin -f kcm_plasmalogin.lang
%{_kf6_libexecdir}/kauth/kcmplasmalogin_authhelper
%{_kf6_qtplugindir}/plasma/kcms/systemsettings/kcm_plasmalogin.so
%{_datadir}/applications/kcm_plasmalogin.desktop
%{_datadir}/dbus-1/system-services/org.kde.kcontrol.kcmplasmalogin.service
%{_datadir}/dbus-1/system.d/org.kde.kcontrol.kcmplasmalogin.conf
%{_datadir}/polkit-1/actions/org.kde.kcontrol.kcmplasmalogin.policy


%changelog
* Thu Feb 12 2026 Steve Cossette <farchord@gmail.com> - 6.6.0-1
- 6.6.0

* Fri Jan 30 2026 Adam Williamson <awilliam@redhat.com> - 6.5.91-2
- Backport MR #102 to fix idle timeout issues

* Tue Jan 27 2026 Steve Cossette <farchord@gmail.com> - 6.5.91-1
- 6.5.91

* Sat Jan 17 2026 Fedora Release Engineering <releng@fedoraproject.org> - 6.5.90-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Tue Jan 13 2026 Steve Cossette <farchord@gmail.com> - 6.5.90-1
- 6.5.90

* Tue Jan 13 2026 farchord@gmail.com
- 6.5.90

* Mon Jan 12 2026 Neal Gompa <ngompa@fedoraproject.org> - 0.21.0~git1.20260112.c96b194-3
- Add WIP fix to avoid KCM breaking wallpaper settings

* Mon Jan 12 2026 Neal Gompa <ngompa@fedoraproject.org> - 0.21.0~git1.20260112.c96b194-2
- Fix install path for main config file

* Mon Jan 12 2026 Neal Gompa <ngompa@fedoraproject.org> - 0.21.0~git1.20260112.c96b194-1
- Bump to new git snapshot
- Drop merged patch

* Sun Jan 11 2026 Neal Gompa <ngompa@fedoraproject.org> - 0.21.0~git1.20260111.99ded95-2
- Add patch to read default wallpaper settings

* Sun Jan 11 2026 Neal Gompa <ngompa@fedoraproject.org> - 0.21.0~git1.20260111.99ded95-1
- Bump to new git snapshot

* Wed Dec 03 2025 Neal Gompa <ngompa@fedoraproject.org> - 0.21.0~git1.20251203.68b0122-1
- Bump to new git snapshot
- Add sample plasmalogin.conf

* Fri Nov 28 2025 Neal Gompa <ngompa@fedoraproject.org> - 0.21.0~git1.20251128.146250b-1
- Bump to new git snapshot

* Tue Nov 25 2025 Neal Gompa <ngompa@fedoraproject.org> - 0.21.0~git1.20251125.6972b55-1
- Initial package (partly forked from sddm)

