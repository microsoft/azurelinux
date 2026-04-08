# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# X.org requires lazy relocations to work.
%undefine _hardened_build
%undefine _strict_symbol_defs_build

# Released ABI versions:
%global ansic_major 0
%global ansic_minor 4
%global videodrv_major 25
%global videodrv_minor 2
%global xinput_major 24
%global xinput_minor 4
%global extension_major 10
%global extension_minor 0

%global pkgname xorg-server

Summary:    X.Org X11 X server
Name:       xorg-x11-server
Version:    21.1.21
Release:    1%{?dist}
URL:        http://www.x.org
# SPDX
License:    Adobe-Display-PostScript AND BSD-3-Clause AND DEC-3-Clause AND HPND AND HPND-sell-MIT-disclaimer-xserver AND HPND-sell-variant AND ICU AND ISC AND MIT AND MIT-open-group AND NTP AND SGI-B-2.0 AND SMLNJ AND X11 AND X11-distribute-modifications-variant

Source0:    https://www.x.org/pub/individual/xserver/%{pkgname}-%{version}.tar.xz

Source10:   xserver.pamd
# "useful" xvfb-run script
Source20:   http://svn.exactcode.de/t2/trunk/package/xorg/xorg-server/xvfb-run.sh
# for requires generation in drivers
Source30:   xserver-sdk-abi-requires
# maintainer convenience script
Source40:   driver-abi-rebuild.sh

# From Debian use intel ddx driver only for gen4 and older chipsets
Patch0:     06_use-intel-only-on-pre-gen4.diff
# Default to xf86-video-modesetting on GeForce 8 and newer
Patch1:     0001-xfree86-use-modesetting-driver-by-default-on-GeForce.patch
# Default to va_gl on intel i965 as we use the modesetting drv there
# va_gl should probably just be the default everywhere ?
Patch2:     0001-xf86-dri2-Use-va_gl-as-vdpau_driver-for-Intel-i965-G.patch
# because the display-managers are not ready yet, do not upstream
Patch3:     0001-Fedora-hack-Make-the-suid-root-wrapper-always-start-.patch

