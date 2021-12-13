Name:		keybinder3
Version:	0.3.2
Release:	10%{?dist}
Summary:	A library for registering global keyboard shortcuts
License:	MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:		https://github.com/kupferlauncher/keybinder
Source0:	%{url}/releases/download/keybinder-3.0-v%{version}/keybinder-3.0-%{version}.tar.gz
Patch0:     %{url}/pull/18.patch#/fix_gtkdoc.patch

BuildRequires:	pkgconfig(gtk+-3.0), gnome-common, gtk-doc, gobject-introspection-devel

%description
Keybinder is a library for registering global keyboard shortcuts. 
Keybinder works with GTK-based applications using the X Window System.

The library contains:
- A C library, libkeybinder
- Gobject-Introspection bindings

%package devel
Summary: Development files for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
%description devel
This package contains the development files for %{name}.

%package doc
Summary: Documentation for %{name}
BuildArch: noarch
Requires: %{name} = %{version}-%{release}
%description doc
This package contains documentation for %{name}.

%prep
%autosetup -p1 -n keybinder-3.0-%{version}

%build
%configure --enable-gtk-doc
%make_build

%install
%make_install

rm -rf %{buildroot}/%{_libdir}/libkeybinder-3.0.la

%ldconfig_scriptlets

%files
%license COPYING
%doc NEWS AUTHORS README
%{_libdir}/libkeybinder-3.0.so.*
%{_libdir}/girepository-1.0/Keybinder-3.0.typelib

%files devel
%dir %{_includedir}/keybinder-3.0/
%{_includedir}/keybinder-3.0/keybinder.h
%{_libdir}/pkgconfig/keybinder-3.0.pc
%{_libdir}/libkeybinder-3.0.so
%{_datadir}/gir-1.0/Keybinder-3.0.gir

%files doc
%dir %{_datadir}/gtk-doc/html/keybinder-3.0/
%{_datadir}/gtk-doc/html/keybinder-3.0/*

%changelog
* Wed Aug 25 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.3.2-10
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Removing 'Requires' on 'devhelp' from the 'doc'.
  We don't provide 'devhelp' and one can use a browser instead.

* Tue Apr 14 2020 Leigh Scott <leigh123linux@gmail.com> - 0.3.2-9
- Fix FTBFS

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Feb 28 2017 Patrick Griffis <tingping@tingping.se> - 0.3.2-0
- Bump version and cleanup

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jul 22 2014 Kalev Lember <kalevlember@gmail.com> - 0.3.0-3
- Rebuilt for gobject-introspection 1.41.4

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Aug 1 2013 TingPing <tingping@tingping.se> - 0.3.0-1
- Initial Package

