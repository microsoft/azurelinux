Summary:        Mobile broadband modem manager
Name:           ModemManager
Version:        1.18.12
Release:        1%{?dist}
License:        GPLv2+
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Applications/System
URL:            https://www.freedesktop.org/wiki/Software/ModemManager/
Source0:        https://www.freedesktop.org/software/%{name}/%{name}-%{version}.tar.xz
BuildRequires:  gobject-introspection-devel
BuildRequires:  libqmi-devel
BuildRequires:  systemd-devel
%if %{with_check}
BuildRequires:  dbus-glib
BuildRequires:  python3-gobject
BuildRequires:  python3-dbus
%endif
Requires:       glib
Requires:       gobject-introspection
Requires:       libqmi
Provides:       %{name}-glib = %{version}-%{release}

%description
ModemManager provides a unified high level API for communicating
with mobile broadband modems, regardless of the protocol used to
communicate with the actual device.

%package    devel
Summary:        Header and development files for ModemManager
Requires:       %{name} = %{version}
Requires:       glib-devel
Requires:       gobject-introspection-devel
Requires:       libqmi-devel
Provides:       %{name}-glib-devel = %{version}-%{release}

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
%{_datadir}/ModemManager/*
%{_unitdir}/*
%exclude %{_datadir}/icons
/lib/udev/rules.d/*

%files devel
%{_includedir}/ModemManager/*
%{_includedir}/libmm-glib/*
%{_libdir}/pkgconfig/ModemManager.pc
%{_libdir}/pkgconfig/mm-glib.pc
%{_libdir}/libmm-glib.la

%changelog
* Fri Oct 27 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.18.12-1
- Auto-upgrade to 1.18.12 - Azure Linux 3.0 - package upgrades

* Tue Mar 22 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.18.6-3
- Adding missing systemd service file to the default package.

* Mon Feb 28 2022 Max Brodeur-Urbas <maxbr@microsoft.com> - 1.18.6-2
- Adding python3-gobject, python3-dbus check BRs to satisfy regressed ptest.

* Fri Feb 18 2022 Max Brodeur-Urbas <maxbr@microsoft.com> - 1.18.6-1
- Upgrading to v1.18.6
- License verified.

* Fri Mar 26 2021 Thomas Crain <thcrain@microsoft.com> - 1.10.4-4
- Merge the following releases from 1.0 to dev branch
- anphel@microsoft.com, 1.10.4-3: Add dbus BuildRequires to fix check tests.

* Fri Dec 11 2020 Joe Schmitt <joschmit@microsoft.com> - 1.10.4-3
- Provide ModemManager-glib and ModemManager-glib-devel.

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 1.10.4-2
- Added %%license line automatically

*   Tue Mar 17 2020 Henry Beberman <henry.beberman@microsoft.com> 1.10.4-1
-   Update to 1.10.4. Fix URL. Fix Source0 URL. Licence verified.

*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 1.8.2-2
-   Initial CBL-Mariner import from Photon (license: Apache2).

*   Mon Dec 10 2018 Alexey Makhalov <amakhalov@vmware.com> 1.8.2-1
-   Initial build. First version
