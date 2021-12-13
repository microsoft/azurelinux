%global commit e31c81f9849c176d7b293ca79cc4507ba740c2fa
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Summary: Graphical Boot Animation and Logger
Name: plymouth
Version: 0.9.4
Release: 16%{?dist}
License: GPLv2+
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL: http://www.freedesktop.org/wiki/Software/Plymouth

Source0: https://gitlab.freedesktop.org/plymouth/plymouth/-/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
Source2: charge.plymouth

# Upstream has bumped the soname because some obscure symbols were dropped,
# but we really do not want to change soname in Fedora during a cycle.
# The only libply* user in Fedora outside this pkg is plymouth-theme-breeze
# and that does not need the removed symbols.
Patch0: 0001-Revert-configure-bump-so-name.patch

BuildRequires: gcc libtool git
BuildRequires: pkgconfig(libdrm)
BuildRequires: pkgconfig(libudev)
BuildRequires: kernel-headers
BuildRequires: libpng-devel
BuildRequires: libxslt, docbook-style-xsl
BuildRequires: pkgconfig(gtk+-3.0)
BuildRequires: pango-devel >= 1.21.0
BuildRequires: pkgconfig(cairo)
BuildRequires: gettext-devel
BuildRequires: intltool

Requires: %{name}-core-libs = %{version}-%{release}
Requires: %{name}-scripts = %{version}-%{release}
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


%package theme-charge
Summary: Plymouth "Charge" plugin
Requires: %{name}-plugin-two-step = %{version}-%{release}
Requires(post): plymouth-scripts

%description theme-charge
This package contains the "charge" boot splash theme for
Plymouth. It features the shadowy hull of a Fedora logo charge up and
and finally burst into full form.


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
Requires: font(cantarell) font(cantarelllight)
Requires(post): plymouth-scripts
Provides: plymouth(system-theme) = %{version}-%{release}

%description theme-spinner
This package contains the "spinner" boot splash theme for
Plymouth. It features a small spinner on a dark background.


%prep
%autosetup -p1 -n %{name}-%{commit}
autoreconf --install --symlink -Wno-portability
# Change the default theme
sed -i -e 's/spinner/bgrt/g' src/plymouthd.defaults


%build
%configure --enable-tracing                                      \
           --with-logo=%{_datadir}/pixmaps/system-logo-white.png \
           --with-background-start-color-stop=0x0073B3           \
           --with-background-end-color-stop=0x00457E             \
           --with-background-color=0x3391cd                      \
           --with-runtimedir=/run                                \
           --disable-gdm-transition                              \
           --enable-systemd-integration                          \
           --without-system-root-install                         \
           --without-rhgb-compat-link
%make_build


%install
%make_install
%find_lang %{name}
find $RPM_BUILD_ROOT -name '*.la' -delete

mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/lib/plymouth

# Add charge, our old default
mkdir -p $RPM_BUILD_ROOT%{_datadir}/plymouth/themes/charge
cp %{SOURCE2} $RPM_BUILD_ROOT%{_datadir}/plymouth/themes/charge
cp $RPM_BUILD_ROOT%{_datadir}/plymouth/themes/glow/{box,bullet,entry,lock}.png $RPM_BUILD_ROOT%{_datadir}/plymouth/themes/charge

# Drop glow, it's not very Fedora-y
rm -rf $RPM_BUILD_ROOT%{_datadir}/plymouth/themes/glow


%ldconfig_scriptlets core-libs

%ldconfig_scriptlets graphics-libs

%postun theme-charge
export PLYMOUTH_PLUGIN_PATH=%{_libdir}/plymouth/
if [ $1 -eq 0 ]; then
    if [ "$(%{_sbindir}/plymouth-set-default-theme)" == "charge" ]; then
        %{_sbindir}/plymouth-set-default-theme --reset
    fi
fi

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
%doc AUTHORS README
%dir %{_datadir}/plymouth
%dir %{_datadir}/plymouth/themes
%dir %{_datadir}/plymouth/themes/details
%dir %{_datadir}/plymouth/themes/text
%dir %{_libexecdir}/plymouth
%dir %{_localstatedir}/lib/plymouth
%dir %{_libdir}/plymouth/renderers
%dir %{_sysconfdir}/plymouth
%config(noreplace) %{_sysconfdir}/plymouth/plymouthd.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/bootlog
%{_sbindir}/plymouthd
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
%ghost %{_localstatedir}/lib/plymouth/boot-duration
%{_prefix}/lib/systemd/system/

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
%{_libdir}/plymouth/label.so

%files plugin-script
%{_libdir}/plymouth/script.so

%files plugin-fade-throbber
%{_libdir}/plymouth/fade-throbber.so

%files plugin-space-flares
%{_libdir}/plymouth/space-flares.so

%files plugin-two-step
%{_libdir}/plymouth/two-step.so

%files theme-charge
%{_datadir}/plymouth/themes/charge

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
* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.9.4-16
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Thu Jun 17 2021 Thomas Crain <thcrain@microsoft.com> - 0.9.4-15.20200306git58a7289
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Use pkgconfig(cairo) build requirement instead of cairo-devel

* Wed Mar 25 2020 Hans de Goede <jwrdegoede@fedoraproject.org> - 0.9.4-14.20200306git58a7289
- New upstream git snapshot
- Add RemainAfterExit=yes to plymouth's systemd service files (rhbz#1807771)
- Fix the spinner / animation missing on shutdown and reboot

