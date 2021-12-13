Vendor:         Microsoft Corporation
Distribution:   Mariner
# -*- rpm-spec -*-

%define with_introspection 1

%define with_vala %{with_introspection}

%define libvirt_version 1.2.5

Name: libvirt-glib
Version: 3.0.0
Release: 3%{?dist}
Summary: libvirt glib integration for events
License: LGPLv2+
URL: http://libvirt.org/
Source0: ftp://libvirt.org/libvirt/glib/%{name}-%{version}.tar.gz

BuildRequires: glib2-devel >= 2.38.0
BuildRequires: libvirt-devel >= %{libvirt_version}
%if %{with_introspection}
BuildRequires: gobject-introspection-devel


%endif
BuildRequires: libxml2-devel
# Hack due to https://bugzilla.redhat.com/show_bug.cgi?id=613466
BuildRequires: libtool
%if %{with_vala}
BuildRequires: vala
%endif
BuildRequires: intltool

%package devel
Summary: libvirt glib integration for events development files
Requires: %{name} = %{version}-%{release}

%package -n libvirt-gconfig
Summary: libvirt object APIs for processing object configuration

%package -n libvirt-gobject
Summary: libvirt object APIs for managing virtualization hosts

%package -n libvirt-gconfig-devel
Summary: libvirt object APIs for processing object configuration development files
Requires: libvirt-gconfig = %{version}-%{release}

%package -n libvirt-gobject-devel
Summary: libvirt object APIs for managing virtualization hosts development files
Requires: %{name}-devel = %{version}-%{release}
Requires: libvirt-gconfig-devel = %{version}-%{release}
Requires: libvirt-gobject = %{version}-%{release}
Requires: libvirt-devel >=  %{libvirt_version}

%description
This package provides integration between libvirt and the glib
event loop.

%description devel
This package provides development header files and libraries for
integration between libvirt and the glib event loop.

%description -n libvirt-gconfig
This package provides APIs for processing the object configuration
data

%description -n libvirt-gconfig-devel
This package provides development header files and libraries for
the object configuration APIs.

%description -n libvirt-gobject
This package provides APIs for managing virtualization host
objects

%description -n libvirt-gobject-devel
This package provides development header files and libraries for
managing virtualization host objects

%prep
%setup -q

%build

%if %{with_introspection}
%define introspection_arg --enable-introspection
%else
%define introspection_arg --disable-introspection
%endif

%configure %{introspection_arg}
%__make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
%__make install  DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/libvirt-glib-1.0.a
rm -f $RPM_BUILD_ROOT%{_libdir}/libvirt-glib-1.0.la
rm -f $RPM_BUILD_ROOT%{_libdir}/libvirt-gconfig-1.0.a
rm -f $RPM_BUILD_ROOT%{_libdir}/libvirt-gconfig-1.0.la
rm -f $RPM_BUILD_ROOT%{_libdir}/libvirt-gobject-1.0.a
rm -f $RPM_BUILD_ROOT%{_libdir}/libvirt-gobject-1.0.la

%find_lang %{name}

%check
if ! make %{?_smp_mflags} check; then
  cat tests/test-suite.log || true
  exit 1
fi

%ldconfig_scriptlets

%ldconfig_scriptlets -n libvirt-gconfig

%ldconfig_scriptlets -n libvirt-gobject

%files -f %{name}.lang
%doc README COPYING AUTHORS ChangeLog NEWS
%{_libdir}/libvirt-glib-1.0.so.*
%if %{with_introspection}
%{_libdir}/girepository-1.0/LibvirtGLib-1.0.typelib
%endif

%files -n libvirt-gconfig
%{_libdir}/libvirt-gconfig-1.0.so.*
%if %{with_introspection}
%{_libdir}/girepository-1.0/LibvirtGConfig-1.0.typelib
%endif

%files -n libvirt-gobject
%{_libdir}/libvirt-gobject-1.0.so.*
%if %{with_introspection}
%{_libdir}/girepository-1.0/LibvirtGObject-1.0.typelib
%endif

%files devel
%doc examples/event-test.c
%{_libdir}/libvirt-glib-1.0.so
%{_libdir}/pkgconfig/libvirt-glib-1.0.pc
%dir %{_includedir}/libvirt-glib-1.0
%dir %{_includedir}/libvirt-glib-1.0/libvirt-glib
%{_includedir}/libvirt-glib-1.0/libvirt-glib/libvirt-glib.h
%{_includedir}/libvirt-glib-1.0/libvirt-glib/libvirt-glib-*.h
%if %{with_introspection}
%{_datadir}/gir-1.0/LibvirtGLib-1.0.gir
%endif
%{_datadir}/gtk-doc/html/Libvirt-glib
%if %{with_vala}
%{_datadir}/vala/vapi/libvirt-glib-1.0.vapi
%endif

%files -n libvirt-gconfig-devel
%doc examples/event-test.c
%{_libdir}/libvirt-gconfig-1.0.so
%{_libdir}/pkgconfig/libvirt-gconfig-1.0.pc
%dir %{_includedir}/libvirt-gconfig-1.0
%dir %{_includedir}/libvirt-gconfig-1.0/libvirt-gconfig
%{_includedir}/libvirt-gconfig-1.0/libvirt-gconfig/libvirt-gconfig.h
%{_includedir}/libvirt-gconfig-1.0/libvirt-gconfig/libvirt-gconfig-*.h
%if %{with_introspection}
%{_datadir}/gir-1.0/LibvirtGConfig-1.0.gir
%endif
%{_datadir}/gtk-doc/html/Libvirt-gconfig
%if %{with_vala}
%{_datadir}/vala/vapi/libvirt-gconfig-1.0.vapi
%endif

%files -n libvirt-gobject-devel
%doc examples/event-test.c
%{_libdir}/libvirt-gobject-1.0.so
%{_libdir}/pkgconfig/libvirt-gobject-1.0.pc
%dir %{_includedir}/libvirt-gobject-1.0
%dir %{_includedir}/libvirt-gobject-1.0/libvirt-gobject
%{_includedir}/libvirt-gobject-1.0/libvirt-gobject/libvirt-gobject.h
%{_includedir}/libvirt-gobject-1.0/libvirt-gobject/libvirt-gobject-*.h
%if %{with_introspection}
%{_datadir}/gir-1.0/LibvirtGObject-1.0.gir
%endif
%{_datadir}/gtk-doc/html/Libvirt-gobject
%if %{with_vala}
%{_datadir}/vala/vapi/libvirt-gobject-1.0.deps
%{_datadir}/vala/vapi/libvirt-gobject-1.0.vapi
%endif

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.0.0-3
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Nov 26 2019 Daniel P. Berrangé <berrange@redhat.com> - 3.0.0-1
- Update to 3.0.0 release

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Feb 04 2019 Kalev Lember <klember@redhat.com> - 2.0.0-3
- Update BRs for vala packaging changes

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Oct 12 2018 Daniel P. Berrangé <berrange@redhat.com> - 2.0.0-1
- Update to 2.0.0 release

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Oct 30 2017 Marek Kasik <mkasik@redhat.com> - 1.0.0-5
- Enable unit tests
- Resolves: #1502639

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Nov  4 2016 Daniel P. Berrange <berrange@redhat.com> - 1.0.0-1
- Update to 1.0.0 release

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild
