# X.org requires lazy relocations to work.
%undefine _hardened_build
%undefine _strict_symbol_defs_build

%global stable_abi 1

%if %{stable_abi}
# Released ABI versions. Have to keep these manually in sync with the source.
%global ansic_major 0
%global ansic_minor 4
%global videodrv_major 24
%global videodrv_minor 1
%global xinput_major 24
%global xinput_minor 1
%global extension_major 10
%global extension_minor 0
%endif

%global pkgname xorg-server

Summary:        X.Org X11 X server
Name:           xorg-x11-server
Version:        1.20.10
Release:        4%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://www.x.org
Source0:        https://www.x.org/pub/individual/xserver/%{pkgname}-%{version}.tar.bz2
Source1:        gitignore
Source4:        10-quirks.conf
Source10:       xserver.pamd
# The xvfb-run script is used by other packages to enable ptests on display-less machines.
Source20:  http://svn.exactcode.de/t2/trunk/package/xorg/xorg-server/xvfb-run.sh
# For requires generation in drivers
Source30:       xserver-sdk-abi-requires.release
Source31:       xserver-sdk-abi-requires.git
# Maintainer convenience script
Source40:       driver-abi-rebuild.sh

# From Debian use intel ddx driver only for gen4 and older chipsets
Patch1:         06_use-intel-only-on-pre-gen4.diff
# Default to xf86-video-modesetting on GeForce 8 and newer
Patch2:         0001-xfree86-use-modesetting-driver-by-default-on-GeForce.patch
# Default to va_gl on intel i965 as we use the modesetting drv there
# va_gl should probably just be the default everywhere ?
Patch3:         0001-xf86-dri2-Use-va_gl-as-vdpau_driver-for-Intel-i965-G.patch
# Submitted upstream, but not going anywhere
Patch5:         0001-autobind-GPUs-to-the-screen.patch
# Because the display-managers are not ready yet, do not upstream
Patch6:         0001-Fedora-hack-Make-the-suid-root-wrapper-always-start-.patch
# Backports from current stable "server-1.20-branch":
# <empty>

# Backports from "master" upstream:
Patch7: CVE-2023-1594.patch
Patch8: CVE-2023-6377.patch
Patch9: CVE-2023-6478.patch

# Backported Xwayland randr resolution change emulation support
Patch501:       0001-dix-Add-GetCurrentClient-helper.patch
Patch502:       0002-xwayland-Add-wp_viewport-wayland-extension-support.patch
Patch503:       0003-xwayland-Use-buffer_damage-instead-of-surface-damage.patch
Patch504:       0004-xwayland-Add-fake-output-modes-to-xrandr-output-mode.patch
Patch505:       0005-xwayland-Use-RandR-1.2-interface-rev-2.patch
Patch506:       0006-xwayland-Add-per-client-private-data.patch
Patch507:       0007-xwayland-Add-support-for-storing-per-client-per-outp.patch
Patch508:       0008-xwayland-Add-support-for-randr-resolution-change-emu.patch
Patch509:       0009-xwayland-Add-xwlRRModeToDisplayMode-helper-function.patch
Patch510:       0010-xwayland-Add-xwlVidModeGetCurrentRRMode-helper-to-th.patch
Patch511:       0011-xwayland-Add-vidmode-mode-changing-emulation-support.patch
Patch512:       0012-xwayland-xwl_window_should_enable_viewport-Add-extra.patch
Patch513:       0013-xwayland-Set-_XWAYLAND_RANDR_EMU_MONITOR_RECTS-prope.patch
Patch514:       0014-xwayland-Cache-client-id-for-the-window-manager-clie.patch
Patch515:       0015-xwayland-Reuse-viewport-instead-of-recreating.patch
Patch516:       0016-xwayland-Recurse-on-finding-the-none-wm-owner.patch
Patch517:       0017-xwayland-Make-window_get_none_wm_owner-return-a-Wind.patch
Patch518:       0018-xwayland-Check-emulation-on-client-toplevel-resize.patch
Patch519:       0019-xwayland-Also-check-resolution-change-emulation-when.patch
Patch520:       0020-xwayland-Also-hook-screen-s-MoveWindow-method.patch
Patch521:       0021-xwayland-Fix-emulated-modes-not-being-removed-when-s.patch
Patch522:       0022-xwayland-Call-xwl_window_check_resolution_change_emu.patch
Patch523:       0023-xwayland-Fix-setting-of-_XWAYLAND_RANDR_EMU_MONITOR_.patch
Patch524:       0024-xwayland-Remove-unnecessary-xwl_window_is_toplevel-c.patch
Patch525:       0025-xwayland-Make-window_get_client_toplevel-non-recursi.patch

