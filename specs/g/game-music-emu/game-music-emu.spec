# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           game-music-emu
Version:        0.6.4
Release: 3%{?dist}
Provides:       libgme%{?_isa} = %{version}-%{release}
Summary:        Video game music file emulation/playback library
# Automatically converted from old format: LGPLv2+ - review is highly recommended.
License:        LicenseRef-Callaway-LGPLv2+
URL:            https://github.com/libgme/game-music-emu
Source0:        %{url}/archive/%{version}/game-music-emu-%{version}.tar.gz


BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  cmake
BuildRequires:  zlib-devel
# needed to build the player
BuildRequires:  SDL2-devel
BuildRequires: make

%package devel
Summary:        Development files for Game_Music_Emu
Provides:       libgme-devel%{?_isa} = %{version}-%{release}
Requires:       %{name}%{?_isa} = %{version}
Requires:       pkgconfig

%package player
Summary:        Demo player utilizing Game_Music_Emu
# Automatically converted from old format: MIT - review is highly recommended.
License:        MIT


%description
Game_Music_Emu is a collection of video game music file emulators that support
the following formats and systems:

 * AY       ZX Spectrum/Amstrad CPC
 * GBS      Nintendo Game Boy
 * GYM      Sega Genesis/Mega Drive
 * HES      NEC TurboGrafx-16/PC Engine
 * KSS      MSX Home Computer/other Z80 systems (doesn't support FM sound)
 * NSF/NSFE Nintendo NES/Famicom (with VRC 6, Namco 106, and FME-7 sound)
 * SAP      Atari systems using POKEY sound chip
 * SPC      Super Nintendo/Super Famicom
 * VGM/VGZ  Sega Master System/Mark III, Sega Genesis/Mega Drive,BBC Micro

%description devel
This package contains files needed to compile code which uses Game_Music_Emu.

%description player
This package contains the demo player for files supported by Game_Music_Emu.


%prep
%setup -q
# add install rule for the player
echo -e "\ninstall(TARGETS gme_player RUNTIME DESTINATION %{_bindir})" >> player/CMakeLists.txt


%build
%cmake -D ENABLE_UBSAN:BOOL=OFF -D GME_BUILD_STATIC:BOOL=OFF
%cmake_build
# explicitly build the player as it has EXCLUDE_FROM_ALL set
%cmake_build --target gme_player


%install
%cmake_install
# explicitly install the player as it has EXCLUDE_FROM_ALL set
pushd %{_vpath_builddir}/player
make install DESTDIR=%{buildroot}
popd


%ldconfig_scriptlets


%files
%doc changes.txt license.txt readme.txt
%{_libdir}/libgme.so.*

%files devel
%doc design.txt gme.txt
%{_libdir}/libgme.so
%{_includedir}/gme/
%{_libdir}/pkgconfig/libgme.pc

%files player
%{_bindir}/gme_player


%changelog
* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Mar 03 2025 Karel Volný <kvolny@redhat.com> 0.6.4-1
- New release 0.6.4 (rhbz#2345943)
- Updated repository location (rhbz#2247599)

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.3-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Aug 28 2024 Miroslav Suchý <msuchy@redhat.com> - 0.6.3-16
- convert license to SPDX

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.3-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.3-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.3-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.3-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.3-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.3-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue May 10 2022 Karel Volný <kvolny@redhat.com> 0.6.3-9
- Removed libubsan BuildRequires

* Wed Mar 16 2022 Karel Volný <kvolny@redhat.com> 0.6.3-8
- Disable UBSAN as per https://bugzilla.redhat.com/show_bug.cgi?id=2045404#c12

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Sep 08 2020 Karel Volný <kvolny@redhat.com> 0.6.3-4
- Adapted to F33 System-Wide Change: CMake to do out-of-source builds
  (fixes rhbz#1863593)

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.3-3
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Mar 30 2020 Karel Volný <kvolny@redhat.com> 0.6.3-1
- New release 0.6.3 (rhbz#1806784)
- Fixes FTBFS (rhbz#1799384)

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Dec 18 2018 Karel Volný <kvolny@redhat.com> 0.6.2-1
- New release 0.6.2
- Fixes CVE-2017-17446 (rhbz#1524562)
- Update tarball url

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Dec 15 2016 Karel Volný <kvolny@redhat.com> 0.6.1-1
- New release 0.6.1
- Fixes CVE-2016-9959 (security issues in SNES emulation)
  https://scarybeastsecurity.blogspot.cz/2016/12/redux-compromising-linux-using-snes.html
- Updated URLs - project moved
- Dropped gme-0.6.0-pc-lib-suffix.patch (accepted upstream)

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 0.6.0-6
- Rebuilt for GCC 5 C++11 ABI change

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Sep 20 2013 Karel Volný <kvolny@redhat.com> 0.6.0-3
- Adjust virtual provides according to further comments on bug#1006881

* Fri Sep 13 2013 Karel Volný <kvolny@redhat.com> 0.6.0-2
- Add virtual provides libgme (bug #1006881)

* Thu Aug 22 2013 Karel Volný <kvolny@redhat.com> 0.6.0-1
- New release
- See changes.txt for list of upstream changes
- Adds pkgconfig file (+ patch to correct path)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jun 24 2011 Karel Volny <kvolny@redhat.com> 0.5.5-1
- Initial release for Fedora 15
