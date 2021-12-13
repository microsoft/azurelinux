Vendor:         Microsoft Corporation
Distribution:   Mariner
%global majorversion 0
%global minorversion 3
%global microversion 15

%global apiversion   0.3
%global spaversion   0.2

#global snap       20141103
#global gitrel     327
#global gitcommit  aec811798cd883a454b9b5cd82c77831906bbd2d
#global shortcommit %(c=%{gitcommit}; echo ${c:0:5})

# https://bugzilla.redhat.com/983606
%global _hardened_build 1

# where/how to apply multilib hacks
%global multilib_archs x86_64 %{ix86} ppc64 ppc s390x s390 sparc64 sparcv9 ppc64le

%global enable_alsa 1


%global enable_jack 1
%global enable_pulse 1
%global enable_vulkan 1


# libpulse and libjack subpackages shouldn't have library provides
# as the files they ship are not in the linker path. We also have
# to exclude requires or else the subpackages wind up requiring the
# libs they're no longer providing
# FIXME: the jack-audio-connection-kit and pulseaudio subpackages
# should get the auto-generated Provides: instead, but they do not,
# either with or without the lines below, not sure how to fix that
%global __provides_exclude_from ^%{_libdir}/pipewire-%{apiversion}/.*$
%global __requires_exclude_from ^%{_libdir}/pipewire-%{apiversion}/.*$

Name:           pipewire
Summary:        Media Sharing Server
Version:        %{majorversion}.%{minorversion}.%{microversion}
Release:        4%{?dist}
License:        MIT
URL:            https://pipewire.org/
%if 0%{?gitrel}
# git clone git://anongit.freedesktop.org/gstreamer/pipewire
# cd pipewire; git reset --hard %{gitcommit}; ./autogen.sh; make; make distcheck
Source0:        pipewire-%{version}-%{gitrel}-g%{shortcommit}.tar.gz
%else
Source0:	https://gitlab.freedesktop.org/pipewire/pipewire/-/archive/%{version}/pipewire-%{version}.tar.gz
%endif

## upstream patches
Patch0:         0001-protocol-native-do-version-check-on-HELLO.patch

## upstreamable patches

## fedora patches

BuildRequires:  meson >= 0.49.0
BuildRequires:  gcc
BuildRequires:  pkgconfig
BuildRequires:  pkgconfig(libudev)
BuildRequires:  pkgconfig(dbus-1)
BuildRequires:  pkgconfig(glib-2.0) >= 2.32
BuildRequires:  pkgconfig(gio-unix-2.0) >= 2.32
BuildRequires:  pkgconfig(gstreamer-1.0) >= 1.10.0
BuildRequires:  pkgconfig(gstreamer-base-1.0) >= 1.10.0
BuildRequires:  pkgconfig(gstreamer-plugins-base-1.0) >= 1.10.0
BuildRequires:  pkgconfig(gstreamer-net-1.0) >= 1.10.0
BuildRequires:  pkgconfig(gstreamer-allocators-1.0) >= 1.10.0
%if 0%{?enable_vulkan}
BuildRequires:  pkgconfig(vulkan)
%endif
BuildRequires:  pkgconfig(bluez)
BuildRequires:  systemd-devel >= 184
BuildRequires:  alsa-lib-devel
BuildRequires:  libv4l-devel
BuildRequires:  doxygen
BuildRequires:  xmltoman
BuildRequires:  graphviz
BuildRequires:  sbc-devel
BuildRequires:  libsndfile-devel

Requires(pre):  shadow-utils
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
Requires:       systemd >= 184
Requires:       rtkit

%description
PipeWire is a multimedia server for Linux and other Unix like operating
systems.

%package libs
Summary:        Libraries for PipeWire clients
License:        MIT
Recommends:     %{name}%{?_isa} = %{version}-%{release}

%description libs
This package contains the runtime libraries for any application that wishes
to interface with a PipeWire media server.

%package gstreamer
Summary:        GStreamer elements for PipeWire
License:        MIT
Recommends:     %{name}%{?_isa} = %{version}-%{release}
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}

%description gstreamer
This package contains GStreamer elements to interface with a
PipeWire media server.

