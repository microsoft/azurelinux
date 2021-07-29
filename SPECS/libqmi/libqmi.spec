Summary:        Library for talking to WWAN modems and devices
Name:           libqmi
Version:        1.22.4
Release:        2%{?dist}
URL:            https://www.freedesktop.org/wiki/Software/libqmi/
Source0:        https://www.freedesktop.org/software/%{name}/%{name}-%{version}.tar.xz
License:        GPLv2+
Group:          Applications/System
Vendor:         Microsoft Corporation
Distribution:   Mariner
BuildRequires:  libmbim-devel
Requires:       libmbim
%description
The libqmi package contains a GLib-based library for talking to WWAN modems
and devices which speak the Qualcomm MSM Interface (QMI) protocol.

%package    devel
Summary:    Header and development files for libqmi
Requires:   %{name} = %{version}
Requires:   libmbim-devel
%description    devel
It contains the libraries and header files for libqmi

%prep
%setup -q

%build
%configure --disable-static
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
%{_libexecdir}/qmi-proxy
%{_bindir}/qmicli
%{_bindir}/qmi-network
%{_bindir}/qmi-firmware-update
%{_libdir}/libqmi-glib.so*
%exclude %{_libdir}/debug
%{_mandir}/man1/*
%{_datadir}/bash-completion/*

%files devel
%{_includedir}/libqmi-glib/*
%{_libdir}/pkgconfig/qmi-glib.pc
%{_libdir}/libqmi-glib.la
%{_datadir}/gtk-doc/*

%changelog
* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 1.22.4-2
- Added %%license line automatically

*   Tue Mar 17 2020 Henry Beberman <henry.beberman@microsoft.com> 1.22.4-1
-   Update to 1.22.4. Fix URL. License verified.
*   Wed Mar 11 2020 Christopher Co <chrco@microsoft.com> 1.20.2-5
-   Updated Source URL
*   Wed Mar 11 2020 Christopher Co <chrco@microsoft.com> 1.20.2-4
-   Updated hash
*   Fri Mar 06 2020 Jon Slobodzian <joslobo@microsoft.com> 1.20.2-3
-   Fixed Source URL. Verified license.
*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 1.20.2-2
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Mon Dec 10 2018 Alexey Makhalov <amakhalov@vmware.com> 1.20.2-1
-   Initial build. First version