BuildRequires:  audit-devel
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  bison
BuildRequires:  dbus-devel
BuildRequires:  flex
BuildRequires:  flex-devel
BuildRequires:  git
BuildRequires:  kernel-headers
BuildRequires:  libX11-devel
BuildRequires:  libXau-devel
BuildRequires:  libXdmcp-devel
BuildRequires:  libXext-devel
BuildRequires:  libXfont2-devel
BuildRequires:  libdrm-devel >= 2.4.0
BuildRequires:  libepoxy-devel
BuildRequires:  libfontenc-devel
BuildRequires:  libpciaccess-devel >= 0.13.1
BuildRequires:  libselinux-devel >= 2.0.86-1
BuildRequires:  libtool
BuildRequires:  libxkbfile-devel
BuildRequires:  make
BuildRequires:  mesa-libEGL-devel
BuildRequires:  mesa-libGL-devel >= 9.2
BuildRequires:  mesa-libgbm-devel
BuildRequires:  openssl-devel
BuildRequires:  pixman-devel >= 0.30.0
BuildRequires:  pkg-config
BuildRequires:  systemd-devel
BuildRequires:  systemtap-sdt-devel
BuildRequires:  wayland-devel
BuildRequires:  wayland-protocols-devel
BuildRequires:  xorg-x11-font-utils >= 7.2-11
BuildRequires:  xorg-x11-proto-devel >= 7.7-10
BuildRequires:  xorg-x11-util-macros >= 1.17
BuildRequires:  xorg-x11-xtrans-devel >= 1.3.2
BuildRequires:  pkgconfig(epoxy)
BuildRequires:  pkgconfig(wayland-client) >= 1.3.0
BuildRequires:  pkgconfig(xshmfence) >= 1.1

%description
X.Org X11 X server

%package common
Summary:        Xorg server common files

Requires:       pixman >= 0.30.0
Requires:       xkbcomp
Requires:       xkeyboard-config

%description common
Common files shared among all X servers.

%package Xorg
Summary:        Xorg X server

Requires:       libEGL
Requires:       systemd
Requires:       xorg-x11-drv-libinput
Requires:       xorg-x11-server-common >= %{version}-%{release}

Provides:       Xorg = %{version}-%{release}
Provides:       Xserver = %{version}-%{release}
# HdG: This should be moved to the wrapper package once the wrapper gets
# its own sub-package:
Provides:       xorg-x11-server-wrapper = %{version}-%{release}
Obsoletes:      xorg-x11-glamor < %{version}-%{release}
Provides:       xorg-x11-glamor = %{version}-%{release}
Obsoletes:      xorg-x11-drv-modesetting < %{version}-%{release}
Provides:       xorg-x11-drv-modesetting = %{version}-%{release}
# Dropped from F25
Obsoletes:      xorg-x11-drv-vmmouse < 13.1.0-4
%if %{stable_abi}
Provides:       xserver-abi(ansic-%{ansic_major}) = %{ansic_minor}
Provides:       xserver-abi(videodrv-%{videodrv_major}) = %{videodrv_minor}
Provides:       xserver-abi(xinput-%{xinput_major}) = %{xinput_minor}
Provides:       xserver-abi(extension-%{extension_major}) = %{extension_minor}
%endif

