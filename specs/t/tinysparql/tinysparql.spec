## START: Set by rpmautospec
## (rpmautospec version 0.8.4)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 6;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global systemd_units tinysparql-xdg-portal-3.service

%global tarball_version %%(echo %{version} | tr '~' '.')

%global tracker_obsoletes_version 3.8

%if 0%{?rhel}
%bcond libstemmer 0
%else
%bcond libstemmer 1
%endif

Name:           tinysparql
Version:        3.10.1
Release:        %autorelease
Summary:        Desktop-neutral metadata database and search tool

License:        GPL-2.0-or-later
URL:            https://gnome.pages.gitlab.gnome.org/tinysparql/
Source0:        https://download.gnome.org/sources/tinysparql/3.10/tinysparql-%{tarball_version}.tar.xz

BuildRequires:  asciidoc
BuildRequires:  gcc
BuildRequires:  gettext
BuildRequires:  gi-docgen
%if %{with libstemmer}
BuildRequires:  libstemmer-devel
%endif
BuildRequires:  meson
BuildRequires:  python3-gobject
BuildRequires:  systemd-rpm-macros
BuildRequires:  vala
BuildRequires:  pkgconfig(avahi-glib)
BuildRequires:  pkgconfig(dbus-1)
BuildRequires:  pkgconfig(gobject-introspection-1.0)
BuildRequires:  pkgconfig(icu-i18n)
BuildRequires:  pkgconfig(icu-uc)
BuildRequires:  pkgconfig(json-glib-1.0)
BuildRequires:  pkgconfig(libsoup-3.0)
BuildRequires:  pkgconfig(libxml-2.0)
BuildRequires:  pkgconfig(sqlite3)
BuildRequires:  /usr/bin/dbus-run-session

# renamed in F42
Obsoletes:      tracker < %{tracker_obsoletes_version}
Provides:       tracker = %{version}-%{release}
Provides:       tracker%{?_isa} = %{version}-%{release}

Requires: libtinysparql%{?_isa} = %{version}-%{release}

Recommends: localsearch%{?_isa}

%description
Tinysparql is a powerful desktop-neutral first class object database,
tag/metadata database and search tool.

It consists of a common object database that allows entities to have an
almost infinite number of properties, metadata (both embedded/harvested as
well as user definable), a comprehensive database of keywords/tags and
links to other entities.

It provides additional features for file based objects including context
linking and audit trails for a file object.

Metadata indexers are provided by the localsearch package.


%package -n     libtinysparql
Summary:        Libtinysparql library
License:        LGPL-2.1-or-later
Recommends:     %{name}%{?_isa} = %{version}-%{release}

# renamed in F42
Obsoletes:      libtracker-sparql < %{tracker_obsoletes_version}
Provides:       libtracker-sparql = %{version}-%{release}
Provides:       libtracker-sparql%{?_isa} = %{version}-%{release}

%description -n libtinysparql
This package contains the libtinysparql library.


%package        devel
Summary:        Development files for %{name}
License:        LGPL-2.1-or-later
Requires:       libtinysparql%{?_isa} = %{version}-%{release}

Obsoletes:      tracker-devel < %{tracker_obsoletes_version}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%package        doc
Summary:        Documentation for %{name}
BuildArch:      noarch
# docs/reference/COPYING
License:        LicenceRef-Fedora-Public-Domain AND LGPL-2.1-or-later AND GPL-2.0-or-later

%description doc
This package contains the documentation for %{name}.


%prep
%autosetup -p1 -n %{name}-%{tarball_version}


%build
%meson \
  -Dunicode_support=icu \
  -Dsystemd_user_services_dir=%{_userunitdir} \
%if %{without libstemmer}
  -Dstemmer=disabled \
%endif
  %{nil}

%meson_build


%install
%meson_install

%find_lang tinysparql3


%post
%systemd_user_post tinysparql-xdg-portal-3.service

%preun
%systemd_user_preun tinysparql-xdg-portal-3.service

%postun
%systemd_user_postun_with_restart tinysparql-xdg-portal-3.service


%files -f tinysparql3.lang
%license COPYING COPYING.GPL
%doc AUTHORS NEWS README.md
%{_bindir}/tinysparql
%{_libexecdir}/tinysparql-sql
%{_libexecdir}/tinysparql-xdg-portal-3
%{_datadir}/dbus-1/services/org.freedesktop.portal.Tracker.service
%{_mandir}/man1/tinysparql*.1*
%{_userunitdir}/tinysparql-xdg-portal-3.service
%{bash_completions_dir}/tinysparql

