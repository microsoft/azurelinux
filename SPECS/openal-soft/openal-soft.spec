## START: Set by rpmautospec
## (rpmautospec version 0.8.4)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 5;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           openal-soft
Version:        1.24.2
Release:        %autorelease
Summary:        Software implementation of the OpenAL 3D audio API

# LGPL-2.0-or-later: Main library
# BSD-3-Clause:
#  - alc/effects/compressor.cpp
#  - alc/effects/vmorpher.cpp
# CC-BY-NC-SA-3.0 : -> NOT FREE
#  - utils/SCUT_KEMAR.def
# GPL-2.0-or-later:
#  - utils/sofa-info.cpp
#  - utils/sofa-support.cpp
#  - utils/makemhr/loaddef.cpp
#  - utils/makemhr/loadsofa.cpp
#  - utils/makemhr/makemhr.cpp
# Apache-2.0:
#  - alc/backends/opensl.cpp
# (LGPL-2.0-or-later AND BSD-3-Clause):
#  - alc/alu.cpp
# NCL:
#  - common/pffft.cpp
#  - common/pffft.h
# MIT:
#  - common/filesystem.cpp
#  - common/filesystem.h
#  - common/ghc_filesystem.h
#  - core/bs2b.cpp
#  - core/bs2b.h
#  - core/rtkit.cpp
#  - core/rtkit.h
#  - examples/
#  - utils/openal-info.c
#  - utils/uhjdecoder.cpp
#  - utils/uhjencoder.cpp
#  - support/docopt.py
#  - support/printable.py
# LicenseRef-Fedora-Public-Domain
#  - core/cubic_tables.cpp
# source of claim:
# These gaussian filter tables are inspired by the gaussian-like filter found
# in the SNES. This is based on the public domain code developed by Near, with
# the help of Ryphecha and nocash, from the nesdev.org forums.
# 
# https://forums.nesdev.org/viewtopic.php?p=251534#p251534>
# Archival:
#  - https://archive.is/wViJG
#  - https://web.archive.org/web/20250130174430/https://forums.nesdev.org/viewtopic.php?p=251534#p251534
# Open license review regarding datasets:
# https://gitlab.com/fedora/legal/fedora-license-data/-/issues/629
License:        LGPL-2.0-or-later AND BSD-3-Clause AND GPL-2.0-or-later AND Apache-2.0 AND (LGPL-2.0-or-later AND BSD-3-Clause) AND (MIT WITH fmt-exception) AND NCL AND MIT AND LicenseRef-Fedora-Public-Domain
URL:            https://openal-soft.org/
VCS:            https://github.com/kcat/openal-soft
# Source without non free datasets
# Run ./make_tarball.sh
# Then don't forget to upload it with:
# fedpkg new-sources *.tar.xz
Source:         openal-soft-1.24.2-clean.tar.xz
Source:         make_tarball.sh
# Patch to unbundle fmt
Patch:          0001-Unbundle-fmt.diff

# Implicit dependencies for the unbundling script: curl, rpm-build, tar.
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  ninja-build
BuildRequires:  pkgconfig(alsa)
BuildRequires:  pkgconfig(fmt)
BuildRequires:  pkgconfig(jack)
BuildRequires:  pkgconfig(libavcodec)
BuildRequires:  pkgconfig(libpulse)
BuildRequires:  pkgconfig(sdl2)
BuildRequires:  pkgconfig(sndfile)
%if 0%{?fedora}
BuildRequires:  pkgconfig(libavcodec)
BuildRequires:  pkgconfig(libmysofa)
BuildRequires:  pkgconfig(portaudio-2.0)
%endif
%if 0%{?fedora} || 0%{?rhel} >= 9
BuildRequires:  pkgconfig(libpipewire-0.3)
%endif
%if 0%{?fedora} || 0%{?rhel} <= 9
BuildRequires:  pkgconfig(Qt5Widgets)
%endif

%description
OpenAL Soft is an LGPL-licensed, cross-platform, software implementation of the 
OpenAL 3D audio API. It's forked from the open-sourced Windows version available 
originally from openal.org's SVN repository (now defunct). OpenAL provides 
capabilities for playing audio in a virtual 3D environment. Distance 
attenuation, doppler shift, and directional sound emitters are among the 
features handled by the API. More advanced effects, including air absorption, 
occlusion, and environmental reverb, are available through the EFX extension. It 
also facilitates streaming audio, multi-channel buffers, and audio capture.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description    devel 
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package        examples
Summary:        Sample applications for OpenAl Soft
Requires:       %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description	examples
Sample applications for OpenAl Soft.

%if 0%{?fedora} || 0%{?rhel} <= 9
%package        qt
Summary:        Qt frontend for configuring OpenAL Soft
Requires:       %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description    qt
The %{name}-qt package contains alsoft-config, a Qt-based tool
for configuring OpenAL features.
%endif

%prep
%autosetup -p1

%build
%cmake -G Ninja \
    -DCMAKE_BUILD_TYPE=Release \
    -DALSOFT_CPUEXT_NEON:BOOL=OFF \
    -DALSOFT_EXAMPLES:BOOL=ON \
    -DALSOFT_UTILS:BOOL=ON \
    -DALSOFT_INSTALL_CONFIG:BOOL=ON \
    -DALSOFT_INSTALL_EXAMPLES:BOOL=ON \
    -DALSOFT_INSTALL_HRTF_DATA:BOOL=ON \
    -DALSOFT_INSTALL_UTILS:BOOL=ON
%cmake_build

%install
%cmake_install

install -Dpm644 alsoftrc.sample %{buildroot}%{_sysconfdir}/openal/alsoft.conf
# Don't pin the pulseaudio stream to a specific output device
sed -i 's/#allow-moves = false/allow-moves = true/' \
  %{buildroot}%{_sysconfdir}/openal/alsoft.conf

%files
%license BSD-3Clause COPYING LICENSE-pffft
%doc README.md ChangeLog
%dir %{_sysconfdir}/openal
%config(noreplace) %{_sysconfdir}/openal/alsoft.conf
%{_bindir}/openal-info
%{_datadir}/openal
%exclude %{_datadir}/openal/alsoftrc.sample
%exclude %{_datadir}/openal/presets/presets.txt
%{_libdir}/libopenal.so.1*

%files devel
%if 0%{?fedora}
%{_bindir}/makemhr
%endif
%{_includedir}/AL
%{_libdir}/cmake/OpenAL
%{_libdir}/libopenal.so
%{_libdir}/pkgconfig/openal.pc

%files examples
%{_bindir}/aldebug
%{_bindir}/aldirect
%{_bindir}/alhrtf
%{_bindir}/allafplay
%{_bindir}/allatency
%{_bindir}/almultireverb
%{_bindir}/alplay
%{_bindir}/alrecord
%{_bindir}/alreverb
%{_bindir}/alstream
%{_bindir}/altonegen

%if 0%{?fedora} || 0%{?rhel} <= 9
%files qt
%{_bindir}/alsoft-config
%endif

%changelog
## START: Generated by rpmautospec
* Mon Apr 06 2026 azldev <> - 1.24.2-5
- Latest state for openal-soft

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.24.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sun Feb 02 2025 Miroslav Suchý <msuchy@redhat.com> - 1.24.2-3
- Correct SPDX license

* Sat Feb 01 2025 Robert-André Mauchin <zebob.m@gmail.com> - 1.24.2-2
- Fix script and upload correct archive

* Sat Feb 01 2025 Robert-André Mauchin <zebob.m@gmail.com> - 1.24.2-1
- Update to 1.24.2
- License reanalysis
- Remove bundled fmt
- Remove unneeded dependencies (fluidsynth)
- Remove proprietary parts
- Use pkgconfig for library dependencies
- Cleanup

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.23.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.23.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.23.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.23.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Aug 16 2023 Yaakov Selkowitz <yselkowi@redhat.com> - 1.23.1-3
- Drop libmysofa and qt5 from RHEL builds

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.23.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Apr 12 2023 Vitaly Zaitsev <vitaly@easycoding.org> - 1.23.1-1
- Updated to version 1.23.1.

* Mon Feb 06 2023 Vitaly Zaitsev <vitaly@easycoding.org> - 1.23.0-1
- Updated to version 1.23.0.

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.22.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sun Dec 18 2022 Vitaly Zaitsev <vitaly@easycoding.org> - 1.22.2-6
- Fixed examples build on RHEL and ELN.

* Sun Dec 18 2022 Vitaly Zaitsev <vitaly@easycoding.org> - 1.22.2-5
- Enabled PipeWire native backend also on RHEL 9+.

* Sun Dec 18 2022 Vitaly Zaitsev <vitaly@easycoding.org> - 1.22.2-4
- Enabled PipeWire native backend on Fedora.
- Switched to SPDX.

* Fri Sep 30 2022 Troy Dawson <tdawson@redhat.com> - 1.22.2-3
- Fix ELN build failures

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.22.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue Jun 28 2022 Vitaly Zaitsev <vitaly@easycoding.org> - 1.22.2-1
- Updated to version 1.22.2.

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.21.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Sep 06 2021 Vitaly Zaitsev <vitaly@easycoding.org> - 1.21.1-1
- Updated to version 1.21.1.

* Wed Aug 04 2021 Wim Taymans <wtaymans@redhat.com> - 1.19.1-15
- Don't package some examples when SDL_sound is disabled

