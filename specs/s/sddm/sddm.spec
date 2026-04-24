# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Disable X11 for RHEL 10+
%bcond x11 %[%{undefined rhel} || 0%{?rhel} < 10]

Name:           sddm
Version:        0.21.0
Release: 11%{?dist}
License:        GPL-2.0-or-later
Summary:        QML based desktop and login manager

URL:            https://github.com/sddm/sddm
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

## upstream patches
# Port all themes to Qt 6
# Submitted: https://github.com/sddm/sddm/pull/1876
Patch1:         sddm-PR1876.patch

## upstreamable patches
# Fix race with logind restart, and start seat0 if !CanGraphical on timer
# https://bugzilla.redhat.com/show_bug.cgi?id=2011991
# https://bugzilla.redhat.com/show_bug.cgi?id=2016310
# Submmited: https://github.com/sddm/sddm/pull/1494
Patch11:        0001-Delay-for-logind-and-fallback-to-seat0.patch

## downstream patches
Patch101:       sddm-0.20.0-fedora_config.patch

# sddm.service: +EnvironmentFile=-/etc/sysconfig/sddm
Patch103:       sddm-0.18.0-environment_file.patch

# Workaround for https://pagure.io/fedora-kde/SIG/issue/87
Patch104:       sddm-rpmostree-tmpfiles-hack.patch

# Workaround lack of Qt 5 greeter build
Patch105:       sddm-0.21.0-qt6greeter.patch

# Shamelessly stolen from gdm
Source10:       sddm.pam
# Shamelessly stolen from gdm
Source11:       sddm-autologin.pam
# Previously included in sddm sources
Source12:       sddm-greeter.pam
# sample sddm.conf generated with sddm --example-config, and entries commented-out
Source13: sddm.conf
# README.scripts
Source14: README.scripts
# sysconfig snippet
Source15: sddm.sysconfig
# sddm x11 override config
Source16:  sddm-x11.conf
# sysusers config file. note these are shipped in the upstream tarball
# but we cannot use the files from the tarball for %pre scriptlet
# generation, so we duplicate them as source files for that purpose;
# this is an ugly hack that should be removed if it becomes possible.
# see https://lists.fedoraproject.org/archives/list/devel@lists.fedoraproject.org/thread/TFDMAU7KLMSQTKPJELHSM6PFVXIZ56GK/
Source17:        sddm-systemd-sysusers.conf


Provides: service(graphical-login) = sddm

BuildRequires:  cmake >= 2.8.8
BuildRequires:  extra-cmake-modules
BuildRequires:  pam-devel
BuildRequires:  pkgconfig(libsystemd)
BuildRequires:  pkgconfig(systemd)
BuildRequires:  pkgconfig(xcb)
BuildRequires:  pkgconfig(xcb-xkb)
# sometimes python-docutils, sometimes python2-docutils, sometimes python3-docutils.
# use path then for sanity
BuildRequires:  /usr/bin/rst2man
BuildRequires:  cmake(Qt6Core)
BuildRequires:  cmake(Qt6DBus)
BuildRequires:  cmake(Qt6Gui)
BuildRequires:  cmake(Qt6Qml)
BuildRequires:  cmake(Qt6Quick)
BuildRequires:  cmake(Qt6LinguistTools)
BuildRequires:  cmake(Qt6Test)
BuildRequires:  cmake(Qt6QuickTest)
# verify presence to pull defaults from /etc/login.defs
BuildRequires:  shadow-utils
BuildRequires:  systemd
BuildRequires:  systemd-rpm-macros

Obsoletes: kde-settings-sddm < 20-5

%if 0%{?fedora}
# for /usr/share/backgrounds/default.{jxl,png}
BuildRequires: desktop-backgrounds-compat
BuildRequires: GraphicsMagick
Requires: desktop-backgrounds-compat
# for jxl support
Requires: kf6-kimageformats%{?_isa}
# for /usr/share/pixmaps/system-logo-white.png
Requires: system-logos
%endif
Requires: systemd
%if %{with x11}
Requires: xorg-x11-xinit
%endif
%{?systemd_requires}

Requires(pre): shadow-utils

# Virtual dependency for sddm greeter setup
Requires: sddm-greeter-displayserver
Suggests: sddm-wayland-generic

%description
SDDM is a modern graphical display manager aiming to be fast, simple and
beautiful. It uses modern technologies like QtQuick, which in turn gives the
designer the ability to create smooth, animated user interfaces.

%package wayland-generic
Summary: Generic Wayland SDDM greeter configuration
Provides: sddm-greeter-displayserver
Conflicts: sddm-greeter-displayserver
Requires: weston
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description wayland-generic
This package contains configuration and dependencies for SDDM
to use Weston for the greeter display server.

This is the generic default Wayland configuration provided
by SDDM.