%package devel
Summary:        Headers and libraries for PipeWire client development
License:        MIT
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
%description devel
Headers and libraries for developing applications that can communicate with
a PipeWire media server.

%package doc
Summary:        PipeWire media server documentation
License:        MIT

%description doc
This package contains documentation for the PipeWire media server.

%package utils
Summary:        PipeWire media server utilities
License:        MIT
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}

%description utils
This package contains command line utilities for the PipeWire media server.

%if 0%{?enable_alsa}
%package alsa
Summary:        PipeWire media server ALSA support
License:        MIT
Recommends:     %{name}%{?_isa} = %{version}-%{release}
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}

%description alsa
This package contains an ALSA plugin for the PipeWire media server.
%endif

%if 0%{?enable_jack}
%package libjack
Summary:        PipeWire libjack library
License:        MIT
Recommends:     %{name}%{?_isa} = %{version}-%{release}
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
BuildRequires:  jack-audio-connection-kit-devel >= 1.9.10
# Renamed in F32
Obsoletes:      pipewire-jack < 0.2.96-2

%description libjack
This package contains a PipeWire replacement for JACK audio connection kit
"libjack" library.

%package jack-audio-connection-kit
Summary:        PipeWire JACK implementation
License:        MIT
Recommends:     %{name}%{?_isa} = %{version}-%{release}
Requires:       %{name}-libjack%{?_isa} = %{version}-%{release}
BuildRequires:  jack-audio-connection-kit-devel >= 1.9.10
Conflicts:      jack-audio-connection-kit
Conflicts:      jack-audio-connection-kit-dbus
Provides:       jack-audio-connection-kit

%description jack-audio-connection-kit
This package provides a JACK implementation based on PipeWire

%package plugin-jack
Summary:        PipeWire media server JACK support
License:        MIT
BuildRequires:  jack-audio-connection-kit-devel
Recommends:     %{name}%{?_isa} = %{version}-%{release}
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
Requires:       jack-audio-connection-kit

%description plugin-jack
This package contains the PipeWire spa plugin to connect to a JACK server.
%endif

%if 0%{?enable_pulse}
%package libpulse
Summary:        PipeWire libpulse library
License:        MIT
Recommends:     %{name}%{?_isa} = %{version}-%{release}
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
BuildRequires:  pulseaudio-libs-devel
# Renamed in F32
Obsoletes:      pipewire-pulseaudio < 0.2.96-2

%description libpulse
This package contains a PipeWire replacement for PulseAudio "libpulse" library.

%package pulseaudio
Summary:        PipeWire PulseAudio implementation
License:        MIT
Recommends:     %{name}%{?_isa} = %{version}-%{release}
Requires:       %{name}-libpulse%{?_isa} = %{version}-%{release}
BuildRequires:  pulseaudio-libs-devel
Conflicts:      pulseaudio-libs
Conflicts:      pulseaudio-libs-glib2
Provides:       pulseaudio-libs
Provides:       pulseaudio-libs-glib2

%description pulseaudio
This package provides a PulseAudio implementation based on PipeWire
%endif

%prep
%setup -q -T -b0 -n %{name}-%{version}%{?gitrel:-%{gitrel}-g%{shortcommit}}

%patch0 -p1 -b .0000

%build
%meson \
    -D docs=true -D man=true -D gstreamer=true -D systemd=true 		\
    %{!?enable_jack:-D jack=false -D pipewire-jack=false} 		\
    %{!?enable_pulse:-D pipewire-pulseaudio=false}			\
    %{!?enable_alsa:-D pipewire-alsa=false}				\
    %{!?enable_vulkan:-D vulkan=false}
%meson_build

%install
%meson_install

%if 0%{?enable_jack}
ln -s pipewire-%{apiversion}/jack/libjack.so.0 %{buildroot}%{_libdir}/libjack.so.0.1.0
ln -s libjack.so.0.1.0 %{buildroot}%{_libdir}/libjack.so.0
ln -s pipewire-%{apiversion}/jack/libjackserver.so.0 %{buildroot}%{_libdir}/libjackserver.so.0.1.0
ln -s libjackserver.so.0.1.0 %{buildroot}%{_libdir}/libjackserver.so.0
ln -s pipewire-%{apiversion}/jack/libjacknet.so.0 %{buildroot}%{_libdir}/libjacknet.so.0.1.0
ln -s libjacknet.so.0.1.0 %{buildroot}%{_libdir}/libjacknet.so.0
%endif