* Mon Aug 02 2021 Wim Taymans <wtaymans@redhat.com> - 1.19.1-14
- Only build SDL_sound support on Fedora and rhel < 9

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.19.1-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.19.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Jan 21 2021 Wim Taymans <wtaymans@redhat.com> - 1.19.1-11
- Only build fluidsynth support on Fedora

* Wed Jan 20 2021 Hans de Goede <hdegoede@redhat.com> - 1.19.1-10
- Only build portaudio-backend on Fedora

* Tue Aug 04 2020 François Cami <fcami@fedoraproject.org> - 1.19.1-9
- Fix FTBFS (rhbz#1865148)
- Set __cmake_in_source_build
- BR qt5-qtbase-devel to keep the GUI frontend

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.19.1-8
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.19.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sat Jul 18 2020 Jeff Law <law@redhat.com> - 1.19.1-6
- Drop qt5-devel buildrequires

* Sun Feb 16 2020 Hans de Goede <hdegoede@redhat.com> - 1.19.1-5
- Fix FTBFS (rhbz#1799829)

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.19.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.19.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.19.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Oct 29 2018 François Cami <fcami@fedoraproject.org> - 1.19.1-1
- New upstream release
- Update upstream URLs for real

* Mon Oct 8 2018 François Cami <fcami@fedoraproject.org> - 1.19.0-1
- Update upstream URLs to http://openal-soft.org/
- New upstream release
- Rebase patches

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.18.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Feb 26 2018 Hans de Goede <hdegoede@redhat.com> - 1.18.2-5
- Allow pulseaudio to move openal-soft output streams (rhbz#1544381)
- Fix release -4 not building (rhbz#1544012)
- Drop unnecessary qt-devel BuildRequires (we also BuildRequire qt5-devel)

* Fri Feb 09 2018 Tomasz Kłoczko <kloczek@fedoraproject.org> - 1.18.2-4
- remove support for no longer supported Fedora versions (<=25)
- fix: add %%{_libdir}/cmake/OpenAL directory to devel
- fix: s/_datarootdir/_datadir/ as this package does not uses datarootdir
  but datadir
- fix: add %%{_datadir}/openal to main package as well and to %%exclude
  %%{_datadir}/openal/{alsoftrc.sample,presets/presets.txt} as those files
  are not needed
- removed Group fields
  (https://fedoraproject.org/wiki/Packaging:Guidelines#Tags_and_Sections)
- add use more macros (%%autosetup, %%make_build, %%make_install)

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.18.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Feb 03 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.18.2-2
- Switch to %%ldconfig_scriptlets

* Sun Jan 21 2018 François Cami <fcami@fedoraproject.org> - 1.18.2-1
- New upstream release
- Move bsincgen to -devel and altonegen to -examples

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.18.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.18.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jul 02 2017 François Cami <fcami@fedoraproject.org> - 1.18.0-1
- New upstream release
- Add BR: qt5-devel + SDL_sound-devel
- Add -examples subpackage

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.17.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sat Feb 20 2016 Hans de Goede <hdegoede@redhat.com> - 1.17.2-2
- Fix FTBFS on ARM (rhbz#1307818)

* Thu Feb 04 2016 François Cami <fcami@fedoraproject.org> - 1.17.2-1
- New upstream release

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.17.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sun Dec 13 2015 François Cami <fcami@fedoraproject.org> - 1.17.1-1
- New upstream release

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.16.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 1.16.0-6
- Rebuilt for GCC 5 C++11 ABI change

* Sun Jan 25 2015 François Cami <fcami@fedoraproject.org> - 1.16.0-5
- Build against FluidSynth.

* Sat Jan 24 2015 Ville Skyttä <ville.skytta@iki.fi> - 1.16.0-4
- Own the hrtf dir

* Mon Sep 8 2014 Marcin Juszkiewicz <mjuszkiewicz@redhat.com> - 1.16.0-3
- Check for arm_neon.h only on 32bit ARM

* Tue Aug 26 2014 François Cami <fcami@fedoraproject.org> - 1.16.0-2
- Add the -qt subpackage to host the alsoft-config tool

* Sun Aug 17 2014 François Cami <fcami@fedoraproject.org> - 1.16.0-1
- New upstream release

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.15.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.15.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.15.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.15.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jan 11 2013 François Cami <fcami@fedoraproject.org> - 1.15.1-1
- New upstream release

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.14-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Apr 12 2012 Dan Horák <dan[at]danny.cz> - 1.14-2
- the used fpu control bits are x86 specific

* Fri Apr  6 2012 Hans de Goede <hdegoede@redhat.com> - 1.14-1
- 1.14-1
- version upgrade (rhbz#808968)
- spec cleanup

* Thu Jan 26 2012 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.13-1
- version upgrade
- spec cleanup

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12.854-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12.854-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Apr 01 2010 Thomas Kowaliczek <linuxdonald@linuxdonald.de> - 1.12.854-1
- New upstream release

* Mon Mar 01 2010 Thomas Kowaliczek <linuxdonald@linuxdonald.de> - 1.11.753-3.20100225
- Fixed Version Number

* Sun Feb 28 2010 Thomas Kowaliczek <linuxdonald@linuxdonald.de> - 1.11.753-2.a9e0e57797c6f4321d5776e1f29bf1e75b11e6a1
- Fixed Bug 567870

* Mon Jan 18 2010 Thomas Kowaliczek <linuxdonald@linuxdonald.de> - 1.11.753-1
- New Upstream Release

* Wed Jan 13 2010 Thomas Kowaliczek <linuxdonald@linuxdonald.de> - 1.10.622-7.931f5875cdc4ce0ac61a5110f11e962426e53d99
- Newer git version that fix more problems with pulseaudio.

* Mon Jan 04 2010 Thomas Kowaliczek <linuxdonald@linuxdonald.de> - 1.10.622-6.0ceaa01c3de75c946ff2e7591e7f69b28ec00409
- Newer git version with more Pulseaudio fixes. Have fun.

* Mon Dec 28 2009 Thomas Kowaliczek <linuxdonald@linuxdonald.de> - 1.10.622-5.3793919892e6d61e5fec3abeaaeebc3f2332be13
- Fixed small spec verion info.

* Mon Dec 28 2009 Thomas Kowaliczek <linuxdonald@linuxdonald.de> - 1.10.622-4.3793919892e6d61e5fec3abeaaeebc3f2332be13
- Fixed broken upgrade paths.

* Sat Dec 26 2009 Thomas Kowaliczek <linuxdonald@linuxdonald.de> - 1.10.622-3.3793919892e6d61e5fec3abeaaeebc3f2332be13
- Updatet to an newer git version because of some pulseaudio fixes.

* Tue Nov 10 2009 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de> - 1.10.622-2
- add default config

* Mon Nov 09 2009 Thomas Kowaliczek <linuxdonald@linuxdonald.de> - 1.10.622-1
- New upstream release

* Sat Nov 07 2009 Thomas Kowaliczek <linuxdonald@linuxdonald.de> - 1.9.563-2.c1b161b44bbf60420de2e1ba886e957d9fcd495e
- Updatet to an newer git version because of some pulseaudio fixes.
- I hope it fix bug 533501

* Fri Oct  09 2009 Hans de Goede <hdegoede@redhat.com> - 1.9.563-1.d6e439244ae00a1750f0dc8b249f47efb4967a23git
- Update to 1.9.563 + some fixes from git
- This fixes:
  - Not having any sound in chromium-bsu
  - Various openal using programs hanging on exit

* Fri Aug 21 2009 Thomas Kowaliczek <linuxdonald@linuxdonald.de> - 1.8.466-9.487f0dde7593144ceabd817306500465caf7602agit
- Fixed version info

* Fri Aug 21 2009 Thomas Kowaliczek <linuxdonald@linuxdonald.de> - 1.8.466-8.487f0dde7593144ceabd817306500465caf7602agit
- Fixed bug 517973

* Sun Aug 16 2009 Thomas Kowaliczek <linuxdonald@linuxdonald.de> - 1.8.466-7
- Fixed bug 517721. Added upstream.patch

* Sat Aug 08 2009 Thomas Kowaliczek <linuxdonald@linuxdonald.de> - 1.8.466-6
- Fixed license and pkgconfig problem thx goes to Christoph Wickert

* Wed Aug 05 2009 Thomas Kowaliczek <linuxdonald@linuxdonald.de> - 1.8.466-5
- Fixed Obsoletes: and Provides: sections

* Tue Aug 04 2009 Thomas Kowaliczek <linuxdonald@linuxdonald.de> - 1.8.466-4
- Added Obsoletes: openal <= 0.0.9 and remove Conflicts: openal-devel

* Fri Jun 26 2009 Thomas Kowaliczek <linuxdonald@linuxdonald.de> - 1.8.466-3
- Fixed all warnings of rpmlint

* Sat Jun 20 2009 Thomas Kowaliczek <linuxdonald@linuxdonald.de> - 1.8.466-2
- Update the SPEC and SRPM file because openal-soft-devel conflicts with
openal-devel

* Sat Jun 20 2009 Thomas Kowaliczek <linuxdonald@linuxdonald.de> - 1.8.466-1
- Initial release for Fedora

## END: Generated by rpmautospec
