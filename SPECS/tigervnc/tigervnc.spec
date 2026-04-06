# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

#defining macros needed by SELinux
%global selinuxtype targeted
%global modulename vncsession

%bcond ffmpeg %[0%{?fedora} || 0%{?epel} || 0%{?eln}]
%bcond xserver %[!(0%{?rhel} >= 10)]

Name:           tigervnc
Version:        1.16.0
Release:        2%{?dist}
Summary:        A TigerVNC remote display system

%global _hardened_build 1

License:        GPL-2.0-or-later
URL:            http://www.tigervnc.com

Source0:        https://github.com/TigerVNC/%{name}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:        xvnc.service
Source2:        xvnc.socket
Source3:        10-libvnc.conf
Source4:        HOWTO.md

# Backwards compatibility
Source5:        vncserver

# Downstream patches
Patch1:         tigervnc-vncsession-restore-script-systemd-service.patch

%if 0%{?fedora} >= 42 || 0%{?rhel} >= 11
# https://fedoraproject.org/wiki/Changes/Unify_bin_and_sbin
Patch2:         tigervnc-sbin-bin-merge.patch
%endif

# Upstream patches

BuildRequires:  make
BuildRequires:  gcc-c++
BuildRequires:  gettext
BuildRequires:  cmake

BuildRequires:  gnutls-devel
BuildRequires:  desktop-file-utils
BuildRequires:  libappstream-glib
BuildRequires:  libjpeg-turbo-devel
BuildRequires:  openssl-devel
BuildRequires:  pam-devel
BuildRequires:  zlib-devel

# TigerVNC 1.4.x requires fltk 1.3.3 for keyboard handling support
# See https://github.com/TigerVNC/tigervnc/issues/8, also bug #1208814
%if 0%{?fedora} >= 44 || 0%{?rhel} >= 11
BuildRequires:  fltk1.3-devel
%else
BuildRequires:  fltk-devel
%endif
BuildRequires:  libxcvt-devel
BuildRequires:  libX11-devel
BuildRequires:  libXext-devel
BuildRequires:  libXi-devel
BuildRequires:  libXrandr-devel
BuildRequires:  libXrender-devel
BuildRequires:  pixman-devel

%if 0%{?fedora} || 0%{?epel} || 0%{?eln}
# Icons
BuildRequires:  ImageMagick
%endif


%if %{with xserver}
# X11/graphics dependencies
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gettext-autopoint
BuildRequires:  libXdamage-devel
BuildRequires:  libXdmcp-devel
BuildRequires:  libXfixes-devel
BuildRequires:  libXfont2-devel
BuildRequires:  libXinerama-devel
BuildRequires:  libXt-devel
BuildRequires:  libXtst-devel
BuildRequires:  libdrm-devel
BuildRequires:  mesa-libgbm-devel
BuildRequires:  libtool
BuildRequires:  libxkbfile-devel
BuildRequires:  libxshmfence-devel
BuildRequires:  mesa-libGL-devel
BuildRequires:  pkgconfig(fontutil)
BuildRequires:  pkgconfig(xkbcomp)
BuildRequires:  xorg-x11-server-devel
BuildRequires:  xorg-x11-server-source
BuildRequires:  xorg-x11-util-macros
BuildRequires:  xorg-x11-xtrans-devel
%endif

%if %{with ffmpeg}
# Codecs
BuildRequires:  pkgconfig(libavcodec)
BuildRequires:  pkgconfig(libavutil)
BuildRequires:  pkgconfig(libswscale)
%endif

# SELinux
BuildRequires:  libselinux-devel
BuildRequires:  selinux-policy-devel
BuildRequires:  systemd

# Wayland
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(gobject-2.0)
BuildRequires:  pkgconfig(libpipewire-0.3)
BuildRequires:  pkgconfig(uuid)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(xkbcommon)

Requires(post): coreutils
Requires(postun):coreutils

Requires:       hicolor-icon-theme
Requires:       tigervnc-license
Requires:       tigervnc-icons
Requires:       which

%description
Virtual Network Computing (VNC) is a remote display system which
allows you to view a computing 'desktop' environment not only on the
machine where it is running, but from anywhere on the Internet and
from a wide variety of machine architectures.  This package contains a
client which will allow you to connect to other desktops running a VNC
server.

%package x11-server
Summary:        A TigerVNC server for X11
Requires:       perl-interpreter
Requires:       tigervnc-server-common = %{version}-%{release}
Requires:       (%{name}-selinux if selinux-policy-%{selinuxtype})
Requires:       xorg-x11-xauth
Requires:       xorg-x11-xinit
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
Obsoletes:      tigervnc-server < %{version}-%{release}
Provides:       tigervnc-server = %{version}-%{release}
Obsoletes:      tigervnc-server-minimal < %{version}-%{release}
Provides:       tigervnc-server-minimal = %{version}-%{release}

%description x11-server
The VNC system allows you to access the same desktop from a wide
variety of platforms.  This package includes set of utilities
which make usage of TigerVNC X11 server more user friendly. It also
contains x0vncserver program which can export your active
X session.

%package wayland-server
Summary:        A TigerVNC server for Wayland compositors
Requires:       tigervnc-server-common = %{version}-%{release}
Requires:       (%{name}-selinux if selinux-policy-%{selinuxtype})

%description wayland-server
TigerVNC server which makes a Wayland compositor that is based on
wlroots, or has the RemoteDesktop portal implemented, remotely
accessible via VNC, TigerVNC or compatible viewers. It does not create
a virtual display, instead, it shares an existing display (typically,
that one connected to the physical screen).


%package server-common
Summary:        Common tools for TigerVNC servers
Requires:       dbus-x11
Requires:       mesa-dri-drivers
Requires:       tigervnc-license
Requires:       xkbcomp
Requires:       xkeyboard-config

%description server-common
Common tools used by both X11 and Wayland TigerVNC servers,
including vncpasswd for password management and vncconfig for
server configuration.

%package x11-server-module
Summary:        TigerVNC module to Xorg
Requires:       xorg-x11-server-Xorg %(xserver-sdk-abi-requires ansic) %(xserver-sdk-abi-requires videodrv)
Requires:       tigervnc-license
Obsoletes:      tigervnc-server-module < %{version}-%{release}
Provides:       tigervnc-server-module = %{version}-%{release}

%description x11-server-module
This package contains libvnc.so module to X server, allowing others
to access the desktop on your machine.

%package license
Summary:        License of TigerVNC suite
BuildArch:      noarch

%description license
This package contains license of the TigerVNC suite

%package icons
Summary:        Icons for TigerVNC viewer
BuildArch:      noarch

%description icons
This package contains icons for TigerVNC viewer

%package selinux
Summary:        SELinux module for TigerVNC
BuildArch:      noarch
BuildRequires:  selinux-policy-devel
Requires:       selinux-policy-%{selinuxtype}
Requires(post): selinux-policy-%{selinuxtype}
BuildRequires:  selinux-policy-devel
%{?selinux_requires}

%description selinux
This package provides the SELinux policy module to ensure TigerVNC
runs properly under an environment with SELinux enabled.

%prep
%setup -q

%patch -P1 -p1 -b .vncsession-restore-script-systemd-service