BuildRequires:  bison
BuildRequires:  flex
BuildRequires:  gawk
BuildRequires:  gcc
BuildRequires:  kernel-headers
BuildRequires:  libXi-devel
BuildRequires:  libXinerama-devel
BuildRequires:  libXres-devel
BuildRequires:  libXv-devel
BuildRequires:  make
BuildRequires:  mesa-libEGL-devel
BuildRequires:  mesa-libGL-devel >= 9.2
BuildRequires:  meson
BuildRequires:  pkgconfig
BuildRequires:  pkgconfig(audit)
BuildRequires:  pkgconfig(bigreqsproto) >= 1.1.0
BuildRequires:  pkgconfig(compositeproto) >= 0.4
BuildRequires:  pkgconfig(damageproto) >= 1.1
BuildRequires:  pkgconfig(dbus-1) >= 1.0
BuildRequires:  pkgconfig(dri2proto) >= 2.8
BuildRequires:  pkgconfig(dri3proto) >= 1.2
BuildRequires:  pkgconfig(epoxy)
BuildRequires:  pkgconfig(epoxy) >= 1.5.4
BuildRequires:  pkgconfig(fixesproto) >= 6.0
BuildRequires:  pkgconfig(fontsproto) >= 2.1.3
BuildRequires:  pkgconfig(gbm) >= 10.2
BuildRequires:  pkgconfig(inputproto) >= 2.3.99.1
BuildRequires:  pkgconfig(kbproto) >= 1.0.3
BuildRequires:  pkgconfig(libdrm) >= 2.4.89
BuildRequires:  pkgconfig(libselinux) >= 2.0.86
BuildRequires:  pkgconfig(libsystemd) >= 209
BuildRequires:  pkgconfig(libudev) >= 143
BuildRequires:  pkgconfig(libunwind)
BuildRequires:  pkgconfig(libxcvt)
BuildRequires:  pkgconfig(openssl)
BuildRequires:  pkgconfig(pciaccess) >= 0.12.901
BuildRequires:  pkgconfig(pixman-1)
BuildRequires:  pkgconfig(randrproto) >= 1.6.0
BuildRequires:  pkgconfig(recordproto) >= 1.13.99.1
BuildRequires:  pkgconfig(renderproto) >= 0.11
BuildRequires:  pkgconfig(resourceproto) >= 1.2.0
BuildRequires:  pkgconfig(scrnsaverproto) >= 1.1
BuildRequires:  pkgconfig(videoproto)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(x11-xcb)
BuildRequires:  pkgconfig(xau)
BuildRequires:  pkgconfig(xcb-aux)
BuildRequires:  pkgconfig(xcb-icccm)
BuildRequires:  pkgconfig(xcb-image)
BuildRequires:  pkgconfig(xcb-keysyms)
BuildRequires:  pkgconfig(xcb-renderutil)
BuildRequires:  pkgconfig(xcmiscproto) >= 1.2.0
BuildRequires:  pkgconfig(xdmcp)
BuildRequires:  pkgconfig(xext) >= 1.0.99.4
BuildRequires:  pkgconfig(xextproto) >= 7.2.99.901
BuildRequires:  pkgconfig(xf86bigfontproto) >= 1.2.0
BuildRequires:  pkgconfig(xf86vidmodeproto) >= 2.2.99.1
BuildRequires:  pkgconfig(xfont2) >= 2.0
BuildRequires:  pkgconfig(xineramaproto)
BuildRequires:  pkgconfig(xkbfile)
BuildRequires:  pkgconfig(xproto) >= 7.0.31
BuildRequires:  pkgconfig(xshmfence) >= 1.1
BuildRequires:  pkgconfig(xtrans) >= 1.3.5
BuildRequires:  pkgconfig(xtrans) >= 1.3.5
BuildRequires:  systemtap-sdt-devel
BuildRequires:  xorg-x11-util-macros >= 1.17
BuildRequires:  xorg-x11-xtrans-devel >= 1.3.2

%description
X.Org X11 X server.


%package        common
Summary:        Xorg server common files
Requires:       pixman
Requires:       xkbcomp
Requires:       xkeyboard-config

%description    common
Common files shared among all X servers.


%package        Xorg
Summary:        Xorg X server
Requires:       libEGL
Requires:       system-setup-keyboard
Requires:       xorg-x11-drv-libinput
Requires:       xorg-x11-server-common >= %{version}-%{release}
Provides:       Xorg = %{version}-%{release}
Provides:       Xserver
# HdG: This should be moved to the wrapper package once the wrapper gets
# its own sub-package:
Provides:       xorg-x11-server-wrapper = %{version}-%{release}
Provides:       xserver-abi(ansic-%{ansic_major}) = %{ansic_minor}
Provides:       xserver-abi(videodrv-%{videodrv_major}) = %{videodrv_minor}
Provides:       xserver-abi(xinput-%{xinput_major}) = %{xinput_minor}
Provides:       xserver-abi(extension-%{extension_major}) = %{extension_minor}
# Dropped from xorg-x11-server-21.1
# https://gitlab.freedesktop.org/xorg/xserver/-/commit/b3b81c8c2090cd49410960a021baf0d27fdd2ab3
Obsoletes:      xorg-x11-server-Xdmx < 1.20.15
# Legacy fbdev devices have been replaced with simpledrm:
# https://fedoraproject.org/wiki/Changes/ReplaceFbdevDrivers
Obsoletes:      xorg-x11-drv-fbdev < 0.5.0-19
Obsoletes:      xorg-x11-drv-vesa < 2.6.0-3
Obsoletes:      xorg-x11-drv-armsoc < 1.4.1-10

%description    Xorg
X.org X11 is an open source implementation of the X Window System. It provides
the basic low level functionality which full fledged graphical user interfaces
(GUIs) such as GNOME and KDE are designed upon.


%package        Xnest
Summary:        A nested server
Requires:       xorg-x11-server-common >= %{version}-%{release}
Provides:       Xnest

