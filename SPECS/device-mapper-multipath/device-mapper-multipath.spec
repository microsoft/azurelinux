Summary:        Provide tools to manage multipath devices
Name:           device-mapper-multipath
Version:        0.9.6
Release:        1%{?dist}
License:        GPLv2
Group:          System Environment/Base
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://github.com/opensvc/multipath-tools
Source0:        https://github.com/opensvc/multipath-tools/archive/refs/tags/%{version}.tar.gz#/multipath-tools-%{version}.tar.gz
BuildRequires:  userspace-rcu-devel
BuildRequires:  libaio-devel
BuildRequires:  device-mapper-devel
BuildRequires:  readline-devel
BuildRequires:  ncurses-devel
BuildRequires:  systemd-devel
BuildRequires:  json-c-devel

Requires:   userspace-rcu
Requires:   libaio
Requires:   device-mapper
Requires:   libselinux
Requires:   libsepol
Requires:   readline
Requires:   ncurses
Requires:   kpartx = %{version}-%{release}


%description
Device-mapper-multipath provides tools to manage multipath devices by
instructing the device-mapper multipath kernel module what to do.

%package -n kpartx
Summary:        Partition device manager for device-mapper devices
Requires:       device-mapper

%description -n kpartx
kpartx manages partition creation and removal for device-mapper devices.

%package devel
Summary:        Development libraries and headers for %{name}
Requires:       %{name} = %{version}-%{release}

%description devel
It contains the libraries and header files to create applications

%prep
%autosetup  -p1 -n multipath-tools-%{version}

%build
make %{?_smp_mflags} CC="gcc %{optflags} $LDFLAGS -Wno-error=sign-compare"

%install
make install DESTDIR=%{buildroot} \
   SYSTEMDPATH=%{_libdir} \
   bindir=%{_sbindir} \
   syslibdir=%{_libdir} \
   usrlibdir=%{_libdir} \
   plugindir=%{_libdir}/multipath \
   includedir=%{_includedir} \
   pkgconfdir=%{_libdir}/pkgconfig \
   mandir=%{_mandir} \
   tmpfilesdir=%{_tmpfilesdir}

install -vd %{buildroot}%{_sysconfdir}/multipath

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%license COPYING
%{_sbindir}/mpathpersist
%{_sbindir}/multipath
%{_sbindir}/multipathc
%{_sbindir}/multipathd
%{_udevrulesdir}/*
%{_unitdir}/*
%{_libdir}/*.so
%{_libdir}/*.so.*
%{_libdir}/multipath/*.so
%{_mandir}/man5/*
%{_mandir}/man8/mpathpersist*
%{_mandir}/man8/multipath*
%dir %{_sysconfdir}/multipath
%{_tmpfilesdir}/multipath.conf
%dir %{_libdir}/modules-load.d
%{_libdir}/modules-load.d/multipath.conf

%files devel
%defattr(-,root,root,-)
%{_mandir}/man3/*
%{_includedir}/*
%{_libdir}/pkgconfig/*

%files -n kpartx
%defattr(-,root,root,-)
%{_sbindir}/kpartx
%{_libdir}/udev/kpartx_id
%{_libdir}/udev/rules.d/*
%{_mandir}/man8/kpartx.8*

%changelog
* Thu Nov 09 2023 Nicolas Guibourge <nicolasg@microsoft.com> - 0.9.6-1
- Upgrade to 0.9.6 - Azure Linux 3.0 - package upgrades

* Wed Sep 20 2023 Jon Slobodzian <joslobo@microsoft.com> - 0.8.6-5
- Recompile with stack-protection fixed gcc version (CVE-2023-4039)

* Wed Dec 14 2022 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 0.8.6-4
- Get patches to fix CVE-2022-41973, CVE-2022-41974 from Fedora 36

* Thu Dec 16 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.8.6-3
- Removing the explicit %%clean stage.

* Fri Nov 12 2021 Andrew Phelps <anphel@microsoft.com> 0.8.6-2
- Fix gcc11 build error

* Thu Apr 29 2021 Andrew Phelps <anphel@microsoft.com> 0.8.6-1
- Update to version 0.8.6 for parallel build fix.
- Update Source0 URL.

* Tue Nov 03 2020 Ruying Chen <v-ruyche@microsoft.com> - 0.8.4-3
- Systemd supports merged /usr. Update with corresponding file locations and macros.

* Wed Jun 17 2020 Joe Schmitt <joschmit@microsoft.com> 0.8.4-2
- Update Source0 URL.
- Use release tag instead of commit.

* Thu Jun 11 2020 Nicolas Ontiveros <niontive@microsoft.com> 0.8.4-1
- Upgrade to version 0.8.4

* Tue May 26 2020 Pawel Winogrodzki <pawelwi@microsoft.com> 0.8.0-2
- Adding the "%%license" macro.

* Wed Mar 25 2020 Nicolas Ontiveros <niontive@microsoft.com> 0.8.0-1
- Update version to 0.8.0. License verified.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 0.7.3-4
- Initial CBL-Mariner import from Photon (license: Apache2).

* Thu Dec 06 2018 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 0.7.3-3
- Make device-mapper a runtime dependency of kpartx.

* Wed Sep 26 2018 Anish Swaminathan <anishs@vmware.com>  0.7.3-2
- Remove rados dependency

* Wed Oct 04 2017 Dheeraj Shetty <dheerajs@vmware.com> 0.7.3-1
- Update to 0.7.3

* Tue May 9  2017 Bo Gan <ganb@vmware.com> 0.7.1-1
- Update to 0.7.1

* Fri Nov 18 2016 Anish Swaminathan <anishs@vmware.com>  0.5.0-3
- Change systemd dependency

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.5.0-2
- GA - Bump release of all rpms

* Mon Jun 22 2015 Divya Thaluru <dthaluru@vmware.com> 0.5.0-1
- Initial build. First version
