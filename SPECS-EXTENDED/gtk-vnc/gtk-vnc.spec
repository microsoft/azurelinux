Vendor:         Microsoft Corporation
Distribution:   Mariner
# -*- rpm-spec -*-

# This spec file assumes you are building for Fedora 26 or newer,
# or for RHEL 7 or newer. It may need some tweaks for other distros.

%if 0%{?fedora} || 0%{?rhel} >= 8
    %global tls_priority "@LIBVIRT,SYSTEM"
%else
    %global tls_priority "NORMAL"
%endif

Summary: A GTK widget for VNC clients
Name: gtk-vnc
Version: 1.0.0
Release: 3%{?dist}
License: LGPLv2+
Source: http://ftp.gnome.org/pub/GNOME/sources/%{name}/0.5/%{name}-%{version}.tar.xz
URL: https://wiki.gnome.org/Projects/gtk-vnc
Requires: gvnc = %{version}-%{release}
%if 0%{?fedora}
BuildRequires: python3
%else
%if 0%{?rhel} > 7
BuildRequires: python3-devel
%else
BuildRequires: python
%endif
%endif
BuildRequires: gnutls-devel libgcrypt-devel cyrus-sasl-devel zlib-devel
BuildRequires: gobject-introspection-devel
BuildRequires: gtk3-devel
BuildRequires: vala-tools
BuildRequires: pulseaudio-libs-devel
BuildRequires: /usr/bin/pod2man
BuildRequires: meson

%description
gtk-vnc is a VNC viewer widget for GTK. It is built using coroutines
allowing it to be completely asynchronous while remaining single threaded.

%package -n gvnc
Summary: A GObject for VNC connections

%description -n gvnc
gvnc is a GObject for managing a VNC connection. It provides all the
infrastructure required to build a VNC client without having to deal
with the raw protocol itself.

%package -n gvnc-devel
Summary: Libraries, includes, etc. to compile with the gvnc library
Requires: gvnc = %{version}-%{release}
Requires: pkgconfig

%description -n gvnc-devel
gvnc is a GObject for managing a VNC connection. It provides all the
infrastructure required to build a VNC client without having to deal
with the raw protocol itself.

Libraries, includes, etc. to compile with the gvnc library

%package -n gvncpulse
Summary: A Pulse Audio bridge for VNC connections
Requires: gvnc = %{version}-%{release}

%description -n gvncpulse
gvncpulse is a bridge to the Pulse Audio system for VNC.
It allows VNC clients to play back audio on the local
system

%package -n gvncpulse-devel
Summary: Libraries, includes, etc. to compile with the gvncpulse library
Requires: gvncpulse = %{version}-%{release}
Requires: pkgconfig

%description -n gvncpulse-devel
gvncpulse is a bridge to the Pulse Audio system for VNC.
It allows VNC clients to play back audio on the local
system

Libraries, includes, etc. to compile with the gvnc library

%package -n gvnc-tools
Summary: Command line VNC tools
Requires: gvnc = %{version}-%{release}

%description -n gvnc-tools
Provides useful command line utilities for interacting with
VNC servers. Includes the gvnccapture program for capturing
screenshots of a VNC desktop

%package -n gtk-vnc2
Summary: A GTK3 widget for VNC clients
Requires: gvnc = %{version}-%{release}
Obsoletes: gtk-vnc

%description -n gtk-vnc2
gtk-vnc is a VNC viewer widget for GTK3. It is built using coroutines
allowing it to be completely asynchronous while remaining single threaded.

%package -n gtk-vnc2-devel
Summary: Development files to build GTK3 applications with gtk-vnc
Requires: gtk-vnc2 = %{version}-%{release}
Requires: pkgconfig
Requires: gtk3-devel
Obsoletes: gtk-vnc-devel

%description -n gtk-vnc2-devel
gtk-vnc is a VNC viewer widget for GTK3. It is built using coroutines
allowing it to be completely asynchronous while remaining single threaded.

Libraries, includes, etc. to compile with the gtk-vnc library

%prep
%autosetup -n gtk-vnc-%{version}

