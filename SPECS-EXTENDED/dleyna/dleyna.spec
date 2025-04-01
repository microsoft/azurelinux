Name:    dleyna
Version: 0.8.3
Release: 5%{?dist}
Summary: Services and D-Bus APIs for UPnP access

License: LGPL-2.1-or-later
URL:     https://gitlab.gnome.org/World/dLeyna
Source0: https://gitlab.gnome.org/World/dLeyna/-/archive/v%{version}/dLeyna-v%{version}.tar.bz2

BuildRequires: /usr/bin/rst2man
BuildRequires: gcc
BuildRequires: meson
BuildRequires: python3-devel
BuildRequires: pkgconfig(gio-unix-2.0)
BuildRequires: pkgconfig(gobject-introspection-1.0)
BuildRequires: pkgconfig(gssdp-1.6)
BuildRequires: pkgconfig(gupnp-1.6)
BuildRequires: pkgconfig(gupnp-av-1.0)
BuildRequires: pkgconfig(gupnp-dlna-2.0)
BuildRequires: pkgconfig(libsoup-3.0)
BuildRequires: pkgconfig(libxml-2.0)

%description
dLeyna is a set of services and D-Bus APIs that aim to simplify access to UPnP
and DLNA media devices in a network.

%package  connector-dbus
Summary:  D-Bus connector for dLeyna services
Requires: %{name}%{?_isa} = %{version}-%{release}

%description connector-dbus
D-Bus connector for dLeyna services.

%package  renderer
Summary:  Service for interacting with Digital Media Renderers
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: %{name}-connector-dbus%{?_isa} = %{version}-%{release}

%description renderer
D-Bus service for clients to discover and manipulate DLNA Digital Media
Renderers (DMRs).

%package  server
Summary:  Service for interacting with Digital Media Servers
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: %{name}-connector-dbus%{?_isa} = %{version}-%{release}

%description server
D-Bus service for clients to discover and manipulate DLNA Digital Media
Servers (DMSes).

%package  devel
Summary:  Development files for the dLeyna components
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
dLeyna is a set of services and D-Bus APIs that aim to simplify access to UPnP
and DLNA media devices in a network. This package contains files used for
development with dleyna.

%prep
%autosetup -p1 -n dLeyna-v%{version}

%build
%meson -Ddocs=false
%meson_build

%install
%meson_install
# No consumers of the Python module in Fedora.
rm -rf %{buildroot}/%{python3_sitelib}
# These were not installed in the previous split packages.
# As there are no consumers in Fedora, only add these to the devel subpackage
# if they are requested in future.
rm -rf %{buildroot}/%{_libdir}/dleyna/libdleyna-renderer-1.0.so \
       %{buildroot}/%{_libdir}/pkgconfig/dleyna-renderer-service-1.0.pc \
       %{buildroot}/%{_libdir}/dleyna-server/libdleyna-server-1.0.so \
       %{buildroot}/%{_libdir}/pkgconfig/dleyna-server-service-1.0.pc \
       %{_includedir}/dleyna-1.0/renderer \
       %{_includedir}/dleyna-1.0/server


%files
%license COPYING
%doc AUTHORS ChangeLog.core NEWS README.md
%dir %{_libdir}/dleyna
%{_libdir}/libdleyna-core-1.0.so.6*

%files connector-dbus
%doc ChangeLog.connector-dbus
%dir %{_libdir}/dleyna-1.0
%dir %{_libdir}/dleyna-1.0/connectors
%{_libdir}/dleyna-1.0/connectors/libdleyna-connector-dbus.so

%files renderer
%doc ChangeLog.renderer
%{_datadir}/dbus-1/services/com.intel.dleyna-renderer.service
%{_libdir}/dleyna/libdleyna-renderer-1.0.so.1*
%{_libexecdir}/dleyna-renderer-service
%config(noreplace) %{_sysconfdir}/dleyna-renderer-service.conf
%{_mandir}/man1/dleyna-renderer-service.1*
%{_mandir}/man5/dleyna-renderer-service.conf.5*

%files server
%doc ChangeLog.server
%{_datadir}/dbus-1/services/com.intel.dleyna-server.service
%dir %{_libdir}/dleyna-server
%{_libdir}/dleyna-server/libdleyna-server-1.0.so.1*
%{_libexecdir}/dleyna-server-service
%{_mandir}/man1/dleyna-server-service.1*
%{_mandir}/man5/dleyna-server-service.conf.5*
%config(noreplace) %{_sysconfdir}/dleyna-server-service.conf

%files devel
%{_includedir}/dleyna-1.0/
%{_libdir}/libdleyna-core-1.0.so
%{_libdir}/pkgconfig/dleyna-core-1.0.pc

%changelog
* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu May 09 2024 David King <amigadave@amigadave.com> - 0.8.3-4
- Server and renderer depend on dbus connector (#2279873)

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Sep 20 2023 David King <amigadave@amigadave.com> - 0.8.3-1
- Update to 0.8.3

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Dec 09 2022 David King <amigadave@amigadave.com> - 0.8.2-1
- Initial version (#2144849)
