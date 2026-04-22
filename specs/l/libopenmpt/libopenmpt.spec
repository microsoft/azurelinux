# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name: libopenmpt
Version: 0.8.4
Release: 3%{?dist}

%global tar_root %{name}-%{version}+release.autotools

License: BSD-3-Clause
Summary: C/C++ library to decode tracker music module (MOD) files

URL: https://lib.openmpt.org/libopenmpt/

Source0: https://lib.openmpt.org/files/libopenmpt/src/%{tar_root}.tar.gz

BuildRequires: make
BuildRequires: gcc-c++
BuildRequires: chrpath
BuildRequires: pkgconfig(libmpg123)
BuildRequires: pkgconfig(ogg)
BuildRequires: pkgconfig(vorbis)
BuildRequires: pkgconfig(sndfile)
BuildRequires: pkgconfig(flac)
BuildRequires: pkgconfig(zlib)

# for command-line player audio output
BuildRequires: pulseaudio-libs-devel
# don't build with niche options
#BuildRequires: portaudio-devel
#BuildRequires: SDL-devel
#BuildRequires: SDL2-devel

%description
libopenmpt is a cross-platform C++ and C library to decode tracked music
files (modules) into a raw PCM audio stream.

libopenmpt is based on the player code of the OpenMPT project (Open
ModPlug Tracker). In order to avoid code base fragmentation, libopenmpt is
developed in the same source code repository as OpenMPT.


%package -n openmpt123
Summary: Command-line tracker music player based on libopenmpt
Group: Applications/Multimedia
Requires: %{name}%{?_isa} = %{version}-%{release}

%description -n openmpt123
Openmpt123 is a cross-platform command-line or terminal based player
for tracker music (MOD) module files.


%package devel
Summary: Development files for the libopenmpt library
Group: Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
Files needed when building software which uses libopenmpt.


%prep
%autosetup -p1 -n %{tar_root}
sed -i 's/\r$//' LICENSE


%build
%configure  \
  --disable-static  \
  --without-sdl --without-sdl2 \
  --without-portaudio --without-portaudiocpp
make %{?_smp_mflags}


%install
%make_install
find ${RPM_BUILD_ROOT} -type f -name "*.la" -exec rm -f {} ';'
chrpath --delete ${RPM_BUILD_ROOT}%{_bindir}/openmpt123


%files -n openmpt123
%{_bindir}/openmpt123
%{_mandir}/man1/*

%files
%license LICENSE
%{_libdir}/*.so.0*
%{_docdir}/%{name}/
%exclude %{_docdir}/%{name}/examples

%files devel
%{_includedir}/%{name}/
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_docdir}/%{name}/examples/


%changelog
* Fri Jan 16 2026 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Sun Dec 14 2025 Michael Schwendt <mschwendt@fedoraproject.org> - 0.8.4-1
- update to 0.8.4

* Sat Sep 06 2025 Michael Schwendt <mschwendt@fedoraproject.org> - 0.8.3-1
- update to 0.8.3

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jul 19 2025 Michael Schwendt <mschwendt@fedoraproject.org> - 0.8.2-1
- update to 0.8.2

* Sat Jun 14 2025 Michael Schwendt <mschwendt@fedoraproject.org> - 0.8.1-1
- update to 0.8.1

* Sat May 31 2025 Michael Schwendt <mschwendt@fedoraproject.org> - 0.8.0-1
- upgrade to new stable release 0.8.0

* Tue May 27 2025 Jitka Plesnikova <jplesnik@redhat.com> - 0.7.13-4
- Rebuilt for flac 1.5.0

* Mon Jan 20 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.13-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Jan  7 2025 Michael Schwendt <mschwendt@fedoraproject.org> - 0.7.13-1
- update to 0.7.13

* Tue Dec  3 2024 Michael Schwendt <mschwendt@fedoraproject.org> - 0.7.12-1
- update to 0.7.12

* Sun Oct 27 2024 Michael Schwendt <mschwendt@fedoraproject.org> - 0.7.11-1
- update to 0.7.11

* Sun Sep 22 2024 Michael Schwendt <mschwendt@fedoraproject.org> - 0.7.10-1
- update to 0.7.10

* Sun Jul 21 2024 Michael Schwendt <mschwendt@fedoraproject.org> - 0.7.9-1
- update to 0.7.9

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sun Jun  9 2024 Michael Schwendt <mschwendt@fedoraproject.org> - 0.7.8-1
- Update to 0.7.8.

* Fri Mar 29 2024 Michael Schwendt <mschwendt@fedoraproject.org> - 0.7.6-1
- update to 0.7.6

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Nov  4 2023 Michael Schwendt <mschwendt@fedoraproject.org> - 0.7.3-1
- update to 0.7.3

* Sun Jul 23 2023 Michael Schwendt <mschwendt@fedoraproject.org> - 0.7.2-1
- upgrade to 0.7.2

* Thu Jul 20 2023 Michael Schwendt <mschwendt@fedoraproject.org> - 0.6.11-1
- update to 0.6.11

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sun Apr 30 2023 Michael Schwendt <mschwendt@fedoraproject.org> - 0.6.10-1
- update to 0.6.10

* Sun Mar  5 2023 Michael Schwendt <mschwendt@fedoraproject.org> - 0.6.9-1
- update to 0.6.9

* Sat Feb 18 2023 Michael Schwendt <mschwendt@fedoraproject.org> - 0.6.8-1
- update to 0.6.8

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild


* Mon Jan  9 2023 Michael Schwendt <mschwendt@fedoraproject.org> - 0.6.7-1
- update to 0.6.7

* Sat Oct  1 2022 Michael Schwendt <mschwendt@fedoraproject.org> - 0.6.6-1
- update to 0.6.6

* Sat Sep 17 2022 Michael Schwendt <mschwendt@fedoraproject.org> - 0.6.5-1
- update to 0.6.5

* Wed Sep 14 2022 Michel Alexandre Salim <salimma@fedoraproject.org> - 0.6.4-3
- Rebuilt for flac 1.4.0

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jun 24 2022 Michael Schwendt <mschwendt@fedoraproject.org> - 0.6.4-1
- update to 0.6.4

* Mon May  2 2022 Michael Schwendt <mschwendt@fedoraproject.org> - 0.6.3-1
- update to 0.6.3

* Tue Feb 15 2022 Michael Schwendt <mschwendt@fedoraproject.org> - 0.6.1-1
- update to 0.6.1

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Dec 23 2021 Michael Schwendt <mschwendt@fedoraproject.org> - 0.6.0-1
- upgrade to 0.6.0 (new stable release branch)

* Thu Dec 23 2021 Michael Schwendt <mschwendt@fedoraproject.org> - 0.5.15-1
- update to 0.5.15 (security release)

* Mon Dec  6 2021 Michael Schwendt <mschwendt@fedoraproject.org> - 0.5.14-1
- update to 0.5.14 (security release)

* Mon Nov 29 2021 Michael Schwendt <mschwendt@fedoraproject.org> - 0.5.13-1
- update to 0.5.13

* Thu Oct  7 2021 Michael Schwendt <mschwendt@fedoraproject.org> - 0.5.12-1
- update to 0.5.12 (security release)

* Wed Aug 25 2021 Michael Schwendt <mschwendt@fedoraproject.org> - 0.5.11-1
- update to 0.5.11 (security release)

* Tue Aug 17 2021 Michael Schwendt <mschwendt@fedoraproject.org> - 0.5.10-1
- update to 0.5.10

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Apr 30 2021 Michael Schwendt <mschwendt@fedoraproject.org> - 0.5.8-1
- update to 0.5.8 (security release for the 0.5 series)

* Fri Apr  2 2021 Michael Schwendt <mschwendt@fedoraproject.org> - 0.5.7-1
- update to 0.5.7 (security release for the 0.5 series)

* Thu Feb 18 2021 Michael Schwendt <mschwendt@fedoraproject.org> - 0.5.5-1
- update to 0.5.5

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Dec 22 2020 Michael Schwendt <mschwendt@fedoraproject.org> - 0.5.4-1
- update to 0.5.4

* Thu Oct 29 2020 Michael Schwendt <mschwendt@fedoraproject.org> - 0.5.3-1
- upgrade to 0.5.3 (security release for the 0.5 series)

* Thu Oct 29 2020 Michael Schwendt <mschwendt@fedoraproject.org> - 0.4.15-1
- update to 0.4.15

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Dec 24 2019 Michael Schwendt <mschwendt@fedoraproject.org> - 0.4.11-1
- update to 0.4.11

* Fri Dec 20 2019 Michael Schwendt <mschwendt@fedoraproject.org> - 0.4.10-2
- spec modifications as per Fedora reviewer comment in rhbz #1768408
- remove RPATH from openmpt123

* Mon Nov  4 2019 Michael Schwendt <mschwendt@fedoraproject.org> - 0.4.10-1
- update to 0.4.10

* Sat Jun 01 2019 Michael Schwendt <mschwendt@fedoraproject.org> - 0.4.5-1
- update to 0.4.5

* Sun Apr 21 2019 Michael Schwendt <mschwendt@fedoraproject.org> - 0.4.4-1
- update to 0.4.4

* Sat Feb 23 2019 Michael Schwendt <mschwendt@fedoraproject.org> - 0.4.3-1
- security update 0.4.3

* Sun Dec 30 2018 Michael Schwendt <mschwendt@fedoraproject.org> - 0.4.0-1
- initial package for libopenmpt 0.4.0