%description Xorg
X.org X11 is an open source implementation of the X Window System.  It
provides the basic low level functionality which full fledged
graphical user interfaces (GUIs) such as GNOME and KDE are designed
upon.

%package Xnest
Summary:        A nested server

Requires:       xorg-x11-server-common >= %{version}-%{release}

Provides:       Xnest = %{version}-%{release}

%description Xnest
Xnest is an X server which has been implemented as an ordinary
X application.  It runs in a window just like other X applications,
but it is an X server itself in which you can run other software.  It
is a very useful tool for developers who wish to test their
applications without running them on their real X server.

%package Xvfb
Summary:        A X Windows System virtual framebuffer X server
# The "xvfb-run.sh" script is GPLv2, rest is MIT.
License:        GPLv2 AND MIT

Requires:       xorg-x11-server-common >= %{version}-%{release}
# Required for "xvfb-run.sh".
Requires:       xorg-x11-xauth

Provides:       Xvfb = %{version}-%{release}

%description Xvfb
Xvfb (X Virtual Frame Buffer) is an X server that is able to run on
machines with no display hardware and no physical input devices.
Xvfb simulates a dumb framebuffer using virtual memory.  Xvfb does
not open any devices, but behaves otherwise as an X display.  Xvfb
is normally used for testing servers.

%package Xwayland
Summary:        Wayland X Server

Requires:       libEGL
Requires:       xorg-x11-server-common >= %{version}-%{release}

%description Xwayland
Xwayland is an X server for running X clients under Wayland.

%package devel
Summary:        SDK for X server driver module development

Requires:       libXfont2-devel
Requires:       libpciaccess-devel
Requires:       pixman-devel
Requires:       pkg-config
Requires:       xorg-x11-proto-devel
Requires:       xorg-x11-util-macros

Provides:       xorg-x11-server-static = %{version}-%{release}
Obsoletes:      xorg-x11-glamor-devel < %{version}-%{release}
Provides:       xorg-x11-glamor-devel = %{version}-%{release}

%description devel
The SDK package provides the developmental files which are necessary for
developing X server driver modules, and for compiling driver modules
outside of the standard X11 source code tree.  Developers writing video
drivers, input drivers, or other X modules should install this package.

%prep
%autosetup -N -n %{pkgname}-%{version}
rm -rf .git
cp %{SOURCE1} .gitignore
# ick
%global __scm git
%{expand:%__scm_setup_git -q}
%autopatch

%if 0%{?stable_abi}
# Check the ABI in the source against what we expect.
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

%endif

%build

%global default_font_path "catalogue:%{_sysconfdir}/X11/fontpath.d,built-ins"

autoreconf -f -v --install || exit 1

%configure \
  --disable-static \
  --disable-systemd-logind \
  --disable-unit-tests \
  --enable-glamor \
  --enable-install-setuid \
  --enable-libunwind=no \
  --enable-suid-wrapper \
  --enable-xnest \
  --enable-xvfb \
  --enable-xwayland \
  --with-builderstring="Build ID: %{name} %{version}-%{release}" \
  --with-default-font-path=%{default_font_path} \
  --with-module-dir=%{_libdir}/xorg/modules \
  --with-pic \
  --with-os-name="$(hostname -s) $(uname -r)" \
  --with-vendor-name="%{vendor}" \
  --with-xkb-output=%{_localstatedir}/lib/xkb \
  --without-dtrace \
  ${CONFIGURE}

make V=1 %{?_smp_mflags}


%install
%make_install

mkdir -p %{buildroot}%{_libdir}/xorg/modules/{drivers,input}

mkdir -p %{buildroot}%{_sysconfdir}/pam.d
install -m 644 %{SOURCE10} %{buildroot}%{_sysconfdir}/pam.d/xserver

mkdir -p %{buildroot}%{_datadir}/X11/xorg.conf.d
install -m 644 %{SOURCE4} %{buildroot}%{_datadir}/X11/xorg.conf.d

install -m 0755 %{SOURCE20} $RPM_BUILD_ROOT%{_bindir}/xvfb-run

