# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global apiver 14

Name:           weston
Version:        14.0.2
Release:        2%{?dist}
Summary:        Reference compositor for Wayland

License:        MIT and CC-BY-SA-3.0
URL:            http://wayland.freedesktop.org/
Source0:        https://gitlab.freedesktop.org/wayland/%{name}/-/releases/%{version}/downloads/%{name}-%{version}.tar.xz

BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  glib2-devel
BuildRequires:  libjpeg-turbo-devel
BuildRequires:  pam-devel
# ninja-build is a dependency from meson
BuildRequires:  meson
BuildRequires:  pkgconfig(cairo)
BuildRequires:  pkgconfig(cairo) >= 1.10.0
BuildRequires:  pkgconfig(cairo-xcb)
BuildRequires:  pkgconfig(colord) >= 0.1.27
BuildRequires:  pkgconfig(dbus-1) >= 1.6
BuildRequires:  pkgconfig(egl)
BuildRequires:  pkgconfig(freerdp3)
BuildRequires:  pkgconfig(gbm) >= 10.2
BuildRequires:  pkgconfig(glesv2)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gobject-2.0)
BuildRequires:  pkgconfig(gstreamer-1.0)
BuildRequires:  pkgconfig(gstreamer-allocators-1.0)
BuildRequires:  pkgconfig(gstreamer-app-1.0)
BuildRequires:  pkgconfig(gstreamer-video-1.0)
BuildRequires:  pkgconfig(lcms2)
BuildRequires:  pkgconfig(libdisplay-info) >= 0.1.1
BuildRequires:  pkgconfig(libdrm) >= 2.4.109
BuildRequires:  pkgconfig(libevdev)
BuildRequires:  pkgconfig(libinput) >= 0.8.0
BuildRequires:  pkgconfig(libpipewire-0.3)
BuildRequires:  pkgconfig(libpng)
BuildRequires:  pkgconfig(libseat) >= 0.6.1
BuildRequires:  pkgconfig(libspa-0.2)
BuildRequires:  pkgconfig(libsystemd) >= 209
BuildRequires:  pkgconfig(libudev) >= 136
# libunwind available only on selected arches
%ifarch %{arm} aarch64 hppa ia64 mips ppc %{power64} %{ix86} x86_64
BuildRequires:  libunwind-devel
%endif
BuildRequires:  pkgconfig(libva) >= 0.34.0
BuildRequires:  pkgconfig(libva-drm) >= 0.34.0
BuildRequires:  pkgconfig(libwebp)
BuildRequires:  pkgconfig(libxml-2.0) >= 2.6
BuildRequires:  pkgconfig(mtdev) >= 1.1.0
BuildRequires:  (pkgconfig(neatvnc) >= 0.7.0 with pkgconfig(neatvnc) < 0.10.0)
BuildRequires:  pkgconfig(pangocairo)
BuildRequires:  pkgconfig(pixman-1) >= 0.25.2
BuildRequires:  pkgconfig(wayland-client) >= 1.22.0
BuildRequires:  pkgconfig(wayland-cursor)
BuildRequires:  pkgconfig(wayland-egl)
BuildRequires:  pkgconfig(wayland-protocols) >= 1.33
BuildRequires:  pkgconfig(wayland-scanner)
BuildRequires:  pkgconfig(wayland-server) >= 1.22
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(x11-xcb)
BuildRequires:  pkgconfig(xcb)
BuildRequires:  pkgconfig(xcb-cursor)
BuildRequires:  pkgconfig(xcb-composite)
BuildRequires:  pkgconfig(xcb-shm)
BuildRequires:  pkgconfig(xcb-xfixes)
BuildRequires:  pkgconfig(xcb-xkb)
BuildRequires:  pkgconfig(xcursor)
BuildRequires:  pkgconfig(xkbcommon)

Conflicts:      %{name} < 13.0.0-4
Obsoletes:      %{name} < 13.0.0-4
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
Requires:       mesa-dri-drivers

%description
Weston is the reference wayland compositor that can run on KMS, under X11
or under another compositor.

%package        session
Summary:        Weston desktop session
Conflicts:      %{name} < 13.0.0-4
Obsoletes:      %{name} < 13.0.0-4
Requires:       %{name} = %{version}-%{release}
BuildArch:      noarch

%description    session
Weston desktop session.

%package        libs
Summary:        Weston compositor libraries

%description    libs
This package contains Weston compositor libraries.

%package        demo
Summary:        Weston demo program files

%description    demo
This package contains Weston demo program files.

%package        devel
Summary:        Common headers for weston
# Automatically converted from old format: MIT - review is highly recommended.
License:        MIT
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}

%description    devel
Common headers for weston

%prep
%autosetup -p1

%build
%meson
%meson_build

%install
%meson_install

%check
# may be standalone tests can be done
#%%meson_test

%files
%config(noreplace) %{_sysconfdir}/pam.d/weston-remote-access
%license COPYING
%doc README.md
%{_bindir}/weston
%{_bindir}/weston-debug
%{_bindir}/weston-screenshooter
%{_bindir}/weston-tablet
%{_bindir}/weston-terminal
%{_bindir}/wcap-decode
%dir %{_libdir}/weston
%{_libdir}/weston/desktop-shell.so
%{_libdir}/weston/fullscreen-shell.so
%{_libdir}/weston/hmi-controller.so
%{_libdir}/weston/ivi-shell.so
%{_libdir}/weston/screen-share.so
%{_libdir}/weston/systemd-notify.so
%{_libdir}/weston/kiosk-shell.so
%{_libdir}/weston/libexec_weston.so*
%{_libexecdir}/weston-*
%{_mandir}/man1/*.1*
%{_mandir}/man5/*.5*
%{_mandir}/man7/*.7*
%dir %{_datadir}/weston
%{_datadir}/weston/*.png
%{_datadir}/weston/wayland.svg

%files session
%{_datadir}/wayland-sessions/weston.desktop

%files libs
%license COPYING
%dir %{_libdir}/libweston-%{apiver}
%{_libdir}/libweston-%{apiver}/color-lcms.so
%{_libdir}/libweston-%{apiver}/drm-backend.so
%{_libdir}/libweston-%{apiver}/gl-renderer.so
%{_libdir}/libweston-%{apiver}/headless-backend.so
%{_libdir}/libweston-%{apiver}/pipewire-backend.so
%{_libdir}/libweston-%{apiver}/pipewire-plugin.so
%{_libdir}/libweston-%{apiver}/remoting-plugin.so
%{_libdir}/libweston-%{apiver}/rdp-backend.so
%{_libdir}/libweston-%{apiver}/vnc-backend.so
%{_libdir}/libweston-%{apiver}/wayland-backend.so
%{_libdir}/libweston-%{apiver}/x11-backend.so
%{_libdir}/libweston-%{apiver}/xwayland.so
%{_libdir}/libweston-%{apiver}.so.0*

%files demo
%license COPYING
%{_bindir}/weston-calibrator
%{_bindir}/weston-clickdot
%{_bindir}/weston-cliptest
%{_bindir}/weston-constraints
%{_bindir}/weston-dnd
%{_bindir}/weston-editor
%{_bindir}/weston-eventdemo
%{_bindir}/weston-flower
%{_bindir}/weston-fullscreen
%{_bindir}/weston-image
%{_bindir}/weston-multi-resource
%{_bindir}/weston-presentation-shm
%{_bindir}/weston-resizor
%{_bindir}/weston-scaler
%{_bindir}/weston-simple-damage
%{_bindir}/weston-content_protection
%{_bindir}/weston-simple-dmabuf-egl
%{_bindir}/weston-simple-dmabuf-feedback
%{_bindir}/weston-simple-dmabuf-v4l
%{_bindir}/weston-simple-egl
%{_bindir}/weston-simple-shm
%{_bindir}/weston-simple-touch
%{_bindir}/weston-smoke
%{_bindir}/weston-stacking
%{_bindir}/weston-subsurfaces
%{_bindir}/weston-touch-calibrator
%{_bindir}/weston-transformed

%files devel
%{_includedir}/libweston-%{apiver}/
%{_includedir}/weston/
%{_libdir}/pkgconfig/libweston-%{apiver}.pc
%{_libdir}/pkgconfig/weston.pc
%{_libdir}/libweston-%{apiver}.so
%{_datadir}/pkgconfig/libweston-%{apiver}-protocols.pc
%{_datadir}/libweston-%{apiver}/protocols/

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 14.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon May 12 2025 Erico Nunes <ernunes@redhat.com> - 14.0.2-1
- Update to 14.0.2
- Drop upstreamed neatvnc patch

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 14.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Nov 21 2024 Neal Gompa <ngompa@fedoraproject.org> - 14.0.1-2
- Backport patch to allow neatvnc 0.9.0 as a dependency

* Mon Nov 11 2024 Neal Gompa <ngompa@fedoraproject.org> - 14.0.1-1
- Update to 14.0.1

* Wed Sep 04 2024 Miroslav Suchý <msuchy@redhat.com> - 14.0.0-2
- convert license to SPDX

* Wed Sep 04 2024 Neal Gompa <ngompa@fedoraproject.org> - 14.0.0-1
- Update to 14.0.0 final

* Mon Sep 02 2024 Neal Gompa <ngompa@fedoraproject.org> - 13.0.95-1
- Rebase to 14.0.0~rc3 (13.0.95)

* Tue Aug 27 2024 Neal Gompa <ngompa@fedoraproject.org> - 13.0.3-3
- Mark weston remote access pam config noreplace (rhbz#2307373)

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 13.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jul 17 2024 Nils Kattenbeck <nilskemail+fedora@gmail.com> - 13.0.3-1
- Update to 13.0.3
- Fix build error caused by neatvnc version increase

* Tue Feb 20 2024 Neal Gompa <ngompa@fedoraproject.org> - 13.0.0-5
- Split desktop session into its own subpackage

* Wed Feb 14 2024 Neal Gompa <ngompa@fedoraproject.org> - 13.0.0-4
- Use correct PipeWire dependency

* Tue Feb 06 2024 František Zatloukal <fzatlouk@redhat.com> - 13.0.0-3
- Rebuilt for turbojpeg 3.0.2

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 13.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Dec 07 2023 Erico Nunes <ernunes@redhat.com> - 13.0.0-1
- Update to 13.0.0
- Remove LDFLAGS which interfered with meson lcms2 function check
- Update demo clients list following upstream

* Thu Aug 03 2023 Erico Nunes <ernunes@redhat.com> - 12.0.2-1
- Update to 12.0.2

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 12.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon Jun 19 2023 Erico Nunes <ernunes@redhat.com> - 12.0.1-1
- Update to 12.0.1

* Wed May 31 2023 Erico Nunes <ernunes@redhat.com> - 12.0.0-1
- Update to 12.0.0

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 11.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Dec 16 2022 Erico Nunes <ernunes@redhat.com> - 11.0.1-1
- Update to 11.0.1
- Update download URL

* Fri Oct 07 2022 Erico Nunes <ernunes@redhat.com> - 11.0.0-1
- Update to 11.0.0
- Remove libweston-desktop following upstream.
- Remove weston-info, cms-{colord,static}.so following upstream.

* Mon Aug 15 2022 Simone Caronni <negativo17@gmail.com> - 10.0.1-3
- Rebuild for updated FreeRDP.

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 10.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jul 14 2022 Erico Nunes <ernunes@redhat.com> - 10.0.1-1
- Update to 10.0.1
- Update download URL

* Tue Apr 12 2022 Erico Nunes <ernunes@redhat.com> - 10.0.0-1
- Update to 10.0.0
- Remove weston-launch following upstream.
- Update shipped libraries.

* Tue Apr 12 2022 Dave Olsthoorn <daveo@fedoraproject.org> - 9.0.0-1
- Update to 9.0.0
- Use pipewire compat package for plugin
- (ernunes) Rebased from https://src.fedoraproject.org/rpms/weston/pull-request/3

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 8.0.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 8.0.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Apr 15 2021 Simone Caronni <negativo17@gmail.com> - 8.0.0-8
- Rebuild for updated FreeRDP.

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 8.0.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 8.0.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 08 2020 Jeff Law <law@redhat.com> - 8.0.0-5
- Fix link flags to work with LTO

* Fri May 22 2020 Simone Caronni <negativo17@gmail.com> - 8.0.0-4
- Rebuild for updated FreeRDP.

* Tue Feb 18 2020 Gerd Pokorra <gp@zimt.uni-siegen.de> - 8.0.0-3
- Add requires mesa-dri-drivers
- Work around at some meson build problem in rawhide

* Fri Feb 07 2020 Simone Caronni <negativo17@gmail.com> - 8.0.0-2
- Rebuild for updated FreeRDP.

* Tue Jan 28 2020 Gerd Pokorra <gp@zimt.uni-siegen.de> - 8.0.0-1
- Update to 8.0.0

* Mon Jan 20 2020 Gerd Pokorra <gp@zimt.uni-siegen.de> - 7.0.93-2
- Do the standard meson build with the meson macros 

* Mon Jan 20 2020 Gerd Pokorra <gp@zimt.uni-siegen.de> - 7.0.93-1
- Update to RC1 for Weston 8.0 (version 7.0.93)
- Remove have_simple_dmabuf_drm_client variable
- The executable weston-simple-dmabuf-drm is gone

* Fri Sep 27 2019 Gerd Pokorra <gp@zimt.uni-siegen.de> - 7.0.0-2
- Add and remove the group 'weston-launch' with the package in the post section

* Thu Sep 12 2019 Gerd Pokorra <gp@zimt.uni-siegen.de> - 7.0.0-1
- Update to 7.0.0
- Use meson as build system
- Use the apivar macro in the version line

* Wed Sep 04 2019 Takao Fujiwara <tfujiwar@redhat.com> - 6.0.0-3
- Add weston-demo sub package to include weston-editor

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Mar 29 2019 Kalev Lember <klember@redhat.com> - 6.0.0-1
- Update to 6.0.0

* Thu Feb 28 2019 Kalev Lember <klember@redhat.com> - 5.0.91-1
- Update to 5.0.91

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Sep 11 2018 Kalev Lember <klember@redhat.com> - 5.0.0-1
- Update to 5.0.0

* Mon Aug 13 2018 Kalev Lember <klember@redhat.com> - 4.0.93-1
- Update to 4.0.93

* Tue Jul 31 2018 Florian Weimer <fweimer@redhat.com> - 4.0.92-2
- Rebuild with fixed binutils

* Sun Jul 29 2018 Kalev Lember <klember@redhat.com> - 4.0.92-1
- Update to 4.0.92

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Apr 09 2018 Kalev Lember <klember@redhat.com> - 4.0.0-1
- Update to 4.0.0

* Tue Apr 03 2018 Kalev Lember <klember@redhat.com> - 3.0.93-1
- Update to 3.0.93
- Remove ldconfig scriptlets
- Build with FreeRDP 1.2

* Tue Mar 20 2018 Kalev Lember <klember@redhat.com> - 3.0.92-1
- Update to 3.0.92

* Tue Feb 27 2018 Kalev Lember <klember@redhat.com> - 3.0.91-1
- Update to 3.0.91

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Jan 16 2018 Simone Caronni <negativo17@gmail.com> - 3.0.0-3
- Drop FreeRDP 1.2 requirement, use FreeRDP 2.0.

* Mon Jan 15 2018 Björn Esser <besser82@fedoraproject.org> - 3.0.0-2
- Rebuilt for libva.so.2

* Wed Aug 09 2017 Kalev Lember <klember@redhat.com> - 3.0.0-1
- Update to 3.0.0

* Wed Aug 02 2017 Kalev Lember <klember@redhat.com> - 2.99.93-1
- Update to 2.99.93

* Sun Jul 30 2017 Florian Weimer <fweimer@redhat.com> - 2.99.92-2
- Rebuild with binutils fix for ppc64le (#1475636)

* Wed Jul 26 2017 Kalev Lember <klember@redhat.com> - 2.99.92-1
- Update to 2.99.92

* Wed Jul 19 2017 Kalev Lember <klember@redhat.com> - 2.99.91-1
- Update to 2.99.91

* Thu Jul 13 2017 Adam Jackson <ajax@redhat.com> - 2.0.0-2
- Stop BuildRequiring cairo-gl. We install none of the additional demo clients
  it builds, and it's going away from the cairo package soon.

* Wed Jun 21 2017 Kalev Lember <klember@redhat.com> - 2.0.0-1
- Update to 2.0.0

* Tue Mar 21 2017 Simone Caronni <negativo17@gmail.com> - 1.12.0-6
- Build requirement compat-freerdp12 has been renamed to freerdp1.2.

* Tue Mar 07 2017 Simone Caronni <negativo17@gmail.com> - 1.12.0-5
- Update build requirements, enable RDP again through FreeRDP 1.2 compatibility
  package.

* Sat Mar 04 2017 Rex Dieter <rdieter@fedoraproject.org> - 1.12.0-4
- %%build: --disable-silent-rules
- fix FTBFS: disable broken rpd support (#1424540)
- fix rpaths

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 01 2017 Sandro Mani <manisandro@gmail.com> - 1.12.0-2
- Rebuild (libwebp)

* Wed Sep 21 2016 Kalev Lember <klember@redhat.com> - 1.12.0-1
- Update to 1.12.0

* Wed Sep 14 2016 Kalev Lember <klember@redhat.com> - 1.11.94-1
- Update to 1.11.94

* Thu Sep 08 2016 Kalev Lember <klember@redhat.com> - 1.11.93-1
- Update to 1.11.93

* Wed Aug 31 2016 Kalev Lember <klember@redhat.com> - 1.11.92-1
- Update to 1.11.92
- Don't set group tags

* Wed Aug 17 2016 Kalev Lember <klember@redhat.com> - 1.11.91-2
- Run ldconfig scripts for the new -libs subpackage

* Wed Aug 17 2016 Kalev Lember <klember@redhat.com> - 1.11.91-1
- Update to 1.11.91
- Add a -libs subpackage

* Wed Jun 01 2016 Kalev Lember <klember@redhat.com> - 1.11.0-1
- Update to 1.11.0

* Wed May 25 2016 Kalev Lember <klember@redhat.com> - 1.10.93-1
- Update to 1.10.93

* Wed May 18 2016 Kalev Lember <klember@redhat.com> - 1.10.92-1
- Update to 1.10.92

* Sun May 08 2016 Kalev Lember <klember@redhat.com> - 1.10.91-1
- Update to 1.10.91

* Fri Apr 22 2016 Adam Williamson <awilliam@redhat.com> - 1.10.0-2
- rebuild for changed freerdp sonames

* Thu Feb 18 2016 Kalev Lember <klember@redhat.com> - 1.10.0-1
- Update to 1.10.0

* Thu Feb 04 2016 Kalev Lember <klember@redhat.com> - 1.9.92-1
- Update to 1.9.92

* Mon Dec 28 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 1.9.0-3
- Rebuilt for libwebp soname bump

* Fri Nov 20 2015 Kalev Lember <klember@redhat.com> - 1.9.0-2
- Rebuilt for freerdp soname bump

* Tue Sep 22 2015 Kalev Lember <klember@redhat.com> - 1.9.0-1
- Update to 1.9.0
- Use make_install macro

* Wed Sep 16 2015 Kalev Lember <klember@redhat.com> - 1.8.93-1
- Update to 1.8.93

* Wed Sep 02 2015 Kalev Lember <klember@redhat.com> - 1.8.92-1
- Update to 1.8.92

* Fri Aug 21 2015 Kalev Lember <klember@redhat.com> - 1.8.91-1
- Update to 1.8.91
- Use license macro for COPYING

* Tue Jul 21 2015 Adam Jackson <ajax@redhat.com> 1.8.0-1
- weston 1.8.0

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.92-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue May 26 2015 Adam Jackson <ajax@redhat.com> 1.7.92-1
- weston 1.7.92
- Backport patches to fall back to argb buffer if no xrgb is available

* Tue Mar 10 2015 Peter Hutterer <peter.hutterer@redhat.com> - 1.7.0-2
- Rebuild for libinput soname bump

* Tue Feb 17 2015 Richard Hughes <rhughes@redhat.com> - 1.7.0-1
- Update to 1.7.0

* Fri Jan 16 2015 Peter Hutterer <peter.hutterer@redhat.com> 1.6.0-4
- Update to and require libinput 0.8

* Fri Dec 19 2014 Kevin Fenzi <kevin@scrye.com> 1.6.0-3
- Rebuild for new freerdp

* Sun Sep 21 2014 Kalev Lember <kalevlember@gmail.com> - 1.6.0-2
- Enable webp and vaapi support
- Install weston-launch as setuid root (#1064023)

* Sun Sep 21 2014 Kalev Lember <kalevlember@gmail.com> - 1.6.0-1
- Update to 1.6.0
- Pull in the main package for -devel subpackage

* Fri Sep 12 2014 Peter Hutterer <peter.hutterer@redhat.com> - 1.5.91-2
- Rebuild for libinput soname bump

* Fri Aug 22 2014 Kevin Fenzi <kevin@scrye.com> 1.5.91-1
- Update to 1.5.91

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jul 19 2014 Kevin Fenzi <kevin@scrye.com> 1.5.0-6
- Rebuild for new libfreerdp

* Sun Jun 15 2014 Lubomir Rintel <lkundrak@v3.sk> - 1.5.0-5
- Enable DBus support so that logind integration actually works

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue May 27 2014 Dan Horák <dan[at]danny.cz> - 1.5.0-3
- libunwind available only on selected arches

* Wed May 21 2014 Richard Hughes <rhughes@redhat.com> - 1.5.0-1
- Weston 1.5.0

* Tue May 13 2014 Richard Hughes <rhughes@redhat.com> - 1.4.93-1
- Weston 1.4.93

* Mon Jan 27 2014 Adam Jackson <ajax@redhat.com> 1.4.0-2
- Rebuild for new sonames in libxcb 1.10

* Fri Jan 24 2014 Richard Hughes <rhughes@redhat.com> - 1.4.0-1
- Weston 1.4.0

* Mon Jan 20 2014 Richard Hughes <rhughes@redhat.com> - 1.3.93-1
- Weston 1.3.93

* Tue Dec 17 2013 Richard Hughes <rhughes@redhat.com> - 1.3.91-1
- Weston 1.3.91

* Mon Nov 25 2013 Lubomir Rintel <lkundrak@v3.sk> - 1.3.1-1
- Weston 1.3.1

* Thu Oct 03 2013 Adam Jackson <ajax@redhat.com> 1.2.0-3
- Build RDP backend if we have new enough freerdp (#991220)

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed May 15 2013 Richard Hughes <rhughes@redhat.com> - 1.1.90-0.1.20130515
- Update to a git snapshot based on what will become 1.1.90

* Tue Apr 16 2013 Richard Hughes <richard@hughsie.com> 1.1.0-1
- weston 1.1.0

* Wed Mar 27 2013 Richard Hughes <richard@hughsie.com> 1.0.6-1
- weston 1.0.6

* Thu Feb 21 2013 Adam Jackson <ajax@redhat.com> 1.0.5-1
- weston 1.0.5+ (actually tip of 1.0 branch)

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Jan 21 2013 Adam Tkac <atkac redhat com> - 1.0.3-2
- rebuild due to "jpeg8-ABI" feature drop

* Wed Jan 02 2013 Adam Jackson <ajax@redhat.com> 1.0.3-1
- weston 1.0.3

* Fri Dec 21 2012 Adam Tkac <atkac redhat com> - 1.0.0-2
- rebuild against new libjpeg

* Tue Oct 23 2012 Adam Jackson <ajax@redhat.com> 1.0.0-1
- weston 1.0.0

* Thu Oct 18 2012 Adam Jackson <ajax@redhat.com> 0.99.0-1
- weston 0.99.0

* Mon Sep 17 2012 Thorsten Leemhuis <fedora@leemhuis.info> 0.95.0-3
- add libXcursor-devel as BR

* Mon Sep 17 2012 Thorsten Leemhuis <fedora@leemhuis.info> 0.95.0-2
- rebuild

* Mon Sep 17 2012 Thorsten Leemhuis <fedora@leemhuis.info> 0.95.0-1
- Update to 0.95.0
- enable xwayland
- make it easier to switch between a release and a git snapshot in spec file

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.89-0.5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 05 2012 Adam Jackson <ajax@redhat.com> 0.89-0.4
- Rebuild for new libudev
- Conditional buildreq for libudev-devel

* Wed Apr 25 2012 Richard Hughes <richard@hughsie.com> 0.89-0.3
- New package addressing Fedora package review concerns.

* Tue Apr 24 2012 Richard Hughes <richard@hughsie.com> 0.89-0.2
- Initial package for Fedora package review.