%if 0%{?fedora} >= 42 || 0%{?rhel} >= 11
%patch -P2 -p1 -b .sbin-bin-merge
%endif

# Upstream patches

%if %{with xserver}
cp -r /usr/share/xorg-x11-server-source/* unix/xserver
pushd unix/xserver
for all in `find . -type f -perm -001`; do
        chmod -x "$all"
done
# EPEL 10 possibly too in the future
%if 0%{?fedora} && 0%{?fedora} > 40
cat ../xserver21.patch | patch -p1
%else
cat ../xserver120.patch | patch -p1
%endif
popd
%else
sed -i -r '/add_subdirectory.(|x0)vncserver/d' unix/CMakeLists.txt
%endif

# Downstream patches

%build
# TODO: Please submit an issue to upstream (rhbz#2381485)
export CMAKE_POLICY_VERSION_MINIMUM=3.5
%ifarch sparcv9 sparc64 s390 s390x
export CFLAGS="$RPM_OPT_FLAGS -fPIC"
%else
export CFLAGS="$RPM_OPT_FLAGS -fpic"
%endif
export CXXFLAGS="$CFLAGS -std=c++11"

%if 0%{?fedora} >= 35 || 0%{?rhel} >= 10
%define __cmake_builddir %{_target_platform}

mkdir -p %{__cmake_builddir}
%endif

%cmake -DCMAKE_INSTALL_UNITDIR=%{_unitdir}

%cmake_build

%if %{with xserver}
pushd unix/xserver

autoreconf -fiv
%configure \
        --disable-xorg --disable-xnest --disable-xvfb --disable-dmx \
        --disable-xwin --disable-xephyr --disable-kdrive --disable-xwayland \
        --with-pic --disable-static \
        --with-default-font-path="catalogue:/etc/X11/fontpath.d,built-ins" \
        --with-xkb-output=%{_localstatedir}/lib/xkb \
        --enable-glx --disable-dri --enable-dri2 --enable-dri3 \
        --disable-unit-tests \
        --disable-config-hal \
        --disable-config-udev \
        --without-dtrace \
        --disable-devel-docs \
        --disable-selective-werror

make TIGERVNC_BUILDDIR="`pwd`/../../%{__cmake_builddir}" %{?_smp_mflags}
popd
%endif

# SELinux
pushd unix/vncserver/selinux
make
popd

%if 0%{?rhel}
# Build icons
%if 0%{?rhel} >= 9
pushd %{_target_platform}/media
%else
pushd media
%endif
make
popd
%endif



%install
%cmake_install
rm -f %{buildroot}%{_docdir}/%{name}-%{version}/{README.rst,LICENCE.TXT}

%if %{with xserver}
pushd unix/xserver/hw/vnc
%make_install TIGERVNC_BUILDDIR="`pwd`/../../../../%{__cmake_builddir}"
popd

# Install systemd unit file
install -m644 %{SOURCE1} %{buildroot}%{_unitdir}/xvnc@.service
install -m644 %{SOURCE2} %{buildroot}%{_unitdir}/xvnc.socket
install -m755 %{SOURCE5} %{buildroot}/%{_bindir}/vncserver
%endif

# Install selinux policy file
pushd unix/vncserver/selinux
make install DESTDIR=%{buildroot} PREFIX=%{_prefix}
popd

# Install desktop stuff
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/{16x16,24x24,48x48}/apps

pushd media/icons
for s in 16 22 24 32 48 64 128; do
install -m644 tigervnc_$s.png %{buildroot}%{_datadir}/icons/hicolor/${s}x$s/apps/tigervnc.png
done
popd

appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/org.tigervnc.vncviewer.metainfo.xml
desktop-file-validate %{buildroot}%{_datadir}/applications/vncviewer.desktop

%find_lang %{name} %{name}.lang

%if %{with xserver}
# remove unwanted files
rm -f  %{buildroot}%{_libdir}/xorg/modules/extensions/libvnc.la

mkdir -p %{buildroot}%{_sysconfdir}/X11/xorg.conf.d/
install -m 644 %{SOURCE3} %{buildroot}%{_sysconfdir}/X11/xorg.conf.d/10-libvnc.conf

install -m 644 %{SOURCE4} %{buildroot}/%{_docdir}/tigervnc/HOWTO.md

%post x11-server
%systemd_post xvnc@.service
%systemd_post xvnc.socket

%preun x11-server
%systemd_preun xvnc@.service
%systemd_preun xvnc.socket

%postun x11-server
%systemd_postun xvnc@.service
%systemd_postun xvnc.socket
%endif

%pre selinux
%selinux_relabel_pre -s %{selinuxtype}

%post selinux
%selinux_modules_install -s %{selinuxtype} %{_datadir}/selinux/packages/%{selinuxtype}/%{modulename}.pp.bz2
%selinux_relabel_post -s %{selinuxtype}

%postun selinux
if [ $1 -eq 0 ]; then
    %selinux_modules_uninstall -s %{selinuxtype} %{modulename}
    %selinux_relabel_post -s %{selinuxtype}
fi


%files -f %{name}.lang
%doc README.rst
%{_bindir}/vncviewer
%{_datadir}/applications/*
%{_mandir}/man1/vncviewer.1*
%{_datadir}/metainfo/org.tigervnc.vncviewer.metainfo.xml

%if %{with xserver}
%files x11-server
%config(noreplace) %{_sysconfdir}/pam.d/tigervnc
%config(noreplace) %{_sysconfdir}/tigervnc/vncserver-config-defaults
%config(noreplace) %{_sysconfdir}/tigervnc/vncserver-config-mandatory
%config(noreplace) %{_sysconfdir}/tigervnc/vncserver.users
%{_unitdir}/vncserver@.service
%{_unitdir}/xvnc@.service
%{_unitdir}/xvnc.socket
%{_bindir}/vncserver
%{_bindir}/x0vncserver
%{_bindir}/Xvnc
%if 0%{?fedora} >= 42 || 0%{?rhel} >= 11
%{_bindir}/vncsession
%else
%{_sbindir}/vncsession
%endif
%{_libexecdir}/vncserver
%{_libexecdir}/vncsession-start
%{_libexecdir}/vncsession-restore
%{_mandir}/man1/x0vncserver.1*
%{_mandir}/man1/Xvnc.1*
%{_mandir}/man8/vncserver.8*
%{_mandir}/man8/vncsession.8*
%{_docdir}/tigervnc/HOWTO.md

%files x11-server-module
%{_libdir}/xorg/modules/extensions/libvnc.so
%config(noreplace) %{_sysconfdir}/X11/xorg.conf.d/10-libvnc.conf
%endif

%files server-common
%{_bindir}/vncconfig
%{_bindir}/vncpasswd
%{_mandir}/man1/vncpasswd.1*
%{_mandir}/man1/vncconfig.1*

%files wayland-server
%{_bindir}/w0vncserver
%{_bindir}/w0vncserver-forget
%{_mandir}/man1/w0vncserver.1*
%{_mandir}/man1/w0vncserver-forget.1*

%files selinux
%{_datadir}/selinux/packages/%{selinuxtype}/%{modulename}.pp.*
%ghost %verify(not md5 size mtime) %{_sharedstatedir}/selinux/%{selinuxtype}/active/modules/200/%{modulename}

%files license
%{_docdir}/tigervnc/LICENCE.TXT

%files icons
%{_datadir}/icons/hicolor/*/apps/*

%changelog
* Tue Feb 10 2026 Jan Grulich <jgrulich@redhat.com> - 1.16.0-2
- Move obsoletes/provides for tigervnc-server-minimal to tigervnc-server-x11

* Tue Jan 27 2026 Jan Grulich <jgrulich@redhat.com> - 1.16.0-1
- 1.16.0

* Fri Jan 23 2026 Jan Grulich <jgrulich@redhat.com> - 1.15.90-1
- 1.15.90
  Split to tigervnc-x11-server and tigervnc-wayland-server

* Sat Jan 17 2026 Fedora Release Engineering <releng@fedoraproject.org> - 1.15.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Wed Jan 14 2026 Jan Grulich <jgrulich@redhat.com> - 1.15.0-11
- Use fltk1.3 compat package on F44+

* Mon Nov 24 2025 Jan Grulich <jgrulich@redhat.com> - 1.15.0-10
- Rebuild (xorg-x11-server)
  Fixes: CVE-2025-62229 CVE-2025-62230 CVE-2025-62231

* Tue Nov 11 2025 Cristian Le <git@lecris.dev> - 1.15.0-9
- Allow to build with CMake 4.0 (rhbz#2381485)

* Wed Oct 15 2025 Dominik Mierzejewski <dominik@greysector.net> - 1.15.0-8
- Rebuilt for FFmpeg 8

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.15.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jun 23 2025 Jan Grulich <jgrulich@redhat.com> - 1.15.0-6
- Rebuild (xorg-x11-server)
  Fixes: CVE-2025-49175 / CVE-2025-49176 / CVE-2025-49177
         CVE-2025-49178 / CVE-2025-49179 / CVE-2025-49180

* Tue Apr 08 2025 Jan Grulich <jgrulich@redhat.com> - 1.15.0-5
- Fix inetd mode not working (rhbz#2357952)

* Wed Apr 02 2025 Jan Grulich <jgrulich@redhat.com> - 1.15.0-4
- Rebuild (fltk)

* Mon Mar 31 2025 Jan Grulich <jgrulich@redhat.com> - 1.15.0-3
- Backport upstream fix for fullscreen option in vncviewer

* Mon Mar 03 2025 Jan Grulich <jgrulich@redhat.com> - 1.15.0-2
- Rebuild (xorg-x11-server)
  Fixes CVE-2025-26594, CVE-2025-26595, CVE-2025-26596, CVE-2025-26597,
        CVE-2025-26598, CVE-2025-26599, CVE-2025-26600, CVE-2025-26601

* Tue Feb 18 2025 Jan Grulich <jgrulich@redhat.com> - 1.15.0-1
- 1.15.0

* Tue Jan 21 2025 Jan Grulich <jgrulich@redhat.com> - 1.14.1-5
- Adjust paths for vncsession binary for /sbin and /bin merge

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.14.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Dec 19 2024 Jan Grulich <jgrulich@redhat.com> - 1.14.1-3
- Add runtime dependency on which

* Wed Oct 30 2024 Jan Grulich <jgrulich@redhat.com> - 1.14.1-2
- Rebuild (xorg-x11-server)
  Fixes CVE-2024-9632

* Wed Oct 23 2024 Jan Grulich <jgrulich@redhat.com> - 1.14.1-1
- 1.14.1

* Sat Oct 05 2024 Neal Gompa <ngompa@fedoraproject.org> - 1.14.0-8
- Rebuild for ffmpeg 7

* Sun Sep 29 2024 Sérgio Basto <sergio@serjux.com> - 1.14.0-7
- Enable ffmpeg

* Fri Sep 27 2024 Sérgio Basto <sergio@serjux.com> - 1.14.0-6
- Rebuild for rebase of xorg-server to versions 21.1.x

* Fri Sep 27 2024 Sérgio Basto <sergio@serjux.com> - 1.14.0-5
- Add compability with X11-server-21.1.x

* Wed Sep 04 2024 Jan Grulich <jgrulich@redhat.com> - 1.14.0-4
- Move old log to log.old if present (fix patch)

* Mon Sep 02 2024 Jan Grulich <jgrulich@redhat.com> - 1.14.0-3
- Correctly handle ZRLE cursors
- Move old log to log.old if present
- Handle existing config directory in vncpasswd

* Mon Aug 05 2024 Jan Grulich <jgrulich@redhat.com> - 1.14.0-2
- vncsession: use /bin/sh if the user shell is not set
- add missing comma in default security type list

* Tue Jul 23 2024 Jan Grulich <jgrulich@redhat.com> - 1.14.0-1
- 1.14.0

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.13.90-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jul 08 2024 Jan Grulich <jgrulich@redhat.com> - 1.13.90-2
- Enable DRI3 support

* Tue Jul 02 2024 Jan Grulich <jgrulich@redhat.com> - 1.13.90-1
- 1.14.0 beta

* Wed Apr 10 2024 Jan Grulich <jgrulich@redhat.com> - 1.13.1-14
- Rebuild (xorg-x11-server)
  Fix regression caused by the fix for CVE-2024-31083

* Thu Apr 04 2024 Jan Grulich <jgrulich@redhat.com> - 1.13.1-13
- Rebuild (xorg-x11-server)
  CVE fix for: CVE-2024-31080, CVE-2024-31081, CVE-2024-31082 and CVE-2024-31083

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.13.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Jan 16 2024 Jan Grulich <jgrulich@redhat.com> - 1.13.1-11
- Rebuild (xorg-x11-server)
  CVE fix for: CVE-2023-6816, CVE-2024-0229, CVE-2024-21885, CVE-2024-21886,
  CVE-2024-0408 and CVE-2024-0409

* Wed Dec 20 2023 Peter Hutterer <peter.hutterer@redhat.com> - 1.13.1-10
- Fix cmake builddir creation

* Wed Dec 13 2023 Jan Grulich <jgrulich@redhat.com> - 1.13.1-9
- Rebuild for Xorg CVEs
  Fixes: CVE-2023-6377, CVE-2023-6478

* Wed Nov 22 2023 Florian Weimer <fweimer@redhat.com> - 1.13.1-8
- Drop incorrect tigervnc-c99-2.patch.

* Wed Nov 22 2023 Florian Weimer <fweimer@redhat.com> - 1.13.1-7
- C compatibility fixes

* Thu Nov 02 2023 Jan Grulich <jgrulich@redhat.com> - 1.13.1-6
- Fix CVE-2023-5380 and CVE-2023-5367 (rebuild with fixed Xorg)

* Wed Oct 18 2023 Kalev Lember <klember@redhat.com> - 1.13.1-5
- Drop unrecognized configure options
- Add buildrequires to get correct font and xkb directories from pkg-config
- Re-enable server in flatpak builds and fix the build

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.13.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Mar 30 2023 Jan Grulich <jgrulich@redhat.com> - 1.13.1-3
- Drop BR: xorg-x11-font-utils
  CVE-2023-1393

* Thu Mar 30 2023 Jan Grulich <jgrulich@redhat.com> - 1.13.1-2
- Rebuild (xorg-x11-server)
  CVE-2023-1393

* Wed Mar 01 2023 Jan Grulich <jgrulich@redhat.com> - 1.13.1-1
- 1.13.1

* Tue Feb 21 2023 Jan Grulich <jgrulich@redhat.com> - 1.13.0-3
- vncsession: allow to create .vnc directory

* Wed Feb 15 2023 Jan Grulich <jgrulich@redhat.com> - 1.13.0-2
- Backport: Sanity check when cleaning up keymap changes

* Tue Feb 07 2023 Jan Grulich <jgrulich@redhat.com> - 1.13.0-1
- 1.13.0
- CVE-2023-0494

* Tue Jan 31 2023 Jan Grulich <jgrulich@redhat.com> - 1.12.0-9
- migrated to SPDX license

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue May 31 2022 Jan Grulich <jgrulich@redhat.com> - 1.12.0-6
- Add some missing build requirements for x0vncserver

* Tue Feb 15 2022 Jan Grulich <jgrulich@redhat.com> - 1.12.0-5
- Fix migration of SELinux context policy

* Fri Jan 21 2022 Jan Grulich <jgrulich@redhat.com> - 1.12.0-4
- Fix crash in vncviewer

* Fri Jan 14 2022 Jan Grulich <jgrulich@redhat.com> - 1.12.0-3
- Remove unavailable option from vncserver script

* Fri Jan 14 2022 Jan Grulich <jgrulich@redhat.com> - 1.12.0-2
- SELinux: restore SELinux context in case of different policies

* Thu Nov 11 2021 Jan Grulich <jgrulich@redhat.com> - 1.12.0-1
- 1.12.0

* Wed Sep 15 2021 Jan Grulich <jgrulich@redhat.com> - 1.11.90-1
- 1.11.90

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.11.0-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jul 21 2021 Jan Grulich <jgrulich@redhat.com> - 1.11.0-13
- Sync upstream patches + drop unused patches
- Fix logout issue with vncserver script

* Wed Jun 16 2021 Jan Grulich <jgrulich@redhat.com> - 1.11.0-12
- Re-enable vncserver script for F34+

* Tue May 25 2021 Jan Grulich <jgrulich@redhat.com> - 1.11.0-11
- SELinux improvements
- Backport some CentOS changes

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.11.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Dec 10 07:45:46 CET 2020 Jan Grulich <jgrulich@redhat.com> - 1.11.0-9
- vncserver: ignore new session parameter from the new systemd support

* Fri Nov 13 14:08:29 CET 2020 Jan Grulich <jgrulich@redhat.com> - 1.11.0-8
- Use /run instead of /var/run which is just a symlink

* Thu Nov 05 2020 Peter Hutterer <peter.hutterer@redhat.com> 1.11.0-7
- Require xkbcomp directly, not xorg-x11-xkb-utils. The latter has had
  Provides xkbcomp for years.

* Tue Sep 29 13:12:22 CEST 2020 Jan Grulich <jgrulich@redhat.com> - 1.11.0-6
- Backport upstream fix allowing Tigervnc to specify boolean valus in configuration
- Revert removal of vncserver for F32 and F33

* Thu Sep 24 07:14:06 CEST 2020 Jan Grulich <jgrulich@redhat.com> - 1.11.0-5
- Actually install the HOWTO.md file

* Wed Sep 23 2020 Jan Grulich <jgrulich@redhat.com> - 1.11.0-4
- Call systemd macros on correct service file

* Tue Sep 22 2020 Jan Grulich <jgrulich@redhat.com> - 1.11.0-3
- Do not overwrite libvnc.conf config file

* Thu Sep 17 2020 Jan Grulich <jgrulich@redhat.com> - 1.11.0-2
- Add /usr/bin/vncserver file informing users to read the HOWTO.md file

* Wed Sep 09 2020 Jan Grulich <jgrulich@redhat.com> - 1.11.0-1
- 1.11.0

* Mon Aug 24 2020 Jan Grulich <jgrulich@redhat.com. - 1.10.90-1
- Update to 1.10.90 (1.11.0 beta)

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.1-9
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 14 2020 Tom Stellard <tstellar@redhat.com> - 1.10.1-7
- Use make macros
- https://fedoraproject.org/wiki/Changes/UseMakeBuildInstallMacro

* Sat Jul 11 2020 Jiri Vanek <jvanek@redhat.com> - 1.10.1-6
- Rebuilt for JDK-11, see https://fedoraproject.org/wiki/Changes/Java11

* Sun Apr 19 2020 Jan Grulich <jgrulich@redhat.com> - 1.10.1-5
- Requires: dbus-x11
  Resolves: bz#1825331

* Fri Mar 13 2020 Olivier Fourdan <ofourdan@redhat.com> - 1.10.1-4
- Fix build with xserver 1.20.7

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Jan 13 2020 Jan Grulich <jgrulich@redhat.com> - 1.10.1-2
- Build with -std=c++11

* Fri Dec 20 2019 Jan Grulich <jgrulich@redhat.com> - 1.10.1-1
- Update to 1.10.1

* Tue Dec 10 2019 Jan Grulich <jgrulich@redhat.com> - 1.10.0-2
- Properly install systemd files

* Mon Nov 18 2019 Jan Grulich <jgrulich@redhat.com> - 1.10.0-1
- Update to 1.10.0

* Fri Oct 18 2019 Jan Grulich <jgrulich@redhat.com> - 1.9.90-1
- Update to 1.9.90 (1.10 beta)
- Add systemd user service file
- Use a wrapper for systemd system service file to workaround systemd limitations

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Jul 19 2019 Dan Horák <dan[at]danny.cz> - 1.9.0-6
- drop the s390x special handling (related #1727029)

* Wed Jun 12 2019 Jan Grulich <jgrulich@redhat.com> - 1.9.0-5
- Add missing arguments to systemd_postun scriptlets
  Resolves: bz#1716411

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Sep 25 2018 Jan Grulich <jgrulich@redhat.com> - 1.9.0-3
- Do not crash passwd when using malloc perturb checks
  Resolves: bz#1631483

* Wed Aug 01 2018 Jan Grulich <jgrulich@redhat.com> - 1.9.0-2
- Ignore buttons in mouse leave events
  Resolves: bz#1609516

* Tue Jul 17 2018 Jan Grulich <jgrulich@redhat.com> - 1.9.0-1
- Update to 1.9.0

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.90-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jul  4 2018 Peter Robinson <pbrobinson@fedoraproject.org> 1.8.90-2
- Clean up spec: use macros consistenly, drop old sys-v migrations
- Drop ancient obsolete/provides

* Thu Jun 14 2018 Jan Grulich <jgrulich@redhat.com> - 1.8.90-1
- Update to 1.8.90

* Wed Jun 13 2018 Jan Grulich <jgrulich@redhat.com> - 1.8.0-10
- Fix tigervnc systemd unit file
  Resolves: bz#1583159

* Wed Jun 06 2018 Adam Jackson <ajax@redhat.com> - 1.8.0-9
- Fix GLX initialization with 1.20

* Wed Apr 04 2018 Adam Jackson <ajax@redhat.com> - 1.8.0-8
- Rebuild for xserver 1.20

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jan 18 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.8.0-6
- Remove obsolete scriptlets

* Fri Dec 15 2017 Jan Grulich <jgrulich@redhat.com> - 1.8.0-5
- Properly initialize tigervnc when started as systemd service

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Jul 13 2017 Petr Pisar <ppisar@redhat.com> - 1.8.0-2
- perl dependency renamed to perl-interpreter
  <https://fedoraproject.org/wiki/Changes/perl_Package_to_Install_Core_Modules>

* Wed May 17 2017 Jan Grulich <jgrulich@redhat.com> - 1.8.0-1
- Update to 1.8.0

* Thu Apr 20 2017 Jan Grulich <jgrulich@redhat.com> - 1.7.90-1
- Update to 1.7.90 (beta)

* Thu Apr 06 2017 Jan Grulich <jgrulich@redhat.com> - 1.7.1-4
- Added systemd unit file for xvnc
  Resolves: bz#891802

* Tue Apr 04 2017 Jan Grulich <jgrulich@redhat.com> - 1.7.1-3
- Bug 1438704 - CVE-2017-7392 CVE-2017-7393 CVE-2017-7394
                CVE-2017-7395 CVE-2017-7396 tigervnc: various flaws
  + other upstream related fixes

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Jan 19 2017 Jan Grulich <jgrulich@redhat.com> - 1.7.1-1
- Update to 1.7.1

* Mon Jan  9 2017 Hans de Goede <hdegoede@redhat.com> - 1.7.0-6
- Fix -inetd no longer working (rhbz#1408724)

* Wed Nov 30 2016 Jan Grulich <jgrulich@redhat.com> - 1.7.0-5
- Fix broken vncserver.service file

* Wed Nov 23 2016 Jan Grulich <jgrulich@redhat.com> - 1.7.0-4
- Improve instructions in vncserver.service
  Resolves: bz#1397207

* Tue Oct  4 2016 Hans de Goede <hdegoede@redhat.com> - 1.7.0-3
- Update tigervnc-1.7.0-xserver119-support.patch to also request write
  notfication when necessary

* Mon Oct  3 2016 Hans de Goede <hdegoede@redhat.com> - 1.7.0-2
- Add patches for use with xserver-1.19
- Rebuild against xserver-1.19
- Cleanup specfile a bit

* Mon Sep 12 2016 Jan Grulich <jgrulich@redhat.com> - 1.7.0-1
- Update to 1.7.0

* Mon Jul 18 2016 Jan Grulich <jgrulich@redhat.com> - 1.6.90-1
- Update to 1.6.90 (1.7.0 beta)

* Wed Jun 01 2016 Jan Grulich <jgrulich@redhat.com> - 1.6.0-6
- Try to pickup upstream fix for compatibility with gtk vnc clients

* Wed Jun 01 2016 Jan Grulich <jgrulich@redhat.com> - 1.6.0-5
- Re-enable patch4 again, will need to find a way to make this work on both sides

* Mon May 23 2016 Jan Grulich <jgrulich@redhat.com> - 1.6.0-4
- Utilize system-wide crypto policies
  Resolves: bz#1179345
- Try to disable patch4 as it was previously written to support an
  older version of a different client and breaks some other usage
  Resolves: bz#1280440

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jan 13 2016 Jan Grulich <jgrulich@redhat.com> - 1.6.0-2
- Update systemd service file
  Resolves: bz#1211789

* Mon Jan 04 2016 Jan Grulich <jgrulich@redhat.com> - 1.6.0-1
- Update to 1.6.0

* Tue Dec 01 2015 Jan Grulich <jgrulich@redhat.com> - 1.5.90-1
- Update to 1.5.90 (1.6.0 beta)

* Thu Nov 19 2015 Jan Grulich <jgrulich@redhat.com> - 1.5.0-4
- rebuild against final xorg server 1.18 release (bug #1279146)

* Tue Sep 22 2015 Kalev Lember <klember@redhat.com> - 1.5.0-3
- xorg server 1.18 ABI rebuild

* Fri Aug 21 2015 Jan Grulich <jgrulich@redhat.com> - 1.5.0-2
- Do not fail with -inetd option

* Wed Aug 19 2015 Jan Grulich <jgrulich@redhat.com> - 1.5.0-1
- 1.5.0

* Tue Aug 04 2015 Kevin Fenzi <kevin@scrye.com> - 1.4.3-12
- Rebuild to fix broken deps and build against xorg 1.18 prerelease

* Thu Jun 25 2015 Tim Waugh <twaugh@redhat.com> - 1.4.3-11
- Rebuilt (bug #1235603).

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.3-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon May 04 2015 Kalev Lember <kalevlember@gmail.com> - 1.4.3-8
- Rebuilt for nettle soname bump

* Wed Apr 22 2015 Tim Waugh <twaugh@redhat.com> - 1.4.3-7
- Removed incorrect parameters from vncviewer manpage (bug #1213199).

* Tue Apr 21 2015 Tim Waugh <twaugh@redhat.com> - 1.4.3-6
- Use full git hash for GitHub tarball release.

* Fri Apr 10 2015 Tim Waugh <twaugh@redhat.com> - 1.4.3-5
- Explicit version build dependency for fltk (bug #1208814).

* Thu Apr  9 2015 Tim Waugh <twaugh@redhat.com> - 1.4.3-4
- Drop upstream xorg-x11-server patch as it is now built (bug #1210407).

* Thu Apr  9 2015 Tim Waugh <twaugh@redhat.com> - 1.4.3-3
- Apply upstream patch to fix byte order (bug #1206060).

* Fri Mar  6 2015 Tim Waugh <twaugh@redhat.com> - 1.4.3-2
- Don't disable Xinerama extension (upstream #147).

* Mon Mar  2 2015 Tim Waugh <twaugh@redhat.com> - 1.4.3-1
- 1.4.3.

* Tue Feb 24 2015 Tim Waugh <twaugh@redhat.com> - 1.4.2-3
- Use calloc instead of xmalloc.
- Removed unnecessary configure flags.

* Wed Feb 18 2015 Rex Dieter <rdieter@fedoraproject.org> 1.4.2-2
- rebuild (fltk)

* Fri Feb 13 2015 Tim Waugh <twaugh@redhat.com> - 1.4.2-1
- Rebased xserver116.patch against xorg-x11-server-1.17.1.
- Allow build against xorg-x11-server-1.17.
- 1.4.2.

* Tue Sep  9 2014 Tim Waugh <twaugh@redhat.com> - 1.3.1-11
- Added missing part of xserver114.patch (bug #1137023).

* Wed Sep  3 2014 Tim Waugh <twaugh@redhat.com> - 1.3.1-10
- Fix build against xorg-x11-server-1.16.0 (bug #1136532).

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jul 15 2014 Tim Waugh <twaugh@redhat.com> - 1.3.1-8
- Input reset fixes from upstream (bug #1116956).
- No longer need ppc64le patch as it's now in xorg-x11-server.
- Rebased xserver114.patch again.

* Fri Jun 20 2014 Hans de Goede <hdegoede@redhat.com> - 1.3.1-7
- xserver 1.15.99.903 ABI rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May 22 2014 Tim Waugh <twaugh@redhat.com> 1.3.1-5
- Keep pointer in sync when using module (upstream bug #152).

* Mon Apr 28 2014 Adam Jackson <ajax@redhat.com> 1.3.1-4
- Add version interlocks for -server-module

* Mon Apr 28 2014 Hans de Goede <hdegoede@redhat.com> - 1.3.1-3
- xserver 1.15.99-20140428 git snapshot ABI rebuild

* Mon Apr  7 2014 Tim Waugh <twaugh@redhat.com> 1.3.1-2
- Allow build with dri3 and present extensions (bug #1063392).

* Thu Mar 27 2014 Tim Waugh <twaugh@redhat.com> 1.3.1-1
- 1.3.1 (bug #1078806).
- Add ppc64le support (bug #1078495).

* Wed Mar 19 2014 Tim Waugh <twaugh@redhat.com> 1.3.0-15
- Disable dri3 to enable building (bug #1063392).
- Fixed heap-based buffer overflow (CVE-2014-0011, bug #1050928).

* Fri Feb 21 2014 Tim Waugh <twaugh@redhat.com> 1.3.0-14
- Enabled hardened build (bug #955206).

* Mon Feb 10 2014 Tim Waugh <twaugh@redhat.com> 1.3.0-13
- Clearer xstartup file (bug #923655).

* Tue Jan 14 2014 Tim Waugh <twaugh@redhat.com> 1.3.0-12
- Fixed instructions in systemd unit file.

* Fri Jan 10 2014 Tim Waugh <twaugh@redhat.com> 1.3.0-11
- Fixed viewer crash when cursor has not been set (bug #1038701).

* Thu Dec 12 2013 Tim Waugh <twaugh@redhat.com> 1.3.0-10
- Avoid invalid read when ZRLE connection closed (upstream bug #133).

* Tue Dec  3 2013 Tim Waugh <twaugh@redhat.com> 1.3.0-9
- Fixed build failure with -Werror=format-security (bug #1037358).

* Thu Nov 07 2013 Adam Jackson <ajax@redhat.com> 1.3.0-8
- Rebuild against xserver 1.15RC1

* Tue Sep 24 2013 Tim Waugh <twaugh@redhat.com> 1.3.0-7
- Removed incorrect patch (for unexpected key_is_down). Fixes stuck
  keys bug (bug #989502).

* Thu Sep 19 2013 Tim Waugh <twaugh@redhat.com> 1.3.0-6
- Fixed typo in 10-libvnc.conf (bug #1009111).

* Wed Sep 18 2013 Tim Waugh <twaugh@redhat.com> 1.3.0-5
- Better fix for PIDFile problem (bug #983232).

* Mon Aug  5 2013 Tim Waugh <twaugh@redhat.com> 1.3.0-4
- Fixed doc-related build failure (bug #992790).

* Wed Jul 24 2013 Tim Waugh <twaugh@redhat.com> 1.3.0-3
- Avoid PIDFile problems in systemd unit file (bug #983232).
- libvnc.so: don't use unexported key_is_down function.
- Don't use shebang in vncserver script.

* Fri Jul 12 2013 Tim Waugh <twaugh@redhat.com> 1.3.0-2
- Renumbered patches.
- libvnc.so: don't use unexported GetMaster function (bug #744881 again).

* Mon Jul  8 2013 Tim Waugh <twaugh@redhat.com> 1.3.0-1
- 1.3.0.

* Wed Jul  3 2013 Tim Waugh <twaugh@redhat.com> 1.2.80-0.18.20130314svn5065
- Removed systemd_requires macro in order to fix the build.

* Wed Jul  3 2013 Tim Waugh <twaugh@redhat.com> 1.2.80-0.17.20130314svn5065
- Synchronise manpages and --help output (bug #980870).

* Mon Jun 17 2013 Adam Jackson <ajax@redhat.com> 1.2.80-0.16.20130314svn5065
- tigervnc-setcursor-crash.patch: Attempt to paper over a crash in Xvnc when
  setting the cursor.

* Sat Jun 08 2013 Dennis Gilmore <dennis@ausil.us> 1.2.80-0.15.20130314svn5065
- bump to rebuild and pick up bugfix causing X to crash on ppc and arm

* Thu May 23 2013 Tim Waugh <twaugh@redhat.com> 1.2.80-0.14.20130314svn5065
- Use systemd rpm macros (bug #850340).  Moved systemd requirements
  from main package to server sub-package.
- Applied Debian patch to fix busy loop when run from inetd in nowait
  mode (bug #920373).
- Added dependency on xorg-x11-xinit to server sub-package so that
  default window manager can be found (bug #896284, bug #923655).
- Fixed bogus changelog date.

* Thu Mar 14 2013 Adam Jackson <ajax@redhat.com> 1.2.80-0.13.20130314svn5065
- Less RHEL customization

* Thu Mar 14 2013 Adam Tkac <atkac redhat com> - 1.2.80-0.12.20130314svn5065
- include /etc/X11/xorg.conf.d/10-libvnc.conf sample configuration (#712482)
- vncserver now honors specified -geometry parameter (#755947)

* Tue Mar 12 2013 Adam Tkac <atkac redhat com> - 1.2.80-0.11.20130307svn5060
- update to r5060
- split icons to separate package to avoid multilib issues

* Tue Feb 19 2013 Adam Tkac <atkac redhat com> - 1.2.80-0.10.20130219svn5047
- update to r5047 (X.Org 1.14 support)

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.80-0.9.20121126svn5015
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Jan 21 2013 Adam Tkac <atkac redhat com> - 1.2.80-0.8.20121126svn5015
- rebuild due to "jpeg8-ABI" feature drop

* Wed Jan 16 2013 Adam Tkac <atkac redhat com> 1.2.80-0.7.20121126svn5015
- rebuild

* Tue Dec 04 2012 Adam Tkac <atkac redhat com> 1.2.80-0.6.20121126svn5015
- rebuild against new fltk

* Mon Nov 26 2012 Adam Tkac <atkac redhat com> 1.2.80-0.5.20121126svn5015
- update to r5015
- build with -fpic instead of -fPIC on all archs except s390/sparc

* Wed Nov  7 2012 Peter Robinson <pbrobinson@fedoraproject.org> 1.2.80-0.4.20120905svn4996
- Build with -fPIC to fix FTBFS on ARM

* Wed Oct 31 2012 Adam Jackson <ajax@redhat.com> 1.2.80-0.3.20120905svn4996
- tigervnc12-xorg113-glx.patch: Fix to only init glx on the first server
  generation

* Fri Sep 28 2012 Adam Jackson <ajax@redhat.com> 1.2.80-0.2.20120905svn4996
- tigervnc12-xorg113-glx.patch: Re-enable GLX against xserver 1.13

* Fri Aug 17 2012 Adam Tkac <atkac redhat com> 1.2.80-0.1.20120905svn4996
- update to 1.2.80
- remove deprecated patches
  - tigervnc-102434.patch
  - tigervnc-viewer-reparent.patch
  - tigervnc11-java7.patch
- patches merged
  - tigervnc11-xorg111.patch
  - tigervnc11-xorg112.patch

* Fri Aug 10 2012 Dave Airlie <airlied@redhat.com> 1.1.0-10
- fix build against newer X server

* Mon Jul 23 2012 Adam Jackson <ajax@redhat.com> 1.1.0-9
- Build with the Composite extension for feature parity with other X servers

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jul 19 2012 Dave Airlie <airlied@redhat.com> 1.1.0-7
- fix building against X.org 1.13

* Wed Apr 04 2012 Adam Jackson <ajax@redhat.com> 1.1.0-6
- RHEL exclusion for -server-module on ppc* too

* Mon Mar 26 2012 Adam Tkac <atkac redhat com> - 1.1.0-5
- clean Xvnc's /tmp environment in service file before startup
- fix building against the latest JAVA 7 and X.Org 1.12

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Nov 22 2011 Adam Tkac <atkac redhat com> - 1.1.0-3
- don't build X.Org devel docs (#755782)
- applet: BR generic java-devel instead of java-gcj-devel (#755783)
- use runuser to start Xvnc in systemd service file (#754259)
- don't attepmt to restart Xvnc session during update/erase (#753216)

* Fri Nov 11 2011 Adam Tkac <atkac redhat com> - 1.1.0-2
- libvnc.so: don't use unexported GetMaster function (#744881)
- remove nasm buildreq

* Mon Sep 12 2011 Adam Tkac <atkac redhat com> - 1.1.0-1
- update to 1.1.0
- update the xorg11 patch
- patches merged
  - tigervnc11-glx.patch
  - tigervnc11-CVE-2011-1775.patch
  - 0001-Use-memmove-instead-of-memcpy-in-fbblt.c-when-memory.patch

* Thu Jul 28 2011 Adam Tkac <atkac redhat com> - 1.0.90-6
- add systemd service file and remove legacy SysV initscript (#717227)

* Thu May 12 2011 Adam Tkac <atkac redhat com> - 1.0.90-5
- make Xvnc buildable against X.Org 1.11

* Tue May 10 2011 Adam Tkac <atkac redhat com> - 1.0.90-4
- viewer can send password without proper validation of X.509 certs
  (CVE-2011-1775)

* Wed Apr 13 2011 Adam Tkac <atkac redhat com> - 1.0.90-3
- fix wrong usage of memcpy which caused screen artifacts (#652590)
- don't point to inaccessible link in sysconfig/vncservers (#644975)

* Fri Apr 08 2011 Adam Tkac <atkac redhat com> - 1.0.90-2
- improve compatibility with vinagre client (#692048)

* Tue Mar 22 2011 Adam Tkac <atkac redhat com> - 1.0.90-1
- update to 1.0.90

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.90-0.32.20110117svn4237
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jan 17 2011 Adam Tkac <atkac redhat com> 1.0.90-0.31.20110117svn4237
- fix libvnc.so module loading

* Mon Jan 17 2011 Adam Tkac <atkac redhat com> 1.0.90-0.30.20110117svn4237
- update to r4237
- patches merged
  - tigervnc11-optionsdialog.patch
  - tigervnc11-rh607866.patch

* Fri Jan 14 2011 Adam Tkac <atkac redhat com> 1.0.90-0.29.20101208svn4225
- improve patch for keyboard issues

* Fri Jan 14 2011 Adam Tkac <atkac redhat com> 1.0.90-0.28.20101208svn4225
- attempt to fix various keyboard-related issues (key repeating etc)

* Fri Jan 07 2011 Adam Tkac <atkac redhat com> 1.0.90-0.27.20101208svn4225
- render "Ok" and "Cancel" buttons in the options dialog correctly

* Wed Dec 15 2010 Jan Görig <jgorig redhat com> 1.0.90-0.26.20101208svn4225
- added vncserver lock file (#662784)

* Fri Dec 10 2010 Adam Tkac <atkac redhat com> 1.0.90-0.25.20101208svn4225
- update to r4225
- patches merged
  - tigervnc11-rh611677.patch
  - tigervnc11-rh633931.patch
  - tigervnc11-xorg1.10.patch
- enable VeNCrypt and PAM support

* Mon Dec 06 2010 Adam Tkac <atkac redhat com> 1.0.90-0.24.20100813svn4123
- rebuild against xserver 1.10.X
- 0001-Return-Success-from-generate_modkeymap-when-max_keys.patch merged

* Wed Sep 29 2010 jkeating - 1.0.90-0.23.20100813svn4123
- Rebuilt for gcc bug 634757

* Tue Sep 21 2010 Adam Tkac <atkac redhat com> 1.0.90-0.22.20100420svn4030
- drop xorg-x11-fonts-misc dependency (#636170)

* Tue Sep 21 2010 Adam Tkac <atkac redhat com> 1.0.90-0.21.20100420svn4030
- improve patch for #633645 (fix tcsh incompatibilities)

* Thu Sep 16 2010 Adam Tkac <atkac redhat com> 1.0.90-0.20.20100813svn4123
- press fake modifiers correctly (#633931)
- supress unneeded debug information emitted from initscript (#633645)

* Wed Aug 25 2010 Adam Tkac <atkac redhat com> 1.0.90-0.19.20100813svn4123
- separate Xvnc, vncpasswd and vncconfig to -server-minimal subpkg (#626946)
- move license to separate subpkg and Requires it from main subpkgs
- Xvnc: handle situations when no modifiers exist well (#611677)

* Fri Aug 13 2010 Adam Tkac <atkac redhat com> 1.0.90-0.18.20100813svn4123
- update to r4123 (#617973)
- add perl requires to -server subpkg (#619791)

* Thu Jul 22 2010 Adam Tkac <atkac redhat com> 1.0.90-0.17.20100721svn4113
- update to r4113
- patches merged
  - tigervnc11-rh586406.patch
  - tigervnc11-libvnc.patch
  - tigervnc11-rh597172.patch
  - tigervnc11-rh600070.patch
  - tigervnc11-options.patch
- don't own %%{_datadir}/icons directory (#614301)
- minor improvements in the .desktop file (#616340)
- bundled libjpeg configure requires nasm; is executed even if system-wide
  libjpeg is used

* Fri Jul 02 2010 Adam Tkac <atkac redhat com> 1.0.90-0.16.20100420svn4030
- build against system-wide libjpeg-turbo (#494458)
- build no longer requires nasm

* Mon Jun 28 2010 Adam Tkac <atkac redhat com> 1.0.90-0.15.20100420svn4030
- vncserver: accept <+optname> option when specified as the first one

* Thu Jun 24 2010 Adam Tkac <atkac redhat com> 1.0.90-0.14.20100420svn4030
- fix memory leak in Xvnc input code (#597172)
- don't crash when receive negative encoding (#600070)
- explicitly disable udev configuration support
- add gettext-autopoint to BR

* Mon Jun 14 2010 Adam Tkac <atkac redhat com> 1.0.90-0.13.20100420svn4030
- update URL about SSH tunneling in the sysconfig file (#601996)

* Fri Jun 11 2010 Adam Tkac <atkac redhat com> 1.0.90-0.12.20100420svn4030
- use newer gettext
- autopoint now uses git instead of cvs, adjust BuildRequires appropriately

* Thu May 13 2010 Adam Tkac <atkac redhat com> 1.0.90-0.11.20100420svn4030
- link libvnc.so "now" to catch "undefined symbol" errors during Xorg startup
- use always XkbConvertCase instead of XConvertCase (#580159, #586406)
- don't link libvnc.so against libXi.la, libdix.la and libxkb.la; use symbols
  from Xorg instead

* Thu May 13 2010 Adam Tkac <atkac redhat com> 1.0.90-0.10.20100420svn4030
- update to r4030 snapshot
- patches merged to upstream
  - tigervnc11-rh522369.patch
  - tigervnc11-rh551262.patch
  - tigervnc11-r4002.patch
  - tigervnc11-r4014.patch

* Thu Apr 08 2010 Adam Tkac <atkac redhat com> 1.0.90-0.9.20100219svn3993
- add server-applet subpackage which contains Java vncviewer applet
- fix Java applet; it didn't work when run from web browser
- add xorg-x11-xkb-utils to server Requires

* Fri Mar 12 2010 Adam Tkac <atkac redhat com> 1.0.90-0.8.20100219svn3993
- add French translation to vncviewer.desktop (thanks to Alain Portal)

* Thu Mar 04 2010 Adam Tkac <atkac redhat com> 1.0.90-0.7.20100219svn3993
- don't crash during pixel format change (#522369, #551262)

* Mon Mar 01 2010 Adam Tkac <atkac redhat com> 1.0.90-0.6.20100219svn3993
- add mesa-dri-drivers and xkeyboard-config to -server Requires
- update to r3993 1.0.90 snapshot
  - tigervnc11-noexecstack.patch merged
  - tigervnc11-xorg18.patch merged
  - xserver18.patch is no longer needed

* Wed Jan 27 2010 Jan Gorig <jgorig redhat com> 1.0.90-0.5.20091221svn3929
- initscript LSB compliance fixes (#523974)

* Fri Jan 22 2010 Adam Tkac <atkac redhat com> 1.0.90-0.4.20091221svn3929
- mark stack as non-executable in jpeg ASM code
- add xorg-x11-xauth to Requires
- add support for X.Org 1.8
- drop shave sources, they are no longer needed

* Thu Jan 21 2010 Adam Tkac <atkac redhat com> 1.0.90-0.3.20091221svn3929
- drop tigervnc-xorg25909.patch, it has been merged to X.Org upstream

* Thu Jan 07 2010 Adam Tkac <atkac redhat com> 1.0.90-0.2.20091221svn3929
- add patch for upstream X.Org issue #25909
- add libXdmcp-devel to build requires to build Xvnc with XDMCP support (#552322)

* Mon Dec 21 2009 Adam Tkac <atkac redhat com> 1.0.90-0.1.20091221svn3929
- update to 1.0.90 snapshot
- patches merged
  - tigervnc10-compat.patch
  - tigervnc10-rh510185.patch
  - tigervnc10-rh524340.patch
  - tigervnc10-rh516274.patch

* Mon Oct 26 2009 Adam Tkac <atkac redhat com> 1.0.0-3
- create Xvnc keyboard mapping before first keypress (#516274)

* Thu Oct 08 2009 Adam Tkac <atkac redhat com> 1.0.0-2
- update underlying X source to 1.6.4-0.3.fc11
- remove bogus '-nohttpd' parameter from /etc/sysconfig/vncservers (#525629)
- initscript LSB compliance fixes (#523974)
- improve -LowColorSwitch documentation and handling (#510185)
- honor dotWhenNoCursor option (and it's changes) every time (#524340)

* Fri Aug 28 2009 Adam Tkac <atkac redhat com> 1.0.0-1
- update to 1.0.0
- tigervnc10-rh495457.patch merged to upstream

* Mon Aug 24 2009 Karsten Hopp <karsten@redhat.com> 0.0.91-0.17
- fix ifnarch s390x for server-module

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 0.0.91-0.16
- rebuilt with new openssl

* Tue Aug 04 2009 Adam Tkac <atkac redhat com> 0.0.91-0.15
- make Xvnc compilable

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.91-0.14.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jul 13 2009 Adam Tkac <atkac redhat com> 0.0.91-0.13.1
- don't write warning when initscript is called with condrestart param (#508367)

* Tue Jun 23 2009 Adam Tkac <atkac redhat com> 0.0.91-0.13
- temporary use F11 Xserver base to make Xvnc compilable
- BuildRequires: libXi-devel
- don't ship tigervnc-server-module on s390/s390x

* Mon Jun 22 2009 Adam Tkac <atkac redhat com> 0.0.91-0.12
- fix local rendering of cursor (#495457)

* Thu Jun 18 2009 Adam Tkac <atkac redhat com> 0.0.91-0.11
- update to 0.0.91 (1.0.0 RC1)
- patches merged
  - tigervnc10-rh499401.patch
  - tigervnc10-rh497592.patch
  - tigervnc10-rh501832.patch
- after discusion in upstream drop tigervnc-bounds.patch
- configure flags cleanup

* Thu May 21 2009 Adam Tkac <atkac redhat com> 0.0.90-0.10
- rebuild against 1.6.1.901 X server (#497835)
- disable i18n, vncviewer is not UTF-8 compatible (#501832)

* Mon May 18 2009 Adam Tkac <atkac redhat com> 0.0.90-0.9
- fix vncpasswd crash on long passwords (#499401)
- start session dbus daemon correctly (#497592)

* Mon May 11 2009 Adam Tkac <atkac redhat com> 0.0.90-0.8.1
- remove merged tigervnc-manminor.patch

* Tue May 05 2009 Adam Tkac <atkac redhat com> 0.0.90-0.8
- update to 0.0.90

* Thu Apr 30 2009 Adam Tkac <atkac redhat com> 0.0.90-0.7.20090427svn3789
- server package now requires xorg-x11-fonts-misc (#498184)

* Mon Apr 27 2009 Adam Tkac <atkac redhat com> 0.0.90-0.6.20090427svn3789
- update to r3789
  - tigervnc-rh494801.patch merged
- tigervnc-newfbsize.patch is no longer needed
- fix problems when vncviewer and Xvnc run on different endianess (#496653)
- UltraVNC and TightVNC clients work fine again (#496786)

* Wed Apr 08 2009 Adam Tkac <atkac redhat com> 0.0.90-0.5.20090403svn3751
- workaround broken fontpath handling in vncserver script (#494801)

* Fri Apr 03 2009 Adam Tkac <atkac redhat com> 0.0.90-0.4.20090403svn3751
- update to r3751
- patches merged
  - tigervnc-xclients.patch
  - tigervnc-clipboard.patch
  - tigervnc-rh212985.patch
- basic RandR support in Xvnc (resize of the desktop)
- use built-in libjpeg (SSE2/MMX accelerated encoding on x86 platform)
- use Tight encoding by default
- use TigerVNC icons

* Tue Mar 03 2009 Adam Tkac <atkac redhat com> 0.0.90-0.3.20090303svn3631
- update to r3631

* Tue Mar 03 2009 Adam Tkac <atkac redhat com> 0.0.90-0.2.20090302svn3621
- package review related fixes

* Mon Mar 02 2009 Adam Tkac <atkac redhat com> 0.0.90-0.1.20090302svn3621
- initial package, r3621