* Mon Mar  9 2020 Hans de Goede <jwrdegoede@fedoraproject.org> - 0.9.4-13.20200306git58a7289
- Add patches fixing crash on monitor hot(un)plug (rhbz#1809681)
- Add patches fixing delay between gdm telling us to deactivate and
  us telling gdm it is ok to continue
- Drop plymouth-plugin-throbgress sub-package, the spinfinity theme now
  uses the two-step plugin

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.4-12.20191022git32c097c
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Oct 22 2019 Hans de Goede <jwrdegoede@fedoraproject.org> - 0.9.4-11.20191022git32c097c
- Drop our private plymouth-update-initrd copy, it is identical to upstream
- New upstream git snapshot, with the following fixes:
- Tweaks to the spinner/bgrt themes to match the gdm/gnome-shell lock screen
  password entry style tweaks done in GNOME 3.34
- Move the keyboard layout and capslock indicator closer to the text field
- Fix flickering below spinner on hidpi displays:
  https://gitlab.freedesktop.org/plymouth/plymouth/issues/83
- Add logrotate file for /var/log/boot.log so that it does not grow endlessly:
  https://gitlab.freedesktop.org/plymouth/plymouth/issues/31
- Some bgrt fixes for devices with non-upright mounted LCD panels

* Tue Oct  1 2019 Hans de Goede <jwrdegoede@fedoraproject.org> - 0.9.4-10.20191001gita8aad27
- We are carrying so much patches from upstream that we are practically
  following upstream master, switch to a git snapshot
- Add keyboard layout and capslock state indicator support (rhbz#825406)
- Fix "Installing Updates..." text being rendered all garbled on devices
  where the panel is mounted 90 degrees rotated (rhbz#1753418)

* Sat Sep  7 2019 Hans de Goede <jwrdegoede@fedoraproject.org> - 0.9.4-9
- Add a patch fixing issues when using cards which default to the radeon
  kms driver with the amdgpu kms driver (rhbz#1490490)
- Extend default DeviceTimeout to 8 seconds (rhbz#1737221)

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.4-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Jul 19 2019 Hans de Goede <jwrdegoede@fedoraproject.org> - 0.9.4-7
- One more patch for dealing with some devices with a non-upright mounted
  LCD-panel (rhbz#1730783)

* Wed Jun 12 2019 Hans de Goede <jwrdegoede@fedoraproject.org> - 0.9.4-6
- Add patches from upstream for:
  - Fix failing to pick the native monitor mode starting with kernel 5.2
  - Fix firmware bootsplash support for devices which use the new
    (in ACPI 6.2) rotation bits in the BGRT header
  - Add support for firmware-upgrade mode

* Mon Mar 25 2019 Hans de Goede <jwrdegoede@fedoraproject.org> - 0.9.4-5
- Update bgrt/spinner background to solid black to make the experience on
  systems where we do not show the firmware boot-splash consistent with
  systems where we do show the firmware boot-splash
- Update translations

* Mon Mar  4 2019 Hans de Goede <jwrdegoede@fedoraproject.org> - 0.9.4-4
- Add translations for the new spinner/bgrt offline-updates splash

* Wed Feb 13 2019 Hans de Goede <jwrdegoede@fedoraproject.org> - 0.9.4-3
- Add patches from upstream for:
  - Monitor hotplug support, this fixes issues with monitors on DP-MST
    docs sometimes not lighting up (rhbz#1652279)
  - Adding support for using the firmware's bootsplash as theme background
  - New bgrt theme which implements the boot-theme design from:
    https://wiki.gnome.org/Design/OS/BootProgress
    Including the new theming for offline-updates shown there
- Make the bgrt theme the new default and upgrade systems which are using the
  charge theme, which is the old default to use the new bgrt theme
- Cleanup the spec-file a bit:
  - Remove unused / unnecessary %%global variables
  - Sort the sections for the various plugins and themes alphabetically
  - Simplify theme filelists

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Nov 05 2018 Ray Strode <rstrode@redhat.com> - 0.9.4-1
- Update to 0.9.4

* Thu Oct 04 2018 Hans de Goede <jwrdegoede@fedoraproject.org> - 0.9.3-14
- Add patches from upstream to fix the disk unlock screen sometimes having
  a very low resolution on UEFI machines:
  https://gitlab.freedesktop.org/plymouth/plymouth/issues/68

* Mon Aug 06 2018 Hans de Goede <jwrdegoede@fedoraproject.org> - 0.9.3-13
- Update patches for CONFIG_FRAMEBUFFER_CONSOLE_DEFERRED_TAKEOVER interaction
  to the latest patches from master, this fixes the transition from plymouth
  to gdm being non smooth
- Drop unused default-boot-duration file (rhbz#1456010)

* Thu Aug  2 2018 Peter Robinson <pbrobinson@fedoraproject.org> 0.9.3-12
- Drop groups in spec
- Drop requires on initscripts (rhbz 1592383)

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.3-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jul 02 2018 Hans de Goede <jwrdegoede@fedoraproject.org> - 0.9.3-10
- Add patches from upstream fixing details view on kernels build with
  CONFIG_FRAMEBUFFER_CONSOLE_DEFERRED_TAKEOVER

* Wed Jun 06 2018 Adam Williamson <awilliam@redhat.com> - 0.9.3-9
- Backport patch to avoid loading renderers on non-rhgb boot
- Backport patch to handle 'rhgb' but no renderers available
- Move frame-buffer rendererer back to graphics-libs subpackage

* Mon Jun 04 2018 Adam Williamson <awilliam@redhat.com> - 0.9.3-8
- Move frame-buffer and drm renderers back to main package
  Having both in subpackage breaks minimal installs with rhgb

* Fri Jun 01 2018 Adam Williamson <awilliam@redhat.com> - 0.9.3-7
- Move frame-buffer renderer to graphics-libs
- Resolves: #1518464

* Sun Apr 15 2018 Hans de Goede <jwrdegoede@fedoraproject.org> - 0.9.3-6
- Add patches from upstream git for devices with non upright mounted LCD panels
  https://bugs.freedesktop.org/show_bug.cgi?id=104714

* Thu Mar 29 2018 Colin Walters <walters@verbum.org> - 0.9.3-5
- Drop default boot duration: https://src.fedoraproject.org/rpms/plymouth/pull-request/1

* Fri Feb 09 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.9.3-4
- Escape macros in %%changelog

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Nov 28 2017 Ray Strode - 0.9.3-2
- Bump ShowDelay back up to 5
  Related: #1518037

* Tue Nov 28 2017 Björn Esser <besser82@fedoraproject.org> - 0.9.3-1
- Update to 0.9.3 release
- Reduce ShowDelay to 0 (rhbz#1518037)
- Change %%define to %%global

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.3-0.9.20160620git0e65b86c
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.3-0.8.20160620git0e65b86c
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.3-0.7.20160620git0e65b86c
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Jun 20 2016 Ray Strode <rstrode@redhat.com> - 0.9.3-0.6.git
- Fix color palette issue
- Fix splash at shutdown (if shutdown takes longer than 5 secs)
- Make sure text based splashes update terminal size when fbcon loads

* Thu Jun 16 2016 Ray Strode <rstrode@redhat.com> - 0.9.3-0.5.git
- really (?) fix password prompt on text plugin
  Resolves: #1344141

* Tue Jun 14 2016 Ray Strode <rstrode@redhat.com> - 0.9.3-0.4.git
- fix password prompt on text plugin
  Resolves: #1344141

* Wed Jun 08 2016 Ray Strode <rstrode@redhat.com> - 0.9.3-0.3.git
- new release versioning scheme to be more guideliney

* Tue Jun 07 2016 Ray Strode <rstrode@redhat.com> - 0.9.3-0.1.
- Update to latest git snapshot
- Fixes use after free
  Related: #1342673

* Tue May 24 2016 Ray Strode <rstrode@redhat.com> - 0.9.3-0.1.20160524
- Update to latest git snapshot
- Drop plymouth-generate-initrd scriptlets

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.9-17.2013.08.14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sun Nov 15 2015 Ray Strode <rstrode@redhat.com> 0.8.9-16.2013.08.14
- Fix plymouth-update-initrd script

* Mon Oct 26 2015 Ray Strode <rstrode@redhat.com> 0.8.9-15.2013.08.15
- Fix updates with script and spinner themes
  Resolves: #1267949

* Mon Aug 24 2015 Kalev Lember <klember@redhat.com> 0.8.9-13.2013.08.14
- Fix a typo in Requires

* Mon Aug 24 2015 Peter Robinson <pbrobinson@fedoraproject.org> 0.8.9-12.2013.08.14
- Fix Requires for various libs subpackages

* Sun Aug 23 2015 Peter Robinson <pbrobinson@fedoraproject.org> 0.8.9-11.2013.08.14
- Use %%license
- Cleanup spec
- Move drm render driver to graphics-libs sub package

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.9-10.2013.08.14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed May 20 2015 Will Woods <wwoods@redhat.com> 0.8.9-9.2013.08.14
- Fix theme override using PLYMOUTH_THEME_NAME (#1223344)

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 0.8.9-8.2013.08.14
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.9-7.2013.08.14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.9-6.2013.08.14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat May 31 2014 Peter Robinson <pbrobinson@fedoraproject.org> 0.8.9-4.2013.08.15
- Move system-logos dep to graphics-libs (no use on text/serial console minimal installs)

* Thu Feb 20 2014 Ray Strode <rstrode@redhat.com> 0.8.9-4.2013.08.14
- Fix splash after change in /sys/class/tty/console/active

* Thu Oct 31 2013 Ray Strode <rstrode@redhat.com> 0.8.9-3.2013.08.14
- Don't timeout plymouth quit waiting
  Related: #967521

* Wed Oct 16 2013 Ray Strode <rstrode@redhat.com> 0.8.9-2.2013.08.14
- Drop rhgb-client compat link

* Sun Oct 06 2013 Kalev Lember <kalevlember@gmail.com> - 0.8.9-1.2013.08.14
- Make sure the release number compares higher than the previous builds

* Wed Aug 14 2013 Ray Strode <rstrode@redhat.com> 0.8.9-0.1.2013.08.14.0
- Update to snapshot to fix system units

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.9-0.2014.03.26.0
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Mar 26 2013 Ray Strode <rstrode@redhat.com> 0.8.9-0.2013.03.26.0
- Update to snapshot to fix systemd vconsole issue

* Thu Feb 21 2013 Peter Robinson <pbrobinson@fedoraproject.org> 0.8.8-6
- Merge newer F18 release into rawhide

* Thu Dec 13 2012 Ray Strode <rstrode@redhat.com> 0.8.8-5
- Ensure fedup gets right splash screen
  Related: #879295

* Thu Nov 15 2012 Ray Strode <rstrode@redhat.com> 0.8.8-4
- Drop set-default-plugin compat script
- Just use upstream update-initrd

* Fri Nov 02 2012 Ray Strode <rstrode@redhat.com> 0.8.8-3
- More boot blocking fixes
  Related: #870695

* Thu Nov 01 2012 Ray Strode <rstrode@redhat.com> 0.8.8-2
- Fix crash when deactivating multiple times
  Related: #870695

* Fri Oct 26 2012 Ray Strode <rstrode@redhat.com> 0.8.8-1
- Latest upstream release
- includes systemd fixes and system update fixes

* Tue Aug 21 2012 Ray Strode <rstrode@redhat.com> 0.8.7-1
- Latest upstream release
- includes systemd fixes

* Tue Aug 21 2012 Dave Airlie <airlied@redhat.com> 0.8.6.2-1.2012.07.23
- fix plymouth race at bootup breaking efi/vesa handoff.
- fix version number - its against fedora package policy to have 0.year

* Mon Jul 23 2012 Ray Strode <rstrode@redhat.com> 0.8.6.2-0.2012.07.23
- One more crack at #830482 (will probably need additional fixes tomorrow)

* Mon Jul 23 2012 Tom Callaway <spot@fedoraproject.org> - 0.8.6.1-3
- fix bz704658 (thanks to Ian Pilcher for the patch), resolves issue where spinfinity theme
  never goes idle and thus, never exits to gdm

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 10 2012 Ray Strode <rstrode@redhat.com> 0.8.6.1-1
- Update to 0.8.6.1 since I mucked up 0.8.6
  Resolves: #830482

* Mon Jul 09 2012 Ray Strode <rstrode@redhat.com> 0.8.6-1
- Update to 0.8.6
- Fixes encrypted fs bug
  Resolves: #830482
- Adds support for offline package updates

* Mon Jun 25 2012 Adam Jackson <ajax@redhat.com> 0.8.5.1-3
- Rebuild without libkms

* Wed Jun 06 2012 Ray Strode <rstrode@redhat.com> 0.8.5.1-2
- Add %%{_prefix} to systemd service path

* Wed Jun 06 2012 Ray Strode <rstrode@redhat.com> 0.8.5.1-1
- Update to latest release
- Ship systemd service files
- Conflict with old systemd

* Tue Apr 24 2012 Richard Hughes <rhughes@redhat.com> 0.8.4-0.20120319.3
- Disable the nouveau driver as I've broken it with the new libdrm ABI

* Tue Mar 20 2012 Daniel Drake <dsd@laptop.org> 0.8.4-0.20120319.1
- Don't try to build against libdrm_intel on non-intel architectures

* Mon Mar 19 2012 Ray Strode <rstrode@redhat.com> 0.8.4-0.20120319.1
- Update to latest snapshot

* Mon Mar 12 2012 Ray Strode <rstrode@redhat.com> 0.8.4-0.20110810.6
- Don't require libdrm_intel on non intel arches

* Mon Feb 20 2012 Adam Williamson <awilliam@redhat.com> 0.8.4-0.20110810.5
- make plymouth-scripts require plymouth (RH #794894)

* Wed Jan 25 2012 Harald Hoyer <harald@redhat.com> 0.8.4-0.20110810.4
- install everything in /usr
  https://fedoraproject.org/wiki/Features/UsrMove

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.4-0.20110810.3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Dec 15 2011 Ray Strode <rstrode@redhat.com> 0.8.4-0.20110809.3
- Change spec based on suggestion from Nicolas Chauvet <kwizart@gmail.com>
  to fix scriptlet error during livecd creation
  Resolves: #666419

* Tue Nov 08 2011 Adam Jackson <ajax@redhat.com> 0.8.4-0.20110822.3
- Rebuild for libpng 1.5

* Fri Sep 02 2011 Ray Strode <rstrode@redhat.com> 0.8.4-0.20110822.2
- Make plymouth background dark gray at the request of Mo / design
  team.

* Mon Aug 22 2011 Ray Strode <rstrode@redhat.com> 0.8.4-0.20110822.1
- Update to latest git snapshot
- Reintroduce accidentally dropped spinner theme and systemd integration

* Tue Aug 09 2011 Ray Strode <rstrode@redhat.com> 0.8.4-0.20110809.1
- Rebuild

* Fri Mar 04 2011 Ray Strode <rstrode@redhat.com> 0.8.4-0.1.20110304.1
- retry reopening tty if we get EIO
  Hopefully Resolves: #681167

* Fri Feb 18 2011 Ray Strode <rstrode@redhat.com> 0.8.4-0.20110419.1
- unlock tty when reopening in case it spontaenously goes bonkers
  and we need to fix it up
  Resolves: #655538

* Wed Feb 09 2011 Christopher Aillon <caillon@redhat.com> 0.8.4-0.20110209.2
- Fix up obsoletes typo

* Wed Feb 09 2011 Ray Strode <rstrode@redhat.com> 0.8.4-0.20110209.1
- Update to latest snapshot

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.4-0.20101120.4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Feb 04 2011 Ray Strode <rstrode@redhat.com> 0.8.4-0.20101119.4
- Drop log viewer

* Sat Jan 29 2011 Ville Skyttä <ville.skytta@iki.fi> - 0.8.4-0.20101119.3
- Dir ownership fixes (#645044).

* Fri Nov 19 2010 Ray Strode <rstrode@redhat.com> 0.8.4-0.20101119.2
- Fix serial console issue eparis was seeing

* Fri Nov 19 2010 Ray Strode <rstrode@redhat.com> 0.8.4-0.20101119.1
- Update to recent snapshot

* Tue Nov 02 2010 Ray Strode <rstrode@redhat.com> 0.8.4-0.20101002.1
- Update to recent snapshot

* Wed Sep 01 2010 Ray Strode <rstrode@redhat.com> 0.8.4-0.20100823.4
- Add more Requirse

* Thu Aug 26 2010 Ray Strode <rstrode@redhat.com> 0.8.4-0.20100823.3
- Add more Requires

* Thu Aug 26 2010 Ray Strode <rstrode@redhat.com> 0.8.4-0.20100823.2
- Fix plymouth-update-initrd
  It's regressed to the pre-dracut version.  This commit fixes that.

* Mon Aug 23 2010 Ray Strode <rstrode@redhat.com> 0.8.4-0.20100823.1
- Update to newer pre-release snapshot of 0.8.4
- Generate separate initrd in /boot

* Sat Aug 21 2010 Ray Strode <rstrode@redhat.com> 0.8.4-0.20100821.1
- Update to newer pre-release snapshot of 0.8.4
- Fix bizarre-o animation during boot up.

* Fri Jul 23 2010 Ray Strode <rstrode@redhat.com> 0.8.4-0.20100723.1
- Update to pre-release snapshot of 0.8.4

* Thu Jan 14 2010 Ray Strode <rstrode@redhat.com> 0.8.0-0.20100114.2
- Don't link plymouthd against libpng either

* Thu Jan 14 2010 Ray Strode <rstrode@redhat.com> 0.8.0-0.20100114.1
- Make it possible to do a basic plymouth installations without
  libpng

* Thu Jan 07 2010 Ray Strode <rstrode@redhat.com> 0.8.0-0.2009129.2
- Drop nash dep

* Tue Dec 22 2009 Dave Airlie <airlied@redhat.com> 0.8.0-0.2009129.1
- rebuild for API bump in libdrm

* Wed Dec 09 2009 Ray Strode <rstrode@redhat.com> 0.8.0-0.2009129
- Update to latest snapshot

* Tue Sep 29 2009 Ray Strode <rstrode@redhat.com> 0.8.0-0.2009.10.05
- Add new x11-renderer plugin from Charlie Brej for debugging

* Tue Sep 29 2009 Ray Strode <rstrode@redhat.com> 0.8.0-0.2009.29.09
- Fix escape and ask-for-password

* Mon Sep 28 2009 Ray Strode <rstrode@redhat.com> 0.8.0-0.2009.28.09
- Add prerelease of 0.8.0 for multihead support

* Fri Sep 11 2009 Ray Strode <rstrode@redhat.com> 0.7.1-7
- Go back to blue charge background (bug 522460)

* Fri Sep 11 2009 Ray Strode <rstrode@redhat.com> 0.7.1-6
- Remove duplicate Provides: plymouth(system-theme)

* Thu Sep 10 2009 Ray Strode <rstrode@redhat.com> 0.7.1-5
- Fix set_verbose error reported by yaneti.

* Wed Sep  9 2009 Ray Strode <rstrode@redhat.com> 0.7.1-4
- Look for inst() in dracut as well as mkinitrd bash source file
- Drop plymouth initrd for now.

* Fri Aug 28 2009 Ray Strode <rstrode@redhat.com> 0.7.1-3
- Create plymouth supplementary initrd in post (bug 515589)

* Tue Aug 25 2009 Ray Strode <rstrode@redhat.com> 0.7.1-2
- Get plugin path from plymouth instead of trying
  to guess.  Should fix bug 502667

* Tue Aug 25 2009 Ray Strode <rstrode@redhat.com> 0.7.1-1
- Update to 0.7.1

* Mon Aug 24 2009 Adam Jackson <ajax@redhat.com> 0.7.0-2
- Set charge bgcolor to black. (#519052)

* Tue Aug 11 2009 Ray Strode <rstrode@redhat.com> 0.7.0-1
- Update to 0.7.0

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.0-0.2010.05.15.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri May 15 2009 Ray Strode <rstrode@redhat.com> 0.7.0-0.2009.05.15.1
- Fix spinfinity theme to point to the right image directory
  (bug 500994)

* Thu May 14 2009 Ray Strode <rstrode@redhat.com> 0.7.0-0.2009.05.14.1
- Update to new snapshot that renames plugins to fix upgrades
  somewhat (bug 499940)

* Fri May 08 2009 Ray Strode <rstrode@redhat.com> 0.7.0-0.2009.05.08.1
- Add some fixes for shutdown

* Fri May 08 2009 Ray Strode <rstrode@redhat.com> 0.7.0-0.2009.05.06.4
- Don't slow down progress updating at the end of boot

* Thu May 07 2009 Ray Strode <rstrode@redhat.com> 0.7.0-0.2009.05.06.3
- Change colors to transition better to gdm

* Wed May 06 2009 Ray Strode <rstrode@redhat.com> 0.7.0-0.2009.05.06.2
- Make "charge" theme require two-step plugin instead of solar (oops)

* Wed May 06 2009 Ray Strode <rstrode@redhat.com> 0.7.0-0.2009.05.06.1
- Update to "plugin-rework" branch from git

* Wed Apr 08 2009 Jesse Keating <jkeating@redhat.com> - 0.7.0-0.2009.03.10.3
- Drop the version on system-logos requires for now, causing hell with
  other -logos providers not having the same version.

* Wed Mar 18 2009 Ray Strode <rstrode@redhat.com> 0.7.0-0.2009.03.10.2
- Destroy terminal on detach (may help with bug 490965)

* Tue Mar 10 2009 Ray Strode <rstrode@redhat.com> 0.7.0-0.2009.03.10.1
- Address one more issue with password handling.  It wasn't working
  well for secondary devices when using the "details" plugin.

* Mon Mar  9 2009 Ray Strode <rstrode@redhat.com> 0.7.0-0.2009.03.09.1
- Attempt to address some problems with password handling in the
  0.7.0 snapshots

* Fri Mar  6 2009 Ray Strode <rstrode@redhat.com> 0.7.0-0.2009.03.06.2
- Fix set default script

* Fri Mar  6 2009 Ray Strode <rstrode@redhat.com> 0.7.0-0.2009.03.06.1
- more scriptlet changes to move from solar to spinfinity

* Fri Mar  6 2009 Ray Strode <rstrode@redhat.com> 0.7.0-0.2009.03.06
- Updated to development snapshot
- Guess progress better on second boot of persistent live images
- Drop upstream patches
- swap "solar" and "spinfinity" scriptlet behavior

* Tue Feb 24 2009 Ray Strode <rstrode@redhat.com> 0.6.0-3
- Add fix-heap-corruptor patch from master.  Problem
  spotted by Mr. McCann.

* Wed Dec 17 2008 Ray Strode <rstrode@redhat.com> 0.6.0-2
- Add patch from drop-nash branch for jeremy

* Wed Dec  3 2008 Ray Strode <rstrode@redhat.com> 0.6.0-1
- Update to 0.6.0

* Sat Nov 22 2008 Matthias Clasen <mclasen@redhat.com> 0.6.0-0.2008.11.17.3.1
- Strip %%name from %%summary

* Mon Nov 17 2008 Ray Strode <rstrode@redhat.com> 0.6.0-0.2008.11.17.3
- don't give error about missing default.so
- rework packaging of boot-duration to prevent .rpmnew droppings
  (bug 469752)

* Mon Nov 17 2008 Ray Strode <rstrode@redhat.com> 0.6.0-0.2008.11.17.2
- Don't tell gdm to transition unless booting into runlevel 3
  (bug 471785)

* Mon Nov 17 2008 Ray Strode <rstrode@redhat.com> 0.6.0-0.2008.11.17.1
- Crawl progress bar if boot is way off course (Charlie, bug 471089)

* Fri Nov 14 2008 Ray Strode <rstrode@redhat.com> 0.6.0-0.2008.11.14.2
- Don't loop forever when tty returns NUL byte (bug 471498)

* Fri Nov 14 2008 Ray Strode <rstrode@redhat.com> 0.6.0-0.2008.11.14.1
- Generate solar background dynamically to reduce ondisk size, and
  look better at various resolutions (Charlie, bug 471227)

* Thu Nov 13 2008 Ray Strode <rstrode@redhat.com> 0.6.0-0.2008.11.12.4
- Move Obsoletes: plymouth-text-and-details-only to base package
  so people who had it installed don't end up solar on upgrade

* Wed Nov 12 2008 Ray Strode <rstrode@redhat.com> 0.6.0-0.2008.11.12.3
- Redo packaging to work better with minimal installs
  (bug 471314)

* Wed Nov 12 2008 Ray Strode <rstrode@redhat.com> 0.6.0-0.2008.11.12.2
- Fix plymouth-set-default-plugin to allow external $LIB

* Wed Nov 12 2008 Ray Strode <rstrode@redhat.com> 0.6.0-0.2008.11.12.1
- Fix star image (Charlie, bug 471113)

* Tue Nov 11 2008 Ray Strode <rstrode@redhat.com> 0.6.0-0.2008.11.11.2
- Improve solar flares (Charlie)
- redirect tty again on --show-splash
- ignore subsequent --hide-splash calls after the first one
- turn off kernel printks during boot up

* Tue Nov 11 2008 Ray Strode <rstrode@redhat.com> 0.6.0-0.2008.11.11.1
- Disconnect from tty when init=/bin/bash (bug 471007)

* Mon Nov 10 2008 Ray Strode <rstrode@redhat.com> 0.6.0-0.2008.11.10.5
- Force the right arch when calling plymouth-set-default-plugin
  (bug 470732)

* Mon Nov 10 2008 Ray Strode <rstrode@redhat.com> 0.6.0-0.2008.11.10.4
- Drop comet (bug 468705)
- make boot-duration config(noreplace)

* Mon Nov 10 2008 Ray Strode <rstrode@redhat.com> 0.6.0-0.2008.11.10.3
- Don't abort if no splash when root is mounted
- Actually move patches upstream

* Mon Nov 10 2008 Ray Strode <rstrode@redhat.com> 0.6.0-0.2008.11.10.1
- Fix feedback loop with plymouth:debug
- Move patches upstream
- Improve comet animation

* Sun Nov  9 2008 Ray Strode <rstrode@redhat.com> 0.6.0-0.2008.11.06.4
- Fix up more-debug patch to not assert with plymouth:nolog
  (bug 470569)

* Fri Nov  7 2008 Ray Strode <rstrode@redhat.com> 0.6.0-0.2008.11.06.3
- add some more debug spew to help debug a problem jlaska is having

* Thu Nov  6 2008 Ray Strode <rstrode@redhat.com> 0.6.0-0.2008.11.06.2
- show details plugin on --hide-splash so people can see why the splash
  got hidden.

* Thu Nov  6 2008 Ray Strode <rstrode@redhat.com> 0.6.0-0.2008.11.06.1
- Don't exit on plymouth --show-splash after sulogin
- Properly retake console after that --show-splash

* Wed Nov  5 2008 Ray Strode <rstrode@redhat.com> 0.6.0-0.2008.11.05.1
- reset colors on quit --retain-splash
- fix off by one in damage calculation for label

* Tue Nov  4 2008 Ray Strode <rstrode@redhat.com> 0.6.0-0.2008.10.30.5
- Add a sample boot-duration for livecds and first time boots
  (bug 469752)

* Mon Nov  3 2008 Jeremy Katz <katzj@redhat.com> - 0.6.0-0.2008.10.30.4
- Allow pre-setting the default plugin when calling plymouth-populate-initrd

* Fri Oct 31 2008 Ray Strode <rstrode@redhat.com> 0.6.0-0.2008.10.30.3
- Add pango minimum version to buildrequires

* Thu Oct 30 2008 Ray Strode <rstrode@redhat.com> 0.6.0-0.2008.10.30.2
- Update prompt text colors to be legible on new artwork

* Thu Oct 30 2008 Ray Strode <rstrode@redhat.com> 0.6.0-0.2008.10.30.1
- Drop upstreamed patches
- Patch from Charlie to update artwork
- Patch from Charlie to make password screen match animation better
  (bug 468899)

* Thu Oct 30 2008 Ray Strode <rstrode@redhat.com> 0.6.0-0.2008.10.27.8
- Fix escape at password prompt (bug 467533)

* Tue Oct 28 2008 Ray Strode <rstrode@redhat.com> 0.6.0-0.2008.10.27.7
- Don't require /bin/plymouth before it's installed (bug 468925)

* Tue Oct 28 2008 Ray Strode <rstrode@redhat.com> 0.6.0-0.2008.10.27.6
- Force raw mode for keyboard input with solar and fade-in
  (bug 468880)
- make sure windows get closed on exit

* Mon Oct 27 2008 Ray Strode <rstrode@redhat.com> 0.6.0-0.2008.10.27.5
- Make "Solar" lock icon the same as the "Spinfinity" one.

* Mon Oct 27 2008 Ray Strode <rstrode@redhat.com> 0.6.0-0.2008.10.27.4
- Make plymouth-libs own /usr/lib/plymouth (bug 458071)

* Mon Oct 27 2008 Ray Strode <rstrode@redhat.com> 0.6.0-0.2008.10.27.3
- Default to "Solar" instead of "Spinfinity"

* Mon Oct 27 2008 Ray Strode <rstrode@redhat.com> 0.6.0-0.2008.10.27.2
- Don't set plymouth default plugin to text in %%post

* Mon Oct 27 2008 Ray Strode <rstrode@redhat.com> 0.6.0-0.2008.10.27.1
- Add Charlie patch to dither in lower color modes (bug 468276)

* Sun Oct 26 2008 Jeremy Katz <katzj@redhat.com> - 0.6.0-0.2008.10.24.2
- More requires changing to avoid loops (#467356)

* Fri Oct 24 2008 Ray Strode <rstrode@redhat.com> 0.6.0-0.2008.10.24.1
- Add updated progress bar for solar plugin from Charlie
- Log plymouth:debug output to boot log
- Ignore sigpipe signals in daemon

* Thu Oct 23 2008 Ray Strode <rstrode@redhat.com> 0.6.0-0.2008.10.23.2
- Bump so name of libply to hopefully force plymouth to get installed
  before kernel (or at least make plymouth-libs and plymouth get installed
  on the same side of kernel in the transaction).

* Thu Oct 23 2008 Ray Strode <rstrode@redhat.com> 0.6.0-0.2008.10.23.1
- Add patch from Charlie to align progress bar to milestones during boot up
- force tty to be sane on exit (bug 467207)

* Thu Oct 23 2008 Ray Strode <rstrode@redhat.com> 0.6.0-0.2008.10.21.3
- add empty files section for text-and-details-only so the subpackage
  shows up.

* Wed Oct 22 2008 Ray Strode <rstrode@redhat.com> 0.6.0-0.2008.10.21.2
- add text-and-details-only subpackage so davej can uninstall
  spinfinity, pango, cairo etc from his router.

* Tue Oct 21 2008 Ray Strode <rstrode@redhat.com> 0.6.0-0.2008.10.21.1
- Minor event loop changes
- drop upstream patches
- Charlie Brej fix for progress bar resetting when escape gets pressed

* Tue Oct 21 2008 Ray Strode <rstrode@redhat.com> 0.6.0-0.2008.10.17.4
- Don't make plymouth-libs require plymouth (more fun with 467356)

* Mon Oct 20 2008 Ray Strode <rstrode@redhat.com> 0.6.0-0.2008.10.17.3
- Add initscripts requires (bug 461322)

* Mon Oct 20 2008 Ray Strode <rstrode@redhat.com> 0.6.0-0.2008.10.17.2
- Put tty1 back in "cooked" mode when going into runlevel 3
  (bug 467207)

* Fri Oct 17 2008 Ray Strode <rstrode@redhat.com> 0.6.0-0.2008.10.17.1
- Clear screen in details plugin when it's done
- Make plymouth-update-initrd a small wrapper around mkinitrd instead
  of the broken monstrosity it was before.

* Fri Oct 17 2008 Ray Strode <rstrode@redhat.com> 0.6.0-0.2008.10.15.3
- Move plymouth-set-default-plugin, plymouth-update-initrd, and
  plymouth-populate-initrd to plymouth-scripts subpackage
  (the last fix didn't actually help with bug 467356)

* Fri Oct 17 2008 Ray Strode <rstrode@redhat.com> 0.6.0-0.2008.10.15.2
- Move plymouth-set-default-plugin to -libs (might help with bug 467356)
- Fix up requires, provides and postun scripts

* Wed Oct 15 2008 Ray Strode <rstrode@redhat.com> 0.6.0-0.2008.10.15.1
- Don't free windows on --hide-splash (fix from Jeremy)

* Tue Oct 14 2008 Ray Strode <rstrode@redhat.com> 0.6.0-0.2008.10.14.1
- Solar fixes from Charlie Brej
- Better cpu usage from Charlie

* Fri Oct 10 2008 Ray Strode <rstrode@redhat.com> 0.6.0-0.2008.10.08.2
- Add Requires(post): nash (bug 466500)

* Wed Oct 08 2008 Ray Strode <rstrode@redhat.com> 0.6.0-0.2008.10.08.1
- Rework how "console=" args done again, to hopefully fix
  bug 460565

* Mon Oct 06 2008 Ray Strode <rstrode@redhat.com> 0.6.0-0.2008.10.06.1
- Add "Solar" plugin from Charles Brej
- Move things around so computers with separate /usr boot
  (hopefully this won't break things, but it probably will)
- Make GDM show up on vt1 for all plugins

* Tue Sep 30 2008 Jeremy Katz <katzj@redhat.com> 0.6.0-0.2008.09.25.2
- Remove mkinitrd requires to break the dep loop and ensure things
  get installed in the right order

* Thu Sep 25 2008 Ray Strode <rstrode@redhat.com> 0.6.0-0.2008.09.25.1
- Add new snapshot to fold in Will Woods progress bar, and
  move ajax's splash upstream, putting the old text splash
  in a "pulser" subpackage

* Tue Sep 23 2008 Ray Strode <rstrode@redhat.com> 0.6.0-0.2008.09.23.1
- Last snapshot was broken

* Mon Sep 22 2008 Ray Strode <rstrode@redhat.com> 0.6.0-0.2008.09.22.1
- Update to latest snapshot to get better transition support

* Fri Sep 19 2008 Ray Strode <rstrode@redhat.com> 0.6.0-0.2008.09.15.2
- Turn on gdm trigger for transition

* Mon Sep 15 2008 Ray Strode <rstrode@redhat.com> 0.6.0-0.2008.09.15.1
- add quit command with --retain-splash option to client

* Wed Sep 10 2008 Ray Strode <rstrode@redhat.com> 0.6.0-0.2008.09.10.1
- Fix text rendering for certain machines

* Mon Sep  8 2008 Ray Strode <rstrode@redhat.com> 0.6.0-0.2008.09.05.4
- More serial console fixes (bug 460565 again)

* Fri Sep  5 2008 Bill Nottingham <notting@redhat.com> 0.6.0-0.2008.09.05.3
- make the text plugin use the system release info rather than a hardcoded 'Fedora 10'

* Fri Sep  5 2008 Ray Strode <rstrode@redhat.com> 0.6.0-0.2008.09.05.2
- Try to support multiple serial consoles better
  (bug 460565)

* Fri Sep  5 2008 Ray Strode <rstrode@redhat.com> 0.6.0-0.2008.09.05.1
- Fix some confusion with password handling in details plugin

* Wed Aug 27 2008 Ray Strode <rstrode@redhat.com> 0.6.0-0.2008.08.27.1
- Fix another crasher for users with encrypted disks (this time in
  the text plugin, not the client)

* Wed Aug 27 2008 Ray Strode <rstrode@redhat.com> 0.6.0-0.2008.08.27
- Update to latest snapshot
- Add the ability to show text prompts in graphical plugin
- Fix crasher for users with encrypted disks

* Fri Aug 22 2008 Ray Strode <rstrode@redhat.com> 0.6.0-0.2008.08.22
- Update to latest snapshot

* Wed Aug 13 2008 Ray Strode <rstrode@redhat.com> 0.5.0-20.2008.08.13
- Update previous patch to remove some assertions

* Wed Aug 13 2008 Ray Strode <rstrode@redhat.com> 0.5.0-19.2008.08.13
- add a patch that may help serial console users

* Wed Aug 13 2008 Ray Strode <rstrode@redhat.com> 0.5.0-18.2008.08.13
- add spool directory to file list

* Wed Aug 13 2008 Ray Strode <rstrode@redhat.com> 0.5.0-17.2008.08.13
- Make plymouth-gdm-hooks require plymouth-utils

* Wed Aug 13 2008 Ray Strode <rstrode@redhat.com> 0.5.0-16.2008.08.13
- Add a boot failure viewer to login screen (written by Matthias)

* Tue Aug 12 2008 Adam Jackson <ajax@redhat.com> 0.5.0-15.2008.08.08
- plymouth-0.5.0-textbar-hotness.patch: Change the text plugin to a slightly
  more traditional progress bar, to maintain the illusion of progress better
  than the eternally oscillating cylon. Note: still incomplete.

* Fri Aug  8 2008 Ray Strode <rstrode@redhat.com> - 0.5.0-14.2008.08.08
- Don't require a modifiable text color map (may fix serial consoles)

* Thu Aug  7 2008 Ray Strode <rstrode@redhat.com> - 0.5.0-13.2008.08.07
- Update to new snapshot which when combined with a new mkinitrd should
  make unlocking encrypted root partitions work again

* Wed Aug  6 2008 Ray Strode <rstrode@redhat.com> - 0.5.0-12.2008.08.06
- Update to new snapshot which fixes some assertion failures in the
  client code

* Wed Aug  6 2008 Ray Strode <rstrode@redhat.com> - 0.5.0-11.2008.08.01
- Add Requires(post): plymouth to plugins so they get plymouth-set-default-plugin (bug 458071)

* Tue Aug  5 2008 Ray Strode <rstrode@redhat.com> - 0.5.0-10.2008.08.01
- Add plymouth dirs to file list (bug 457871)

* Fri Aug  1 2008 Ray Strode <rstrode@redhat.com> - 0.5.0-9.2008.08.01
- new plymout-populate-initrd features don't work with the set -e at the
  top of it.

* Thu Jul 31 2008 Ray Strode <rstrode@redhat.com> - 0.5.0-8.2008.08.01
- Update to another snapshot to actually get new
  plymouth-populate-initrd features

* Thu Jul 31 2008 Ray Strode <rstrode@redhat.com> - 0.5.0-8.2008.07.31
- Update to snapshot to get new plymouth-populate-initrd features
- Make removing rhgb use details plugin instead of exiting

* Thu Jul 31 2008 Peter Jones <pjones@redhat.com> - 0.5.0-7
- Make it a mkinitrd requires instead of a nash requires (that will
  still pull in nash, but we need mkinitrd for newer plymouth-populate-initrd)

* Wed Jul 30 2008 Ray Strode <rstrode@redhat.com> - 0.5.0-6
- Add nash requires

* Wed Jul  9 2008 Ray Strode <rstrode@redhat.com> - 0.5.0-5
- Use a new heuristic for finding libdir, since the old
  one falls over on ia64

* Wed Jul  9 2008 Ray Strode <rstrode@redhat.com> - 0.5.0-4
- add ctrl-r to rotate text color palette back to stock values

* Tue Jul  8 2008 Ray Strode <rstrode@redhat.com> - 0.5.0-3
- Fix populate script on ppc (bug 454353)

* Tue Jul  1 2008 Ray Strode <rstrode@redhat.com> - 0.5.0-2
- Pull in spinfinity by default.  This whole "figure out
  which plugin to use" set of scripts and scriptlets
  needs work.  We need to separate distro default from
  user choice.

* Tue Jul  1 2008 Ray Strode <rstrode@redhat.com> - 0.5.0-1
- Add new client "ask-for-password" command which feeds
  the user input to a program instead of standard output,
  and loops when the program returns non-zero exit status.

* Thu Jun 26 2008 Ray Strode <rstrode@redhat.com> - 0.4.5-1
- Update to version 0.4.5
- Make text plugin blue and less 80s

* Wed Jun 25 2008 Ray Strode <rstrode@redhat.com> - 0.4.0-4
- Make "Password: " show up correctly in text plugin

* Wed Jun 25 2008 Ray Strode <rstrode@redhat.com> - 0.4.0-3
- Require elfutils (bug 452797)

* Sun Jun 22 2008 Ray Strode <rstrode@redhat.com> - 0.4.0-2
- Make plymouth-set-default-plugin --reset choose the latest
  installed plugin, not the earliest

* Sun Jun 22 2008 Ray Strode <rstrode@redhat.com> - 0.4.0-1
- Update to version 0.4.0
- Only run if rhgb is on kernel command line
- Make text plugin more animated

* Mon Jun 16 2008 Ray Strode <rstrode@redhat.com> - 0.3.2-2
- dont go back to text mode on exit

* Mon Jun 16 2008 Ray Strode <rstrode@redhat.com> - 0.3.2-1
- Update to version 0.3.2
- show gradient in spinfinity plugin
- Drop fade out in spinfinity plugin
- fix throbber placement
- rename graphical.so to default.so

* Thu Jun 12 2008 Ray Strode <rstrode@redhat.com> - 0.3.1-3
- scriplet should be preun, not postun

* Thu Jun 12 2008 Ray Strode <rstrode@redhat.com> - 0.3.1-2
- Fix postun scriptlet

* Thu Jun 12 2008 Ray Strode <rstrode@redhat.com> - 0.3.1-1
- Update to version 0.3.1
- Don't ship generated initrd scripts in tarball

* Thu Jun 12 2008 Ray Strode <rstrode@redhat.com> - 0.3.0-1
- Update to version 0.3.0
- Better plugin handling
- Better integration with mkinitrd (pending mkinitrd changes)
- random bug fixes

* Mon Jun  9 2008 Ray Strode <rstrode@redhat.com> - 0.2.0-1
- Update to version 0.2.0
- Integrate more tightly with nash (pending nash changes)
- ship libs for out of tree splash plugins
- gradient support
- random bug fixes

* Fri May 30 2008 Ray Strode <rstrode@redhat.com> - 0.1.0-1
- Initial import, version 0.1.0
