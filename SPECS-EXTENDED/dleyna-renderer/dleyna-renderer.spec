Vendor:         Microsoft Corporation
Distribution:   Mariner
%global api 1.0

Name:           dleyna-renderer
Version:        0.6.0
Release:        7%{?dist}
Summary:        Service for interacting with Digital Media Renderers

License:        LGPLv2
URL:            https://01.org/dleyna/
Source0:        https://01.org/sites/default/files/downloads/dleyna/%{name}-%{version}.tar_2.gz

# https://bugzilla.gnome.org/show_bug.cgi?id=741257
Patch0:         0001-UPnP-Disconnect-signal-handlers-during-destruction.patch

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  pkgconfig
BuildRequires:  pkgconfig(dleyna-core-1.0)
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gssdp-1.0)
BuildRequires:  pkgconfig(gupnp-1.0)
BuildRequires:  pkgconfig(gupnp-av-1.0)
BuildRequires:  pkgconfig(gupnp-dlna-2.0)
BuildRequires:  pkgconfig(libsoup-2.4)
Requires:       dbus
Requires:       dleyna-connector-dbus%{?_isa}

%description
D-Bus service for clients to discover and manipulate DLNA Digital Media
Renderers (DMRs).


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q
%patch0 -p1


%build
autoreconf -f -i
%configure \
  --disable-silent-rules \
  --disable-static

# Omit unused direct shared library dependencies.
sed --in-place --expression 's! -shared ! -Wl,--as-needed\0!g' libtool

%make_build


%install
%make_install
find $RPM_BUILD_ROOT -name '*.la' -delete

# We don't need to install the headers because only the daemon is supposed to be
# using the library.
rm -rf $RPM_BUILD_ROOT/%{_includedir}
rm -f $RPM_BUILD_ROOT/%{_libdir}/%{name}/libdleyna-renderer-%{api}.so


%files
%license COPYING
%doc AUTHORS
%doc ChangeLog
%doc README
%{_datadir}/dbus-1/services/com.intel.%{name}.service

%dir %{_libdir}/%{name}
%{_libdir}/%{name}/libdleyna-renderer-%{api}.so.*

%{_libexecdir}/%{name}-service
%config(noreplace) %{_sysconfdir}/%{name}-service.conf

%files devel
%{_libdir}/pkgconfig/dleyna-renderer-service-%{api}.pc


%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.6.0-7
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Oct 06 2017 Debarshi Ray <rishi@fedoraproject.org> - 0.6.0-1
- Update to 0.6.0

* Fri Oct 06 2017 Debarshi Ray <rishi@fedoraproject.org> - 0.5.0-9
- Use arch-specific Requires on dleyna-connector-dbus

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Sep 15 2016 Debarshi Ray <rishi@fedoraproject.org> - 0.5.0-5
- Avoid any attempts to delete the same dlr_upnp_t twice (RH #1251366)

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jan 21 2016 Kalev Lember <klember@redhat.com> - 0.5.0-3
- Add -devel subpackage with the .pc file
- Use make_install macro
- Use license macro for COPYING

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu May 07 2015 Debarshi Ray <rishi@fedoraproject.org> - 0.5.0-1
- Update to 0.5.0

* Tue Jan 20 2015 Debarshi Ray <rishi@fedoraproject.org> - 0.4.0-4
- Fix crash when spawned by a call to com.intel.dLeynaRenderer.Manager.Release
  (RH #1154788)

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Jan 15 2014 Bastien Nocera <bnocera@redhat.com> - 0.4.0-1
- Update to 0.4.0

* Mon Sep 02 2013 Debarshi Ray <rishi@fedoraproject.org> - 0.1.3-2
- Do not remove the rpaths anymore because the library has now been moved to a
  private location.

* Mon Sep 02 2013 Debarshi Ray <rishi@fedoraproject.org> - 0.1.3-1
- Update to 0.1.3.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jun 26 2013 Debarshi Ray <rishi@fedoraproject.org> - 0.1.1-1
- Initial spec.