%if %{with x11}
%package x11
Summary: X11 SDDM greeter configuration
Provides: sddm-greeter-displayserver
Conflicts: sddm-greeter-displayserver
# This will eventually go away...
Provides: deprecated()
Requires: xorg-x11-server-Xorg
Requires: %{name} = %{version}-%{release}
Recommends: qt6-qtvirtualkeyboard
BuildArch: noarch

%description x11
This package contains configuration and dependencies for SDDM
to use X11 for the greeter display server.
%endif

%package themes
Summary: SDDM Themes
# for upgrade path
Obsoletes: sddm < 0.2.0-0.12
Requires: %{name} = %{version}-%{release}
BuildArch: noarch
%description themes
A collection of sddm themes, including: elarun, maldives, maya


%prep
%autosetup -p1 %{?commitdate:-n %{name}-%{commit}}

%if 0%{?fedora}
bg_file_ext="jxl"
if [ -f "/usr/share/backgrounds/default.png" ]; then
bg_file_ext="png"
fi
#FIXME/TODO: use version on filesystem instead of using a bundled copy
cp -v "/usr/share/backgrounds/default.${bg_file_ext}"  \
      "src/greeter/theme/background.${bg_file_ext}"
ls -sh "src/greeter/theme/background.${bg_file_ext}"
gm mogrify -resize 1920x1200 "src/greeter/theme/background.${bg_file_ext}"
ls -sh "src/greeter/theme/background.${bg_file_ext}"

if [ "$bg_file_ext" != "png" ]; then
sed -e "s/background.png/background.${bg_file_ext}/g" -i src/greeter/theme.qrc src/greeter/theme/{Main.qml,theme.conf}
fi
%endif


%build
%cmake \
  -DBUILD_WITH_QT6:BOOL=ON \
  -DBUILD_MAN_PAGES:BOOL=ON \
  -DCMAKE_BUILD_TYPE:STRING="Release" \
  -DENABLE_JOURNALD:BOOL=ON \
  -DSESSION_COMMAND:PATH=/etc/X11/xinit/Xsession \
  -DWAYLAND_SESSION_COMMAND:PATH=/etc/sddm/wayland-session

%cmake_build


%install
%cmake_install

mkdir -p %{buildroot}%{_sysconfdir}/sddm.conf.d
mkdir -p %{buildroot}%{_prefix}/lib/sddm/sddm.conf.d
install -Dpm 644 %{SOURCE10} %{buildroot}%{_sysconfdir}/pam.d/sddm
install -Dpm 644 %{SOURCE11} %{buildroot}%{_sysconfdir}/pam.d/sddm-autologin
install -Dpm 644 %{SOURCE12} %{buildroot}%{_sysconfdir}/pam.d/sddm-greeter
install -Dpm 644 %{SOURCE13} %{buildroot}%{_sysconfdir}/sddm.conf
install -Dpm 644 %{SOURCE14} %{buildroot}%{_datadir}/sddm/scripts/README.scripts
install -Dpm 644 %{SOURCE15} %{buildroot}%{_sysconfdir}/sysconfig/sddm
%if %{with x11}
install -Dpm 644 %{SOURCE16} %{buildroot}%{_prefix}/lib/sddm/sddm.conf.d/x11.conf
%endif
mkdir -p %{buildroot}/run/sddm
mkdir -p %{buildroot}%{_localstatedir}/lib/sddm
mkdir -p %{buildroot}%{_sysconfdir}/sddm/
cp -a %{buildroot}%{_datadir}/sddm/scripts/* \
      %{buildroot}%{_sysconfdir}/sddm/
# we're using /etc/X11/xinit/Xsession (by default) instead
rm -fv %{buildroot}%{_sysconfdir}/sddm/Xsession

# De-conflict the dbus file
mv %{buildroot}%{_datadir}/dbus-1/system.d/org.freedesktop.DisplayManager.conf \
   %{buildroot}%{_datadir}/dbus-1/system.d/org.freedesktop.DisplayManager-sddm.conf

%if 0%{?fedora} && 0%{?fedora} < 43
# Provide unversioned greeter until F40 is EOL
ln -sr %{buildroot}%{_bindir}/sddm-greeter-qt6 %{buildroot}%{_bindir}/sddm-greeter
%endif


%pre
%sysusers_create_compat %{SOURCE17}

%post
%systemd_post sddm.service
# handle incompatible configuration changes
(grep \
   -e '^Current=fedora$' \
   -e '^\[XDisplay\]$' \
   -e '^\[WaylandDisplay\]$' \
   %{_sysconfdir}/sddm.conf > /dev/null && \
 sed -i.rpmsave \
   -e 's|^Current=fedora$|#Current=01-breeze-fedora|' \
   -e 's|^\[XDisplay\]$|\[X11\]|' \
   -e 's|^\[WaylandDisplay\]$|\[Wayland\]|' \
   %{_sysconfdir}/sddm.conf
) ||:


%preun
%systemd_preun sddm.service


%postun
%systemd_postun sddm.service


%files
%license LICENSE
%doc README.md CONTRIBUTORS
%dir %{_sysconfdir}/sddm/
%dir %{_sysconfdir}/sddm.conf.d
%dir %{_prefix}/lib/sddm/sddm.conf.d
%config(noreplace)   %{_sysconfdir}/sddm/*
%config(noreplace)   %{_sysconfdir}/sddm.conf
%config(noreplace) %{_sysconfdir}/sysconfig/sddm
%config(noreplace) %{_sysconfdir}/pam.d/sddm*
%{_datadir}/dbus-1/system.d/org.freedesktop.DisplayManager-sddm.conf
%{_bindir}/sddm
%{_bindir}/sddm-greeter*
%{_libexecdir}/sddm-helper
%{_libexecdir}/sddm-helper-start-wayland
%{_libexecdir}/sddm-helper-start-x11user
%{_tmpfilesdir}/sddm.conf
%{_sysusersdir}/sddm.conf
%attr(0711, root, sddm) %dir /run/sddm
%attr(1770, sddm, sddm) %dir %{_localstatedir}/lib/sddm
%{_unitdir}/sddm.service
%{_qt6_archdatadir}/qml/SddmComponents/
%dir %{_datadir}/sddm
%{_datadir}/sddm/faces/
%{_datadir}/sddm/flags/
%{_datadir}/sddm/scripts/
%dir %{_datadir}/sddm/themes/
# %%lang'ify? they're small, probably not worth it -- rex
%{_datadir}/sddm/translations*/
%{_mandir}/man1/sddm.1*
%{_mandir}/man1/sddm-greeter.1*
%{_mandir}/man5/sddm.conf.5*
%{_mandir}/man5/sddm-state.conf.5*