%description    Xnest
Xnest is an X server which has been implemented as an ordinary X application. It
runs in a window just like other X applications, but it is an X server itself in
which you can run other software. It is a very useful tool for developers who
wish to test their applications without running them on their real X server.


%package        Xvfb
Summary:        A X Windows System virtual framebuffer X server
# xvfb-run is GPLv2, rest is MIT
License:        MIT and GPL-2.0-only
Requires:       xorg-x11-server-common >= %{version}-%{release}
# required for xvfb-run
Requires:       xorg-x11-xauth
Provides:       Xvfb
Requires:       util-linux

%description    Xvfb
Xvfb (X Virtual Frame Buffer) is an X server that is able to run on machines
with no display hardware and no physical input devices. Xvfb simulates a dumb
framebuffer using virtual memory. Xvfb does not open any devices, but behaves
otherwise as an X display. Xvfb is normally used for testing servers.


%package        Xephyr
Summary:        A nested server
Requires:       xorg-x11-server-common >= %{version}-%{release}
Provides:       Xephyr

%description    Xephyr
Xephyr is an X server which has been implemented as an ordinary X application.
It runs in a window just like other X applications, but it is an X server itself
in which you can run other software. It is a very useful tool for developers who
wish to test their applications without running them on their real X server.
Unlike Xnest, Xephyr renders to an X image rather than relaying the X protocol,
and therefore supports the newer X extensions like Render and Composite.


%package        devel
Summary:        SDK for X server driver module development
Requires:       libpciaccess-devel
Requires:       libXfont2-devel
Requires:       xorg-x11-proto-devel
Requires:       xorg-x11-util-macros
Requires:       pixman-devel
Requires:       pkgconfig
Provides:       xorg-x11-server-static

%description devel
The SDK package provides the developmental files which are necessary for
developing X server driver modules, and for compiling driver modules outside of
the standard X11 source code tree. Developers writing video drivers, input
drivers, or other X modules should install this package.


%package        source
Summary:        Xserver source code required to build VNC server (Xvnc)
BuildArch:      noarch

%description        source
Xserver source code needed to build VNC server (Xvnc).


%prep
%autosetup -p1 -n %{pkgname}-%{version}

# check the ABI in the source against what we expect.
getmajor() {
    grep -i ^#define.ABI.$1_VERSION hw/xfree86/common/xf86Module.h |
    tr '(),' '   ' | awk '{ print $4 }'
}

getminor() {
    grep -i ^#define.ABI.$1_VERSION hw/xfree86/common/xf86Module.h |
    tr '(),' '   ' | awk '{ print $5 }'
}

test `getmajor ansic` == %{ansic_major}
test `getminor ansic` == %{ansic_minor}
test `getmajor videodrv` == %{videodrv_major}
test `getminor videodrv` == %{videodrv_minor}
test `getmajor xinput` == %{xinput_major}
test `getminor xinput` == %{xinput_minor}
test `getmajor extension` == %{extension_major}
test `getminor extension` == %{extension_minor}

%build
%meson \
    -D agp=auto \
    -D builder_string="Build ID: %{name} %{version}-%{release}" \
    -D default_font_path="catalogue:/etc/X11/fontpath.d,built-ins" \
    -D devel-docs=false \
    -D dga=true \
    -D docs-pdf=false \
    -D docs=false \
    -D dpms=true \
    -D dri1=false \
    -D dri2=true \
    -D dri3=true \
    -D drm=true \
    -D dtrace=false \
    -D fallback_input_driver=libinput \
    -D glamor=true \
    -D glx=true \
    -D hal=false \
    -D input_thread=true \
    -D int10=false \
    -D ipv6=true \
    -D libunwind=true \
    -D linux_acpi=false \
    -D linux_apm=false \
    -D listen_local=true \
    -D listen_tcp=false \
    -D listen_unix=true \
    -D log_dir="%{_localstatedir}/log" \
    -D mitshm=auto \
    -D module_dir="%{_libdir}/xorg/modules" \
    -D pciaccess=true \
    -D screensaver=true \
    -D secure-rpc=false \
    -D sha1=libcrypto \
    -D suid_wrapper=true \
    -D systemd_logind=true \
    -D udev_kms=true \
    -D udev=true \
    -D vgahw=true \
    -D xace=true \
    -D xcsecurity=true \
    -D xdm-auth-1=true \
    -D xdmcp=true \
    -D xephyr=true \
    -D xf86bigfont=false \
    -D xf86-input-inputtest=true \
    -D xinerama=true \
    -D xkb_output_dir="%{_localstatedir}/lib/xkb" \
    -D xnest=true \
    -D xorg=true \
    -D xpbproxy=false \
    -D xquartz=false \
    -D xres=true \
    -D xselinux=true \
    -D xvfb=true \
    -D xvmc=true \
    -D xv=true \
    -D xwin=false

%meson_build

%install
%meson_install

install -D -m 0644 -p xkb/README.compiled %{buildroot}%{_localstatedir}/lib/xkb/README.compiled
install -D -m 0644 %{SOURCE10} %{buildroot}%{_sysconfdir}/pam.d/xserver

# make sure the (empty) /etc/X11/xorg.conf.d is there, system-setup-keyboard
# relies on it more or less.
mkdir -p %{buildroot}%{_sysconfdir}/X11/xorg.conf.d

install -D -m 0755 %{SOURCE30} %{buildroot}%{_bindir}/xserver-sdk-abi-requires
install -D -m 0755 %{SOURCE20} %{buildroot}%{_bindir}/xvfb-run

# Make the source package
%global xserver_source_dir %{_datadir}/xorg-x11-server-source
%global inst_srcdir %{buildroot}/%{xserver_source_dir}

mkdir -p %{inst_srcdir}/{Xext,xkb,GL,hw/{xquartz/bundle,xfree86/common}}
mkdir -p %{inst_srcdir}/{hw/dmx/doc,man,doc,hw/dmx/doxygen}
cp {,%{inst_srcdir}/}hw/xquartz/bundle/cpprules.in
cp {,%{inst_srcdir}/}man/Xserver.man
cp {,%{inst_srcdir}/}doc/smartsched
#cp {,%{inst_srcdir}/}hw/dmx/doxygen/doxygen.conf.in
cp {,%{inst_srcdir}/}xserver.ent.in
cp {,%{inst_srcdir}/}hw/xfree86/Xorg.sh.in
cp xkb/README.compiled %{inst_srcdir}/xkb
cp hw/xfree86/xorgconf.cpp %{inst_srcdir}/hw/xfree86

find . -type f -not -path "./%{_vpath_builddir}/*" | egrep '.*\.(c|h|am|ac|inc|m4|h.in|pc.in|man.pre|pl|txt)$' |
xargs tar cf - | (cd %{inst_srcdir} && tar xf -)
find %{inst_srcdir}/hw/xfree86 -name \*.c -delete

# Remove unwanted files/dirs
find %{buildroot} -type f -name '*.la' -delete


%files common
%doc COPYING
%{_mandir}/man1/Xserver.1*
%{_libdir}/xorg/protocol.txt
%dir %{_localstatedir}/lib/xkb
%{_localstatedir}/lib/xkb/README.compiled

