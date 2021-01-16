Summary:        Mobile broadband modem manager
Name:           ModemManager
Version:        1.10.4
Release:        3%{?dist}
URL:            https://www.freedesktop.org/wiki/Software/ModemManager/
Source0:        https://www.freedesktop.org/software/%{name}/%{name}-%{version}.tar.xz
License:        GPLv2
Group:          Applications/System
Vendor:         Microsoft Corporation
Distribution:   Mariner

BuildRequires:  libqmi-devel
BuildRequires:  gobject-introspection-devel
%if %{with_check}
BuildRequires:  dbus-glib
%endif

Requires:       libqmi
Requires:       gobject-introspection

%description
ModemManager provides a unified high level API for communicating
with mobile broadband modems, regardless of the protocol used to
communicate with the actual device.

%package    devel
Summary:    Header and development files for ModemManager
Requires:   %{name} = %{version}
Requires:   libqmi-devel
Requires:   gobject-introspection-devel
%description    devel
It contains the libraries and header files for ModemManager

%prep
%setup -q

%build
%configure --disable-static --enable-more-warnings=no
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install

%check
make  %{?_smp_mflags} check

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%license COPYING
%{_sysconfdir}/dbus-1/system.d/org.freedesktop.ModemManager1.conf
%{_bindir}/mmcli
%{_sbindir}/ModemManager
%{_libdir}/libmm-glib.so*
%{_libdir}/girepository-1.0/ModemManager-1.0.typelib
%{_libdir}/ModemManager/*
%exclude %{_libdir}/debug
%{_mandir}/man1/mmcli.1.gz
%{_mandir}/man8/ModemManager.8.gz
%{_datadir}/dbus-1/*
%{_datadir}/locale/*
%{_datadir}/bash-completion/*
%{_datadir}/gir-1.0/ModemManager-1.0.gir
%exclude %{_datadir}/icons
%exclude %{_datadir}/ModemManager/mm-dell-dw5821e-carrier-mapping.conf
/lib/udev/rules.d/*

%files devel
%{_includedir}/ModemManager/*
%{_includedir}/libmm-glib/*
%{_libdir}/pkgconfig/ModemManager.pc
%{_libdir}/pkgconfig/mm-glib.pc
%{_libdir}/libmm-glib.la

%changelog
*   Fri Jan 15 2021 Andrew Phelps <anphel@microsoft.com> 1.10.4-3
-   Add dbus BuildRequires to fix check tests.
*   Sat May 09 2020 Nick Samson <nisamson@microsoft.com> 1.10.4-2
-   Added %%license line automatically
*   Tue Mar 17 2020 Henry Beberman <henry.beberman@microsoft.com> 1.10.4-1
-   Update to 1.10.4. Fix URL. Fix Source0 URL. Licence verified.
*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 1.8.2-2
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Mon Dec 10 2018 Alexey Makhalov <amakhalov@vmware.com> 1.8.2-1
-   Initial build. First version
