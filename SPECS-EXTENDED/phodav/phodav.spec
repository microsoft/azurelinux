%global gtk_doc 0
Summary:        A WebDAV server using libsoup3
Name:           phodav
Version:        3.0
Release:        6%{?dist}
License:        LGPLv2+
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://wiki.gnome.org/phodav
Source0:        https://download.gnome.org/sources/%{name}/%{version}/%{name}-%{version}.tar.xz
%if %{with gtk_doc}
BuildRequires:  gtk-doc
%endif
BuildRequires:  gettext-devel
BuildRequires:  meson
BuildRequires:  git-core
BuildRequires:  gcc
BuildRequires:  systemd-devel
BuildRequires:  systemd-units
BuildRequires:  libsoup-devel
BuildRequires:  avahi-gobject-devel
BuildRequires:  asciidoc
BuildRequires:  xmlto
BuildRequires:  libxml2-devel

%description
phởdav is a WebDAV server implementation using libsoup3 (RFC 4918).

%package -n     libphodav
Summary:        A library to serve files with WebDAV
Obsoletes:      libphodav-2.0 <= 0:2.0-3
Obsoletes:      libphodav2 <= 0:2.0-4
Obsoletes:      libphodav-1.0 <= 0:0.4-6

%description -n libphodav
phởdav is a WebDAV server implementation using libsoup3 (RFC 4918).
This package provides the library.

%package -n     libphodav-devel
Summary:        Development files for libphodav
Requires:       libphodav%{?_isa} = %{version}-%{release}
Obsoletes:      libphodav-2.0-devel <= 0:2.0-3
Obsoletes:      libphodav2-devel <= 0:2.0-4
Obsoletes:      libphodav-1.0-devel <= 0:0.4-6

%description -n libphodav-devel
The libphodav-devel package includes the header files for libphodav.

%package -n     chezdav
Summary:        A simple WebDAV server program

%description -n chezdav
The chezdav package contains a simple tool to share a directory
with WebDAV. The service is announced over mDNS for clients to discover.

%package -n     spice-webdavd
Summary:        Spice daemon for the DAV channel
Requires:       avahi

Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units

%description -n spice-webdavd
The spice-webdavd package contains a daemon to proxy WebDAV request to
the Spice virtio channel.

%prep
%autosetup -p1

%build
%meson \
    -Dsystemdsystemunitdir=%{_unitdir} \
%if %{with gtk_doc}
    -Dgtk_doc=enabled \
%else
    -Dgtk_doc=disabled \
%endif
    -Dudevrulesdir=%{_udevrulesdir} || cat %_vpath_builddir/meson-logs/meson-log.txt

%meson_build

%install
%meson_install

%find_lang phodav-3.0 --with-gnome

%ldconfig_scriptlets -n libphodav

%post -n spice-webdavd
%systemd_post spice-webdavd.service

%preun -n spice-webdavd
%systemd_preun spice-webdavd.service

%postun -n spice-webdavd
%systemd_postun_with_restart spice-webdavd.service

%files -n libphodav -f phodav-3.0.lang
%license COPYING
%{_libdir}/libphodav-3.0.so.0*

%files -n libphodav-devel
%dir %{_includedir}/libphodav-3.0/
%{_includedir}/libphodav-3.0/*
%{_libdir}/libphodav-3.0.so
%{_libdir}/pkgconfig/libphodav-3.0.pc
%if %{with gtk_doc}
%{_datadir}/gtk-doc/html/phodav-3.0/*
%endif

%files -n chezdav
%{_bindir}/chezdav
%{_mandir}/man1/chezdav.1*

%files -n spice-webdavd
%license COPYING
%{_sbindir}/spice-webdavd
%{_udevrulesdir}/70-spice-webdavd.rules
%{_unitdir}/spice-webdavd.service

%changelog
* Wed Mar 08 2023 Sumedh Sharma <sumsharma@microsoft.com> - 3.0-6
- Initial CBL-Mariner import from Fedora 38 (license: MIT)
- Disable gtk-doc
- license verified

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Jan 09 2023 Yaakov Selkowitz <yselkowi@redhat.com> - 3.0-4
- Fix flatpak build

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jul 04 2022 Marc-André Lureau <marcandre.lureau@redhat.com> - 3.0-2
- BR on libxml2

* Fri Jul 01 2022 Marc-André Lureau <marcandre.lureau@redhat.com> - 3.0-1
- Update to 3.0

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Mar 02 2021 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2.5-4
- Rebuilt for updated systemd-rpm-macros
  See https://pagure.io/fesco/issue/2583.

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Oct 21 12:27:53 +04 2020 Marc-André Lureau <marcandre.lureau@redhat.com> - 2.5-2
- Add avahi dependency for spice-webdavd. Fixes rhbz#1889944

* Thu Aug 27 2020 Marc-André Lureau <marcandre.lureau@redhat.com> - 2.5-1
- new version

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Mar 05 2020 Victor Toso <victortoso@redhat.com> - 2.4-1
- v2.4 release

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Feb 26 2019 Marc-André Lureau <marcandre.lureau@redhat.com> - 2.3-1
- v2.3 release

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Oct 12 2017 Peter Robinson <pbrobinson@fedoraproject.org> 2.2-1
- Update to 2.2
- Modernise spec

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Dec 20 2016 Marc-André Lureau <marcandre.lureau@redhat.com> - 2.1-1
- new version

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Apr 02 2015 Christophe Fergeau <cfergeau@redhat.com> 2.0-4
- Rename package to foo to be consistant with library naming.

* Tue Feb 24 2015 Marc-André Lureau <marcandre.lureau@redhat.com> - 2.0-3
- Rename packages from foo-2.0 to foo2 to be more compliant with other
  Fedora packages names. Fixes: rhbz#1195913

* Tue Feb 24 2015 Marc-André Lureau <marcandre.lureau@redhat.com> - 2.0-2
- Fix gettext and doc to be under -2.0 directories. Fixes: rhbz#1195913

* Sat Feb 21 2015 Marc-André Lureau <marcandre.lureau@redhat.com> - 2.0-1
- Bump to libphodav-2.0

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Thu Jun 12 2014 Yaakov Selkowitz <yselkowi@redhat.com> - 0.4-4
- Fix FTBFS due to Makefiles triggering old automake (#1106318)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon May 5 2014 Marc-André Lureau <marcandre.lureau@redhat.com> - 0.4-2
- Remove systemd target, use only service. rhbz#1087907

* Mon Jan 27 2014 Marc-André Lureau <marcandre.lureau@redhat.com> - 0.4-1
- Initial packaging. rhbz#1059708
