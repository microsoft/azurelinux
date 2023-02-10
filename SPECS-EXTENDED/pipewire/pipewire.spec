%global majorversion 0
%global minorversion 3
%global microversion 60
%global apiversion   0.3
%global spaversion   0.2
%global soversion    0
%global libversion   %{soversion}.%(bash -c '((intversion = (%{minorversion} * 100) + %{microversion})); echo ${intversion}').0
%global ms_version   0.4.1
%global _hardened_build 1
# where/how to apply multilib hacks
%global multilib_archs x86_64 %{ix86}
# Build conditions for various features
%bcond_without alsa
%bcond_without vulkan
%bcond_without media_session
%bcond_without libusb
%bcond_without v4l2
Summary:        Media Sharing Server
Name:           pipewire
Version:        %{majorversion}.%{minorversion}.%{microversion}
Release:        2%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://pipewire.org/
Source0:        https://github.com/PipeWire/%{name}/archive/refs/tags/%{version}.tar.gz#/%{name}-%{version}.tar.gz
%if %{with media_session}
Source1:        https://gitlab.freedesktop.org/pipewire/media-session/-/archive/%{ms_version}/media-session-%{ms_version}.tar.gz
Patch0:      0001-Build-media-session-from-local-tarbal.patch
%endif
BuildRequires:  gettext
BuildRequires:  meson >= 0.59.0
BuildRequires:  gcc
BuildRequires:  g++
BuildRequires:  pkgconfig
#BuildRequires:  pkgconfig(libudev)
BuildRequires:  pkgconfig(dbus-1)
BuildRequires:  pkgconfig(glib-2.0) >= 2.32
BuildRequires:  pkgconfig(gio-unix-2.0) >= 2.32
BuildRequires:  pkgconfig(gstreamer-1.0) >= 1.10.0
BuildRequires:  pkgconfig(gstreamer-base-1.0) >= 1.10.0
BuildRequires:  pkgconfig(gstreamer-plugins-base-1.0) >= 1.10.0
BuildRequires:  pkgconfig(gstreamer-net-1.0) >= 1.10.0
BuildRequires:  pkgconfig(gstreamer-allocators-1.0) >= 1.10.0
BuildRequires:  pkgconfig(fdk-aac)
%if %{with vulkan}
BuildRequires:  pkgconfig(vulkan)
%endif
BuildRequires:  pkgconfig(bluez)
#BuildRequires:  systemd
BuildRequires:  systemd-devel
BuildRequires:  alsa-lib-devel
BuildRequires:  libv4l-devel
BuildRequires:  doxygen
BuildRequires:  graphviz
BuildRequires:  sbc-devel
BuildRequires:  libsndfile-devel
BuildRequires:  ncurses-devel
BuildRequires:  pulseaudio-libs-devel
BuildRequires:  avahi-devel
BuildRequires:  pkgconfig(webrtc-audio-processing) >= 0.2
%if %{with libusb}
BuildRequires:  libusb-devel
%endif
BuildRequires:  readline-devel
BuildRequires:  lilv-devel
BuildRequires:  openssl-devel
BuildRequires:  libcanberra-devel
BuildRequires:  python3-docutils

Requires(pre):  shadow-utils
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
Requires:       systemd
Requires:       rtkit
# A virtual Provides so we can swap session managers
Requires:       pipewire-session-manager
# Prefer WirePlumber for session manager
Suggests:       wireplumber

%description
PipeWire is a multimedia server for Linux and other Unix like operating
systems.

%package libs
Summary:        Libraries for PipeWire clients
Recommends:     %{name}%{?_isa} = %{version}-%{release}
Obsoletes:      %{name}-libpulse < %{version}-%{release}

%description libs
This package contains the runtime libraries for any application that wishes
to interface with a PipeWire media server.

%package gstreamer
Summary:        GStreamer elements for PipeWire
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
Recommends:     %{name}%{?_isa} = %{version}-%{release}

%description gstreamer
This package contains GStreamer elements to interface with a
PipeWire media server.

%package devel
Summary:        Headers and libraries for PipeWire client development
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}

%description devel
Headers and libraries for developing applications that can communicate with
a PipeWire media server.

%package doc
Summary:        PipeWire media server documentation

%description doc
This package contains documentation for the PipeWire media server.

%package utils
Summary:        PipeWire media server utilities
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}

%description utils
This package contains command line utilities for the PipeWire media server.

%if %{with media_session}
%package media-session
Summary:        PipeWire Media Session Manager
Recommends:     %{name}%{?_isa} = %{version}-%{release}
# before 0.3.30-5 the session manager was in the main pipewire package
Conflicts:      %{name}%{?_isa} < 0.3.30-5
Conflicts:      pipewire-session-manager
Obsoletes:      %{name}-libpulse < %{version}-%{release}
# Virtual Provides to support swapping between PipeWire session manager implementations
Provides:       pipewire-session-manager

%description media-session
This package contains the reference Media Session Manager for the
PipeWire media server.
%endif

%if %{with alsa}
%package alsa
Summary:        PipeWire media server ALSA support
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
Recommends:     %{name}%{?_isa} = %{version}-%{release}
# Ensure this is provided by default to route all audio
Supplements:    %{name} = %{version}-%{release}
# Replace PulseAudio and JACK ALSA plugins with PipeWire
## N.B.: If alsa-plugins gets updated in F33, this will need to be bumped
Obsoletes:      alsa-plugins-jack < 1.2.2-5
Obsoletes:      alsa-plugins-pulseaudio < 1.2.2-5

%description alsa
This package contains an ALSA plugin for the PipeWire media server.
%endif

%package pulseaudio
Summary:        PipeWire PulseAudio implementation
BuildRequires:  pulseaudio-libs
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
Requires:       pulseaudio-utils
Recommends:     %{name}%{?_isa} = %{version}-%{release}
# Ensure this is provided by default to route all audio
Supplements:    %{name} = %{version}-%{release}
# Fixed pulseaudio subpackages
Conflicts:      %{name}-libpulse < 0.3.13-6
Conflicts:      %{name}-pulseaudio < 0.3.13-6
Conflicts:      pulseaudio
Conflicts:      pulseaudio-daemon
# Replace PulseAudio with PipeWire-PulseAudio
## N.B.: If pulseaudio gets updated in F33, this will need to be bumped
Obsoletes:      pulseaudio < 14.2-3
Obsoletes:      pulseaudio-esound-compat < 14.2-3
Obsoletes:      pulseaudio-module-bluetooth < 14.2-3
Obsoletes:      pulseaudio-module-gconf < 14.2-3
Obsoletes:      pulseaudio-module-gsettings < 14.2-3
Obsoletes:      pulseaudio-module-jack < 14.2-3
Obsoletes:      pulseaudio-module-lirc < 14.2-3
Obsoletes:      pulseaudio-module-x11 < 14.2-3
Obsoletes:      pulseaudio-module-zeroconf < 14.2-3
Obsoletes:      pulseaudio-qpaeq < 14.2-3
# Virtual Provides to support swapping between PipeWire-PA and PA
Provides:       pulseaudio-daemon
Provides:       pulseaudio-module-bluetooth
Provides:       pulseaudio-module-jack

%description pulseaudio
This package provides a PulseAudio implementation based on PipeWire

%if %{with v4l2}
%package v4l2
Summary:        PipeWire media server v4l2 LD_PRELOAD support
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
Recommends:     %{name}%{?_isa} = %{version}-%{release}

%description v4l2
This package contains an LD_PRELOAD library that redirects v4l2 applications to
PipeWire.
%endif

%prep
%autosetup -p1 -n %{name}-%{version}

%if %{with media_session}
mkdir subprojects/packagefiles
cp %{SOURCE1} subprojects/packagefiles/
%endif

%build
%meson \
    -D docs=enabled -D man=enabled -D gstreamer=enabled -D systemd=enabled	\
    -D gstreamer-device-provider=disabled -D sdl2=disabled 			\
    -D audiotestsrc=disabled -D videotestsrc=disabled				\
    -D volume=disabled -D bluez5-codec-aptx=disabled -D roc=disabled 		\
    -D bluez5-codec-lc3plus=disabled						\
    -D bluez5-codec-ldac=disabled						\
    -D bluez5-codec-opus=disabled                                               \
    -D x11-xfixes=disabled                                                      \
%if %{with media_session}
    -D session-managers="media-session" 	         			\
%else
    -D session-managers=[]                           				\
%endif
    %{!?with_jack:-D pipewire-jack=disabled} 					\
    %{!?with_jackserver_plugin:-D jack=disabled} 				\
    %{!?with_libcamera_plugin:-D libcamera=disabled} 				\
    %{?with_jack:-D jack-devel=true} 						\
    %{!?with_alsa:-D pipewire-alsa=disabled}					\
    %{?with_vulkan:-D vulkan=enabled}						\
    %{!?with_libusb:-D libusb=disabled}
%meson_build

%install
%meson_install

rm %{buildroot}%{_datadir}/pipewire/jack.conf

%if %{with media_session}
rm %{buildroot}%{_datadir}/pipewire/media-session.d/with-jack
%endif

%if %{with alsa}
mkdir -p %{buildroot}%{_sysconfdir}/alsa/conf.d/
cp %{buildroot}%{_datadir}/alsa/alsa.conf.d/50-pipewire.conf \
        %{buildroot}%{_sysconfdir}/alsa/conf.d/50-pipewire.conf
cp %{buildroot}%{_datadir}/alsa/alsa.conf.d/99-pipewire-default.conf \
        %{buildroot}%{_sysconfdir}/alsa/conf.d/99-pipewire-default.conf
%if %{with media_session}
touch %{buildroot}%{_datadir}/pipewire/media-session.d/with-alsa
%endif

%endif

%find_lang %{name}
%if %{with media_session}
%find_lang media-session
%endif

# upstream should use udev.pc
mkdir -p %{buildroot}%{_libdir}/udev/rules.d
mv -fv %{buildroot}/lib/udev/rules.d/90-pipewire-alsa.rules %{buildroot}%{_libdir}/udev/rules.d

# AMD64-Build-Fix:
# Build requires pkg "gstreamer1" installs fileattrs to provide rpm dependency generation
# macros for shared libraries installed under "%{_libdir}/gstreamer-1.0/" path.
# However, the generator script gstreamer1.prov is stuck when generating the provides list
# causing the build to hang when building in amd64 docker enviroment.
# The plugin loader helper binary "gst-plugin-scanner" causes this hang issue.
# Disabling the binary fixes the hang and gst-inspect-1.0 binary successfully parses the
# plugin and generates the rpm provides information.
rm %{_libexecdir}/gstreamer-1.0/gst-plugin-scanner

%check
%meson_test

%pre
getent group pipewire >/dev/null || groupadd -r pipewire
getent passwd pipewire >/dev/null || \
    useradd -r -g pipewire -d %{_localstatedir}/run/pipewire -s /sbin/nologin -c "PipeWire System Daemon" pipewire
exit 0

%post
%systemd_user_post pipewire.service
%systemd_user_post pipewire.socket

