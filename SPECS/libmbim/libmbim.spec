Summary:        Library for talking to WWAN modems and devices
Name:           libmbim
Version:        1.26.2
Release:        1%{?dist}
License:        GPLv2
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Applications/System
URL:            https://www.freedesktop.org/wiki/Software/libmbim/
Source0:        https://www.freedesktop.org/software/%{name}/%{name}-%{version}.tar.xz
BuildRequires:  libgudev-devel
Requires:       libgudev

%description
The libmbim package contains a GLib-based library for talking to WWAN modems
and devices which speak the Mobile Interface Broadband Model (MBIM) protocol.

%package    devel
Summary:        Header and development files for libmbim
Requires:       %{name} = %{version}
Requires:       libgudev-devel

%description    devel
It contains the libraries and header files for libmbim

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
%{_libexecdir}/mbim-proxy
%{_bindir}/mbimcli
%{_bindir}/mbim-network
%{_libdir}/libmbim-glib.so*
%exclude %{_libdir}/debug
%{_mandir}/man1/*
%{_datadir}/bash-completion/*

%files devel
%{_includedir}/libmbim-glib/*
%{_libdir}/pkgconfig/mbim-glib.pc
%{_libdir}/libmbim-glib.la
%{_datadir}/gtk-doc/*

%changelog
* Mon Jan 10 2022 Henry Li <lihl@microsoft.com> - 1.26.2-1
- Upgrade to version 1.26.2

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 1.18.2-2
- Added %%license line automatically

*   Tue Mar 17 2020 Henry Beberman <henry.beberman@microsoft.com> 1.18.2-1
-   Update to 1.18.2. URL fixed. Source0 URL fixed. License verified.

*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 1.16.2-2
-   Initial CBL-Mariner import from Photon (license: Apache2).

*   Mon Dec 10 2018 Alexey Makhalov <amakhalov@vmware.com> 1.16.2-1
-   Initial build. First version