%if 0%{?enable_pulse}
ln -s pipewire-%{apiversion}/pulse/libpulse.so.0 %{buildroot}%{_libdir}/libpulse.so.0
ln -s pipewire-%{apiversion}/pulse/libpulse-simple.so.0 %{buildroot}%{_libdir}/libpulse-simple.so.0
ln -s pipewire-%{apiversion}/pulse/libpulse-mainloop-glib.so.0 %{buildroot}%{_libdir}/libpulse-mainloop-glib.so.0
%endif

%if 0%{?enable_alsa}
mkdir -p %{buildroot}%{_sysconfdir}/alsa/conf.d/
cp %{buildroot}%{_datadir}/alsa/alsa.conf.d/50-pipewire.conf \
        %{buildroot}%{_sysconfdir}/alsa/conf.d/50-pipewire.conf
cp %{buildroot}%{_datadir}/alsa/alsa.conf.d/99-pipewire-default.conf \
        %{buildroot}%{_sysconfdir}/alsa/conf.d/99-pipewire-default.conf
%endif

# upstream should use udev.pc
mkdir -p %{buildroot}%{_prefix}/lib/udev/rules.d
mv -fv %{buildroot}/lib/udev/rules.d/90-pipewire-alsa.rules %{buildroot}%{_prefix}/lib/udev/rules.d


%check
%ifarch s390x
# FIXME: s390x FAIL: pw-test-stream, pw-test-endpoint
%global tests_nonfatal 1
%endif
%meson_test || TESTS_ERROR=$?
if [ "${TESTS_ERROR}" != "" ]; then
echo "test failed"
%{!?tests_nonfatal:exit $TESTS_ERROR}
fi

%pre
getent group pipewire >/dev/null || groupadd -r pipewire
getent passwd pipewire >/dev/null || \
    useradd -r -g pipewire -d %{_localstatedir}/run/pipewire -s /usr/sbin/nologin -c "PipeWire System Daemon" pipewire
exit 0

%post
%{?ldconfig}
%systemd_user_post pipewire.service
%systemd_user_post pipewire.socket

%ldconfig_postun

%triggerun -- %{name} < 0.3.6-2
# This is for upgrades from previous versions which had a static symlink.
# The %%post scriptlet above only does anything on initial package installation.
# Remove before F33.
systemctl --no-reload preset --global pipewire.socket >/dev/null 2>&1 || :

%files
%license LICENSE COPYING
%doc README.md
%{_userunitdir}/pipewire.*
%{_bindir}/pipewire
%{_bindir}/pipewire-media-session
%{_mandir}/man1/pipewire.1*
%dir %{_sysconfdir}/pipewire/
%config(noreplace) %{_sysconfdir}/pipewire/pipewire.conf
%{_mandir}/man5/pipewire.conf.5*

%files libs
%license LICENSE COPYING
%doc README.md
%{_libdir}/libpipewire-%{apiversion}.so.*
%{_libdir}/pipewire-%{apiversion}/libpipewire-*.so
%dir %{_datadir}/alsa-card-profile/
%dir %{_datadir}/alsa-card-profile/mixer/
%{_datadir}/alsa-card-profile/mixer/paths/
%{_datadir}/alsa-card-profile/mixer/profile-sets/
%{_prefix}/lib/udev/rules.d/90-pipewire-alsa.rules
%dir %{_libdir}/spa-%{spaversion}
%{_libdir}/spa-%{spaversion}/alsa/
%{_libdir}/spa-%{spaversion}/audioconvert/
%{_libdir}/spa-%{spaversion}/audiomixer/
%{_libdir}/spa-%{spaversion}/bluez5/
%{_libdir}/spa-%{spaversion}/control/
%{_libdir}/spa-%{spaversion}/support/
%{_libdir}/spa-%{spaversion}/v4l2/
%{_libdir}/spa-%{spaversion}/videoconvert/
%if 0%{?enable_vulkan}
%{_libdir}/spa-%{spaversion}/vulkan/
%endif

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
%{_bindir}/pw-mididump
%{_bindir}/pw-midiplay
%{_bindir}/pw-midirecord
%{_bindir}/pw-cli
%{_bindir}/pw-dot
%{_bindir}/pw-cat
%{_bindir}/pw-play
%{_bindir}/pw-profiler
%{_bindir}/pw-record
%{_bindir}/pw-reserve
%{_mandir}/man1/pw-mon.1*
%{_mandir}/man1/pw-cli.1*
%{_mandir}/man1/pw-cat.1*
%{_mandir}/man1/pw-dot.1*
%{_mandir}/man1/pw-metadata.1*
%{_mandir}/man1/pw-mididump.1*
%{_mandir}/man1/pw-profiler.1*

