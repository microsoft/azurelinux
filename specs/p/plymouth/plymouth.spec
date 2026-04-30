## START: Set by rpmautospec
## (rpmautospec version 0.8.3)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 25;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Summary: Graphical Boot Animation and Logger
Name: plymouth
Version: 24.004.60
Release: %autorelease
License: GPL-2.0-or-later
URL: http://www.freedesktop.org/wiki/Software/Plymouth

Source0: https://gitlab.freedesktop.org/plymouth/plymouth/-/archive/%{version}/%{name}-%{version}.tar.bz2
# Spinner update from: https://gitlab.freedesktop.org/plymouth/plymouth/-/commit/1a01883fa2659bfb5e7417e1d5bd8d287a2cac36
# Drop this on next rebase to latest upstream
Source1: spinner-update.tar.gz
Source2: charge.plymouth

# Revert https://gitlab.freedesktop.org/plymouth/plymouth/-/commit/48881ba
# to fix console display on minimal installs
# https://bugzilla.redhat.com/show_bug.cgi?id=2269385
# This bug should also be fixed by:
# https://gitlab.freedesktop.org/plymouth/plymouth/-/commit/d2ab367e12423646d3a6bb35d16570f8e3126234
# https://gitlab.freedesktop.org/plymouth/plymouth/-/commit/1e206268df99d28e9fb3d3cf8379a553abb05af0
# Drop this Fedora patch on next rebase to latest upstream
Patch: 0001-Revert-src-Hide-console-text-when-splash-is-requeste.patch

# https://gitlab.freedesktop.org/plymouth/plymouth/-/commit/10ac8d2dc927b112ce6aeb06bc73d9c46550954c
# Fix encryption passphrase appearing in plain text in text mode
# https://bugzilla.redhat.com/show_bug.cgi?id=2271337
Patch: 0001-ply-boot-splash-Set-unbuffered-input-when-creating-a.patch

# Revert patch to immediately switch to text mode on first renderer plugin error
# Fixes unwanted text mode when drm-plugin init races with simpledrm unregistration
# https://gitlab.freedesktop.org/plymouth/plymouth/-/merge_requests/319 (merged)
# https://bugzilla.redhat.com/show_bug.cgi?id=2270030
Patch: 0001-ply-device-manager-Revert-Fall-back-to-text-plugin-i.patch

# Probe simpledrm immediately instead of waiting for udev_device_get_is_initialized ()
# to return true. This fixes users getting the text splash on laptops with somewhat
# slower CPUs combined with loading the amdgpu module which may take 7+ seconds
# https://gitlab.freedesktop.org/plymouth/plymouth/-/merge_requests/323/ (merged)
# https://bugzilla.redhat.com/show_bug.cgi?id=2183743
# https://bugzilla.redhat.com/show_bug.cgi?id=2274770
Patch: plymouth-24.004.60-immediately-probe-simpledrm.patch

# Backport of upstream commit 709f21e80199ee51badff2d9b5dc6bae8af2a1a1
# "renderers: Do not assume all keyboards have LEDs"
# This fixes:
# https://bugzilla.redhat.com/show_bug.cgi?id=2282384
Patch: 0001-renderers-Do-not-assume-all-keyboards-have-LEDs.patch

# Fix Dvorak layout icon not showing when the evdev keyboard driver is used
# https://gitlab.freedesktop.org/plymouth/plymouth/-/merge_requests/341 (merged)
# https://bugzilla.redhat.com/show_bug.cgi?id=2341810
Patch: 0001-ply-keymap-icon-Make-Dvorak-check-case-insensitive.patch
# And a generic fix for missing pre-rendered keyboard-layout texts
# https://gitlab.freedesktop.org/plymouth/plymouth/-/merge_requests/358
Patch: 0001-ply-keymap-icon-Fix-falling-back-to-label-plugin-whe.patch

# https://gitlab.freedesktop.org/plymouth/plymouth/-/commit/792fe7474a02a1facacdd52e0dcf9053da4b1f6e
# Fix for the label plugin not finding fonts
Patch: 0001-label-freetype-fix-fallback-not-working-when-fc-matc.patch

# 2 tweaks for hidpi scale factor calculations
# https://gitlab.freedesktop.org/plymouth/plymouth/-/commit/acf97c73670b80a65329aaa35e40438d86fca3c6
# https://gitlab.freedesktop.org/plymouth/plymouth/-/commit/3b8e918479f47a845d4f88d281f7dfe412195628
Patch: plymouth-24.004.60-device-scale-fixes.patch

# A set of 5 patches to make use-simpledrm configurable from the config file
# https://gitlab.freedesktop.org/plymouth/plymouth/-/merge_requests/342
# https://bugzilla.redhat.com/show_bug.cgi?id=2346150
Patch: plymouth-24.004.60-use_simpledrm-config.patch

# Backport upstream fix for crash when using 2 GPUs with displays attached and
# using evdev input support (XKBLAYOUT set in /etc/vconsole.conf)
# https://gitlab.freedesktop.org/plymouth/plymouth/-/commit/d20b1be527817c21500c3daa4dfdd0e9c7c731b8
# https://bugzilla.redhat.com/show_bug.cgi?id=2368186
Patch: 0001-drm-Check-for-NULL-terminal-in-watch_input_device.patch

# Fix a crash caused by calling ply_event_loop_watch_fd () with a -1 fd
# https://gitlab.freedesktop.org/plymouth/plymouth/-/merge_requests/354
# https://bugzilla.redhat.com/show_bug.cgi?id=2370979
Patch: 0001-drm-Fix-crash-when-terminal-fd-is-still-1-after-reco.patch

# Don't use simpledrm together with LUKS, see commit message for details
# https://gitlab.freedesktop.org/plymouth/plymouth/-/merge_requests/355
# https://bugzilla.redhat.com/show_bug.cgi?id=2359283
Patch: 0001-Add-UseSimpledrmNoLuks-config-file-keyword.patch

# Fix Disk unlock screen keymap and capslock icons not shown on monitor on second GPU
# https://gitlab.freedesktop.org/plymouth/plymouth/-/merge_requests/356
# https://bugzilla.redhat.com/show_bug.cgi?id=2375854
Patch: 0001-Fix-keymap-and-capslock-icon-on-displays-on-second-G.patch

# Make the prompt below the diskunlock password entry box look a bit better
# https://gitlab.freedesktop.org/plymouth/plymouth/-/merge_requests/357
# https://gitlab.freedesktop.org/plymouth/plymouth/-/issues/294
# https://bugzilla.redhat.com/show_bug.cgi?id=2356893
Patch: 0001-two-step-Remove-at-the-end-of-passphrase-prompt-belo.patch
Patch: 0002-two-step-Add-some-padding-between-text-entry-field-a.patch

# Patches from upstream to fix messages being logged twice on serial consoles
Patch: 0001-utils-Don-t-lose-log-level-when-silencing-kmsg.patch
Patch: 0002-details-Suppress-kernel-s-own-kmsg-console-output.patch
Patch: 0003-kmsg-reader-Seek-to-the-end-of-the-ringbuffer.patch

# Fix crash in drm plugin close_input_source() rhbz#2416551
# https://gitlab.freedesktop.org/plymouth/plymouth/-/commit/5c10072a978dd7566559f44a54c3e031bb4cb216
Patch: 0001-renderers-Only-call-ply_terminal_set_unbuffered_inpu.patch

# Fix wrong KBD layout when a user has configured multiple layouts rhbz#2416197
# https://gitlab.freedesktop.org/plymouth/plymouth/-/commit/b609687e8d15b23aaa39100221b62d37b5859011
Patch: 0001-Display-the-first-specified-XKBLAYOUT-as-the-active-.patch

# Fix race in fb_device_has_drm_device () causing frame-buffer plugin to
# sometimes load while drm plugin is already handling the display
Patch: 0001-ply-device-manager-Fix-race-in-fb_device_has_drm_dev.patch

# https://gitlab.freedesktop.org/plymouth/plymouth/-/issues/321
# https://bugzilla.redhat.com/show_bug.cgi?id=2433079
# https://gitlab.freedesktop.org/plymouth/plymouth/-/commit/45655f12fa2d5553ab4ba509f2e203c249191664
Patch: 0001-ply-keyboard-Fix-hang-on-read-of-incomplete-terminal.patch

BuildRequires: meson
BuildRequires: system-logos
BuildRequires: gcc libtool git
BuildRequires: pkgconfig(libdrm)
BuildRequires: pkgconfig(libevdev)
BuildRequires: pkgconfig(libudev)
BuildRequires: pkgconfig(xkeyboard-config)
BuildRequires: kernel-headers
BuildRequires: libpng-devel
BuildRequires: libxslt, docbook-style-xsl
BuildRequires: pkgconfig(gtk+-3.0)
BuildRequires: pango-devel >= 1.21.0
BuildRequires: cairo-devel
BuildRequires: gettext-devel
# for /usr/bin/systemd-tty-ask-password-agent
BuildRequires: systemd
# for _unitdir macro
BuildRequires: systemd-rpm-macros

Requires: %{name}-core-libs = %{version}-%{release}
Requires: %{name}-scripts = %{version}-%{release}
# For keyboard layouts
Requires: xkeyboard-config
Suggests: logrotate

%description
Plymouth provides an attractive graphical boot animation in
place of the text messages that normally get shown.  Text
messages are instead redirected to a log file for viewing
after boot.


%package system-theme
Summary: Plymouth default theme
Requires: plymouth(system-theme) = %{version}-%{release}

%description system-theme
This meta-package tracks the current distribution default theme.


%package core-libs
Summary: Plymouth core libraries

%description core-libs
This package contains the core libraries used by Plymouth.


%package graphics-libs
Summary: Plymouth graphics libraries
Requires: %{name}-core-libs = %{version}-%{release}
Requires: system-logos

%description graphics-libs
This package contains the libraries used by graphical Plymouth splashes.


%package devel
Summary: Libraries and headers for writing Plymouth splash plugins
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig

%description devel
This package contains the libraries and headers needed to develop
3rd party splash plugins for Plymouth.


%package scripts
Summary: Plymouth related scripts
Requires: findutils, coreutils, gzip, cpio, dracut
Requires: xkeyboard-config
Requires: %{name} = %{version}-%{release}

%description scripts
This package contains scripts that help integrate Plymouth with
the system.


%package plugin-label
Summary: Plymouth label plugin
Requires: %{name} = %{version}-%{release}
Requires: %{name}-graphics-libs = %{version}-%{release}

%description plugin-label
This package contains the label control plugin for Plymouth.
It provides the ability to render text on graphical boot splashes.


%package plugin-script
Summary: Plymouth "script" plugin
Requires: %{name} = %{version}-%{release}
Requires: %{name}-graphics-libs = %{version}-%{release}

%description plugin-script
This package contains the "script" boot splash plugin for
Plymouth. It features an extensible boot splash language that
allows writing new plugins as scripts, simplifying the process
of designing custom boot splash themes.


%package plugin-fade-throbber
Summary: Plymouth "Fade-Throbber" plugin
Requires: %{name} = %{version}-%{release}
Requires: %{name}-graphics-libs = %{version}-%{release}

%description plugin-fade-throbber
This package contains the "Fade-In" boot splash plugin for
Plymouth. It features a centered image that fades in and out
while other images pulsate around during system boot up.


%package plugin-space-flares
Summary: Plymouth "space-flares" plugin
Requires: %{name} = %{version}-%{release}
Requires: %{name}-graphics-libs = %{version}-%{release}
Requires: plymouth-plugin-label = %{version}-%{release}

%description plugin-space-flares
This package contains the "space-flares" boot splash plugin for
Plymouth. It features a corner image with animated flares.


