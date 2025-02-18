%if 0%{?rhel}
%bcond_with avtp
%bcond_with jack
%bcond_with ffmpeg
%else
%bcond_without avtp
%bcond_without jack
%bcond_without ffmpeg
%endif

Name:           alsa-plugins
Version:        1.2.12
Release:        3%{?dist}
Summary:        The Advanced Linux Sound Architecture (ALSA) Plugins
# All packages are LGPL-2.1-or-later with the exception of samplerate
# which is GPL-2.0-or-later, pph plugin is BSD-3-Clause licensed
License:        GPL-2.0-or-later and LGPL-2.1-or-later and BSD-3-Clause
URL:            http://www.alsa-project.org/
Source0:        ftp://ftp.alsa-project.org/pub/plugins/%{name}-%{version}.tar.bz2
Patch0:         alsa-git.patch

BuildRequires:  autoconf automake libtool
BuildRequires:  make
BuildRequires:  alsa-lib-devel

%description
The Advanced Linux Sound Architecture (ALSA) provides audio and MIDI
functionality to the Linux operating system.

This package includes plugins for ALSA.

%if %{with jack}
%package jack
Recommends:     jack-audio-connection-kit
BuildRequires:  jack-audio-connection-kit-devel
Summary:        Jack PCM output plugin for ALSA
License:        LGPL-2.1-or-later

%description jack
This plugin converts the ALSA API over JACK (Jack Audio Connection
Kit, http://jackit.sf.net) API.  ALSA native applications can work
transparently together with jackd for both playback and capture.
This plugin provides the PCM type "jack"
%endif

%package oss
Summary:        Oss PCM output plugin for ALSA
License:        LGPL-2.1-or-later

%description oss
This plugin converts the ALSA API over OSS API.  With this plugin,
ALSA native apps can run on OSS drivers.

This plugin provides the PCM type "oss".

%package pulseaudio
Recommends:     pulseaudio-daemon
BuildRequires:  pulseaudio-libs-devel
Summary:        Alsa to PulseAudio backend
License:        LGPL-2.1-or-later

%description pulseaudio
This plugin allows any program that uses the ALSA API to access a PulseAudio
sound daemon. In other words, native ALSA applications can play and record
sound across a network. There are two plugins in the suite, one for PCM and
one for mixer control.

%package samplerate
BuildRequires:  libsamplerate-devel
Summary:        External rate converter plugin for ALSA
License:        GPL-2.0-or-later

%description samplerate
This plugin is an external rate converter using libsamplerate by Erik de
Castro Lopo.

%package upmix
BuildRequires:  libsamplerate-devel
Summary:        Upmixer channel expander plugin for ALSA
License:        LGPL-2.1-or-later

%description upmix
The upmix plugin is an easy-to-use plugin for upmixing to 4 or
6-channel stream.  The number of channels to be expanded is determined
by the slave PCM or explicitly via channel option.

%package vdownmix
BuildRequires:  libsamplerate-devel
Summary:        Downmixer to stereo plugin for ALSA
License:        LGPL-2.1-or-later

%description vdownmix
The vdownmix plugin is a downmixer from 4-6 channels to 2-channel
stereo headphone output.  This plugin processes the input signals with
a simple spacialization, so the output sounds like a kind of "virtual
surround".

%package usbstream
Summary:        USB stream plugin for ALSA
License:        LGPL-2.1-or-later

%description usbstream
The usbstream plugin is for snd-usb-us122l driver. It converts PCM
stream to USB specific stream.

%package arcamav
Summary:        Arcam AV amplifier plugin for ALSA
License:        LGPL-2.1-or-later

%description arcamav
This plugin exposes the controls for an Arcam AV amplifier
(see: http://www.arcam.co.uk/) as an ALSA mixer device.

%package speex
Requires:       speex speexdsp
BuildRequires:  speex-devel speexdsp-devel
Summary:        Rate Converter Plugin Using Speex Resampler
License:        LGPL-2.1-or-later

%description speex
The rate plugin is an external rate converter using the Speex resampler
(aka Public Parrot Hack) by Jean-Marc Valin. The pcm plugin provides
pre-processing of a mono stream like denoise using libspeex DSP API.

%package maemo
BuildRequires:  dbus-devel
Summary:        Maemo plugin for ALSA
License:        LGPL-2.1-or-later

%description maemo
This plugin converts the ALSA API over PCM task nodes protocol. In this way,
ALSA native applications can run over DSP Gateway and use DSP PCM task nodes.

%if %{with avtp}
%package avtp
BuildRequires:  libavtp-devel
Summary:        Audio Video Transport Protocol (AVTP) plugin for ALSA
License:        LGPL-2.1-or-later

%description avtp
This plugin supports Audio Video Transport Protocol (AVTP) as specified in
IEEE 1722-2016 spec. AVTP is part of the Audio/Video Broadcast using TSN.
%endif

%if %{with ffmpeg}
%package a52
BuildRequires:  ffmpeg-free-devel
Obsoletes:      alsa-plugins-freeworld-a52 <= %{version}-%{release}
Summary:        A52 output plugin for ALSA using libavcodec
License:        LGPL-2.1-or-later

%description a52
This plugin converts S16 linear format to A52 compressed stream and
send to an SPDIF output.  It requires libavcodec for encoding the
audio stream.

%package lavrate
BuildRequires:  ffmpeg-free-devel
Obsoletes:      alsa-plugins-freeworld-lavrate <= %{version}-%{release}
Summary:        Rate converter plugin for ALSA using libavcodec
License:        LGPL-2.1-or-later

%description lavrate
The plugin uses ffmpeg audio resample library to convert audio rates.
%endif

%prep
%autosetup -n %{name}-%{version}%{?prever} -p1

%build
autoreconf -vif
%configure --disable-static \
           --with-speex=lib \
           --enable-maemo-plugin \
           --enable-maemo-resource-manager
%make_build

%install
%make_install

mv %{buildroot}%{_sysconfdir}/alsa/conf.d/99-pulseaudio-default.conf.example \
        %{buildroot}%{_sysconfdir}/alsa/conf.d/99-pulseaudio-default.conf

find %{buildroot} -name "*.la" -delete


%if %{with jack}
%files jack
%license COPYING COPYING.GPL
%doc doc/README-jack
%dir %{_sysconfdir}/alsa
%dir %{_sysconfdir}/alsa/conf.d
%config(noreplace) %{_sysconfdir}/alsa/conf.d/50-jack.conf
%dir %{_datadir}/alsa/alsa.conf.d
%{_datadir}/alsa/alsa.conf.d/50-jack.conf
%dir %{_libdir}/alsa-lib
%{_libdir}/alsa-lib/libasound_module_pcm_jack.so
%endif

%files oss
%license COPYING COPYING.GPL
%doc doc/README-pcm-oss
%dir %{_sysconfdir}/alsa
%dir %{_sysconfdir}/alsa/conf.d
%config(noreplace) %{_sysconfdir}/alsa/conf.d/50-oss.conf
%dir %{_datadir}/alsa/alsa.conf.d
%{_datadir}/alsa/alsa.conf.d/50-oss.conf
%dir %{_libdir}/alsa-lib
%{_libdir}/alsa-lib/libasound_module_ctl_oss.so
%{_libdir}/alsa-lib/libasound_module_pcm_oss.so

%files pulseaudio
%license COPYING COPYING.GPL
%doc doc/README-pulse
%dir %{_libdir}/alsa-lib
%{_libdir}/alsa-lib/libasound_module_pcm_pulse.so
%{_libdir}/alsa-lib/libasound_module_ctl_pulse.so
%{_libdir}/alsa-lib/libasound_module_conf_pulse.so
%dir %{_sysconfdir}/alsa
%dir %{_sysconfdir}/alsa/conf.d
%config(noreplace) %{_sysconfdir}/alsa/conf.d/50-pulseaudio.conf
%config(noreplace) %{_sysconfdir}/alsa/conf.d/99-pulseaudio-default.conf
%dir %{_datadir}/alsa/alsa.conf.d
%{_datadir}/alsa/alsa.conf.d/50-pulseaudio.conf

%files samplerate
%license COPYING COPYING.GPL
%doc doc/samplerate.txt
%dir %{_sysconfdir}/alsa
%dir %{_sysconfdir}/alsa/conf.d
%config(noreplace) %{_sysconfdir}/alsa/conf.d/10-samplerate.conf
%dir %{_datadir}/alsa/alsa.conf.d
%{_datadir}/alsa/alsa.conf.d/10-samplerate.conf
%dir %{_libdir}/alsa-lib
%{_libdir}/alsa-lib/libasound_module_rate_samplerate.so
%{_libdir}/alsa-lib/libasound_module_rate_samplerate_best.so
%{_libdir}/alsa-lib/libasound_module_rate_samplerate_linear.so
%{_libdir}/alsa-lib/libasound_module_rate_samplerate_medium.so
%{_libdir}/alsa-lib/libasound_module_rate_samplerate_order.so

%files upmix
%license COPYING COPYING.GPL
%doc doc/upmix.txt
%dir %{_sysconfdir}/alsa
%dir %{_sysconfdir}/alsa/conf.d
%config(noreplace) %{_sysconfdir}/alsa/conf.d/60-upmix.conf
%dir %{_datadir}/alsa/alsa.conf.d
%{_datadir}/alsa/alsa.conf.d/60-upmix.conf
%dir %{_libdir}/alsa-lib
%{_libdir}/alsa-lib/libasound_module_pcm_upmix.so

%files vdownmix
%license COPYING COPYING.GPL
%doc doc/vdownmix.txt
%dir %{_sysconfdir}/alsa
%dir %{_sysconfdir}/alsa/conf.d
%config(noreplace) %{_sysconfdir}/alsa/conf.d/60-vdownmix.conf
%dir %{_datadir}/alsa/alsa.conf.d
%{_datadir}/alsa/alsa.conf.d/60-vdownmix.conf
%dir %{_libdir}/alsa-lib
%{_libdir}/alsa-lib/libasound_module_pcm_vdownmix.so

%files usbstream
%license COPYING COPYING.GPL
%dir %{_sysconfdir}/alsa
%dir %{_sysconfdir}/alsa/conf.d
%config(noreplace) %{_sysconfdir}/alsa/conf.d/98-usb-stream.conf
%dir %{_datadir}/alsa/alsa.conf.d
%{_datadir}/alsa/alsa.conf.d/98-usb-stream.conf
%dir %{_libdir}/alsa-lib
%{_libdir}/alsa-lib/libasound_module_pcm_usb_stream.so

%files arcamav
%license COPYING COPYING.GPL
%doc doc/README-arcam-av
%dir %{_sysconfdir}/alsa
%dir %{_sysconfdir}/alsa/conf.d
%config(noreplace) %{_sysconfdir}/alsa/conf.d/50-arcam-av-ctl.conf
%dir %{_datadir}/alsa/alsa.conf.d
%{_datadir}/alsa/alsa.conf.d/50-arcam-av-ctl.conf
%dir %{_libdir}/alsa-lib
%{_libdir}/alsa-lib/libasound_module_ctl_arcam_av.so

%files speex
%license COPYING COPYING.GPL
%doc doc/speexdsp.txt doc/speexrate.txt
%dir %{_sysconfdir}/alsa
%dir %{_sysconfdir}/alsa/conf.d
%config(noreplace) %{_sysconfdir}/alsa/conf.d/10-speexrate.conf
%config(noreplace) %{_sysconfdir}/alsa/conf.d/60-speex.conf
%dir %{_datadir}/alsa/alsa.conf.d
%{_datadir}/alsa/alsa.conf.d/10-speexrate.conf
%{_datadir}/alsa/alsa.conf.d/60-speex.conf
%dir %{_libdir}/alsa-lib
%{_libdir}/alsa-lib/libasound_module_pcm_speex.so
%{_libdir}/alsa-lib/libasound_module_rate_speexrate.so
%{_libdir}/alsa-lib/libasound_module_rate_speexrate_best.so
%{_libdir}/alsa-lib/libasound_module_rate_speexrate_medium.so

%files maemo
%license COPYING COPYING.GPL
%doc doc/README-maemo
%dir %{_sysconfdir}/alsa
%dir %{_sysconfdir}/alsa/conf.d
%config(noreplace) %{_sysconfdir}/alsa/conf.d/98-maemo.conf
%dir %{_datadir}/alsa/alsa.conf.d
%{_datadir}/alsa/alsa.conf.d/98-maemo.conf
%dir %{_libdir}/alsa-lib
%{_libdir}/alsa-lib/libasound_module_ctl_dsp_ctl.so
%{_libdir}/alsa-lib/libasound_module_pcm_alsa_dsp.so

%if %{with avtp}
%files avtp
%license COPYING COPYING.GPL
%{_libdir}/alsa-lib/libasound_module_pcm_aaf.so
%endif

%if %{with ffmpeg}
%files a52
%license COPYING COPYING.GPL
%doc doc/a52.txt
%dir %{_sysconfdir}/alsa
%dir %{_sysconfdir}/alsa/conf.d
%config(noreplace) %{_sysconfdir}/alsa/conf.d/60-a52-encoder.conf
%dir %{_datadir}/alsa/alsa.conf.d
%{_datadir}/alsa/alsa.conf.d/60-a52-encoder.conf
%dir %{_libdir}/alsa-lib
%{_libdir}/alsa-lib/libasound_module_pcm_a52.so

%files lavrate
%license COPYING COPYING.GPL
%doc doc/lavrate.txt
%dir %{_sysconfdir}/alsa
%dir %{_sysconfdir}/alsa/conf.d
%config(noreplace) %{_sysconfdir}/alsa/conf.d/10-rate-lav.conf
%dir %{_datadir}/alsa/alsa.conf.d
%{_datadir}/alsa/alsa.conf.d/10-rate-lav.conf
%dir %{_libdir}/alsa-lib
%{_libdir}/alsa-lib/libasound_module_rate_lavrate.so
%{_libdir}/alsa-lib/libasound_module_rate_lavrate_fast.so
%{_libdir}/alsa-lib/libasound_module_rate_lavrate_faster.so
%{_libdir}/alsa-lib/libasound_module_rate_lavrate_high.so
%{_libdir}/alsa-lib/libasound_module_rate_lavrate_higher.so
%endif

%changelog
* Mon Sep 23 2024 Fabio Valentini <decathorpe@gmail.com> - 1.2.12-3
- Rebuild for ffmpeg 7

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Jun 11 2024 Jaroslav Kysela <perex@perex.cz> - 1.2.12-1
- Updated to 1.2.12

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.7.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.7.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Aug 25 2023 Yaakov Selkowitz <yselkowi@redhat.com> - 1.2.7.1-8
- Disable avtp plugin in RHEL builds

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.7.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun  6 2023 Jaroslav Kysela <perex@perex.cz> - 1.2.7.1-6
- change to SPDX licenses

* Sun Mar 12 2023 Neal Gompa <ngompa@fedoraproject.org> - 1.2.7.1-5
- Rebuild for ffmpeg 6.0

* Mon Mar  6 2023 Jaroslav Kysela <perex@perex.cz> - 1.2.7.1-4
- Enable avtp plugin - Peter Robinson <pbrobinson@fedoraproject.org>
- Enable a52 and lavrate plugins - Yaakov Selkowitz <yselkowi@redhat.com>
- Remove or soften excess dependendencies - Yaakov Selkowitz <yselkowi@redhat.com>
- CI test & RHEL cleanups

* Wed Jan 18 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.7.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.7.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jun 17 2022 Jaroslav Kysela <perex@perex.cz> - 1.2.7.1-1
- Updated to 1.2.7.1

* Wed Jan 19 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Dec  6 2021 Jaroslav Kysela <perex@perex.cz> - 1.2.6-1
- Updated to 1.2.6

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sun May 30 2021 Jaroslav Kysela <perex@perex.cz> - 1.2.5-1
- Updated to 1.2.5
- Modernize the spec file (Neal Gompa)

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jan 04 2021 Rex Dieter <rdieter@fedoraproject.org> - 1.2.2-4
- -pulseaudio: Requires: pulseaudio-daemon

* Fri Jul 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.2-3
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Feb 19 2020 Jaroslav Kysela <perex@perex.cz> - 1.2.2-1
- Updated to 1.2.2

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Nov 13 2019 Jaroslav Kysela <perex@perex.cz> - 1.2.1-1
- Updated to 1.2.1

* Tue Aug 20 2019 Gwyn Ciesla <gwync@protonmail.com> - 1.1.9-3
- macroize %%{_sysconfdir}.

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 10 2019 Jaroslav Kysela <perex@perex.cz> - 1.1.9-1
- Updated to 1.1.9

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jan  7 2019 Jaroslav Kysela <perex@perex.cz> - 1.1.8-1
- Updated to 1.1.8

* Wed Oct 24 2018 Jaroslav Kysela <perex@perex.cz> - 1.1.7-2
- Updated to 1.1.7

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Apr 16 2018 Jaroslav Kysela <perex@perex.cz> - 1.1.6-3
- /etc/alsa/conf.d contains symlinks to /usr/share/alsa/alsa.conf.d templates

* Wed Apr 04 2018 Jaroslav Kysela <perex@perex.cz> - 1.1.6-2
- Changed the add-on config directory to /etc/alsa/conf.d
- Changed the config files

* Tue Apr 03 2018 Jaroslav Kysela <perex@perex.cz> - 1.1.6-1
- Updated to 1.1.6

* Sun Feb 25 2018 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.1.5-3
- Let plugin packages own %%{_libdir}/alsa-lib (RHBZ#1548865)

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Nov 14 2017 Jaroslav Kysela <perex@perex.cz> - 1.1.5-1
- Updated to 1.1.5

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue May 16 2017 Jaroslav Kysela <perex@perex.cz> - 1.1.4-1
- Updated to 1.1.4

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Mar 31 2016 Jaroslav Kysela <perex@perex.cz> - 1.1.1-1
- Updated to 1.1.1

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Oct 27 2015 Jaroslav Kysela <perex@perex.cz> - 1.1.0-1
- Updated to 1.1.0

* Tue Jun 16 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.29-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Feb 26 2015 Jaroslav Kysela <perex@perex.cz> - 1.0.29-1
- Updated to 1.0.29

* Thu Jan 29 2015 Peter Robinson <pbrobinson@fedoraproject.org> 1.0.28-4
- Add speexdsp-devel as a dep to fix FTBFS

* Fri Aug 15 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.28-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Thu Jul 24 2014 Peter Robinson <pbrobinson@fedoraproject.org> 1.0.28-2
- Fix Source1 conditional for src.rpm generation (RHBZ 856543)

* Thu Jul 24 2014 Peter Robinson <pbrobinson@fedoraproject.org> 1.0.28-1
- Update to 1.0.28

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.27-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.27-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Apr 12 2013 Jaroslav Kysela <jkysela@redhat.com> - 1.0.27-1
- Updated to 1.0.27

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.26-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Sep  6 2012 Jaroslav Kysela <jkysela@redhat.com> - 1.0.26-2
- Changed dependency on pulseaudio-lib-devel to pulseaudio-libs-devel

* Thu Sep  6 2012 Jaroslav Kysela <jkysela@redhat.com> - 1.0.26-1
- Updated to 1.0.26

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.25-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Apr 23 2012 Paul Howarth <paul@city-fan.org> - 1.0.25-3
- Bump and rebuild to maintain upgrade path (#806218)

* Wed Feb  1 2012 Jaroslav Kysela <jkysela@redhat.com> - 1.0.25-1
- Updated to 1.0.25
- Moved plugin specific configuration from /etc/alsa/pcm to /usr/share/alsa/alsa.conf.d

* Thu Jan 19 2012 Nikola Pajkovsky <npajkovs@redhat.com> - 1.0.24-4
- 761244 - please disable JACK for RHEL

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.24-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.24-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jan 28 2011 Jaroslav Kysela <jkysela@redhat.com> - 1.0.24-1
- Updated to 1.0.24

* Thu Jan 14 2010 Jaroslav Kysela <jkysela@redhat.com> - 1.0.22-1
- Updated to 1.0.22

* Mon Sep 7 2009 Eric Moret <eric.moret@gmail.com> - 1.0.21-2
- Added missing dbus-devel dependency to maemo subpackage

* Mon Sep 7 2009 Eric Moret <eric.moret@gmail.com> - 1.0.21-1
- Updated to 1.0.21
- Patch clean up
- Added maemo subpackage

* Tue Aug 4 2009 Lennart Poettering <lpoetter@redhat.com> - 1.0.20-5
- Add a couple of more clean up patches for the pulse plugin

* Fri Jul 31 2009 Lennart Poettering <lpoetter@redhat.com> - 1.0.20-4
- Add a couple of clean up patches for the pulse plugin

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.20-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jun 24 2009 Eric Moret <eric.moret@gmail.com> - 1.0.20-2
- Added speex subpackage
- Removed ascii-art from jack's plugin description

* Fri May 8 2009 Eric Moret <eric.moret@gmail.com> - 1.0.20-1
- Updated to 1.0.20
- Added arcam-av subpackage

* Fri Apr 24 2009 Eric Moret <eric.moret@gmail.com> - 1.0.19-1
- Updated to 1.0.19
- Added Requires: alsa-utils to address #483322
- Added dir {_sysconfdir}/alsa/pcm to address #483322

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.18-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Dec 28 2008 Eric Moret <eric.moret@gmail.com> - 1.0.18-2
- Updated to 1.0.18 final

* Thu Sep 11 2008 Jaroslav Kysela <jkysela@redhat.com> - 1.0.18-1.rc3
- Updated to 1.0.18rc3
- Added usbstream subpackage

* Mon Jul 21 2008 Jaroslav Kysela <jkysela@redhat.com> - 1.0.17-1
- Updated to 1.0.17

* Tue Mar 25 2008 Lubomir Kundrak <lkundrak@redhat.com> - 1.0.16-4
- Kind of fix the plugins not to complain about the hints

* Wed Mar 19 2008 Eric Moret <eric.moret@gmail.com> - 1.0.16-3
- Fixing jack.conf (#435343)

* Sun Mar 09 2008 Lubomir Kundrak <lkundrak@redhat.com> - 1.0.16-2
- Add descriptions to various PCM plugins, so they're visible in aplay -L

* Sat Mar 08 2008 Lubomir Kundrak <lkundrak@redhat.com> - 1.0.16-1
- New upstream, dropping upstreamed patches
- Do not assert fail when pulseaudio is unavailable (#435148)

* Tue Mar 04 2008 Lubomir Kundrak <lkundrak@redhat.com> - 1.0.15-4
- Be more heplful when there's PulseAudio trouble.
- This may save us some bogus bug reports

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.0.15-3
- Autorebuild for GCC 4.3

* Fri Jan 18 2008 Eric Moret <eric.moret@epita.fr> - 1.0.15-2
- Update to upstream 1.0.15 (#429249)
- Add "Requires: pulseaudio" to alsa-plugins-pulseaudio (#368891)
- Fix pulse_hw_params() when state is SND_PCM_STATE_PREPARED (#428030)
- run /sbin/ldconfig on post and postun macros

* Thu Oct 18 2007 Lennart Poettering <lpoetter@redhat.com> - 1.0.14-6
- Merge the whole /etc/alsa/pcm/pulseaudio.conf stuff into
  /etc/alsa/pulse-default.conf, because the former is practically
  always ignored, since it is not referenced for inclusion by any other
  configuration file fragment (#251943)
  The other fragments installed in /etc/alsa/pcm/ are useless, too. But
  since we are in a freeze and they are not that important, I am not fixing
  this now.

* Wed Oct 17 2007 Lennart Poettering <lpoetter@redhat.com> - 1.0.14-5
- Split pulse.conf into two, so that we can load one part from
  form /etc/alsa/alsa.conf. (#251943)

* Mon Oct 1 2007 Lennart Poettering <lpoetter@redhat.com> - 1.0.14-4
- In the pulse plugin: reflect the XRUN state back to the application.
  Makes XMMS work on top of the alsa plugin. (#307341)

* Mon Sep 24 2007 Lennart Poettering <lpoetter@redhat.com> - 1.0.14-3
- Change PulseAudio buffering defaults to more sane values

* Tue Aug 14 2007 Eric Moret <eric.moret@epita.fr> - 1.0.14-2
- Adding pulse as ALSA "default" pcm and ctl when the alsa-plugins-pulseaudio
package is installed, fixing #251943.

* Mon Jul 23 2007 Eric Moret <eric.moret@epita.fr> - 1.0.14-1
- update to upstream 1.0.14
- use configure --without-speex instead of patches to remove a52

* Tue Mar 13 2007 Matej Cepl <mcepl@redhat.com> - 1.0.14-0.3.rc2
- Really remove a52 plugin package (including changes in
  configure and configure.in)

* Thu Feb 15 2007 Eric Moret <eric.moret@epita.fr> 1.0.14-0.2.rc2
- Adding configuration files
- Removing a52 plugin package

* Wed Jan 10 2007 Eric Moret <eric.moret@epita.fr> 1.0.14-0.1.rc2
- Initial package for Fedora