%{_bindir}/spa-acp-tool
%{_bindir}/spa-inspect
%{_bindir}/spa-monitor
%{_bindir}/spa-resample

%if 0%{?enable_alsa}
%files alsa
%{_libdir}/alsa-lib/libasound_module_pcm_pipewire.so
%{_libdir}/alsa-lib/libasound_module_ctl_pipewire.so
%{_datadir}/alsa/alsa.conf.d/50-pipewire.conf
%{_datadir}/alsa/alsa.conf.d/99-pipewire-default.conf
%config(noreplace) %{_sysconfdir}/alsa/conf.d/50-pipewire.conf
%config(noreplace) %{_sysconfdir}/alsa/conf.d/99-pipewire-default.conf
%endif

%if 0%{?enable_jack}
%files libjack
%{_libdir}/pipewire-%{apiversion}/jack/libjack.so*
%{_libdir}/pipewire-%{apiversion}/jack/libjacknet.so*
%{_libdir}/pipewire-%{apiversion}/jack/libjackserver.so*
%{_bindir}/pw-jack
%{_mandir}/man1/pw-jack.1*

%files jack-audio-connection-kit
%{_libdir}/libjack.so.*
%{_libdir}/libjackserver.so.*
%{_libdir}/libjacknet.so.*

%files plugin-jack
%{_libdir}/spa-%{spaversion}/jack/
%endif

%if 0%{?enable_pulse}
%files libpulse
%{_libdir}/pipewire-%{apiversion}/pulse/libpulse.so*
%{_libdir}/pipewire-%{apiversion}/pulse/libpulse-simple.so*
%{_libdir}/pipewire-%{apiversion}/pulse/libpulse-mainloop-glib.so*
%{_bindir}/pw-pulse
%{_mandir}/man1/pw-pulse.1*

%files pulseaudio
%{_libdir}/libpulse.so.0
%{_libdir}/libpulse-simple.so.0
%{_libdir}/libpulse-mainloop-glib.so.0
%endif

%changelog
* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.3.15-4
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Fri Apr 30 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.3.15-3
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Making binaries paths compatible with CBL-Mariner's paths.

* Wed Nov 4 2020 Wim Taymans <wtaymans@redhat.com> - 0.3.15-2
- Add patch to fix screen sharing for old clients

* Wed Nov 4 2020 Wim Taymans <wtaymans@redhat.com> - 0.3.15-1
- Update to 0.3.15

* Sun Nov 1 2020 Wim Taymans <wtaymans@redhat.com> - 0.3.14-2
- Add some pulse server patches

* Fri Oct 30 2020 Wim Taymans <wtaymans@redhat.com> - 0.3.14-1
- Update to 0.3.14

* Thu Oct 1 2020 Wim Taymans <wtaymans@redhat.com> - 0.3.13-3
- Add patches for some crasher bugs
- Fixes rhbz#1884177

* Tue Sep 29 2020 Wim Taymans <wtaymans@redhat.com> - 0.3.13-2
- Add patch to improve pulse compatibility

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

* Wed Jul 29 2020 Wim Taymans <wtaymans@redhat.com> - 0.3.8-2
- Add patch for fix chrome audio hicups
- Add patch for infinite loop in device add/remove

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
