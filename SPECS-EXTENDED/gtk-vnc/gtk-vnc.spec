%global tls_priority "@LIBVIRT,SYSTEM"
%global verdir 1.3

Vendor:         Microsoft Corporation
Distribution:   Mariner
Summary: A GTK widget for VNC clients
Name: gtk-vnc
Version: 1.3.0
Release: 3%{?dist}
License: LGPLv2+
Source: https://download.gnome.org/sources/%{name}/%{verdir}/%{name}-%{version}.tar.xz
URL: https://gitlab.gnome.org/GNOME/gtk-vnc
Requires: gvnc = %{version}-%{release}
BuildRequires: python3-devel
BuildRequires: gnutls-devel libgcrypt-devel cyrus-sasl-devel zlib-devel
BuildRequires: gobject-introspection-devel
BuildRequires: gtk3-devel
BuildRequires: vala
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
Obsoletes: gtk-vnc < 1.0.0

%description -n gtk-vnc2
gtk-vnc is a VNC viewer widget for GTK3. It is built using coroutines
allowing it to be completely asynchronous while remaining single threaded.

%package -n gtk-vnc2-devel
Summary: Development files to build GTK3 applications with gtk-vnc
Requires: gtk-vnc2 = %{version}-%{release}
Requires: pkgconfig
Requires: gtk3-devel
Obsoletes: gtk-vnc-devel < 1.0.0

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
* Mon Mar 06 2023 Muhammad Falak R Wani <mwani@microsoft.com> - 1.3.0-3
- Initial CBL-Mariner import from Fedora 36 (license: MIT).
- License Verified

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Nov 22 2021 Daniel P. Berrangé <berrange@redhat.com> - 1.3.0-1
- Update to 1.3.0 release

* Mon Aug 23 2021 Kalev Lember <klember@redhat.com> - 1.2.0-3
- BR vala instead of vala-tools

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Apr 14 2021 Daniel P. Berrangé <berrange@redhat.com> - 1.2.0-1
- Update to 1.2.0 release
- Drop outdated conditionals
- Drop outdated ldconfig script
- Use versioned obsoletes tags

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild
