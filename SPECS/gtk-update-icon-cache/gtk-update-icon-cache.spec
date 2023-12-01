%global glib2_version 2.57.2
%global gdk_pixbuf_version 2.30.0
Summary:        Icon theme caching utility
Name:           gtk-update-icon-cache
Version:        3.24.26
Release:        1%{?dist}
License:        LGPLv2+
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://www.gtk.org
Source0:        https://gitlab.gnome.org/Community/gentoo/%{name}/-/archive/%{version}/%{name}-%{version}.tar.gz
BuildRequires:  libxslt
BuildRequires:  meson
BuildRequires:  pkg-config
BuildRequires:  pkgconfig(gdk-pixbuf-2.0) >= %{gdk_pixbuf_version}
BuildRequires:  pkgconfig(glib-2.0) >= %{glib2_version}
Requires:       gdk-pixbuf2-modules%{?_isa}
Requires:       glib2%{?_isa} >= %{glib2_version}

%description
GTK+ can use the cache files created by gtk-update-icon-cache to avoid a lot of
system call and disk seek overhead when the application starts. Since the
format of the cache files allows them to be mmap()ed shared between multiple
applications, the overall memory consumption is reduced as well.

%prep
%autosetup

%build
# building man pages reaches out to the internet
%meson -Dman-pages=false
%meson_build

%install
%meson_install

%find_lang %{name}

%files -f %{name}.lang
%license COPYING
%{_bindir}/gtk-update-icon-cache

%changelog
* Fri May 21 2021 Olivia Crain <oliviacrain@microsoft.com> - 3.24.26-1
- Original version for CBL-Mariner
- License verified