%files Xorg
%config %attr(0644,root,root) %{_sysconfdir}/pam.d/xserver
%{_bindir}/gtf
%{_bindir}/X
%{_bindir}/Xorg
%{_libexecdir}/Xorg
# Disable until module loading is audited
# %attr(0711,root,root) %caps(cap_sys_admin,cap_sys_rawio,cap_dac_override=pe)
%attr(4755, root, root) %{_libexecdir}/Xorg.wrap
%dir %{_libdir}/xorg
%dir %{_libdir}/xorg/modules
%dir %{_libdir}/xorg/modules/drivers
%{_libdir}/xorg/modules/drivers/modesetting_drv.so
%dir %{_libdir}/xorg/modules/extensions
%{_libdir}/xorg/modules/extensions/libglx.so
%dir %{_libdir}/xorg/modules/input
%{_libdir}/xorg/modules/input/inputtest_drv.so
%{_libdir}/xorg/modules/libexa.so
%{_libdir}/xorg/modules/libfbdevhw.so
#%%{_libdir}/xorg/modules/libfb.so
%{_libdir}/xorg/modules/libglamoregl.so
%{_libdir}/xorg/modules/libshadow.so
%{_libdir}/xorg/modules/libshadowfb.so
%{_libdir}/xorg/modules/libvgahw.so
%{_libdir}/xorg/modules/libwfb.so
%{_mandir}/man1/gtf.1*
%{_mandir}/man1/Xorg.1*
%{_mandir}/man1/Xorg.wrap.1*
%{_mandir}/man4/exa.4*
%{_mandir}/man4/fbdevhw.4*
%{_mandir}/man4/inputtestdrv.4*
%{_mandir}/man4/modesetting.4*
%{_mandir}/man5/xorg.conf.5*
%{_mandir}/man5/xorg.conf.d.5*
%{_mandir}/man5/Xwrapper.config.5*
%dir %{_sysconfdir}/X11/xorg.conf.d
%dir %{_datadir}/X11/xorg.conf.d
%{_datadir}/X11/xorg.conf.d/10-quirks.conf

%files Xnest
%{_bindir}/Xnest
%{_mandir}/man1/Xnest.1*

%files Xvfb
%{_bindir}/Xvfb
%{_bindir}/xvfb-run
%{_mandir}/man1/Xvfb.1*

%files Xephyr
%{_bindir}/Xephyr
%{_mandir}/man1/Xephyr.1*