%files -n libtinysparql
%license COPYING COPYING.LGPL
%{_libdir}/girepository-1.0/Tracker-3.0.typelib
%{_libdir}/girepository-1.0/Tsparql-3.0.typelib
%{_libdir}/libtinysparql-3.0.so.0*
%{_libdir}/libtracker-sparql-3.0.so.0*
%{_libdir}/tinysparql-3.0/

%files devel
%license COPYING COPYING.LGPL
%{_includedir}/tinysparql-3.0/
%{_libdir}/libtinysparql-3.0.so
%{_libdir}/libtracker-sparql-3.0.so
%{_libdir}/pkgconfig/tinysparql-3.0.pc
%{_libdir}/pkgconfig/tracker-sparql-3.0.pc
%{_datadir}/vala/vapi/tinysparql-3.0.deps
%{_datadir}/vala/vapi/tinysparql-3.0.vapi
%{_datadir}/gir-1.0/Tracker-3.0.gir
%{_datadir}/gir-1.0/Tsparql-3.0.gir
%{_datadir}/vala/vapi/tracker-sparql-3.0.deps
%{_datadir}/vala/vapi/tracker-sparql-3.0.vapi

%files doc
%license docs/reference/COPYING
%{_docdir}/Tsparql-3.0/


%changelog
## START: Generated by rpmautospec
* Wed Apr 22 2026 azldev <azurelinux@microsoft.com> - 3.10.1-6
- Latest state for tinysparql

* Mon Dec 08 2025 Fxzx micah <fxzxmicah@outlook.com> - 3.10.1-5
- Move the .gir files to the devel package

* Tue Oct 14 2025 Petr Schindler <pschindl@redhat.com> - 3.10.1-1
- Update to 3.10.1

* Mon Sep 15 2025 Michael Catanzaro <mcatanzaro@redhat.com> - 3.10.0-1
- Update to 3.10.0

* Wed Sep 10 2025 Michael Catanzaro <mcatanzaro@redhat.com> - 3.10~rc.1-1
- Update to 3.10.rc.1

* Fri Sep 05 2025 Michael Catanzaro <mcatanzaro@redhat.com> - 3.10~rc-1
- Update to 3.10.rc

* Wed Aug 06 2025 František Zatloukal <fzatlouk@redhat.com> - 3.10~beta-2
- Rebuilt for icu 77.1

* Tue Aug 05 2025 nmontero <nmontero@redhat.com> - 3.10~beta-1
- Update to 3.10.beta

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.10~alpha-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Wed Jul 09 2025 Milan Crha <mcrha@redhat.com> - 3.10~alpha-1
- Update to 3.10.alpha

* Mon Apr 21 2025 nmontero <nmontero@redhat.com> - 3.9.2-1
- Update to 3.9.2

* Fri Mar 21 2025 nmontero <nmontero@redhat.com> - 3.9.1-2
- Add Obsoletes line to devel package

* Mon Mar 17 2025 nmontero <nmontero@redhat.com> - 3.9.1-1
- Update to 3.9.1

* Mon Mar 03 2025 nmontero <nmontero@redhat.com> - 3.9~rc-1
- Update to 3.9.rc

* Thu Feb 06 2025 nmontero <nmontero@redhat.com> - 3.8~rc-9
- Move Provides lines

* Wed Feb 05 2025 nmontero <nmontero@redhat.com> - 3.8~rc-8
- Move Obsoletes line

* Wed Feb 05 2025 Adam Williamson <awilliam@redhat.com> - 3.8~rc-7
- Move the libtracker-sparql devel library to the devel package

* Tue Feb 04 2025 nmontero <nmontero@redhat.com> - 3.8~rc-6
- Version bump

* Fri Jan 31 2025 Adam Williamson <awilliam@redhat.com> - 3.8~rc-5
- Bump the version of the tracker obsoletes

* Fri Jan 31 2025 nmontero <nmontero@redhat.com> - 3.8~rc-4
- Version bump

* Thu Jan 23 2025 nmontero <nmontero@redhat.com> - 3.8~rc-3
- Minor change in %files

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.8~rc-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Oct 10 2024 nmontero <nmontero@redhat.com> - 3.8~rc-1
- Rename tracker to tinysparql Rename libtracker-sparql to libtinysparql
  Update to 3.8~rc Delete README


## END: Generated by rpmautospec