%files wayland-generic
# No files since default configuration


%if %{with x11}
%files x11
%{_prefix}/lib/sddm/sddm.conf.d/x11.conf
%endif


%files themes
%{_datadir}/sddm/themes/elarun/
%{_datadir}/sddm/themes/maldives/
%{_datadir}/sddm/themes/maya/


%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.21.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Feb 15 2025 Neal Gompa <ngompa@fedoraproject.org> - 0.21.0-9
- Fix embedding correct background in default theme

* Sat Feb 15 2025 Neal Gompa <ngompa@fedoraproject.org> - 0.21.0-8
- Adapt to backgrounds in JPEG-XL format

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.21.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Oct 15 2024 Neal Gompa <ngompa@fedoraproject.org> - 0.21.0-6
- Rebuild to pick up F41 wallpapers

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.21.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Mar 20 2024 Neal Gompa <ngompa@fedoraproject.org> - 0.21.0-4
- Move pam configs back to /etc for now

* Wed Mar 20 2024 Neal Gompa <ngompa@fedoraproject.org> - 0.21.0-3
- Use our own greeter pam config and install pam configs to /usr

* Tue Mar 05 2024 Neal Gompa <ngompa@fedoraproject.org> - 0.21.0-2
- De-conflict sddm dbus configuration file

* Wed Feb 28 2024 Neal Gompa <ngompa@fedoraproject.org> - 0.21.0-1
- Update to 0.21.0

* Wed Feb 14 2024 Neal Gompa <ngompa@fedoraproject.org> - 0.20.0-11
- Add patch to fix desktop file parsing

* Wed Jan 31 2024 Alessandro Astone <ales.astone@gmail.com> - 0.20.0-10
- Remove LayerShellQt patch

* Mon Jan 29 2024 Neal Gompa <ngompa@fedoraproject.org> - 0.20.0-9
- Add patch to make SDDM uses kiosk-shell rather than fullscreen-shell

* Sat Jan 27 2024 Neal Gompa <ngompa@fedoraproject.org> - 0.20.0-8
- Switch to SPDX license identifiers

* Thu Nov 23 2023 Neal Gompa <ngompa@fedoraproject.org> - 0.20.0-7
- Disable X11 subpackage in RHEL 10+
- Drop unneeded scriptlets

* Mon Nov 20 2023 Alessandro Astone <ales.astone@gmail.com> - 0.20.0-6
- Backport patch to fix the keyboard with layer-shell

* Sun Nov 19 2023 Alessandro Astone <ales.astone@gmail.com> - 0.20.0-5
- Build against Qt6

* Tue Sep 19 2023 Alessandro Astone <ales.astone@gmail.com> - 0.20.0-4
- Hide keyboard layout picker in the wayland greeter

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.20.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jul 18 2023 Adam Williamson <awilliam@redhat.com> - 0.20.0-2
- Fix user/group creation - the config file *has* to be a package source

* Fri Jun 23 2023 Neal Gompa <ngompa@fedoraproject.org> - 0.20.0-1
- Update to 0.20.0 final