%files devel
%doc COPYING
%{_bindir}/xserver-sdk-abi-requires
%{_libdir}/pkgconfig/xorg-server.pc
%dir %{_includedir}/xorg
%{_includedir}/xorg/*.h
%{_datadir}/aclocal/xorg-server.m4

%files source
%{xserver_source_dir}


%changelog
* Tue Nov 25 2025 Olivier Fourdan <ofourdan@redhat.com> - 21.1.21-1
- Update to xserver 21.1.21 (#2417000)

* Tue Oct 28 2025 Olivier Fourdan <ofourdan@redhat.com> - 21.1.20-1
- Update to xserver 21.1.20 (#2406803)
- CVE fix for: CVE-2025-62229, CVE-2025-62230, CVE-2025-62231

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 21.1.18-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Wed Jul 09 2025 Peter Hutterer <peter.hutterer@redhat.com>
- Update Xvfb SPDX license identifier

* Wed Jun 18 2025 Olivier Fourdan <ofourdan@redhat.com> - 21.1.18-1
- Update to xserver 21.1.18
- Contains an additional fix for CVE-2025-49176

* Tue Jun 17 2025 Olivier Fourdan <ofourdan@redhat.com> - 21.1.17-1
- Update to xserver 21.1.17
- CVE fix for: CVE-2025-49175, CVE-2025-49176, CVE-2025-49177
               CVE-2025-49178, CVE-2025-49179, CVE-2025-49180

* Wed Feb 26 2025 Olivier Fourdan <ofourdan@redhat.com> - 21.1.16-1
- Update to xserver 21.1.16 (#2347558)
- CVE fix for: CVE-2025-26594, CVE-2025-26595, CVE-2025-26596, CVE-2025-26597,
               CVE-2025-26598, CVE-2025-26599, CVE-2025-26600, CVE-2025-26601

* Tue Feb 25 2025 Olivier Fourdan <ofourdan@redhat.com> - 21.1.15-3
- Fix DRI2 failure (#2347345)

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 21.1.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Dec 20 2024 José Expósito <jexposit@redhat.com> - 21.1.15-1
- Update to v21.1.15

* Fri Nov 29 2024 Sérgio Basto <sergio@serjux.com> - 21.1.14-3
- Revert commit "Fix error copying Xorg.wrap", debugedit-5.1-2 have the real fix

* Mon Nov 18 2024 José Expósito <jexposit@redhat.com> - 21.1.14-2
- Fix build issues caused by Xorg.wrap
- Restore quirks for Apple silicon
  Fixes: 422064e45a42 ("Update X11-server to 21.1.13 and ABI numbers of videodrv and xinput")
  Resolves: https://bugzilla.redhat.com/show_bug.cgi?id=2326701

* Tue Oct 29 2024 José Expósito <jexposit@redhat.com> - 21.1.14-1
- Update to v21.1.14

* Wed Oct 16 2024 Peter Robinson <pbrobinson@fedoraproject.org>
- Obsolete xorg-x11-drv-armsoc

* Mon Sep 30 2024 Simone Caronni <negativo17@gmail.com> - 21.1.13-5
- After removal of int10/vbe, obsolete vesa and fbdev X drivers:
  https://fedoraproject.org/wiki/Changes/ReplaceFbdevDrivers

* Sat Sep 28 2024 Simone Caronni <negativo17@gmail.com> - 21.1.13-4
- Remove all conditionals. Drop int10 everywhere and enable libunwind/dri3 on
  ELN.

* Fri Sep 27 2024 Simone Caronni <negativo17@gmail.com> - 21.1.13-3
- Switch to meson, drop no longer required patch.
- Drop Obsoletes/Provides that have been removed in ~2014.
- Add build depdendencies as they are searched by meson.
- Format SPEC file.

* Thu Sep 26 2024 Simone Caronni <negativo17@gmail.com> - 21.1.13-2
- Drop support for building snapshots. If they need to be built, there are
  anyway more simpler ways.
- Trim changelog.
- Drop custom compileri/linker flags that are part of the standard already.

* Mon Sep 02 2024 Sérgio Basto <sergio@serjux.com> - 21.1.13-1
- Update X11-server to 21.1.13 and ABI numbers of videodrv and xinput
- DMX DDX was dropped
- 0001-Disallow-byte-swapped-clients-by-default.patch is upstreamed
- 0001-autobind-GPUs-to-the-screen.patch is upstreamed
- 0001-xf86-dri2-Use-va_gl-as-vdpau_driver-for-Intel-i965-G.patch updated

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.20.14-37
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Apr 10 2024 José Expósito <jexposit@redhat.com> - 1.20.14-35
- Backport fix for invalid Unicode sequence

* Wed Apr 10 2024 José Expósito <jexposit@redhat.com> - 1.20.14-35
- Fix regression caused by the fix for CVE-2024-31083

* Wed Apr 03 2024 José Expósito <jexposit@redhat.com> - 1.20.14-34
- CVE fix for: CVE-2024-31080, CVE-2024-31081, CVE-2024-31082 and
  CVE-2024-31083

* Mon Mar 04 2024 José Expósito <jexposit@redhat.com> - 1.20.14-33
- Add util-linux as a dependency of Xvfb

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.20.14-32
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 José Expósito <jexposit@redhat.com> - 1.20.14-31
- Fix compilation error on i686

* Fri Jan 19 2024 José Expósito <jexposit@redhat.com> - 1.20.14-30
- Fix use after free related to CVE-2024-21886

* Tue Jan 16 2024 José Expósito <jexposit@redhat.com> - 1.20.14-29
- CVE fix for: CVE-2023-6816, CVE-2024-0229, CVE-2024-21885, CVE-2024-21886,
  CVE-2024-0408 and CVE-2024-0409

* Wed Dec 13 2023 Peter Hutterer <peter.hutterer@redhat.com> - 1.20.14-28
- CVE fix for: CVE-2023-6377, CVE-2023-6478

* Fri Nov 10 2023 Peter Hutterer <peter.hutterer@redhat.com> - 1.20.14-27
- Update with full SPDX license list

* Wed Oct 25 2023 Peter Hutterer <peter.hutterer@redhat.com> - 1.20.14-26
- CVE fix for: CVE-2023-5367, CVE-2023-5380

* Fri Oct 20 2023 José Expósito <jexposit@redhat.com>
- SPDX migration: license is already SPDX compatible

* Fri Sep 29 2023 Orion Poplawski <orion@nwra.com> - 1.20.14-25
- Fix xvfb-run --error-file / auth-file options

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.20.14-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Apr 25 2023 Olivier Fourdan <ofourdan@redhat.com> - 1.20.14-23
- Backport fix for a deadlock with DRI3 (#2189434)

* Thu Apr 13 2023 Florian Weimer <fweimer@redhat.com> - 1.20.14-22
- Make more functions available in fb.h with !FB_ACCESS_WRAPPER

* Wed Mar 29 2023 Olivier Fourdan <ofourdan@redhat.com> - 1.20.14-21
- CVE fix for: CVE-2023-1393

* Thu Feb 23 2023 Olivier Fourdan <ofourdan@redhat.com> - 1.20.14-20
- Fix xvfb-run script with --listen-tcp

* Thu Feb 09 2023 Iker Pedrosa <ipedrosa@redhat.com> - 1.20.14-19
- Remove pam_console from service file (#1822209)

* Thu Feb 02 2023 Peter Hutterer <peter.hutterer@redhat.com> - 1.20.14-18
- CVE-2023-0494: potential use-after-free

* Wed Feb 01 2023 Peter Hutterer <peter.hutterer@redhat.com> - 1.20.14-17
- Updated conditional fedora statement

* Tue Jan 17 2023 Olivier Fourdan <ofourdan@redhat.com> - 1.20.14-16
- Use the recommended way to apply conditional patches without
  conditionalizing the sources (for byte-swapped clients).

* Fri Jan 13 2023 Leif Liddy <leifliddy@fedoraproject.org> 1.20.14-15
- Xorg server does not correctly select the DCP for the display
  without a quirk on Apple silicon machines (#2152414)

* Fri Jan 13 2023 Peter Hutterer <peter.hutterer@redhat.com> - 1.20.14-14
- Disallow byte-swapped clients (#2159489)

* Wed Jan 11 2023 Olivier Fourdan <ofourdan@redhat.com> - 1.20.14-13
- Rename boolean config value field from bool to boolean to fix drivers
  build failures due to a conflict with C++ and stdbool.h

* Mon Dec 19 2022 Peter Hutterer <peter.hutterer@redhat.com> - 1.20.14-12
- Fix buggy patch to CVE-2022-46340

* Wed Dec 14 2022 Peter Hutterer <peter.hutterer@redhat.com> 1.20.14-11
- CVE fix for: CVE-2022-4283, CVE-2022-46340, CVE-2022-46341,
  CVE-2022-46342, CVE-2022-46343, CVE-2022-46344

* Wed Nov 23 2022 Peter Hutterer <peter.hutterer@redhat.com> - 1.20.14-10
- Drop dependency on xorg-x11-font-utils, it was only there for on
  build-time variable that's always the same value anyway (#2145088)

* Tue Nov  8 2022 Olivier Fourdan <ofourdan@redhat.com> - 1.20.14-9
- Fix CVE-2022-3550, CVE-2022-3551

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.20.14-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue Jul 12 2022 Olivier Fourdan <ofourdan@redhat.com> - 1.20.14-7
- Fix CVE-2022-2319/ZDI-CAN-16062, CVE-2022-2320/ZDI-CAN-16070

* Wed Apr 13 2022 Dominik Mierzejewski <rpm@greysector.net> - 1.20.14-6
- Don't hardcode fps for fake screen (#2054188)

* Fri Apr 8 2022 Jocelyn Falempe <jfalempe@redhat.com> - 1.20.14-5
- Fix basic graphic mode not working with simpledrm (#2067151)

* Fri Jan 28 2022 Olivier Fourdan <ofourdan@redhat.com> - 1.20.14-4
- Fix build with GCC 12 (#2047134)

* Tue Jan 25 2022 Olivier Fourdan <ofourdan@redhat.com> - 1.20.14-3
- Fix crash with NVIDIA proprietary driver with Present (#2046147)

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.20.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild
