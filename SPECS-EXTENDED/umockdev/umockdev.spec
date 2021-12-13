Vendor:         Microsoft Corporation
Distribution:   Mariner
Name:             umockdev
Version:          0.14
Release:          2%{?dist}
Summary:          Mock hardware devices

License:          LGPLv2+
URL:              https://github.com/martinpitt/%{name}
Source0:          https://github.com/martinpitt/%{name}/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildRequires:    autoconf automake libtool
BuildRequires:    gtk-doc
BuildRequires:    gobject-introspection-devel
BuildRequires:    glib2-devel
BuildRequires:    systemd-devel
BuildRequires:    vala
BuildRequires:    chrpath
# Required for tests
BuildRequires:    gphoto2
BuildRequires:    python3

%description
With this program and libraries you can easily create mock udev objects.
This is useful for writing tests for software which talks to
hardware devices.

%package devel
Summary: Development packages for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
The %{name}-devel package contains the libraries to develop
using %{name}.

%prep
%setup -q -n %{name}-%{version}

%build
NOCONFIGURE=1 ./autogen.sh
%configure --disable-static --enable-gtk-doc

make %{?_smp_mflags}

%install

make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"

#nuke the .la file(s)
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

# Remove rpath
chrpath --delete %{buildroot}%{_bindir}/umockdev-record \
	%{buildroot}%{_bindir}/umockdev-run
chrpath --delete %{buildroot}%{_libdir}/libumockdev.so.*
chrpath --delete %{buildroot}%{_libdir}/libumockdev-preload.so.*

rm -rf $RPM_BUILD_ROOT/%{_datadir}/doc/umockdev

%check

# Disabled for now, as the Xorg tests don't pass
# https://github.com/martinpitt/umockdev/issues/47
# make check

%ldconfig_scriptlets

%files
%license COPYING
%doc README.rst
%{_bindir}/umockdev-*
%{_libdir}/libumockdev.so.*
%{_libdir}/libumockdev-preload.so.*
%{_libdir}/girepository-1.0/UMockdev-1.0.typelib

%files devel
%doc docs/script-format.txt docs/examples/battery.c docs/examples/battery.py
%{_libdir}/libumockdev.so
%{_libdir}/pkgconfig/umockdev-1.0.pc
%{_datadir}/gir-1.0/UMockdev-1.0.gir
%{_includedir}/umockdev-1.0
%{_datadir}/gtk-doc/html/umockdev/
%{_datadir}/vala/vapi/umockdev-1.0.vapi

%changelog
* Fri Mar 26 2021 Henry Li <lihl@microsoft.com> - 0.14-2
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Remove libgudev1-devel to disable circular dependency

* Sun Feb 09 2020 Bastien Nocera <bnocera@redhat.com> - 0.14-1
+ umockdev-0.14-1
- Fix FTBS (#1800217)

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.13.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Sep 02 2019 Bastien Nocera <bnocera@redhat.com> - 0.13.2-1
+ umockdev-0.13.2-1
- Update to 0.13.2 (#1747088)

* Mon Aug 19 2019 Bastien Nocera <bnocera@redhat.com> - 0.13.1-1
+ umockdev-0.13.1-1
- Update to 0.13.1 (#1742178)

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.12.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed May 29 2019 Christian Kellner <ckellner@redhat.com> - 0.12.1-1
- Update to umockdev-0.12.1

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.11.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.11.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jun 06 2018 Bastien Nocera <bnocera@redhat.com> - 0.11.3-1
+ umockdev-0.11.3-1
- Update to 0.11.3 (#1550306)

* Wed Mar 28 2018 Bastien Nocera <bnocera@redhat.com> - 0.11.2-1
+ umockdev-0.11.2-1
- Update to 0.11.2 (#1550306)

* Thu Mar 01 2018 Bastien Nocera <bnocera@redhat.com> - 0.11.1-1
+ umockdev-0.11.1-1
- Update to 0.11.1

* Mon Feb 12 2018 Bastien Nocera <bnocera@redhat.com> - 0.11-1
+ umockdev-0.11-1
- Update to 0.11 (#1544128)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Jan 08 2018 Fedora Release Monitoring  <release-monitoring@fedoraproject.org> - 0.10-1
- Update to 0.10 (#1490889)

* Thu Aug 10 2017 Bastien Nocera <bnocera@redhat.com> - 0.9.2-1
- Update to 0.9.2

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.13-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.13-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Jan 26 2017 Bastien Nocera <bnocera@redhat.com> - 0.8.13-1
+ umockdev-0.8.13-1
- Update to 0.8.13

* Tue Jan 24 2017 Bastien Nocera <bnocera@redhat.com> - 0.8.12-1
+ umockdev-0.8.12-1
- Update to 0.8.12

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Sep 23 2015 Bastien Nocera <bnocera@redhat.com> 0.8.11-1
- Update to 0.8.11

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Apr 29 2015 Bastien Nocera <bnocera@redhat.com> 0.8.8-3
- Fix license/doc mixup
- Add isa to Requires

* Wed Apr 29 2015 Bastien Nocera <bnocera@redhat.com> 0.8.8-2
- Review comments

* Mon Apr 27 2015 Bastien Nocera <bnocera@redhat.com> 0.8.8-1
- Initial package for Fedora