* Wed Apr 05 2023 Neal Gompa <ngompa@fedoraproject.org> - 0.19.0^git20230404.e652433-1
- Update to new snapshot to include a fix for logout issues (#2179591)

* Mon Mar 20 2023 Neal Gompa <ngompa@fedoraproject.org> - 0.19.0^git20230320.e07e805-2
- Add patch to stop launching xdg-desktop-portal with Wayland greeter (#2178971, #2129479)

* Mon Mar 20 2023 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 0.19.0^git20230320.e07e805-1
- Update to snapshot e07e805c21310572b4fecc810fd5610b1d3d03fd
- Fixes #2179591

* Mon Mar 06 2023 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 0.19.0^git20230306.7bd10de-1
- Update to new snapshot
- Fixes #2175947

* Mon Feb 20 2023 Neal Gompa <ngompa@fedoraproject.org> - 0.19.0^git20230214.8f1e3df-1
- Update to new snapshot
- Drop our sysusers and tmpfiles configuration for upstream versions

* Wed Feb 01 2023 Marc Deop <marcdeop@fedoraproject.org> - 0.19.0^git20230201.3ee57e9-2
- Update to new snapshot

* Wed Feb 01 2023 Marc Deop <marcdeop@fedoraproject.org> - 0.19.0^git20230201.b042f69-1
- Update to new snapshot.
- Remove patches merged upstream.

* Sun Jan 29 2023 Neal Gompa <ngompa@fedoraproject.org> - 0.19.0^git20221123.3e48649-3
- Add proposed patch to recover from tty switching failures (#2110801)

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.19.0^git20221123.3e48649-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Dec 24 2022 Neal Gompa <ngompa@fedoraproject.org> - 0.19.0^git20221123.3e48649-1
- Update to new snapshot
- Add patch to support non-default wayland socket names for sway/weston/etc.
- Refreshed patch for waiting on logind seat0 initialization

* Mon Nov 14 2022 Neal Gompa <ngompa@fedoraproject.org> - 0.19.0^git20221114.1d15689-1
- Update to new snapshot

* Tue Oct 25 2022 Neal Gompa <ngompa@fedoraproject.org> - 0.19.0^git20221025.fc24321-1
- Update to new snapshot

* Thu Sep 22 2022 Neal Gompa <ngompa@fedoraproject.org> - 0.19.0^git20220921.21e965a-1
- Update to new snapshot

* Thu Aug 18 2022 Timothée Ravier <tim@siosm.fr> - 0.19.0^git20220321.e67307e-4
- Skip enabling Wayland by default on F37

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.19.0^git20220321.e67307e-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sun Apr 03 2022 Neal Gompa <ngompa@fedoraproject.org> - 0.19.0^git20220321.e67307e-2
- Switch X11 greeter to rootful X server (#2070130)

* Sun Apr 03 2022 Neal Gompa <ngompa@fedoraproject.org> - 0.19.0^git20220321.e67307e-1
- Bump to new git snapshot to include refreshed fix for sddm crash (#2057419)

* Mon Mar 14 2022 Neal Gompa <ngompa@fedoraproject.org> - 0.19.0^git20220228.c257a40-4
- Switch back to the X11 greeter for F36

* Sun Mar 06 2022 Neal Gompa <ngompa@fedoraproject.org> - 0.19.0^git20220228.c257a40-3
- Backport fix to get sddm to log to the journal more

* Mon Feb 28 2022 Adam Williamson <awilliam@redhat.com> - 0.19.0^git20220228.c257a40-2
- Backport PR#1522 to try and fix crash after login (#2057419)

* Mon Feb 28 2022 Neal Gompa <ngompa@fedoraproject.org> - 0.19.0^git20220228.c257a40-1
- Update to new snapshot
- Drop merged proposed patch to not ignore EINTR when activating

* Fri Feb 25 2022 Neal Gompa <ngompa@fedoraproject.org> - 0.19.0^git20220224.5ad9f19-2
- Add proposed patch to not ignore EINTR when activating

* Fri Feb 25 2022 Neal Gompa <ngompa@fedoraproject.org> - 0.19.0^git20220224.5ad9f19-1
- Update to new snapshot release

* Mon Feb 07 2022 Neal Gompa <ngompa@fedoraproject.org> - 0.19.0^git20220130.85cbf3f-2
- Use unprivileged X server for sddm-x11 configuration

* Sun Jan 30 2022 Neal Gompa <ngompa@fedoraproject.org> - 0.19.0^git20220130.85cbf3f-1
- Update to snapshot release
- Drop upstreamed patches
- Drop Xauth patch due to inability to apply it
- Update status on remaining patches
- Add support for using a Wayland greeter
- Clean up Wayland conditionals

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.19.0-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Oct 25 2021 Adam Williamson <awilliam@redhat.com> - 0.19.0-18
- Simplify Wayland session hiding to just look for /dev/dri (jlinton) (#2016788)

* Sat Oct 23 2021 Adam Williamson <awilliam@redhat.com> - 0.19.0-17
- Patch udev rules, logind race and seat0 fallback (jlinton) (#2011991) (#2016310)

* Wed Oct 13 2021 Timothée Ravier <tim@siosm.fr> - 0.19.0-16
- Install the correct configuration for systemd-sysusers

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.19.0-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jun 08 2021 Rex Dieter <rdieter@fedoraproject.org> - 0.19.0-14
- Use systemd-sysusers config to setup user/group

* Fri Apr 23 2021 Neal Gompa <ngompa13@gmail.com> - 0.19.0-13
- Simplify to creating/deleting the flag file in the udev rule (#1952431)

* Thu Apr 22 2021 Neal Gompa <ngompa13@gmail.com> - 0.19.0-12
- Enable hiding Wayland sessions with a flag file (#1952431)

* Thu Apr 22 2021 Neal Gompa <ngompa13@gmail.com> - 0.19.0-11
- Add auto-fallback hack for when KMS isn't available (#1952431)

* Tue Apr 13 2021 Adam Williamson <awilliam@redhat.com> - 0.19.0-10
- Backport part of PR #1371 to improve session switching (#1929643)

* Fri Apr 02 2021 Rex Dieter <rdieter@fedoraproject.org> - 0.19.0-9
- initial support for sddm.conf.d snippets

* Sun Feb 28 2021 Neal Gompa <ngompa13@gmail.com> - 0.19.0-8
- Add trigger to auto-transition to Wayland session on upgrade to F34

* Wed Feb 03 2021 Rex Dieter <rdieter@fedoraproject.org> - 0.19.0-7
- adjust perms on /run/sddm to 1733 to future-proof xauth handling (#1922772)

* Mon Feb 01 2021 Rex Dieter <rdieter@fedoraproject.org> - 0.19.0-6
- revert to older Redesign-Xauth-handling.patch (#1922772)

* Thu Jan 28 2021 Rex Dieter <rdieter@fedoraproject.org> - 0.19.0-5
- pull in upstream fix for autologin (sddm issue #1348)

* Tue Jan 26 2021 Rex Dieter <rdieter@fedoraproject.org> - 0.19.0-4
- Refresh Xauth patch from upstream PR
- minor .spec cosmetics

* Fri Jan 22 2021 Neal Gompa <ngompa13@gmail.com> - 0.19.0-3
- Adjust sddm state file trigger for plasma-workspace 5.20.90-2

* Sun Jan 17 2021 Neal Gompa <ngompa13@gmail.com> - 0.19.0-2
- Add fix proposed upstream to fix SHELL setting in Wayland sessions

* Tue Nov 10 2020 Neal Gompa <ngompa13@gmail.com> - 0.19.0-1
- Rebase to version 0.19.0
- Refresh patch set and drop upstreamed patches

* Sun Oct 18 2020 Neal Gompa <ngompa13@gmail.com> - 0.18.1-9
- Add patch to prefer Wayland sessions on F34+
- Correctly handle Plasma session filename changes on upgrade to F34+

* Wed Aug 05 2020 Rex Dieter <rdieter@fedoraproject.org> - 0.18.1-8
- tmpfiles: use /run instead of /var/run

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.18.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jun 26 2020 Rex Dieter <rdieter@fedoraproject.org> - 0.18.1-6
- pull in upstream fix for duplicate session name

* Wed Apr 08 2020 Rex Dieter <rdieter@fedoraproject.org> - 0.18.1-5
- remove pam_console dependency (#182218)

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.18.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.18.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 03 2019 Rex Dieter <rdieter@fedoraproject.org> - 0.18.1-2
- consistently use auto_start in pam config (#1706029)

* Mon Apr 01 2019 Rex Dieter <rdieter@fedoraproject.org> - 0.18.1-1
- 0.18.1

* Fri Mar 15 2019 Rex Dieter <rdieter@fedoraproject.org> 0.18.0-6
- rebuild

* Thu Mar 14 2019 Rex Dieter <rdieter@fedoraproject.org> - 0.18.0-5
- sddm.service: EnvironmentFile=-/etc/sysconfig/sddm (#1686675)
- %%build: use %%make_build

* Wed Mar 13 2019 Rex Dieter <rdieter@fedoraproject.org> - 0.18.0-4
- pull in upstream fix for https://github.com/sddm/sddm/issues/1145 (#1667171)

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.18.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Oct 26 2018 Rex Dieter <rdieter@fedoraproject.org> - 0.18.0-2
- rebuild for f29 background

* Wed Jul 18 2018 Rex Dieter <rdieter@fedoraproject.org> - 0.18.0-1
- sddm-0.18.0
- rebase libXau patch (upstream pull request #863)
- drop patch from upstream pull request #735
- drop remnants of 02-fedora sddm theme

* Tue Jul 17 2018 Rex Dieter <rdieter@fedoraproject.org> - 0.17.0-6
- BR: /usr/bin/rst2man

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.17.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jun 18 2018 Rex Dieter <rdieter@fedoraproject.org> - 0.17.0-4
- pull in some upstream fixes

* Wed May 09 2018 Rex Dieter <rdieter@fedoraproject.org> - 0.17.0-3
- Suggests: qt5-qtvirtualkeyboard

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.17.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Dec 06 2017 Rex Dieter <rdieter@fedoraproject.org> - 0.17.0-1
- sddm-0.17.0, rebase patches
- Recommends: qt5-qtvirtualkeyboard

* Fri Dec 01 2017 Rex Dieter <rdieter@fedoraproject.org> - 0.16.0-2
- omit 'fedora' theme (rely on fallback maui instead)
- %%post themes: drop config hack, no longer needed

* Thu Nov 23 2017 Martin Bříza <mbriza@redhat.com> - 0.16.0-1
- sddm-0.16.0 (#1504466)

* Fri Oct 27 2017 Rex Dieter <rdieter@fedoraproject.org> - 0.15.0-3
- use fedora wallpaper for fallback/maui theme

* Wed Oct 04 2017 Martin Bříza <mbriza@redhat.com> - 0.15.0-2
- Fix a crash in the libXau patch (#1492371)

* Mon Sep 04 2017 Rex Dieter <rdieter@fedoraproject.org> - 0.15.0-1
- sddm-0.15.0 (#1487460)

* Fri Aug 25 2017 Martin Bříza <mbriza@redhat.com> - 0.14.0-14
- Update the libXau patch based on Steve Storey's findings

* Thu Aug 17 2017 Martin Bříza <mbriza@redhat.com> - 0.14.0-13
- Port from xauth to libXau (#1370222)

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jun 13 2017 Rex Dieter <rdieter@fedoraproject.org> - 0.14.0-10
- actually apply patch for bug #1446782

* Tue Jun 13 2017 Rex Dieter <rdieter@fedoraproject.org> - 0.14.0-9
- backport: UserModel: Check for duplicates from getpwent() (#1446782)

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sat Jan 28 2017 Rex Dieter <rdieter@fedoraproject.org> - 0.14.0-7
- EnableHiDPI=false default

* Tue Nov 08 2016 Adam Williamson <awilliam@redhat.com> - 0.14.0-6
- backport PR #735 to fix RHBZ #1392654

* Wed Nov 02 2016 Rex Dieter <rdieter@fedoraproject.org> - 0.14.0-5
- pull in upstream fixes

* Fri Oct 07 2016 Rex Dieter <rdieter@fedoraproject.org> - 0.14.0-4
- sddm.conf default: Current=01-breeze-fedora

* Mon Oct 03 2016 Rex Dieter <rdieter@fedoraproject.org> - 0.14.0-3
- drop deps used for fedora-only theme

* Mon Oct 03 2016 Rex Dieter <rdieter@fedoraproject.org> - 0.14.0-2
- make 02-fedora theme, fedora only

* Sun Aug 28 2016 Rex Dieter <rdieter@fedoraproject.org> - 0.14.0-1
- sddm-0.14.0
- -themes: circles theme was removed

* Fri Mar 11 2016 Rex Dieter <rdieter@fedoraproject.org> - 0.13.0-7
- pull in upstream fixes, some new features
- The desktop selection drop down list has an empty box (#1222228)
- sddm: RememberLastUser=false does not work (#1240749)

* Fri Mar 11 2016 Rex Dieter <rdieter@fedoraproject.org> 0.13.0-6
- sddm: use pam_gnome_keyring (#1317066)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.13.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Nov 16 2015 Rex Dieter <rdieter@fedoraproject.org> - 0.13.0-4
- rev sddm.conf for new defaults
- add /usr/share/sddm/scripts/README.scripts

* Sun Nov 15 2015 Rex Dieter <rdieter@fedoraproject.org> - 0.13.0-3
- merge Configuration.h into fedora_config.patch
- copy all scripts into /etc/sddm as %%config(noreplace)

* Sun Nov 15 2015 Rex Dieter <rdieter@fedoraproject.org> 0.13.0-2
- %%config(noreplace) /etc/sddm/Xsetup

* Sat Nov 07 2015 Rex Dieter <rdieter@fedoraproject.org> 0.13.0-1
- 0.13.0

* Thu Oct 29 2015 Rex Dieter <rdieter@fedoraproject.org> 0.12.0-6
- tweak DefaultPath (#1276450)

* Thu Oct 15 2015 Rex Dieter <rdieter@fedoraproject.org> 0.12.0-5
- Security fix for CVE-2015-0856 (#1271992,#1271993)

* Thu Sep 24 2015 Rex Dieter <rdieter@fedoraproject.org> 0.12.0-4
- omit 0008-Inherit-path-environment-variables-from-parent.patch pending security concerns

* Thu Sep 24 2015 Rex Dieter <rdieter@fedoraproject.org> - 0.12.0-3
- pull in upstream fixes (#1265813)
- fedora theme QML error (#1264946)

* Thu Sep 10 2015 Rex Dieter <rdieter@fedoraproject.org> 0.12.0-2
- sddm.pam: add pam_kwallet5 support

* Tue Sep 08 2015 Rex Dieter <rdieter@fedoraproject.org> 0.12.0-1
- 0.12.0

* Wed Sep 02 2015 Rex Dieter <rdieter@fedoraproject.org> 0.11.0-2
- use %%license tag

* Thu Aug 06 2015 Rex Dieter <rdieter@fedoraproject.org> - 0.11.0-1
- sddm-0.11 (#1209689), plus pull in a few post 0.11.0 upstream fixes
- Enable two fedora themes, allowing user selector as default (#1250204)

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 0.10.0-5
- Rebuilt for GCC 5 C++11 ABI change

* Thu Jan 29 2015 Dan Horák <dan[at]danny.cz> - 0.10.0-4
- don't Require Xorg server on s390(x)

* Wed Jan 21 2015 Martin Briza <mbriza@redhat.com> - 0.10.0-3
- Fixed positioning in the Fedora theme
- Resolves: #1183207

* Mon Oct 27 2014 Rex Dieter <rdieter@fedoraproject.org> - 0.10.0-2
- create/own %%{_sysconfdir}/sddm.conf, %%{_localstatedir}/lib/sddm (#1155898)
- don't mark stuff under /etc/dbus-1 %%config
- make %%{_localstatedir}/run/sddm group writable

* Thu Oct 16 2014 Martin Briza <mbriza@redhat.com> - 0.10.0-1
- Bump to 0.10.0

* Thu Oct 09 2014 Martin Briza <mbriza@redhat.com> - 0.9.0-2.20141007git6a28c29b
- Remove pam_gnome_keyring.so (temporarily) from sddm.pam to fix impossibility to log out
- Resolves: #1150283

* Tue Oct 07 2014 Martin Briza <mbriza@redhat.com> - 0.9.0-1.20141007git6a28c29b
- Bump to latest upstream git (and a new release)
- Hack around focus problem in the Fedora theme
- Compile against Qt5
- Removed upstreamed patch and files
- Resolves: #1114192 #1119777 #1123506 #1125129 #1140386 #1112841 #1128463 #1128465 #1149608 #1149628 #1148659 #1148660 #1149610 #1149629

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.0-0.32.20140627gitf49c2c79
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Jun 27 2014 Martin Briza <mbriza@redhat.com> - 0.2.0-0.31.20140627gitf49c2c79
- Patch unitialized values in signal handler in the daemon

* Fri Jun 27 2014 Martin Briza <mbriza@redhat.com> - 0.2.0-0.30.20140627gitf49c2c79
- Bump to latest upstream, switch back to sddm project
- Drop sddm.service
- Enable manpage and journald support

* Tue Jun 24 2014 Martin Briza <mbriza@redhat.com> - 0.2.0-0.29.20140623gitdb1d7381
- Fix default config to respect the new /usr/share paths
- Fixed multiple users after autologin

* Mon Jun 23 2014 Martin Briza <mbriza@redhat.com> - 0.2.0-0.28.20140623gitdb1d7381
- Fix Requires, release

* Mon Jun 23 2014 Martin Briza <mbriza@redhat.com> - 0.2.0-0.27.20131125gitdb1d7381
- Updated to the latest upstream git
- Notable changes: Greeter runs under the sddm user, it's possible to configure display setup, different install paths in /usr/share
- Resolves: #1034414 #1035939 #1035950 #1036308 #1038548 #1045722 #1045937 #1065715 #1082229 #1007067 #1027711 #1031745 #1008951 #1016902 #1031415 #1020921

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.0-0.26.20131125git7a008602
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May 01 2014 Rex Dieter <rdieter@fedoraproject.org> 0.2.0-0.25.20131125git7a008602
- update pam config (+pam_kwallet,-pam_mate_keyring)

* Mon Jan 27 2014 Adam Jackson <ajax@redhat.com> 0.2.0-0.24.20131125git7a008602
- Rebuild for new sonames in libxcb 1.10

* Mon Dec 16 2013 Martin Briza <mbriza@redhat.com> - 0.2.0-0.23.20131125git7a008602
- Revert all work done on authentication, doesn't support multiple logins right now

* Mon Nov 25 2013 Martin Briza <mbriza@redhat.com> - 0.2.0-0.22.20131125git7a008602
- Fix saving of last session and user

* Mon Nov 25 2013 Martin Briza <mbriza@redhat.com> - 0.2.0-0.21.20131125git7a008602
- Rebase to current upstream
- Fix the theme (and improve it by a bit)
- Fix the authentication stack
- Don't touch numlock on startup
- Disabled the XDMCP server until it's accepted upstream
- Resolves: #1016902 #1028799 #1031415 #1031745 #1020921 #1008951 #1004621

* Tue Nov 05 2013 Martin Briza <mbriza@redhat.com> - 0.2.0-0.20.20130914git50ca5b20
- Fix xdisplay and tty vars

* Tue Nov 05 2013 Martin Briza <mbriza@redhat.com> - 0.2.0-0.19.20130914git50ca5b20
- Patch cleanup

* Tue Nov 05 2013 Martin Briza <mbriza@redhat.com> - 0.2.0-0.18.20130914git50ca5b20
- Cmake magic

* Tue Nov 05 2013 Martin Briza <mbriza@redhat.com> - 0.2.0-0.17.20130914git50ca5b20
- Rewritten the authentication stack to work right with PAM

* Tue Oct 15 2013 Martin Briza <mbriza@redhat.com> - 0.2.0-0.16.20130914git50ca5b20
- Fixed the Fedora theme wallpaper path

* Tue Oct 15 2013 Martin Briza <mbriza@redhat.com> - 0.2.0-0.15.20130914git50ca5b20
- Added XDMCP support patch
- Modified the config to reflect the added XDMCP support (disabled by default)

* Tue Oct 15 2013 Rex Dieter <rdieter@fedoraproject.org> - 0.2.0-0.14.20130914git50ca5b20
- sddm.conf: CurrentTheme=fedora

* Mon Oct 14 2013 Rex Dieter <rdieter@fedoraproject.org> - 0.2.0-0.13.20130914git50ca5b20
- include standard theme/config here, Obsoletes: kde-settings-sddm
- sddm.conf: SessionCommand=/etc/X11/xinit/Xsession

* Mon Oct 14 2013 Rex Dieter <rdieter@fedoraproject.org> - 0.2.0-0.12.20130914git50ca5b20
- -themes: Obsoletes: sddm ... for upgrade path

* Mon Oct 14 2013 Rex Dieter <rdieter@fedoraproject.org> - 0.2.0-0.11.20130914git50ca5b20
- -themes subpkg

* Sat Sep 21 2013 Rex Dieter <rdieter@fedoraproject.org> - 0.2.0-0.10.20130914git50ca5b20
- use %%_qt4_importdir, %%systemd_requires macros
- own %%_datadir/apps/sddm
- fix Release
- drop explicit Requires: pam (let rpm autodeps handle it)

* Mon Sep 16 2013 Martin Briza <mbriza@redhat.com> - 0.2.0-0.9.20130914git50ca5b20
- Requires: kde-settings-sddm

* Mon Sep 16 2013 Martin Briza <mbriza@redhat.com> - 0.2.0-0.8.20130914git50ca5b20
- Moved the config to the kde-settings-sddm package

* Sat Sep 14 2013 Martin Briza <mbriza@redhat.com> - 0.2.0-0.7.20130914git50ca5b20
- Removed the nonfree font from the package, replaced with "Sans"
- Temporarily set my own repository as the origin to avoid having the font in the srpm
- Changing the source also brings us a few new commits and removes Patch1 for PAM

* Mon Sep 09 2013 Martin Briza <mbriza@redhat.com> - 0.2.0-0.6.20130821gite707e229
- Added the patch, forgot to apply it, now it's okay

* Mon Sep 09 2013 Martin Briza <mbriza@redhat.com> - 0.2.0-0.5.20130821gite707e229
- Set a better order of the X sessions selection and hidden the Custom one (#1004902)

* Mon Sep 02 2013 Martin Briza <mbriza@redhat.com> - 0.2.0-0.4.20130821gite707e229
- Complete PAM conversations and end them properly when the session ends
- Ship our own systemd service file especially to provide Conflicts: getty@tty1.service

* Tue Aug 27 2013 Martin Briza <mbriza@redhat.com> - 0.2.0-0.3.20130821gite707e229
- Suppress error output from missing PAMs.

* Tue Aug 27 2013 Martin Briza <mbriza@redhat.com> - 0.2.0-0.2.20130821gite707e229
- Switched the pam config to the one GDM uses. Solves issues with pulseaudio and possibly more.

* Thu Aug 22 2013 Martin Briza <mbriza@redhat.com> - 0.2.0-0.1.20130821gite707e229
- Fixed the package version

* Wed Aug 21 2013 Martin Briza <mbriza@redhat.com> - 0.2.0-0.130821.git.e707e229
- Imported the latest upstream git commit

* Mon Aug 19 2013 Martin Briza <mbriza@redhat.com> - 0.1.0-7
- Set the build to be hardened

* Tue Aug 06 2013 Martin Briza <mbriza@redhat.com> - 0.1.0-6
- Added mate-keyring to PAM config (#993397)

* Mon Jul 22 2013 Martin Briza <mbriza@redhat.com> - 0.1.0-5
- Store xauth in /var/run/sddm

* Mon Jul 22 2013 Martin Briza <mbriza@redhat.com> - 0.1.0-4
- Added the documentation bits

* Thu Jul 18 2013 Martin Briza <mbriza@redhat.com> - 0.1.0-3
- Changed the source package to tar.gz
- Config files are now noreplace
- Buildrequires -systemd-devel +systemd +cmake

* Tue Jul 16 2013 Martin Briza <mbriza@redhat.com> - 0.1.0-2
- Removed unneeded BuildRequires
- Fixed systemd scriptlets
- Fixed release
- Simplified setup
- Added Requires needed for basic function
- Added Provides for graphical login

* Thu Jul 04 2013 Martin Briza <mbriza@redhat.com> - 0.1.0-1
- Initial build