# Make sure the (empty) /etc/X11/xorg.conf.d is there, system-setup-keyboard
# relies on it more or less.
mkdir -p %{buildroot}%{_sysconfdir}/X11/xorg.conf.d

install -m 755 %{SOURCE30} %{buildroot}%{_bindir}/xserver-sdk-abi-requires

# Remove unwanted files/dirs
{
find %{buildroot} -type f -name "*.la" -delete -print
}


%files common
%license COPYING
%{_mandir}/man1/Xserver.1*
%{_libdir}/xorg/protocol.txt
%dir %{_localstatedir}/lib/xkb
%{_localstatedir}/lib/xkb/README.compiled

%files Xorg
%config %attr(0644,root,root) %{_sysconfdir}/pam.d/xserver
%{_bindir}/X
%{_bindir}/Xorg
%{_libexecdir}/Xorg
%attr(4755, root, root) %{_libexecdir}/Xorg.wrap
%{_bindir}/cvt
%{_bindir}/gtf
%dir %{_libdir}/xorg
%dir %{_libdir}/xorg/modules
%dir %{_libdir}/xorg/modules/drivers
%{_libdir}/xorg/modules/drivers/modesetting_drv.so
%dir %{_libdir}/xorg/modules/extensions
%{_libdir}/xorg/modules/extensions/libglx.so
%dir %{_libdir}/xorg/modules/input
%{_libdir}/xorg/modules/libfbdevhw.so
%{_libdir}/xorg/modules/libexa.so
%{_libdir}/xorg/modules/libfb.so
%{_libdir}/xorg/modules/libglamoregl.so
%{_libdir}/xorg/modules/libshadow.so
%{_libdir}/xorg/modules/libshadowfb.so
%{_libdir}/xorg/modules/libvgahw.so
%{_libdir}/xorg/modules/libwfb.so
%ifarch %{arm} %{ix86} aarch64 x86_64
%{_libdir}/xorg/modules/libint10.so
%{_libdir}/xorg/modules/libvbe.so
%endif
%{_mandir}/man1/gtf.1*
%{_mandir}/man1/Xorg.1*
%{_mandir}/man1/Xorg.wrap.1*
%{_mandir}/man1/cvt.1*
%{_mandir}/man4/fbdevhw.4*
%{_mandir}/man4/exa.4*
%{_mandir}/man4/modesetting.4*
%{_mandir}/man5/Xwrapper.config.5*
%{_mandir}/man5/xorg.conf.5*
%{_mandir}/man5/xorg.conf.d.5*
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

%files Xwayland
%{_bindir}/Xwayland

