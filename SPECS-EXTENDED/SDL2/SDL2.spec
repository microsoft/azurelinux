%bcond_with jack
Summary:        Cross-platform multimedia library
Name:           SDL2
Version:        2.24.0
Release:        2%{?dist}
License:        zlib AND MIT
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://www.libsdl.org/
Source0:        https://www.libsdl.org/release/%{name}-%{version}.tar.gz
Source1:        SDL_config.h
Source2:        SDL_revision.h
Patch0:         multilib.patch
# ptrdiff_t is not the same as khronos defines on 32bit arches
Patch1:         SDL2-2.0.9-khrplatform.patch
# Prefer Wayland by default
Patch2:         SDL2-2.0.22-prefer-wayland.patch
BuildRequires:  git-core
BuildRequires:  cmake
BuildRequires:  make
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  alsa-lib-devel
BuildRequires:  mesa-libGL-devel
BuildRequires:  mesa-libGLU-devel
BuildRequires:  mesa-libEGL-devel
BuildRequires:  mesa-libGLES-devel
BuildRequires:  libXext-devel
BuildRequires:  libX11-devel
BuildRequires:  libXi-devel
BuildRequires:  libXrandr-devel
BuildRequires:  libXrender-devel
BuildRequires:  libXScrnSaver-devel
BuildRequires:  libXinerama-devel
BuildRequires:  libXcursor-devel
BuildRequires:  systemd-devel
BuildRequires:  pkgconfig(libusb-1.0)
# PulseAudio
BuildRequires:  pkgconfig(libpulse-simple)
%if %{with jack}
# Jack
BuildRequires:  pkgconfig(jack)
%endif
# PipeWire
BuildRequires:  pkgconfig(libpipewire-0.3)
# D-Bus
BuildRequires:  pkgconfig(dbus-1)
# IBus
BuildRequires:  pkgconfig(ibus-1.0)
# Wayland
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-egl)
BuildRequires:  pkgconfig(wayland-cursor)
BuildRequires:  pkgconfig(wayland-protocols)
BuildRequires:  pkgconfig(wayland-scanner)
BuildRequires:  pkgconfig(xkbcommon)
# Vulkan
BuildRequires:  vulkan-devel
# KMS
BuildRequires:  mesa-libgbm-devel
BuildRequires:  libdrm-devel

%description
Simple DirectMedia Layer (SDL) is a cross-platform multimedia library designed
to provide fast access to the graphics frame buffer and audio device.

%package devel
Summary:        Files needed to develop Simple DirectMedia Layer applications
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       libX11-devel%{?_isa}
Requires:       mesa-libEGL-devel%{?_isa}
Requires:       mesa-libGLES-devel%{?_isa}
# Conflict with versions before libSDLmain moved here
Conflicts:      %{name}-static < 2.0.18-4

%description devel
Simple DirectMedia Layer (SDL) is a cross-platform multimedia library designed
to provide fast access to the graphics frame buffer and audio device. This
package provides the libraries, include files, and other resources needed for
developing SDL applications.

%package static
Summary:        Static libraries for SDL2
# Needed to keep CMake happy
Requires:       %{name}-devel%{?_isa} = %{version}-%{release}
# Conflict with versions before libSDLmain moved to -devel
Conflicts:      %{name}-devel < 2.0.18-4

%description static
Static libraries for SDL2.

%prep
%autosetup -p1 -n %{name}-%{version}
sed -i -e 's/\r//g' TODO.txt README.md WhatsNew.txt BUGS.txt LICENSE.txt CREDITS.txt README-SDL.txt

%build
# Deal with new CMake policy around whitespace in LDFLAGS...
export LDFLAGS="%{shrink:%{build_ldflags}}"

mkdir -p buildDir

%cmake \
    -DSDL_DLOPEN=ON \
    -DSDL_VIDEO_KMSDRM=ON \
    -DSDL_ARTS=OFF \
    -DSDL_ESD=OFF \
    -DSDL_NAS=OFF \
    -DSDL_PULSEAUDIO_SHARED=ON \
%if %{with jack}
    -DSDL_JACK_SHARED=ON \
%else
    -DSDL_JACK=OFF \
%endif
    -DSDL_PIPEWIRE_SHARED=ON \
    -DSDL_ALSA=ON \
    -DSDL_VIDEO_WAYLAND=ON \
    -DSDL_VIDEO_VULKAN=ON \
    -DSDL_SSE3=OFF \
    -DSDL_RPATH=OFF \
    -DSDL_STATIC=ON \
    -DSDL_STATIC_PIC=ON -B ./buildDir

cmake --build buildDir %{?_smp_mflags} --verbose

%install
DESTDIR=%{buildroot} cmake --install buildDir

# Rename SDL_config.h to SDL_config-<arch>.h to avoid file conflicts on
# multilib systems and install SDL_config.h wrapper
mv %{buildroot}%{_includedir}/SDL2/SDL_config.h %{buildroot}%{_includedir}/SDL2/SDL_config-%{_arch}.h
install -p -m 644 %{SOURCE1} %{buildroot}%{_includedir}/SDL2/SDL_config.h

# Rename SDL_revision.h to SDL_revision-<arch>.h to avoid file conflicts on
# multilib systems and install SDL_revision.h wrapper
# TODO: Figure out how in the hell the SDL_REVISION changes between architectures on the same SRPM.
mv %{buildroot}%{_includedir}/SDL2/SDL_revision.h %{buildroot}%{_includedir}/SDL2/SDL_revision-%{_arch}.h
install -p -m 644 %{SOURCE2} %{buildroot}%{_includedir}/SDL2/SDL_revision.h

%files
%license LICENSE.txt
%doc BUGS.txt CREDITS.txt README-SDL.txt
%{_libdir}/libSDL2-2.0.so.0*