%package plugin-two-step
Summary: Plymouth "two-step" plugin
Requires: %{name} = %{version}-%{release}
Requires: %{name}-graphics-libs = %{version}-%{release}
Requires: plymouth-plugin-label = %{version}-%{release}
# Spinifinity like themes should now use two-step instead of throbgress
# No provides, the throbgress plugin has been removed upstream
Obsoletes: %{name}-plugin-throbgress < %{version}-%{release}

%description plugin-two-step
This package contains the "two-step" boot splash plugin for
Plymouth. It features a two phased boot process that starts with
a progressing animation synced to boot time and finishes with a
short, fast one-shot animation.

# Don't build charge theme in ELN/RHEL as it's Fedora specific
%if ! 0%{?rhel}
%package theme-charge
Summary: Plymouth "Charge" plugin
Requires: %{name}-plugin-two-step = %{version}-%{release}
Requires: fedora-logos-classic
Requires(post): plymouth-scripts

%description theme-charge
This package contains the "charge" boot splash theme for
Plymouth. It features the shadowy hull of a Fedora logo charge up and
and finally burst into full form.
%endif

%package theme-fade-in
Summary: Plymouth "Fade-In" theme
Requires: %{name}-plugin-fade-throbber = %{version}-%{release}
Requires(post): plymouth-scripts

%description theme-fade-in
This package contains the "Fade-In" boot splash theme for
Plymouth. It features a centered logo that fades in and out
while stars twinkle around the logo during system boot up.


%package theme-script
Summary: Plymouth "Script" plugin
Requires: %{name}-plugin-script = %{version}-%{release}
Requires(post): plymouth-scripts

%description theme-script
This package contains the "script" boot splash theme for
Plymouth. It it is a simple example theme the uses the "script"
plugin.


%package theme-solar
Summary: Plymouth "Solar" theme
Requires: %{name}-plugin-space-flares = %{version}-%{release}
Requires(post): plymouth-scripts

%description theme-solar
This package contains the "Solar" boot splash theme for
Plymouth. It features a blue flamed sun with animated solar flares.


%package theme-spinfinity
Summary: Plymouth "Spinfinity" theme
Requires: %{name}-plugin-two-step = %{version}-%{release}
Requires(post): plymouth-scripts

%description theme-spinfinity
This package contains the "Spinfinity" boot splash theme for
Plymouth. It features a centered logo and animated spinner that
spins in the shape of an infinity sign.


%package theme-spinner
Summary: Plymouth "Spinner" theme
Requires: %{name}-plugin-two-step = %{version}-%{release}
%if 0%{?rhel} > 9
Requires: redhat-mono-vf-fonts
Requires: redhat-text-vf-fonts
%else
Requires: font(cantarell) font(cantarelllight)
%endif
Requires(post): plymouth-scripts
Provides: plymouth(system-theme) = %{version}-%{release}

%description theme-spinner
This package contains the "spinner" boot splash theme for
Plymouth. It features a small spinner on a dark background.


%prep
%autosetup -p1 -a 1
# Change the default theme
sed -i -e 's/spinner/bgrt/g' src/plymouthd.defaults
# Use simpledrm /dev/dri/card# by default, except when LUKS disk encrpytion is used
echo UseSimpledrmNoLuks=1 >> src/plymouthd.defaults

%if 0%{?rhel} > 9
find -type f -exec sed -i -e 's/Cantarell/Red Hat Text/g' {} \;
%endif

%build
%meson -Dtracing=true  \
       -Dlogo=%{_datadir}/pixmaps/system-logo-white.png \
       -Dbackground-start-color-stop=0x0073B3           \
       -Dbackground-end-color-stop=0x00457E             \
       -Dbackground-color=0x3391cd
%meson_build

%install
%meson_install

%find_lang %{name}
find $RPM_BUILD_ROOT -name '*.la' -delete

mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/lib/plymouth

%if ! 0%{?rhel}
# Add charge, our old default
mkdir -p $RPM_BUILD_ROOT%{_datadir}/plymouth/themes/charge
cp %{SOURCE2} $RPM_BUILD_ROOT%{_datadir}/plymouth/themes/charge
cp $RPM_BUILD_ROOT%{_datadir}/plymouth/themes/glow/{box,bullet,entry,lock}.png $RPM_BUILD_ROOT%{_datadir}/plymouth/themes/charge
%endif

# Drop glow, it's not very Fedora-y
rm -rf $RPM_BUILD_ROOT%{_datadir}/plymouth/themes/glow


%ldconfig_scriptlets core-libs

%ldconfig_scriptlets graphics-libs

%if ! 0%{?rhel}
%postun theme-charge
export PLYMOUTH_PLUGIN_PATH=%{_libdir}/plymouth/
if [ $1 -eq 0 ]; then
    if [ "$(%{_sbindir}/plymouth-set-default-theme)" == "charge" ]; then
        %{_sbindir}/plymouth-set-default-theme --reset
    fi
fi
%endif

%postun theme-fade-in
export PLYMOUTH_PLUGIN_PATH=%{_libdir}/plymouth/
if [ $1 -eq 0 ]; then
    if [ "$(%{_sbindir}/plymouth-set-default-theme)" == "fade-in" ]; then
        %{_sbindir}/plymouth-set-default-theme --reset
    fi
fi

%postun theme-solar
export PLYMOUTH_PLUGIN_PATH=%{_libdir}/plymouth/
if [ $1 -eq 0 ]; then
    if [ "$(%{_sbindir}/plymouth-set-default-theme)" == "solar" ]; then
        %{_sbindir}/plymouth-set-default-theme --reset
    fi
fi

%postun theme-spinfinity
export PLYMOUTH_PLUGIN_PATH=%{_libdir}/plymouth/
if [ $1 -eq 0 ]; then
    if [ "$(%{_sbindir}/plymouth-set-default-theme)" == "spinfinity" ]; then
        %{_sbindir}/plymouth-set-default-theme --reset
    fi
fi

%post theme-spinner
export PLYMOUTH_PLUGIN_PATH=%{_libdir}/plymouth/
# On upgrades replace charge with the new bgrt default
if [ $1 -eq 2 ]; then
    if [ "$(%{_sbindir}/plymouth-set-default-theme)" == "charge" ]; then
        %{_sbindir}/plymouth-set-default-theme bgrt
    fi
fi

%postun theme-spinner
export PLYMOUTH_PLUGIN_PATH=%{_libdir}/plymouth/
if [ $1 -eq 0 ]; then
    if [ "$(%{_sbindir}/plymouth-set-default-theme)" == "bgrt" -o \
         "$(%{_sbindir}/plymouth-set-default-theme)" == "spinner" ]; then
        %{_sbindir}/plymouth-set-default-theme --reset
    fi
fi


