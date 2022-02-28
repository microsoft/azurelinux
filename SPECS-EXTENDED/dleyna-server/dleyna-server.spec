Vendor:         Microsoft Corporation
Distribution:   Mariner
%global api 1.0

Name:           dleyna-server
Version:        0.6.0
Release:        7%{?dist}
Summary:        Service for interacting with Digital Media Servers

License:        LGPLv2
URL:            https://01.org/dleyna/
Source0:        https://01.org/sites/default/files/downloads/dleyna/%{name}-%{version}.tar_2.gz

BuildRequires:  autoconf automake libtool
BuildRequires:  pkgconfig(dleyna-core-1.0) >= 0.5.0
BuildRequires:  pkgconfig(gio-2.0) >= 2.28
BuildRequires:  pkgconfig(glib-2.0) >= 2.28
BuildRequires:  pkgconfig(gobject-2.0) >= 2.28
BuildRequires:  pkgconfig(gssdp-1.0) >= 0.13.2
BuildRequires:  pkgconfig(gupnp-1.0) >= 0.20.3
BuildRequires:  pkgconfig(gupnp-av-1.0) >= 0.11.5
BuildRequires:  pkgconfig(gupnp-dlna-2.0) >= 0.9.4
BuildRequires:  pkgconfig(libsoup-2.4) >= 2.28.2
Requires:       dbus
Requires:       dleyna-connector-dbus%{?_isa}

%description
D-Bus service for clients to discover and manipulate DLNA Digital Media
Servers (DMSes).


%prep
%setup -q


%build
autoreconf -fiv
%configure \
  --disable-silent-rules \
  --disable-static

# Omit unused direct shared library dependencies.
sed --in-place --expression 's! -shared ! -Wl,--as-needed\0!g' libtool

%make_build


%install
%make_install
find $RPM_BUILD_ROOT -name '*.la' -delete -print

# We don't need a -devel package because only the daemon is supposed to be
# using the library.
rm -rf $RPM_BUILD_ROOT/%{_includedir}
rm -f $RPM_BUILD_ROOT/%{_libdir}/%{name}/libdleyna-server-%{api}.so
rm -rf $RPM_BUILD_ROOT/%{_libdir}/pkgconfig


%files
%license COPYING
%doc AUTHORS
%doc ChangeLog
%doc README
%{_datadir}/dbus-1/services/com.intel.%{name}.service

%dir %{_libdir}/%{name}
%{_libdir}/%{name}/libdleyna-server-%{api}.so.*

%{_libexecdir}/%{name}-service
%config(noreplace) %{_sysconfdir}/%{name}-service.conf


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

* Thu Oct 05 2017 Debarshi Ray <rishi@fedoraproject.org> - 0.5.0-9
- Use arch-specific Requires on dleyna-connector-dbus

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Mar 03 2017 Debarshi Ray <rishi@fedoraproject.org> - 0.5.0-6
- Fix build failure due to missing header

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Sep 16 2016 Debarshi Ray <rishi@fedoraproject.org> - 0.5.0-4
- Fix crash due to double-free when destroying the same dls_upnp_t or
  dls_manager_t twice (RH #1251365)
- Use make_build and make_install macros
- Update minimum required versions; use pkgconfig(...) for BRs
- Miscellaneous clean-ups

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue May 12 2015 Debarshi Ray <rishi@fedoraproject.org> - 0.5.0-1
- Update to 0.5.0

* Mon May 11 2015 Nils Philippsen <nils@redhat.com> - 0.4.0-8
- rebuild for new dleyna-core

* Tue Feb 24 2015 Bastien Nocera <bnocera@redhat.com> 0.4.0-7
- Fix warning on totem startup

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Feb 24 2014 Debarshi Ray <rishi@fedoraproject.org> - 0.4.0-4
- Pass -v to autoreconf and -print to find

* Fri Feb 21 2014 Debarshi Ray <rishi@fedoraproject.org> - 0.4.0-3
- Fix the Source0 as per
  https://fedoraproject.org/wiki/Packaging:SourceURL#Github

* Tue Feb 11 2014 Debarshi Ray <rishi@fedoraproject.org> - 0.4.0-2
- Mention the full commit hash corresponding to the release as per
  https://fedoraproject.org/wiki/Packaging:SourceURL#Github

* Wed Jan 15 2014 Bastien Nocera <bnocera@redhat.com> - 0.4.0-1
- Initial version
