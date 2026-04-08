# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%if 0%{?fedora} >= 40 || 0%{?rhel} >= 10
%bcond initialsetup_gui_backend 1
%else
%bcond initialsetup_gui_backend 0
%endif

Summary: Config files for KDE
Name:    kde-settings
Version: 43.101
Release: 3%{?dist}

License: MIT
URL:     https://pagure.io/fedora-kde/kde-settings
Source0: %{url}/archive/%{version}/kde-settings-%{version}.tar.gz
Source1: COPYING

BuildArch: noarch

BuildRequires: kde-filesystem
# ssh-agent.service
BuildRequires: systemd-rpm-macros
Source10: ssh-agent.sh

BuildRequires: system-backgrounds-kde

# when kdebugrc was moved here
Conflicts: kf5-kdelibs4support < 5.7.0-3

Obsoletes: kde-settings-ksplash < 24-2
Obsoletes: kde-settings-minimal < 24-3

Requires: kde-filesystem
Requires: xdg-user-dirs >= 0.18-9
## add breeze deps here? probably, need more too -- rex
Requires: breeze-icon-theme
# Baseline mimeapps associations, e.g. LibreOffice
Requires: shared-mime-info

%description
%{summary}.

%package plasma
Summary: Configuration files for plasma
Requires: %{name} = %{version}-%{release}
Requires: system-backgrounds-kde
Requires: system-logos
Requires: google-noto-sans-fonts
# Not required but expected by users as we use other fonts from the noto "family"
Recommends: google-noto-serif-fonts
%if 0%{?rhel} && 0%{?rhel} < 9
Requires: google-noto-mono-fonts
%else
Requires: google-noto-sans-mono-fonts
%endif
%description plasma
%{summary}.


%package sddm
Summary: Configuration files for sddm
Requires: sddm
Requires: breeze-cursor-theme
%description sddm
%{summary}.

%package plasmalogin
Summary: Configuration files for Plasma Login Manager
Requires: plasma-login-manager >= 0.21.0~git1.20260112
%if 0%{?version_maj:1}
Requires: f%{version_maj}-backgrounds-kde
%endif
Supplements: (%{name} and plasma-login-manager)
%description plasmalogin
%{summary}.


# FIXME/TODO: can probably consider dropping this subpkg now that we
# have good comps and soft dependencies support -- rex
%package pulseaudio
Summary: Enable pulseaudio support in KDE
# nothing here to license
License: LicenseRef-Not-Copyrightable
Requires: %{name} = %{version}-%{release}
%if 0%{?rhel} && 0%{?rhel} < 9
Requires: pulseaudio
%else
Requires: pulseaudio-daemon
%endif
## legacy apps
Requires: (pipewire-alsa if pipewire-pulseaudio)
Requires: (alsa-plugins-pulseaudio if pulseaudio)
%description pulseaudio
%{summary}.

%package -n qt-settings
Summary: Configuration files for Qt
# qt-graphicssystem.* scripts use lspci
#Requires: pciutils
%description -n qt-settings
%{summary}.

%if %{with initialsetup_gui_backend}
%package -n initial-setup-gui-wayland-plasma
Summary: Run initial-setup GUI on Plasma Wayland
Provides: firstboot(gui-backend)
Conflicts: firstboot(gui-backend)
Requires: kwin-wayland
Requires: plasma-keyboard
Requires: xorg-x11-server-Xwayland
Requires: initial-setup-gui >= 0.3.99
Supplements: ((initial-setup or initial-setup-gui) and kwin-wayland)
Enhances: (initial-setup-gui and kwin-wayland)

%description -n initial-setup-gui-wayland-plasma
%{summary}.
%endif


%prep
%autosetup -p1

# omit crud
rm -fv Makefile


%build
# Intentionally left blank.  Nothing to see here.


%install
tar cpf - . | tar --directory %{buildroot} -xvpf -

if [ %{_prefix} != /usr ] ; then
   pushd %{buildroot}
   mv %{buildroot}/usr %{buildroot}%{_prefix}
   mv %{buildroot}/etc %{buildroot}%{_sysconfdir}
   popd
fi

cp -p %{SOURCE1} .

# legacy default wallpaper symlink
mkdir -p %{buildroot}%{_datadir}/wallpapers
ln -s Default %{buildroot}%{_datadir}/wallpapers/Fedora

%if 0%{?rhel} && 0%{?rhel} < 9
# for rhel 8 and older with older noto fonts
sed -e "s/Noto Sans Mono/Noto Mono/g" \
    -i %{buildroot}%{_datadir}/kde-settings/kde-profile/default/{share/config/kdeglobals,xdg/kdeglobals}
%endif

# for ssh-agent.serivce, set SSH_AUTH_SOCK
install -p -m644 -D %{SOURCE10} %{buildroot}%{_sysconfdir}/xdg/plasma-workspace/env/ssh-agent.sh

%if ! %{with initialsetup_gui_backend}
rm -rv %{buildroot}%{_libexecdir}/initial-setup
%endif

## unpackaged files


%check
test -e %{_datadir}/wallpapers/Default || ls -l %{_datadir}/wallpapers


%files
%license COPYING
%config(noreplace) %{_sysconfdir}/profile.d/kde*
%{_sysconfdir}/fonts/conf.d/10-sub-pixel-rgb-for-kde.conf
%{_sysconfdir}/kde/env/env.sh
%{_sysconfdir}/kde/env/gpg-agent-startup.sh
%{_sysconfdir}/kde/shutdown/gpg-agent-shutdown.sh
%{_sysconfdir}/kde/env/gtk2_rc_files.sh
%if 0%{?fedora} || 0%{?rhel} > 7
%{_sysconfdir}/kde/env/fedora-bookmarks.sh
%{_datadir}/kde-settings/
# these can probably go now -- rex
%{_prefix}/lib/rpm/plasma4.prov
%{_prefix}/lib/rpm/plasma4.req
%{_prefix}/lib/rpm/fileattrs/plasma4.attr
%{_datadir}/polkit-1/rules.d/11-fedora-kde-policy.rules
%endif
%config(noreplace) %{_sysconfdir}/xdg/kcm-about-distrorc
%config(noreplace) %{_sysconfdir}/xdg/kdebugrc
%dir %{_sysconfdir}/pam.d
%config(noreplace) %{_sysconfdir}/pam.d/kcheckpass
%config(noreplace) %{_sysconfdir}/pam.d/kscreensaver
# drop noreplace, so we can be sure to get the new kiosk bits
%config %{_sysconfdir}/kderc
%config %{_sysconfdir}/kde4rc
%if 0%{?rhel} && 0%{?rhel} <= 7
%exclude %{_datadir}/kde-settings/kde-profile/default/share/apps/plasma-desktop/init/00-defaultLayout.js
%endif

%files plasma
%{_datadir}/plasma/shells/org.kde.plasma.desktop/contents/updates/00-start-here-2.js
%{_sysconfdir}/xdg/plasma-workspace/env/env.sh
%{_sysconfdir}/xdg/plasma-workspace/env/gtk2_rc_files.sh
%{_sysconfdir}/xdg/plasma-workspace/env/gtk3_scrolling.sh
%dir %{_datadir}/plasma/look-and-feel/org.fedoraproject.fedora*.desktop/contents/plasmoidsetupscripts/
%{_datadir}/plasma/look-and-feel/org.fedoraproject.fedora*.desktop/contents/plasmoidsetupscripts/org.kde.plasma.kicker.js
%{_datadir}/plasma/look-and-feel/org.fedoraproject.fedora*.desktop/contents/plasmoidsetupscripts/org.kde.plasma.kickerdash.js
%{_datadir}/plasma/look-and-feel/org.fedoraproject.fedora*.desktop/contents/plasmoidsetupscripts/org.kde.plasma.kickoff.js
%{_datadir}/wallpapers/Fedora
%{_sysconfdir}/xdg/plasma-workspace/env/ssh-agent.sh


%files sddm
%{_prefix}/lib/sddm/sddm.conf.d/kde_settings.conf


%files plasmalogin
%{_prefix}/lib/plasmalogin/defaults.conf


%files pulseaudio
# nothing, this is a metapackage

%files -n qt-settings
%license COPYING
%config(noreplace) %{_sysconfdir}/Trolltech.conf

%if %{with initialsetup_gui_backend}
%files -n initial-setup-gui-wayland-plasma
%{_libexecdir}/initial-setup/run-gui-backend
%endif


%changelog
* Sun Feb 08 2026 Neal Gompa <ngompa@fedoraproject.org> - 43.101-3
- Correctly require plasma-keyboard

* Fri Jan 16 2026 Fedora Release Engineering <releng@fedoraproject.org> - 43.101-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Mon Jan 12 2026 Neal Gompa <ngompa@fedoraproject.org> - 43.101-1
- plasmalogin, kscreenlocker: Use the proper wallpaper theme and PLM config file path

* Sun Jan 11 2026 Neal Gompa <ngompa@fedoraproject.org> - 43.100-1
- Set wallpaper configuration for plasmalogin and kscreenlocker properly

* Fri Jan 09 2026 Yaakov Selkowitz <yselkowi@redhat.com> - 43.99-2
- Use system-backgrounds-kde for wallpaper symlink

* Sat Dec 27 2025 Neal Gompa <ngompa@fedoraproject.org> - 43.99-1
- look-and-feel: Add support for Fedora light/dark themes

* Mon Dec 15 2025 Alessandro Astone <ales.astone@gmail.com> - 43.98-1
- Use plasma-keyboard as the virtual keyboard for initial-setup

* Sun Dec 14 2025 Alessandro Astone <ales.astone@gmail.com> - 43.97-1
- Set org.kde.plasma.keyboard as default virtual keyboard

* Mon Sep 29 2025 Alessandro Astone <ales.astone@gmail.com> - 43.1-1
- Add default list of favorites for the application launcher

* Mon Sep 01 2025 Neal Gompa <ngompa@fedoraproject.org> - 43.0-1
- Bump for F43 backgrounds
- ShellCheck fixes for gpg-agent startup script
- Fixes for prelink handling logic in profile.d shell scripts

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 42.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue May 13 2025 Than Ngo <than@redhat.com> - 42.0-4
- Fix rhbz#2291074 - Directory is missing in RPM database

* Thu Feb 20 2025 Neal Gompa <ngompa@fedoraproject.org> - 42.0-3
- Bump minimum xdg-user-dirs package version to require systemd unit

* Wed Feb 19 2025 Neal Gompa <ngompa@fedoraproject.org> - 42.0-2
- Drop xdg-user-dirs hack as it's no longer needed

* Fri Feb 14 2025 Neal Gompa <ngompa@fedoraproject.org> - 42.0-1
- Bump for F42 backgrounds
- Cleanup and sync profile.d shell scripts

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 41.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jan 03 2025 Yaakov Selkowitz <yselkowi@redhat.com> - 41.2-2
- Avoid pam dependency

* Wed Sep 25 2024 Neal Gompa <ngompa@fedoraproject.org> - 41.2-1
- Drop AT-SPI Xwayland property script as it's now handled by KWin

* Tue Aug 20 2024 Neal Gompa <ngompa@fedoraproject.org> - 41.1-1
- Add AT-SPI Xwayland property script
- Make `ksshaskpass` the default for openssh