%files -f %{name}.lang
%license COPYING
%doc AUTHORS README.md
%dir %{_datadir}/plymouth
%dir %{_datadir}/plymouth/themes
%dir %{_datadir}/plymouth/themes/details
%dir %{_datadir}/plymouth/themes/text
%dir %{_datadir}/plymouth/themes/tribar
%dir %{_libexecdir}/plymouth
%dir %{_localstatedir}/lib/plymouth
%dir %{_libdir}/plymouth/renderers
%dir %{_sysconfdir}/plymouth
%config(noreplace) %{_sysconfdir}/plymouth/plymouthd.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/bootlog
%{_sbindir}/plymouthd
%{_libexecdir}/plymouth/plymouthd-fd-escrow
%{_bindir}/plymouth
%{_libdir}/plymouth/details.so
%{_libdir}/plymouth/text.so
%{_libdir}/plymouth/tribar.so
%{_datadir}/plymouth/themes/details/details.plymouth
%{_datadir}/plymouth/themes/text/text.plymouth
%{_datadir}/plymouth/themes/tribar/tribar.plymouth
%{_datadir}/plymouth/plymouthd.defaults
%{_localstatedir}/spool/plymouth
%{_mandir}/man?/*
%ghost %attr(0644,root,root) %{_localstatedir}/lib/plymouth/boot-duration
%{_unitdir}/

%files devel
%{_libdir}/libply.so
%{_libdir}/libply-splash-core.so
%{_libdir}/libply-boot-client.so
%{_libdir}/libply-splash-graphics.so
%{_libdir}/pkgconfig/ply-splash-core.pc
%{_libdir}/pkgconfig/ply-splash-graphics.pc
%{_libdir}/pkgconfig/ply-boot-client.pc
%{_libdir}/plymouth/renderers/x11*
%{_includedir}/plymouth-1

%files core-libs
%{_libdir}/libply.so.*
%{_libdir}/libply-splash-core.so.*
%{_libdir}/libply-boot-client.so.*
%dir %{_libdir}/plymouth

%files graphics-libs
%{_libdir}/libply-splash-graphics.so.*
%{_libdir}/plymouth/renderers/drm*
%{_libdir}/plymouth/renderers/frame-buffer*

%files scripts
%{_sbindir}/plymouth-set-default-theme
%{_libexecdir}/plymouth/plymouth-update-initrd
%{_libexecdir}/plymouth/plymouth-generate-initrd
%{_libexecdir}/plymouth/plymouth-populate-initrd

%files plugin-label
%{_libdir}/plymouth/label-freetype.so
%{_libdir}/plymouth/label-pango.so

%files plugin-script
%{_libdir}/plymouth/script.so

%files plugin-fade-throbber
%{_libdir}/plymouth/fade-throbber.so

%files plugin-space-flares
%{_libdir}/plymouth/space-flares.so

%files plugin-two-step
%{_libdir}/plymouth/two-step.so

%if ! 0%{?rhel}
%files theme-charge
%{_datadir}/plymouth/themes/charge
%endif

%files theme-fade-in
%{_datadir}/plymouth/themes/fade-in

%files theme-script
%{_datadir}/plymouth/themes/script

%files theme-solar
%{_datadir}/plymouth/themes/solar

%files theme-spinfinity
%{_datadir}/plymouth/themes/spinfinity

%files theme-spinner
# bgrt is a variant of spinner with different settings in its .plymouth file
%{_datadir}/plymouth/themes/bgrt
%{_datadir}/plymouth/themes/spinner

%files system-theme

%changelog
## START: Generated by rpmautospec
* Thu Apr 30 2026 Daniel McIlvaney <damcilva@microsoft.com> - 24.004.60-25
- test: add initial lock files

* Tue Jan 27 2026 Hans de Goede <johannes.goede@oss.qualcomm.com> - 24.004.60-24
- Fix hang in on_key_event() (rhbz#2433079)

* Sat Jan 17 2026 Fedora Release Engineering <releng@fedoraproject.org> - 24.004.60-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Sun Dec 21 2025 Hans de Goede <johannes.goede@oss.qualcomm.com> - 24.004.60-22
- Fix crash in drm plugin close_input_source() (rhbz#2416551)
- Fix wrong KBD layout when a user has configured multiple layouts
  (rhbz#2416197)
- Fix race in fb_device_has_drm_device () causing frame-buffer plugin to
  sometimes load while drm plugin is already handling the display

* Fri Aug 15 2025 Ray Strode <rstrode@redhat.com> - 24.004.60-21
- rebuild

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 24.004.60-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jul 03 2025 Hans de Goede <hansg@kernel.org> - 24.004.60-19
- Don't use simpledrm together with LUKS (rhbz#2359283, rhbz#2339072)
- Fix crash when using 2 GPUs with displays attached (rhbz#2368186)
- Fix crash caused by calling ply_event_loop_watch_fd () with a -1 fd
  (rhbz#2370979)
- Fix /usr/lib64/plymouth/tribar dir not being owned (rhbz#2279776)
- Fix keymap and capslock icons not shown on monitor on second GPU
  (rhbz#2375854)
- Make the prompt on the diskunlock screen look a bit better (rhbz#2356893)
- Add patches from upstream to fix messages being logged twice on serial
  consoles

* Thu Mar 06 2025 Hans de Goede <hdegoede@redhat.com> - 24.004.60-18
- Update simpledrm hiDPI scaling heuristics (rhbz#2347519)
- Ignore simpledrm when EFI fb is running at 1024x768/800x600
  (rhbz#2347519)
- Update spinner theme to match latest libadwaita spinner (rhbz#2325399)

* Mon Feb 17 2025 Hans de Goede <hdegoede@redhat.com> - 24.004.60-17
- Fix Dvorak layout icon not showing when the evdev keyboard driver is used
  (rhbz#2341810)
- Fix label plugin not finding fonts
- Add UseSimpledrm setting support to configfile (rhbz#2346150)

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 24.004.60-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sun Sep 22 2024 Niels De Graef <ndegraef@redhat.com> - 24.004.60-15
- Drop intltool dependency

* Sat Sep 21 2024 Anisse Astier <anisse@astier.eu> - 24.004.60-14
- Backport upstream crash fix (rhbz#2282384)

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 24.004.60-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Hans de Goede <hdegoede@redhat.com> - 24.004.60-12
- Probe simpledrm immediately (rhbz#2183743, rhbz#2274770)

* Thu Jun 06 2024 Hans de Goede <hdegoede@redhat.com> - 24.004.60-11
- Merge remote-tracking branch 'origin/f40' into rawhide

* Thu May 23 2024 Yaakov Selkowitz <yselkowi@redhat.com> - 24.004.60-10
- Fix redhat-fonts dependencies

* Wed May 15 2024 Ray Strode <rstrode@redhat.com> - 24.004.60-9
- Move font substitution to %%prep where it belongs

* Wed May 15 2024 Ray Strode <rstrode@redhat.com> - 24.004.60-8
- Use Red Hat Text font in RHEL

* Tue May 07 2024 Hans de Goede <hdegoede@redhat.com> - 24.004.60-7
- Revert patch to immediately switch to text mode on first renderer plugin
  error (#2270030)

* Sat Apr 27 2024 Adam Williamson <awilliam@redhat.com> - 24.004.60-6
- Backport upstream 10ac8d2 to fix passphrase appearing in text mode
  (#2271337)

* Sun Mar 17 2024 Adam Williamson <awilliam@redhat.com> - 24.004.60-5
- Revert upstream 48881ba to fix minimal installs (#2269385)

* Fri Feb 16 2024 Yaakov Selkowitz <yselkowi@redhat.com> - 24.004.60-4
- Generalize system-logos build dependency

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 24.004.60-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 24.004.60-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jan 04 2024 Ray Strode <rstrode@redhat.com> - 24.004.60-1
- Update to 24.004.60

* Tue Jan 02 2024 Miroslav Suchý <msuchy@redhat.com> - 23.360.11-2
- Migrate to SPDX license

* Tue Dec 26 2023 Ray Strode <rstrode@redhat.com> - 23.360.11-1
- Update to 23.360.11

* Tue Dec 26 2023 Ray Strode <rstrode@redhat.com> - 23.358.4-6
- Various fixes for more minimal installs

* Mon Dec 25 2023 Ray Strode <rstrode@redhat.com> - 23.358.4-5
- Fix systemd integration

* Mon Dec 25 2023 Ray Strode <rstrode@redhat.com> - 23.358.4-4
- Add xkeyboard-config requires for plymouth-scripts too

* Mon Dec 25 2023 Ray Strode <rstrode@redhat.com> - 23.358.4-3
- Add xkeyboard-config requires

* Sun Dec 24 2023 Ray Strode <rstrode@redhat.com> - 23.358.4-2
- New sources

* Sun Dec 24 2023 Ray Strode <rstrode@redhat.com> - 23.358.4-1
- Update to 23.358.4 (fixes initramfs crashers)

* Fri Dec 22 2023 Ray Strode <rstrode@redhat.com> - 23.356.9-4
- Add new build requires

* Fri Dec 22 2023 Ray Strode <rstrode@redhat.com> - 23.356.9-3
- Upload new sources

* Fri Dec 22 2023 Ray Strode <rstrode@redhat.com> - 23.356.9-2
- Add fedora-logos buildrequires

* Fri Dec 22 2023 Ray Strode <rstrode@redhat.com> - 23.356.9-1
- Update to 23.356.9

* Tue Nov 21 2023 Tomas Popela <tpopela@redhat.com> - 22.02.122-7
- Disable charge theme in ELN/RHEL 10

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 22.02.122-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 22.02.122-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Sep 28 2022 Hans de Goede <hdegoede@redhat.com> - 22.02.122-4
- Fix build now that systemd-devel no longer brings in ystemd

* Wed Sep 28 2022 Hans de Goede <hdegoede@redhat.com> - 22.02.122-3
- Fix SimpleDRM sometimes not being ignored (rhbz#2127663)

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 22.02.122-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Mar 07 2022 Hans de Goede <hdegoede@redhat.com> - 22.02.122-1
- New upstream release 22.02.122 (#2039427)

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Dec 06 2021 Hans de Goede <hdegoede@redhat.com> - 0.9.5-4
- Add "Requires: fedora-logos-classic" to the plymouth-theme-charge package

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Mar 31 2021 Hans de Goede <hdegoede@redhat.com> - 0.9.5-2
- New git snapshot Fixes 1933378 - Bootsplash doesn't always fully clear on
  boot to console Fixes 1941329 - Flickering plymouth on shutdown/reboot
  Prune spec-file changelog a bit

* Tue Mar 23 2021 Hans de Goede <hdegoede@redhat.com> - 0.9.5-1
- Update to 0.9.5 + a bunch of extra fixes from git (new upstream git
  snapshot) Fixes 1896929 - systemd complains about Unit configured to use
  KillMode=none

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.4-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Jan 08 2021 Tom Stellard <tstellar@redhat.com> - 0.9.4-18
- Add BuildRequires: make

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.4-17
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.4-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Mar 25 2020 Hans de Goede <hdegoede@redhat.com> - 0.9.4-15
- New upstream git snapshot Add RemainAfterExit=yes to plymouth's systemd
  service files (rhbz#1807771) Fix the spinner / animation missing on
  shutdown and reboot

* Mon Mar 09 2020 Hans de Goede <hdegoede@redhat.com> - 0.9.4-14
- Add patches fixing crash on monitor hot(un)plug (rhbz#1809681) Add
  patches fixing delay between gdm telling us to deactivate and us telling
  gdm it is ok to continue Drop plymouth-plugin-throbgress sub-package, the
  spinfinity theme now uses the two-step plugin

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.4-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Oct 22 2019 Hans de Goede <hdegoede@redhat.com> - 0.9.4-12
- Drop our private plymouth-update-initrd copy, it is identical to upstream
  New upstream git snapshot, with the following fixes: Tweaks to the
  spinner/bgrt themes to match the gdm/gnome-shell lock screen password
  entry style tweaks done in GNOME 3.34 Move the keyboard layout and
  capslock indicator closer to the text field Fix flickering below spinner
  on hidpi displays:
  https://gitlab.freedesktop.org/plymouth/plymouth/issues/83 Add logrotate
  file for /var/log/boot.log so that it does not grow endlessly:
  https://gitlab.freedesktop.org/plymouth/plymouth/issues/31 Some bgrt
  fixes for devices with non-upright mounted LCD panels

* Tue Oct 01 2019 Hans de Goede <hdegoede@redhat.com> - 0.9.4-11
- We are carrying so much patches from upstream that we are practically
  following upstream master, switch to a git snapshot Add keyboard layout
  and capslock state indicator support (rhbz#825406) Fix "Installing
  Updates..." text being rendered all garbled on devices where the panel is
  mounted 90 degrees rotated (rhbz#1753418)

* Sat Sep 07 2019 Hans de Goede <hdegoede@redhat.com> - 0.9.4-10
- Add a patch fixing issues when using cards which default to the radeon
  kms driver with the amdgpu kms driver (rhbz#1490490) Extend default
  DeviceTimeout to 8 seconds (rhbz#1737221)

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.4-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Jul 19 2019 Hans de Goede <hdegoede@redhat.com> - 0.9.4-8
- One more patch for dealing with some devices with a non-upright mounted
  LCD-panel (rhbz#1730783)

* Wed Jun 12 2019 Hans de Goede <hdegoede@redhat.com> - 0.9.4-7
- Add patches from upstream for: Fix failing to pick the native monitor
  mode starting with kernel 5.2 Fix firmware bootsplash support for devices
  which use the new (in ACPI 6.2) rotation bits in the BGRT header Add
  support for firmware-upgrade mode

* Mon Mar 25 2019 Hans de Goede <hdegoede@redhat.com> - 0.9.4-6
- Update bgrt/spinner background to solid black to make the experience on
  systems where we do not show the firmware boot-splash consistent with
  systems where we do show the firmware boot-splash Update translations

* Mon Mar 04 2019 Hans de Goede <hdegoede@redhat.com> - 0.9.4-5
- Add translations for the new spinner/bgrt offline-updates splash

* Wed Feb 13 2019 Hans de Goede <hdegoede@redhat.com> - 0.9.4-4
- Add patches from upstream for: Monitor hotplug support, this fixes issues
  with monitors on DP-MST docs sometimes not lighting up (rhbz#1652279)
  Adding support for using the firmware's bootsplash as theme background
  New bgrt theme which implements the boot-theme design from:
  https://wiki.gnome.org/Design/OS/BootProgress Including the new theming
  for offline-updates shown there Make the bgrt theme the new default and
  upgrade systems which are using the charge theme, which is the old
  default to use the new bgrt theme Cleanup the spec-file a bit: Remove
  unused / unnecessary %%global variables Sort the sections for the various
  plugins and themes alphabetically Simplify theme filelists

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Jan 22 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.9.4-2
- Remove obsolete ldconfig scriptlets

* Mon Nov 05 2018 Ray Strode <rstrode@redhat.com> - 0.9.4-1
- Update to 0.9.4

* Thu Oct 04 2018 Hans de Goede <hdegoede@redhat.com> - 0.9.3-27
- Add patches from upstream to fix the disk unlock screen sometimes having
  a very low resolution on UEFI machines:
  https://gitlab.freedesktop.org/plymouth/plymouth/issues/68

* Mon Aug 06 2018 Hans de Goede <hdegoede@redhat.com> - 0.9.3-26
- Update patches for CONFIG_FRAMEBUFFER_CONSOLE_DEFERRED_TAKEOVER
  interaction to the latest patches from master, this fixes the transition
  from plymouth to gdm being non smooth Drop unused default-boot-duration
  file (rhbz#1456010)

* Thu Aug 02 2018 Peter Robinson <pbrobinson@gmail.com> - 0.9.3-25
- Drop groups in spec, Drop requires on initscripts (rhbz 1592383) long
  migrated to systemd and original bug where it was added (461322) no
  longer relevant

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.3-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jul 09 2018 Igor Gnatenko <ignatenko@redhat.com> - 0.9.3-23
- add BuildRequires: gcc

* Mon Jul 02 2018 Hans de Goede <hdegoede@redhat.com> - 0.9.3-22
- Add patches from upstream fixing details view on kernels build with
  CONFIG_FRAMEBUFFER_CONSOLE_DEFERRED_TAKEOVER

* Thu Jun 07 2018 Adam Williamson <awilliam@redhat.com> - 0.9.3-21
- Move frame-buffer back to subpackage, patch bugs

* Mon Jun 04 2018 Adam Williamson <awilliam@redhat.com> - 0.9.3-20
- Move frame-buffer and drm renderers back to main package

* Fri Jun 01 2018 Adam Williamson <awilliam@redhat.com> - 0.9.3-19
- Merge branch 'master' into f28

* Tue Apr 17 2018 Hans de Goede <hdegoede@redhat.com> - 0.9.3-18
- Merge remote-tracking branch 'origin/master' into f28

* Thu Mar 29 2018 Colin Walters <walters@verbum.org> - 0.9.3-17
- Drop default boot duration:
  https://src.fedoraproject.org/rpms/plymouth/pull-request/1

* Thu Mar 29 2018 Colin Walters <walters@verbum.org> - 0.9.3-16
- Drop default boot-duration

* Fri Feb 09 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.9.3-15
- Escape macros in %%changelog

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.3-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Nov 28 2017 Ray Strode <rstrode@redhat.com> - 0.9.3-13
- Bump ShowDelay back up to 5

* Tue Nov 28 2017 Björn Esser <besser82@fedoraproject.org> - 0.9.3-12
- Fix invalid date in %%%%changelog

* Tue Nov 28 2017 Björn Esser <besser82@fedoraproject.org> - 0.9.3-11
- Update to 0.9.3 release Reduce ShowDelay to 0 (rhbz#1518037) Change
  %%%%define to %%%%global

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.3-10
- Rebuilt for
  https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Jun 20 2016 Ray Strode <rstrode@redhat.com> - 0.9.3-7
- misc fixes
- Fix color palette issue
- Fix splash at shutdown (if shutdown takes longer than 5 secs)
- Make sure text based splashes update terminal size when fbcon loads

* Thu Jun 16 2016 Ray Strode <rstrode@redhat.com> - 0.9.3-6
- really (?) fix password prompt on text plugin

* Tue Jun 14 2016 Ray Strode <rstrode@redhat.com> - 0.9.3-5
- fix password prompt on text plugin

* Wed Jun 08 2016 Ray Strode <rstrode@redhat.com> - 0.9.3-4
- new release versioning scheme to be more guideliney

* Tue Jun 07 2016 Ray Strode <rstrode@redhat.com> - 0.9.3-3
- Update to latest git snapshot
- Fixes use after free Related: #1342673

* Tue May 24 2016 Ray Strode <rstrode@redhat.com> - 0.9.3-2
- update build requires

* Tue May 24 2016 Ray Strode <rstrode@redhat.com> - 0.9.3-1
- Update to latest git snapshot

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.9-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Nov 16 2015 Ray Strode <rstrode@redhat.com> - 0.8.9-22
- fix plymouth-update-initrd

* Mon Nov 02 2015 Ray Strode <rstrode@redhat.com> - 0.8.9-21
- Fix updates with script and spinner themes

* Mon Aug 24 2015 Kalev Lember <klember@redhat.com> - 0.8.9-20
- Fix a typo in Requires

* Mon Aug 24 2015 Peter Robinson <pbrobinson@gmail.com> - 0.8.9-19
- fix confusion between scripts and plugin-scripts sub package

* Mon Aug 24 2015 Peter Robinson <pbrobinson@gmail.com> - 0.8.9-18
- Fix Requires for various libs subpackages

* Sun Aug 23 2015 Peter Robinson <pbrobinson@gmail.com> - 0.8.9-17
- Use %%%%license, Cleanup spec, Move drm render driver to graphics-libs
  sub package

* Thu Jun 18 2015 Dennis Gilmore <dennis@ausil.us> - 0.8.9-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed May 20 2015 Will Woods <wwoods@redhat.com> - 0.8.9-15
- add patch for #1223344

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 0.8.9-14
- Rebuilt for Fedora 23 Change

* Sun Aug 17 2014 Peter Robinson <pbrobinson@fedoraproject.org> - 0.8.9-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Jun 13 2014 Adam Jackson <ajax@redhat.com> - 0.8.9-12
- fix changelog date warnings

* Sat Jun 07 2014 Dennis Gilmore <dennis@ausil.us> - 0.8.9-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat May 31 2014 Peter Robinson <pbrobinson@gmail.com> - 0.8.9-10
- Move system-logos dep to graphics-libs (no use on text/serial console
  minimal installs)

* Thu Feb 20 2014 Ray Strode <rstrode@redhat.com> - 0.8.9-9
- Include patch

* Thu Feb 20 2014 Ray Strode <rstrode@redhat.com> - 0.8.9-8
- Fix splash after change in /sys/class/tty/console/active

* Thu Oct 31 2013 Ray Strode <rstrode@redhat.com> - 0.8.9-7
- Don't timeout plymouth quit waiting

* Wed Oct 16 2013 Ray Strode <rstrode@redhat.com> - 0.8.9-6
- need an explicit --without-rhgb-compat-link

* Wed Oct 16 2013 Ray Strode <rstrode@redhat.com> - 0.8.9-5
- drop rhgb-client compat link

* Sun Oct 06 2013 Kalev Lember <kalevlember@gmail.com> - 0.8.9-4
- Make sure the release number compares higher than the previous builds

* Wed Aug 14 2013 Ray Strode <rstrode@redhat.com> - 0.8.9-3
- Update to snapshot to fix system units

* Sun Aug 04 2013 Dennis Gilmore <dennis@ausil.us> - 0.8.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Mar 26 2013 Ray Strode <rstrode@redhat.com> - 0.8.9-1
- Update to snapshot to fix systemd vconsole issue

* Thu Feb 21 2013 Peter Robinson <pbrobinson@gmail.com> - 0.8.8-1
- Merge newer F18 release into rawhide

* Thu Feb 14 2013 Dennis Gilmore <dennis@ausil.us> - 0.8.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Aug 20 2012 Ray Strode <rstrode@redhat.com> - 0.8.7-1
- Latest upstream release - includes systemd fixes

* Mon Aug 20 2012 Dave Airlie <airlied@redhat.com> - 0.8.6.2-6
- fix plymouth race at bootup breaking efi/vesa handoff.
- fix version number - its against fedora package policy to have 0.year

* Tue Jul 24 2012 Ray Strode <rstrode@redhat.com> - 0.8.6.2-5
- Make plugins require main package

* Tue Jul 24 2012 Ray Strode <rstrode@redhat.com> - 0.8.6.2-4
- Update URL: in spec file to upstream homepage

* Tue Jul 24 2012 Ray Strode <rstrode@redhat.com> - 0.8.6.2-3
- Update snapshot to one that builds

* Mon Jul 23 2012 Ray Strode <rstrode@redhat.com> - 0.8.6.2-2
- drop upstreamed patch

* Mon Jul 23 2012 Ray Strode <rstrode@redhat.com> - 0.8.6.2-1
- One more crack at #830482 (will probably need additional fixes tomorrow)

* Mon Jul 23 2012 Tom Callaway <spot@fedoraproject.org> - 0.8.6.1-3
- [ProvenPackager] Applying tested fix for bz704658, more than a year after
  patch posted

* Sat Jul 21 2012 Dennis Gilmore <dennis@ausil.us> - 0.8.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 10 2012 Ray Strode <rstrode@redhat.com> - 0.8.6.1-1
- 0.8.6.1 fixes muck up from 0.8.6

* Mon Jul 09 2012 Ray Strode <rstrode@redhat.com> - 0.8.6-1
- Update to 0.8.6
- Fixes encrypted fs bug Resolves: #830482
- Adds support for offline updates

* Mon Jun 25 2012 Adam Jackson <ajax@redhat.com> - 0.8.5.1-5
- Rebuild without libkms

* Wed Jun 06 2012 Ray Strode <rstrode@redhat.com> - 0.8.5.1-4
- Add %%{_prefix} to systemd service path

* Wed Jun 06 2012 Ray Strode <rstrode@redhat.com> - 0.8.5.1-3
- add %%{_prefix} to systemd service files patch

* Wed Jun 06 2012 Ray Strode <rstrode@redhat.com> - 0.8.5.1-2
- Update to latest release

* Wed Jun 06 2012 Ray Strode <rstrode@redhat.com> - 0.8.5.1-1
- Update to latest release

* Tue Apr 24 2012 Richard Hughes <richard@hughsie.com> - 0.8.4-34
- Disable the nouveau driver as I've broken it with the new libdrm ABI

* Tue Mar 20 2012 Daniel Drake <dsd@laptop.org> - 0.8.4-33
- fix ARM build

* Tue Mar 20 2012 Ray Strode <rstrode@redhat.com> - 0.8.4-32
- Update to latest snapshot

* Mon Mar 12 2012 Ray Strode <rstrode@redhat.com> - 0.8.4-31
- Merge branch 'master' into f17

* Tue Feb 21 2012 Adam Williamson <awilliam@redhat.com> - 0.8.4-30
- Merge commit '2ff2e2df59398f65d87b954c601df6963a9fd9f3' into f17

* Wed Jan 25 2012 Harald Hoyer <harald@redhat.com> - 0.8.4-29
- install everything in /usr

* Sat Jan 14 2012 Dennis Gilmore <dennis@ausil.us> - 0.8.4-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Dec 15 2011 Ray Strode <rstrode@redhat.com> - 0.8.4-27
- Fix scriptlet error during livecd creation

* Wed Nov 09 2011 Adam Jackson <ajax@redhat.com> - 0.8.4-26
- Merge branch 'f16'

* Mon Nov 07 2011 Adam Jackson <ajax@redhat.com> - 0.8.4-25
- Rebuild for libpng 1.5

* Tue Aug 09 2011 Ray Strode <rstrode@redhat.com> - 0.8.4-24
- Update file list

* Tue Aug 09 2011 Ray Strode <rstrode@redhat.com> - 0.8.4-23
- Update to latest snapshot

* Fri Mar 04 2011 Ray Strode <rstrode@redhat.com> - 0.8.4-22
- Try to fix tty horkage mentioned in bug 681167

* Tue Mar 01 2011 Ray Strode <rstrode@redhat.com> - 0.8.4-21
- jlaska test

* Fri Feb 18 2011 Ray Strode <rstrode@redhat.com> - 0.8.4-20
- potentially fix bug 655538

* Thu Feb 10 2011 Christopher Aillon <caillon@redhat.com> - 0.8.4-19
- Fix up obsoletes typo

* Wed Feb 09 2011 Ray Strode <rstrode@redhat.com> - 0.8.4-18
- Add buildrequires for gtk

* Wed Feb 09 2011 Ray Strode <rstrode@redhat.com> - 0.8.4-17
- Update to latest snapshot

* Wed Feb 09 2011 Dennis Gilmore <dennis@ausil.us> - 0.8.4-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Feb 04 2011 Ray Strode <rstrode@redhat.com> - 0.8.4-15
- Drop boot log viewer

* Sat Jan 29 2011 Ville Skyttä <ville.skytta@iki.fi> - 0.8.4-14
- Dir ownership fixes (#645044).

* Sat Nov 20 2010 Ray Strode <rstrode@redhat.com> - 0.8.4-13
- Fix serial console problem

* Fri Nov 19 2010 Ray Strode <rstrode@redhat.com> - 0.8.4-12
- Update to recent snapshot

* Tue Nov 02 2010 Ray Strode <rstrode@redhat.com> - 0.8.4-11
- Update sources again

* Tue Nov 02 2010 Ray Strode <rstrode@redhat.com> - 0.8.4-10
- Update sources

* Tue Nov 02 2010 Ray Strode <rstrode@redhat.com> - 0.8.4-9
- Update sources

* Tue Nov 02 2010 Ray Strode <rstrode@redhat.com> - 0.8.4-8
- Update to recent snapshot

* Wed Sep 01 2010 Ray Strode <rstrode@redhat.com> - 0.8.4-7
- Require dracut

* Thu Aug 26 2010 Ray Strode <rstrode@redhat.com> - 0.8.4-6
- Add more Requires: to spec

* Thu Aug 26 2010 Ray Strode <rstrode@redhat.com> - 0.8.4-5
- Fix plymouth-update-initrd to work with dracut

* Mon Aug 23 2010 Ray Strode <rstrode@redhat.com> - 0.8.4-4
- Latest snapshot and turn on separate initrd generation

* Sat Aug 21 2010 Ray Strode <rstrode@redhat.com> - 0.8.4-3
- Update to recent snapshot from git

* Thu Jul 29 2010 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.4-2
- dist-git conversion

* Sat Jul 24 2010 Ray Strode <rstrode@fedoraproject.org> - 0.8.4-1
- Update to pre-release snapshot of 0.8.4

* Thu Jan 14 2010 Ray Strode <rstrode@fedoraproject.org> - 0.8.0-12
- Don't link plymouthd against libpng either

* Thu Jan 14 2010 Ray Strode <rstrode@fedoraproject.org> - 0.8.0-11
- Make it possible to do a basic plymouth installations without libpng

* Thu Jan 07 2010 Ray Strode <rstrode@fedoraproject.org> - 0.8.0-10
- Drop nash dep

* Mon Dec 21 2009 Dave Airlie <airlied@fedoraproject.org> - 0.8.0-9
- rebuild for API bump in libdrm

* Wed Dec 09 2009 Ray Strode <rstrode@fedoraproject.org> - 0.8.0-8
- Update to latest snapshot

* Wed Nov 25 2009 Bill Nottingham <notting@fedoraproject.org> - 0.8.0-7
- Fix typo that causes a failure to update the common directory. (releng
  #2781)

* Mon Nov 23 2009 Ray Strode <rstrode@fedoraproject.org> - 0.8.0-6
- Add missing buildreq

* Mon Nov 23 2009 Ray Strode <rstrode@fedoraproject.org> - 0.8.0-5
- Update to latest snapshot

* Mon Oct 05 2009 Ray Strode <rstrode@fedoraproject.org> - 0.8.0-4
- Add new x11-renderer plugin from Charlie Brej for debugging

* Tue Sep 29 2009 Ray Strode <rstrode@fedoraproject.org> - 0.8.0-3
- Fix escape and ask-for-password

* Mon Sep 28 2009 Ray Strode <rstrode@fedoraproject.org> - 0.8.0-2
- Add BuildRequires for libdrm

* Mon Sep 28 2009 Ray Strode <rstrode@fedoraproject.org> - 0.8.0-1
- Add prerelease of 0.8.0 for multihead support

* Fri Sep 11 2009 Ray Strode <rstrode@fedoraproject.org> - 0.7.1-8
- Go back to blue charge background (bug 522460)

* Fri Sep 11 2009 Ray Strode <rstrode@fedoraproject.org> - 0.7.1-7
- Remove duplicate Provides: plymouth(system-theme)

* Thu Sep 10 2009 Ray Strode <rstrode@fedoraproject.org> - 0.7.1-6
- Fix set_verbose error reported by yaneti.

* Wed Sep 09 2009 Ray Strode <rstrode@fedoraproject.org> - 0.7.1-5
- Add patch

* Wed Sep 09 2009 Ray Strode <rstrode@fedoraproject.org> - 0.7.1-4
- Look for inst() in dracut as well as mkinitrd bash source file - Drop
  plymouth initrd for now.

* Sat Aug 29 2009 Ray Strode <rstrode@fedoraproject.org> - 0.7.1-3
- Create plymouth supplementary initrd in post (bug 515589)

* Tue Aug 25 2009 Ray Strode <rstrode@fedoraproject.org> - 0.7.1-2
- Get plugin path from plymouth instead of trying to guess. Should fix bug
  502667

* Tue Aug 25 2009 Ray Strode <rstrode@fedoraproject.org> - 0.7.1-1
- Update to 0.7.1

* Mon Aug 24 2009 Adam Jackson <ajax@fedoraproject.org> - 0.7.0-19
- Set charge bgcolor to black. (#519052)

* Tue Aug 11 2009 Ray Strode <rstrode@fedoraproject.org> - 0.7.0-18
- Update to 0.7.0

* Sun Jul 26 2009 Jesse Keating <jkeating@fedoraproject.org> - 0.7.0-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri May 15 2009 Ray Strode <rstrode@fedoraproject.org> - 0.7.0-16
- Fix spinfinity theme to point to the right image directory (bug 500994)

* Thu May 14 2009 Ray Strode <rstrode@fedoraproject.org> - 0.7.0-15
- Update to new snapshot that renames plugins to fix upgrades somewhat (bug
  499940)

* Thu May 14 2009 Ray Strode <rstrode@fedoraproject.org> - 0.7.0-14
- Update to new snapshot that renames plugins to fix upgrades somewhat (bug
  499940)

* Fri May 08 2009 Ray Strode <rstrode@fedoraproject.org> - 0.7.0-13
- Add some fixes for shutdown

* Fri May 08 2009 Ray Strode <rstrode@fedoraproject.org> - 0.7.0-12
- Don't slow down progress updating at the end of boot

* Thu May 07 2009 Ray Strode <rstrode@fedoraproject.org> - 0.7.0-11
- Change colors to transition better to gdm

* Thu May 07 2009 Ray Strode <rstrode@fedoraproject.org> - 0.7.0-10
- Make "charge" theme require two-step plugin instead of solar (oops)

* Wed May 06 2009 Ray Strode <rstrode@fedoraproject.org> - 0.7.0-9
- Update to "plugin-rework" branch from git

* Wed Apr 08 2009 Jesse Keating <jkeating@fedoraproject.org> - 0.7.0-8
- Drop the version on system-logos requires for now, causing hell with
  other -logos providers not having the same version.

* Wed Mar 18 2009 Ray Strode <rstrode@fedoraproject.org> - 0.7.0-7
- Destroy terminal on detach (may help with bug 490965)

* Tue Mar 10 2009 Ray Strode <rstrode@fedoraproject.org> - 0.7.0-6
- Address one more issue with password handling. It wasn't working well for
  secondary devices when using the "details" plugin.

* Mon Mar 09 2009 Ray Strode <rstrode@fedoraproject.org> - 0.7.0-5
- Attempt to address some problems with password handling in the 0.7.0
  snapshots

* Fri Mar 06 2009 Ray Strode <rstrode@fedoraproject.org> - 0.7.0-4
- Fix set default script

* Fri Mar 06 2009 Ray Strode <rstrode@fedoraproject.org> - 0.7.0-3
- Rev release

* Fri Mar 06 2009 Ray Strode <rstrode@fedoraproject.org> - 0.7.0-2
- more scriptlet changes to move from solar to spinfinity

* Fri Mar 06 2009 Ray Strode <rstrode@fedoraproject.org> - 0.7.0-1
- Updated to development snapshot - Guess progress better on second boot of
  persistent live images - Drop upstream patches - swap "solar" and
  "spinfinity" scriptlet behavior

* Tue Feb 24 2009 Ray Strode <rstrode@fedoraproject.org> - 0.6.0-83
- Add fix-heap-corruptor patch from master. Problem spotted by Mr. McCann.

* Wed Dec 17 2008 Ray Strode <rstrode@fedoraproject.org> - 0.6.0-82
- Add patch from drop-nash branch for jeremy

* Wed Dec 03 2008 Ray Strode <rstrode@fedoraproject.org> - 0.6.0-81
- Update to 0.6.0

* Sun Nov 23 2008 Matthias Clasen <mclasen@fedoraproject.org> - 0.6.0-80
- Tweak %%%%summary

* Mon Nov 17 2008 Ray Strode <rstrode@fedoraproject.org> - 0.6.0-79
- don't give error about missing default.so - rework packaging of boot-
  duration to prevent .rpmnew droppings (bug 469752)

* Mon Nov 17 2008 Ray Strode <rstrode@fedoraproject.org> - 0.6.0-78
- Don't tell gdm to transition unless booting into runlevel 3 (bug 471785)

* Mon Nov 17 2008 Ray Strode <rstrode@fedoraproject.org> - 0.6.0-77
- Crawl progress bar if boot is way off course (Charlie, bug 471089)

* Fri Nov 14 2008 Ray Strode <rstrode@fedoraproject.org> - 0.6.0-76
- Don't loop forever when tty returns NUL byte (bug 471498)

* Fri Nov 14 2008 Ray Strode <rstrode@fedoraproject.org> - 0.6.0-75
- Generate solar background dynamically to reduce ondisk size, and look
  better at various resolutions (Charlie, bug 471227)

* Thu Nov 13 2008 Ray Strode <rstrode@fedoraproject.org> - 0.6.0-74
- Move Obsoletes: plymouth-text-and-details-only to base package so people
  who had it installed don't end up solar on upgrade

* Thu Nov 13 2008 Ray Strode <rstrode@fedoraproject.org> - 0.6.0-73
- Redo packaging to work better with minimal installs (bug 471314)

* Wed Nov 12 2008 Ray Strode <rstrode@fedoraproject.org> - 0.6.0-72
- Fix plymouth-set-default-plugin to allow external $LIB

* Wed Nov 12 2008 Ray Strode <rstrode@fedoraproject.org> - 0.6.0-71
- Fix star image (Charlie, bug 471113)

* Tue Nov 11 2008 Ray Strode <rstrode@fedoraproject.org> - 0.6.0-70
- Improve solar flares (Charlie) - redirect tty again on --show-splash -
  ignore subsequent --hide-splash calls after the first one - turn off
  kernel printks during boot up

* Tue Nov 11 2008 Ray Strode <rstrode@fedoraproject.org> - 0.6.0-69
- Disconnect from tty when init=/bin/bash (bug 471007)

* Mon Nov 10 2008 Ray Strode <rstrode@fedoraproject.org> - 0.6.0-68
- Force the right arch when calling plymouth-set-default-plugin (bug
  470732)

* Mon Nov 10 2008 Ray Strode <rstrode@fedoraproject.org> - 0.6.0-67
- Drop comet (bug 468705) - make boot-duration config(noreplace)

* Mon Nov 10 2008 Ray Strode <rstrode@fedoraproject.org> - 0.6.0-66
- Don't abort if no splash when root is mounted - Actually move patches
  upstream

* Mon Nov 10 2008 Ray Strode <rstrode@fedoraproject.org> - 0.6.0-65
- Fix feedback loop with plymouth:debug - Move patches upstream - Improve
  comet animation

* Mon Nov 10 2008 Ray Strode <rstrode@fedoraproject.org> - 0.6.0-64
- Fix feedback loop with plymouth:debug - Move patches upstream - Improve
  comet animation

* Mon Nov 10 2008 Ray Strode <rstrode@fedoraproject.org> - 0.6.0-63
- Fix up more-debug patch to not assert with plymouth:nolog (bug 470569)

* Fri Nov 07 2008 Ray Strode <rstrode@fedoraproject.org> - 0.6.0-62
- fix date stamp

* Fri Nov 07 2008 Ray Strode <rstrode@fedoraproject.org> - 0.6.0-61
- add some more debug spew to help debug a problem jlaska is having

* Fri Nov 07 2008 Ray Strode <rstrode@fedoraproject.org> - 0.6.0-60
- add some more debug spew to help debug a problem jlaska is having

* Fri Nov 07 2008 Ray Strode <rstrode@fedoraproject.org> - 0.6.0-59
- Update tarball so patch applies

* Fri Nov 07 2008 Ray Strode <rstrode@fedoraproject.org> - 0.6.0-58
- show details plugin on --hide-splash so people can see why the splash got
  hidden.

* Thu Nov 06 2008 Ray Strode <rstrode@fedoraproject.org> - 0.6.0-57
- Don't exit on plymouth --show-splash after sulogin - Properly retake
  console after that --show-splash

* Wed Nov 05 2008 Ray Strode <rstrode@fedoraproject.org> - 0.6.0-56
- reset colors on quit --retain-splash - fix off by one in damage
  calculation for label

* Tue Nov 04 2008 Ray Strode <rstrode@fedoraproject.org> - 0.6.0-55
- rev release

* Tue Nov 04 2008 Ray Strode <rstrode@fedoraproject.org> - 0.6.0-54
- Add a sample boot-duration for livecds and first time boots (bug 469752)

* Mon Nov 03 2008 Jeremy Katz <katzj@fedoraproject.org> - 0.6.0-53
- Allow pre-setting the default plugin when calling plymouth-populate-
  initrd

* Fri Oct 31 2008 Ray Strode <rstrode@fedoraproject.org> - 0.6.0-52
- Add pango minimum version to buildrequires

* Thu Oct 30 2008 Ray Strode <rstrode@fedoraproject.org> - 0.6.0-51
- Update prompt text colors to be legible on new artwork

* Thu Oct 30 2008 Ray Strode <rstrode@fedoraproject.org> - 0.6.0-50
- drop unused patches from version control

* Thu Oct 30 2008 Ray Strode <rstrode@fedoraproject.org> - 0.6.0-49
- Drop upstreamed patches - Patch from Charlie to update artwork - Patch
  from Charlie to make password screen match animation better (bug 468899)

* Thu Oct 30 2008 Ray Strode <rstrode@fedoraproject.org> - 0.6.0-48
- Fix escape at password prompt (bug 467533)

* Wed Oct 29 2008 Ray Strode <rstrode@fedoraproject.org> - 0.6.0-47
- Don't require /bin/plymouth before it's installed (bug 468925)

* Tue Oct 28 2008 Ray Strode <rstrode@fedoraproject.org> - 0.6.0-46
- Force raw mode for keyboard input with solar and fade-in (bug 468880) -
  make sure windows get closed on exit

* Tue Oct 28 2008 Ray Strode <rstrode@fedoraproject.org> - 0.6.0-45
- Make "Solar" lock icon the same as the "Spinfinity" one.

* Tue Oct 28 2008 Ray Strode <rstrode@fedoraproject.org> - 0.6.0-44
- Make plymouth-libs own /usr/lib/plymouth (bug 458071)

* Tue Oct 28 2008 Ray Strode <rstrode@fedoraproject.org> - 0.6.0-43
- Default to "Solar" instead of "Spinfinity"

* Mon Oct 27 2008 Ray Strode <rstrode@fedoraproject.org> - 0.6.0-42
- Don't set plymouth default plugin to text in %%post

* Mon Oct 27 2008 Ray Strode <rstrode@fedoraproject.org> - 0.6.0-41
- Add Charlie patch to dither in lower color modes (bug 468276)

* Sun Oct 26 2008 Jeremy Katz <katzj@fedoraproject.org> - 0.6.0-40
- More requires changing to avoid loops (#467356)

* Fri Oct 24 2008 Ray Strode <rstrode@fedoraproject.org> - 0.6.0-39
- Add updated progress bar for solar plugin from Charlie - Log
  plymouth:debug output to boot log - Ignore sigpipe signals in daemon

* Fri Oct 24 2008 Ray Strode <rstrode@fedoraproject.org> - 0.6.0-38
- Bump so name of libply to hopefully force plymouth to get installed
  before kernel (or at least make plymouth-libs and plymouth get installed
  on the same side of kernel in the transaction).

* Thu Oct 23 2008 Ray Strode <rstrode@fedoraproject.org> - 0.6.0-37
- Add patch from Charliie to align progress bar to milestones during boot
  up - force tty to be sane on exit (bug 467207)

* Thu Oct 23 2008 Ray Strode <rstrode@fedoraproject.org> - 0.6.0-36
- add empty files section for text-and-details-only so the subpackage shows
  up.

* Thu Oct 23 2008 Ray Strode <rstrode@fedoraproject.org> - 0.6.0-35
- add text-and-details-only subpackage so davej can uninstall spinfinity,
  pango, cairo etc from his router.

* Tue Oct 21 2008 Ray Strode <rstrode@fedoraproject.org> - 0.6.0-34
- Minor event loop changes - drop upstream patches - Charlie Brej fix for
  progress bar resetting when escape gets pressed

* Tue Oct 21 2008 Ray Strode <rstrode@fedoraproject.org> - 0.6.0-33
- Don't make plymouth-libs require plymouth (more fun with 467356)

* Tue Oct 21 2008 Ray Strode <rstrode@fedoraproject.org> - 0.6.0-32
- Add initscripts requires (bug 461322)

* Mon Oct 20 2008 Ray Strode <rstrode@fedoraproject.org> - 0.6.0-31
- Put tty1 back in "cooked" mode when going into runlevel 3 (bug 467207)

* Fri Oct 17 2008 Ray Strode <rstrode@fedoraproject.org> - 0.6.0-30
- Clear screen in details plugin when it's done - Make plymouth-update-
  initrd a small wrapper around mkinitrd instead of the broken monstrosity
  it was before.

* Fri Oct 17 2008 Ray Strode <rstrode@fedoraproject.org> - 0.6.0-29
- Fix up Requires for new plymouth-scripts

* Fri Oct 17 2008 Ray Strode <rstrode@fedoraproject.org> - 0.6.0-28
- Move plymouth-set-default-plugin, plymouth-update-initrd, and plymouth-
  populate-initrd to plymouth-scripts subpackage (the last fix didn't
  actually help with bug 467356)

* Fri Oct 17 2008 Ray Strode <rstrode@fedoraproject.org> - 0.6.0-27
- Move plymouth-set-default-plugin to -libs (might help with bug 467356) -
  Fix up requires, provides and postun scripts

* Wed Oct 15 2008 Ray Strode <rstrode@fedoraproject.org> - 0.6.0-26
- Don't free windows on --hide-splash (fix from Jeremy)

* Tue Oct 14 2008 Ray Strode <rstrode@fedoraproject.org> - 0.6.0-25
- Solar fixes from Charlie Brej - Better cpu usage from Charlie

* Fri Oct 10 2008 Ray Strode <rstrode@fedoraproject.org> - 0.6.0-24
- Add Requires(post): nash (bug 466500)

* Wed Oct 08 2008 Ray Strode <rstrode@fedoraproject.org> - 0.6.0-23
- Rework how "console=" args done again, to hopefully fix bug 460565

* Mon Oct 06 2008 Ray Strode <rstrode@fedoraproject.org> - 0.6.0-22
- Add "Solar" plugin from Charles Brej - Move things around so computers
  with separate /usr boot (hopefully this won't break things, but it
  probably will) - Make GDM show up on vt1 for all plugins

* Tue Sep 30 2008 Ray Strode <rstrode@fedoraproject.org> - 0.6.0-21
- Fix changelog attribution to reflect who commited the last change

* Tue Sep 30 2008 Jeremy Katz <katzj@fedoraproject.org> - 0.6.0-20
- Remove mkinitrd requires to break the dep loop and ensure things get
  installed in the right order

* Fri Sep 26 2008 Ray Strode <rstrode@fedoraproject.org> - 0.6.0-19
- Package some unpackaged files

* Thu Sep 25 2008 Ray Strode <rstrode@fedoraproject.org> - 0.6.0-18
- Add new snapshot to fold in Will Woods progress bar, and move ajax's
  splash upstream

* Tue Sep 23 2008 Ray Strode <rstrode@fedoraproject.org> - 0.6.0-17
- Last snapshot was broken

* Mon Sep 22 2008 Ray Strode <rstrode@fedoraproject.org> - 0.6.0-16
- Update to latest snapshot to get better transition support

* Fri Sep 19 2008 Ray Strode <rstrode@fedoraproject.org> - 0.6.0-15
- Turn on gdm trigger for transition

* Mon Sep 15 2008 Ray Strode <rstrode@fedoraproject.org> - 0.6.0-14
- add quit command with --retain-splash option to client

* Wed Sep 10 2008 Ray Strode <rstrode@fedoraproject.org> - 0.6.0-13
- drop upstreamed patch

* Wed Sep 10 2008 Ray Strode <rstrode@fedoraproject.org> - 0.6.0-12
- Fix text rendering for certain machines

* Mon Sep 08 2008 Ray Strode <rstrode@fedoraproject.org> - 0.6.0-11
- fix typo in patch

* Mon Sep 08 2008 Ray Strode <rstrode@fedoraproject.org> - 0.6.0-10
- More serial console fixes (bug 460565 again)

* Fri Sep 05 2008 Bill Nottingham <notting@fedoraproject.org> - 0.6.0-9
- Put /etc/system-release on the initrd, and read that instead of
  hardcoding 'Fedora 10'.

* Fri Sep 05 2008 Ray Strode <rstrode@fedoraproject.org> - 0.6.0-8
- Try to support multiple serial consoles better (bug 460565)

* Fri Sep 05 2008 Ray Strode <rstrode@fedoraproject.org> - 0.6.0-7
- Fix some confusion with password handling in details plugin

* Wed Aug 27 2008 Ray Strode <rstrode@fedoraproject.org> - 0.6.0-6
- Fix patch line

* Wed Aug 27 2008 Ray Strode <rstrode@fedoraproject.org> - 0.6.0-5
- If user hits escape, send "" as the password (bug 459111)

* Wed Aug 27 2008 Ray Strode <rstrode@fedoraproject.org> - 0.6.0-4
- Fix another crasher for users with encrypted disks (this time in the text
  plugin, not the client)

* Wed Aug 27 2008 Ray Strode <rstrode@fedoraproject.org> - 0.6.0-3
- Package new label plugin used by spinfinity

* Wed Aug 27 2008 Ray Strode <rstrode@fedoraproject.org> - 0.6.0-2
- Update to latest snapshot - Add the ability to show text prompts in
  graphical plugin - Fix crasher for users with encrypted disks

* Fri Aug 22 2008 Ray Strode <rstrode@fedoraproject.org> - 0.6.0-1
- Update to latest snapshot

* Wed Aug 13 2008 Ray Strode <rstrode@fedoraproject.org> - 0.5.0-23
- Update previous patch to remove some assertions

* Wed Aug 13 2008 Ray Strode <rstrode@fedoraproject.org> - 0.5.0-22
- add a patch that may help serial console users

* Wed Aug 13 2008 Ray Strode <rstrode@fedoraproject.org> - 0.5.0-21
- add spool directory to file list

* Wed Aug 13 2008 Ray Strode <rstrode@fedoraproject.org> - 0.5.0-20
- Make plymouth-gdm-hooks require plymouth-utils

* Wed Aug 13 2008 Ray Strode <rstrode@fedoraproject.org> - 0.5.0-19
- fix build issues from last commit

* Wed Aug 13 2008 Ray Strode <rstrode@fedoraproject.org> - 0.5.0-18
- Add a boot failure viewer to login screen (written by Matthias)

* Tue Aug 12 2008 Adam Jackson <ajax@fedoraproject.org> - 0.5.0-17
- plymouth-0.5.0-textbar-hotness.patch: Change the text plugin to a
  slightly more traditional progress bar, to maintain the illusion of
  progress better than the eternally oscillating cylon. Note: still
  incomplete.

* Fri Aug 08 2008 Ray Strode <rstrode@fedoraproject.org> - 0.5.0-16
- Don't require a modifiable text color map (may fix serial consoles)

* Thu Aug 07 2008 Ray Strode <rstrode@fedoraproject.org> - 0.5.0-15
- Update to new snapshot which when combined with a new mkinitrd should
  make unlocking encrypted root partitions work again

* Thu Aug 07 2008 Ray Strode <rstrode@fedoraproject.org> - 0.5.0-14
- Update to new snapshot which fixes some assertion failures in the client
  code

* Wed Aug 06 2008 Ray Strode <rstrode@fedoraproject.org> - 0.5.0-13
- Add Requires(post): plymouth to plugins so they get plymouth-set-default-
  plugin (bug 458071)

* Tue Aug 05 2008 Ray Strode <rstrode@fedoraproject.org> - 0.5.0-12
- Add plymouth dirs to file list (bug 457871)

* Fri Aug 01 2008 Ray Strode <rstrode@fedoraproject.org> - 0.5.0-11
- new plymout-populate-initrd features don't work with the set -e at the
  top of it.

* Fri Aug 01 2008 Ray Strode <rstrode@fedoraproject.org> - 0.5.0-10
- Update to another snapshot to actually get new plymouth-populate-initrd
  features

* Thu Jul 31 2008 Ray Strode <rstrode@fedoraproject.org> - 0.5.0-9
- Drop defunct patch lines

* Thu Jul 31 2008 Ray Strode <rstrode@fedoraproject.org> - 0.5.0-8
- Update to snapshot to get new plymouth-populate-initrd features - Make
  removing rhgb use details plugin instead of exiting

* Thu Jul 31 2008 Peter Jones <pjones@fedoraproject.org> - 0.5.0-7
- Make it a mkinitrd requires instead of a nash requires (that will still
  pull in nash, but we need mkinitrd for newer plymouth-populate-initrd)

* Wed Jul 30 2008 Ray Strode <rstrode@fedoraproject.org> - 0.5.0-6
- Add nash requires

* Thu Jul 10 2008 Ray Strode <rstrode@fedoraproject.org> - 0.5.0-5
- Use a new heuristic for finding libdir, since the old one falls over on
  ia64

* Wed Jul 09 2008 Ray Strode <rstrode@fedoraproject.org> - 0.5.0-4
- add ctrl-r to rotate text color palette back to stock values

* Tue Jul 08 2008 Ray Strode <rstrode@fedoraproject.org> - 0.5.0-3
- Fix populate script on ppc (bug 454353)

* Tue Jul 01 2008 Ray Strode <rstrode@fedoraproject.org> - 0.5.0-2
- Pull in spinfinity by default. This whole "figure out which plugin to
  use" set of scripts and scriptlets needs work. We need to separate distro
  default from user choice.

* Tue Jul 01 2008 Ray Strode <rstrode@fedoraproject.org> - 0.5.0-1
- Add new client "ask-for-password" command which feeds the user input to a
  program instead of standard output, and loops when the program returns
  non-zero exit status.

* Thu Jun 26 2008 Ray Strode <rstrode@fedoraproject.org> - 0.4.5-1
- Update to version 0.4.5 - Make text plugin blue and less 80s

* Wed Jun 25 2008 Ray Strode <rstrode@fedoraproject.org> - 0.4.0-4
- Make "Password: " show up correctly in text plugin

* Wed Jun 25 2008 Ray Strode <rstrode@fedoraproject.org> - 0.4.0-3
- Require elfutils (bug 452797)

* Mon Jun 23 2008 Ray Strode <rstrode@fedoraproject.org> - 0.4.0-2
- Make plymouth-set-default-plugin --reset choose the latest installed
  plugin, not the earliest

* Sun Jun 22 2008 Ray Strode <rstrode@fedoraproject.org> - 0.4.0-1
- Update to version 0.4.0 - Only run if rhgb is on kernel command line -
  Make text plugin more animated

* Wed Jun 18 2008 Ray Strode <rstrode@fedoraproject.org> - 0.3.2-4
- drop echos

* Tue Jun 17 2008 Peter Jones <pjones@fedoraproject.org> - 0.3.2-3
- Fix ldconfig to be run on -libs not on the main package. Fix main package
  and plugins not to reset inappropriately.

* Mon Jun 16 2008 Ray Strode <rstrode@fedoraproject.org> - 0.3.2-2
- dont go back to text mode on exit

* Mon Jun 16 2008 Ray Strode <rstrode@fedoraproject.org> - 0.3.2-1
- Update to version 0.3.2 - show gradient in spinfinity plugin - Drop fade
  out in spinfinity plugin - fix throbber placement - rename graphical.so
  to default.so

* Fri Jun 13 2008 Ray Strode <rstrode@fedoraproject.org> - 0.3.1-4
- scriplet should be preun, not postun

* Thu Jun 12 2008 Ray Strode <rstrode@fedoraproject.org> - 0.3.1-3
- Should run --reset in preun not postun

* Thu Jun 12 2008 Ray Strode <rstrode@fedoraproject.org> - 0.3.1-2
- Fix postun scriptlet

* Thu Jun 12 2008 Ray Strode <rstrode@fedoraproject.org> - 0.3.1-1
- Update to version 0.3.1 - Don't ship generated initrd scripts in tarball

* Thu Jun 12 2008 Ray Strode <rstrode@fedoraproject.org> - 0.3.0-1
- Update to version 0.3.0 - Better plugin handling - Better integration
  with mkinitrd (pending mkinitrd changes) - random bug fixes

* Mon Jun 09 2008 Ray Strode <rstrode@fedoraproject.org> - 0.2.0-1
- Update to version 0.2.0 - Integrate more tightly with nash (pending nash
  changes) - ship libs for out of tree splash plugins - gradient support -
  random bug fixes

* Sat May 31 2008 Ray Strode <rstrode@fedoraproject.org> - 0.1.0-6
- Initial import, version 0.1.0

* Fri Sep 02 2011 Ray Strode <rstrode@redhat.com> - 0.8.4-5
- Make plymouth background dark gray at the request of Mo / design team.

* Mon Aug 22 2011 Ray Strode <rstrode@redhat.com> - 0.8.4-4
- Update to latest git snapshot - Reintroduce accidentally dropped spinner
  theme and systemd integration

* Tue Aug 09 2011 Ray Strode <rstrode@redhat.com> - 0.8.4-3
- rebuild with higher release number

* Tue Feb 21 2012 Adam Williamson <awilliam@redhat.com> - 0.8.4-2
- make plymouth-scripts depend on plymouth (EH #794894)

* Mon Mar 12 2012 Ray Strode <rstrode@redhat.com> - 0.8.4-1
- Don't require libdrm_intel on non intel arches

* Thu Dec 13 2012 Ray Strode <rstrode@redhat.com> - 0.8.8-5
- Ensure fedup gets right splash screen

* Fri Nov 16 2012 Ray Strode <rstrode@redhat.com> - 0.8.8-4
- Drop set-default-plugin compat script - Just use upstream update-initrd

* Fri Nov 02 2012 Ray Strode <rstrode@redhat.com> - 0.8.8-3
- More boot blocking fixes

* Thu Nov 01 2012 Ray Strode <rstrode@redhat.com> - 0.8.8-2
- Fix crash when deactivating multiple times

* Fri Oct 26 2012 Ray Strode <rstrode@redhat.com> - 0.8.8-1
- Latest upstream release
- includes systemd fixes and system update fixes

* Tue Apr 17 2018 Hans de Goede <hdegoede@redhat.com> - 0.9.3-4
- Merge with F28 branch, fix FTBFS
- Sync in changes which were only added to the F28 branch
- Add a patch from upstream git to fix FTBFS

* Tue Apr 17 2018 Hans de Goede <hdegoede@redhat.com> - 0.9.3-3
- Add patches from upstream git for devices with non upright mounted LCD
  panels https://bugs.freedesktop.org/show_bug.cgi?id=104714

* Tue Mar 27 2018 Colin Walters <walters@verbum.org> - 0.9.3-2
- Drop default boot-duration

* Fri Jun 01 2018 Adam Williamson <awilliam@redhat.com> - 0.9.3-1
- Move frame-buffer renderer to graphics-libs (#1518464)

* Tue May 28 2024 Hans de Goede <hdegoede@redhat.com> - 24.004.60-6
- Merge remote-tracking branch 'origin/rawhide' into f40

* Sat Apr 27 2024 Adam Williamson <awilliam@redhat.com> - 24.004.60-5
- Backport upstream 10ac8d2 to fix passphrase appearing in text mode
  (#2271337)

* Sun Mar 17 2024 Adam Williamson <awilliam@redhat.com> - 24.004.60-4
- Revert upstream 48881ba to fix minimal installs (#2269385)

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 24.004.60-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 24.004.60-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jan 04 2024 Ray Strode <rstrode@redhat.com> - 24.004.60-1
- Update to 24.004.60

* Tue Jan 02 2024 Miroslav Suchý <msuchy@redhat.com> - 23.360.11-2
- Migrate to SPDX license

* Tue Dec 26 2023 Ray Strode <rstrode@redhat.com> - 23.360.11-1
- Update to 23.360.11

* Tue Dec 26 2023 Ray Strode <rstrode@redhat.com> - 23.358.4-6
- Various fixes for more minimal installs

* Mon Dec 25 2023 Ray Strode <rstrode@redhat.com> - 23.358.4-5
- Fix systemd integration

* Mon Dec 25 2023 Ray Strode <rstrode@redhat.com> - 23.358.4-4
- Add xkeyboard-config requires for plymouth-scripts too

* Mon Dec 25 2023 Ray Strode <rstrode@redhat.com> - 23.358.4-3
- Add xkeyboard-config requires

* Sun Dec 24 2023 Ray Strode <rstrode@redhat.com> - 23.358.4-2
- New sources

* Sun Dec 24 2023 Ray Strode <rstrode@redhat.com> - 23.358.4-1
- Update to 23.358.4 (fixes initramfs crashers)

* Fri Dec 22 2023 Ray Strode <rstrode@redhat.com> - 23.356.9-4
- Add new build requires

* Fri Dec 22 2023 Ray Strode <rstrode@redhat.com> - 23.356.9-3
- Upload new sources

* Fri Dec 22 2023 Ray Strode <rstrode@redhat.com> - 23.356.9-2
- Add fedora-logos buildrequires

* Fri Dec 22 2023 Ray Strode <rstrode@redhat.com> - 23.356.9-1
- Update to 23.356.9

* Tue Nov 21 2023 Tomas Popela <tpopela@redhat.com> - 22.02.122-7
- Disable charge theme in ELN/RHEL 10

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 22.02.122-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 22.02.122-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Sep 28 2022 Hans de Goede <hdegoede@redhat.com> - 22.02.122-4
- Fix build now that systemd-devel no longer brings in ystemd

* Wed Sep 28 2022 Hans de Goede <hdegoede@redhat.com> - 22.02.122-3
- Fix SimpleDRM sometimes not being ignored (rhbz#2127663)

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 22.02.122-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Mar 07 2022 Hans de Goede <hdegoede@redhat.com> - 22.02.122-1
- New upstream release 22.02.122 (#2039427)

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Dec 06 2021 Hans de Goede <hdegoede@redhat.com> - 0.9.5-4
- Add "Requires: fedora-logos-classic" to the plymouth-theme-charge package

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Mar 31 2021 Hans de Goede <hdegoede@redhat.com> - 0.9.5-2
- New git snapshot Fixes 1933378 - Bootsplash doesn't always fully clear on
  boot to console Fixes 1941329 - Flickering plymouth on shutdown/reboot
  Prune spec-file changelog a bit

* Tue Mar 23 2021 Hans de Goede <hdegoede@redhat.com> - 0.9.5-1
- Update to 0.9.5 + a bunch of extra fixes from git (new upstream git
  snapshot) Fixes 1896929 - systemd complains about Unit configured to use
  KillMode=none

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.4-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Jan 08 2021 Tom Stellard <tstellar@redhat.com> - 0.9.4-18
- Add BuildRequires: make

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.4-17
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.4-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Mar 25 2020 Hans de Goede <hdegoede@redhat.com> - 0.9.4-15
- New upstream git snapshot Add RemainAfterExit=yes to plymouth's systemd
  service files (rhbz#1807771) Fix the spinner / animation missing on
  shutdown and reboot

* Mon Mar 09 2020 Hans de Goede <hdegoede@redhat.com> - 0.9.4-14
- Add patches fixing crash on monitor hot(un)plug (rhbz#1809681) Add
  patches fixing delay between gdm telling us to deactivate and us telling
  gdm it is ok to continue Drop plymouth-plugin-throbgress sub-package, the
  spinfinity theme now uses the two-step plugin

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.4-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Oct 22 2019 Hans de Goede <hdegoede@redhat.com> - 0.9.4-12
- Drop our private plymouth-update-initrd copy, it is identical to upstream
  New upstream git snapshot, with the following fixes: Tweaks to the
  spinner/bgrt themes to match the gdm/gnome-shell lock screen password
  entry style tweaks done in GNOME 3.34 Move the keyboard layout and
  capslock indicator closer to the text field Fix flickering below spinner
  on hidpi displays:
  https://gitlab.freedesktop.org/plymouth/plymouth/issues/83 Add logrotate
  file for /var/log/boot.log so that it does not grow endlessly:
  https://gitlab.freedesktop.org/plymouth/plymouth/issues/31 Some bgrt
  fixes for devices with non-upright mounted LCD panels

* Tue Oct 01 2019 Hans de Goede <hdegoede@redhat.com> - 0.9.4-11
- We are carrying so much patches from upstream that we are practically
  following upstream master, switch to a git snapshot Add keyboard layout
  and capslock state indicator support (rhbz#825406) Fix "Installing
  Updates..." text being rendered all garbled on devices where the panel is
  mounted 90 degrees rotated (rhbz#1753418)

* Sat Sep 07 2019 Hans de Goede <hdegoede@redhat.com> - 0.9.4-10
- Add a patch fixing issues when using cards which default to the radeon
  kms driver with the amdgpu kms driver (rhbz#1490490) Extend default
  DeviceTimeout to 8 seconds (rhbz#1737221)

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.4-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Jul 19 2019 Hans de Goede <hdegoede@redhat.com> - 0.9.4-8
- One more patch for dealing with some devices with a non-upright mounted
  LCD-panel (rhbz#1730783)

* Wed Jun 12 2019 Hans de Goede <hdegoede@redhat.com> - 0.9.4-7
- Add patches from upstream for: Fix failing to pick the native monitor
  mode starting with kernel 5.2 Fix firmware bootsplash support for devices
  which use the new (in ACPI 6.2) rotation bits in the BGRT header Add
  support for firmware-upgrade mode

* Mon Mar 25 2019 Hans de Goede <hdegoede@redhat.com> - 0.9.4-6
- Update bgrt/spinner background to solid black to make the experience on
  systems where we do not show the firmware boot-splash consistent with
  systems where we do show the firmware boot-splash Update translations

* Mon Mar 04 2019 Hans de Goede <hdegoede@redhat.com> - 0.9.4-5
- Add translations for the new spinner/bgrt offline-updates splash

* Wed Feb 13 2019 Hans de Goede <hdegoede@redhat.com> - 0.9.4-4
- Add patches from upstream for: Monitor hotplug support, this fixes issues
  with monitors on DP-MST docs sometimes not lighting up (rhbz#1652279)
  Adding support for using the firmware's bootsplash as theme background
  New bgrt theme which implements the boot-theme design from:
  https://wiki.gnome.org/Design/OS/BootProgress Including the new theming
  for offline-updates shown there Make the bgrt theme the new default and
  upgrade systems which are using the charge theme, which is the old
  default to use the new bgrt theme Cleanup the spec-file a bit: Remove
  unused / unnecessary %%global variables Sort the sections for the various
  plugins and themes alphabetically Simplify theme filelists

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Jan 22 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.9.4-2
- Remove obsolete ldconfig scriptlets

* Mon Nov 05 2018 Ray Strode <rstrode@redhat.com> - 0.9.4-1
- Update to 0.9.4

* Thu Oct 04 2018 Hans de Goede <hdegoede@redhat.com> - 0.9.3-28
- Add patches from upstream to fix the disk unlock screen sometimes having
  a very low resolution on UEFI machines:
  https://gitlab.freedesktop.org/plymouth/plymouth/issues/68

* Mon Aug 06 2018 Hans de Goede <hdegoede@redhat.com> - 0.9.3-27
- Update patches for CONFIG_FRAMEBUFFER_CONSOLE_DEFERRED_TAKEOVER
  interaction to the latest patches from master, this fixes the transition
  from plymouth to gdm being non smooth Drop unused default-boot-duration
  file (rhbz#1456010)

* Thu Aug 02 2018 Peter Robinson <pbrobinson@gmail.com> - 0.9.3-26
- Drop groups in spec, Drop requires on initscripts (rhbz 1592383) long
  migrated to systemd and original bug where it was added (461322) no
  longer relevant

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.3-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jul 09 2018 Igor Gnatenko <ignatenko@redhat.com> - 0.9.3-24
- add BuildRequires: gcc

* Mon Jul 02 2018 Hans de Goede <hdegoede@redhat.com> - 0.9.3-23
- Add patches from upstream fixing details view on kernels build with
  CONFIG_FRAMEBUFFER_CONSOLE_DEFERRED_TAKEOVER

* Thu Jun 07 2018 Adam Williamson <awilliam@redhat.com> - 0.9.3-22
- Move frame-buffer back to subpackage, patch bugs

* Mon Jun 04 2018 Adam Williamson <awilliam@redhat.com> - 0.9.3-21
- Move frame-buffer and drm renderers back to main package

* Fri Jun 01 2018 Adam Williamson <awilliam@redhat.com> - 0.9.3-19
- Move frame-buffer renderer to graphics-libs (#1518464)

* Tue Apr 17 2018 Hans de Goede <hdegoede@redhat.com> - 0.9.3-18
- Merge with F28 branch, fix FTBFS
- Sync in changes which were only added to the F28 branch
- Add a patch from upstream git to fix FTBFS

* Tue Apr 17 2018 Hans de Goede <hdegoede@redhat.com> - 0.9.3-17
- Add patches from upstream git for devices with non upright mounted LCD
  panels https://bugs.freedesktop.org/show_bug.cgi?id=104714

* Tue Mar 27 2018 Colin Walters <walters@verbum.org> - 0.9.3-16
- Drop default boot-duration

* Fri Feb 09 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.9.3-15
- Escape macros in %%changelog

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.3-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Nov 28 2017 Ray Strode <rstrode@redhat.com> - 0.9.3-13
- Bump ShowDelay back up to 5

* Tue Nov 28 2017 Björn Esser <besser82@fedoraproject.org> - 0.9.3-12
- Fix invalid date in %%%%changelog

* Tue Nov 28 2017 Björn Esser <besser82@fedoraproject.org> - 0.9.3-11
- Update to 0.9.3 release Reduce ShowDelay to 0 (rhbz#1518037) Change
  %%%%define to %%%%global

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.3-10
- Rebuilt for
  https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Jun 20 2016 Ray Strode <rstrode@redhat.com> - 0.9.3-7
- misc fixes
- Fix color palette issue
- Fix splash at shutdown (if shutdown takes longer than 5 secs)
- Make sure text based splashes update terminal size when fbcon loads

* Thu Jun 16 2016 Ray Strode <rstrode@redhat.com> - 0.9.3-6
- really (?) fix password prompt on text plugin

* Tue Jun 14 2016 Ray Strode <rstrode@redhat.com> - 0.9.3-5
- fix password prompt on text plugin

* Wed Jun 08 2016 Ray Strode <rstrode@redhat.com> - 0.9.3-4
- new release versioning scheme to be more guideliney

* Tue Jun 07 2016 Ray Strode <rstrode@redhat.com> - 0.9.3-3
- Update to latest git snapshot
- Fixes use after free Related: #1342673

* Tue May 24 2016 Ray Strode <rstrode@redhat.com> - 0.9.3-2
- update build requires

* Tue May 24 2016 Ray Strode <rstrode@redhat.com> - 0.9.3-1
- Update to latest git snapshot

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.9-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Nov 16 2015 Ray Strode <rstrode@redhat.com> - 0.8.9-22
- fix plymouth-update-initrd

* Mon Nov 02 2015 Ray Strode <rstrode@redhat.com> - 0.8.9-21
- Fix updates with script and spinner themes

* Mon Aug 24 2015 Kalev Lember <klember@redhat.com> - 0.8.9-20
- Fix a typo in Requires

* Mon Aug 24 2015 Peter Robinson <pbrobinson@gmail.com> - 0.8.9-19
- fix confusion between scripts and plugin-scripts sub package

* Mon Aug 24 2015 Peter Robinson <pbrobinson@gmail.com> - 0.8.9-18
- Fix Requires for various libs subpackages

* Sun Aug 23 2015 Peter Robinson <pbrobinson@gmail.com> - 0.8.9-17
- Use %%%%license, Cleanup spec, Move drm render driver to graphics-libs
  sub package

* Thu Jun 18 2015 Dennis Gilmore <dennis@ausil.us> - 0.8.9-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed May 20 2015 Will Woods <wwoods@redhat.com> - 0.8.9-15
- add patch for #1223344

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 0.8.9-14
- Rebuilt for Fedora 23 Change

* Sun Aug 17 2014 Peter Robinson <pbrobinson@fedoraproject.org> - 0.8.9-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Jun 13 2014 Adam Jackson <ajax@redhat.com> - 0.8.9-12
- fix changelog date warnings

* Sat Jun 07 2014 Dennis Gilmore <dennis@ausil.us> - 0.8.9-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat May 31 2014 Peter Robinson <pbrobinson@gmail.com> - 0.8.9-10
- Move system-logos dep to graphics-libs (no use on text/serial console
  minimal installs)

* Thu Feb 20 2014 Ray Strode <rstrode@redhat.com> - 0.8.9-9
- Include patch

* Thu Feb 20 2014 Ray Strode <rstrode@redhat.com> - 0.8.9-8
- Fix splash after change in /sys/class/tty/console/active

* Thu Oct 31 2013 Ray Strode <rstrode@redhat.com> - 0.8.9-7
- Don't timeout plymouth quit waiting

* Wed Oct 16 2013 Ray Strode <rstrode@redhat.com> - 0.8.9-6
- need an explicit --without-rhgb-compat-link

* Wed Oct 16 2013 Ray Strode <rstrode@redhat.com> - 0.8.9-5
- drop rhgb-client compat link

* Sun Oct 06 2013 Kalev Lember <kalevlember@gmail.com> - 0.8.9-4
- Make sure the release number compares higher than the previous builds

* Wed Aug 14 2013 Ray Strode <rstrode@redhat.com> - 0.8.9-3
- Update to snapshot to fix system units

* Sun Aug 04 2013 Dennis Gilmore <dennis@ausil.us> - 0.8.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Mar 26 2013 Ray Strode <rstrode@redhat.com> - 0.8.9-1
- Update to snapshot to fix systemd vconsole issue

* Thu Feb 21 2013 Peter Robinson <pbrobinson@gmail.com> - 0.8.8-6
- RPMAUTOSPEC: unresolvable merge
## END: Generated by rpmautospec