%build
%meson
%meson_build
chmod -x examples/*.pl examples/*.js examples/*.py

%install
%meson_install

%find_lang %{name}

%check
%meson_test

%ldconfig_scriptlets -n gvnc

%ldconfig_scriptlets -n gvncpulse

%ldconfig_scriptlets -n gtk-vnc2

%files -n gvnc -f %{name}.lang
%{_libdir}/libgvnc-1.0.so.*
%{_libdir}/girepository-1.0/GVnc-1.0.typelib
%{_datadir}/vala/vapi/gvnc-1.0.deps
%{_datadir}/vala/vapi/gvnc-1.0.vapi

%files -n gvnc-devel
%{_libdir}/libgvnc-1.0.so
%dir %{_includedir}/gvnc-1.0/
%{_includedir}/gvnc-1.0/*.h
%{_libdir}/pkgconfig/gvnc-1.0.pc
%{_datadir}/gir-1.0/GVnc-1.0.gir

%files -n gvncpulse -f %{name}.lang
%{_libdir}/libgvncpulse-1.0.so.*
%{_libdir}/girepository-1.0/GVncPulse-1.0.typelib
%{_datadir}/vala/vapi/gvncpulse-1.0.deps
%{_datadir}/vala/vapi/gvncpulse-1.0.vapi

%files -n gvncpulse-devel
%{_libdir}/libgvncpulse-1.0.so
%dir %{_includedir}/gvncpulse-1.0/
%{_includedir}/gvncpulse-1.0/*.h
%{_libdir}/pkgconfig/gvncpulse-1.0.pc
%{_datadir}/gir-1.0/GVncPulse-1.0.gir

%files -n gvnc-tools
%doc AUTHORS
%doc ChangeLog
%doc ChangeLog-old
%doc NEWS
%doc README
%doc COPYING.LIB
%{_bindir}/gvnccapture
%{_mandir}/man1/gvnccapture.1*

%files -n gtk-vnc2
%{_libdir}/libgtk-vnc-2.0.so.*
%{_libdir}/girepository-1.0/GtkVnc-2.0.typelib
%{_datadir}/vala/vapi/gtk-vnc-2.0.deps
%{_datadir}/vala/vapi/gtk-vnc-2.0.vapi

%files -n gtk-vnc2-devel
%doc examples/gvncviewer.c
%doc examples/gvncviewer.js
%doc examples/gvncviewer.pl
%doc examples/gvncviewer.py
%{_libdir}/libgtk-vnc-2.0.so
%dir %{_includedir}/%{name}-2.0/
%{_includedir}/%{name}-2.0/*.h
%{_libdir}/pkgconfig/%{name}-2.0.pc
%{_datadir}/gir-1.0/GtkVnc-2.0.gir

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.0.0-3
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Aug  8 2019 Daniel P. Berrangé <berrange@redhat.com> - 1.0.0-1
- Update to 1.0.0 release

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Feb 04 2019 Kalev Lember <klember@redhat.com> - 0.9.0-5
- Update BRs for vala packaging changes

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Aug 30 2018 Daniel P. Berrangé <berrange@redhat.com> - 0.9.0-3
- Fix gvnc-1.0.pc file version dep

* Fri Aug 24 2018 Daniel P. Berrangé <berrange@redhat.com> - 0.9.0-2
- Fix crash if connection fails early (rhbz #1620203)

* Fri Aug 17 2018 Daniel P. Berrangé <berrange@redhat.com> - 0.9.0-1
- Update to 0.9.0 release

* Wed Aug  1 2018 Daniel P. Berrangé <berrange@redhat.com> - 0.8.0-1
- Update to 0.8.0 release

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Mar 23 2018 Daniel P. Berrangé <berrange@redhat.com> - 0.7.2-1
- Rebase to 0.7.2 release
- Disable python2 sub-RPM

* Wed Feb 14 2018 Iryna Shcherbina <ishcherb@redhat.com> - 0.7.1-7
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sun Aug 20 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.7.1-5
- Add Provides for the old name without %%_isa

* Sat Aug 19 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.7.1-4
- Python 2 binary package renamed to python2-gtk-vnc
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri May 19 2017 Daniel P. Berrange <berrange@redhat.com> - 0.7.1-1
- Update to 0.7.1 release
- Fix incompatibility with libvncserver/x11vnc (rhbz #1421785)

* Thu Feb  9 2017 Daniel P. Berrange <berrange@redhat.com> - 0.7.0-1
- Update to 0.7.0 release
- CVE-2017-5884 - fix bounds checking for RRE, hextile and
  copyrect encodings
- CVE-2017-5885 - fix color map index bounds checking

* Thu Oct  6 2016 Daniel P. Berrange <berrange@redhat.com> - 0.6.0-1
- Update to 0.6.0 release

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.4-4
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild
