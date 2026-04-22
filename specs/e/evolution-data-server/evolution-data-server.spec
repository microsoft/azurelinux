## START: Set by rpmautospec
## (rpmautospec version 0.8.4)
## RPMAUTOSPEC: autochangelog
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%undefine __cmake_in_source_build

%define ldap_support 1
%define static_ldap 0
%define krb5_support 1
%define largefile_support 1

# disable for i686, because libphonenumber 8.12.57 is not built for it
%ifarch i686
%global phonenum_support 0
%else
# enabled only for Fedora
%global phonenum_support 0%{?fedora}
%endif

# Coverity scan can override this to 0, to skip checking in gtk-doc generated code
%{!?with_docs: %global with_docs 1}

%if 0%{?flatpak}
%global with_docs 0
%endif

%{!?with_webkitgtk: %global with_webkitgtk (%{undefined rhel} || 0%{?rhel} < 10)}

%define glib2_version 2.68
%define gtk3_version 3.20
%define gtk4_version 4.4
%define gtk_doc_version 1.9
%define goa_version 3.8
%define libsecret_version 0.5
%define libgweather_version 4.0
%define libical_version 3.0.16
%define libsoup_version 3.1.1
%define nss_version 3.14
%define sqlite_version 3.7.17
%define webkit2gtk_version 2.34.0
%define webkit2gtk4_version 2.36.0
%define json_glib_version 1.0.4
%define uuid_version 2.0

%define credential_modules_dir %{_libdir}/evolution-data-server/credential-modules
%define camel_provider_dir %{_libdir}/evolution-data-server/camel-providers
%define ebook_backends_dir %{_libdir}/evolution-data-server/addressbook-backends
%define ecal_backends_dir %{_libdir}/evolution-data-server/calendar-backends
%define modules_dir %{_libdir}/evolution-data-server/registry-modules
%define uimodules_dir %{_libdir}/evolution-data-server/ui-modules

%global dbus_service_name_address_book	org.gnome.evolution.dataserver.AddressBook10
%global dbus_service_name_calendar	org.gnome.evolution.dataserver.Calendar8
%global dbus_service_name_sources	org.gnome.evolution.dataserver.Sources5
%global dbus_service_name_user_prompter	org.gnome.evolution.dataserver.UserPrompter0

### Abstract ###

Name: evolution-data-server
Version: 3.58.3
Release: 2%{?dist}
Summary: Backend data server for Evolution
License: LGPL-2.0-or-later
URL: https://gitlab.gnome.org/GNOME/evolution/-/wikis/home
Source: http://download.gnome.org/sources/%{name}/3.58/%{name}-%{version}.tar.xz

# 0-99: General patches
# enable corresponding autopatch below to make them applied

# 100-199: Flatpak-specific patches
# https://gitlab.gnome.org/GNOME/evolution-data-server/-/merge_requests/144
Patch100: Make-DBUS_SERVICES_PREFIX-runtime-configurable.patch

Provides: evolution-webcal = %{version}
Obsoletes: evolution-webcal < 2.24.0

# RH-bug #1362477
Recommends: pinentry-gui

%if 0%{?fedora}
# From rhughes-f20-gnome-3-12 copr
Obsoletes: compat-evolution-data-server310-libcamel < 3.12
%endif

### Dependencies ###

Requires: %{name}-langpacks = %{version}-%{release}

### Build Dependencies ###

BuildRequires: cmake
BuildRequires: gcc
BuildRequires: gcc-c++
BuildRequires: gettext
BuildRequires: gperf
%if %{with_docs}
BuildRequires: gtk-doc >= %{gtk_doc_version}
%endif
BuildRequires: vala
BuildRequires: systemd

BuildRequires: pkgconfig(gio-2.0) >= %{glib2_version}
BuildRequires: pkgconfig(gio-unix-2.0) >= %{glib2_version}
BuildRequires: pkgconfig(gmodule-2.0) >= %{glib2_version}
BuildRequires: pkgconfig(icu-i18n)
BuildRequires: pkgconfig(gtk+-3.0) >= %{gtk3_version}
BuildRequires: pkgconfig(gtk4) >= %{gtk4_version}
BuildRequires: pkgconfig(goa-1.0) >= %{goa_version}
BuildRequires: pkgconfig(gweather4) >= %{libgweather_version}
BuildRequires: pkgconfig(libical-glib) >= %{libical_version}
BuildRequires: pkgconfig(libsecret-unstable) >= %{libsecret_version}
BuildRequires: pkgconfig(libsoup-3.0) >= %{libsoup_version}
BuildRequires: pkgconfig(libxml-2.0)
BuildRequires: pkgconfig(nspr)
BuildRequires: pkgconfig(nss) >= %{nss_version}
BuildRequires: pkgconfig(sqlite3) >= %{sqlite_version}
BuildRequires: pkgconfig(uuid) >= %{uuid_version}
%if %{with_webkitgtk}
BuildRequires: pkgconfig(webkit2gtk-4.1) >= %{webkit2gtk_version}
BuildRequires: pkgconfig(webkitgtk-6.0) >= %{webkit2gtk4_version}
%endif
BuildRequires: pkgconfig(json-glib-1.0) >= %{json_glib_version}
BuildRequires: pkgconfig(libcanberra-gtk3)

%if %{ldap_support}
BuildRequires: openldap-devel >= 2.0.11
%if %{static_ldap}
BuildRequires: pkgconfig(openssl)
%endif
%endif

%if %{krb5_support}
BuildRequires: krb5-devel >= 1.11
%endif

%if %{phonenum_support}
BuildRequires: libphonenumber-devel
BuildRequires: protobuf-devel
BuildRequires: boost-devel
BuildRequires: abseil-cpp-devel
%endif

# libical 3.0.16 added new API, this ensures to bring it in
Requires: libical-glib >= %{libical_version}

%description
The %{name} package provides a unified backend for programs that work
with contacts, tasks, and calendar information.

It was originally developed for Evolution (hence the name), but is now used
by other packages.

%package devel
Summary: Development files for building against %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}

Requires: pkgconfig(goa-1.0) >= %{goa_version}
Requires: pkgconfig(gweather4) >= %{libgweather_version}
Requires: pkgconfig(libical-glib) >= %{libical_version}
Requires: pkgconfig(libsecret-unstable) >= %{libsecret_version}
Requires: pkgconfig(libsoup-3.0) >= %{libsoup_version}
Requires: pkgconfig(sqlite3) >= %{sqlite_version}
%if %{with_webkitgtk}
Requires: pkgconfig(webkit2gtk-4.1) >= %{webkit2gtk_version}
Requires: pkgconfig(webkitgtk-6.0) >= %{webkit2gtk4_version}
%endif
Requires: pkgconfig(json-glib-1.0) >= %{json_glib_version}

%description devel
Development files needed for building things which link against %{name}.

%package langpacks
Summary: Translations for %{name}
BuildArch: noarch
Requires: %{name} = %{version}-%{release}

%description langpacks
This package contains translations for %{name}.

%if %{with_docs}

%package doc
Summary: Documentation files for %{name}
BuildArch: noarch

%description doc
This package contains developer documentation for %{name}.

# %%{with_docs}
%endif

%package perl
Summary: Supplemental utilities that require Perl
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: perl-interpreter

%description perl
This package contains supplemental utilities for %{name} that require Perl.

%package tests
Summary: Tests for the %{name} package
Requires: %{name}%{?_isa} = %{version}-%{release}

%description tests
The %{name}-tests package contains tests that can be used to verify
the functionality of the installed %{name} package.

%prep
%autosetup -p1 -S gendiff -N

# General patches
# %%autopatch -p1 -m 0 -M 99

# Flatpak-specific patches
%if 0%{?flatpak}
%autopatch -p1 -m 100 -M 199
%endif

%build

%if %{ldap_support}

%if %{static_ldap}
%define ldap_flags -DWITH_OPENLDAP=ON -DWITH_STATIC_LDAP=ON
# Set LIBS so that configure will be able to link with static LDAP libraries,
# which depend on Cyrus SASL and OpenSSL.  XXX Is the "else" clause necessary?
if pkg-config openssl ; then
	export LIBS="-lsasl2 `pkg-config --libs openssl`"
else
	export LIBS="-lsasl2 -lssl -lcrypto"
fi
# newer versions of openldap are built with Mozilla NSS crypto, so also need
# those libs to link with the static ldap libs
if pkg-config nss ; then
    export LIBS="$LIBS `pkg-config --libs nss`"
else
    export LIBS="$LIBS -lssl3 -lsmime3 -lnss3 -lnssutil3 -lplds4 -lplc4 -lnspr4"
fi
%else
%define ldap_flags -DWITH_OPENLDAP=ON
%endif

%else
%define ldap_flags -DWITH_OPENLDAP=OFF
%endif

%if %{krb5_support}
%define krb5_flags -DWITH_KRB5=ON
%else
%define krb5_flags -DWITH_KRB5=OFF
%endif

%if %{largefile_support}
%define largefile_flags -DENABLE_LARGEFILE=ON
%else
%define largefile_flags -DENABLE_LARGEFILE=OFF
%endif

%if %{phonenum_support}
%define phonenum_flags -DWITH_PHONENUMBER=ON
%else
%define phonenum_flags -DWITH_PHONENUMBER=OFF
%endif

%define ssl_flags -DENABLE_SMIME=ON

%if %{with_docs}
%define gtkdoc_flags -DENABLE_GTK_DOC=ON
%else
%define gtkdoc_flags -DENABLE_GTK_DOC=OFF
%endif

%if %{with_webkitgtk}
%define webkitgtk_flags -DENABLE_OAUTH2_WEBKITGTK=ON -DENABLE_OAUTH2_WEBKITGTK4=ON
%else
%define webkitgtk_flags -DENABLE_OAUTH2_WEBKITGTK=OFF -DENABLE_OAUTH2_WEBKITGTK4=OFF
%endif

if ! pkg-config --exists nss; then
  echo "Unable to find suitable version of nss to use!"
  exit 1
fi

export CPPFLAGS="-I%{_includedir}/et"
export CFLAGS="$RPM_OPT_FLAGS -DLDAP_DEPRECATED -fPIC -I%{_includedir}/et -Wno-deprecated-declarations"

%cmake -DENABLE_MAINTAINER_MODE=OFF \
	-DENABLE_FILE_LOCKING=fcntl \
	-DENABLE_DOT_LOCKING=OFF \
	-DENABLE_INTROSPECTION=ON \
	-DENABLE_VALA_BINDINGS=ON \
	-DENABLE_INSTALLED_TESTS=ON \
	-DWITH_LIBDB=OFF \
        -DWITH_SYSTEMDUSERUNITDIR=%{_userunitdir} \
	%ldap_flags %krb5_flags %ssl_flags %webkitgtk_flags \
	%largefile_flags %gtkdoc_flags %phonenum_flags \
	-DINCLUDE_INSTALL_DIR:PATH=%{_includedir} \
	-DLIB_INSTALL_DIR:PATH=%{_libdir} \
	-DSYSCONF_INSTALL_DIR:PATH=%{_sysconfdir} \
	-DSHARE_INSTALL_PREFIX:PATH=%{_datadir} \
	%if "%{?_lib}" == "lib64"
		-DLIB_SUFFIX=64 \
	%endif
	%{nil}

%cmake_build

%install
%cmake_install

# make sure the directory exists, because it's owned by eds
mkdir $RPM_BUILD_ROOT/%{uimodules_dir} || :
mkdir $RPM_BUILD_ROOT/%{credential_modules_dir} || :

# give the libraries some executable bits
find $RPM_BUILD_ROOT -name '*.so.*' -exec chmod +x {} \;

%find_lang %{name}

%files
%license COPYING
%doc README ChangeLog NEWS
%{_libdir}/libcamel-1.2.so.66
%{_libdir}/libcamel-1.2.so.66.0.0
%{_libdir}/libebackend-1.2.so.11
%{_libdir}/libebackend-1.2.so.11.0.0
%{_libdir}/libebook-1.2.so.21
%{_libdir}/libebook-1.2.so.21.1.3
%{_libdir}/libebook-contacts-1.2.so.4
%{_libdir}/libebook-contacts-1.2.so.4.0.0
%{_libdir}/libecal-2.0.so.3
%{_libdir}/libecal-2.0.so.3.0.0
%{_libdir}/libedata-book-1.2.so.27
%{_libdir}/libedata-book-1.2.so.27.0.0
%{_libdir}/libedata-cal-2.0.so.2
%{_libdir}/libedata-cal-2.0.so.2.0.0
%{_libdir}/libedataserver-1.2.so.27
%{_libdir}/libedataserver-1.2.so.27.0.0
%{_libdir}/libedataserverui-1.2.so.4
%{_libdir}/libedataserverui-1.2.so.4.0.0
%{_libdir}/libedataserverui4-1.0.so.0
%{_libdir}/libedataserverui4-1.0.so.0.0.0

%{_libdir}/girepository-1.0/Camel-1.2.typelib
%{_libdir}/girepository-1.0/EBackend-1.2.typelib
%{_libdir}/girepository-1.0/EBook-1.2.typelib
%{_libdir}/girepository-1.0/EBookContacts-1.2.typelib
%{_libdir}/girepository-1.0/ECal-2.0.typelib
%{_libdir}/girepository-1.0/EDataBook-1.2.typelib
%{_libdir}/girepository-1.0/EDataCal-2.0.typelib
%{_libdir}/girepository-1.0/EDataServer-1.2.typelib
%{_libdir}/girepository-1.0/EDataServerUI-1.2.typelib
%{_libdir}/girepository-1.0/EDataServerUI4-1.0.typelib

%{_libexecdir}/camel-gpg-photo-saver
%{_libexecdir}/camel-index-control-1.2
%{_libexecdir}/camel-lock-helper-1.2
%{_libexecdir}/evolution-addressbook-factory
%{_libexecdir}/evolution-addressbook-factory-subprocess
%{_libexecdir}/evolution-calendar-factory
%{_libexecdir}/evolution-calendar-factory-subprocess
%{_libexecdir}/evolution-scan-gconf-tree-xml
%{_libexecdir}/evolution-source-registry
%{_libexecdir}/evolution-user-prompter

%dir %{_libexecdir}/evolution-data-server
%{_libexecdir}/evolution-data-server/addressbook-export
%{_libexecdir}/evolution-data-server/evolution-alarm-notify
%{_libexecdir}/evolution-data-server/evolution-oauth2-handler
%{_libexecdir}/evolution-data-server/list-sources
%if 0%{?flatpak}
%{_libexecdir}/evolution-data-server/set-dbus-prefix
%endif

%{_sysconfdir}/xdg/autostart/org.gnome.Evolution-alarm-notify.desktop
%{_datadir}/applications/org.gnome.Evolution-alarm-notify.desktop
%{_datadir}/applications/org.gnome.evolution-data-server.OAuth2-handler.desktop

# GSettings schemas:
%{_datadir}/GConf/gsettings/evolution-data-server.convert
%{_datadir}/glib-2.0/schemas/org.gnome.Evolution.DefaultSources.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnome.evolution-data-server.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnome.evolution-data-server.addressbook.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnome.evolution-data-server.calendar.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnome.evolution.eds-shell.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnome.evolution.shell.network-config.gschema.xml

%{_datadir}/evolution-data-server
%{_datadir}/dbus-1/services/%{dbus_service_name_address_book}.service
%{_datadir}/dbus-1/services/%{dbus_service_name_calendar}.service
%{_datadir}/dbus-1/services/%{dbus_service_name_sources}.service
%{_datadir}/dbus-1/services/%{dbus_service_name_user_prompter}.service
%{_datadir}/pixmaps/evolution-data-server
%{_datadir}/icons/hicolor/scalable/apps/org.gnome.Evolution-alarm-notify.svg

%{_userunitdir}/evolution-addressbook-factory.service
%{_userunitdir}/evolution-calendar-factory.service
%{_userunitdir}/evolution-source-registry.service
%{_userunitdir}/evolution-user-prompter.service
%{_userunitdir}/evolution-alarm-notify.service

%dir %{_libdir}/evolution-data-server
%dir %{credential_modules_dir}
%dir %{camel_provider_dir}
%dir %{ebook_backends_dir}
%dir %{ecal_backends_dir}
%dir %{modules_dir}
%dir %{uimodules_dir}

%{_libdir}/evolution-data-server/libedbus-private.so

# Camel providers:
%{camel_provider_dir}/libcamelimapx.so
%{camel_provider_dir}/libcamelimapx.urls

%{camel_provider_dir}/libcamellocal.so
%{camel_provider_dir}/libcamellocal.urls

%{camel_provider_dir}/libcamelnntp.so
%{camel_provider_dir}/libcamelnntp.urls

%{camel_provider_dir}/libcamelpop3.so
%{camel_provider_dir}/libcamelpop3.urls

%{camel_provider_dir}/libcamelsendmail.so
%{camel_provider_dir}/libcamelsendmail.urls

%{camel_provider_dir}/libcamelsmtp.so
%{camel_provider_dir}/libcamelsmtp.urls

# e-d-s extensions:
%{credential_modules_dir}/module-credentials-goa.so
%{ebook_backends_dir}/libebookbackendcarddav.so
%{ebook_backends_dir}/libebookbackendfile.so
%{ebook_backends_dir}/libebookbackendldap.so
%{ecal_backends_dir}/libecalbackendcaldav.so
%{ecal_backends_dir}/libecalbackendcontacts.so
%{ecal_backends_dir}/libecalbackendfile.so
%{ecal_backends_dir}/libecalbackendgtasks.so
%{ecal_backends_dir}/libecalbackendhttp.so
%{ecal_backends_dir}/libecalbackendweather.so
%{ecal_backends_dir}/libecalbackendwebdavnotes.so
%{modules_dir}/module-cache-reaper.so
%{modules_dir}/module-google-backend.so
%{modules_dir}/module-gnome-online-accounts.so
%{modules_dir}/module-oauth2-services.so
%{modules_dir}/module-outlook-backend.so
%{modules_dir}/module-secret-monitor.so
%{modules_dir}/module-trust-prompt.so
%{modules_dir}/module-webdav-backend.so
%{modules_dir}/module-yahoo-backend.so

%files devel
%{_includedir}/evolution-data-server
%{_libdir}/libcamel-1.2.so
%{_libdir}/libebackend-1.2.so
%{_libdir}/libebook-1.2.so
%{_libdir}/libebook-contacts-1.2.so
%{_libdir}/libecal-2.0.so
%{_libdir}/libedata-book-1.2.so
%{_libdir}/libedata-cal-2.0.so
%{_libdir}/libedataserver-1.2.so
%{_libdir}/libedataserverui-1.2.so
%{_libdir}/libedataserverui4-1.0.so
%{_libdir}/pkgconfig/camel-1.2.pc
%{_libdir}/pkgconfig/evolution-data-server-1.2.pc
%{_libdir}/pkgconfig/libebackend-1.2.pc
%{_libdir}/pkgconfig/libebook-1.2.pc
%{_libdir}/pkgconfig/libebook-contacts-1.2.pc
%{_libdir}/pkgconfig/libecal-2.0.pc
%{_libdir}/pkgconfig/libedata-book-1.2.pc
%{_libdir}/pkgconfig/libedata-cal-2.0.pc
%{_libdir}/pkgconfig/libedataserver-1.2.pc
%{_libdir}/pkgconfig/libedataserverui-1.2.pc
%{_libdir}/pkgconfig/libedataserverui4-1.0.pc
%{_datadir}/gir-1.0/Camel-1.2.gir
%{_datadir}/gir-1.0/EBackend-1.2.gir
%{_datadir}/gir-1.0/EBook-1.2.gir
%{_datadir}/gir-1.0/EBookContacts-1.2.gir
%{_datadir}/gir-1.0/ECal-2.0.gir
%{_datadir}/gir-1.0/EDataBook-1.2.gir
%{_datadir}/gir-1.0/EDataCal-2.0.gir
%{_datadir}/gir-1.0/EDataServer-1.2.gir
%{_datadir}/gir-1.0/EDataServerUI-1.2.gir
%{_datadir}/gir-1.0/EDataServerUI4-1.0.gir
%{_datadir}/vala/vapi/camel-1.2.deps
%{_datadir}/vala/vapi/camel-1.2.vapi
%{_datadir}/vala/vapi/libebackend-1.2.deps
%{_datadir}/vala/vapi/libebackend-1.2.vapi
%{_datadir}/vala/vapi/libebook-1.2.deps
%{_datadir}/vala/vapi/libebook-1.2.vapi
%{_datadir}/vala/vapi/libebook-contacts-1.2.deps
%{_datadir}/vala/vapi/libebook-contacts-1.2.vapi
%{_datadir}/vala/vapi/libecal-2.0.deps
%{_datadir}/vala/vapi/libecal-2.0.vapi
%{_datadir}/vala/vapi/libedata-book-1.2.deps
%{_datadir}/vala/vapi/libedata-book-1.2.vapi
%{_datadir}/vala/vapi/libedata-cal-2.0.deps
%{_datadir}/vala/vapi/libedata-cal-2.0.vapi
%{_datadir}/vala/vapi/libedataserver-1.2.deps
%{_datadir}/vala/vapi/libedataserver-1.2.vapi
%{_datadir}/vala/vapi/libedataserverui-1.2.deps
%{_datadir}/vala/vapi/libedataserverui-1.2.vapi
%{_datadir}/vala/vapi/libedataserverui4-1.0.deps
%{_datadir}/vala/vapi/libedataserverui4-1.0.vapi

%files langpacks -f %{name}.lang

%if %{with_docs}

%files doc
%{_datadir}/gtk-doc/html/*

%endif

%files perl
%{_libexecdir}/evolution-data-server/csv2vcard

%files tests
%{_libdir}/libetestserverutils.so
%{_libdir}/libetestserverutils.so.0
%{_libdir}/libetestserverutils.so.0.0.0
%{_libexecdir}/%{name}/installed-tests
%{_datadir}/installed-tests

%changelog
## START: Generated by rpmautospec
* Wed Apr 22 2026 azldev <azurelinux@microsoft.com> - 3.58.3-2
- Latest state for evolution-data-server

* Fri Jan 30 2026 Milan Crha <mcrha@redhat.com> - 3.58.3-1
- Update to 3.58.3

* Fri Nov 21 2025 Milan Crha <mcrha@redhat.com> - 3.58.2-1
- Update to 3.58.2

* Fri Oct 10 2025 Milan Crha <mcrha@redhat.com> - 3.58.1-1
- Update to 3.58.1

* Mon Oct 06 2025 Yaakov Selkowitz <yselkowi@redhat.com> - 3.58.0-2
- Update flatpak dbus services prefix patch

* Fri Sep 12 2025 Milan Crha <mcrha@redhat.com> - 3.58.0-1
- Update to 3.58.0

* Fri Aug 29 2025 Milan Crha <mcrha@redhat.com> - 3.57.3-1
- Update to 3.57.3

* Wed Aug 06 2025 František Zatloukal <fzatlouk@redhat.com> - 3.57.2-2
- Rebuilt for icu 77.1

* Fri Aug 01 2025 Milan Crha <mcrha@redhat.com> - 3.57.2-1
- Update to 3.57.2

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.57.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jul 17 2025 Milan Crha <mcrha@redhat.com> - 3.57.1-2
- Do not force a CMake build system generator

* Fri Jun 27 2025 Milan Crha <mcrha@redhat.com> - 3.57.1-1
- Update to 3.57.1

* Fri May 23 2025 Milan Crha <mcrha@redhat.com> - 3.56.2-1
- Update to 3.56.2

* Fri Apr 11 2025 Milan Crha <mcrha@redhat.com> - 3.56.1-1
- Update to 3.56.1

* Sun Mar 16 2025 Yaakov Selkowitz <yselkowi@redhat.com> - 3.56.0-3
- Update flatpak patch

* Fri Mar 14 2025 Milan Crha <mcrha@redhat.com> - 3.56.0-2
- Temporarily adapt to CMake macro changes

* Fri Mar 14 2025 Milan Crha <mcrha@redhat.com> - 3.56.0-1
- Update to 3.56.0

* Fri Feb 28 2025 Milan Crha <mcrha@redhat.com> - 3.55.3-1
- Update to 3.55.3

* Fri Jan 31 2025 Milan Crha <mcrha@redhat.com> - 3.55.2-1
- Update to 3.55.2

* Thu Jan 23 2025 Milan Crha <mcrha@redhat.com> - 3.55.1-3
- Add patch to replace variables named 'bool', which C23 considers keyword

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.55.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Jan 07 2025 Milan Crha <mcrha@redhat.com> - 3.55.1-1
- Update to 3.55.1

* Fri Dec 13 2024 Adam Williamson <awilliam@redhat.com> - 3.54.2-3
- Rebuild for new libphonenumber

* Sun Dec 08 2024 Pete Walter <pwalter@fedoraproject.org> - 3.54.2-2
- Rebuild for ICU 76

* Fri Nov 22 2024 Milan Crha <mcrha@redhat.com> - 3.54.2-1
- Update to 3.54.2

* Mon Nov 18 2024 Adam Williamson <awilliam@redhat.com> - 3.54.1-3
- Backport MR #166 to fix build with GTK 4.17+

* Mon Nov 18 2024 Adam Williamson <awilliam@redhat.com> - 3.54.1-2
- Rebuild for libphonenumber 8.13.50

* Fri Oct 18 2024 Milan Crha <mcrha@redhat.com> - 3.54.1-1
- Update to 3.54.1

* Fri Sep 13 2024 Milan Crha <mcrha@redhat.com> - 3.54.0-1
- Update to 3.54.0

* Fri Aug 30 2024 Milan Crha <mcrha@redhat.com> - 3.53.3-1
- Update to 3.53.3

* Fri Aug 02 2024 Milan Crha <mcrha@redhat.com> - 3.53.2-2
- Add 'uuid' build dependency

* Fri Aug 02 2024 Milan Crha <mcrha@redhat.com> - 3.53.2-1
- Update to 3.53.2

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.53.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 28 2024 Milan Crha <mcrha@redhat.com> - 3.53.1-1
- Update to 3.53.1

* Fri May 24 2024 Milan Crha <mcrha@redhat.com> - 3.52.2-1
- Update to 3.52.2

* Fri Apr 19 2024 Milan Crha <mcrha@redhat.com> - 3.52.1-1
- Update to 3.52.1

* Tue Mar 26 2024 Milan Crha <mcrha@redhat.com> - 3.52.0-2
- Update URL to point to the new Wiki space

* Fri Mar 15 2024 Milan Crha <mcrha@redhat.com> - 3.52.0-1
- Update to 3.52.0

* Fri Mar 01 2024 Milan Crha <mcrha@redhat.com> - 3.51.3-1
- Update to 3.51.3

* Fri Mar 01 2024 Owen W. Taylor <otaylor@fishsoup.net> - 3.51.2-3
- Add patch to allow reconfiguring the dbus-prefix without rebuilding.

* Fri Feb 09 2024 Milan Crha <mcrha@redhat.com> - 3.51.2-2
- Add org.gnome.Evolution-alarm-notify.svg

* Fri Feb 09 2024 Milan Crha <mcrha@redhat.com> - 3.51.2-1
- Update to 3.51.2

* Wed Jan 31 2024 Pete Walter <pwalter@fedoraproject.org> - 3.51.1-6
- Rebuild for ICU 74

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.51.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.51.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 08 2024 Milan Crha <mcrha@redhat.com> - 3.51.1-3
- Add a patch to fix a build

* Fri Jan 05 2024 Milan Crha <mcrha@redhat.com> - 3.51.1-2
- Bump libecal-2.0 soname version

* Fri Jan 05 2024 Milan Crha <mcrha@redhat.com> - 3.51.1-1
- Update to 3.51.1

* Tue Dec 19 2023 Florian Weimer <fweimer@redhat.com> - 3.50.2-3
- Backport upstream patch to fix C issue in CMake probing

* Fri Dec 01 2023 Milan Crha <mcrha@redhat.com> - 3.50.2-2
- Add OAuth2 handler bits into the .spec file

* Fri Dec 01 2023 Milan Crha <mcrha@redhat.com> - 3.50.2-1
- Update to 3.50.2

* Fri Oct 20 2023 Milan Crha <mcrha@redhat.com> - 3.50.1-1
- Update to 3.50.1

* Fri Sep 15 2023 Milan Crha <mcrha@redhat.com> - 3.50.0-1
- Update to 3.50.0

* Fri Sep 01 2023 Milan Crha <mcrha@redhat.com> - 3.49.3-1
- Update to 3.49.3

* Fri Aug 04 2023 Milan Crha <mcrha@redhat.com> - 3.49.2-1
- Update to 3.49.2

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.49.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jul 11 2023 František Zatloukal <fzatlouk@redhat.com> - 3.49.1-2
- Rebuilt for ICU 73.2

* Fri Jun 30 2023 Milan Crha <mcrha@redhat.com> - 3.49.1-1
- Update to 3.49.1

* Wed Jun 21 2023 Milan Crha <mcrha@redhat.com> - 3.48.3-2
- Make it possible to build without WebKitGTK dependency

* Fri Jun 02 2023 Milan Crha <mcrha@redhat.com> - 3.48.3-1
- Update to 3.48.3

* Fri May 26 2023 Milan Crha <mcrha@redhat.com> - 3.48.2-1
- Update to 3.48.2

* Wed May 17 2023 Sérgio M. Basto <sergio@serjux.com> - 3.48.1-2
- Rebuild for libphonenumber-8.13.x

* Fri Apr 21 2023 Milan Crha <mcrha@redhat.com> - 3.48.1-1
- Update to 3.48.1

* Fri Mar 17 2023 Milan Crha <mcrha@redhat.com> - 3.48.0-1
- Update to 3.48.0

* Thu Mar 09 2023 Michael Catanzaro <mcatanzaro@redhat.com> - 3.47.3-3
- Really rebuild against WebKitGTK 2.39.91

* Thu Mar 09 2023 Michael Catanzaro <mcatanzaro@redhat.com> - 3.47.3-2
- Rebuild for WebKitGTK 2.39.91

* Fri Mar 03 2023 Milan Crha <mcrha@redhat.com> - 3.47.3-1
- Update to 3.47.3

* Wed Feb 22 2023 Michael Catanzaro <mcatanzaro@redhat.com> - 3.47.2-3
- Really rebuild for WebKitGTK 2.39.90

* Wed Feb 22 2023 Michael Catanzaro <mcatanzaro@redhat.com> - 3.47.2-2
- Rebuild for WebKitGTK 2.39.90

* Fri Feb 10 2023 Milan Crha <mcrha@redhat.com> - 3.47.2-1
- Update to 3.47.2

* Wed Feb 01 2023 Michael Catanzaro <mcatanzaro@redhat.com> - 3.47.1-4
- Build against WebKitGTK 2.39.6

* Sat Jan 21 2023 Michael Catanzaro <mcatanzaro@redhat.com> - 3.47.1-3
- Build for WebKitGTK 2.39.5

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.47.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jan 06 2023 Milan Crha <mcrha@redhat.com> - 3.47.1-1
- Update to 3.47.1; Require libical 3.0.16 for added new API

* Sat Dec 31 2022 Pete Walter <pwalter@fedoraproject.org> - 3.46.2-6
- Rebuild for ICU 72

* Tue Dec 06 2022 David King <amigadave@amigadave.com> - 3.46.2-5
- Fix webkitgtk BuildRequires

* Mon Dec 05 2022 Michael Catanzaro <mcatanzaro@redhat.com> - 3.46.2-4
- Build against webkitgtk-6.0

* Mon Dec 05 2022 Milan Crha <mcrha@redhat.com> - 3.46.2-3
- Disable libphonenumber support under i686

* Mon Dec 05 2022 Milan Crha <mcrha@redhat.com> - 3.46.2-2
- Add 'BuildRequires: abseil-cpp-devel' when building with libphonenumber

* Fri Dec 02 2022 Milan Crha <mcrha@redhat.com> - 3.46.2-1
- Update to 3.46.2

* Thu Nov 10 2022 Milan Crha <mcrha@redhat.com> - 3.46.1-2
- Update License tag to SPDX

* Fri Oct 21 2022 Milan Crha <mcrha@redhat.com> - 3.46.1-1
- Update to 3.46.1

* Fri Sep 16 2022 Milan Crha <mcrha@redhat.com> - 3.46.0-1
- Update to 3.46.0

* Fri Sep 02 2022 Milan Crha <mcrha@redhat.com> - 3.45.3-1
- Update to 3.45.3

* Thu Aug 18 2022 Milan Crha <mcrha@redhat.com> - 3.45.2-2
- Add rpminspect.yaml (settings for the RUNPATH test)

* Fri Aug 05 2022 Milan Crha <mcrha@redhat.com> - 3.45.2-1
- Update to 3.45.2

* Mon Aug 01 2022 František Zatloukal <fzatlouk@redhat.com> - 3.45.1-3
- Rebuilt for ICU 71.1

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.45.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue Jul 19 2022 Milan Crha <mcrha@redhat.com> - 3.45.1-1
- Update to 3.45.1 (with some temporarily disabled parts)

* Mon Jul 18 2022 Milan Crha <mcrha@redhat.com> - 3.44.3-2
- Add patch for RH bug #2107751 (glib2's G_TLS_CERTIFICATE_FLAGS_NONE
  causes infinite loop)

* Fri Jul 01 2022 Milan Crha <mcrha@redhat.com> - 3.44.3-1
- Update to 3.44.3

* Fri May 27 2022 Milan Crha <mcrha@redhat.com> - 3.44.2-1
- Update to 3.44.2

* Fri Apr 22 2022 Milan Crha <mcrha@redhat.com> - 3.44.1-1
- Update to 3.44.1

* Fri Mar 18 2022 Milan Crha <mcrha@redhat.com> - 3.44.0-1
- Update to 3.44.0

* Fri Mar 04 2022 Milan Crha <mcrha@redhat.com> - 3.43.3-1
- Update to 3.43.3

* Fri Feb 11 2022 Milan Crha <mcrha@redhat.com> - 3.43.2-1
- Update to 3.43.2

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.43.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jan 07 2022 Milan Crha <mcrha@redhat.com> - 3.43.1.1-1
- Update to 3.43.1.1

* Fri Dec 03 2021 Milan Crha <mcrha@redhat.com> - 3.42.2-1
- Update to 3.42.2

* Sat Nov 06 2021 Adrian Reber <adrian@lisas.de> - 3.42.1-3
- Rebuilt for protobuf 3.19.0

* Fri Nov 05 2021 Milan Crha <mcrha@redhat.com> - 3.42.1-2
- Add patch to correct ICalCompIter component's usage

* Fri Oct 29 2021 Milan Crha <mcrha@redhat.com> - 3.42.1-1
- Update to 3.42.1

* Thu Oct 28 2021 Adam Williamson <awilliam@redhat.com> - 3.42.0-2
- Rebuild with newer protobuf and libphonenumber

* Fri Sep 17 2021 Milan Crha <mcrha@redhat.com> - 3.42.0-1
- Update to 3.42.0

* Fri Sep 03 2021 Milan Crha <mcrha@redhat.com> - 3.41.3-1
- Update to 3.41.3

* Fri Aug 13 2021 Milan Crha <mcrha@redhat.com> - 3.41.2-1
- Update to 3.41.2

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.41.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jul 09 2021 Milan Crha <mcrha@redhat.com> - 3.41.1-2
- Remove reference to dropped file libebookbackendgoogle.so

* Fri Jul 09 2021 Milan Crha <mcrha@redhat.com> - 3.41.1-1
- Update to 3.41.1

* Fri Jun 04 2021 Milan Crha <mcrha@redhat.com> - 3.40.2-1
- Update to 3.40.2

* Wed May 19 2021 Pete Walter <pwalter@fedoraproject.org> - 3.40.1-2
- Rebuild for ICU 69

* Fri Apr 30 2021 Milan Crha <mcrha@redhat.com> - 3.40.1-1
- Update to 3.40.1

* Mon Mar 29 2021 Milan Crha <mcrha@redhat.com> - 3.40.0-4
- Resolves: #1943818 (ESourceWebDAV: Fallback to SHA1 on SSL trust
  verification if needed)

* Fri Mar 26 2021 Kalev Lember <klember@redhat.com> - 3.40.0-3
- Don't use ldconfig_scriptlets

* Fri Mar 26 2021 Kalev Lember <klember@redhat.com> - 3.40.0-2
- Drop unnecessary requires on dconf

* Fri Mar 19 2021 Milan Crha <mcrha@redhat.com> - 3.40.0-1
- Update to 3.40.0

* Fri Mar 12 2021 Milan Crha <mcrha@redhat.com> - 3.39.3-1
- Update to 3.39.3

* Sat Feb 13 2021 Kalev Lember <klember@redhat.com> - 3.39.2-4
- Drop temporary ABI compat

* Fri Feb 12 2021 Kalev Lember <klember@redhat.com> - 3.39.2-3
- Keep temporary ABI compat with previous soname

* Fri Feb 12 2021 Milan Crha <mcrha@redhat.com> - 3.39.2-2
- Bump soname versions for libedataserver/libedataserverui

* Fri Feb 12 2021 Milan Crha <mcrha@redhat.com> - 3.39.2-1
- Update to 3.39.2

* Tue Feb 09 2021 Kalev Lember <klember@redhat.com> - 3.39.1-4
- Simplify flatpak conditionals

* Fri Feb 05 2021 Kalev Lember <klember@redhat.com> - 3.39.1-3
- Recommend pinentry-gui virtual provide, rather than pinentry-gtk

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.39.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Jan 08 2021 Milan Crha <mcrha@redhat.com> - 3.39.1-1
- Update to 3.39.1

* Fri Nov 27 2020 Milan Crha <mcrha@redhat.com> - 3.38.2-2
- Enable libphonenumber usage only for Fedora

* Fri Nov 20 2020 Milan Crha <mcrha@redhat.com> - 3.38.2-1
- Update to 3.38.2

* Mon Oct 05 2020 Milan Crha <mcrha@redhat.com> - 3.38.1-3
- Replace perl-generators build time dependency with perl-interpreter
  install time dependency

* Mon Oct 05 2020 Milan Crha <mcrha@redhat.com> - 3.38.1-2
- Correct D-Bus service file name - it can change when
  _eds_dbus_services_prefix is defined

* Fri Oct 02 2020 Milan Crha <mcrha@redhat.com> - 3.38.1-1
- Update to 3.38.1

* Sat Sep 26 2020 Adrian Reber <adrian@lisas.de> - 3.38.0-2
- Rebuilt for protobuf 3.13

* Fri Sep 11 2020 Milan Crha <mcrha@redhat.com> - 3.38.0-1
- Update to 3.38.0

* Fri Sep 04 2020 Milan Crha <mcrha@redhat.com> - 3.37.92-1
- Update to 3.37.92

* Fri Aug 07 2020 Milan Crha <mcrha@redhat.com> - 3.37.90-1
- Update to 3.37.90

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.37.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 20 2020 Igor Raits <ignatenkobrain@fedoraproject.org> - 3.37.3-4
- Improve compatibility with new CMake macro

* Tue Jul 14 2020 Milan Crha <mcrha@redhat.com> - 3.37.3-3
- Rebuild in a side tag for bodhi, to be able to create an update

* Fri Jul 03 2020 Milan Crha <mcrha@redhat.com> - 3.37.3-2
- Add a patch for missing G_BEGIN_DECLS in e-soup-logger.h

* Fri Jul 03 2020 Milan Crha <mcrha@redhat.com> - 3.37.3-1
- Update to 3.37.3

* Tue Jun 23 2020 Adam Williamson <awilliam@redhat.com> - 3.37.2-2
- Rebuild with newer protobuf and libphonenumber, backport fixes

* Fri May 29 2020 Milan Crha <mcrha@redhat.com> - 3.37.2-1
- Update to 3.37.2

* Sun May 17 2020 Pete Walter <pwalter@fedoraproject.org> - 3.37.1-3
- Rebuild for ICU 67

* Fri Apr 24 2020 Milan Crha <mcrha@redhat.com> - 3.37.1-2
- Add new libecalbackendwebdavnotes.so into the .spec file

* Fri Apr 24 2020 Milan Crha <mcrha@redhat.com> - 3.37.1-1
- Update to 3.37.1

* Wed Apr 01 2020 Nikhil Jha <hi@nikhiljha.com> - 3.36.1-3
- Build with phonenumber support

* Mon Mar 30 2020 Milan Crha <mcrha@redhat.com> - 3.36.1-2
- Remove libdb dependency

* Fri Mar 27 2020 Milan Crha <mcrha@redhat.com> - 3.36.1-1
- Update to 3.36.1

* Fri Mar 06 2020 Milan Crha <mcrha@redhat.com> - 3.36.0-1
- Update to 3.36.0

* Fri Feb 28 2020 Milan Crha <mcrha@redhat.com> - 3.35.92-1
- Update to 3.35.92

* Fri Feb 14 2020 Milan Crha <mcrha@redhat.com> - 3.35.91-1
- Update to 3.35.91

* Fri Jan 31 2020 Milan Crha <mcrha@redhat.com> - 3.35.90-1
- Update to 3.35.90

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.35.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Jan 07 2020 Milan Crha <mcrha@redhat.com> - 3.35.3-2
- Add patch for RH bug #1754321 (alarm-notify: Double-free with certain
  types of the reminder)

* Fri Jan 03 2020 Milan Crha <mcrha@redhat.com> - 3.35.3-1
- Update to 3.35.3

* Fri Nov 22 2019 Milan Crha <mcrha@redhat.com> - 3.35.2-1
- Update to 3.35.2

* Fri Nov 01 2019 Pete Walter <pwalter@fedoraproject.org> - 3.35.1-2
- Rebuild for ICU 65

* Fri Oct 11 2019 Milan Crha <mcrha@redhat.com> - 3.35.1-1
- Update to 3.35.1

* Mon Oct 07 2019 Milan Crha <mcrha@redhat.com> - 3.34.1-1
- Update to 3.34.1

* Mon Sep 09 2019 Milan Crha <mcrha@redhat.com> - 3.34.0-1
- Update to 3.34.0

* Mon Sep 02 2019 Milan Crha <mcrha@redhat.com> - 3.33.92-1
- Update to 3.33.92

* Mon Aug 19 2019 Milan Crha <mcrha@redhat.com> - 3.33.91-1
- Update to 3.33.91

* Tue Aug 06 2019 Milan Crha <mcrha@redhat.com> - 3.33.90-3
- Change how flatpak version is built

* Mon Aug 05 2019 Milan Crha <mcrha@redhat.com> - 3.33.90-2
- Add a patch to add also CFLAGS into gtkdoc-scangobj call

* Mon Aug 05 2019 Milan Crha <mcrha@redhat.com> - 3.33.90-1
- Update to 3.33.90

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.33.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Jul 15 2019 Milan Crha <mcrha@redhat.com> - 3.33.4-1
- Update to 3.33.4

* Thu Jul 11 2019 Felipe Borges <felipeborges@gnome.org> - 3.33.3-3
- Exclude systemd unit files for Flatpak builds

* Mon Jul 08 2019 Kalev Lember <klember@redhat.com> - 3.33.3-2
- Rebuilt for libgweather soname bump

* Mon Jun 17 2019 Milan Crha <mcrha@redhat.com> - 3.33.3-1
- Update to 3.33.3

* Mon May 20 2019 Milan Crha <mcrha@redhat.com> - 3.33.2-1
- Update to 3.33.2

* Mon Apr 22 2019 Milan Crha <mcrha@redhat.com> - 3.33.1-2
- Package new EBackend .typelib and .gir files

* Mon Apr 22 2019 Milan Crha <mcrha@redhat.com> - 3.33.1-1
- Update to 3.33.1

* Mon Apr 08 2019 Milan Crha <mcrha@redhat.com> - 3.32.1-2
- Upload the .tar.xz file

* Mon Apr 08 2019 Milan Crha <mcrha@redhat.com> - 3.32.1-1
- Update to 3.32.1

* Mon Mar 11 2019 Milan Crha <mcrha@redhat.com> - 3.32.0-1
- Update to 3.32.0

* Mon Mar 04 2019 Milan Crha <mcrha@redhat.com> - 3.31.92-1
- Update to 3.31.92

* Mon Feb 18 2019 Milan Crha <mcrha@redhat.com> - 3.31.91-1
- Update to 3.31.91

* Mon Feb 04 2019 Kalev Lember <klember@redhat.com> - 3.31.90-2
- Update BRs for vala packaging changes

* Mon Feb 04 2019 Milan Crha <mcrha@redhat.com> - 3.31.90-1
- Update to 3.31.90

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.31.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jan 28 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 3.31.4-6
- Remove obsolete Group tag

* Wed Jan 23 2019 Pete Walter <pwalter@fedoraproject.org> - 3.31.4-5
- Rebuild for ICU 63

* Tue Jan 22 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 3.31.4-4
- Remove obsolete ldconfig scriptlets

* Mon Jan 07 2019 Milan Crha <mcrha@redhat.com> - 3.31.4-3
- Fix typo in the latest Igor Gnatenko's commit (Remove obsolete
  scriptlets)

* Mon Jan 07 2019 Milan Crha <mcrha@redhat.com> - 3.31.4-2
- Fix typo in the latest Igor Gnatenko's commit

* Mon Jan 07 2019 Milan Crha <mcrha@redhat.com> - 3.31.4-1
- Update to 3.31.4

* Sun Jan 06 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 3.31.3-2
- Remove obsolete scriptlets

* Mon Dec 10 2018 Milan Crha <mcrha@redhat.com> - 3.31.3-1
- Update to 3.31.3

* Mon Nov 12 2018 Milan Crha <mcrha@redhat.com> - 3.31.2-1
- Update to 3.31.2

* Mon Oct 08 2018 Milan Crha <mcrha@redhat.com> - 3.31.1-1
- Update to 3.31.1

* Mon Sep 24 2018 Milan Crha <mcrha@redhat.com> - 3.30.1-1
- Update to 3.30.1; Remove patch for GNOME Evolution issue #86 (fixed
  upstream)

* Mon Sep 03 2018 Milan Crha <mcrha@redhat.com> - 3.30.0-1
- Update to 3.30.0; Add patch for GNOME Evolution issue #86 (Quoting of
  plain text mail into HTML mode mangles deeper levels)

* Mon Aug 27 2018 Milan Crha <mcrha@redhat.com> - 3.29.92-1
- Update to 3.29.92

* Mon Aug 13 2018 Milan Crha <mcrha@redhat.com> - 3.29.91-1
- Update to 3.29.91

* Mon Jul 30 2018 Milan Crha <mcrha@redhat.com> - 3.29.90-2
- libebookbackendwebdav.so had been renamed to libebookbackendcarddav.so

* Mon Jul 30 2018 Milan Crha <mcrha@redhat.com> - 3.29.90-1
- Update to 3.29.90

* Mon Jul 16 2018 Milan Crha <mcrha@redhat.com> - 3.29.4-1
- Update to 3.29.4

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.29.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jul 10 2018 Pete Walter <pwalter@fedoraproject.org> - 3.29.3-2
- Rebuild for ICU 62

* Mon Jun 18 2018 Milan Crha <mcrha@redhat.com> - 3.29.3-1
- Update to 3.29.3

* Mon May 21 2018 Milan Crha <mcrha@redhat.com> - 3.29.2-1
- Update to 3.29.2

* Wed May 02 2018 Milan Crha <mcrha@redhat.com> - 3.29.1-3
- Add an upstream patch to be able to build with icu 61.1

* Mon Apr 30 2018 Pete Walter <pwalter@fedoraproject.org> - 3.29.1-2
- Rebuild for ICU 61.1

* Mon Apr 16 2018 Milan Crha <mcrha@redhat.com> - 3.29.1-1
- Update to 3.29.1

* Tue Apr 10 2018 Adam Williamson <awilliam@redhat.com> - 3.28.1-3
- Backport fix to strip closing > from URLs when linkifying

* Mon Apr 09 2018 Milan Crha <mcrha@redhat.com> - 3.28.1-2
- Return back incorrectly dropped python3 build dependency

* Mon Apr 09 2018 Milan Crha <mcrha@redhat.com> - 3.28.1-1
- Update to 3.28.1; Drop build dependency on python3

* Mon Mar 12 2018 Milan Crha <mcrha@redhat.com> - 3.28.0-1
- Update to 3.28.0

* Mon Mar 05 2018 Milan Crha <mcrha@redhat.com> - 3.27.92-1
- Update to 3.27.92

* Mon Feb 19 2018 Milan Crha <mcrha@redhat.com> - 3.27.91-1
- Update to 3.27.91

* Wed Feb 14 2018 Milan Crha <mcrha@redhat.com> - 3.27.90-6
- Resolves: #1545175 (Do not use arch-dependent BuildRequires)

* Wed Feb 14 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 3.27.90-5
- Remove %%clean section

* Tue Feb 13 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 3.27.90-4
- Remove BuildRoot definition

* Fri Feb 09 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 3.27.90-3
- Escape macros in %%changelog

* Tue Feb 06 2018 Milan Crha <mcrha@redhat.com> - 3.27.90-2
- Add module-oauth2-services.so module

* Tue Feb 06 2018 Milan Crha <mcrha@redhat.com> - 3.27.90-1
- Update to 3.27.90

* Mon Feb 05 2018 Kalev Lember <klember@redhat.com> - 3.27.4-2
- Rebuilt for libgweather soname bump

* Mon Jan 08 2018 Milan Crha <mcrha@redhat.com> - 3.27.4-1
- Update to 3.27.4

* Mon Dec 11 2017 Milan Crha <mcrha@redhat.com> - 3.27.3-1
- Update to 3.27.3

* Thu Nov 30 2017 Pete Walter <pwalter@fedoraproject.org> - 3.27.2-2
- Rebuild for ICU 60.1

* Mon Nov 13 2017 Milan Crha <mcrha@redhat.com> - 3.27.2-1
- Update to 3.27.2

* Mon Nov 06 2017 Milan Crha <mcrha@redhat.com> - 3.27.1-2
- Rebuild for libical 3.0.0

* Mon Oct 16 2017 Milan Crha <mcrha@redhat.com> - 3.27.1-1
- Update to 3.27.1

* Mon Oct 02 2017 Milan Crha <mcrha@redhat.com> - 3.26.1-1
- Update to 3.26.1

* Mon Sep 11 2017 Milan Crha <mcrha@redhat.com> - 3.26.0-1
- Update to 3.26.0

* Mon Sep 04 2017 Milan Crha <mcrha@redhat.com> - 3.25.92-1
- Update to 3.25.92

* Tue Aug 22 2017 Ville Skyttä <ville.skytta@iki.fi> - 3.25.91-2
- Own the %%{_libexecdir}/evolution-data-server dir, install COPYING as
  %%license

* Mon Aug 21 2017 Milan Crha <mcrha@redhat.com> - 3.25.91-1
- Update to 3.25.91

* Mon Aug 07 2017 Milan Crha <mcrha@redhat.com> - 3.25.90-1
- Update to 3.25.90

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.25.4-3
- Rebuilt for
  https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.25.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jul 17 2017 Milan Crha <mcrha@redhat.com> - 3.25.4-1
- Update to 3.25.4

* Mon Jun 19 2017 Milan Crha <mcrha@redhat.com> - 3.25.3-1
- Update to 3.25.3

* Mon May 22 2017 Milan Crha <mcrha@redhat.com> - 3.25.2-1
- Update to 3.25.2

* Thu Apr 27 2017 Milan Crha <mcrha@redhat.com> - 3.25.1-2
- Split translations into separate package

* Mon Apr 24 2017 Milan Crha <mcrha@redhat.com> - 3.25.1-1
- Update to 3.25.1

* Mon Apr 10 2017 Milan Crha <mcrha@redhat.com> - 3.24.1-1
- Update to 3.24.1

* Mon Mar 20 2017 Milan Crha <mcrha@redhat.com> - 3.24.0-1
- Update to 3.24.0

* Mon Mar 13 2017 Milan Crha <mcrha@redhat.com> - 3.23.92-1
- Update to 3.23.92

* Mon Feb 27 2017 Milan Crha <mcrha@redhat.com> - 3.23.91-1
- Update to 3.23.91

* Mon Feb 13 2017 Milan Crha <mcrha@redhat.com> - 3.23.90-1
- Update to 3.23.90

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.23.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Jan 16 2017 Milan Crha <mcrha@redhat.com> - 3.23.4-2
- Add new installed, but unpackaged files, into the .spec file

* Mon Jan 16 2017 Milan Crha <mcrha@redhat.com> - 3.23.4-1
- Update to 3.23.4; Add Recommends: pinentry-gtk (RH bug #1362477)

* Mon Dec 12 2016 Milan Crha <mcrha@redhat.com> - 3.23.3-2
- Add Camel-1.2.typelib

* Mon Dec 12 2016 Milan Crha <mcrha@redhat.com> - 3.23.3-1
- Update to 3.23.3

* Mon Nov 21 2016 Milan Crha <mcrha@redhat.com> - 3.23.2-2
- Add a patch for RH bug #1395987 (Build GSSAPI support for Camel)

* Mon Nov 21 2016 Milan Crha <mcrha@redhat.com> - 3.23.2-1
- Update to 3.23.2

* Mon Oct 24 2016 Milan Crha <mcrha@redhat.com> - 3.23.1-2
- Bump also eds_base_version

* Mon Oct 24 2016 Milan Crha <mcrha@redhat.com> - 3.23.1-1
- Update to 3.23.1

* Mon Oct 10 2016 Milan Crha <mcrha@redhat.com> - 3.22.1-1
- Update to 3.22.1

* Mon Sep 19 2016 Milan Crha <mcrha@redhat.com> - 3.22.0-1
- Update to 3.22.0

* Mon Sep 12 2016 Milan Crha <mcrha@redhat.com> - 3.21.92-1
- Update to 3.21.92

* Mon Aug 29 2016 Milan Crha <mcrha@redhat.com> - 3.21.91-1
- Update to 3.21.91

* Mon Aug 15 2016 Milan Crha <mcrha@redhat.com> - 3.21.90-2
- Rename variable webkitgtk_version to webkit2gtk_version

* Mon Aug 15 2016 Milan Crha <mcrha@redhat.com> - 3.21.90-1
- Update to 3.21.90

* Mon Jul 18 2016 Milan Crha <mcrha@redhat.com> - 3.21.4-3
- Introduce new "perl" subpackage (code moved from the evolution)

* Mon Jul 18 2016 Milan Crha <mcrha@redhat.com> - 3.21.4-2
- Package new libexec binaries, moved from the evolution

* Mon Jul 18 2016 Milan Crha <mcrha@redhat.com> - 3.21.4-1
- Update to 3.21.4

* Mon Jun 20 2016 Milan Crha <mcrha@redhat.com> - 3.21.3-1
- Update to 3.21.3

* Mon May 23 2016 Milan Crha <mcrha@redhat.com> - 3.21.2-1
- Update to 3.21.2

* Mon Apr 25 2016 Milan Crha <mcrha@redhat.com> - 3.21.1-1
- Update to 3.21.1

* Fri Apr 15 2016 David Tardon <dtardon@redhat.com> - 3.20.1-2
- rebuild for ICU 57.1

* Mon Apr 11 2016 Milan Crha <mcrha@redhat.com> - 3.20.1-1
- Update to 3.20.1

* Mon Mar 21 2016 Milan Crha <mcrha@redhat.com> - 3.20.0-1
- Update to 3.20.0

* Mon Mar 14 2016 Milan Crha <mcrha@redhat.com> - 3.19.92-1
- Update to 3.19.92

* Mon Feb 29 2016 Milan Crha <mcrha@redhat.com> - 3.19.91-1
- Update to 3.19.91

* Mon Feb 15 2016 Milan Crha <mcrha@redhat.com> - 3.19.90-2
- Renamed vala's libcamel-1.2.deps/.vapi to camel-1.2.deps/.vapi

* Mon Feb 15 2016 Milan Crha <mcrha@redhat.com> - 3.19.90-1
- Update to 3.19.90

* Wed Feb 03 2016 Dennis Gilmore <dennis@ausil.us> - 3.19.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jan 27 2016 Milan Crha <mcrha@redhat.com> - 3.19.4-4
- Remove unneeded %%defattr

* Mon Jan 18 2016 David Tardon <dtardon@redhat.com> - 3.19.4-3
- rebuild for libical 2.0.0

* Mon Jan 18 2016 Milan Crha <mcrha@redhat.com> - 3.19.4-2
- Add forgotten gir/vala files

* Mon Jan 18 2016 Milan Crha <mcrha@redhat.com> - 3.19.4-1
- Update to 3.19.4

* Mon Dec 14 2015 Milan Crha <mcrha@redhat.com> - 3.19.3-1
- Update to 3.19.3

* Mon Nov 23 2015 Milan Crha <mcrha@redhat.com> - 3.19.2-1
- Update to 3.19.2

* Wed Oct 28 2015 David Tardon <dtardon@redhat.com> - 3.19.1-4
- rebuild for ICU 56.1

* Mon Oct 26 2015 Milan Crha <mcrha@redhat.com> - 3.19.1-3
- Add systemd user unit files into the main package

* Mon Oct 26 2015 Milan Crha <mcrha@redhat.com> - 3.19.1-2
- Add BuildRequires: pkgconfig(sqlite3) >= %%{sqlite_version}

* Mon Oct 26 2015 Milan Crha <mcrha@redhat.com> - 3.19.1-1
- Update to 3.19.1

* Mon Oct 12 2015 Milan Crha <mcrha@redhat.com> - 3.18.1-1
- Update to 3.18.1

* Mon Sep 21 2015 Milan Crha <mcrha@redhat.com> - 3.18.0-1
- Update to 3.18.0; Remove a patch for compatibility with glib 2.45.8
  (fixed upstream)

* Thu Sep 17 2015 Kalev Lember <klember@redhat.com> - 3.17.92-2
- Backport a patch for compatibility with glib 2.45.8

* Mon Sep 14 2015 Milan Crha <mcrha@redhat.com> - 3.17.92-1
- Update to 3.17.92

* Mon Aug 31 2015 Milan Crha <mcrha@redhat.com> - 3.17.91-1
- Update to 3.17.91

* Mon Aug 17 2015 Milan Crha <mcrha@redhat.com> - 3.17.90-1
- Update to 3.17.90

* Mon Jul 20 2015 Milan Crha <mcrha@redhat.com> - 3.17.4-1
- Update to 3.17.4

* Mon Jun 22 2015 Milan Crha <mcrha@redhat.com> - 3.17.3-1
- Update to 3.17.3

* Wed Jun 17 2015 Dennis Gilmore <dennis@ausil.us> - 3.17.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon May 25 2015 Milan Crha <mcrha@redhat.com> - 3.17.2-1
- Update to 3.17.2

* Mon Apr 27 2015 Milan Crha <mcrha@redhat.com> - 3.17.1-1
- Update to 3.17.1

* Mon Apr 13 2015 Milan Crha <mcrha@redhat.com> - 3.16.1-1
- Update to 3.16.1

* Mon Mar 23 2015 Milan Crha <mcrha@redhat.com> - 3.16.0-1
- Update to 3.16.0

* Mon Mar 16 2015 Milan Crha <mcrha@redhat.com> - 3.15.92-2
- Add new org.gnome.evolution-data-server.gschema.xml file

* Mon Mar 16 2015 Milan Crha <mcrha@redhat.com> - 3.15.92-1
- Update to 3.15.92; Remove patch to fix libdb configure.ac check (fixed
  upstream)

* Mon Mar 02 2015 Milan Crha <mcrha@redhat.com> - 3.15.91-2
- Add patch to fix libdb configure.ac check

* Mon Mar 02 2015 Milan Crha <mcrha@redhat.com> - 3.15.91-1
- Update to 3.15.91

* Mon Feb 16 2015 Milan Crha <mcrha@redhat.com> - 3.13.90-1
- Update to 3.13.90

* Mon Jan 26 2015 David Tardon <dtardon@redhat.com> - 3.13.10-2
- rebuild for ICU 54.1

* Mon Jan 26 2015 Milan Crha <mcrha@redhat.com> - 3.13.10-1
- Update to 3.13.10

* Mon Dec 22 2014 Milan Crha <mcrha@redhat.com> - 3.13.9-1
- Update to 3.13.9

* Mon Nov 24 2014 Milan Crha <mcrha@redhat.com> - 3.13.8-1
- Update to 3.13.8

* Sun Nov 16 2014 Kalev Lember <kalevlember@gmail.com> - 3.13.7-2
- Obsolete compat-evolution-data-server310-libcamel from
  rhughes-f20-gnome-3-12 copr.

* Mon Oct 27 2014 Milan Crha <mcrha@redhat.com> - 3.13.7-1
- Update to 3.13.7

* Mon Sep 22 2014 Milan Crha <mcrha@redhat.com> - 3.13.6-2
- New unpackaged libedbus-private.so file

* Mon Sep 22 2014 Milan Crha <mcrha@redhat.com> - 3.13.6-1
- Update to 3.13.6

* Wed Aug 27 2014 Milan Crha <mcrha@redhat.com> - 3.13.5-3
- Add patch for GNOME bug #735311 (Adapt to new Google HTTP restriction)

* Tue Aug 26 2014 David Tardon <dtardon@redhat.com> - 3.13.5-2
- rebuild for ICU 53.1

* Mon Aug 25 2014 Milan Crha <mcrha@redhat.com> - 3.13.5-1
- Update to 3.13.5

* Sat Aug 16 2014 Peter Robinson <pbrobinson@fedoraproject.org> - 3.13.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Wed Jul 30 2014 Milan Crha <mcrha@redhat.com> - 3.13.4-1
- Update to 3.13.4; Introduce tests subpackage with installed tests

* Tue Jul 22 2014 Kalev Lember <kalevlember@gmail.com> - 3.12.4-5
- Rebuilt for gobject-introspection 1.41.4

* Fri Jul 18 2014 Milan Crha <mcrha@redhat.com> - 3.12.4-4
- Update patch for GNOME bug 733081 (IMAPx job stuck with IDLE)

* Wed Jul 16 2014 Milan Crha <mcrha@redhat.com> - 3.12.4-3
- Add patch for GNOME bug 733081 (IMAPx job stuck with IDLE)

* Mon Jul 14 2014 Milan Crha <mcrha@redhat.com> - 3.12.4-2
- Add forgotten libecalbackendgtasks.so

* Mon Jul 14 2014 Milan Crha <mcrha@redhat.com> - 3.12.4-1
- Update to 3.12.4

* Mon Jun 09 2014 Milan Crha <mcrha@redhat.com> - 3.12.3-1
- Update to 3.12.3

* Sat Jun 07 2014 Dennis Gilmore <dennis@ausil.us> - 3.12.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon May 12 2014 Milan Crha <mcrha@redhat.com> - 3.12.2-1
- Update to 3.12.2

* Wed Apr 16 2014 Adam Williamson <awilliam@redhat.com> - 3.12.1-2
- rebuild for new libgdata

* Mon Apr 14 2014 Milan Crha <mcrha@redhat.com> - 3.12.1-1
- Update to 3.12.1

* Mon Mar 24 2014 Milan Crha <mcrha@redhat.com> - 3.12.0-1
- Update to 3.12.0

* Mon Mar 17 2014 Milan Crha <mcrha@redhat.com> - 3.11.92-1
- Update to 3.11.92

* Wed Mar 12 2014 Milan Crha <mcrha@redhat.com> - 3.11.91-2
- Use pkgconfig() notations in [Build]Requires where applicable

* Mon Mar 03 2014 Milan Crha <mcrha@redhat.com> - 3.11.91-1
- Update to 3.11.91

* Mon Feb 17 2014 Milan Crha <mcrha@redhat.com> - 3.11.90-2
- Add module-secret-monitor.so into rpm

* Mon Feb 17 2014 Milan Crha <mcrha@redhat.com> - 3.11.90-1
- Update to 3.11.90

* Fri Feb 14 2014 Adam Williamson <awilliam@redhat.com> - 3.11.5-3
- rebuild for new icu

* Mon Feb 03 2014 Milan Crha <mcrha@redhat.com> - 3.11.5-2
- Avoid compiler warning due to incorrect krb5 include folder

* Mon Feb 03 2014 Milan Crha <mcrha@redhat.com> - 3.11.5-1
- Update to 3.11.5

* Mon Jan 13 2014 Milan Crha <mcrha@redhat.com> - 3.11.4-2
- Update the doc subpackage, and fix a date typo in a changelog section

* Mon Jan 13 2014 Milan Crha <mcrha@redhat.com> - 3.11.4-1
- Update to 3.11.4

* Sun Dec 22 2013 Ville Skyttä <ville.skytta@iki.fi> - 3.11.2-7
- Drop empty AUTHORS from docs.

* Thu Nov 21 2013 Milan Crha <mcrha@redhat.com> - 3.11.2-6
- Rebuild for new libical (RH bug #1023020)

* Tue Nov 19 2013 Milan Crha <mcrha@redhat.com> - 3.11.2-5
- Fix a Source URL

* Mon Nov 18 2013 Milan Crha <mcrha@redhat.com> - 3.11.2-4
- Add evolution-scan-gconf-tree-xml

* Mon Nov 18 2013 Milan Crha <mcrha@redhat.com> - 3.11.2-3
- Remove libedataserver.convert

* Mon Nov 18 2013 Milan Crha <mcrha@redhat.com> - 3.11.2-2
- Correct a copy&paste typo in %%changelog

* Mon Nov 18 2013 Milan Crha <mcrha@redhat.com> - 3.11.2-1
- Update to 3.11.2 Conditionally build devel documentation Disable compiler
  warnings about deprecated symbols

* Tue Oct 22 2013 Matthew Barnes <mbarnes@redhat.com> - 3.11.1-1
- 3.11.1

* Mon Oct 14 2013 Milan Crha <mcrha@redhat.com> - 3.10.1-2
- Add new module-outlook-backend

* Mon Oct 14 2013 Milan Crha <mcrha@redhat.com> - 3.10.1-1
- Update to 3.10.1

* Mon Sep 23 2013 Milan Crha <mcrha@redhat.com> - 3.10.0-1
- Update to 3.10.0

* Mon Sep 16 2013 Milan Crha <mcrha@redhat.com> - 3.9.92-1
- Update to 3.9.92

* Mon Sep 02 2013 Milan Crha <mcrha@redhat.com> - 3.9.91-1
- Update to 3.9.91

* Mon Aug 19 2013 Milan Crha <mcrha@redhat.com> - 3.9.90-1
- Update to 3.9.90

* Mon Aug 12 2013 Milan Crha <mcrha@redhat.com> - 3.9.5-4
- Forgot to bump the package version to 3.9.5-3 in the previous commit

* Mon Aug 12 2013 Milan Crha <mcrha@redhat.com> - 3.9.5-3
- Bump nss version requirement to 3.14

* Tue Aug 06 2013 Adam Williamson <awilliam@redhat.com> - 3.9.5-2
- rebuild for new libgweather

* Mon Jul 29 2013 Milan Crha <mcrha@redhat.com> - 3.9.5-1
- Update to 3.9.5

* Sun Jul 21 2013 Matthew Barnes <mbarnes@redhat.com> - 3.9.4-2
- Require dconf for dconf-service.

* Mon Jul 08 2013 Milan Crha <mcrha@redhat.com> - 3.9.4-1
- Update to 3.9.4

* Thu Jun 20 2013 Kalev Lember <kalevlember@gmail.com> - 3.9.3-2
- Rebuilt for libgweather 3.9.3 soname bump

* Mon Jun 17 2013 Milan Crha <mcrha@redhat.com> - 3.9.3-1
- Update to 3.9.3

* Mon May 27 2013 Milan Crha <mcrha@redhat.com> - 3.9.2-1
- Update to 3.9.2

* Fri May 24 2013 Rex Dieter <rdieter@math.unl.edu> - 3.9.1-6
- rebuild (libical)

* Mon Apr 29 2013 Milan Crha <mcrha@redhat.com> - 3.9.1-5
- Files module-data-book/cal-factory-goa are gone

* Mon Apr 29 2013 Milan Crha <mcrha@redhat.com> - 3.9.1-4
- Do not use static ldap

* Mon Apr 29 2013 Milan Crha <mcrha@redhat.com> - 3.9.1-3
- Use --with-openldap=yes, not --with-openldap=%%{_libdir}

* Mon Apr 29 2013 Milan Crha <mcrha@redhat.com> - 3.9.1-2
- Drop reference to openldap-evolution, which was needed for evolution-
  exchange only

* Mon Apr 29 2013 Milan Crha <mcrha@redhat.com> - 3.9.1-1
- Update to 3.9.1

* Mon Mar 25 2013 Milan Crha <mcrha@redhat.com> - 3.8.0-1
- Update to 3.8.0

* Mon Mar 18 2013 Milan Crha <mcrha@redhat.com> - 3.7.92-1
- Update to 3.7.92

* Mon Mar 04 2013 Milan Crha <mcrha@redhat.com> - 3.7.91-2
- Add %%{_datadir}/gtk-doc/html/libebook-contacts into 'doc' subpackage

* Mon Mar 04 2013 Milan Crha <mcrha@redhat.com> - 3.7.91-1
- Update to 3.7.91

* Thu Feb 21 2013 Milan Crha <mcrha@redhat.com> - 3.7.90-4
- Add patch gor GNOME bug #693101 (IMAPx vanishes folder summary) Add patch
  for Red Hat bug #912503 (incorrect G_BEGIN/END_DECLS)

* Mon Feb 18 2013 Milan Crha <mcrha@redhat.com> - 3.7.90-3
- Add an upstream .pc files fix for a libebook split

* Mon Feb 18 2013 Milan Crha <mcrha@redhat.com> - 3.7.90-2
- Add overlooked .so/.typelib/.gir files

* Mon Feb 18 2013 Milan Crha <mcrha@redhat.com> - 3.7.90-1
- Update to 3.7.90

* Mon Feb 04 2013 Milan Crha <mcrha@redhat.com> - 3.7.5-1
- Update to 3.7.5

* Mon Jan 14 2013 Milan Crha <mcrha@redhat.com> - 3.7.4-3
- Add libedataserver-1.2.deps

* Mon Jan 14 2013 Milan Crha <mcrha@redhat.com> - 3.7.4-2
- Add --add-missing to automake call and remove legacy imap camel provider

* Mon Jan 14 2013 Milan Crha <mcrha@redhat.com> - 3.7.4-1
- Update to 3.7.4

* Tue Jan 08 2013 Milan Crha <mcrha@redhat.com> - 3.7.3-3
- Remove obsolete --enable-nss and fix a typo in largefile_flags variable
  name

* Thu Dec 20 2012 Kalev Lember <kalevlember@gmail.com> - 3.7.3-2
- Rebuilt for libgweather 3.7.3 soname bump

* Tue Dec 18 2012 Matthew Barnes <mbarnes@redhat.com> - 3.7.3-1
- 3.7.3

* Mon Nov 19 2012 Milan Crha <mcrha@redhat.com> - 3.7.2.1-6
- Return back %%{_datadir}/evolution-data-server and add goa factory
  modules

* Mon Nov 19 2012 Milan Crha <mcrha@redhat.com> - 3.7.2.1-5
- Include directory is also without version now

* Mon Nov 19 2012 Milan Crha <mcrha@redhat.com> - 3.7.2.1-4
- Fix bogus dates in %%changelog

* Mon Nov 19 2012 Milan Crha <mcrha@redhat.com> - 3.7.2.1-3
- Drop removed file and folder

* Mon Nov 19 2012 Milan Crha <mcrha@redhat.com> - 3.7.2.1-2
- Bump GLib version requirement to 2.34.0

* Mon Nov 19 2012 Milan Crha <mcrha@redhat.com> - 3.7.2.1-1
- Update to 3.7.2.1

* Wed Oct 24 2012 Milan Crha <mcrha@redhat.com> - 3.7.1-4
- module-online-accounts renamed to module-gnome-online-accounts

* Wed Oct 24 2012 Milan Crha <mcrha@redhat.com> - 3.7.1-3
- Revert add of BuildRequires: nss-util-devel

* Tue Oct 23 2012 Milan Crha <mcrha@redhat.com> - 3.7.1-2
- Add BuildRequires: nss-util-devel

* Mon Oct 22 2012 Milan Crha <mcrha@redhat.com> - 3.7.1-1
- Update to 3.7.1

* Mon Sep 17 2012 Milan Crha <mcrha@redhat.com> - 3.5.92-1
- Update to 3.5.92

* Mon Sep 03 2012 Milan Crha <mcrha@redhat.com> - 3.5.91-1
- Update to 3.5.91

* Mon Aug 20 2012 Milan Crha <mcrha@redhat.com> - 3.5.90-1
- Update to 3.5.90

* Mon Aug 06 2012 Milan Crha <mcrha@redhat.com> - 3.5.5-1
- Update to 3.5.5

* Thu Jul 26 2012 Milan Crha <mcrha@redhat.com> - 3.5.4-5
- Add patch for less memory usage from vTrash camel folders

* Thu Jul 19 2012 Dennis Gilmore <dennis@ausil.us> - 3.5.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul 16 2012 Milan Crha <mcrha@redhat.com> - 3.5.4-3
- Change dependency from db4 to libdb

* Mon Jul 16 2012 Milan Crha <mcrha@redhat.com> - 3.5.4-2
- Increase version dependency on libgweather to 3.5.0

* Mon Jul 16 2012 Milan Crha <mcrha@redhat.com> - 3.5.4-1
- Update to 3.5.4

* Sun Jul 01 2012 Matthew Barnes <mbarnes@redhat.com> - 3.5.3.1-1
- 3.5.3.1

* Wed Jun 27 2012 Matthew Barnes <mbarnes@redhat.com> - 3.5.3-5
- Avoid exposing <db.h> in a public header file.

* Wed Jun 27 2012 Matthias Clasen <mclasen@redhat.com> - 3.5.3-4
- Build against new gweather

* Mon Jun 25 2012 Matthew Barnes <mbarnes@redhat.com> - 3.5.3-3
- Add some missing GSettings schemas.

* Mon Jun 25 2012 Matthew Barnes <mbarnes@redhat.com> - 3.5.3-2
- Update build requirements.

* Mon Jun 25 2012 Matthew Barnes <mbarnes@redhat.com> - 3.5.3-1
- Update to 3.5.3

* Mon Jun 04 2012 Milan Crha <mcrha@redhat.com> - 3.5.2-1
- Update to 3.5.2

* Sun Apr 29 2012 Matthew Barnes <mbarnes@redhat.com> - 3.5.1-1
- Update to 3.5.1

* Tue Apr 24 2012 Kalev Lember <kalevlember@gmail.com> - 3.4.1-2
- Silence rpm scriptlet output

* Tue Apr 24 2012 Richard Hughes <richard@hughsie.com> - 3.4.1-1
- Update to 3.4.1

* Mon Mar 26 2012 Milan Crha <mcrha@redhat.com> - 3.4.0-1
- Update to 3.4.0

* Mon Mar 19 2012 Milan Crha <mcrha@redhat.com> - 3.3.92-1
- Update to 3.3.92

* Tue Mar 06 2012 Milan Crha <mcrha@redhat.com> - 3.3.91-1
- Update to 3.3.91

* Mon Feb 20 2012 Milan Crha <mcrha@redhat.com> - 3.3.90-2
- Change openldap-evolution-devel BuildRequires

* Mon Feb 20 2012 Milan Crha <mcrha@redhat.com> - 3.3.90-1
- Update to 3.3.90

* Mon Feb 06 2012 Milan Crha <mcrha@redhat.com> - 3.3.5-1
- Update to 3.3.5

* Mon Jan 16 2012 Milan Crha <mcrha@redhat.com> - 3.3.4-1
- Update to 3.3.4

* Fri Jan 13 2012 Dennis Gilmore <dennis@ausil.us> - 3.3.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Dec 30 2011 Matthew Barnes <mbarnes@redhat.com> - 3.3.3-4
- Require libgnome-keyring-devel instead of gnome-keyring-devel.

* Fri Dec 30 2011 Matthew Barnes <mbarnes@redhat.com> - 3.3.3-3
- Bump release.

* Fri Dec 30 2011 Matthew Barnes <mbarnes@redhat.com> - 3.3.3-2
- Change gnome-keyring-devel to gnome-keyring.

* Mon Dec 19 2011 Milan Crha <mcrha@redhat.com> - 3.3.3-1
- Update to 3.3.3

* Mon Nov 21 2011 Milan Crha <mcrha@redhat.com> - 3.3.2-1
- Update to 3.3.2

* Mon Oct 24 2011 Milan Crha <mcrha@redhat.com> - 3.3.1-4
- Return incorrectly removed line from a .spec file

* Mon Oct 24 2011 Milan Crha <mcrha@redhat.com> - 3.3.1-3
- Factory binaries have been renamed

* Mon Oct 24 2011 Milan Crha <mcrha@redhat.com> - 3.3.1-2
- Add patch to not call g_thread_init()

* Mon Oct 24 2011 Milan Crha <mcrha@redhat.com> - 3.3.1-1
- Update to 3.3.1

* Mon Sep 26 2011 Milan Crha <mcrha@redhat.com> - 3.2.0-1
- Update to 3.2.0

* Mon Sep 19 2011 Milan Crha <mcrha@redhat.com> - 3.1.92-1
- Update to 3.1.92

* Mon Sep 05 2011 Milan Crha <mcrha@redhat.com> - 3.1.91-1
- Update to 3.1.91

* Mon Aug 29 2011 Milan Crha <mcrha@redhat.com> - 3.1.90-1
- Update to 3.1.90

* Mon Aug 15 2011 Milan Crha <mcrha@redhat.com> - 3.1.5-1
- Update to 3.1.5

* Sat Jul 23 2011 Matthew Barnes <mbarnes@redhat.com> - 3.1.4-1
- 3.1.4

* Mon Jul 04 2011 Matthew Barnes <mbarnes@redhat.com> - 3.1.3-1
- 3.1.3

* Tue Jun 14 2011 Milan Crha <mcrha@redhat.com> - 3.1.2-3
- Add EBook gir files to the package

* Tue Jun 14 2011 Milan Crha <mcrha@redhat.com> - 3.1.2-2
- Add patch by Philip Withnall to build against libgdata-0.9.0

* Tue Jun 14 2011 Milan Crha <mcrha@redhat.com> - 3.1.2-1
- Update to 3.1.2

* Mon May 09 2011 Milan Crha <mcrha@redhat.com> - 3.1.1-2
- New base version is 3.2

* Mon May 09 2011 Milan Crha <mcrha@redhat.com> - 3.1.1-1
- Update to 3.1.1

* Mon Apr 04 2011 Milan Crha <mcrha@redhat.com> - 3.0.0-1
- Update to 3.0.0

* Mon Mar 21 2011 Milan Crha <mcrha@redhat.com> - 2.91.92-1
- Update to 2.91.92

* Mon Mar 07 2011 Milan Crha <mcrha@redhat.com> - 2.91.91-1
- Update to 2.91.91

* Mon Feb 21 2011 Milan Crha <mcrha@redhat.com> - 2.91.90-1
- Update to 2.91.90

* Fri Feb 11 2011 Matthias Clasen <mclasen@redhat.com> - 2.91.6-7
- rebuild

* Tue Feb 08 2011 Dennis Gilmore <dennis@ausil.us> - 2.91.6-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Feb 02 2011 Matthias Clasen <mclasen@redhat.com> - 2.91.6-5
- rebuild

* Mon Jan 31 2011 Milan Crha <mcrha@redhat.com> - 2.91.6-4
- libedataserverui is 3.0 now

* Mon Jan 31 2011 Milan Crha <mcrha@redhat.com> - 2.91.6-3
- One more gtk3 change overlook

* Mon Jan 31 2011 Milan Crha <mcrha@redhat.com> - 2.91.6-2
- Require gtk3-devel

* Mon Jan 31 2011 Milan Crha <mcrha@redhat.com> - 2.91.6-1
- Update to 2.91.6

* Mon Jan 31 2011 Caolán McNamara <caolanm@redhat.com> - 2.91.5-5
- Rebuild against new libgweather

* Tue Jan 18 2011 Matthias Clasen <mclasen@redhat.com> - 2.91.5-4
- Rebuild against newer libgdata

* Thu Jan 13 2011 Matthias Clasen <mclasen@redhat.com> - 2.91.5-3
- Move girs to devel

* Mon Jan 10 2011 Milan Crha <mcrha@redhat.com> - 2.91.5-2
- Revert change in eds include dir

* Mon Jan 10 2011 Milan Crha <mcrha@redhat.com> - 2.91.5-1
- Update to 2.91.5

* Mon Dec 20 2010 Milan Crha <mcrha@redhat.com> - 2.91.4-1
- Update to 2.91.4

* Mon Nov 29 2010 Milan Crha <mcrha@redhat.com> - 2.91.3-1
- Update to 2.91.3

* Mon Nov 08 2010 Milan Crha <mcrha@redhat.com> - 2.91.2-2
- Add Gir files

* Mon Nov 08 2010 Milan Crha <mcrha@redhat.com> - 2.91.2-1
- Update to 2.91.2

* Fri Nov 05 2010 Milan Crha <mcrha@redhat.com> - 2.91.1-4
- Little formatting mistake in the changelog line

* Fri Nov 05 2010 Milan Crha <mcrha@redhat.com> - 2.91.1-3
- Rebuild against newer libxml2

* Mon Oct 25 2010 Milan Crha <mcrha@redhat.com> - 2.91.1-2
- Add test patch to workaround imapx Gnome bug #631804

* Mon Oct 18 2010 Milan Crha <mcrha@redhat.com> - 2.91.1-1
- Update to 2.91.1

* Mon Oct 11 2010 Milan Crha <mcrha@redhat.com> - 2.91.0-3
- Bump package version requirements

* Mon Oct 11 2010 Milan Crha <mcrha@redhat.com> - 2.91.0-2
- Update also Source url

* Mon Oct 11 2010 Milan Crha <mcrha@redhat.com> - 2.91.0-1
- Update to 2.91.0

* Wed Sep 29 2010 Jesse Keating <jkeating@redhat.com> - 2.31.92-2
- Rebuilt for gcc bug 634757

* Mon Sep 13 2010 Milan Crha <mcrha@redhat.com> - 2.31.92-1
- Update to 2.31.92

* Mon Aug 30 2010 Milan Crha <mcrha@redhat.com> - 2.31.91-2
- Add also itermediate changes from f14 branch

* Mon Aug 30 2010 Milan Crha <mcrha@redhat.com> - 2.31.91-1
- * Mon Aug 30 2010 Milan Crha <mcrha@redhat.com> - 2.31.91-1.fc15 - Update
  to 2.31.91

* Wed Jul 28 2010 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.31.5-3
- dist-git conversion

* Thu Jul 15 2010 Milan Crha <mcrha@fedoraproject.org> - 2.31.5-2
- Add also Mozilla NSS crypto for LDAP, as it requires it now. Patch by
  Rich Megginson

* Tue Jul 13 2010 Milan Crha <mcrha@fedoraproject.org> - 2.31.5-1
- Update to 2.31.5

* Mon Jun 07 2010 Milan Crha <mcrha@fedoraproject.org> - 2.31.3-3
- Remove gtk+ version check lowering patch and add patch for a GSEAL_ENABLE
  removal

* Mon Jun 07 2010 Milan Crha <mcrha@fedoraproject.org> - 2.31.3-2
- Patch for gtk+ version check lowered to 2.21.1

* Mon Jun 07 2010 Milan Crha <mcrha@fedoraproject.org> - 2.31.3-1
- Update to 2.31.3

* Tue May 25 2010 Matthew Barnes <mbarnes@fedoraproject.org> - 2.31.2-3
- Enable largefile support in Camel, to help debug GNOME bug #612082.
  Debian turned this on recently and is experiencing problems, and I want
  to get to the bottom of it and finally break this 2 GB barrier.

* Mon May 24 2010 Milan Crha <mcrha@fedoraproject.org> - 2.31.2-2
- libecalbackendgoogle dropped.

* Mon May 24 2010 Milan Crha <mcrha@fedoraproject.org> - 2.31.2-1
- Update to 2.31.2

* Tue May 04 2010 Milan Crha <mcrha@fedoraproject.org> - 2.31.1-3
- devel package requires libgdata-devel

* Mon May 03 2010 Milan Crha <mcrha@fedoraproject.org> - 2.31.1-2
- Doesn't provide libgdata files anymore, uses system's

* Mon May 03 2010 Milan Crha <mcrha@fedoraproject.org> - 2.31.1-1
- Update to 2.31.1 - Update BuildRequires. - Remove imap4 camel provider
  support (dropped upstream).

* Tue Feb 09 2010 Milan Crha <mcrha@fedoraproject.org> - 2.29.90-6
- Return back BuildRequires: libglade2-devel.

* Tue Feb 09 2010 Milan Crha <mcrha@fedoraproject.org> - 2.29.90-5
- Release bump

* Tue Feb 09 2010 Milan Crha <mcrha@fedoraproject.org> - 2.29.90-4
- Add BuildRequires: libglade2-devel back as a test

* Tue Feb 09 2010 Matthew Barnes <mbarnes@fedoraproject.org> - 2.29.90-3
- Rebuild to hopefully fix pkgconfig auto-provides glitch.

* Mon Feb 08 2010 Milan Crha <mcrha@fedoraproject.org> - 2.29.90-2
- Removed unneeded BuildRequires.

* Mon Feb 08 2010 Milan Crha <mcrha@fedoraproject.org> - 2.29.90-1
- Update to 2.29.90

* Mon Jan 25 2010 Milan Crha <mcrha@fedoraproject.org> - 2.29.6-1
- Update to 2.29.6

* Tue Jan 12 2010 Milan Crha <mcrha@fedoraproject.org> - 2.29.5-2
- Correct Source URL

* Tue Jan 12 2010 Milan Crha <mcrha@fedoraproject.org> - 2.29.5-1
- Update to 2.29.5

* Mon Dec 21 2009 Milan Crha <mcrha@fedoraproject.org> - 2.29.4-1
- Update to 2.29.4 - Remove patch for GNOME bug #487988 (fixed upstream).

* Wed Dec 09 2009 Bastien Nocera <hadess@fedoraproject.org> - 2.29.3-4
- Remove libgnome and libgnomeui requirements

* Wed Dec 09 2009 Bastien Nocera <hadess@fedoraproject.org>
- Remove libgnome and libgnomeui requirements

* Wed Dec 02 2009 Matthew Barnes <mbarnes@fedoraproject.org> - 2.29.3-2
- Devel subpackage does not need to require doc subpackage.

* Mon Nov 30 2009 Milan Crha <mcrha@fedoraproject.org> - 2.29.3-1
- Update to 2.29.3

* Wed Nov 25 2009 Bill Nottingham <notting@fedoraproject.org> - 2.29.2-2
- Fix typo that causes a failure to update the common directory. (releng
  #2781)

* Mon Nov 16 2009 Milan Crha <mcrha@fedoraproject.org> - 2.29.2-1
- Update to 2.29.2

* Tue Oct 27 2009 Matthew Barnes <mbarnes@fedoraproject.org> - 2.29.1-1
- Update to 2.29.1 - Bump eds_base_version to 2.30. - Add dbus-glib build
  requirement. - Drop Bonobo + ORBit dependency (yay!). - Remove option to
  use OpenSSL instead of NSS. - Drop eds_api_version definition since it
  will never change. - Remove patch for GNOME bug #373146 (deviates from
  upstream).

* Mon Sep 21 2009 Milan Crha <mcrha@fedoraproject.org> - 2.28.0-1
- Update to 2.28.0

* Mon Sep 07 2009 Milan Crha <mcrha@fedoraproject.org> - 2.27.92-1
- Update to 2.27.92

* Thu Aug 27 2009 Matthew Barnes <mbarnes@fedoraproject.org> - 2.27.91-4
- Rebuild with old OpenSSL, er something...

* Thu Aug 27 2009 Tomáš Mráz <tmraz@fedoraproject.org> - 2.27.91-3
- rebuilt with new openssl

* Mon Aug 24 2009 Milan Crha <mcrha@fedoraproject.org> - 2.27.91-2
- Use aclocal -I m4 as acinclude.m4 is divided there now

* Mon Aug 24 2009 Milan Crha <mcrha@fedoraproject.org> - 2.27.91-1
- Update to 2.27.91

* Fri Aug 21 2009 Tomáš Mráz <tmraz@fedoraproject.org> - 2.27.90-2
- rebuilt with new openssl

* Mon Aug 10 2009 Milan Crha <mcrha@fedoraproject.org> - 2.27.90-1
- Update to 2.27.90

* Mon Jul 27 2009 Milan Crha <mcrha@fedoraproject.org> - 2.27.5-1
- Update to 2.27.5

* Fri Jul 24 2009 Jesse Keating <jkeating@fedoraproject.org> - 2.27.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jul 13 2009 Matthew Barnes <mbarnes@fedoraproject.org> - 2.27.4-1
- Update to 2.27.4 - Remove patch for RH bug #505661 (fixed upstream).

* Fri Jul 03 2009 Matthew Barnes <mbarnes@fedoraproject.org> - 2.27.3-3
- Add patch for RH bug #505661 (crash on startup).

* Wed Jul 01 2009 Milan Crha <mcrha@fedoraproject.org> - 2.27.3-2
- Rebuild against newer gcc

* Mon Jun 15 2009 Matthew Barnes <mbarnes@fedoraproject.org> - 2.27.3-1
- Update to 2.27.3

* Tue May 26 2009 Matthew Barnes <mbarnes@fedoraproject.org> - 2.27.2-1
- Update to 2.27.2 - Remove strict_build_settings since the settings are
  used upstream now.

* Mon May 04 2009 Matthew Barnes <mbarnes@fedoraproject.org> - 2.27.1-1
- Update to 2.27.1 - Bump evo_major to 2.28.

* Wed Apr 15 2009 Matthew Barnes <mbarnes@fedoraproject.org> - 2.26.1.1-1
- Update to 2.26.1.1

* Tue Apr 14 2009 Matthew Barnes <mbarnes@fedoraproject.org> - 2.26.1-1
- Update to 2.26.1

* Mon Mar 16 2009 Matthew Barnes <mbarnes@fedoraproject.org> - 2.26.0-1
- Update to 2.26.0 - Remove patch for RH bug #568332 (fixed upstream). -
  Remove patch for GNOME bug #573240 (reverted upstream).

* Fri Mar 13 2009 Matthew Barnes <mbarnes@fedoraproject.org> - 2.25.92-5
- Revise patch for RH bug #568332 to match upstream commit.

* Thu Mar 12 2009 Matthew Barnes <mbarnes@fedoraproject.org> - 2.25.92-4
- Bother...

* Thu Mar 12 2009 Matthew Barnes <mbarnes@fedoraproject.org> - 2.25.92-3
- Add patch for RH bug #568332 (thread leak in fsync() rate limiting).

* Sat Mar 07 2009 Matthew Barnes <mbarnes@fedoraproject.org> - 2.25.92-2
- Add patch to revert GNOME bug #573240 (IMAP message loading regressions).

* Mon Mar 02 2009 Matthew Barnes <mbarnes@fedoraproject.org> - 2.25.92-1
- Update to 2.25.92

* Wed Feb 25 2009 Matthias Clasen <mclasen@fedoraproject.org> - 2.25.91-3
- Make doc noarch

* Tue Feb 24 2009 Jesse Keating <jkeating@fedoraproject.org> - 2.25.91-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 16 2009 Matthew Barnes <mbarnes@fedoraproject.org> - 2.25.91-1
- Update to 2.25.91

* Fri Feb 06 2009 Matthew Barnes <mbarnes@fedoraproject.org> - 2.25.90-5
- Update BuildRoot, License, Source and URL tags. - Require gnome-common so
  we don't have to patch it out.

* Wed Feb 04 2009 Matthew Barnes <mbarnes@fedoraproject.org> - 2.25.90-4
- ... and fix our own <ical.h> includes too.

* Wed Feb 04 2009 Matthew Barnes <mbarnes@fedoraproject.org> - 2.25.90-3
- Work around libical's broken pkg-config file.

* Tue Feb 03 2009 Matthew Barnes <mbarnes@fedoraproject.org> - 2.25.90-2
- Forgot the libical requirement in devel subpackage.

* Mon Feb 02 2009 Matthew Barnes <mbarnes@fedoraproject.org> - 2.25.90-1
- Update to 2.25.90 - Add libical build requirement.

* Tue Jan 20 2009 Matthew Barnes <mbarnes@fedoraproject.org> - 2.25.5-1
- Update to 2.25.5 - Bump gtk2_version to 2.14.0.

* Fri Jan 16 2009 Tomáš Mráz <tmraz@fedoraproject.org> - 2.25.4-2
- rebuild with new openssl

* Tue Jan 06 2009 Matthew Barnes <mbarnes@fedoraproject.org> - 2.25.4-1
- Update to 2.25.4

* Mon Dec 15 2008 Matthew Barnes <mbarnes@fedoraproject.org> - 2.25.3-1
- Update to 2.25.3 - New BR: libgweather-devel

* Fri Dec 05 2008 Matthew Barnes <mbarnes@fedoraproject.org> - 2.25.2-2
- Rebuild due to recent pkg-config breakage.

* Mon Dec 01 2008 Matthew Barnes <mbarnes@fedoraproject.org> - 2.25.2-1
- Update to 2.25.2

* Thu Nov 27 2008 Matthew Barnes <mbarnes@fedoraproject.org> - 2.25.1-2
- Obsolete the evolution-webcal package (RH bug #468855).

* Mon Nov 03 2008 Matthew Barnes <mbarnes@fedoraproject.org> - 2.25.1-1
- Update to 2.25.1 - Bump eds_base_version to 2.26. - Remove patch for RH
  bug #467804 (fixed upstream).

* Thu Oct 23 2008 Matthew Barnes <mbarnes@fedoraproject.org> - 2.24.1-2
- Add patch for RH bug #467804 (remove console spew).

* Tue Oct 21 2008 Matthew Barnes <mbarnes@fedoraproject.org> - 2.24.1-1
- Update to 2.24.1

* Mon Sep 22 2008 Matthew Barnes <mbarnes@fedoraproject.org> - 2.24.0-1
- Update to 2.24.0

* Mon Sep 08 2008 Matthew Barnes <mbarnes@fedoraproject.org> - 2.23.92-1
- Update to 2.23.92

* Mon Sep 01 2008 Matthew Barnes <mbarnes@fedoraproject.org> - 2.23.91-1
- Update to 2.23.91

* Wed Aug 20 2008 Matthew Barnes <mbarnes@fedoraproject.org> - 2.23.90.1-1
- Update to 2.23.90.1

* Mon Aug 04 2008 Matthew Barnes <mbarnes@fedoraproject.org> - 2.23.6-9
- Koji hates me.

* Mon Aug 04 2008 Matthew Barnes <mbarnes@fedoraproject.org> - 2.23.6-8
- Add sqlite3 to Camel's pkgconfig requirements. - Add sqlite3 requirement
  to devel subpackage.

* Mon Aug 04 2008 Matthew Barnes <mbarnes@fedoraproject.org> - 2.23.6-7
- Add sqlite3 to Camel's pkgconfig requirements.

* Mon Aug 04 2008 Matthew Barnes <mbarnes@fedoraproject.org> - 2.23.6-6
- Require /devel/ package for building!

* Mon Aug 04 2008 Matthew Barnes <mbarnes@fedoraproject.org> - 2.23.6-5
- It's Monday.

* Mon Aug 04 2008 Matthew Barnes <mbarnes@fedoraproject.org> - 2.23.6-4
- Oh bugger.

* Mon Aug 04 2008 Matthew Barnes <mbarnes@fedoraproject.org> - 2.23.6-3
- Add missing BR.

* Mon Aug 04 2008 Matthew Barnes <mbarnes@fedoraproject.org> - 2.23.6-2
- Update to 2.23.6

* Mon Aug 04 2008 Matthew Barnes <mbarnes@fedoraproject.org> - 2.23.6-1
- Update to 2.23.6

* Thu Jul 24 2008 Matthew Barnes <mbarnes@fedoraproject.org> - 2.23.5-1
- Update to 2.23.5 - Remove patch for RH bug #534080 (fixed upstream).

* Fri Jul 18 2008 Tom Callaway <spot@fedoraproject.org> - 2.23.4-3
- fix license tag

* Thu Jul 03 2008 Matthew Barnes <mbarnes@fedoraproject.org> - 2.23.4-2
- Add patch for GNOME bug #534080 (fix attachment saving).

* Mon Jun 16 2008 Matthew Barnes <mbarnes@fedoraproject.org> - 2.23.4-1
- Update to 2.23.4

* Mon Jun 02 2008 Matthew Barnes <mbarnes@fedoraproject.org> - 2.23.3-1
- Update to 2.23.3 - Remove patch for GNOME bug #531439 (fixed upstream).

* Mon May 19 2008 Matthew Barnes <mbarnes@fedoraproject.org> - 2.23.2-3
- Add patch for GNOME bug #531439 (GPG passphrases destroy passwords).

* Tue May 13 2008 Matthew Barnes <mbarnes@fedoraproject.org> - 2.23.2-2
- Fix some third-party package breakage caused by libebackend.

* Mon May 12 2008 Matthew Barnes <mbarnes@fedoraproject.org> - 2.23.2-1
- Update to 2.23.2 - Add files for new libebackend library. - Remove patch
  for RH bug #202309 (fixed upstream).

* Tue Apr 22 2008 Matthew Barnes <mbarnes@fedoraproject.org> - 2.23.1-1
- Update to 2.23.1 - Bump eds_base_version to 2.24. - Bump glib2
  requirement to 2.16.1. - Drop gnome-vfs2 requirement.

* Mon Apr 07 2008 Matthew Barnes <mbarnes@fedoraproject.org> - 2.22.1-1
- Update to 2.22.1 - Remove patch for RH bug #296671 (fixed upstream). -
  Remove patch for GNOME bug #523023 (fixed upstream).

* Mon Mar 24 2008 Matthew Barnes <mbarnes@fedoraproject.org> - 2.22.0-3
- Add patch for GNOME bug #523023 (EFolder leak in evo-ex-storage).

* Wed Mar 12 2008 Matthew Barnes <mbarnes@fedoraproject.org> - 2.22.0-2
- Add patch for RH bug #296671 (GC servers may not support NTLM).

* Mon Mar 10 2008 Matthew Barnes <mbarnes@fedoraproject.org> - 2.22.0-1
- Update to 2.22.0

* Mon Feb 25 2008 Matthew Barnes <mbarnes@fedoraproject.org> - 2.21.92-1
- Update to 2.21.92 - Remove patch for GNOME bug #516074 (fixed upstream).

* Thu Feb 14 2008 Matthew Barnes <mbarnes@fedoraproject.org> - 2.21.91-6
- Worked, remove the patch for real.

* Thu Feb 14 2008 Matthew Barnes <mbarnes@fedoraproject.org> - 2.21.91-5
- Try removing the ancient "ldap-x86_64-hack" patch.

* Wed Feb 13 2008 Matthew Barnes <mbarnes@fedoraproject.org> - 2.21.91-4
- Rebuild against libsoup 2.3.2.

* Tue Feb 12 2008 Matthew Barnes <mbarnes@fedoraproject.org> - 2.21.91-3
- Update to 2.21.91 - Add patch for GNOME bug #516074 (latest glibc breaks
  Camel).

* Tue Feb 12 2008 Matthew Barnes <mbarnes@fedoraproject.org> - 2.21.91-2
- Update to 2.21.91 - Add patch for GNOME bug #516074 (latest glibc breaks
  Camel).

* Mon Feb 11 2008 Matthew Barnes <mbarnes@fedoraproject.org> - 2.21.91-1
- Update to 2.21.91

* Fri Feb 08 2008 Matthew Barnes <mbarnes@fedoraproject.org> - 2.21.90-2
- Try disabling a potentially obsolete patch ("ldaphack").

* Mon Jan 28 2008 Matthew Barnes <mbarnes@fedoraproject.org> - 2.21.90-1
- Update to 2.21.90 - Remove patch for GNOME bug #509644 (fixed upstream).

* Thu Jan 17 2008 Matthew Barnes <mbarnes@fedoraproject.org> - 2.21.5-4
- Rename evolution-1.4.4-ldap-x86_64-hack.patch to avoid namespace
  collision with similarly named patch in evolution (RH bug #395551).

* Wed Jan 16 2008 Matthew Barnes <mbarnes@fedoraproject.org> - 2.21.5-3
- Add patch for GNOME bug #509644 (password dialog breakage). - Remove
  patch for RH bug #384741 (fixed upstream). - Remove patch for GNOME bug
  #363695 (obsolete). - Remove patch for GNOME bug #376991 (obsolete).

* Mon Jan 14 2008 Matthew Barnes <mbarnes@fedoraproject.org> - 2.21.5-2
- I swear I did this already...

* Mon Jan 14 2008 Matthew Barnes <mbarnes@fedoraproject.org> - 2.21.5-1
- Update to 2.21.5

* Mon Dec 17 2007 Matthew Barnes <mbarnes@fedoraproject.org> - 2.21.4-1
- Update to 2.21.4 - Require gtk-doc >= 1.9.

* Wed Dec 05 2007 Matthias Clasen <mclasen@fedoraproject.org> - 2.21.3-2
- Rebuild

* Mon Dec 03 2007 Matthew Barnes <mbarnes@fedoraproject.org> - 2.21.3-1
- Update to 2.21.3

* Thu Nov 15 2007 Matthew Barnes <mbarnes@fedoraproject.org> - 2.21.2-2
- Add patch for RH bug #384741 (authentication crash).

* Mon Nov 12 2007 Matthew Barnes <mbarnes@fedoraproject.org> - 2.21.2-1
- Update to 2.21.2

* Mon Oct 29 2007 Matthew Barnes <mbarnes@fedoraproject.org> - 2.21.1-1
- Update to 2.21.1 - Bump eds_base_version to 2.22. - Remove patch for RH
  bug #212106 (fixed upstream). - Remove patch for GNOME bug #417999 (fixed
  upstream).

* Fri Oct 26 2007 Matthew Barnes <mbarnes@fedoraproject.org> - 1.12.1-5
- Remove the use_gtk_doc macro. - Remove redundant requirements. - Use the
  name tag where appropriate. - Add an evolution-data-server-doc
  subpackage.

* Fri Oct 19 2007 Matthew Barnes <mbarnes@fedoraproject.org> - 1.12.1-4
- Porting a couple patches over from RHEL5: - Add patch for RH bug #212106
  (address book error on fresh install). - Add patch for RH bug #215702
  (bad search filter for LDAP address books).

* Tue Oct 16 2007 Matthew Barnes <mbarnes@fedoraproject.org> - 1.12.1-3
- Disable patch for GNOME bug #376991 for now. It may be contributing to
  password prompting problems as described in RH bug #296671.

* Mon Oct 15 2007 Bill Nottingham <notting@fedoraproject.org> - 1.12.1-2
- makefile update to properly grab makefile.common

* Mon Oct 15 2007 Milan Crha <mcrha@fedoraproject.org> - 1.12.1-1
- Update to 1.12.1

* Mon Sep 17 2007 Matthew Barnes <mbarnes@fedoraproject.org> - 1.12.0-1
- Update to 1.12.0

* Tue Sep 04 2007 Matthew Barnes <mbarnes@fedoraproject.org> - 1.11.92-1
- Update to 1.11.92

* Tue Aug 28 2007 Milan Crha <mcrha@fedoraproject.org> - 1.11.91-1
- Update to 1.11.91 - Removed patch for RH bug #215634 (fixed upstream). -
  Removed patch for GNOME bug #466987 (fixed upstream).

* Wed Aug 22 2007 Adam Jackson <ajax@fedoraproject.org> - 1.11.90-6
- Add Requires: glib2 >= 2.14.0, since it's in the buildroot now, and
  forcibly introduces deps on symbols that don't exist in 2.13. If only we
  had working symbol versioning.

* Tue Aug 21 2007 Matthew Barnes <mbarnes@fedoraproject.org> - 1.11.90-5
- Revise patch for GNOME bug #417999 to fix GNOME bug #447591 (Automatic
  Contacts combo boxes don't work).

* Wed Aug 15 2007 Matthew Barnes <mbarnes@fedoraproject.org> - 1.11.90-4
- Fix a typo.

* Wed Aug 15 2007 Matthew Barnes <mbarnes@fedoraproject.org> - 1.11.90-3
- Re-enable the --with-libdb configure option.

* Wed Aug 15 2007 Matthew Barnes <mbarnes@fedoraproject.org> - 1.11.90-2
- Update to 1.11.90 - Add patch for GNOME bug #466987 (glibc redefines
  "open"). - Remove patch for GNOME bug #415891 (fixed upstream).

* Tue Aug 14 2007 Matthew Barnes <mbarnes@fedoraproject.org> - 1.11.90-1
- Update to 1.11.90 - Remove patch for GNOME bug #415891 (fixed upstream).

* Wed Aug 08 2007 Matthew Barnes <mbarnes@fedoraproject.org> - 1.11.6.1-3
- Update to 1.11.6.1

* Wed Aug 01 2007 Matthew Barnes <mbarnes@fedoraproject.org> - 1.11.6.1-2
- Update to 1.11.6.1 - Add patch to fix some <db.h> inclusion breakage.

* Wed Aug 01 2007 Matthew Barnes <mbarnes@fedoraproject.org> - 1.11.6.1-1
- Update to 1.11.6.1

* Tue Jul 31 2007 Matthew Barnes <mbarnes@fedoraproject.org> - 1.11.6-1
- Update to 1.11.6 - Remove patch for GNOME bug #380534 (fixed upstream).

* Fri Jul 27 2007 Matthew Barnes <mbarnes@fedoraproject.org> - 1.11.5-3
- Add patch for GNOME bug #380534 (clarify version requirements).

* Tue Jul 17 2007 Matthew Barnes <mbarnes@fedoraproject.org> - 1.11.5-2
- Add patch for RH bug #243296 (fix LDAP configuration).

* Mon Jul 09 2007 Matthew Barnes <mbarnes@fedoraproject.org> - 1.11.5-1
- Update to 1.11.5

* Mon Jun 18 2007 Matthew Barnes <mbarnes@fedoraproject.org> - 1.11.4-1
- Update to 1.11.4 - Remove patch for RH bug #202309 (fixed upstream). -
  Remove patch for GNOME bug #312854 (fixed upstream). - Remove patch for
  GNOME bug #447414 (fixed upstream).

* Fri Jun 15 2007 Matthew Barnes <mbarnes@fedoraproject.org> - 1.11.3-3
- Add patch for GNOME bug #224277 (Camel IMAP security flaw).

* Thu Jun 14 2007 Matthew Barnes <mbarnes@fedoraproject.org> - 1.11.3-2
- Add patch for GNOME bug #312584 (renaming Exchange folders).

* Mon Jun 04 2007 Matthew Barnes <mbarnes@fedoraproject.org> - 1.11.3-1
- Update to 1.11.3 - Remove patch for GNOME bug #415922 (fixed upstream).

* Fri Jun 01 2007 Matthew Barnes <mbarnes@fedoraproject.org> - 1.11.2-3
- Revise patch for GNOME bug #376991 to fix RH bug #241974.

* Mon May 21 2007 Matthew Barnes <mbarnes@fedoraproject.org> - 1.11.2-2
- Store account passwords in GNOME Keyring.

* Fri May 18 2007 Matthew Barnes <mbarnes@fedoraproject.org> - 1.11.2-1
- Update to 1.11.2 - Bump eds_base_version to 1.12. - Add patch to fix
  implicit function declarations. - Remove patch for RH bug #203058 (fixed
  upstream). - Remove patch for RH bug #210142 (fixed upstream). - Remove
  patch for RH bug #235290 (fixed upstream). - Remove patch for GNOME bug
  #360240 (fixed upstream). - Remove patch for GNOME bug #360619 (fixed
  upstream). - Remove patch for GNOME bug #373117 (fixed upstream). -
  Revise patch for GNOME bug #415891 (partially fixed upstream).

* Thu May 10 2007 Matthew Barnes <mbarnes@fedoraproject.org> - 1.10.1-6
- Add patch for RH bug #215634 (read NSS certificates more reliably).

* Tue May 08 2007 Matthew Barnes <mbarnes@fedoraproject.org> - 1.10.1-5
- Add patch for GNOME bug #373146 (spam message triggers crash).

* Mon May 07 2007 Matthew Barnes <mbarnes@fedoraproject.org> - 1.10.1-4
- Add patch to fix a dangling pointer in e-source-group.c.

* Mon Apr 30 2007 Matthew Barnes <mbarnes@fedoraproject.org> - 1.10.1-3
- Revise patch for RH bug #235290 to not break string freeze.

* Tue Apr 24 2007 Matthew Barnes <mbarnes@fedoraproject.org> - 1.10.1-2
- Add patch for RH bug #235290 (APOP authentication vulnerability).

* Mon Apr 09 2007 Matthew Barnes <mbarnes@fedoraproject.org> - 1.10.1-1
- Update to 1.10.1 - Remove evolution-data-server-1.10.0-no-more-
  beeps.patch (fixed upstream).

* Wed Apr 04 2007 Matthew Barnes <mbarnes@fedoraproject.org> - 1.10.0-7
- Revise patch for GNOME bug #417999 (another ESourceComboBox goof).

* Mon Apr 02 2007 Matthew Barnes <mbarnes@fedoraproject.org> - 1.10.0-6
- Make the new ESourceComboBox widget work properly (RH bug #234760).

* Tue Mar 27 2007 Matthew Barnes <mbarnes@fedoraproject.org> - 1.10.0-5
- BuildRequire openssl-devel when using evolution-openldap.

* Tue Mar 27 2007 Matthew Barnes <mbarnes@fedoraproject.org> - 1.10.0-4
- Link to static evolution-openldap library (RH bug #210126). - Add
  -Wdeclaration-after-statement to strict build settings.

* Thu Mar 22 2007 Matthew Barnes <mbarnes@fedoraproject.org> - 1.10.0-3
- Stop beeping at me!

* Thu Mar 15 2007 Matthew Barnes <mbarnes@fedoraproject.org> - 1.10.0-2
- Modify patch for GNOME bug #376991 to fix RH bug #231994. - Add patch for
  GNOME bug #419999 (avoid deprecated GTK+ symbols). - Remove evolution-
  data-server-1.0.2-workaround-cal-backend-leak.patch. - Remove evolution-
  data-server-1.2.2-fix_open_calendar_declaration.patch. - Remove
  evolution-data-server-1.3.8-fix-implicit-function-declarations.

* Tue Mar 13 2007 Matthew Barnes <mbarnes@fedoraproject.org> - 1.10.0-1
- Update to 1.10.0 - Remove patch for GNOME bug #301363 (fixed upstream).

* Fri Mar 09 2007 Matthew Barnes <mbarnes@fedoraproject.org> - 1.9.92-4
- Add patch for GNOME bug #415922 (support MS ISA Server 2004). - Patch by
  Kenny Root.

* Fri Mar 09 2007 Matthew Barnes <mbarnes@fedoraproject.org> - 1.9.92-3
- Add patch for GNOME bug #415891 (introduce EFlag API). - Add patch for
  GNOME bug #376991 (refactor password handling).

* Tue Mar 06 2007 Matthew Barnes <mbarnes@fedoraproject.org> - 1.9.92-2
- Add patch for GNOME bug #301363 (update timezones).

* Mon Feb 26 2007 Matthew Barnes <mbarnes@fedoraproject.org> - 1.9.92-1
- Update to 1.9.92 - Remove patch for GNOME bug #356177 (fixed upstream). -
  Add minimum version to intltool requirement (current >= 0.35.5).

* Mon Feb 12 2007 Matthew Barnes <mbarnes@fedoraproject.org> - 1.9.91-1
- Update to 1.9.91 - Add flag to disable deprecated Pango symbols. - Remove
  patch for GNOME bug #359979 (fixed upstream).

* Mon Jan 22 2007 Matthew Barnes <mbarnes@fedoraproject.org> - 1.9.5-5
- Revise evolution-data-server-1.8.0-no-gnome-common.patch so that we no
  longer have to run autoconf before building.

* Wed Jan 10 2007 Matthew Barnes <mbarnes@fedoraproject.org> - 1.9.5-4
- Add patch for GNOME bug #359979 (change EMsgPort semantics).

* Tue Jan 09 2007 Matthew Barnes <mbarnes@fedoraproject.org> - 1.9.5-3
- Forgot to bump release.

* Tue Jan 09 2007 Matthew Barnes <mbarnes@fedoraproject.org> - 1.9.5-2
- Require libsoup-devel in devel subpackage (RH bug #152482).

* Tue Jan 09 2007 Matthew Barnes <mbarnes@fedoraproject.org> - 1.9.5-1
- Update to 1.9.5 - Remove patch for GNOME bug #362638 (fixed upstream). -
  Remove patch for GNOME bug #387638 (fixed upstream).

* Tue Dec 19 2006 Matthew Barnes <mbarnes@fedoraproject.org> - 1.9.4-1
- Update to 1.9.4 - Add patch for GNOME bug #373117 (storing color
  settings). - Add patch for GNOME bug #387638 (implicit function
  declaration).

* Mon Dec 04 2006 Matthew Barnes <mbarnes@fedoraproject.org> - 1.9.3-1
- Update to 1.9.3 - Remove patch for GNOME bug #353924 (fixed upstream).

* Fri Nov 10 2006 Matthew Barnes <mbarnes@fedoraproject.org> - 1.9.2-3
- Add patch for RH bug #210142 (calendar crash in indic locales).

* Wed Nov 08 2006 Matthew Barnes <mbarnes@fedoraproject.org> - 1.9.2-2
- Add patch for RH bug #203058 (name selector dialog glitch).

* Tue Nov 07 2006 Matthew Barnes <mbarnes@fedoraproject.org> - 1.9.2-1
- Update to 1.9.2 - Remove patch for Gnome.org bugs #369168, #369259, and
  #369261 (fixed upstream).

* Thu Nov 02 2006 Matthew Barnes <mbarnes@fedoraproject.org> - 1.9.1-5
- Add patch for Gnome.org bug #369168, #369259, and #369261 (misc camel
  bugs reported by Hans Petter Jansson).

* Wed Nov 01 2006 Matthew Barnes <mbarnes@fedoraproject.org> - 1.9.1-4
- Add patch for Gnome.org bug #353924 (category sorting).

* Fri Oct 27 2006 Matthew Barnes <mbarnes@fedoraproject.org> - 1.9.1-3
- Rebuild

* Fri Oct 27 2006 Matthew Barnes <mbarnes@fedoraproject.org> - 1.9.1-2
- Update to 1.9.1 - Add patch for Gnome.org bug #356177 (deprecate EMutex).
  - Add patch for Gnome.org bug #363695 (deprecate EMemPool, EStrv,
  EPoolv). - Remove Jerusalem.ics timezone file (fixed upstream). - Remove
  patch for RH bug #198935 (fixed upstream).

* Tue Oct 17 2006 Matthew Barnes <mbarnes@fedoraproject.org> - 1.9.1-1
- Update to 1.9.1 - Remove patch for RH bug #198935 (fixed upstream).

* Mon Oct 16 2006 Matthew Barnes <mbarnes@fedoraproject.org> - 1.8.1-1
- Update to 1.8.1 - Use stricter build settings. - Add patch for Gnome.org
  bug #360240 ("unused variable" warnings). - Add patch for Gnome.org bug
  #360619 ("incompatible pointer type" warnings). - Add patch for Gnome.org
  bug #362638 (deprecate EThread). - Remove patch for RH bug #198935 (fixed
  upstream). - Remove patch for RH bug #205187 (fixed upstream). - Remove
  patch for Gnome.org bug #353478 (fixed upstream). - Remove patch for
  Gnome.org bug #356828 (fixed upstream). - Remove patch for Gnome.org bug
  #357666 (fixed upstream).

* Wed Sep 27 2006 Matthew Barnes <mbarnes@fedoraproject.org> - 1.8.0-11
- Add patch for RH bug #203915 (fix dangerous mallocs in camel).

* Mon Sep 25 2006 Matthew Barnes <mbarnes@fedoraproject.org> - 1.8.0-10
- Add patch for Gnome.org bug #357666.

* Thu Sep 21 2006 Matthew Barnes <mbarnes@fedoraproject.org> - 1.8.0-9
- Revise patch for RH bug #198935 (fix a crash reported in bug #207446).

* Wed Sep 20 2006 Matthew Barnes <mbarnes@fedoraproject.org> - 1.8.0-8
- Revise patch for RH bug #198935 (fix a typo).

* Wed Sep 20 2006 Matthias Clasen <mclasen@fedoraproject.org> - 1.8.0-7
- Jerusalem

* Wed Sep 20 2006 Matthew Barnes <mbarnes@fedoraproject.org> - 1.8.0-6
- Add patch for Gnome.org bug #356828 (lingering file on uninstall).

* Mon Sep 18 2006 Matthew Barnes <mbarnes@fedoraproject.org> - 1.8.0-5
- Revise patch for RH bug #205187 (use upstream's version).

* Sat Sep 16 2006 Matthew Barnes <mbarnes@fedoraproject.org> - 1.8.0-4
- Add patch for RH bug #205187 (crash on startup).

* Fri Sep 15 2006 Matthew Barnes <mbarnes@fedoraproject.org> - 1.8.0-3
- Revise patch for RH bug #198935 to eliminate a race condition.

* Tue Sep 12 2006 Matthew Barnes <mbarnes@fedoraproject.org> - 1.8.0-2
- Add patch for RH bug #198935.

* Tue Sep 05 2006 Matthew Barnes <mbarnes@fedoraproject.org> - 1.8.0-1
- Update to 1.8.0 - Remove evolution-data-
  server-1.5.4-make_imap4_optional.patch (fixed upstream) and save
  remaining hunk as evolution-data-server-1.8.0-no-gnome-common.patch. -
  Remove patch for RH bug #202329 (fixed upstream). - Remove patch for
  Gnome.org bug #349847 (fixed upstream).

* Tue Aug 29 2006 Matthew Barnes <mbarnes@fedoraproject.org> - 1.7.92-4
- Revise patch for RH bug #198935. - Add patch for Gnome.org bug #353478.

* Mon Aug 28 2006 Ray Strode <rstrode@fedoraproject.org> - 1.7.92-3
- Add patch from Veerapuram Varadhan to fix fd leak (bug 198935).

* Tue Aug 22 2006 Matthew Barnes <mbarnes@fedoraproject.org> - 1.7.92-2
- Add patch for Gnome.org bug #349847.

* Mon Aug 21 2006 Matthew Barnes <mbarnes@fedoraproject.org> - 1.7.92-1
- Update to 1.7.92

* Wed Aug 16 2006 Ray Strode <rstrode@fedoraproject.org> - 1.7.91-4
- give patch file proper name

* Wed Aug 16 2006 Ray Strode <rstrode@fedoraproject.org> - 1.7.91-3
- Add fix from Matthias Clasen that might help bug 202309.

* Mon Aug 14 2006 Matthew Barnes <mbarnes@fedoraproject.org> - 1.7.91-2
- Add patch for RH bug #202329.

* Mon Aug 07 2006 Matthew Barnes <mbarnes@fedoraproject.org> - 1.7.91-1
- Update to 1.7.91 - Remove patch for Gnome.org bug #348725 (fixed
  upstream).

* Fri Aug 04 2006 Matthew Barnes <mbarnes@fedoraproject.org> - 1.7.90.1-1
- Update to 1.7.90.1 (again)

* Thu Aug 03 2006 Matthew Barnes <mbarnes@fedoraproject.org> - 1.7.4-4
- Try again.

* Thu Aug 03 2006 Matthew Barnes <mbarnes@fedoraproject.org> - 1.7.4-3
- Fix Release tag.

* Thu Aug 03 2006 Matthew Barnes <mbarnes@fedoraproject.org> - 1.7.4-2
- Remove patches for Gnome.org bug #309079 (rejected upstream). - One of
  these patches was causing RH bug #167157. - No longer packaging unused
  patches.

* Mon Jul 31 2006 Matthew Barnes <mbarnes@fedoraproject.org> - 1.7.4-1
- Revert to version 1.7.4 to prevent API/ABI breakage. - Add back patch to
  make --with-libdb configure option work.

* Mon Jul 31 2006 Ray Strode <rstrode@fedoraproject.org> - 1.7.90.1-4
- add executable bits to libs

* Mon Jul 31 2006 Matthias Clasen <mclasen@fedoraproject.org> - 1.7.90.1-3
- re build

* Wed Jul 26 2006 Matthew Barnes <mbarnes@fedoraproject.org> - 1.7.90.1-2
- Rebuild

* Wed Jul 26 2006 Matthew Barnes <mbarnes@fedoraproject.org> - 1.7.90.1-1
- Update to 1.7.90.1 - Add patch for Gnome.org bug #348725. - Remove patch
  to make --with-db configure option work (fixed upstream).

* Wed Jul 19 2006 Matthew Barnes <mbarnes@fedoraproject.org> - 1.7.4-2
- Dynamically link to BDB. - Add patch to make --with-db configure option
  work. - Add Requires for db4 and BuildRequires for db4-devel. - Clean up
  spec file, renumber patches.

* Wed Jul 12 2006 Matthew Barnes <mbarnes@fedoraproject.org> - 1.7.4-1
- Update to 1.7.4 - Remove patch for Gnome.org bug #345965 (fixed
  upstream).

* Wed Jul 12 2006 Jesse Keating <jkeating@fedoraproject.org> - 1.7.3-4
- bumped for rebuild

* Tue Jun 27 2006 Matthew Barnes <mbarnes@fedoraproject.org> - 1.7.3-3
- Show GPG key name when asking for the password (Gnome.org #345965).

* Wed Jun 14 2006 Tomáš Mráz <tmraz@fedoraproject.org> - 1.7.3-2
- rebuilt with new gnutls

* Tue Jun 13 2006 Matthias Clasen <mclasen@fedoraproject.org> - 1.7.3-1
- 1.7.3

* Fri Jun 09 2006 Jeremy Katz <katzj@fedoraproject.org> - 1.7.2-5
- BR flex

* Fri Jun 09 2006 Jeremy Katz <katzj@fedoraproject.org> - 1.7.2-4
- don't do parallel build

* Fri Jun 09 2006 Jeremy Katz <katzj@fedoraproject.org> - 1.7.2-3
- bump

* Sun May 28 2006 Matthew Barnes <mbarnes@fedoraproject.org> - 1.7.2-2
- Add missing BuildRequires for gettext (#193360).

* Wed May 17 2006 Matthew Barnes <mbarnes@fedoraproject.org> - 1.7.2-1
- Update to 1.7.2 - Remove evolution-data-
  server-1.7.1-nss_auto_detect.patch; in upstream now.

* Mon May 15 2006 Matthew Barnes <mbarnes@fedoraproject.org> - 1.7.1-2
- Add temporary patch evolution-data-server-1.7.1-nss_auto_detect.patch to
  help `configure' detect the SSL modules (closes #191567).

* Thu May 11 2006 Matthew Barnes <mbarnes@fedoraproject.org> - 1.7.1-1
- Update to 1.7.1 - Bump eds_base_version from 1.6 to 1.8. - Disable
  evolution-data-server-1.2.0-validatehelo.patch (accepted upstream).

* Tue Apr 11 2006 Matthias Clasen <mclasen@fedoraproject.org> - 1.6.1-2
- fix a multilib conflict

* Tue Apr 11 2006 Matthias Clasen <mclasen@fedoraproject.org> - 1.6.1-1
- 1.6.1

* Mon Mar 13 2006 Ray Strode <rstrode@fedoraproject.org> - 1.6.0-1
- 1.6.0

* Mon Feb 27 2006 Ray Strode <rstrode@fedoraproject.org> - 1.5.92-1
- 1.5.92

* Wed Feb 15 2006 dmalcolm <dmalcolm@fedoraproject.org> - 1.5.91-1
- 1.5.91

* Sat Feb 11 2006 Jesse Keating <jkeating@fedoraproject.org> - 1.5.90-4
- bump for bug in double-long on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@fedoraproject.org> - 1.5.90-3
- bump for new gcc/glibc

* Tue Jan 31 2006 Ray Strode <rstrode@fedoraproject.org> - 1.5.90-2
- add build deps (bug 137553)

* Mon Jan 30 2006 dmalcolm <dmalcolm@fedoraproject.org> - 1.5.90-1
- 1.5.90 - explicitly list various files rather than rely on globbing -
  enabled parallel make

* Thu Jan 26 2006 dmalcolm <dmalcolm@fedoraproject.org> - 1.5.5-1
- 1.5.5 - added CalDAV backend to the list of packaged extensions

* Mon Jan 09 2006 dmalcolm <dmalcolm@fedoraproject.org> - 1.5.4-4
- updated patch 300 to remove usage of GNOME_COMPILE_WARNINGS from
  configure.in (since gnome-common might not be available when we rerun the
  autotools)

* Mon Jan 09 2006 dmalcolm <dmalcolm@fedoraproject.org> - 1.5.4-3
- added patch to make the "imap4"/"IMAP4rev1" backend optional; disable it
  in our packages; re-run automake since we have touched various
  Makefile.am files; rerun intltoolize to avoid incompatibilities between
  tarball copy of intltool-merge.in and intltool.m4 in intltool package
  (@EXPANDED_LIBDIR@ renamed to @INTLTOOL_LIBDIR@) (#167574) - explicitly
  list the camel providers and e-d-s extension files in the spec file

* Thu Jan 05 2006 dmalcolm <dmalcolm@fedoraproject.org> - 1.5.4-2
- added patch from David Woodhouse to validate reverse DNS domain before
  using in SMTP greeting (patch 103, #151121)

* Tue Jan 03 2006 dmalcolm <dmalcolm@fedoraproject.org> - 1.5.4-1
- 1.5.4

* Mon Dec 19 2005 dmalcolm <dmalcolm@fedoraproject.org> - 1.5.3-2
- Update specfile and patch 5 (evolution-data-server-1.3.5-nspr_fix.patch)
  to use nss rather than mozilla-nss throughout

* Mon Dec 19 2005 dmalcolm <dmalcolm@fedoraproject.org> - 1.5.3-1
- 1.5.3

* Fri Dec 09 2005 Jesse Keating <jkeating@fedoraproject.org> - 1.5.2-2
- gcc update bump

* Tue Dec 06 2005 dmalcolm <dmalcolm@fedoraproject.org> - 1.5.2-1
- 1.5.2 - bump eds_base_version from 1.4 to 1.6 - updated patch 102

* Mon Dec 05 2005 dmalcolm <dmalcolm@fedoraproject.org> - 1.4.2.1-1
- 1.4.2.1

* Thu Dec 01 2005 dmalcolm <dmalcolm@fedoraproject.org> - 1.4.2-1
- 1.4.2

* Tue Nov 29 2005 dmalcolm <dmalcolm@fedoraproject.org> - 1.4.1.1-3
- add -DLDAP_DEPRECATED to CFLAGS (#172999)

* Fri Nov 11 2005 dmalcolm <dmalcolm@fedoraproject.org> - 1.4.1.1-2
- Updated license field to reflect change from GPL to LGPL - Remove all
  static libraries, not just those in /usr/lib; avoid listing libdir
  subdirectory so that we can be more explicit about the package payload
  (bug #172882)

* Tue Oct 18 2005 dmalcolm <dmalcolm@fedoraproject.org> - 1.4.1.1-1
- 1.4.1.1

* Mon Oct 17 2005 dmalcolm <dmalcolm@fedoraproject.org> - 1.4.1-2
- Updated patch 102 (fix-implicit-function-declarations) to include fix for
  http calendar backend (thanks to Peter Robinson)

* Tue Oct 04 2005 dmalcolm <dmalcolm@fedoraproject.org> - 1.4.1-1
- 1.4.1

* Thu Sep 15 2005 Jeremy Katz <katzj@fedoraproject.org> - 1.4.0-2
- rebuild now that mozilla builds on ppc64

* Wed Sep 07 2005 dmalcolm <dmalcolm@fedoraproject.org> - 1.4.0-1
- 1.4.0 - Removed evolution-data-server-1.3.8-fix-libical-
  vsnprintf.c.patch; a version of this is now upstream (was patch 103,
  added in 1.3.8-2)

* Thu Sep 01 2005 dmalcolm <dmalcolm@fedoraproject.org> - 1.3.8-6
- Use regular LDAP library for now, rather than evolution-openldap
  (#167238)

* Tue Aug 30 2005 dmalcolm <dmalcolm@fedoraproject.org> - 1.3.8-5
- Add -Werror-implicit-function-declaration back to CFLAGS at the make
  stage, after the configure, to spot 64-bit problems whilst avoiding
  breaking configuration tests; expand patch 102 to avoid this breaking
  libdb's CFLAGS

* Fri Aug 26 2005 dmalcolm <dmalcolm@fedoraproject.org> - 1.3.8-4
- Remove -Werror-implicit-function-declaration from CFLAGS; this broke the
  configuration test for fast mutexes in the internal copy of libdb, and
  hence broke access to local addressbooks (#166742) - Introduce
  static_ldap macro; use it to link to static evolution-openldap library,
  containing NTLM support for LDAP binds (needed by Exchange support)

* Wed Aug 24 2005 dmalcolm <dmalcolm@fedoraproject.org> - 1.3.8-3
- Updated patch 102 to fix further implicit function declarations

* Tue Aug 23 2005 dmalcolm <dmalcolm@fedoraproject.org> - 1.3.8-2
- added patch (103) to fix problem with configuration macros in libical's
  vsnprintf.c

* Tue Aug 23 2005 dmalcolm <dmalcolm@fedoraproject.org> - 1.3.8-1
- 1.3.8 - Add -Werror-implicit-function-declaration to CFLAGS, to avoid
  64-bit issues and add patch to fix these where they occur (patch 102)

* Mon Aug 15 2005 dmalcolm <dmalcolm@fedoraproject.org> - 1.3.7-2
- rebuild

* Tue Aug 09 2005 dmalcolm <dmalcolm@fedoraproject.org> - 1.3.7-1
- 1.3.7

* Mon Aug 08 2005 Tomáš Mráz <tmraz@fedoraproject.org> - 1.3.6.1-2
- rebuild with new gnutls

* Fri Jul 29 2005 dmalcolm <dmalcolm@fedoraproject.org> - 1.3.6.1-1
- 1.3.6.1

* Thu Jul 28 2005 dmalcolm <dmalcolm@fedoraproject.org> - 1.3.6-1
- 1.3.6

* Mon Jul 25 2005 dmalcolm <dmalcolm@fedoraproject.org> - 1.3.5-2
- Added patch to use nspr rather than mozilla-nspr when doing pkg-config
  tests (Patch5: evolution-data-server-1.3.5-nspr_fix.patch)

* Mon Jul 25 2005 dmalcolm <dmalcolm@fedoraproject.org> - 1.3.5-1
- 1.3.5 - Split eds_major (was 1.2) into eds_base_version (1.4) and
  eds_api_version (1.2) to correspond to BASE_VERSION and API_VERSION in
  configure.in; updated rest of specfile accordingly. - Removed upstreamed
  patch: evolution-data-server-1.2.0-cope-with-a-macro-called-read.patch

* Sat Jul 09 2005 Matthias Clasen <mclasen@fedoraproject.org> - 1.2.2-5
- Update comments

* Mon Jun 27 2005 dmalcolm <dmalcolm@fedoraproject.org> - 1.2.2-4
- Added leak fixes for GNOME bug 309079 provided by Mark G. Adams

* Wed May 18 2005 dmalcolm <dmalcolm@fedoraproject.org> - 1.2.2-3
- bumped libsoup requirement to 2.2.3; removed mozilla_build_version, using
  pkg-config instead for locating NSPRS and NSS headers/libraries (#158085)

* Tue Apr 12 2005 dmalcolm <dmalcolm@fedoraproject.org> - 1.2.2-2
- added patch to calendar/libecal/e-cal.c to fix missing declaration of
  open_calendar

* Tue Apr 12 2005 dmalcolm <dmalcolm@fedoraproject.org> - 1.2.2-1
- 1.2.2

* Thu Mar 17 2005 dmalcolm <dmalcolm@fedoraproject.org> - 1.2.1-1
- 1.2.1

* Thu Mar 10 2005 dmalcolm <dmalcolm@fedoraproject.org> - 1.2.0-3
- Removed explicit run-time spec-file requirement on mozilla. The Mozilla
  NSS API/ABI stabilised by version 1.7.3 The libraries are always located
  in the libdir However, the headers are in
  /usr/include/mozilla-%%{mozilla_build_version} and so they move each time
  the mozilla version changes. So we no longer have an explicit mozilla
  run-time requirement in the specfile; a requirement on the appropriate
  NSS and NSPR .so files is automagically generated on build. We have an
  explicit, exact build-time version, so that we can find the headers
  (without invoking an RPM query from the spec file; to do so is considered
  bad practice) - Introduced mozilla_build_version, to replace
  mozilla_version - Set mozilla_build_version to 1.7.6 to reflect current
  state of tree

* Tue Mar 08 2005 dmalcolm <dmalcolm@fedoraproject.org> - 1.2.0-2
- Added a patch to deal with glibc defining a macro called "read"

* Tue Mar 08 2005 dmalcolm <dmalcolm@fedoraproject.org> - 1.2.0-1
- 1.2.0 - Removed patch for GCC 4 as this is now in upstream tarball

* Wed Mar 02 2005 Jeremy Katz <katzj@fedoraproject.org> - 1.1.6-6
- rebuild to fix library linking silliness

* Tue Mar 01 2005 dmalcolm <dmalcolm@fedoraproject.org> - 1.1.6-5
- disabling gtk-doc on ia64 and s390x

* Tue Mar 01 2005 dmalcolm <dmalcolm@fedoraproject.org> - 1.1.6-4
- added macro use_gtk_doc; added missing BuildRequires on gtk-doc; enabled
  gtk-doc generation on all platforms (had been disabled on ia64)

* Tue Mar 01 2005 dmalcolm <dmalcolm@fedoraproject.org> - 1.1.6-3
- extended patch to deal with camel-groupwise-store-summary.c

* Tue Mar 01 2005 dmalcolm <dmalcolm@fedoraproject.org> - 1.1.6-2
- added patch to fix badly-scoped declaration of "namespace_clear" in
  camel-imap-store-summary.c

* Tue Mar 01 2005 dmalcolm <dmalcolm@fedoraproject.org> - 1.1.6-1
- 1.1.6

* Wed Feb 09 2005 dmalcolm <dmalcolm@fedoraproject.org> - 1.1.5-3
- rebuild

* Tue Feb 08 2005 dmalcolm <dmalcolm@fedoraproject.org> - 1.1.5-2
- forgot to upload source tarball

* Tue Feb 08 2005 dmalcolm <dmalcolm@fedoraproject.org> - 1.1.5-1
- 1.1.5

* Mon Jan 31 2005 Matthias Clasen <mclasen@fedoraproject.org> - 1.1.4.2-2
- Add a hint

* Thu Jan 27 2005 dmalcolm <dmalcolm@fedoraproject.org> - 1.1.4.2-1
- Update from unstable 1.1.4.1 to unstable 1.1.1.4.2

* Thu Jan 27 2005 dmalcolm <dmalcolm@fedoraproject.org> - 1.1.4.1-3
- disable gtk-doc generation on ia64 for now

* Thu Jan 27 2005 dmalcolm <dmalcolm@fedoraproject.org> - 1.1.4.1-2
- Exclude ppc64 due to missing mozilla dependency

* Thu Jan 27 2005 dmalcolm <dmalcolm@fedoraproject.org> - 1.1.4.1-1
- Update from 1.0.3 to 1.1.4.1 - Updated eds_major from 1.0 to 1.2; fixed
  translation search path. - Removed 64-bit patch for calendar backend hash
  table; upstream now stores pointers to ECalBackendFactory, rather than
  GType - Removed calendar optimisation patch for part of part of bug
  #141283 as this is now in the upstream tarball - Added
  /usr/lib/evolution-data-server-%%{eds_major} to cover the extensions,
  plus the camel code now in e-d-s, rather than evolution - Added
  /usr/share/pixmaps/evolution-data-server-%%{eds_major} to cover the
  category pixmaps - Camel code from evolution is now in evolution-data-
  server: - Added camel-index-control and camel-lock-helper to packaged
  files - Added mozilla dependency code from the evolution package - Ditto
  for LDAP - Ditto for krb5 - Ditto for NNTP support handling - Ditto for
  --enable-file-locking and --enable-dot-locking - Added requirements on
  libbonobo, libgnomeui, gnome-vfs2, GConf2, libglade2 - Updated libsoup
  requirement from 2.2.1 to 2.2.2 - Enabled gtk-doc

* Thu Dec 16 2004 dmalcolm <dmalcolm@fedoraproject.org> - 1.0.3-2
- fixed packaging of translation files to reflect upstream change to
  GETTEXT_PACKAGE being evolution-data-server-1.0 rather than -1.5

* Thu Dec 16 2004 dmalcolm <dmalcolm@fedoraproject.org> - 1.0.3-1
- update from upstream 1.0.2 to 1.0.3: Address Book - prevent
  e_book_commit_contact from crashing on multiple calls (Diego Gonzalez) -
  prevent file backend from crashing if uid of vcard is NULL (Diego
  Gonzalez) Calendar #XB59904 - Speed up calendar queries (Rodrigo)
  #XB69624 - make changes in evo corresponding to soap schema changes
  (Siva) - fix libical build for automake 1.9 (Rodney) - fix putenv usage
  for portability (Julio M. Merino Vidal) - sv (Christian Rose) - Removed
  patches to fix build on x86_64 and calendar optimisation for XB59004 as
  these are in the upstream tarball

* Wed Dec 08 2004 dmalcolm <dmalcolm@fedoraproject.org> - 1.0.2-5
- Amortize writes to a local cache of a webcal calendar, fixing further
  aspect of #141283 (upstream bugzilla #70267), as posted to mailing list
  here: http://lists.ximian.com/archives/public/evolution-
  patches/2004-December /008338.html (The groupwise part of that patch did
  not cleanly apply, so I removed it).

* Fri Dec 03 2004 dmalcolm <dmalcolm@fedoraproject.org> - 1.0.2-4
- Added fix for #141283 (upstream bugzilla XB 59904), a backported calendar
  optimisation patch posted to upstream development mailing list here:
  http://lists.ximian.com/archives/public/evolution-patches/2004-November
  /008139.html Wed Nov 3 2004 David Malcolm <dmalcolm@redhat.com> - 1.0.2-4
  - Added patch to fix usage of GINT_TO_POINTER/GPOINTER_TO_INT for
  calendar backend GType hash table, breaking on ia64 (#136914)

* Wed Oct 20 2004 dmalcolm <dmalcolm@fedoraproject.org> - 1.0.2-3
- added workaround for a backend leak that causes the "contacts" calendar
  backend to hold open an EBook for the local contacts (filed upstream at:
  http://bugzilla.ximian.com/show_bug.cgi?id=68533 ); this was causing
  e-d-s to never lose its last addressbook, and hence never quit. We
  workaround this by detecting this condition and exiting when it occurs,
  fixing bug #134851 and #134849.

* Tue Oct 12 2004 dmalcolm <dmalcolm@fedoraproject.org> - 1.0.2-2
- Added patch to fix build on x86_64 (had multiple definitions of mutex
  code in libdb/dbinc.mutex.h)

* Tue Oct 12 2004 dmalcolm <dmalcolm@fedoraproject.org> - 1.0.2-1
- 1.0.21.0.2 1.0.2

* Tue Sep 28 2004 dmalcolm <dmalcolm@fedoraproject.org> - 1.0.1-1
- update from 1.0.0 to 1.0.1 - removed patch that fixed warnings in
  calendar code (now in upstream tarball)

* Mon Sep 20 2004 dmalcolm <dmalcolm@fedoraproject.org> - 1.0.0-3
- Added upstream bugzilla reference

* Mon Sep 20 2004 dmalcolm <dmalcolm@fedoraproject.org> - 1.0.0-2
- Fixed various warnings in the calendar code

* Tue Sep 14 2004 dmalcolm <dmalcolm@fedoraproject.org> - 1.0.0-1
- Update from 0.0.99 to 1.0.0; fixed source FTP location

* Thu Sep 09 2004 cvsdist <cvsdist@fedoraproject.org> - 0.0.99-1
- auto-import changelog data from evolution-data-server-0.0.99-1.src.rpm
  Tue Aug 31 2004 David Malcolm <dmalcolm@redhat.com> - 0.0.99-1 - update
  from 0.0.98 to 0.0.99 - increased libsoup requirement to 2.2.0 to match
  configuration script

* Thu Sep 09 2004 cvsdist <cvsdist@fedoraproject.org> - 0.0.98-1
- auto-import changelog data from evolution-data-server-0.0.98-1.src.rpm
  Mon Aug 16 2004 David Malcolm <dmalcolm@redhat.com> - 0.0.98-1 - updated
  tarball from 0.0.97 to 0.0.98; updated required libsoup version to 2.1.13

* Thu Sep 09 2004 cvsdist <cvsdist@fedoraproject.org> - 0.0.97-2
- auto-import changelog data from evolution-data-server-0.0.97-2.src.rpm
  Thu Aug 05 2004 Warren Togami <wtogami@redhat.com> - 0.0.97-2 - pkgconfig
  -devel Requires libbonobo-devel, libgnome-devel

* Thu Sep 09 2004 cvsdist <cvsdist@fedoraproject.org> - 0.0.97-1
- auto-import changelog data from evolution-data-server-0.0.97-1.src.rpm
  Wed Aug 04 2004 David Malcolm <dmalcolm@redhat.com> - 0.0.97-1 - upgraded
  to 0.0.97; rewrote the package's description

* Thu Sep 09 2004 cvsdist <cvsdist@fedoraproject.org> - 0.0.96-1
- auto-import changelog data from evolution-data-server-0.0.96-3.src.rpm
  Mon Jul 26 2004 David Malcolm <dmalcolm@redhat.com> - rebuilt Tue Jul 20
  2004 David Malcolm <dmalcolm@redhat.com> - 0.0.96-2 - added version
  numbers to the BuildRequires test for libsoup-devel and ORBit2-devel Tue
  Jul 20 2004 David Malcolm <dmalcolm@redhat.com> - 0.0.96-1 - 0.0.96;
  libsoup required is now 2.1.12

* Thu Sep 09 2004 cvsdist <cvsdist@fedoraproject.org> - 0.0.95-2
- auto-import changelog data from evolution-data-server-0.0.95-3.src.rpm
  Thu Jul 08 2004 David Malcolm <dmalcolm@redhat.com> - rebuilt

* Thu Sep 09 2004 cvsdist <cvsdist@fedoraproject.org> - 0.0.95-1
- auto-import changelog data from evolution-data-server-0.0.95-2.src.rpm
  Wed Jul 07 2004 David Malcolm <dmalcolm@redhat.com> - rebuilt Tue Jul 06
  2004 David Malcolm <dmalcolm@redhat.com> - 0.0.95-1 - 0.0.95

* Thu Sep 09 2004 cvsdist <cvsdist@fedoraproject.org> - 0.0.94.1-1
- auto-import changelog data from evolution-data-server-0.0.94.1-1.src.rpm
  Thu Jun 17 2004 David Malcolm <dmalcolm@redhat.com> - 0.0.94.1-1 -
  0.0.94.1

* Thu Sep 09 2004 cvsdist <cvsdist@fedoraproject.org> - 0.0.94-2
- auto-import evolution-data-server-0.0.94-2 from evolution-data-
  server-0.0.94-2.src.rpm

* Thu Sep 09 2004 cvsdist <cvsdist@fedoraproject.org> - 0.0.94-1
- auto-import changelog data from evolution-data-server-0.0.94-1.src.rpm
  Mon Jun 07 2004 David Malcolm <dmalcolm@redhat.com> - 0.0.94-1 - 0.0.94
  Wed May 26 2004 David Malcolm <dmalcolm@redhat.com> - 0.0.93-4 - added
  ORBit2 requirement

* Thu Sep 09 2004 cvsdist <cvsdist@fedoraproject.org> - 0.0.93-2
- auto-import evolution-data-server-0.0.93-3 from evolution-data-
  server-0.0.93-3.src.rpm

* Thu Sep 09 2004 cvsdist <cvsdist@fedoraproject.org> - 0.0.93-1
- auto-import changelog data from evolution-data-server-0.0.93-2.src.rpm
  Fri May 21 2004 David Malcolm <dmalcolm@redhat.com> - 0.0.93-2 - rebuilt
  Thu May 20 2004 David Malcolm <dmalcolm@redhat.com> - 0.0.93-1 - 0.0.93;
  libsoup required is now 2.1.10

* Thu Sep 09 2004 cvsdist <cvsdist@fedoraproject.org> - 0.0.92-1
- auto-import changelog data from evolution-data-server-0.0.92-1.src.rpm
  Wed Apr 21 2004 David Malcolm <dmalcolm@redhat.com> - 0.0.92-1 - Update
  to 0.0.92; added a define and a requirement on the libsoup version Wed
  Mar 10 2004 Jeremy Katz <katzj@redhat.com> - 0.0.90-1 - 0.0.90 Fri Feb 13
  2004 Elliot Lee <sopwith@redhat.com> - rebuilt

* Thu Sep 09 2004 cvsdist <cvsdist@fedoraproject.org> - 0.0.6-1
- auto-import changelog data from evolution-data-server-0.0.6-1.src.rpm Mon
  Jan 26 2004 Jeremy Katz <katzj@redhat.com> - 0.0.6-1 - 0.0.6

* Thu Sep 09 2004 cvsdist <cvsdist@fedoraproject.org> - 0.0.5-1
- auto-import changelog data from evolution-data-server-0.0.5-2.src.rpm Wed
  Jan 21 2004 Jeremy Katz <katzj@redhat.com> - 0.0.5-2 - better fix by
  using system libtool Mon Jan 19 2004 Jeremy Katz <katzj@redhat.com>
  0.0.5-1 - add some libdb linkage to make the build on x86_64 happy Wed
  Jan 14 2004 Jeremy Katz <katzj@redhat.com> 0.0.5-0 - update to 0.0.5 Sat
  Jan 03 2004 Jeremy Katz <katzj@redhat.com> 0.0.4-0 - Initial build.
## END: Generated by rpmautospec