* Thu Aug 15 2024 Neal Gompa <ngompa@fedoraproject.org> - 41.0-1
- New release for new wallpapers (#2305264)

* Thu Aug 15 2024 Neal Gompa <ngompa@fedoraproject.org> - 40.1-1
- Set recommended space for NeoChat
- Set SDDM cursor size

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 40.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Mar 07 2024 Neal Gompa <ngompa@fedoraproject.org> - 40.0-1
- Bump for F40 backgrounds
- Enable login/logout sounds for a11y

* Tue Feb 20 2024 Alessandro Astone <ales.astone@gmail.com> - 39.1-7
- Enable maliit-keyboard by default
- Provide default mimeapps associations overrides over plasma-desktop

* Fri Feb 02 2024 Alessandro Astone <ales.astone@gmail.com> - 39.1-6
- Re-enable kwin blur plugin

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 39.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 39.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 05 2024 Alessandro Astone <ales.astone@gmail.com> - 39.1-3
- Fix initial-setup-gui version requirement

* Wed Jan 03 2024 Neal Gompa <ngompa@fedoraproject.org> - 39.1-2
- Add initial-setup-gui-wayland-plasma subpackage for f40+/epel10+

* Wed Jan 03 2024 Neal Gompa <ngompa@fedoraproject.org> - 39.1-1
- Add fontconfig snippet to enable RGBA subpixel rendering for KDE
- Reland: feat: remove KDE Action Restrictions
- Set the default theme for sddm

* Fri Oct 13 2023 Timothée Ravier <tim@siosm.fr> - 39.0-2
- Switch google-noto-serif-fonts to a Recommends

* Fri Sep 01 2023 Adam Williamson <awilliam@redhat.com> - 39.0-1
- New release 39.0 (to pick up Fedora 39 backgrounds)

* Mon Aug 07 2023 Neal Gompa <ngompa@fedoraproject.org> - 38.3-1
- kwinrc: Disable the Blur plugin in kwin by default

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 38.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon Mar 13 2023 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 38.2-2
- Add Requires: breeze-cursor-theme to sddm subpackage

* Sun Mar 12 2023 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 38.2-1
- Add sddm subpackage containing sddm config files

* Mon Feb 20 2023 Neal Gompa <ngompa@fedoraproject.org> - 38.1-1
- Disable fast user switching again (#2171316)

* Tue Feb 07 2023 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 38.0-1
- 38.0

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 37.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Aug 15 2022 Timothée Ravier <tim@siosm.fr> - 37.0-1
- 37.0

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 36.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue Jun 14 2022 Neal Gompa <ngompa@fedoraproject.org> - 36.1-1
- kdeglobals: Actually set default global theme properly

* Mon Feb 21 2022 Timothée Ravier <tim@siosm.fr> - 36.0-1
- 36.0

* Mon Feb 07 2022 Neal Gompa <ngompa@fedoraproject.org> - 35.1-1
- kdeglobals: Set the default Look and Feel package to Fedora Breeze

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 35.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Nov 15 2021 Timothée Ravier <tim@siosm.fr> - 35.0-2
- Add google-noto-serif-fonts as dependency

* Thu Sep 02 2021 Rex Dieter <rdieter@fedoraproject.org> - 35.0-1
- 35.0

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 34.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Jul 19 2021 Neal Gompa <ngompa@fedoraproject.org> - 34.7-2
- Add tweaks for RHEL 8 compatibility

* Sun Jul 18 2021 Neal Gompa <ngompa@fedoraproject.org> - 34.7-1
- kcm-about-distrorc: Drop Website setting and use os-release data instead

* Mon Jun 21 2021 Rex Dieter <rdieter@fedoraproject.org> - 34.6-1
- kdeglobals: Use double click to activate desktop icons by default (kdesig issue #17)

* Tue Apr 20 2021 Rex Dieter <rdieter@fedoraproject.org> - 34.5-1
- kdeglobals: disable user switching (#1929643)

* Thu Apr 15 2021 Rex Dieter <rdieter@fedoraproject.org> - 34.4-1
- drop deprecated/unused kde-profile/minimal
- kdeglobals: cleanup, drop [WM] section causing problems with color scheme

* Thu Apr 08 2021 Rex Dieter <rdieter@fedoraproject.org> - 34.2-1
- -plasma: explicitly use BreezeTwilight lookandfeel elements (#1947446)

* Mon Apr 05 2021 Rex Dieter <rdieter@fedoraproject.org> - 34.1-1
- 34.1
- -plasma: use Noto fonts

* Mon Apr 05 2021 Onuralp SEZER <thunderbirdtr@fedoraproject.org> - 34.0-10
- xdg/autostart removed and wallpaper test disabled for flatpak builds

* Sat Mar 06 2021 Rex Dieter <rdieter@fedoraproject.org> - 34.0-9
- drop ssh-agent.service, moved to openssh-clients (yay)

* Tue Mar 02 2021 Rex Dieter <rdieter@fedoraproject.org> - 34.0-8
- ssh-agent.service improvements

* Mon Mar 01 2021 Rex Dieter <rdieter@fedoraproject.org> - 34.0-7
- ssh-agent.service: drop After=plasma-core.target

* Mon Mar 01 2021 Rex Dieter <rdieter@fedoraproject.org> - 34.0-6
- ssh-agent.sh: only set SSH_AUTH_SOCK if not already

* Sun Feb 28 2021 Rex Dieter <rdieter@fedoraproject.org> - 34.0-5
- ssh-agent.service improvements

* Thu Feb 25 2021 Rex Dieter <rdieter@fedoraproject.org> - 34.0-4
- add ssh-agent.service (#1761817)

* Wed Feb 24 2021 Rex Dieter <rdieter@fedoraproject.org> - 34.0-3
- -plasma: +xdg-user-dirs-kde.desktop (#1932447)

* Fri Feb 12 2021 Neal Gompa <ngompa13@gmail.com> - 34.0-2
- Fix alsa dependency in pulseaudio subpackage

* Fri Feb 12 2021 Rex Dieter <rdieter@fedoraproject.org> - 34.0-1
- 34.0
- pagure.io upstream

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 33.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jan 04 2021 Rex Dieter <rdieter@fedoraproject.org> - 33.0-3
- -pulseaudio: Requires: pulseaudio-daemon

* Fri Oct 16 2020 Rex Dieter <rdieter@fedoraproject.org> - 33.0-2
- add 99-restart-dbus.sh plasma shutdown script, to forcefully restart user dbus (#1861700)

* Tue Sep 08 2020 Than Ngo <than@redhat.com> - 33-1
- bump for Fedora 33
- Fix background image (RHBZ #1872054)

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 32.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Mar 20 2020 Rex Dieter <rdieter@fedoraproject.org> - 32.2-1
- 32.2

* Thu Mar 19 2020 Rex Dieter <rdieter@fedoraproject.org> - 32.0-3
- provide /usr/share/wallpapers/Fedora symlink pointing to default wallpaper (#1812293)

* Tue Mar 10 2020 Adam Williamson <awilliam@redhat.com> - 32.0-2
- Update -plasma backgrounds dep to 32 (#1811160)

* Mon Mar 09 2020 Rex Dieter <rdieter@fedoraproject.org> - 32.0-1
- bump for fedora 32 (#1811160)

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 31.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Sep 10 2019 Adam Williamson <awilliam@redhat.com> - 31.0-1
- Bump for Fedora 31 (#1749086)

* Mon Aug 12 2019 Kevin Kofler <Kevin@tigcc.ticalc.org> 30.3-1
- Remove settings that call xdg-user-dir (no longer supported by KConfig)

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 30.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Jul 02 2019 Rex Dieter <rdieter@fedoraproject.org> - 30.2-1
- kde-mimeapps.list: remove ark duplicates

* Tue Jul 02 2019 Rex Dieter <rdieter@fedoraproject.org> - 30.1-1
- kde-mimeapps.list: use kf5 apps where available (#1726152)

* Thu Mar 14 2019 Rex Dieter <rdieter@fedoraproject.org> - 30.0-1
- 30.0 (#1688925)

* Thu Mar  7 2019 Tim Landscheidt <tim@tim-landscheidt.de> - 29.0-4
- Remove obsolete requirement for %%post scriptlet

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 29.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Sep 20 2018 Owen Taylor <otaylor@redhat.com> - 29.0-2
- Handle %%{_prefix} != /usr
- Fix double-listed files in %%{_datadir}/kde-settings/

* Thu Sep 13 2018 Rex Dieter <rdieter@fedoraproject.org> - 29.0-1
- 29.0

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 28.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Mar 12 2018 Rex Dieter <rdieter@fedoraproject.org> - 28.0-2
- -plasma: Requires: f28-backgrounds-kde

* Mon Mar 12 2018 Rex Dieter <rdieter@fedoraproject.org> - 28.0-1
- Update for Fedora 28

* Fri Feb 09 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 27-1.3
- Escape macros in %%changelog

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 27-1.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Oct 25 2017 Troy Dawson <tdawson@redhat.com> - 27-1.1
- Cleanup spec file conditionals

* Thu Sep 21 2017 Jan Grulich <jgrulich@redhat.com> - 27-1
- Properly update for Fedora 27 (updated tarball)

* Wed Sep 20 2017 Jan Grulich <jgrulich@redhat.com> - 26-1.2
- Update for Fedora 27

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 26-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Apr 20 2017 Rex Dieter <rdieter@fedoraproject.org> - 26-1
- init kde-settings-26

* Thu Apr 20 2017 Rex Dieter <rdieter@fedoraproject.org> - 25-6
- baloofilerc: drop explicit folders= key (use default set in kf5-baloo)

* Thu Mar 30 2017 Rex Dieter <rdieter@fedoraproject.org> - 25-5.1
- drop Requires: polkit-js-engine

* Mon Mar 27 2017 Adam Williamson <awilliam@redhat.com> - 25-5
- Patch another thing needed to get correct F26 theme

* Mon Mar 27 2017 Adam Williamson <awilliam@redhat.com> - 25-4
- Bump to F26 backgrounds

* Wed Mar 15 2017 Rex Dieter <rdieter@fedoraproject.org> - 25-3
- mimeapps: prefer plasma-discover (over apper)

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 25-2.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun Oct 09 2016 Rex Dieter <rdieter@fedoraproject.org> - 25-2
- init kde-settings-25

* Wed Jul 06 2016 Rex Dieter <rdieter@fedoraproject.org> - 24-7
- better start-here scriplet

* Tue Apr 19 2016 Rex Dieter <rdieter@fedoraproject.org> - 24-6
- drop 00-start-here-kde-fedora-2.js

* Wed Mar 30 2016 Rex Dieter <rdieter@fedoraproject.org> - 24-5
- plasmarc: Theme=F24
- drop remnants of -ksplash subpkg

* Tue Mar 29 2016 Rex Dieter <rdieter@fedoraproject.org> - 24-4
- drop -kdm (superceded by kdm-settings subpkg of kde-workspace)
- ksmserverrc: disable session management

* Tue Mar 29 2016 Rex Dieter <rdieter@fedoraproject.org> 24-3.2
- -kdm: Requires: s/redhat-logos/system-logos/

* Thu Mar 24 2016 Rex Dieter <rdieter@fedoraproject.org> 24-3.1
- omit qt-graphicssystem.* shell hacks (#1306524)

* Mon Mar 21 2016 Rex Dieter <rdieter@fedoraproject.org> - 24-3
- drop -minimal
- drop deprecated kde4 bits
- generic theming (for now)

* Sat Mar 12 2016 Rex Dieter <rdieter@fedoraproject.org> 24-1.3
- (re)enable -kdm (dropping needswork)

* Fri Mar 11 2016 Rex Dieter <rdieter@fedoraproject.org> 24-1.2
- drop -kdm, -ksplash

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 24-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sat Jan 30 2016 Rex Dieter <rdieter@fedoraproject.org> 24-1
- init v24, kde-mimeapps.list: adjust to kf5 versions of ark, dragon, gwenview

* Thu Jan 07 2016 Rex Dieter <rdieter@fedoraproject.org> 23-10
- revert prior commit, use prefix/plasma/shells/<package>/contents/updates instead

* Mon Nov 16 2015 Rex Dieter <rdieter@fedoraproject.org> 23-9
- copy plasma update scripts to canonical $XDG_DATA_DIRS/plasma/shells/<package>/contents/updates
  (needed when plasma-5.5 lands)

* Sun Nov 08 2015 Rex Dieter <rdieter@fedoraproject.org> 23-8
- add kcm-about-distrorc (#1279221)

* Thu Oct 08 2015 Rex Dieter <rdieter@fedoraproject.org> 23-7
- workaround lingering kuiserver processes (kde#348123)

* Tue Oct 06 2015 Rex Dieter <rdieter@fedoraproject.org> 23-6
- restore gtk3 scrolling workaround (#1226465)

* Sat Oct 03 2015 Rex Dieter <rdieter@fedoraproject.org> 23-5
- baloofilerc: index only well-known document-centric dirs by default (#1235026)

* Mon Sep 21 2015 Rex Dieter <rdieter@fedoraproject.org> - 23-4
- support XDG_CONFIG_DIR (/usr/share/kde-settings/kde-profile/default/xdg)
- kcminputrc,kdeglobals,plasmarc: explicitly set theming elements

* Tue Sep 01 2015 Rex Dieter <rdieter@fedoraproject.org> 23-3
- kde-mimeapps.list: s/kde-dolphin.desktop/org.kde.dolphin.desktop/

* Wed Aug 26 2015 Rex Dieter <rdieter@fedoraproject.org> 23-2
- kde-mimeapps.list: add calligra words,sheets,stage, fix text/plain

* Wed Aug 26 2015 Rex Dieter <rdieter@fedoraproject.org> 23-1
- init for f23

* Tue Jun 16 2015 Rex Dieter <rdieter@fedoraproject.org> - 22-11
- env: set GDK_CORE_DEVICE_EVENTS=1 to workaround gtk3 scrolling issues (#1226465)
- env: omit gpg-agent management, no longer needed (#1229918)

* Wed May 20 2015 Rex Dieter <rdieter@fedoraproject.org> 22-10
- qt-settings: /etc/xdg/QtProject/qtlogging.ini

* Wed May 20 2015 Rex Dieter <rdieter@fedoraproject.org> 22-9
- qt-settings: qtlogging.ini: disable *.debug logging

* Wed May 20 2015 Rex Dieter <rdieter@fedoraproject.org> 22-8
- kcminputrc: explicitly set breeze_cursors theme default (#1199521)

* Wed May 13 2015 Jan Grulich <jgrulich@redhat.com> - 22-7
- update kickoff icon from working location

* Wed May 13 2015 Jan Grulich <jgrulich@redhat.com> - 22-6
- use fedora icon in kickoff

* Wed Apr 22 2015 Rex Dieter <rdieter@fedoraproject.org> 22-4
- kdmrc: fix kdm theme #1214323)

* Wed Apr 15 2015 Rex Dieter <rdieter@fedoraproject.org> - 22-3.1
- -plasma: move plasmarc plasma-workspace/{env,shutdown} here
- omit kde4 ksplashrc, plasmarc

* Tue Mar 10 2015 Rex Dieter <rdieter@fedoraproject.org> 22-3
- plasmarc: F22 theme default

* Mon Mar 09 2015 Rex Dieter <rdieter@fedoraproject.org> 22-2.2
- s/-plasma-desktoptheme/-plasma-theme/ for consistency

* Thu Mar 05 2015 Rex Dieter <rdieter@fedoraproject.org> 22-2.1
- Conflicts: kf5-kdelibs4support < 5.7.0-3 (#1199108)

* Tue Mar 03 2015 Rex Dieter <rdieter@fedoraproject.org> - 22-2
- kdeburc: disable debug output
- kdeglobals: use Sans/Monospace fonts, breeze widgets/icons
- default gtk config to adwaita (replaces oxygen-gtk)

* Sun Feb 08 2015 Rex Dieter <rdieter@fedoraproject.org> 22-1.1
- %%config(noreplace) /etc/xdg/kdeglobals

* Sun Feb 08 2015 Rex Dieter <rdieter@fedoraproject.org> 22-1
- init for f22/plasma5, needs more love

* Thu Jan 01 2015 Rex Dieter <rdieter@fedoraproject.org> 21-2
- kwalletrc: empty most of [Wallet] section
- fixes problems on initial wallet creation with pam_kwallet (#1177991)

* Tue Sep 02 2014 Rex Dieter <rdieter@fedoraproject.org> 21-1
- branch for f21 (and new theming)

* Wed Aug 06 2014 Rex Dieter <rdieter@fedoraproject.org> 20-17
- add kf5/plasma5 support (/etc/xdg/plasma-workspace)

* Thu Jul 03 2014 Rex Dieter <rdieter@fedoraproject.org> 20-16
- QT_PLUGIN_PATH contains repeated paths (#1115268)

* Wed Jul 02 2014 Rex Dieter <rdieter@fedoraproject.org> 20-15
- kwalletrc: disable autoclose

* Mon Jun 30 2014 Rex Dieter <rdieter@fedoraproject.org> 20-14
- baloo default config: index only well-known dirs (#1114216)

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20-13.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May 01 2014 Rex Dieter <rdieter@fedoraproject.org> 20-13
- /etc/pam.d/kdm: pam-kwallet support

* Tue Nov 26 2013 Rex Dieter <rdieter@fedoraproject.org> 20-12
- kwalletrc: [Auto Allow] kdewallet=+KDE Daemon

* Tue Nov 26 2013 Rex Dieter <rdieter@fedoraproject.org> 20-11
- kwalletrc: whitelist/trust a few well-known trusted apps by default

* Tue Nov 26 2013 Rex Dieter <rdieter@fedoraproject.org> 20-10
- kwalletrc: +Silently Create Initial Wallet=true

* Mon Nov 25 2013 Rex Dieter <rdieter@fedoraproject.org> 20-9
- plasma4.req: fix bogus self-auto-Requires being generated for script engines

* Tue Nov 19 2013 Rex Dieter <rdieter@fedoraproject.org> 20-8
- cleanup/fix gpg-agent startup/shutdown

* Fri Nov 08 2013 Rex Dieter <rdieter@fedoraproject.org> 20-7
- kdmrc: ServerAttempts=2,ServerTimeout=60 (#967521)

* Thu Nov 07 2013 Rex Dieter <rdieter@fedoraproject.org> 20-6
- kmixrc: VolumeFeedback=true
- kdmrc: ConfigVersion 2.4
- gpg-agent isn't started automatically with KDE anymore (#845492)

* Mon Oct 14 2013 Rex Dieter <rdieter@fedoraproject.org> 20-4
- drop -sddm

* Sat Sep 21 2013 Rex Dieter <rdieter@fedoraproject.org> 20-3.1
- -sddm: add/fix %%description, *really* own /var/run/sddm

* Sat Sep 21 2013 Rex Dieter <rdieter@fedoraproject.org> 20-3
- -sddm: create/own /var/run/sddm (#1010590)

* Mon Sep 16 2013 Martin Briza <mbriza@redhat.com> - 20-2
- typo in system-kde-theme version

* Mon Sep 16 2013 Martin Briza <mbriza@redhat.com> - 20-2
- sddm subpackage - added the config containing the Heisenbug artwork

* Tue Sep 10 2013 Jaroslav Reznik <jreznik@fedoraproject.org> - 20-1
- reset Version to match target fedora release (20)
- default to Heisenbug artwork

* Mon Jul 29 2013 Martin Briza <mbriza@redhat.com> - 19-23.1
- Fixed a typo in systemd_preun (#989145)

* Fri May 31 2013 Martin Briza <mbriza@redhat.com> - 19-23
- remove Console login menu option from KDM (#966095)

* Wed May 22 2013 Than Ngo <than@redhat.com> - 19-22
- disable java by default

* Tue May 21 2013 Rex Dieter <rdieter@fedoraproject.org> 19-21
- cleanup systemd macros
- kde-settings-kdm is misusing preset files (#963898)
- prune %%changelog

* Mon May 13 2013 Rex Dieter <rdieter@fedoraproject.org> 19-20
- plymouth-quit-wait service fails resulting in very long boot time (#921785)

* Wed Apr 24 2013 Martin Briza <mbriza@redhat.com> 19-19
- Return to the usual X server invocation in case there's no systemd provided wrapper

* Wed Apr 24 2013 Daniel Vrátil <dvratil@redhat.com> 19-18
- remove Mugshot from Konqueror bookmarks (#951279)

* Mon Apr 15 2013 Martin Briza <mbriza@redhat.com> 19-17.2
- so depending on /lib/systemd/systemd-multi-seat-x is considered a broken dependency - kdm depends on systemd instead

* Sat Apr 13 2013 Rex Dieter <rdieter@fedoraproject.org> 19-17.1
- use %%_tmpfilesdir macro

* Thu Apr 11 2013 Martin Briza <mbriza@redhat.com> 19-17
- Use /lib/systemd/systemd-multi-seat-x as the X server in KDM

* Wed Apr 03 2013 Martin Briza <mbriza@redhat.com> 19-16
- Fedora release number was wrong in /etc/kde/kdm/kdmrc

* Wed Apr 03 2013 Martin Briza <mbriza@redhat.com> 19-15
- Fixed KDM theme name in /etc

* Thu Mar 28 2013 Martin Briza <mbriza@redhat.com> 19-14
- Changed the strings in the settings to Schrödinger's Cat instead of Spherical Cow

* Mon Feb 04 2013 Kevin Kofler <Kevin@tigcc.ticalc.org> 19-13.1
- Requires: polkit-js-engine

* Mon Jan 28 2013 Rex Dieter <rdieter@fedoraproject.org> 19-13
- +fedora-kde-display-handler kconf_update script

* Wed Dec 05 2012 Rex Dieter <rdieter@fedoraproject.org> 19-12
- plasma4.req: be more careful wrt IFS

* Tue Dec 04 2012 Rex Dieter <rdieter@fedoraproject.org> 19-11
- plasma4.req: allow for > 1 scriptengine

* Tue Nov 27 2012 Dan Vratil <dvratil@redhat.com> 19-10
- provide kwin rules to fix maximization of some Gtk2 apps

* Sun Nov 11 2012 Rex Dieter <rdieter@fedoraproject.org> 19-9.1
- fixup kdmrc for upgraders who had UserAuthDir=/var/run/kdm

* Thu Nov 08 2012 Rex Dieter <rdieter@fedoraproject.org> 19-9
- tighten permissions on /var/run/kdm
- support /var/run/xdmctl

* Fri Oct 12 2012 Kevin Kofler <Kevin@tigcc.ticalc.org> 19-8
- kslideshow.kssrc: use xdg-user-dir instead of hardcoding $HOME/Pictures

* Fri Oct 12 2012 Kevin Kofler <Kevin@tigcc.ticalc.org> 19-7
- port 11-fedora-kde-policy from old pkla format to new polkit-1 rules (#829881)
- nepomukstrigirc: index translated xdg-user-dirs (dvratil, #861129)

* Thu Sep 27 2012 Dan Vratil <dvratil@redhat.com> 19-5
- fix indexing paths in nepomukstrigirc (#861129)

* Mon Sep 24 2012 Rex Dieter <rdieter@fedoraproject.org> 19-4
- -minimal subpkg

* Tue Sep 04 2012 Dan Vratil <dvratil@redhat.com> 19-3
- add 81-fedora-kdm-preset (#850775)
- start kdm.service after livesys-late.service

* Wed Aug 29 2012 Rex Dieter <rdieter@fedoraproject.org> - 19-1
- reset Version to match target fedora release (19)
- kdm.pam: pam_gnome_keyring.so should be loaded after pam_systemd.so (#852723)

* Tue Aug 21 2012 Martin Briza <mbriza@redhat.com> 4.9-5
- Change strings to Fedora 18 (Spherical Cow)
- bump system_kde_theme_ver to 17.91

* Sat Aug 11 2012 Rex Dieter <rdieter@fedoraproject.org> 4.9-2.1
- -kdm: drop old stuff, fix systemd scriptlets

* Thu Aug 09 2012 Rex Dieter <rdieter@fedoraproject.org> 4.9-2
- /etc/pam.d/kdm missing: -session optional pam_ck_connector.so (#847114)

* Wed Aug 08 2012 Rex Dieter <rdieter@fedoraproject.org> - 4.9-1
- adapt kdm for display manager rework feature (#846145)

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.8-16.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 29 2012 Rex Dieter <rdieter@fedoraproject.org> 4.8-16
- qt-graphicssystem.csh: fix typo s|/usr/bin/lspci|/usr/sbin/lspci| (#827440)

* Wed Jun 13 2012 Rex Dieter <rdieter@fedoraproject.org> 4.8-15.1
- kde-settings-kdm conflicts with gdm (#819254)

* Wed Jun 13 2012 Rex Dieter <rdieter@fedoraproject.org> 4.8-15
- qt-settings does NOT fully quallify path to lspci in /etc/profile.d/qt-graphicssystem.{csh,sh} (#827440)

* Fri May 25 2012 Than Ngo <than@redhat.com> - 4.8-14.1
- rhel/fedora condtion

* Wed May 16 2012 Rex Dieter <rdieter@fedoraproject.org> 4.8-14
- Pure Qt applications can't use KDE styles outside of KDE (#821062)

* Tue May 15 2012 Rex Dieter <rdieter@fedoraproject.org> 4.8-13
- kdmrc: GUIStyle=Plastique (#810161)

* Mon May 14 2012 Rex Dieter <rdieter@fedoraproject.org> 4.8-12
- drop hack/workaround for bug #750423
- move /etc/tmpfiles.d => /usr/lib/tmpfiles.d

* Thu May 10 2012 Rex Dieter <rdieter@fedoraproject.org> 4.8-10
- +qt-settings: move cirrus workaround(s) here (#810161)

* Wed May 09 2012 Than Ngo <than@redhat.com> - 4.8-8.2
- fix rhel condition

* Tue May 08 2012 Than Ngo <than@redhat.com> - 4.8-8.1
- add workaround for cirrus

* Mon Apr 30 2012 Rex Dieter <rdieter@fedoraproject.org> 4.8-8
- fix application/x-rpm mimetype defaults

* Wed Apr 18 2012 Than Ngo <than@redhat.com> - 4.8-7.1
- add rhel condition

* Mon Mar 19 2012 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.8-7
- plasma4.prov: change spaces in runner names to underscores

* Tue Feb 28 2012 Rex Dieter <rdieter@fedoraproject.org> 4.8-6
- kslideshow.kssrc: include some sane/working defaults

* Tue Feb 14 2012 Jaroslav Reznik <jreznik@redhat.com> 4.8-5
- fix plasmarc Beefy Miracle reference

* Tue Feb 14 2012 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.8-4
- kdmrc: GreetString=Fedora 17 (Beefy Miracle)
- kdmrc, ksplashrc, plasmarc: s/Verne/BeefyMiracle/g (for the artwork themes)
- bump system_kde_theme_ver to 16.91

* Mon Jan 16 2012 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.8-3
- merge the plasma-rpm tarball into the SVN trunk and thus the main tarball

* Mon Jan 16 2012 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.8-2
- allow org.kde.kcontrol.kcmclock.save without password for wheel again
- Requires: polkit (instead of polkit-desktop-policy)

* Mon Jan 16 2012 Rex Dieter <rdieter@fedoraproject.org> 4.8-1
- kwinrc: drop [Compositing] Enabled=false

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.7-14.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Nov 19 2011 Rex Dieter <rdieter@fedoraproject.org> 4.7-14
- add explicit apper defaults
- add script to init $XDG_DATA_HOME (to workaround bug #750423)

* Mon Oct 31 2011 Rex Dieter <rdieter@fedoraproject.org> 4.7-13.4
- make new-subpkgs Requires: %%name for added safety

* Mon Oct 31 2011 Rex Dieter <rdieter@fedoraproject.org> 4.7-13.3
- -ksplash: Requires: system-ksplash-theme >= 15.90
- -plasma: Requires: system-plasma-desktoptheme >= 15.90

* Mon Oct 31 2011 Rex Dieter <rdieter@fedoraproject.org> 4.7-13.2
- -kdm: Requires: system-kdm-theme >= 15.90

* Mon Oct 31 2011 Rex Dieter <rdieter@fedoraproject.org> 4.7-13.1
- -kdm: Requires: verne-kdm-theme (#651305)

* Fri Oct 21 2011 Rex Dieter <rdieter@fedoraproject.org> 4.7-13
- s/kpackagekit/apper/ configs
- drop gpg-agent scripts (autostarts on demand now)

* Sat Oct 15 2011 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.7-12
- disable the default Plasma digital-clock's displayEvents option by default

* Wed Oct 12 2011 Rex Dieter <rdieter@fedoraproject.org> 4.7-11
- krunnerrc: org.kde.events_runnerEnabled=false
- follow Packaging:Tmpfiles.d guildelines

* Wed Oct 05 2011 Rex Dieter <rdieter@fedoraproject.org> 4.7-10
- don't spam syslog if pam-gnome-keyring is not present (#743044)

* Fri Sep 30 2011 Rex Dieter <rdieter@fedoraproject.org> 4.7-9
- -kdm: add explicit Requires: xorg-x11-xinit

* Tue Sep 27 2011 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.7-8
- plasma4.prov: don't trust the Name of script engines, always use the API

* Thu Sep 22 2011 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.7-7
- ship the Plasma RPM dependency generators only on F17+
- use xz tarball
- don't rm Makefile, no longer in the tarball
- set up a folder view on the desktop by default for new users (#740676)
- kdmrc: set MinShowUID=-1 (use /etc/login.defs) instead of 500 (#717115)
- -kdm: Requires: kdm >= 4.7.1-2 (required for MinShowUID=-1)

* Wed Aug 31 2011 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.7-6
- put under the MIT license as agreed with the other contributors

* Sun Aug 21 2011 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.7-5
- fix the RPM dependency generators to also accept ServiceTypes= (#732271)

* Sun Aug 21 2011 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.7-4
- add the RPM dependency generators for Plasma (GSoC 2011), as Source1 for now

* Tue Aug 02 2011 Jaroslav Reznik <jreznik@redhat.com> 4.7-3
- update to Verne theming/branding

* Wed Jul 13 2011 Rex Dieter <rdieter@fedoraproject.org> 4.7-2
- kmixrc: [Global] startkdeRestore=false

* Thu Mar 24 2011 Rex Dieter <rdieter@fedoraproject.org> 4.6-10
- konq webbrowsing profile: start.fedoraproject.org
- konq tabbedbrowsing : start.fedoraproject.org, fedoraproject.org/wiki/KDE

* Tue Mar 22 2011 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.6-9
- Requires: polkit-desktop-policy

* Thu Mar 10 2011 Rex Dieter <rdieter@fedoraproject.org> 4.6-8
- s/QtCurve/oxygen-gtk/

* Mon Mar 07 2011 Rex Dieter <rdieter@fedoraproject.org> 4.6-7
- use adwaita-cursor-theme

* Mon Mar 07 2011 Rex Dieter <rdieter@fedoraproject.org> 4.6-6
- use lovelock-kdm-theme
- /var/log/kdm.log is never clean up (logrotate) (#682761)
- -kdm, move xterm dep to comps (#491251)

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.6-4.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Feb 07 2011 Rex Dieter <rdieter@fedoraproject.org> 4.6-4
- de-Laughlin-ize theming, be genericish/upstream (for now)
- kcminputrc: theme=dmz-aa, Requires: dmz-cursor-themes (#675509)

* Tue Feb 01 2011 Rex Dieter <rdieter@fedoraproject.org> 4.6-3
- add support for the postlogin PAM stack to kdm (#665060)

* Wed Dec 08 2010 Rex Dieter <rdieter@fedoraproject.org> 4.6-2.1
- %%post kdm : sed -e 's|-nr|-background none|' kdmrc (#659684)
- %%post kdm : drop old stuff

* Fri Dec 03 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.6-2
- drop old Conflicts
- Xserver-1.10: Fatal server error: Unrecognized option: -nr (#659684)

* Mon Nov 29 2010 Rex Dieter <rdieter@fedoraproject.org> 4.6-1
- init 4.6
- /var/run/kdm/ fails to be created on boot (#657785)

* Thu Nov 11 2010 Rex Dieter <rdieter@fedoraproject.org> 4.5-11
- kdebugrc: DisableAll=true (#652367)

* Fri Oct 29 2010 Rex Dieter <rdieter@fedoraproject.org> 4.5-10
- kdmrc: UserList=false

* Thu Oct 14 2010 Rex Dieter <rdieter@fedoraproject.org> 4.5-9
- drop plasma-{desktop,netbook}-appletsrc
- plasmarc: set default plasma(-netbook) themes (#642763)

* Sat Oct 09 2010 Rex Dieter <rdieter@fedoraproject.org> 4.5-8
- rename 00-start-here script to ensure it runs (again).

* Fri Oct 08 2010 Rex Dieter <rdieter@fedoraproject.org> 4.5-7
- make 00-start-here-kde-fedora.js look for simplelauncher too (#615621)

* Tue Sep 28 2010 Rex Dieter <rdieter@fedoraproject.org> 4.5-6
- move plasma-desktop bits into kde-settings/kde-profile instead

* Tue Sep 28 2010 Rex Dieter <rdieter@fedoraproject.org> 4.5-5
- 00-start-here-kde-fedora.js plasma updates script (#615621)

* Fri Sep 03 2010 Rex Dieter <rdieter@fedoraproject.org> 4.5-4
- kdeglobals : drop [Icons] Theme=Fedora-KDE (#615621)

* Tue Aug 03 2010 Jaroslav Reznik <jreznik@redhat.com> 4.5-3
- laughlin kde theme as default

* Mon Apr 26 2010 Rex Dieter <rdieter@fedoraproject.org> 4.5-2
- kde-settings-kdm depends on xorg-x11-xdm (#537608)

* Tue Apr 13 2010 Rex Dieter <rdieter@fedoraproject.org> 4.5-1.1
- -kdm: own /var/spool/gdm (#551310,#577482)

* Tue Feb 23 2010 Rex Dieter <rdieter@fedoraproject.org> 4.5-1
- 4.5 branch for F-14
- (re)enable kdebug

* Tue Feb 23 2010 Rex Dieter <rdieter@fedoraproject.org> 4.4-13
- disable kdebug by default (#560508)

* Mon Feb 22 2010 Jaroslav Reznik <jreznik@redhat.com> 4.4-12
- added dist tag to release

* Mon Feb 22 2010 Jaroslav Reznik <jreznik@redhat.com> 4.4-11
- goddard kde theme as default

* Sat Jan 30 2010 Rex Dieter <rdieter@fedoraproject.org> 4.4-10
- move /etc/kde/kdm/backgroundrc => /var/lib/kdm/backgroundrc (#522513)
- own /var/lib/kdm (regression, #442081)

* Fri Jan 29 2010 Rex Dieter <rdieter@fedoraproject.org> 4.4-9
- krunnerrc: disable nepomuksearch plugin by default (#559977)

* Wed Jan 20 2010 Rex Dieter <rdieter@fedoraproject.org> 4.4-8
- plasma-netbook workspace has no wallpaper configured (#549996)

* Tue Jan 05 2010 Rex Dieter <rdieter@fedoraproject.org> 4.4-7
- externalize fedora-kde-icon-theme (#547701)

* Wed Dec 30 2009 Rex Dieter <rdieter@fedoraproject.org> 4.4-6.1
- -kdm: Requires: kdm

* Fri Dec 25 2009 Rex Dieter <rdieter@fedoraproject.org> 4.4-6
- use qtcurve-gtk2 by default (#547700)

* Wed Dec 23 2009 Rex Dieter <rdieter@fedoraproject.org> 4.4-4
- enable nepomuk, with some conservative defaults (#549436)

* Tue Dec 01 2009 Rex Dieter <rdieter@fedoraproject.org> 4.4-3
- kdmrc: ServerArgsLocal=-nr , for better transition from plymouth

* Tue Dec 01 2009 Rex Dieter <rdieter@fedoraproject.org> 4.4-2
- kdmrc: revert to ServerVTs=-1 (#475890)

* Sun Nov 29 2009 Rex Dieter <rdieter@fedoraproject.org> 4.4-1
- -pulseaudio: drop xine-lib-pulseaudio (subpkg no longer exists)
