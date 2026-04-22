## START: Set by rpmautospec
## (rpmautospec version 0.8.4)
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
* Wed Apr 22 2026 azldev <azurelinux@microsoft.com> - 24.004.60-25
- Latest state for plymouth

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