%files devel
%doc README.md TODO.txt WhatsNew.txt
%{_bindir}/*-config
%{_libdir}/lib*.so
%{_libdir}/libSDL2main.a
%{_libdir}/pkgconfig/sdl2.pc
%dir %{_libdir}/cmake/SDL2
%{_libdir}/cmake/SDL2/SDL2Config*.cmake
%{_libdir}/cmake/SDL2/SDL2Targets*.cmake
%{_libdir}/cmake/SDL2/SDL2mainTargets*.cmake
%{_includedir}/SDL2
%{_datadir}/aclocal/*
%{_libdir}/libSDL2_test.a
%{_libdir}/cmake/SDL2/SDL2testTargets*.cmake

%files static
%license LICENSE.txt
%{_libdir}/libSDL2.a
%{_libdir}/cmake/SDL2/SDL2staticTargets*.cmake

%changelog
* Fri Nov 25 2022 Sumedh Sharma <sumsharma@microsoft.com> - 2.24.0-2
- Initial CBL-Mariner import from Fedora 37 (license: MIT)
- Build with feature disabled: jack
- License verified

* Fri Aug 19 2022 Neal Gompa <ngompa@fedoraproject.org> - 2.24.0-1
- Update to 2.24.0
- Drop backported patches included in this release

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.22-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jul 07 2022 Ian Mullins <imullins@redhat.com> - 2.0.22-3
- Fix assumption that DRI_DEVNAME begins at 0 patch

* Sat Apr 30 2022 Neal Gompa <ngompa@fedoraproject.org> - 2.0.22-2
- Use the correct BR for libusb

* Sat Apr 30 2022 Neal Gompa <ngompa@fedoraproject.org> - 2.0.22-1
- Update to 2.0.22
- Drop backported patches included in this release

* Tue Feb 08 2022 Neal Gompa <ngompa@fedoraproject.org> - 2.0.20-3
- Backport Wayland and PipeWire fixes from upstream

* Wed Jan 19 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.20-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Jan 11 2022 Neal Gompa <ngompa@fedoraproject.org> - 2.0.20-1
- Update to 2.0.20
- Drop backported patches included in this release

* Fri Jan 07 2022 Neal Gompa <ngompa@fedoraproject.org> - 2.0.18-5
- Refresh SDL target split patch to include targets correctly

* Fri Jan 07 2022 Neal Gompa <ngompa@fedoraproject.org> - 2.0.18-4
- Move libSDLmain from -static to -devel

* Tue Jan 04 2022 Neal Gompa <ngompa@fedoraproject.org> - 2.0.18-3
- Backport fix for building against wayland-1.20+
- Add patch to split SDL2 CMake targets for static libraries

* Wed Dec 01 2021 Neal Gompa <ngompa@fedoraproject.org> - 2.0.18-2
- Use correct build options

* Wed Dec 01 2021 Neal Gompa <ngompa@fedoraproject.org> - 2.0.18-1
- Update to 2.0.18

* Wed Oct  6 2021 Tom Callaway <spot@fedoraproject.org> - 2.0.16-4
- fix multilib conflict with SDL_revision.h (bz 2008838)

* Sun Sep 26 2021 Neal Gompa <ngompa@fedoraproject.org> - 2.0.16-3
- Backport select fixes from upstream
  + Support legacy 'pulse' alias for PulseAudio driver
  + Fix handling of Ctrl key on Wayland
  + Add support for HiDPI cursors on Wayland
  + Fix keymap support on Wayland (rhbz#2007969)
  + Use EGL_EXT_present_opaque when available on Wayland
  + Expose xdg_toplevel to SysWM on Wayland

* Sun Aug 22 2021 Neal Gompa <ngompa@fedoraproject.org> - 2.0.16-2
- Ensure libdecor is pulled in when libwayland-client is (rhbz#1992804)

* Tue Aug 10 2021 Neal Gompa <ngompa@fedoraproject.org> - 2.0.16-1
- Update to 2.0.16

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.14-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Jun  3 2021 Tom Callaway <spot@fedoraproject.org> - 2.0.14-5
- add -static Requires to -devel to make CMake stop failing on missing files (bz1965359)

* Mon May 17 2021 Neal Gompa <ngompa13@gmail.com> - 2.0.14-4
- Switch to CMake to build SDL2
- Build JACK support unconditionally since PipeWire-JACK exists in RHEL 9

* Mon Feb 22 2021 Hans de Goede <hdegoede@redhat.com> - 2.0.14-3
- SDL2 no longer uses audiofile, drop the audiofile-devel BuildRequires

* Mon Jan 25 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Jan 21 2021 Pete Walter <pwalter@fedoraproject.org> - 2.0.14-1
- Update to 2.0.14
- Rebase multilib.patch
- Don't use globs in the form of libFOO.so.* for listing files

* Tue Jan 12 2021 Wim Taymans <wtaymans@redhat.com> - 2.0.12-5
- Disable JACK on rhel >= 8

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.12-4
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.12-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 13 2020 Tom Stellard <tstellar@redhat.com> - 2.0.12-2
- Use make macros
- https://fedoraproject.org/wiki/Changes/UseMakeBuildInstallMacro

* Wed Mar 11 2020 Pete Walter <pwalter@fedoraproject.org> - 2.0.12-1
- Update to 2.0.12

* Tue Feb 11 2020 Tom Callaway <spot@fedoraproject.org> - 2.0.10-3
- apply upstream fix for FTBFS

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Pete Walter <pwalter@fedoraproject.org> - 2.0.10-1
- Update to 2.0.10

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 15 2019 Tom Callaway <spot@fedoraproject.org> - 2.0.9-3
- use khrplatform defines, not ptrdiff_t

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Nov  2 2018 Tom Callaway <spot@fedoraproject.org> - 2.0.9-1
- update to 2.0.9

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.8-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon May 21 2018 Adam Jackson <ajax@redhat.com> - 2.0.8-5
- Backport a crash/hang fix from 2.0.9 (#1580541)

* Wed Apr 11 2018 Tom Callaway <spot@fedoraproject.org> - 2.0.8-4
- enable video-kmsdrm

* Fri Mar 30 2018 David Abdurachmanov <david.abdurachmanov@gmail.com> - 2.0.8-3
- Add riscv64 to SDL_config.h

* Sun Mar 04 2018 Miro Hrončok <mhroncok@redhat.com> - 2.0.8-2
- Disable altivec on ppc64le (RHBZ #1551338)

* Sun Mar  4 2018 Peter Robinson <pbrobinson@fedoraproject.org> 2.0.8-1
- Update to 2.0.8

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jan 31 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.0.7-3
- Switch to %%ldconfig_scriptlets

* Sun Nov 05 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.0.7-2
- Fix IBus

* Tue Oct 24 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.0.7-1
- Update to 2.0.7

* Thu Oct 19 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.0.6-4
- Fully fix last overflow

* Wed Oct 11 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.0.6-3
- Fix potential overflow in surface allocation

* Thu Oct 05 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.0.6-2
- Fix invalid dbus arguments

* Sat Sep 23 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.0.6-1
- Update to 2.0.6

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Jan 27 2017 Igor Gnatenko <ignatenko@redhat.com> - 2.0.5-3
- Fix NULL dereference (RHBZ #1416945)

* Wed Oct 26 2016 Dan Horák <dan[at]danny.cz> - 2.0.5-2
- fix FTBFS on ppc64/ppc64le

* Thu Oct 20 2016 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 2.0.5-1
- Update to 2.0.5 (RHBZ #1387238)

* Mon Sep 05 2016 Kalev Lember <klember@redhat.com> - 2.0.4-9
- Backport Wayland fixes from upstream

* Sun Aug 14 2016 Igor Gnatenko <ignatenko@redhat.com> - 2.0.4-8
- Fix whitespaces in CMake file (RHBZ #1366868)

* Sun Jul 10 2016 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 2.0.4-7
- Remove useless Requirements from -devel subpkg

* Sun Jul 10 2016 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 2.0.4-6
- Add ibus support

* Sun Jul 10 2016 Joseph Mullally <jwmullally@gmail.com> - 2.0.4-5
- fix Wayland dynamic symbol loading (bz1354155)

* Thu Feb 25 2016 Tom Callaway <spot@fedoraproject.org> - 2.0.4-4
- enable static subpackage (bz1253930)

* Fri Feb  5 2016 Tom Callaway <spot@fedoraproject.org> - 2.0.4-3
- fix compile against latest wayland

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Jan 04 2016 Tom Callaway <spot@fedoraproject.org> - 2.0.4-1
- update to 2.0.4

* Fri Sep 04 2015 Michal Toman <mtoman@fedoraproject.org> - 2.0.3-7
- Add support for MIPS architecture to SDL_config.h

* Tue Jun 16 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Jun  2 2015 Tom Callaway <spot@fedoraproject.org> - 2.0.3-5
- remove code preventing builds with ancient gcc

* Fri Aug 15 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Wed Jun 11 2014 Karsten Hopp <karsten@redhat.com> 2.0.3-3
- fix filename of SDL_config.h for ppc64le

* Fri Jun 06 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Mar 19 2014 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 2.0.3-1
- 2.0.3 upstream release

* Sat Mar 08 2014 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 2.0.2-1
- 2.0.2 upstream release
- Enable wayland backend

* Tue Dec 10 2013 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 2.0.1-2
- Add libXinerama, libudev, libXcursor support (RHBZ #1039702)

* Thu Oct 24 2013 Tom Callaway <spot@fedoraproject.org> - 2.0.1-1
- update to 2.0.1

* Sat Aug 24 2013 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 2.0.0-3
- Fix multilib issues

* Tue Aug 13 2013 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 2.0.0-2
- SDL2 is released. Announce:
- https://lists.libsdl.org/pipermail/sdl-libsdl.org/2013-August/089854.html

* Sat Aug 10 2013 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 2.0.0-1.rc4
- Update to latest SDL2 (08.08.2013)

* Tue Jul 30 2013 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 2.0.0-1.rc3
- Fix Licenses
- some cleanups in spec

* Tue Jul 30 2013 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 2.0.0-1.rc2
- Delete -static package
- Fix License tag
- Fix end-of-line in documents
- Remove all spike-nails EL-specify (if someone will want to do - 'patches are welcome')
- Change Release tag to .rcX%%{?dist} (maintainer has changed released tarballs)

* Mon Jul 29 2013 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 2.0.0-1.rc1
- Some fixes in spec and cleanup

* Mon Jul 29 2013 Jon Ciesla <limburgher@gmail.com> - 2.0.0-1
- Ported from SDL 1.2.15-10