%files devel
%license COPYING
%{_bindir}/xserver-sdk-abi-requires
%{_libdir}/pkgconfig/xorg-server.pc
%dir %{_includedir}/xorg
%{_includedir}/xorg/*.h
%{_datadir}/aclocal/xorg-server.m4

%changelog
* Fri Aug 11 2023 Sean Dougherty <sdougherty@microsoft.com> - 1.20.10-4
- Add patch for CVE-2023-1594

* Fri Nov 05 2021 Muhammad Falak <mwani@microsft.com> - 0.13.0.7-4
- Remove epoch from xorg-x11-font-utils

* Tue Jan 05 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.20.10-2
- Initial CBL-Mariner import from Fedora 33 (license: MIT).
- License verified.
- Changed BuildRequires for "audit-libs-devel" to "audit-devel".
- Made 'libint10.so' and 'libvbe.so' be packaged for ARM architectures as well.
- Removed dependency on "libunwind".
- Removed following subpackages: source, Xdmx, Xephyr.
- Removed using the set of "redhat-hardened-*" compiler and linker specs.
- Replacing 'Requires' on 'system-setup-keyboard' with 'systemd'.

* Wed Dec  2 2020 Olivier Fourdan <ofourdan@redhat.com> - 1.20.10-1
- xserver 1.20.10 (CVE-2020-14360, CVE-2020-25712)

* Thu Nov  5 10:35:09 AEST 2020 Peter Hutterer <peter.hutterer@redhat.com> - 1.20.9-3
- Add BuildRequires for make

* Wed Nov 04 2020 Peter Hutterer <peter.hutterer@redhat.com> 1.20.9-2
- Drop BuildRequires to git-core only

* Thu Oct  8 2020 Olivier Fourdan <ofourdan@redhat.com> - 1.20.9-1
- xserver 1.20.9 + all current fixes from upstream

* Wed Aug 12 2020 Adam Jackson <ajax@redhat.com> - 1.20.8-4
- Enable XC-SECURITY

* Fri Jul 31 2020 Adam Jackson <ajax@redhat.com> - 1.20.8-3
- Fix information disclosure bug in pixmap allocation (CVE-2020-14347)

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.20.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Mar 30 2020 Olivier Fourdan <ofourdan@redhat.com> - 1.20.8-1
- xserver 1.20.8
- Backport latest Xwayland randr resolution change emulation support
  patches.

* Wed Mar 18 2020 Olivier Fourdan <ofourdan@redhat.com> - 1.20.7-2
- Fix a crash on closing a window using Present found upstream:
  https://gitlab.freedesktop.org/xorg/xserver/issues/1000

* Fri Mar 13 2020 Olivier Fourdan <ofourdan@redhat.com> - 1.20.7-1
- xserver 1.20.7
- backport from stable "xserver-1.20-branch" up to commit ad7364d8d
  (for mutter fullscreen unredirect on Wayland)
- Update videodrv minor ABI as 1.20.7 changed the minor ABI version
  (backward compatible, API addition in glamor)
- Rebase Xwayland randr resolution change emulation support patches

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.20.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Nov 25 2019 Olivier Fourdan <ofourdan@redhat.com> - 1.20.6-1
- xserver 1.20.6

* Mon Nov  4 2019 Hans de Goede <hdegoede@redhat.com> - 1.20.5-9
- Fix building with new libglvnd-1.2.0 (E)GL headers and pkgconfig files

* Mon Nov  4 2019 Hans de Goede <hdegoede@redhat.com> - 1.20.5-8
- Backport Xwayland randr resolution change emulation support

* Thu Aug 29 2019 Olivier Fourdan <ofourdan@redhat.com> 1.20.5-7
- Pick latest fixes from xserver stable branch upstream (rhbz#1729925)

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.20.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Jul  8 2019 Olivier Fourdan <ofourdan@redhat.com> 1.20.5-5
- Do not include <sys/io.h> on ARM with glibc to avoid compilation failure.
- Do not force vbe and int10 sdk headers as this enables int10 which does
  not build on ARM without <sys/io.h>

* Mon Jul  8 2019 Olivier Fourdan <ofourdan@redhat.com> 1.20.5-4
- Fix regression causing screen tearing with upstream xserver 1.20.5
  (rhbz#1726419)

* Fri Jun 28 2019 Olivier Fourdan <ofourdan@redhat.com> 1.20.5-3
- Remove atomic downstream patches causing regressions (#1714981, #1723715)
- Xwayland crashes (#1708119, #1691745)
- Cursor issue with tablet on Xwayland
- Xorg/modesetting issue with flipping pixmaps with Present (#1645553)

* Thu Jun 06 2019 Peter Hutterer <peter.hutterer@redhat.com> 1.20.5-2
- Return AlreadyGrabbed for keycodes > 255 (#1697804)

* Thu May 30 2019 Adam Jackson <ajax@redhat.com> - 1.20.5-1
- xserver 1.20.5

* Tue Apr 23 2019 Adam Jackson <ajax@redhat.com> - 1.20.4-4
- Fix some non-atomic modesetting calls to be atomic

* Wed Mar 27 2019 Peter Hutterer <peter.hutterer@redhat.com> 1.20.4-3
- Fix a Qt scrolling bug, don't reset the valuator on slave switch

* Thu Mar 21 2019 Adam Jackson <ajax@redhat.com> - 1.20.4-2
- Backport an Xwayland crash fix in the Present code

* Tue Feb 26 2019 Adam Jackson <ajax@redhat.com> - 1.20.4-1
- xserver 1.20.4

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.20.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jan 11 2019 Olivier Fourdan <ofourdan@redhat.com> - 1.20.3-3
- More Xwayland/Present fixes from upstream (rhbz#1609181, rhbz#1661748)

* Thu Dec 06 2018 Olivier Fourdan <ofourdan@redhat.com> - 1.20.3-2
- Xwayland/Present fixes from master upstream

* Thu Nov 01 2018 Adam Jackson <ajax@redhat.com> - 1.20.3-1
- xserver 1.20.3

* Mon Oct 15 2018 Adam Jackson <ajax@redhat.com> - 1.20.2-1
- xserver 1.20.2

* Thu Oct  4 2018 Hans de Goede <hdegoede@redhat.com> - 1.20.1-4
- Rebase patch to use va_gl as vdpau driver on i965 GPUs, re-fix rhbz#1413733

* Thu Sep 13 2018 Dave Airlie <airlied@redhat.com> - 1.20.1-3
- Build with PIE enabled (this doesn't enable bind now)

* Mon Sep 10 2018 Olivier Fourdan <ofourdan@redhat.com> - 1.20.1-2
- Include patches from upstream to fix Xwayland crashes

* Thu Aug 09 2018 Adam Jackson <ajax@redhat.com> - 1.20.1-1
- xserver 1.20.1

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.20.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 12 2018 Adam Jackson <ajax@redhat.com> - 1.20.0-4
- Xorg and Xwayland Requires: libEGL

* Fri Jun 01 2018 Adam Williamson <awilliam@redhat.com> - 1.20.0-3
- Backport fixes for RHBZ#1579067

* Wed May 16 2018 Adam Jackson <ajax@redhat.com> - 1.20.0-2
- Xorg Requires: xorg-x11-drv-libinput

* Thu May 10 2018 Adam Jackson <ajax@redhat.com> - 1.20.0-1
- xserver 1.20

* Wed Apr 25 2018 Adam Jackson <ajax@redhat.com> - 1.19.99.905-2
- Fix xvfb-run's default depth to be 24

* Tue Apr 24 2018 Adam Jackson <ajax@redhat.com> - 1.19.99.905-1
- xserver 1.20 RC5

* Thu Apr 12 2018 Olivier Fourdan <ofourdan@redhat.com> - 1.19.99.904-2
- Re-fix "use type instead of which in xvfb-run (rhbz#1443357)" which
  was overridden inadvertently

* Tue Apr 10 2018 Adam Jackson <ajax@redhat.com> - 1.19.99.904-1
- xserver 1.20 RC4

* Mon Apr 02 2018 Adam Jackson <ajax@redhat.com> - 1.19.99.903-1
- xserver 1.20 RC3

* Tue Feb 13 2018 Olivier Fourdan <ofourdan@redhat.com> 1.19.6-5
- xwayland: avoid race condition on new keymap
- xwayland: Keep separate variables for pointer and tablet foci (rhbz#1519961)
- xvfb-run now support command line option “--auto-display”

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.19.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Jan 30 2018 Olivier Fourdan <ofourdan@redhat.com> 1.19.6-3
- Avoid generating a core file when the Wayland compositor is gone.

* Thu Jan 11 2018 Peter Hutterer <peter.hutterer@redhat.com> 1.19.6-2
- Fix handling of devices with ID_INPUT=null

* Wed Dec 20 2017 Adam Jackson <ajax@redhat.com> - 1.19.6-1
- xserver 1.19.6

* Thu Oct 12 2017 Adam Jackson <ajax@redhat.com> - 1.19.5-1
- xserver 1.19.5

* Thu Oct 05 2017 Olivier Fourdan <ofourdan@redhat.com> - 1.19.4-1
- xserver-1.19.4
- Backport tablet support for Xwayland

* Fri Sep 08 2017 Troy Dawson <tdawson@redhat.com> - 1.19.3-9
- Cleanup spec file conditionals

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.19.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.19.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jul  2 2017 Ville Skyttä <ville.skytta@iki.fi> - 1.19.3-6
- Use type instead of which in xvfb-run (rhbz#1443357)

* Thu May 04 2017 Orion Poplawski <orion@cora.nwra.com> - 1.19.3-5
- Enable full build for s390/x

* Mon Apr 24 2017 Ben Skeggs <bskeggs@redhat.com> - 1.19.3-4
- Default to xf86-video-modesetting on GeForce 8 and newer

* Fri Apr 07 2017 Adam Jackson <ajax@redhat.com> - 1.19.3-3
- Inoculate against a versioning bug with libdrm 2.4.78

* Thu Mar 23 2017 Hans de Goede <hdegoede@redhat.com> - 1.19.3-2
- Use va_gl as vdpau driver on i965 GPUs (rhbz#1413733)

* Wed Mar 15 2017 Adam Jackson <ajax@redhat.com> - 1.19.3-1
- xserver 1.19.3

* Thu Mar 02 2017 Adam Jackson <ajax@redhat.com> - 1.19.2-1
- xserver 1.19.2

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.19.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 01 2017 Peter Hutterer <peter.hutterer@redhat.com> 1.19.1-3
- Fix a few input thread lock issues causing intel crashes (#1384486)

* Mon Jan 16 2017 Adam Jackson <ajax@redhat.com> - 1.19.1-2
- Limit the intel driver only on F26 and up

* Wed Jan 11 2017 Adam Jackson <ajax@redhat.com> - 1.19.1-1
- xserver 1.19.1

* Tue Jan 10 2017 Hans de Goede <hdegoede@redhat.com> - 1.19.0-4
- Follow Debian and only default to the intel ddx on gen4 or older intel GPUs

* Tue Dec 20 2016 Hans de Goede <hdegoede@redhat.com> - 1.19.0-3
- Add one more patch for better integration with the nvidia binary driver

* Thu Dec 15 2016 Hans de Goede <hdegoede@redhat.com> - 1.19.0-2
- Add some patches for better integration with the nvidia binary driver
- Add a patch from upstream fixing a crash (rhbz#1389886)

* Wed Nov 23 2016 Olivier Fourdan <ofourdan@redhat.com> 1.19.0-1
- xserver 1.19.0
- Fix use after free of cursors in Xwayland (rhbz#1385258)
- Fix an issue where some monitors would show only black, or
  partially black when secondary GPU outputs are used

* Tue Nov 15 2016 Peter Hutterer <peter.hutterer@redhat.com> 1.19.0-0.8.rc2
- Update device barriers for new master devices (#1384432)

* Thu Nov  3 2016 Hans de Goede <hdegoede@redhat.com> - 1.19.0-0.7.rc2
- Update to 1.19.0-rc2
- Fix (hopefully) various crashes in FlushAllOutput() (rhbz#1382444)
- Fix Xwayland crashing in glamor on non glamor capable hw (rhbz#1390018)

* Tue Nov  1 2016 Ben Crocker <bcrocker@redhat.com> - 1.19.0-0.6.20161028
- Fix Config record allocation during startup: if xorg.conf.d directory
- was absent, a segfault resulted.

* Mon Oct 31 2016 Adam Jackson <ajax@redhat.com> - 1.19.0-0.5.20161026
- Use %%autopatch instead of doing our own custom git-am trick

* Fri Oct 28 2016 Hans de Goede <hdegoede@redhat.com> - 1.19.0-0.4.20161026
- Add missing Requires: libXfont2-devel to -devel sub-package (rhbz#1389711)

* Wed Oct 26 2016 Hans de Goede <hdegoede@redhat.com> - 1.19.0-0.3.20161026
- Sync with upstream git, bringing in a bunch if bug-fixes
- Add some extra fixes which are pending upstream
- This also adds PointerWarping emulation to Xwayland, which should improve
  compatiblity with many games