%triggerun -- %{name} < 0.3.6-2
# This is for upgrades from previous versions which had a static symlink.
# The %%post scriptlet above only does anything on initial package installation.
# Remove before F33.
systemctl --no-reload preset --global pipewire.socket >/dev/null 2>&1 || :

%post pulseaudio
%systemd_user_post pipewire-pulse.service
%systemd_user_post pipewire-pulse.socket

%if %{with media_session}
%post media-session
%systemd_user_post pipewire-media-session.service
%endif

%files
%license LICENSE COPYING
%doc README.md
%{_userunitdir}/pipewire.*
%{_userunitdir}/filter-chain.*
%{_bindir}/pipewire
%{_bindir}/pipewire-avb
%{_mandir}/man1/pipewire.1*
%dir %{_datadir}/pipewire/
%{_datadir}/pipewire/pipewire.conf
%{_datadir}/pipewire/minimal.conf
%{_datadir}/pipewire/filter-chain.conf
%{_datadir}/pipewire/filter-chain/*.conf
%{_datadir}/pipewire/pipewire-avb.conf
%{_mandir}/man5/pipewire.conf.5*

%if %{with media_session}
%files media-session -f media-session.lang
%{_bindir}/pipewire-media-session
%{_userunitdir}/pipewire-media-session.service
%dir %{_datadir}/pipewire/media-session.d/
%{_datadir}/pipewire/media-session.d/alsa-monitor.conf
%{_datadir}/pipewire/media-session.d/bluez-monitor.conf
%{_datadir}/pipewire/media-session.d/media-session.conf
%{_datadir}/pipewire/media-session.d/v4l2-monitor.conf

%if %{with alsa}
%{_datadir}/pipewire/media-session.d/with-alsa
%endif
%{_datadir}/pipewire/media-session.d/with-pulseaudio
%endif

%files libs -f %{name}.lang
%license LICENSE COPYING
%doc README.md
%{_libdir}/libpipewire-%{apiversion}.so.*
%{_libdir}/pipewire-%{apiversion}/libpipewire-*.so
%dir %{_datadir}/alsa-card-profile/
%dir %{_datadir}/alsa-card-profile/mixer/
%{_datadir}/alsa-card-profile/mixer/paths/
%{_datadir}/alsa-card-profile/mixer/profile-sets/
%dir %{_datadir}/spa-0.2/
%{_datadir}/spa-0.2/bluez5/bluez-hardware.conf
%{_libdir}/udev/rules.d/90-pipewire-alsa.rules
%dir %{_libdir}/spa-%{spaversion}
%{_libdir}/spa-%{spaversion}/aec/
%{_libdir}/spa-%{spaversion}/alsa/
%{_libdir}/spa-%{spaversion}/audioconvert/
%{_libdir}/spa-%{spaversion}/audiomixer/
%{_libdir}/spa-%{spaversion}/avb/
%{_libdir}/spa-%{spaversion}/bluez5/
%{_libdir}/spa-%{spaversion}/control/
%{_libdir}/spa-%{spaversion}/support/
%{_libdir}/spa-%{spaversion}/v4l2/
%{_libdir}/spa-%{spaversion}/videoconvert/
%if %{with vulkan}
%{_libdir}/spa-%{spaversion}/vulkan/
%endif
%{_datadir}/pipewire/client.conf
%{_datadir}/pipewire/client-rt.conf

%files gstreamer
%{_libdir}/gstreamer-1.0/libgstpipewire.*

%files devel
%{_libdir}/libpipewire-%{apiversion}.so
%{_includedir}/pipewire-%{apiversion}/
%{_includedir}/spa-%{spaversion}/
%{_libdir}/pkgconfig/libpipewire-%{apiversion}.pc
%{_libdir}/pkgconfig/libspa-%{spaversion}.pc

%files doc
%{_datadir}/doc/pipewire/html

%files utils
%{_bindir}/pw-mon
%{_bindir}/pw-metadata
%{_bindir}/pw-dsdplay
%{_bindir}/pw-mididump
%{_bindir}/pw-midiplay
%{_bindir}/pw-midirecord
%{_bindir}/pw-cli
%{_bindir}/pw-dot
%{_bindir}/pw-cat
%{_bindir}/pw-dump
%{_bindir}/pw-link
%{_bindir}/pw-loopback
%{_bindir}/pw-play
%{_bindir}/pw-profiler
%{_bindir}/pw-record
%{_bindir}/pw-reserve
%{_bindir}/pw-top
%{_mandir}/man1/pw-mon.1*
%{_mandir}/man1/pw-cli.1*
%{_mandir}/man1/pw-cat.1*
%{_mandir}/man1/pw-dot.1*
%{_mandir}/man1/pw-link.1*
%{_mandir}/man1/pw-metadata.1*
%{_mandir}/man1/pw-mididump.1*
%{_mandir}/man1/pw-profiler.1*
%{_mandir}/man1/pw-top.1*

%{_bindir}/spa-acp-tool
%{_bindir}/spa-inspect
%{_bindir}/spa-json-dump
%{_bindir}/spa-monitor
%{_bindir}/spa-resample

%if %{with alsa}
%files alsa
%{_libdir}/alsa-lib/libasound_module_pcm_pipewire.so
%{_libdir}/alsa-lib/libasound_module_ctl_pipewire.so
%{_datadir}/alsa/alsa.conf.d/50-pipewire.conf
%{_datadir}/alsa/alsa.conf.d/99-pipewire-default.conf
%config(noreplace) %{_sysconfdir}/alsa/conf.d/50-pipewire.conf
%config(noreplace) %{_sysconfdir}/alsa/conf.d/99-pipewire-default.conf
%endif

%files pulseaudio
%{_bindir}/pipewire-pulse
%{_mandir}/man1/pipewire-pulse.1*
%{_userunitdir}/pipewire-pulse.*
%{_datadir}/pipewire/pipewire-pulse.conf

%if %{with v4l2}
%files v4l2
%{_bindir}/pw-v4l2
%{_libdir}/pipewire-%{apiversion}/v4l2/libpw-v4l2.so
%endif

%changelog
* Thu Nov 24 2022 Sumedh Sharma <sumsharma@microsoft.com> - 0.3.60-2
- Initial CBL-Mariner import from Fedora 37 (license: MIT)
- Build with features disabled: jack, jackserver-plugin and libcamera-plugin
- Enable check section
- License verified

* Thu Nov 10 2022 Wim Taymans <wtaymans@redhat.com> - 0.3.60-1
- Update version to 0.3.60

* Fri Oct 21 2022 Wim Taymans <wtaymans@redhat.com> - 0.3.59-4
- Add a patch to fix midi processing in some cases.
- Add a patch to fix crash when exiting some JACK apps such as
  Ardour7.
- Add a patch to fix a crash when switching bluetooth profiles.
- Add a patch to fix bluetooth source switching between drivers.

* Thu Oct 06 2022 Wim Taymans <wtaymans@redhat.com> - 0.3.59-3
- Rebuild with new libcamera.

* Tue Oct 04 2022 Wim Taymans <wtaymans@redhat.com> - 0.3.59-2
- Rebuild with new libcamera.

* Fri Sep 30 2022 Wim Taymans <wtaymans@redhat.com> - 0.3.59-1
- Update version to 0.3.59

* Thu Sep 22 2022 Wim Taymans <wtaymans@redhat.com> - 0.3.58-3
- Add patch to fix ffmpeg capture and other stutterings.

* Mon Sep 19 2022 Wim Taymans <wtaymans@redhat.com> - 0.3.58-2
- Add patch to fix stuttering in Teamspeak.

* Thu Sep 15 2022 Wim Taymans <wtaymans@redhat.com> - 0.3.58-1
- Update version to 0.3.58

* Fri Sep 2 2022 Wim Taymans <wtaymans@redhat.com> - 0.3.57-1
- Update version to 0.3.57
- Add systemd BuildRequires

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.56-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue Jul 19 2022 Wim Taymans <wtaymans@redhat.com> - 0.3.56-1
- Update version to 0.3.56

* Tue Jul 12 2022 Wim Taymans <wtaymans@redhat.com> - 0.3.55-2
- Add patch to avoid crash in JACK.

* Tue Jul 12 2022 Wim Taymans <wtaymans@redhat.com> - 0.3.55-1
- Update version to 0.3.55

* Thu Jul 07 2022 Wim Taymans <wtaymans@redhat.com> - 0.3.54-1
- Update version to 0.3.54

* Mon Jul 4 2022 Wim Taymans <wtaymans@redhat.com> - 0.3.53-4
- Add channel remap patch.

* Mon Jul 4 2022 Wim Taymans <wtaymans@redhat.com> - 0.3.53-3
- Add patch to fix speaker-test.
- Add patch to fix noise in resampler.

* Fri Jul 1 2022 Wim Taymans <wtaymans@redhat.com> - 0.3.53-2
- Add patch to avoid crash in audioconvert (mpv)

* Thu Jun 30 2022 Wim Taymans <wtaymans@redhat.com> - 0.3.53-1
- Update version to 0.3.53

* Thu Jun 23 2022 Wim Taymans <wtaymans@redhat.com> - 0.3.52-4
- Add patch to remove 44.1KHz from samplerates
- See rhbz#2096193

* Wed Jun 15 2022 Wim Taymans <wtaymans@redhat.com> - 0.3.52-3
- Add patch to fix stuttering in TeamSpeak.
- Inc baserel to 3, previous build was accidentally done with 2
  instead of 1.

* Thu Jun 09 2022 Wim Taymans <wtaymans@redhat.com> - 0.3.52-1
- Update version to 0.3.52
- Disable LC3plus codec.

* Thu May 19 2022 Wim Taymans <wtaymans@redhat.com> - 0.3.51-2
- Add pulseaudio-utils as Requires for pipewire-pulseaudio

* Thu Apr 28 2022 Wim Taymans <wtaymans@redhat.com> - 0.3.51-1
- Update version to 0.3.51

* Wed Apr 13 2022 Wim Taymans <wtaymans@redhat.com> - 0.3.50-1
- Update version to 0.3.50

* Tue Mar 29 2022 Wim Taymans <wtaymans@redhat.com> - 0.3.49-1
- Update version to 0.3.49
- libusb was removed from f37

* Thu Mar 3 2022 Wim Taymans <wtaymans@redhat.com> - 0.3.48-1
- Update version to 0.3.48

* Fri Feb 18 2022 Wim Taymans <wtaymans@redhat.com> - 0.3.47-1
- Update version to 0.3.47

* Thu Feb 17 2022 Wim Taymans <wtaymans@redhat.com> - 0.3.46-1
- Update version to 0.3.46

* Mon Feb 7 2022 Wim Taymans <wtaymans@redhat.com> - 0.3.45-2
- Add patch for kernels with CONFIG_SND_VERBOSE_PROCFS=n
- Add patch to make Musescore work again

* Thu Feb 3 2022 Wim Taymans <wtaymans@redhat.com> - 0.3.45-1
- Update version to 0.3.45

* Thu Jan 27 2022 Wim Taymans <wtaymans@redhat.com> - 0.3.44-1
- Update version to 0.3.44

* Tue Jan 25 2022 Wim Taymans <wtaymans@redhat.com> - 0.3.43-5
- Add more patches to avoid segfaults in bluez5

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.43-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Jan 18 2022 Wim Taymans <wtaymans@redhat.com> - 0.3.43-3
- Add patch to avoid segfault in bluez5 (rhbz#2041481)

* Mon Jan 17 2022 Wim Taymans <wtaymans@redhat.com> - 0.3.43-2
- Add patch to avoid segfault in bluez5 (rhbz#2041481)

* Wed Jan 5 2022 Wim Taymans <wtaymans@redhat.com> - 0.3.43-1
- Update version to 0.3.43

* Thu Dec 16 2021 Wim Taymans <wtaymans@redhat.com> - 0.3.42-1
- Update version to 0.3.42

* Mon Dec 13 2021 Wim Taymans <wtaymans@redhat.com> - 0.3.41-1
- Update version to 0.3.41

* Thu Nov 11 2021 Wim Taymans <wtaymans@redhat.com> - 0.3.40-1
- Update version to 0.3.40 and media-session 0.4.1
- Enable tests for s390x again

* Tue Nov 09 2021 Peter Hutterer <peter.hutterer@redhat.com> - 0.3.39-3
- Don't build media-session on F35, it's a separate package now, see #2016247

* Wed Oct 27 2021 Peter Hutterer <peter.hutterer@redhat.com> - 0.3.39-2
- Don't build media-session on F36, it's a separate package now, see #2016247
- Remove versioned systemd dependency, 184 was released in 2012

* Thu Oct 21 2021 Wim Taymans <wtaymans@redhat.com> - 0.3.39-1
- Update version to 0.3.39

* Wed Oct 13 2021 Neal Gompa <ngompa@fedoraproject.org> - 0.3.38-2
- Fix libcamera bcond to work properly in RHEL10+ and F36+

* Thu Sep 30 2021 Wim Taymans <wtaymans@redhat.com> - 0.3.38-1
- Update version to 0.3.38

* Wed Sep 29 2021 Wim Taymans <wtaymans@redhat.com> - 0.3.37-3
- Rebuild for new libcamera

* Thu Sep 23 2021 Javier Martinez Canillas <javierm@redhat.com> - 0.3.37-2
- Enable libcamera SPA plugin

* Thu Sep 23 2021 Wim Taymans <wtaymans@redhat.com> - 0.3.37-1
- Update version to 0.3.37

* Thu Sep 16 2021 Wim Taymans <wtaymans@redhat.com> - 0.3.36-2
- Update version to 0.3.36

* Thu Sep 16 2021 Wim Taymans <wtaymans@redhat.com> - 0.3.36-1
- Update to 0.3.36
- Do systemd post install of pipewire-media-session.service

* Thu Sep 09 2021 Wim Taymans <wtaymans@redhat.com> - 0.3.35-2
- Add patch to fix passthrough check.

* Thu Sep 09 2021 Wim Taymans <wtaymans@redhat.com> - 0.3.35-1
- Update to 0.3.35

* Mon Aug 30 2021 Neal Gompa <ngompa@fedoraproject.org> - 0.3.34-2
- Add preference for WirePlumber for session manager (#1989959)

* Thu Aug 26 2021 Wim Taymans <wtaymans@redhat.com> - 0.3.34-1
- Update to 0.3.34

* Wed Aug 11 2021 Wim Taymans <wtaymans@redhat.com> - 0.3.33-3
- Add more upstream patches.

* Tue Aug 10 2021 Wim Taymans <wtaymans@redhat.com> - 0.3.33-2
- Add patch to fix default device persistence.

* Thu Aug 5 2021 Wim Taymans <wtaymans@redhat.com> - 0.3.33-1
- Update to 0.3.33

* Thu Aug 5 2021 Wim Taymans <wtaymans@redhat.com> - 0.3.32-4
- Add media-session Conflicts: with older pipewire versions, they can't be
  installed at the same time because they both contain the media-session binary.

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.32-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jul 21 2021 Neal Gompa <ngompa@fedoraproject.org> - 0.3.32-2
- Add conditional for media-session subpackage

* Tue Jul 20 2021 Wim Taymans <wtaymans@redhat.com> - 0.3.32-1
- Update to 0.3.32

* Thu Jul 15 2021 Peter Hutterer <peter.hutterer@redhat.com> - 0.3.31-4
- Enable media-session.service, requires fedora-release-35-0.10 to enable the
  service by default (#1976006).

* Mon Jul 05 2021 Neal Gompa <ngompa13@gmail.com> - 0.3.31-3
- Add "Conflicts: pipewire-session-manager" to pipewire-media-session
  to enforce one implementation of the session manager at a time

* Mon Jun 28 2021 Wim Taymans <wtaymans@redhat.com> - 0.3.31-2
- Fix session manager path

* Mon Jun 28 2021 Wim Taymans <wtaymans@redhat.com> - 0.3.31-1
- Update to 0.3.31

* Fri Jun 25 2021 Peter Hutterer <peter.hutterer@redhat.com> - 0.3.30-5
- Split media-session into a subpackage and Require it through a virtual
  Provides from the main pipewire package

* Tue Jun 15 2021 Łukasz Patron <priv.luk@gmail.com> - 0.3.30-4
- Add patch for setting node description for module-combine-sink

* Tue Jun 15 2021 Wim Taymans <wtaymans@redhat.com> - 0.3.30-3
- Rebuild for Gstreamer update

* Thu Jun 10 2021 Wim Taymans <wtaymans@redhat.com> - 0.3.30-2
- Add ALSA UCM 1.2.5 compatibility fixes

* Wed Jun 09 2021 Wim Taymans <wtaymans@redhat.com> - 0.3.30-1
- Update to 0.3.30

* Fri Jun 04 2021 Wim Taymans <wtaymans@redhat.com> - 0.3.29-2
- Add some important patches.

* Thu Jun 03 2021 Wim Taymans <wtaymans@redhat.com> - 0.3.29-1
- Update to 0.3.29

* Mon May 17 2021 Wim Taymans <wtaymans@redhat.com> - 0.3.28-1
- Update to 0.3.28

* Mon May 10 2021 Wim Taymans <wtaymans@redhat.com> - 0.3.27-2
- Add patch to fix volume issues.

* Thu May 06 2021 Wim Taymans <wtaymans@redhat.com> - 0.3.27-1
- Update to 0.3.27

* Thu Apr 29 2021 Wim Taymans <wtaymans@redhat.com> - 0.3.26-4
- Add some more important upstream patches.

* Mon Apr 26 2021 Wim Taymans <wtaymans@redhat.com> - 0.3.26-3
- Add some important upstream patches.

* Sat Apr 24 2021 Neal Gompa <ngompa13@gmail.com> - 0.3.26-2
- Disable JACK server integration on RHEL

* Thu Apr 22 2021 Wim Taymans <wtaymans@redhat.com> - 0.3.26-1
- Update to 0.3.26

* Tue Apr 20 2021 Neal Gompa <ngompa13@gmail.com> - 0.3.25-2
- Add jack-devel subpackage, enable JACK support on RHEL 9+ (#1945951)

* Tue Apr 06 2021 Wim Taymans <wtaymans@redhat.com> - 0.3.25-1
- Update to 0.3.25

* Thu Mar 25 2021 Wim Taymans <wtaymans@redhat.com> - 0.3.24-4
- Apply some critical upstream patches

* Thu Mar 25 2021 Kalev Lember <klember@redhat.com> - 0.3.24-3
- Fix RHEL build

* Thu Mar 25 2021 Kalev Lember <klember@redhat.com> - 0.3.24-2
- Move individual config files to the subpackages that make use of them

* Thu Mar 18 2021 Wim Taymans <wtaymans@redhat.com> - 0.3.24-1
- Update to 0.3.24

* Tue Mar 09 2021 Wim Taymans <wtaymans@redhat.com> - 0.3.23-2
- Add patch to enable UCM Microphones

* Thu Mar 04 2021 Wim Taymans <wtaymans@redhat.com> - 0.3.23-1
- Update to 0.3.23

* Wed Feb 24 2021 Wim Taymans <wtaymans@redhat.com> - 0.3.22-7
- Add patch to sample destroy use after free

* Wed Feb 24 2021 Wim Taymans <wtaymans@redhat.com> - 0.3.22-6
- Add patch for jack names

* Mon Feb 22 2021 Wim Taymans <wtaymans@redhat.com> - 0.3.22-5
- Add some critical patches

* Fri Feb 19 2021 Neal Gompa <ngompa13@gmail.com> - 0.3.22-4
- Replace more PulseAudio modules on upgrade in F34+

* Fri Feb 19 2021 Neal Gompa <ngompa13@gmail.com> - 0.3.22-3
- Replace ALSA plugins and PulseAudio modules on upgrade in F34+

* Fri Feb 19 2021 Neal Gompa <ngompa13@gmail.com> - 0.3.22-2
- Replace JACK and PulseAudio on upgrade in F34+
  Reference: https://fedoraproject.org/wiki/Changes/DefaultPipeWire

* Thu Feb 18 2021 Wim Taymans <wtaymans@redhat.com> - 0.3.22-1
- Update to 0.3.22
- disable sdl2 examples

* Thu Feb 04 2021 Wim Taymans <wtaymans@redhat.com> - 0.3.21-2
- Add some upstream patches
- Fixes rhbz#1925138

* Wed Feb 03 2021 Wim Taymans <wtaymans@redhat.com> - 0.3.21-1
- Update to 0.3.21

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.20-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jan 20 2021 Wim Taymans <wtaymans@redhat.com> - 0.3.20-1
- Update to 0.3.20
- Fix baseversion
- Add gettext dependency

* Tue Jan 12 2021 Neal Gompa <ngompa13@gmail.com> - 0.3.19-4
- Rework conditional build to fix ELN builds

* Sat Jan  9 2021 Evan Anderson <evan@eaanderson.com> - 0.3.19-3
- Add LDAC and AAC dependency to enhance Bluetooth support

* Thu Jan  7 2021 Neal Gompa <ngompa13@gmail.com> - 0.3.19-2
- Obsolete useless libjack subpackage with jack-audio-connection-kit subpackage

* Tue Jan 5 2021 Wim Taymans <wtaymans@redhat.com> - 0.3.19-1
- Update to 0.3.19
- Add ncurses-devel BR

* Tue Dec 15 2020 Wim Taymans <wtaymans@redhat.com> - 0.3.18-1
- Update to 0.3.18

* Fri Nov 27 2020 Wim Taymans <wtaymans@redhat.com> - 0.3.17-2
- Add some more Provides: for pulseaudio

* Thu Nov 26 2020 Wim Taymans <wtaymans@redhat.com> - 0.3.17-1
- Update to 0.3.17

* Tue Nov 24 2020 Neal Gompa <ngompa13@gmail.com> - 0.3.16-4
- Add 'pulseaudio-daemon' Provides + Conflicts to pipewire-pulseaudio
- Remove useless ldconfig macros that expand to nothing

* Fri Nov 20 2020 Wim Taymans <wtaymans@redhat.com> - 0.3.16-3
- Fix Requires for pipewire-pulseaudio
- Fixes rhbz#1899945

* Fri Nov 20 2020 Wim Taymans <wtaymans@redhat.com> - 0.3.16-2
- Add patch to fix crash in kwin, Fixes rhbz#1899826

* Thu Nov 19 2020 Wim Taymans <wtaymans@redhat.com> - 0.3.16-1
- Update to 0.3.16

* Wed Nov 4 2020 Wim Taymans <wtaymans@redhat.com> - 0.3.15-2
- Add patch to fix screen sharing for old clients

* Wed Nov 4 2020 Wim Taymans <wtaymans@redhat.com> - 0.3.15-1
- Update to 0.3.15

* Sun Nov 1 2020 Wim Taymans <wtaymans@redhat.com> - 0.3.14-2
- Add some pulse server patches

* Fri Oct 30 2020 Wim Taymans <wtaymans@redhat.com> - 0.3.14-1
- Update to 0.3.14

* Sun Oct 18 2020 Neal Gompa <ngompa13@gmail.com> - 0.3.13-6
- Fix jack and pulseaudio subpackages to generate dependencies properly

* Tue Oct 13 2020 Wim Taymans <wtaymans@redhat.com> - 0.3.13-5
- Disable device provider for now
- Fixes rhbz#1884260

* Thu Oct 1 2020 Wim Taymans <wtaymans@redhat.com> - 0.3.13-4
- Add patches for some crasher bugs
- Fixes rhbz#1884177

* Tue Sep 29 2020 Wim Taymans <wtaymans@redhat.com> - 0.3.13-3
- Add patch to improve pulse compatibility

* Mon Sep 28 2020 Jeff Law <law@redhat.com> - 0.3.13-2
- Re-enable LTO as upstream GCC target/96939 has been fixed

* Mon Sep 28 2020 Wim Taymans <wtaymans@redhat.com> - 0.3.13-1
- Update to 0.3.13

* Fri Sep 18 2020 Wim Taymans <wtaymans@redhat.com> - 0.3.12-1
- Update to 0.3.12

* Fri Sep 11 2020 Wim Taymans <wtaymans@redhat.com> - 0.3.11-2
- Add some patches to improve pulse compatibility

* Thu Sep 10 2020 Wim Taymans <wtaymans@redhat.com> - 0.3.11-1
- Update to 0.3.11

* Mon Aug 17 2020 Wim Taymans <wtaymans@redhat.com> - 0.3.10-1
- Update to 0.3.10

* Tue Aug 04 2020 Wim Taymans <wtaymans@redhat.com> - 0.3.9-1
- Update to 0.3.9

* Tue Aug 04 2020 Wim Taymans <wtaymans@redhat.com> - 0.3.8-3
- Add patch to avoid segfault when iterating ports.
- Fixes #1865827

* Wed Jul 29 2020 Wim Taymans <wtaymans@redhat.com> - 0.3.8-2
- Add patch for fix chrome audio hicups
- Add patch for infinite loop in device add/remove
- Disable LTO on armv7

* Tue Jul 28 2020 Wim Taymans <wtaymans@redhat.com> - 0.3.8-1
- Update to 0.3.8

* Tue Jul 21 2020 Wim Taymans <wtaymans@redhat.com> - 0.3.7-2
- Add patch to avoid crash when clearing metadata

* Tue Jul 21 2020 Wim Taymans <wtaymans@redhat.com> - 0.3.7-1
- Update to 0.3.7

* Wed Jun 10 2020 Wim Taymans <wtaymans@redhat.com> - 0.3.6-2
- Use systemd presets to enable pipewire.socket
- Remove duplicate hardened_build flags
- Add meson build again
- Fix -gstreamer subpackage Requires:

* Wed Jun 10 2020 Wim Taymans <wtaymans@redhat.com> - 0.3.6-1
- Update to 0.3.6
- Add new man pages
- Only build vulkan/pulse/jack in Fedora.

* Mon May 11 2020 Wim Taymans <wtaymans@redhat.com> - 0.3.5-1
- Update to 0.3.5

* Fri May 01 2020 Adam Williamson <awilliam@redhat.com> - 0.3.4-2
- Suppress library provides from pipewire-lib{pulse,jack}

* Thu Apr 30 2020 Wim Taymans <wtaymans@redhat.com> - 0.3.4-1
- Update to 0.3.4
- Add 2 more packages that replace libjack and libpulse

* Tue Mar 31 2020 Wim Taymans <wtaymans@redhat.com> - 0.3.2-3
- Add patch to unsubscribe unused sequencer ports
- Change config to only disable bluez5 handling by default.

* Mon Mar 30 2020 Wim Taymans <wtaymans@redhat.com> - 0.3.2-2
- Add config to disable alsa and bluez5 handling by default.

* Thu Mar 26 2020 Wim Taymans <wtaymans@redhat.com> - 0.3.2-1
- Update to 0.3.2

* Fri Mar 06 2020 Wim Taymans <wtaymans@redhat.com> - 0.3.1-1
- Update to 0.3.1

* Thu Feb 20 2020 Wim Taymans <wtaymans@redhat.com> - 0.3.0-1
- Update to 0.3.0
- Add libpulse-simple-pw.so

* Wed Feb 19 2020 Wim Taymans <wtaymans@redhat.com> - 0.2.97-1
- Update to 0.2.97
- Change download link

* Tue Feb 18 2020 Kalev Lember <klember@redhat.com> - 0.2.96-2
- Rename subpackages so that libjack-pw is in -libjack
  and libpulse-pw is in -libpulse
- Split libspa-jack.so out to -plugin-jack subpackage
- Avoid hard-requiring the daemon from any of the library subpackages

* Tue Feb 11 2020 Wim Taymans <wtaymans@redhat.com> - 0.2.96-1
- Update to 0.2.96
- Split -gstreamer package
- Enable aarch64 tests again

* Fri Feb 07 2020 Wim Taymans <wtaymans@redhat.com> - 0.2.95-1
- Update to 0.2.95
- Disable test on aarch64 for now

* Wed Feb 05 2020 Wim Taymans <wtaymans@redhat.com> - 0.2.94-1
- Update to 0.2.94
- Move pipewire modules to -libs
- Add pw-profiler
- Add libsndfile-devel as a BR

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.92-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Jan 28 2020 Wim Taymans <wtaymans@redhat.com> - 0.2.93-1
- Update to 0.2.93

* Wed Jan 15 2020 Wim Taymans <wtaymans@redhat.com> - 0.2.92-1
- Update to 0.2.92

* Wed Jan 15 2020 Wim Taymans <wtaymans@redhat.com> - 0.2.91-1
- Update to 0.2.91
- Add some more BR
- Fix some unit tests

* Mon Jan 13 2020 Wim Taymans <wtaymans@redhat.com> - 0.2.90-1
- Update to 0.2.90

* Thu Nov 28 2019 Kalev Lember <klember@redhat.com> - 0.2.7-2
- Move spa plugins to -libs subpackage

* Thu Sep 26 2019 Wim Taymans <wtaymans@redhat.com> - 0.2.7-1
- Update to 0.2.7

* Mon Sep 16 2019 Kalev Lember <klember@redhat.com> - 0.2.6-5
- Don't require the daemon package for -devel subpackage
- Move pipewire.conf man page to the daemon package

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Jun 19 2019 Wim Taymans <wtaymans@redhat.com> - 0.2.6-3
- Add patch to reuse fd in pipewiresrc
- Add patch for device provider
- Add patch to disable extra security checks until portal is fixed.

* Tue Jun 04 2019 Kalev Lember <klember@redhat.com> - 0.2.6-2
- Split libpipewire and the gstreamer plugin out to -libs subpackage

* Wed May 22 2019 Wim Taymans <wtaymans@redhat.com> - 0.2.6-1
- Update to 0.2.6
- Add patch for alsa-lib 1.1.9 include path

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jan 04 2019 Wim Taymans <wtaymans@redhat.com> - 0.2.5-2
- Add patch to avoid invalid conversion error with C++ compilers

* Thu Nov 22 2018 Wim Taymans <wtaymans@redhat.com> - 0.2.5-1
- Update to 0.2.5

* Thu Nov 22 2018 Wim Taymans <wtaymans@redhat.com> - 0.2.4-1
- Update to 0.2.4

* Thu Oct 18 2018 Wim Taymans <wtaymans@redhat.com> - 0.2.3-2
- Add systemd socket activation

* Thu Aug 30 2018 Wim Taymans <wtaymans@redhat.com> - 0.2.3-1
- Update to 0.2.3

* Tue Jul 31 2018 Wim Taymans <wtaymans@redhat.com> - 0.2.2-1
- Update to 0.2.2

* Fri Jul 20 2018 Wim Taymans <wtaymans@redhat.com> - 0.2.1-1
- Update to 0.2.1

* Tue Jul 17 2018 Wim Taymans <wtaymans@redhat.com> - 0.2.0-1
- Update to 0.2.0

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Feb 27 2018 Wim Taymans <wtaymans@redhat.com> - 0.1.9-1
- Update to 0.1.9

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Feb 03 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.1.8-2
- Switch to %%ldconfig_scriptlets

* Tue Jan 23 2018 Wim Taymans <wtaymans@redhat.com> - 0.1.8-1
- Update to 0.1.8

* Fri Nov 24 2017 Wim Taymans <wtaymans@redhat.com> - 0.1.7-1
- Update to 0.1.7
- Add to build when memfd_create is already defined

* Fri Nov 03 2017 Wim Taymans <wtaymans@redhat.com> - 0.1.6-1
- Update to 0.1.6

* Tue Sep 19 2017 Wim Taymans <wtaymans@redhat.com> - 0.1.5-2
- Add patch to avoid segfault when probing

* Tue Sep 19 2017 Wim Taymans <wtaymans@redhat.com> - 0.1.5-1
- Update to 0.1.5

* Thu Sep 14 2017 Kalev Lember <klember@redhat.com> - 0.1.4-3
- Rebuilt for GNOME 3.26.0 megaupdate

* Fri Sep 08 2017 Wim Taymans <wtaymans@redhat.com> - 0.1.4-2
- Install SPA hooks

* Wed Aug 23 2017 Wim Taymans <wtaymans@redhat.com> - 0.1.4-1
- Update to 0.1.4

* Wed Aug 09 2017 Wim Taymans <wtaymans@redhat.com> - 0.1.3-1
- Update to 0.1.3

* Tue Jul 04 2017 Wim Taymans <wtaymans@redhat.com> - 0.1.2-1
- Update to 0.1.2
- Added more build requirements
- Make separate doc package

* Mon Jun 26 2017 Wim Taymans <wtaymans@redhat.com> - 0.1.1-1
- Update to 0.1.1
- Add dbus-1 to BuildRequires
- change libs-devel to -devel

* Wed Sep 9 2015 Wim Taymans <wtaymans@redhat.com> - 0.1.0-2
- Fix BuildRequires to use pkgconfig, add all dependencies found in configure.ac
- Add user and groups  if needed
- Add license to %%licence

* Tue Sep 1 2015 Wim Taymans <wtaymans@redhat.com> - 0.1.0-1
- First version
