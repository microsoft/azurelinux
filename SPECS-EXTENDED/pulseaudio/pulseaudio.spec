%bcond_with missing_dependencies

%undefine _strict_symbol_defs_build
%global with_webrtc 1
%global enable_lirc 0
%global enable_jack 0
%global _hardened_build 1
# support systemd activation
%global systemd 1
# where/how to apply multilib hacks
%global multilib_archs x86_64
%global bash_completionsdir %(pkg-config --variable=completionsdir bash-completion 2>/dev/null || echo '%{_sysconfdir}/bash_completion.d')
Summary:        Improved Linux Sound Server
Name:           pulseaudio
Version:        16.1
Release:        2%{?dist}
License:        LGPLv2+
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://www.freedesktop.org/wiki/Software/PulseAudio
Source0:        https://freedesktop.org/software/%{name}/releases/%{name}-%{version}.tar.gz
# revert upstream commit to rely solely on autospawn for autostart, instead
# include a fallback to manual launch when autospawn fails, like when
# user disables autospawn, or logging in as root
# valid even when using systemd socket activation too
Patch0:         pulseaudio-autostart.patch
%if 0%{?systemd}
# disable autospawn
Patch1:         pulseaudio-11.1-autospawn_disable.patch
%endif
BuildRequires:  meson >= 0.50.0
BuildRequires:  gcc
BuildRequires:  g++
BuildRequires:  pkgconfig(bash-completion)
BuildRequires:  m4
BuildRequires:  libtool-ltdl-devel
BuildRequires:  intltool
BuildRequires:  pkgconfig
BuildRequires:  doxygen
BuildRequires:  xmltoman
BuildRequires:  libsndfile-devel
BuildRequires:  alsa-lib-devel
BuildRequires:  glib2-devel
BuildRequires:  gtk2-devel
BuildRequires:  avahi-devel
BuildRequires:  libatomic_ops-devel
BuildRequires:  pkgconfig(bluez) >= 5.0
BuildRequires:  sbc-devel
BuildRequires:  libXt-devel
BuildRequires:  xorg-x11-proto-devel
BuildRequires:  libXtst-devel
BuildRequires:  libXi-devel
BuildRequires:  libSM-devel
BuildRequires:  libX11-devel
BuildRequires:  libICE-devel
BuildRequires:  xcb-util-devel
BuildRequires:  openssl-devel
BuildRequires:  orc-devel
BuildRequires:  libtdb-devel
BuildRequires:  pkgconfig(speexdsp) >= 1.2
BuildRequires:  libasyncns-devel
BuildRequires:  dbus-devel
BuildRequires:  libcap-devel
BuildRequires:  pkgconfig(fftw3f)
BuildRequires:  pkgconfig(gstreamer-1.0) >= 1.16.0
BuildRequires:  pkgconfig(gstreamer-app-1.0) >= 1.16.0
BuildRequires:  pkgconfig(gstreamer-rtp-1.0) >= 1.16.0
%if 0%{?systemd}
BuildRequires:  systemd
BuildRequires:  systemd-devel >= 184
%{?systemd_requires}
%endif
%if 0%{?with_webrtc}
BuildRequires:  pkgconfig(webrtc-audio-processing) >= 0.2
%endif
%if 0%{?with_check}
BuildRequires:  pkgconfig(check)
%endif
# retired along with -libs-zeroconf, add Obsoletes here for lack of anything better
Obsoletes:      padevchooser < 1.0
Requires(pre):  shadow-utils
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
Requires:       rtkit

# Virtual Provides to support swapping between PipeWire-PA and PA
Provides:       pulseaudio-daemon
Conflicts:      pulseaudio-daemon

# Packages removed in 15.0
Obsoletes:      pulseaudio-esound-compat < 15.0
Obsoletes:      pulseaudio-module-gconf < 15.0

%description
PulseAudio is a sound server for Linux and other Unix like operating
systems. It is intended to be an improved drop-in replacement for the
Enlightened Sound Daemon (ESOUND).

%package qpaeq
Summary:        Pulseaudio equalizer interface
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       python3-dbus
%if 0%{with missing_dependencies}
Requires:       python3-qt5-base
%endif

%description qpaeq
qpaeq is a equalizer interface for pulseaudio's equalizer sinks.

%if 0%{?enable_lirc}
%package module-lirc
Summary:        LIRC support for the PulseAudio sound server
BuildRequires:  lirc-devel
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description module-lirc
LIRC volume control module for the PulseAudio sound server.
%endif

%package module-x11
Summary:        X11 support for the PulseAudio sound server
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       %{name}-utils

%description module-x11
X11 bell and security modules for the PulseAudio sound server.

%package module-zeroconf
Summary:        Zeroconf support for the PulseAudio sound server
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       %{name}-utils

%description module-zeroconf
Zeroconf publishing module for the PulseAudio sound server.

%package module-bluetooth
Summary:        Bluetooth support for the PulseAudio sound server
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       bluez >= 5.0

%description module-bluetooth
Contains Bluetooth audio (A2DP/HSP/HFP) support for the PulseAudio sound server.

%if 0%{?enable_jack}
%package module-jack
Summary:        JACK support for the PulseAudio sound server
BuildRequires:  jack-audio-connection-kit-devel
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description module-jack
JACK sink and source modules for the PulseAudio sound server.
%endif

%package module-gsettings
Summary:        Gsettings support for the PulseAudio sound server
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description module-gsettings
GSettings configuration backend for the PulseAudio sound server.

%package libs
Summary:        Libraries for PulseAudio clients
Obsoletes:      pulseaudio-libs-zeroconf < 1.1

%description libs
This package contains the runtime libraries for any application that wishes
to interface with a PulseAudio sound server.

%package libs-glib2
Summary:        GLIB 2.x bindings for PulseAudio clients
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}

%description libs-glib2
This package contains bindings to integrate the PulseAudio client library with
a GLIB 2.x based application.

%package libs-devel
Summary:        Headers and libraries for PulseAudio client development
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
Requires:       %{name}-libs-glib2%{?_isa} = %{version}-%{release}

%description libs-devel
Headers and libraries for developing applications that can communicate with
a PulseAudio sound server.

%package utils
Summary:        PulseAudio sound server utilities
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
# when made non-multilib'd, https://bugzilla.redhat.com/891425
Obsoletes:      pulseaudio-utils < 3.0-3

%description utils
This package contains command line utilities for the PulseAudio sound server.

%prep
%autosetup -p1 -n %{name}-%{version}

sed -i.no_consolekit -e \
  's/^load-module module-console-kit/#load-module module-console-kit/' \
  src/daemon/default.pa.in

%build
%meson \
  -D system_user=pulse \
  -D system_group=pulse \
  -D access_group=pulse-access \
  -D oss-output=disabled \
  -D jack=disabled \
  -D lirc=disabled \
  -D tcpwrap=disabled \
  -D bluez5=enabled \
  -D gstreamer=enabled \
  -D bluez5-gstreamer=enabled \
  -D gsettings=enabled \
  -D elogind=disabled \
  -D valgrind=disabled \
  -D gtk=disabled \
  -D soxr=disabled \
  -D webrtc-aec=%{?with_webrtc:enabled}%{!?with_webrtc:disabled} \
  -D systemd=%{?systemd:enabled}%{!?systemd:disabled} \
  -D tests=true

# we really should preopen here --preopen-mods=module-udev-detect.la, --force-preopen
%meson_build

%meson_build doxygen

%install
%meson_install

# upstream should use udev.pc
mkdir -p %{buildroot}%{_libdir}/udev/rules.d
mv -fv %{buildroot}/lib/udev/rules.d/90-pulseaudio.rules %{buildroot}%{_libdir}/udev/rules.d

## unpackaged files
# extraneous libtool crud
rm -fv %{buildroot}%{_libdir}/lib*.la
rm -fv %{buildroot}%{_libdir}/pulseaudio/lib*.la
rm -fv %{buildroot}%{_libdir}/pulseaudio/modules/*.la

# PA_MODULE_DEPRECATED("Please use module-udev-detect instead of module-detect!");
rm -fv %{buildroot}%{_libdir}/pulseaudio/modules/module-detect.so

%find_lang %{name}

%check
%meson_test

%pre
getent group pulse-access >/dev/null || groupadd -r pulse-access
getent group pulse-rt >/dev/null || groupadd -r pulse-rt
getent group pulse >/dev/null || groupadd -f -g 171 -r pulse
if ! getent passwd pulse >/dev/null ; then
    if ! getent passwd 171 >/dev/null ; then
      useradd -r -u 171 -g pulse -d %{_localstatedir}/run/pulse -s /sbin/nologin -c "PulseAudio System Daemon" pulse
    else
      useradd -r -g pulse -d %{_localstatedir}/run/pulse -s /sbin/nologin -c "PulseAudio System Daemon" pulse
    fi
fi
exit 0

%posttrans
# handle renamed module-cork-music-on-phone => module-role-cork
(grep '^load-module module-cork-music-on-phone$' %{_sysconfdir}/pulse/default.pa > /dev/null && \
 sed -i.rpmsave -e 's|^load-module module-cork-music-on-phone$|load-module module-role-cork|' \
 %{_sysconfdir}/pulse/default.pa
) ||:

%post
%{?ldconfig}
%if 0%{?systemd}
%systemd_user_post pulseaudio.socket
%endif

%if 0%{?systemd}
%preun
%systemd_user_preun pulseaudio.socket
%endif

%ldconfig_postun

%if 0%{?systemd}
%triggerun -- pulseaudio < 12.2-4
# This is for upgrades from previous versions which had a static symlink.
# The %%post scriptlet above only does anything on initial package installation.
# Remove before F33.
systemctl --no-reload preset --global pulseaudio.socket >/dev/null 2>&1 || :
%endif

%files
%doc README
%license LICENSE GPL LGPL
%config(noreplace) %{_sysconfdir}/pulse/daemon.conf
%config(noreplace) %{_sysconfdir}/pulse/default.pa
%config(noreplace) %{_sysconfdir}/pulse/system.pa
%{_sysconfdir}/dbus-1/system.d/pulseaudio-system.conf
%{bash_completionsdir}/pulseaudio
%if 0%{?systemd}
%{_userunitdir}/pulseaudio.service
%{_userunitdir}/pulseaudio.socket
%endif
%{_bindir}/pa-info
%{_bindir}/pulseaudio
%{_libdir}/pulseaudio/libpulsecore-%{version}.so
%dir %{_libdir}/pulseaudio/
%dir %{_libdir}/pulseaudio/modules/
%{_libdir}/pulseaudio/modules/libalsa-util.so
%{_libdir}/pulseaudio/modules/libcli.so
%{_libdir}/pulseaudio/modules/libprotocol-cli.so
%{_libdir}/pulseaudio/modules/libprotocol-http.so
%{_libdir}/pulseaudio/modules/libprotocol-native.so
%{_libdir}/pulseaudio/modules/libprotocol-simple.so
%{_libdir}/pulseaudio/modules/librtp.so
%if 0%{?with_webrtc}
%{_libdir}/pulseaudio/modules/libwebrtc-util.so
%endif
%{_libdir}/pulseaudio/modules/module-allow-passthrough.so
%{_libdir}/pulseaudio/modules/module-alsa-sink.so
%{_libdir}/pulseaudio/modules/module-alsa-source.so
%{_libdir}/pulseaudio/modules/module-alsa-card.so
%{_libdir}/pulseaudio/modules/module-cli-protocol-tcp.so
%{_libdir}/pulseaudio/modules/module-cli-protocol-unix.so
%{_libdir}/pulseaudio/modules/module-cli.so
%{_libdir}/pulseaudio/modules/module-combine.so
%{_libdir}/pulseaudio/modules/module-combine-sink.so
%{_libdir}/pulseaudio/modules/module-dbus-protocol.so
%{_libdir}/pulseaudio/modules/module-filter-apply.so
%{_libdir}/pulseaudio/modules/module-filter-heuristics.so
%{_libdir}/pulseaudio/modules/module-device-manager.so
%{_libdir}/pulseaudio/modules/module-loopback.so
%{_libdir}/pulseaudio/modules/module-udev-detect.so
%{_libdir}/pulseaudio/modules/module-hal-detect.so
%{_libdir}/pulseaudio/modules/module-http-protocol-tcp.so
%{_libdir}/pulseaudio/modules/module-http-protocol-unix.so
%{_libdir}/pulseaudio/modules/module-match.so
%{_libdir}/pulseaudio/modules/module-mmkbd-evdev.so
%{_libdir}/pulseaudio/modules/module-native-protocol-fd.so
%{_libdir}/pulseaudio/modules/module-native-protocol-tcp.so
%{_libdir}/pulseaudio/modules/module-native-protocol-unix.so
%{_libdir}/pulseaudio/modules/module-null-sink.so
%{_libdir}/pulseaudio/modules/module-null-source.so
%{_libdir}/pulseaudio/modules/module-pipe-sink.so
%{_libdir}/pulseaudio/modules/module-pipe-source.so
%{_libdir}/pulseaudio/modules/module-remap-source.so
%{_libdir}/pulseaudio/modules/module-rescue-streams.so
%{_libdir}/pulseaudio/modules/module-role-ducking.so
%{_libdir}/pulseaudio/modules/module-rtp-recv.so
%{_libdir}/pulseaudio/modules/module-rtp-send.so
%{_libdir}/pulseaudio/modules/module-simple-protocol-tcp.so
%{_libdir}/pulseaudio/modules/module-simple-protocol-unix.so
%{_libdir}/pulseaudio/modules/module-sine.so
%{_libdir}/pulseaudio/modules/module-switch-on-port-available.so
%{_libdir}/pulseaudio/modules/module-systemd-login.so
%{_libdir}/pulseaudio/modules/module-tunnel-sink-new.so
%{_libdir}/pulseaudio/modules/module-tunnel-sink.so
%{_libdir}/pulseaudio/modules/module-tunnel-source-new.so
%{_libdir}/pulseaudio/modules/module-tunnel-source.so
%{_libdir}/pulseaudio/modules/module-volume-restore.so
%{_libdir}/pulseaudio/modules/module-suspend-on-idle.so
%{_libdir}/pulseaudio/modules/module-default-device-restore.so
%{_libdir}/pulseaudio/modules/module-device-restore.so
%{_libdir}/pulseaudio/modules/module-stream-restore.so
%{_libdir}/pulseaudio/modules/module-card-restore.so
%{_libdir}/pulseaudio/modules/module-ladspa-sink.so
%{_libdir}/pulseaudio/modules/module-remap-sink.so
%{_libdir}/pulseaudio/modules/module-always-sink.so
%{_libdir}/pulseaudio/modules/module-always-source.so
%{_libdir}/pulseaudio/modules/module-console-kit.so
%{_libdir}/pulseaudio/modules/module-position-event-sounds.so
%{_libdir}/pulseaudio/modules/module-augment-properties.so
%{_libdir}/pulseaudio/modules/module-role-cork.so
%{_libdir}/pulseaudio/modules/module-sine-source.so
%{_libdir}/pulseaudio/modules/module-intended-roles.so
%{_libdir}/pulseaudio/modules/module-rygel-media-server.so
%{_libdir}/pulseaudio/modules/module-echo-cancel.so
%{_libdir}/pulseaudio/modules/module-switch-on-connect.so
%{_libdir}/pulseaudio/modules/module-virtual-sink.so
%{_libdir}/pulseaudio/modules/module-virtual-source.so
%{_libdir}/pulseaudio/modules/module-virtual-surround-sink.so
%dir %{_datadir}/pulseaudio/
%dir %{_datadir}/pulseaudio/alsa-mixer/
%{_datadir}/pulseaudio/alsa-mixer/paths/
%{_datadir}/pulseaudio/alsa-mixer/profile-sets/
%{_mandir}/man1/pulseaudio.1*
%{_mandir}/man5/default.pa.5*
%{_mandir}/man5/pulse-cli-syntax.5*
%{_mandir}/man5/pulse-client.conf.5*
%{_mandir}/man5/pulse-daemon.conf.5*
%{_libdir}/udev/rules.d/90-pulseaudio.rules
%dir %{_libexecdir}/pulse
%dir %{_datadir}/zsh/
%dir %{_datadir}/zsh/site-functions/
%{_datadir}/zsh/site-functions/_pulseaudio

%files qpaeq
%{_bindir}/qpaeq
%{_libdir}/pulseaudio/modules/module-equalizer-sink.so

%if 0%{?enable_lirc}
%files module-lirc
%{_libdir}/pulseaudio/modules/module-lirc.so
%endif

%files module-x11
%config(noreplace) %{_sysconfdir}/xdg/autostart/pulseaudio.desktop
%config(noreplace) %{_sysconfdir}/xdg/Xwayland-session.d/00-pulseaudio-x11
%{_userunitdir}/pulseaudio-x11.service
#{_bindir}/start-pulseaudio-kde
%{_bindir}/start-pulseaudio-x11
%{_libdir}/pulseaudio/modules/module-x11-bell.so
%{_libdir}/pulseaudio/modules/module-x11-publish.so
%{_libdir}/pulseaudio/modules/module-x11-xsmp.so
%{_libdir}/pulseaudio/modules/module-x11-cork-request.so
%{_mandir}/man1/start-pulseaudio-x11.1.gz

%files module-zeroconf
%{_libdir}/pulseaudio/modules/libavahi-wrap.so
%{_libdir}/pulseaudio/modules/module-zeroconf-publish.so
%{_libdir}/pulseaudio/modules/module-zeroconf-discover.so
%{_libdir}/pulseaudio/modules/libraop.so
%{_libdir}/pulseaudio/modules/module-raop-discover.so
%{_libdir}/pulseaudio/modules/module-raop-sink.so

%if 0%{?enable_jack}
%files module-jack
%{_libdir}/pulseaudio/modules/module-jackdbus-detect.so
%{_libdir}/pulseaudio/modules/module-jack-sink.so
%{_libdir}/pulseaudio/modules/module-jack-source.so
%endif

%files module-bluetooth
%{_libdir}/pulseaudio/modules/libbluez*-util.so
%{_libdir}/pulseaudio/modules/module-bluez*-device.so
%{_libdir}/pulseaudio/modules/module-bluez*-discover.so
%{_libdir}/pulseaudio/modules/module-bluetooth-discover.so
%{_libdir}/pulseaudio/modules/module-bluetooth-policy.so

%files module-gsettings
%{_libdir}/pulseaudio/modules/module-gsettings.so
%{_libexecdir}/pulse/gsettings-helper
%{_datadir}/GConf/gsettings/pulseaudio.convert
%{_datadir}/glib-2.0/schemas/org.freedesktop.pulseaudio.gschema.xml

%ldconfig_scriptlets libs

%files libs -f %{name}.lang
%doc README
%license LICENSE GPL LGPL
%dir %{_sysconfdir}/pulse/
%config(noreplace) %{_sysconfdir}/pulse/client.conf
%{_libdir}/libpulse.so.0*
%{_libdir}/libpulse-simple.so.0*
%dir %{_libdir}/pulseaudio/
%{_libdir}/pulseaudio/libpulsecommon-%{version}.so

%ldconfig_scriptlets libs-glib2

%files libs-glib2
%{_libdir}/libpulse-mainloop-glib.so.0*

%files libs-devel
%doc %{_vpath_builddir}/doxygen/html
%{_includedir}/pulse/
%{_libdir}/libpulse.so
%{_libdir}/libpulse-mainloop-glib.so
%{_libdir}/libpulse-simple.so
%{_libdir}/pkgconfig/libpulse*.pc
%dir %{_datadir}/vala
%dir %{_datadir}/vala/vapi
%{_datadir}/vala/vapi/libpulse.vapi
%{_datadir}/vala/vapi/libpulse.deps
%{_datadir}/vala/vapi/libpulse-mainloop-glib.vapi
%{_datadir}/vala/vapi/libpulse-mainloop-glib.deps
%{_datadir}/vala/vapi/libpulse-simple.deps
%{_datadir}/vala/vapi/libpulse-simple.vapi

%dir %{_libdir}/cmake
%{_libdir}/cmake/PulseAudio/

%files utils
%{_bindir}/pacat
%{_bindir}/pacmd
%{_bindir}/pactl
%{_bindir}/paplay
%{_bindir}/parec
%{_bindir}/pamon
%{_bindir}/parecord
%{_bindir}/pax11publish
%{_bindir}/pasuspender
%{_mandir}/man1/pacat.1*
%{_mandir}/man1/pacmd.1*
%{_mandir}/man1/pactl.1*
%{_mandir}/man1/pamon.1*
%{_mandir}/man1/paplay.1*
%{_mandir}/man1/parec.1*
%{_mandir}/man1/parecord.1*
%{_mandir}/man1/pasuspender.1*
%{_mandir}/man1/pax11publish.1*
%{bash_completionsdir}/pacat
%{bash_completionsdir}/pacmd
%{bash_completionsdir}/pactl
%{bash_completionsdir}/padsp
%{bash_completionsdir}/paplay
%{bash_completionsdir}/parec
%{bash_completionsdir}/parecord
%{bash_completionsdir}/pasuspender

%changelog
* Wed Nov 23 2022 Sumedh Sharma <sumsharma@microsoft.com> - 16.1-2
- Initial CBL-Mariner import from Fedora 36 (license: MIT)
- Build with lirc and jack disabled
- Enable check section
- License verified

* Thu Jul 21 2022 Rex Dieter <rdieter@fedoraproject.org> - 16.1-1
- 16.1

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 15.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Sep 14 2021 Sahana Prasad <sahana@redhat.com> - 15.0-4
- Rebuilt with OpenSSL 3.0.0

* Fri Sep 10 2021 Rex Dieter <rdieter@fedoraproject.org> - 15.0-3
- fix autostart.patch (#2001664)

* Wed Sep 08 2021 Wim Taymans <wtaymans@redhat.com> - 15.0-2
- Obsoletes: pulseaudio-esound-compat and pulseaudio-module-gconf
- Resolves: #2001334

* Wed Jul 28 2021 Wim Taymans <wtaymans@redhat.com> - 15.0-1
- Update to 15.0
- convert to meson build
- esound, gconf, oss are no longer supported

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 14.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sat Feb 06 2021 Rex Dieter <rdieter@fedoraproject.org> - 14.2-3
- -utils: move appropriate bash completions here (#1925706)

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 14.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jan 18 2021 Rex Dieter <rdieter@fedoraproject.org> - 14.2-1
- 14.2

* Wed Jan 13 2021 Rex Dieter <rdieter@fedoraproject.org> - 14.1-1
- 14.1

* Tue Jan 12 2021 Wim Taymans <wtaymans@redhat.com> - 14.0-3
- Move enable_ switches next to the other switches on top
- Only enable gconf on fedora

* Tue Nov 24 2020 Neal Gompa <ngompa13@gmail.com> - 14.0-2
- Add 'pulseaudio-daemon' Provides + Conflicts to support swapping with PipeWire

* Mon Nov 23 2020 Rex Dieter <rdieter@fedoraproject.org> - 14.0-1
- 14.0

* Sun Nov 01 2020 Rex Dieter <rdieter@fedoraproject.org> - 13.99.3-1
- 13.99.3

* Tue Sep 22 2020 Rex Dieter <rdieter@fedoraproject.org> - 13.99.2-1
-  13.99.2

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 13.99.1-6
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 13.99.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jun 15 2020 Wim Taymans <wtaymans@redhat.com> - 13.99.1-4
- Add patch to fix crash with profile name (#1817092)

* Tue Mar 31 2020 Wim Taymans <wtaymans@redhat.com> - 13.99.1-3
- Add more UCM patches (#1818883)

* Fri Mar 20 2020 Wim Taymans <wtaymans@redhat.com> - 13.99.1-2
- Add some more UCM patches
- Fix missing UCM mixers crash (#1815437)

* Fri Feb 14 2020 Rex Dieter <rdieter@fedoraproject.org> - 13.99.1-1
- 13.99.1

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 13.0-3.20200105gitf5d36
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jan 08 2020 Jaroslav Kysela <perex@perex.cz> - 13.0-2
- Update to upstream gitsnapshot
- ALSA UCM fixes
- active_port sink selection fixes

* Fri Sep 13 2019 Rex Dieter <rdieter@fedoraproject.org> - 13.0-1
- 13.0

* Mon Sep 02 2019 Rex Dieter <rdieter@fedoraproject.org> - 12.99.3-1
- pulseaudio-12.99.3

* Wed Aug 07 2019 Rex Dieter <rdieter@fedoraproject.org> - 12.99.2-2
- -qpaeq: use python3 (#1738047)

* Tue Aug 06 2019 Rex Dieter <rdieter@fedoraproject.org> - 12.99.2-1
- pulseaudio-12.99.2

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 12.99.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Jul 09 2019 Rex Dieter <rdieter@fedoraproject.org> - 12.99.1-1
- pulseaudio-12.99.1

* Wed Jul 03 2019 Rex Dieter <rdieter@fedoraproject.org> - 12.2-7
- alsa-sink: clear pollfd revents before poll

* Mon Jun 17 2019 Rex Dieter <rdieter@fedoraproject.org> - 12.2-6
- pull in upstream patch for alsa include paths

* Thu May 09 2019 Rex Dieter <rdieter@fedoraproject.org> - 12.2-5
- Use systemd presets to enable user units
- conditionals: simplify and support rhel8

* Wed Apr 10 2019 Rex Dieter <rdieter@fedoraproject.org> - 12.2-4
- test using only socket activation (f31+ only for now)

* Tue Feb 12 2019 Rex Dieter <rdieter@fedoraproject.org> - 12.2-3
- qpaeq_python2.patch

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 12.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jul 16 2018 Rex Dieter <rdieter@fedoraproject.org> - 12.2-1
- pulseaudio-12.2

* Sat Jul 14 2018 Rex Dieter <rdieter@fedoraproject.org> - 12.1-1
- pulseaudio-12.1

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 12.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jul 05 2018 Rex Dieter <rdieter@fedoraproject.org> - 12.0-3
- ladspa-sink-fix-search-path.patch (#1594568, fdo#107078)

* Sun Jul 01 2018 Rex Dieter <rdieter@fedoraproject.org> - 12.0-2
- switch-on-port-available-ignore-bluetooth-cards.patch (#1594596, fdo#107044)
- use upstreamed exit-idle-time.patch

* Thu Jun 21 2018 Rex Dieter <rdieter@fedoraproject.org> - 12.0-1
- pulseaudio-12.0 is available (#1593489)
- -libs: use %%license

* Sun May 13 2018 Rex Dieter <rdieter@fedoraproject.org> - 11.99.1-1
- 11.99.1 (#1577603)
- use %%ldconfig_scriptlets
- new pulseaudio--module-gsettings subpkg

* Tue May 08 2018 Rex Dieter <rdieter@fedoraproject.org> - 11.1-21
- drop unused getaffinity,memfd patches
- include experimental bluetooth patches only on rawhide

* Mon Apr 23 2018 Hans de Goede <hdegoede@redhat.com> - 11.1-20
- Fix Intel LPE HDMI problems:
- Update to upstream gitsnapshot which contains a fix for the crash caused
  by patch93 (and contains patch93 fixing the Intel LPE HDMI pa crash)
- Fix-realtime-scheduling-on-byt-cht.patch, Fix-Intel-HDMI-LPE-problems.patch:
  drop both, both fixes are included in the git snapshot

* Fri Mar 23 2018 Iryna Shcherbina <ishcherb@redhat.com> - 11.1-19
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Wed Mar 21 2018 Rex Dieter <rdieter@fedoraproject.org> - 11.1-18
- manually package sockets.target.wants/pulseaudio.socket to help
  handle socket activation on upgrades

* Tue Mar 20 2018 Rex Dieter <rdieter@fedoraproject.org> - 11.1-17
- omit -gdm-hooks, moved to gdm (f28+)

* Tue Mar 13 2018 Rex Dieter <rdieter@fedoraproject.org> - 11.1-16
- skip patch93, seems to cause crashes w/headphone jacks (#1544507,#1551270,#1554035)

* Mon Mar 05 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 11.1-15
- Fixup ldconfig scriptlets

* Thu Mar 01 2018 Rex Dieter <rdieter@fedoraproject.org> - 11.1-14
- use %%make_build, %%make_install
- enable systemd socket/service activation on f28+ (and disable autospawn)

* Wed Feb 28 2018 Rex Dieter <rdieter@fedoraproject.org> - 11.1-13
- use %%license, %%ldconfig_scriptlets
- use better upstream patch for exit-idle-time

* Sun Feb 25 2018 Rex Dieter <rdieter@fedoraproject.org> - 11.1-12
- BR: gcc-c++

* Fri Feb 09 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 11.1-11
- Escape macros in %%changelog

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 11.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Feb 01 2018 Rex Dieter <rdieter@fedoraproject.org> - 11.1-9
- backport upstream fixes: memfd, qpape PyQt5 port

* Mon Jan 08 2018 Rex Dieter <rdieter@fedoraproject.org> - 11.1-8
- exit-idle-time = 4 (#1510301)
- f28+ ftbfs: memfd_create conflicts
- drop getaffinity.patch (no longer needed)
- enable webrtc support for all archs
- make tests non-fatal on i686,s390x

* Mon Dec 04 2017 Rex Dieter <rdieter@fedoraproject.org> - 11.1-7
- backport 'pa_sink_input_assert_ref()' crashfix (#1472285)
- --disable-tcpwrap on f28+ (#1518777)

* Wed Nov 08 2017 Hans de Goede <hdegoede@redhat.com> - 11.1-6
- Fix pa crashing on Bay- and Cherry-Trail devices

* Wed Nov 01 2017 Rex Dieter <rdieter@fedoraproject.org> - 11.1-5
- actually install new dell-dock-tb16-usb-audio.conf alsa profile (#1492344)

* Thu Oct 12 2017 Rex Dieter <rdieter@fedoraproject.org> - 11.1-4
- experimental fixes bluetooth profile switching (f28+ only, fdo#93898)

* Thu Oct 12 2017 Rex Dieter <rdieter@fedoraproject.org> - 11.1-3
- include experiemental Intel HDMI LPE fixes (fdo#100488)

* Mon Oct 09 2017 Rex Dieter <rdieter@fedoraproject.org> - 11.1-2
- backport some alsa-mixer related fixes (#1492344)

* Wed Sep 20 2017 Rex Dieter <rdieter@fedoraproject.org> - 11.1-1 
- pulseaudio-11.1

* Tue Sep 05 2017 Rex Dieter <rdieter@fedoraproject.org> - 11.0-1
- pulseaudio-11.0

* Mon Aug 28 2017 Pete Walter <pwalter@fedoraproject.org> - 10.99.1-6
- Enable pulseaudio-module-bluetooth on s390x

* Fri Aug 18 2017 Wim Taymans <wtaymans@redhat.com> - 10.99.1-5
- Remove /var/run/pulse and /var/lib/pulse, they are directories in tmpfs

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 10.99.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Sun Jul 30 2017 Florian Weimer <fweimer@redhat.com> - 10.99.1-3
- Rebuild with binutils fix for ppc64le (#1475636)

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 10.99.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jul 25 2017 Rex Dieter <rdieter@fedoraproject.org> - 10.99.1-1
- pulseaudio-10.99.1 (#1474559)

* Mon Feb 13 2017 Wim Taymans <wtaymans@redhat.com> - 10.0-4
- Add flatpak access control

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 10.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Jan 19 2017 Kalev Lember <klember@redhat.com> - 10.0-2
- Fix the build on RHEL

* Thu Jan 19 2017 Kalev Lember <klember@redhat.com> - 10.0-1
- Update to 10.0

* Fri Jan 06 2017 Rex Dieter <rdieter@fedoraproject.org> - 9.99.1-1
- pulseaudio-9.99.1 (#1409939)
- %%check: use %%_smp_mflags

* Fri Jun 24 2016 Rex Dieter <rdieter@fedoraproject.org> - 9.0-1
- pulseaudio-9.0

* Wed Jun 22 2016 Than Ngo <than@redhat.com> - 8.99.2-3
- enable %%check
- fix bz#1345826, only start threads on activ CPUs

* Mon Jun 13 2016 Rex Dieter <rdieter@fedoraproject.org> - 8.99.2-2
- %%check: make non-fatal, echo test-suite.log on failure (#1345826)

* Tue May 31 2016 Rex Dieter <rdieter@fedoraproject.org> - 8.99.2-1
- pulseaudio-8.99.2

* Thu May 12 2016 Rex Dieter <rdieter@fedoraproject.org> - 8.99.1-2
- re-enable webrtc support (arm,x86_64 only for now)

* Thu May 12 2016 Rex Dieter <rdieter@fedoraproject.org> - 8.99.1-1
- pulseaudio-8.99.1 (#1335527)
- disable webrtc support for now (waiting on #1335536)

* Fri May 06 2016 Rex Dieter <rdieter@fedoraproject.org> - 8.0-7
- use %%tests macro, enable systemd socket activation (#1265720)

* Sat Mar 05 2016 Rex Dieter <rdieter@fedoraproject.org> - 8.0-6
- respin disable_flat_volumes.patch harder

* Sat Mar 05 2016 Rex Dieter <rdieter@fedoraproject.org> - 8.0-5
- respin disable_flat_volumes.patch

* Fri Mar 04 2016 Rex Dieter <rdieter@fedoraproject.org> - 8.0-4
- RFE: Disable PulseAudio's flat volumes f24+ (#1265267)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 8.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jan 22 2016 Rex Dieter <rdieter@fedoraproject.org> - 8.0-2
- own /var/run/pulse (#1173811)

* Fri Jan 22 2016 Rex Dieter <rdieter@fedoraproject.org> - 8.0-1
- pulseaudio-8.0 (#1301040)

* Wed Jan 13 2016 Rex Dieter <rdieter@fedoraproject.org> - 7.99.2-1
- pulseaudio-7.99.2 (#1297774)

* Mon Dec 28 2015 Rex Dieter <rdieter@fedoraproject.org> - 7.99.1-1
- pulseaudio-7.99.1 (8.0 rc1) (#1294555)

* Sat Oct 31 2015 Rex Dieter <rdieter@fedoraproject.org> - 7.1-1
- pulseaudio-7.1 (#1276811)

* Sat Oct 31 2015 Rex Dieter <rdieter@fedoraproject.org> - 7.0-4
- apply srbchannel patch

* Tue Oct 27 2015 Rex Dieter <rdieter@fedoraproject.org> - 7.0-3
- backport srbchannel crasher fix

* Sun Sep 27 2015 Rex Dieter <rdieter@fedoraproject.org> - 7.0-2
- PulseAudio doesn't load locales (fdo#92142)

* Wed Sep 23 2015 Rex Dieter <rdieter@fedoraproject.org> - 7.0-1 
- pulseaudio-7.0

* Sat Sep 12 2015 Rex Dieter <rdieter@fedoraproject.org> - 6.99.2-1 
- 6.99.2 (#1262579)

* Sat Aug 29 2015 Rex Dieter <rdieter@fedoraproject.org> - 6.99.1-2
- enable libsoxr support

* Fri Aug 28 2015 Rex Dieter <rdieter@fedoraproject.org> - 6.99.1-1
- 6.99.1 (#1257770)

* Mon Jul 06 2015 Rex Dieter <rdieter@fedoraproject.org> - 6.0-8
- autostart.patch: fix stdout/stderr redirection

* Mon Jul 06 2015 Rex Dieter <rdieter@fedoraproject.org> - 6.0-7
- fix resampler-related build dependencies (libsamplerate/speex) (#1239208)

* Mon Jun 22 2015 Rex Dieter <rdieter@fedoraproject.org> - 6.0-6
- better autostart.patch, handle case were autospawn is disabled (or otherwise doesn't work, like for root user)

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jun 11 2015 Rex Dieter <rdieter@fedoraproject.org> - 6.0-4
- pulseaudio 6.0 breaks 5.1 network sound configuration (#1230957)

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 6.0-3
- Rebuilt for GCC 5 C++11 ABI change

* Tue Feb 17 2015 Rex Dieter <rdieter@fedoraproject.org> 6.0-2
- duplicate directory between pulseaudio and pulseaudio-libs (#909690)

* Fri Feb 13 2015 Rex Dieter <rdieter@fedoraproject.org> 6.0-1
- pulseaudio-6.0 (#1192384)

* Thu Jan 22 2015 Rex Dieter <rdieter@fedoraproject.org> 5.99.3-1
- pulseaudio-5.99.3 (6.0-rc3) (#1184850)

* Sat Dec 20 2014 Rex Dieter <rdieter@fedoraproject.org> 5.99.2-2
- fix changelog

* Fri Dec 19 2014 Rex Dieter <rdieter@fedoraproject.org> 5.99.2-1
- pulseaudio-5.99.2 (6.0-rc2)

* Fri Nov 21 2014 Rex Dieter <rdieter@fedoraproject.org> 5.99.1-1
- pulseaudio-5.99.1 (6.0-rc1)

* Fri Nov 14 2014 Rex Dieter <rdieter@fedoraproject.org> 5.0-100.20141103gitaec81
- artificially bump Release to 100, to ensure upgrade path

* Thu Nov 06 2014 Rex Dieter <rdieter@fedoraproject.org> 5.0-24.20141103gitaec81
- --disable-systemd-daemon, revert to autospawn mode

* Thu Nov 06 2014 Rex Dieter <rdieter@fedoraproject.org> - 5.0-23.20141103gitaec81
- 20141103 327-gaec81 snapshot, pulseaudio socket activation support
- use bash completionsdir

* Wed Nov 05 2014 Orion Poplawski <orion@cora.nwra.com> 5.0-22.20141007git4971d 
- Really add pulse-rt group when needed (bug #885020)

* Wed Oct 22 2014 Rex Dieter <rdieter@fedoraproject.org> 5.0-21.20141007git4971d 
- BR: automake libtool (for bootstrap.sh)

* Wed Oct 22 2014 Rex Dieter <rdieter@fedoraproject.org> 5.0-20.20141007git4971d
- snapshot, with wip bt headset2 patches (#1045548,#1067470)

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jul 29 2014 Kalev Lember <kalevlember@gmail.com> - 5.0-9
- Rebuilt once more for libjson-c

* Mon Jul 28 2014 Peter Robinson <pbrobinson@fedoraproject.org> 5.0-8
- Rebuild (libjson-c)

* Wed Jul 16 2014 Rex Dieter <rdieter@fedoraproject.org> 5.0-7
- Provide padsp-32, /usr/bin/padsp is native arch only (#856146)

* Mon Jul 07 2014 Rex Dieter <rdieter@fedoraproject.org> - 5.0-6
- rtp-recv: fix crash on empty UDP packets (CVE-2014-3970,#1104835,#1108011)
- name HDMI outputs uniquely

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue May 13 2014 Dan Horák <dan[at]danny.cz> 5.0-4
- always run tests, but don't fail the build on big endian arches (relates #1067470)

* Sat Apr 12 2014 Rex Dieter <rdieter@fedoraproject.org> 5.0-3
- Pulse Audio settings lost after reboot / HDMI is set as default (#1035025)

* Tue Mar 11 2014 Rex Dieter <rdieter@fedoraproject.org> 5.0-2
- drop Requires: kernel (per recent -devel ml thread)

* Tue Mar 04 2014 Rex Dieter <rdieter@fedoraproject.org> 5.0-1
- 5.0 (#1072259)

* Wed Feb 26 2014 Karsten Hopp <karsten@redhat.com> 4.99.4-3
- disable make check on PPC* (rhbz #1067470)

* Mon Feb 17 2014 Rex Dieter <rdieter@fedoraproject.org> 4.99.4-2
- -qpaeq subpkg (#1002585)

* Sat Feb 15 2014 Rex Dieter <rdieter@fedoraproject.org> 4.99.4-1
- 4.99.4

* Wed Jan 29 2014 Rex Dieter <rdieter@fedoraproject.org> 4.99.3-1
- 4.99.3

* Mon Jan 27 2014 Wim Taymans <wtaymans@redhat.com> - 4.99.2-2
- don't mark .desktop and dbus configurations as %%config

* Fri Jan 24 2014 Rex Dieter <rdieter@fedoraproject.org> - 4.99.2-1
- 4.99.2 (#1057528)

* Wed Jan 22 2014 Wim Taymans <wtaymans@redhat.com> - 4.0-12.gitf81e3
- Use the statically allocated UID and GID from /usr/share/doc/setup/uidgid (#1056656)
- The pulse-rt group doesn't exist (#885020)

* Wed Jan 22 2014 Rex Dieter <rdieter@fedoraproject.org> - 4.0-11.gitf81e3
- handle jack/lirc modules better (#1056619)
- -libs-devel: own some dirs to avoid deps on cmake/vala
- -module-bluetooth: make dep arch'd for consistency

* Fri Jan 10 2014 Rex Dieter <rdieter@fedoraproject.org> - 4.0-10.gitf81e3
- enable hardened build (#983606)

* Sat Dec 07 2013 Rex Dieter <rdieter@fedoraproject.org> - 4.0-9.gitf81e3
- X-KDE-autostart-phase=1

* Wed Oct 30 2013 Rex Dieter <rdieter@fedoraproject.org> - 4.0-8.gitf81e3
- fix PACKAGE_VERSION

* Mon Oct 14 2013 Rex Dieter <rdieter@fedoraproject.org> - 4.0-7.gitf81e3
- %%build fix typo, explicitly --enable-tests

* Mon Oct 14 2013 Rex Dieter <rdieter@fedoraproject.org> - 4.0-6.gitf81e3 
- ship a single autostart file

* Fri Oct 11 2013 Rex Dieter <rdieter@fedoraproject.org> - 4.0-5.gitf81e3
- fresh snapshot

* Mon Sep 23 2013 Kalev Lember <kalevlember@gmail.com> - 4.0-4.gita89ca
- Update to today's git snapshot
- Backport a patch for pulseaudio crash at startup (#1000966)

* Thu Aug 15 2013 Kalev Lember <kalevlember@gmail.com> - 4.0-3.gitbf9b3
- Update to git snapshot bf9b3f0 for BlueZ 5 support

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jun  4 2013 Peter Robinson <pbrobinson@fedoraproject.org> 4.0-1
- New 4.0 stable release
- https://www.freedesktop.org/wiki/Software/PulseAudio/Notes/4.0/

* Thu May 30 2013 Rex Dieter <rdieter@fedoraproject.org> 3.99.2-2
- [RFE] Build with libcap (#969232)

* Sun May 26 2013 Peter Robinson <pbrobinson@fedoraproject.org> 3.99.2-1
- pulseaudio-3.99.2 (#966631)

* Fri May 03 2013 Rex Dieter <rdieter@fedoraproject.org> 3.99.1-1
- pulseaudio-3.99.1 (#952594)
- RFE: Restore the pipe-sink and pipe-source modules (#958949)
- prune (pre 1.x) changelog

* Thu Apr 11 2013 Rex Dieter <rdieter@fedoraproject.org> 3.0-7
- pull a few more patches from upstream stable-3.x branch

* Fri Feb 08 2013 Rex Dieter <rdieter@fedoraproject.org> 3.0-6
- default.pa: fix for renamed modules (#908117)

* Sat Jan 19 2013 Ville Skyttä <ville.skytta@iki.fi> - 3.0-5
- Own the %%{_libdir}/pulseaudio dir.
- Fix bogus %%changelog dates.

* Fri Jan 04 2013 Rex Dieter <rdieter@fedoraproject.org> 3.0-4
- alsa-mixer: Fix the analog-output-speaker-always path

* Fri Jan 04 2013 Rex Dieter <rdieter@fedoraproject.org> 3.0-3
- move libpulsedsp plugin to -libs, avoids -utils multilib (#891425)

* Wed Dec 19 2012 Dan Horák <dan[at]danny.cz> 3.0-2
- SBC is needed only when BlueZ is used

* Tue Dec 18 2012 Rex Dieter <rdieter@fedoraproject.org> 3.0-1
- pulseaudio-3.0

* Tue Dec 11 2012 Peter Robinson <pbrobinson@fedoraproject.org> 2.99.3-1
- PulseAudio 2.99.3 (3.0 rc3)

* Wed Oct 10 2012 Dan Horák <dan[at]danny.cz> 2.1-4
- fix the with_webrtc condition

* Tue Oct 09 2012 Dan Horák <dan[at]danny.cz> 2.1-3
- webrtc-aec is x86 and ARM only for now

* Mon Oct 08 2012 Debarshi Ray <rishi@fedoraproject.org> 2.1-2
- Enable webrtc-aec

* Tue Sep 25 2012 Rex Dieter <rdieter@fedoraproject.org> 2.1-1
- pulseaudio-2.1

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jun 23 2012 Kalev Lember <kalevlember@gmail.com> - 2.0-3
- Move module-jackdbus-detect.so to -module-jack subpackage with the
  rest of the jack modules

* Mon Jun 04 2012 Kay Sievers <kay@redhat.com> - 2.0-2
- rebuild for libudev1

* Sat May 12 2012 Rex Dieter <rdieter@fedoraproject.org> 2.0-1
- pulseaudio-2.0

* Sat Apr 21 2012 Matthias Clasen <mclasen@redhat.com> - 1.1-9
- Don't load the ck module in gdm, either

* Tue Feb 28 2012 Bruno Wolff III <bruno@wolff.to> - 1.1-8
- Bring in Lennart's patch from f17
- Temporary fix for CK/systemd move (#794690)

* Tue Feb 28 2012 Bruno Wolff III <bruno@wolff.to> - 1.1-7
- Fix for building with gcc 4.7

* Mon Jan 23 2012 Dan Horák <dan@danny.cz> - 1.1-6
- rebuilt for json-c-0.9-4.fc17

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 13 2011 Adam Jackson <ajax@redhat.com> 1.1-4
- Fix RHEL build

* Tue Nov 22 2011 Rex Dieter <rdieter@fedoraproject.org> 1.1-3
- Obsoletes: padevchooser < 1.0

* Thu Nov 10 2011 Rex Dieter <rdieter@fedoraproject.org> 1.1-2
- -libs: Obsoletes: pulseaudio-libs-zeroconf
- use versioned Obsoletes/Provides
- tighten subpkg deps via %%_isa
- remove autoconf/libtool hackery

* Thu Nov  3 2011 Lennart Poettering <lpoetter@redhat.com> - 1.1-1
- New upstream release
