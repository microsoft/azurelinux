#
# spec file for package libadwaita
#
# Copyright (c) 2024 SUSE LLC
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via https://bugs.opensuse.org/
#


Name:           libadwaita
Version:        1.4.3
Release:        0
Summary:        Building blocks for modern GNOME applications
License:        LGPL-2.1-or-later
URL:            https://gitlab.gnome.org/GNOME/%{name}
Source:         https://gitlab.gnome.org/GNOME/%{name}/-/archive/%{version}/%{name}-%{version}.tar.gz

BuildRequires:  fdupes
BuildRequires:  meson >= 0.59.0
BuildRequires:  pkgconfig
BuildRequires:  libsass
BuildRequires:  vala
BuildRequires:  fribidi-devel
BuildRequires:  pkgconfig(glib-2.0) >= 2.72
BuildRequires:  gobject-introspection-devel

%description
Building blocks for modern GNOME applications.

%package -n libadwaita-1-0
Summary:        Building blocks for modern GNOME applications
Provides:       %{name} = %{version}

%description -n libadwaita-1-0
Building blocks for modern GNOME applications.
This package provides the shared library for libadwaita.

%package docs
Summary:        Developer documentation for libadwaita
BuildArch:      noarch

%description docs
Building blocks for modern GNOME applications.
This package provides the documentation for libadwaita.

%package devel
Summary:        Development files for the Adwaita library
Requires:       libadwaita-1-0 = %{version}
Requires:       typelib-1_0-Adw-1 = %{version}

%description devel
Building blocks for modern GNOME applications.
This package provides the development files for libadwaita.

%package -n typelib-1_0-Adw-1
Summary:        Introspection bindings for Adwaita
Group:          System/Libraries

%description -n typelib-1_0-Adw-1
Building blocks for modern GNOME applications.
This package provides the GObject Introspection bindings for libadwaita.

%prep
%autosetup -p1

%build
%meson \
	-Dexamples=false \
	-Dintrospection=enabled \
	-Dgtk_doc=disabled \
	-Dman=true \
	%{nil}
%meson_build

%install
%meson_install
%fdupes %{buildroot}%{_datadir}

%{ldconfig_scriptlets -n libadwaita-1-0}

%files -n libadwaita-1-0
%license COPYING
%doc README.md
%{_libdir}/libadwaita-1.so.0

%files -n typelib-1_0-Adw-1
%{_libdir}/girepository-1.0/Adw-1.typelib

%files docs
%{_datadir}/doc/%{name}-1/

%files devel
%{_includedir}/libadwaita-1/
%{_libdir}/libadwaita-1.so
%{_libdir}/pkgconfig/libadwaita-1.pc
%{_datadir}/gir-1.0/Adw-1.gir
%dir %{_datadir}/vala/vapi
%{_datadir}/vala/vapi/libadwaita-1.{deps,vapi}

%changelog
* Wed Feb 21 2024 Sharath Srikanth Chellappa <sharathsr@microsoft.com> - 1.4.3-1
- Bring in v1.4.3 version of libadwaita into Mariner
- Required for rest package.
- Remove the creation of the lang packages
- Disabled docs until gi-docgen is a supported package
