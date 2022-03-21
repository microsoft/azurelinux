Summary:        libvirt glib integration for events
Name:           libvirt-glib
Version:        4.0.0
Release:        4%{?dist}
License:        LGPLv2+
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://libvirt.org/
Source0:        https://libvirt.org/sources/glib/%{name}-%{version}.tar.xz
Patch1:         %{name}-%{version}-cast-align.patch

BuildRequires:  gettext
BuildRequires:  glib2-devel
BuildRequires:  gobject-introspection-devel
BuildRequires:  gtk-doc
BuildRequires:  libvirt-devel
BuildRequires:  libxml2-devel
BuildRequires:  meson
BuildRequires:  vala

%description
This package provides integration between libvirt and the glib
event loop.

%package devel
Summary:        libvirt glib integration for events development files
Requires:       %{name} = %{version}-%{release}

%description devel
This package provides development header files and libraries for
integration between libvirt and the glib event loop.

%package -n libvirt-gconfig
Summary:        libvirt object APIs for processing object configuration

%description -n libvirt-gconfig
This package provides APIs for processing the object configuration
data

%package -n libvirt-gobject
Summary:        libvirt object APIs for managing virtualization hosts

%description -n libvirt-gobject
This package provides APIs for managing virtualization host
objects

%package -n libvirt-gconfig-devel
Summary:        libvirt object APIs for processing object configuration development files
Requires:       libvirt-gconfig = %{version}-%{release}

%description -n libvirt-gconfig-devel
This package provides development header files and libraries for
the object configuration APIs.

%package -n libvirt-gobject-devel
Summary:        libvirt object APIs for managing virtualization hosts development files
Requires:       %{name}-devel = %{version}-%{release}
Requires:       libvirt-devel
Requires:       libvirt-gconfig-devel = %{version}-%{release}
Requires:       libvirt-gobject = %{version}-%{release}

%description -n libvirt-gobject-devel
This package provides development header files and libraries for
managing virtualization host objects

%prep
%autosetup -p1

%build
%meson -Drpath=disabled
%meson_build

%install
%meson_install

%find_lang %{name}

%check
%meson_test

%ldconfig_scriptlets

%ldconfig_scriptlets -n libvirt-gconfig

%ldconfig_scriptlets -n libvirt-gobject

%files -f %{name}.lang
%license COPYING
%doc README AUTHORS NEWS
%{_libdir}/libvirt-glib-1.0.so.*
%{_libdir}/girepository-1.0/LibvirtGLib-1.0.typelib

%files -n libvirt-gconfig
%license COPYING
%{_libdir}/libvirt-gconfig-1.0.so.*
%{_libdir}/girepository-1.0/LibvirtGConfig-1.0.typelib

%files -n libvirt-gobject
%license COPYING
%{_libdir}/libvirt-gobject-1.0.so.*
%{_libdir}/girepository-1.0/LibvirtGObject-1.0.typelib

%files devel
%doc examples/event-test.c
%{_libdir}/libvirt-glib-1.0.so
%{_libdir}/pkgconfig/libvirt-glib-1.0.pc
%dir %{_includedir}/libvirt-glib-1.0
%dir %{_includedir}/libvirt-glib-1.0/libvirt-glib
%{_includedir}/libvirt-glib-1.0/libvirt-glib/libvirt-glib.h
%{_includedir}/libvirt-glib-1.0/libvirt-glib/libvirt-glib-*.h
%{_datadir}/gir-1.0/LibvirtGLib-1.0.gir
%{_datadir}/gtk-doc/html/Libvirt-glib
%{_datadir}/vala/vapi/libvirt-glib-1.0.deps
%{_datadir}/vala/vapi/libvirt-glib-1.0.vapi

%files -n libvirt-gconfig-devel
%doc examples/event-test.c
%{_libdir}/libvirt-gconfig-1.0.so
%{_libdir}/pkgconfig/libvirt-gconfig-1.0.pc
%dir %{_includedir}/libvirt-gconfig-1.0
%dir %{_includedir}/libvirt-gconfig-1.0/libvirt-gconfig
%{_includedir}/libvirt-gconfig-1.0/libvirt-gconfig/libvirt-gconfig.h
%{_includedir}/libvirt-gconfig-1.0/libvirt-gconfig/libvirt-gconfig-*.h
%{_datadir}/gir-1.0/LibvirtGConfig-1.0.gir
%{_datadir}/gtk-doc/html/Libvirt-gconfig
%{_datadir}/vala/vapi/libvirt-gconfig-1.0.deps
%{_datadir}/vala/vapi/libvirt-gconfig-1.0.vapi

%files -n libvirt-gobject-devel
%doc examples/event-test.c
%{_libdir}/libvirt-gobject-1.0.so
%{_libdir}/pkgconfig/libvirt-gobject-1.0.pc
%dir %{_includedir}/libvirt-gobject-1.0
%dir %{_includedir}/libvirt-gobject-1.0/libvirt-gobject
%{_includedir}/libvirt-gobject-1.0/libvirt-gobject/libvirt-gobject.h
%{_includedir}/libvirt-gobject-1.0/libvirt-gobject/libvirt-gobject-*.h
%{_datadir}/gir-1.0/LibvirtGObject-1.0.gir
%{_datadir}/gtk-doc/html/Libvirt-gobject
%{_datadir}/vala/vapi/libvirt-gobject-1.0.deps
%{_datadir}/vala/vapi/libvirt-gobject-1.0.vapi

%changelog
* Wed Jan 05 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 4.0.0-4
- Initial CBL-Mariner import from Fedora 36 (license: MIT).
- License verified.

* Mon Aug 23 2021 Kalev Lember <klember@redhat.com> - 4.0.0-3
- BR vala instead of vala-tools

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Feb 15 2021 Daniel P. Berrangé <berrange@redhat.com> - 4.0.0-1
- Rebased to 4.0.0 release

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild
